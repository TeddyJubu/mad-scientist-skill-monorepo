#!/usr/bin/env python3
"""
run_actor.py - Run an Apify actor with given input and save results to CSV.

Usage:
    python3.11 run_actor.py <api_key> <actor_id> <input_json> [--output path/to/output.csv] [--timeout 300] [--max-items 100]

Arguments:
    api_key     Your Apify API key
    actor_id    Actor ID in the form username~actor-name (e.g. compass~crawler-google-places)
    input_json  JSON string of the actor input (e.g. '{"searchStringsArray": ["coffee Austin"]}')

Options:
    --output    Path to save the CSV file (default: apify_results.csv)
    --timeout   Max seconds to wait for the run to finish (default: 300)
    --max-items Max number of dataset items to charge for (default: 100)

Output:
    Saves results to a CSV file and prints the path.
"""

from __future__ import annotations

import argparse
import csv
import io
import json
import sys
import time
import urllib.error
import urllib.parse
import urllib.request

API_BASE = "https://api.apify.com/v2"
FORMULA_PREFIXES = ("=", "+", "-", "@")


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
    with urllib.request.urlopen(req) as resp:
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
    with urllib.request.urlopen(req) as resp:
        return json.loads(resp.read())


def start_run(api_key: str, actor_id: str, input_data: dict, max_items: int) -> dict:
    """Start an actor run and return the run object."""
    params = {"waitForFinish": 60}
    if max_items:
        params["maxItems"] = max_items
    return apify_post(api_key, f"/acts/{actor_id}/runs", input_data, params)["data"]


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
    with urllib.request.urlopen(req) as resp:
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
    parser.add_argument(
        "--max-items",
        type=int,
        default=100,
        help="Max items to retrieve (default: 100)",
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
        run = start_run(args.api_key, args.actor_id, input_data, args.max_items)
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
    except (OSError, UnicodeError, csv.Error, urllib.error.URLError) as e:
        print(f"Error downloading results: {e}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
