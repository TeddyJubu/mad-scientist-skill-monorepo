#!/usr/bin/env python3
"""Run an Apify Actor and save its dataset as a formula-safe CSV file."""

from __future__ import annotations

import argparse
import csv
import http.client
import io
import json
import sys
import time
import urllib.error
import urllib.parse
import urllib.request
from decimal import Decimal, InvalidOperation

API_BASE = "https://api.apify.com/v2"
FORMULA_PREFIXES = ("=", "+", "-", "@")
HTTP_TIMEOUT = 90


def positive_item_cap(value: str) -> int:
    """Return a positive item cap."""
    amount = int(value)
    if amount <= 0:
        raise argparse.ArgumentTypeError("item cap must be positive")
    return amount


def positive_charge_cap(value: str) -> str:
    """Return a positive finite USD cap."""
    try:
        amount = Decimal(value)
    except InvalidOperation as error:
        raise argparse.ArgumentTypeError("charge cap must be positive") from error
    if not amount.is_finite() or amount <= 0:
        raise argparse.ArgumentTypeError("charge cap must be positive")
    return format(amount, "f")


def neutralize_spreadsheet_formula(value: str) -> str:
    """Prevent a CSV cell from being interpreted as a spreadsheet formula."""
    if value.lstrip().startswith(FORMULA_PREFIXES):
        return "'" + value
    return value


def apify_get(api_key: str, path: str) -> dict:
    url = f"{API_BASE}{path}"
    req = urllib.request.Request(
        url,
        headers={
            "Authorization": f"Bearer {api_key}",
            "Accept": "application/json",
        },
    )
    with urllib.request.urlopen(req, timeout=HTTP_TIMEOUT) as resp:
        return json.loads(resp.read())


def apify_post(
    api_key: str,
    path: str,
    body: dict,
    params: dict | None = None,
) -> dict:
    qs = ("?" + urllib.parse.urlencode(params)) if params else ""
    url = f"{API_BASE}{path}{qs}"
    payload = json.dumps(body).encode("utf-8")
    req = urllib.request.Request(
        url,
        data=payload,
        headers={
            "Authorization": f"Bearer {api_key}",
            "Content-Type": "application/json",
            "Accept": "application/json",
        },
    )
    with urllib.request.urlopen(req, timeout=HTTP_TIMEOUT) as resp:
        return json.loads(resp.read())


def start_run(
    api_key: str,
    actor_id: str,
    input_data: dict,
    max_items: int | None,
    max_total_charge_usd: str | None,
) -> dict:
    """Start an actor run and return the run object."""
    if (max_items is None) == (max_total_charge_usd is None):
        raise ValueError("set exactly one pricing-specific run cap")
    params = {"waitForFinish": 60}
    if max_items is not None:
        params["maxItems"] = max_items
    else:
        params["maxTotalChargeUsd"] = max_total_charge_usd
    return apify_post(api_key, f"/actors/{actor_id}/runs", input_data, params)["data"]


def wait_for_run(api_key: str, run_id: str, timeout: int = 300) -> dict:
    """Poll until the run reaches a terminal status or timeout."""
    terminal = {"SUCCEEDED", "FAILED", "ABORTED", "TIMED-OUT"}
    deadline = time.time() + timeout
    poll_interval = 5

    while time.time() < deadline:
        run = apify_get(api_key, f"/actor-runs/{run_id}")["data"]
        status = run.get("status", "")
        print(f"  Status: {status}", flush=True)
        if status in terminal:
            return run
        time.sleep(poll_interval)
        poll_interval = min(poll_interval * 1.5, 30)  # back off up to 30s

    raise TimeoutError(f"Run {run_id} did not finish within {timeout} seconds.")


def download_csv(api_key: str, dataset_id: str, output_path: str) -> int:
    """Download dataset items as CSV and save to output_path. Returns item count."""
    url = f"{API_BASE}/datasets/{dataset_id}/items?format=csv&clean=true"
    req = urllib.request.Request(
        url,
        headers={
            "Authorization": f"Bearer {api_key}",
        },
    )
    with urllib.request.urlopen(req, timeout=HTTP_TIMEOUT) as resp:
        content = resp.read()

    source = io.StringIO(content.decode("utf-8-sig"), newline="")
    rows = [
        [neutralize_spreadsheet_formula(cell) for cell in row]
        for row in csv.reader(source)
    ]

    with open(output_path, "w", encoding="utf-8", newline="") as f:
        writer = csv.writer(f, lineterminator="\n")
        writer.writerows(rows)

    return max(0, len(rows) - 1)


def main():
    parser = argparse.ArgumentParser(
        description="Run an Apify actor and save results to CSV."
    )
    parser.add_argument("api_key", help="Apify API key")
    parser.add_argument(
        "actor_id", help="Actor ID (e.g. compass~crawler-google-places)"
    )
    parser.add_argument("input_json", help="JSON string of actor input")
    parser.add_argument(
        "--output", default="apify_results.csv", help="Output CSV file path"
    )
    parser.add_argument(
        "--timeout", type=int, default=300, help="Max seconds to wait (default: 300)"
    )
    run_cap = parser.add_mutually_exclusive_group(required=True)
    run_cap.add_argument(
        "--max-items",
        type=positive_item_cap,
        help="Pay-per-result run ceiling",
    )
    run_cap.add_argument(
        "--max-total-charge-usd",
        type=positive_charge_cap,
        help="Pay-per-event run ceiling in USD",
    )
    args = parser.parse_args()

    try:
        input_data = json.loads(args.input_json)
    except json.JSONDecodeError as e:
        print(f"Error: Invalid JSON input: {e}", file=sys.stderr)
        sys.exit(1)

    print(f"Starting actor: {args.actor_id}")
    print(f"Input: {json.dumps(input_data, indent=2)}")

    try:
        run = start_run(
            args.api_key,
            args.actor_id,
            input_data,
            args.max_items,
            args.max_total_charge_usd,
        )
    except urllib.error.HTTPError as e:
        body = e.read().decode()
        print(f"Error starting run: HTTP {e.code} — {body}", file=sys.stderr)
        sys.exit(1)

    run_id = run["id"]
    dataset_id = run["defaultDatasetId"]
    status = run.get("status", "RUNNING")
    print(f"Run started: {run_id} (initial status: {status})")

    if status not in {"SUCCEEDED", "FAILED", "ABORTED", "TIMED-OUT"}:
        print(f"Waiting for run to finish (timeout: {args.timeout}s)...")
        try:
            run = wait_for_run(args.api_key, run_id, timeout=args.timeout)
        except TimeoutError as e:
            print(f"Warning: {e}", file=sys.stderr)
            print("Downloading partial results...")

    final_status = run.get("status", "UNKNOWN")
    if final_status == "FAILED":
        print(
            "Error: Actor run failed. Check the Apify console for details.",
            file=sys.stderr,
        )
        sys.exit(1)

    print(f"Run finished with status: {final_status}")
    print(f"Downloading results from dataset: {dataset_id}")

    try:
        count = download_csv(args.api_key, dataset_id, args.output)
        print(f"Saved {count} rows to: {args.output}")
    except (
        OSError,
        UnicodeError,
        csv.Error,
        urllib.error.URLError,
        http.client.HTTPException,
    ) as e:
        print(f"Error downloading results: {e}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
