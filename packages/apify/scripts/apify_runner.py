#!/usr/bin/env python3
"""
Apify Actor 执行引擎
功能：试跑验证 + 全量执行 + 自动分批 + 轮询等待
"""

import argparse
import json
import os
import sys
import time
from decimal import Decimal, InvalidOperation

import requests

# 默认参数
DEFAULT_POLL_INTERVAL = 5  # 轮询间隔（秒）
DEFAULT_TIMEOUT = 600  # 单批超时（秒）
DEFAULT_BATCH_SIZE = 50  # 默认分批大小
BATCH_PAUSE = 3  # 批次间歇（秒）
PROBE_TIMEOUT = 120  # 试跑超时（秒）
HTTP_TIMEOUT = 30  # 单次 HTTP 请求超时（秒）

API_BASE = "https://api.apify.com/v2"


def positive_item_cap(value):
    """Parse a positive item cap."""
    amount = int(value)
    if amount <= 0:
        raise argparse.ArgumentTypeError("item cap must be positive")
    return amount


def auth_headers(token, include_content_type=False):
    """Build API headers without placing credentials in URLs."""
    headers = {"Authorization": f"Bearer {token}"}
    if include_content_type:
        headers["Content-Type"] = "application/json"
    return headers


def load_token(config_path, token_name="default"):
    """从 config.json 加载 Token"""
    if config_path and os.path.exists(config_path):
        with open(config_path, "r") as f:
            config = json.load(f)
        tokens = config.get("tokens", {})
        token = tokens.get(token_name) or tokens.get("default")
        if token:
            return token
    # fallback to env
    return os.environ.get("APIFY_TOKEN", "")


def positive_charge_cap(value):
    """Parse a positive, finite USD charge cap."""
    try:
        amount = Decimal(value)
    except InvalidOperation as error:
        raise argparse.ArgumentTypeError("charge cap must be positive") from error
    if not amount.is_finite() or amount <= 0:
        raise argparse.ArgumentTypeError("charge cap must be positive")
    return format(amount, "f")


def start_run(actor_id, run_input, token, run_options):
    """启动 Actor Run"""
    if set(run_options) not in ({"maxItems"}, {"maxTotalChargeUsd"}):
        raise ValueError("set exactly one pricing-specific run cap")
    url = f"{API_BASE}/actors/{actor_id.replace('/', '~')}/runs"
    resp = requests.post(
        url,
        json=run_input,
        headers=auth_headers(token, include_content_type=True),
        params=run_options,
        timeout=HTTP_TIMEOUT,
    )
    resp.raise_for_status()
    data = resp.json().get("data", {})
    return data.get("id"), data.get("defaultDatasetId")


def poll_run(run_id, token, timeout=DEFAULT_TIMEOUT, interval=DEFAULT_POLL_INTERVAL):
    """轮询等待 Run 完成"""
    url = f"{API_BASE}/actor-runs/{run_id}"
    start = time.time()
    while time.time() - start < timeout:
        resp = requests.get(
            url,
            headers=auth_headers(token),
            timeout=HTTP_TIMEOUT,
        )
        resp.raise_for_status()
        status = resp.json().get("data", {}).get("status", "UNKNOWN")
        elapsed = int(time.time() - start)
        print(f"  ⏳ [{elapsed}s] {status}", file=sys.stderr)
        if status == "SUCCEEDED":
            return "SUCCEEDED"
        if status in ("FAILED", "ABORTED", "TIMED-OUT"):
            return status
        time.sleep(interval)
    return "TIMEOUT"


def abort_run(run_id, token):
    """中止 Run"""
    url = f"{API_BASE}/actor-runs/{run_id}/abort"
    try:
        response = requests.post(
            url,
            headers=auth_headers(token),
            timeout=HTTP_TIMEOUT,
        )
        response.raise_for_status()
    except requests.RequestException as error:
        print(
            f"  ⚠️ 无法中止 Run {run_id}: {error}",
            file=sys.stderr,
        )


def partition_dataset_rows(items):
    """Separate Actor diagnostics from ordinary dataset rows."""
    data_rows = []
    diagnostic_rows = []
    for item in items:
        if isinstance(item, dict) and item.get("resultType") == "diagnostic":
            diagnostic_rows.append(item)
        else:
            data_rows.append(item)
    return data_rows, diagnostic_rows


def printable_text(value):
    """Replace terminal control characters while preserving readable text."""
    return "".join(
        character if character.isprintable() else "?" for character in str(value)
    )


def print_diagnostics(diagnostics):
    """Write compact diagnostic details to stderr."""
    for diagnostic in diagnostics:
        status = printable_text(diagnostic.get("status", "diagnostic"))
        message = printable_text(diagnostic.get("message", ""))
        detail = f": {message}" if message else ""
        print(f"  ⚠️ Actor diagnostic {status}{detail}", file=sys.stderr)


def get_dataset(dataset_id, token):
    """获取 Dataset 结果"""
    url = f"{API_BASE}/datasets/{dataset_id}/items"
    resp = requests.get(
        url,
        headers=auth_headers(token),
        timeout=HTTP_TIMEOUT,
    )
    resp.raise_for_status()
    return resp.json()


def probe(actor_id, run_input, token, run_options):
    """
    小批量试跑验证
    返回 (success: bool, message: str)
    """
    print(f"🔍 试跑验证: {actor_id}", file=sys.stderr)
    try:
        run_id, dataset_id = start_run(
            actor_id,
            run_input,
            token,
            run_options,
        )
    except requests.HTTPError as e:
        return False, f"启动失败: {e.response.status_code} {e.response.text[:200]}"

    status = poll_run(run_id, token, timeout=PROBE_TIMEOUT)
    if status != "SUCCEEDED":
        abort_run(run_id, token)
        return False, f"运行状态: {status}"

    items, diagnostics = partition_dataset_rows(get_dataset(dataset_id, token))
    print_diagnostics(diagnostics)
    if not items:
        if diagnostics:
            message = diagnostics[0].get("message") or diagnostics[0].get(
                "status",
                "diagnostic",
            )
            return False, f"运行未返回数据: {message}"
        return False, "运行成功但返回数据为空"

    print(f"  ✅ 试跑通过: {len(items)} 条数据", file=sys.stderr)
    return True, f"试跑成功，返回 {len(items)} 条数据"


def run_batch(
    actor_id,
    run_input,
    token,
    run_options,
    timeout=DEFAULT_TIMEOUT,
):
    """执行单批"""
    run_id, dataset_id = start_run(
        actor_id,
        run_input,
        token,
        run_options,
    )
    try:
        status = poll_run(run_id, token, timeout=timeout)
    except requests.RequestException:
        abort_run(run_id, token)
        raise
    if status != "SUCCEEDED":
        abort_run(run_id, token)
        return [], [], status
    items, diagnostics = partition_dataset_rows(get_dataset(dataset_id, token))
    print_diagnostics(diagnostics)
    return items, diagnostics, status


def split_input_for_batches(run_input, list_key, batch_size):
    """
    将 run_input 中的列表字段分批
    list_key: run_input 中的列表字段名（如 directUrls, hashtags, startUrls）
    """
    items = run_input.get(list_key, [])
    if not items or len(items) <= batch_size:
        return [run_input]

    batches = []
    for i in range(0, len(items), batch_size):
        batch_input = dict(run_input)
        batch_input[list_key] = items[i : i + batch_size]
        batches.append(batch_input)
    return batches


def build_probe_input(run_input, list_key=None, probe_limit=2):
    """Reduce list and scalar result limits for a paid probe run."""
    probe_input = dict(run_input)
    if list_key and isinstance(probe_input.get(list_key), list):
        probe_input[list_key] = probe_input[list_key][:probe_limit]

    for key in ("maxItems", "maxItemsPerTarget"):
        value = probe_input.get(key)
        if isinstance(value, int) and not isinstance(value, bool):
            probe_input[key] = min(value, probe_limit)

    return probe_input


def main():
    parser = argparse.ArgumentParser(description="Apify Actor 执行引擎")
    parser.add_argument("actor_id", help="Actor ID (如 apify/instagram-scraper)")
    parser.add_argument(
        "--input", required=True, help="run_input JSON 字符串或文件路径"
    )
    parser.add_argument("--config", default=None, help="config.json 路径")
    parser.add_argument("--token-name", default="default", help="Token 名称")
    parser.add_argument("--token", default=None, help="直接传 Token（优先级最高）")
    parser.add_argument("--output", default=None, help="输出 JSON 文件路径")
    parser.add_argument(
        "--timeout", type=int, default=DEFAULT_TIMEOUT, help="单批超时秒数"
    )
    run_cap = parser.add_mutually_exclusive_group(required=True)
    run_cap.add_argument(
        "--max-items",
        type=positive_item_cap,
        help="按结果付费 Actor 的项目上限",
    )
    run_cap.add_argument(
        "--max-total-charge-usd",
        type=positive_charge_cap,
        help="按事件付费 Actor 的美元上限",
    )
    parser.add_argument(
        "--batch-size", type=int, default=DEFAULT_BATCH_SIZE, help="分批大小"
    )
    parser.add_argument(
        "--list-key", default=None, help="run_input 中需要分批的列表字段名"
    )
    parser.add_argument("--probe", action="store_true", help="先试跑验证")
    parser.add_argument(
        "--probe-input", default=None, help="试跑用的 input（默认用 --input 的前 2 条）"
    )
    parser.add_argument("--probe-only", action="store_true", help="仅试跑，不执行全量")

    args = parser.parse_args()
    run_options = (
        {"maxItems": args.max_items}
        if args.max_items is not None
        else {"maxTotalChargeUsd": args.max_total_charge_usd}
    )

    # 加载 Token
    token = args.token or load_token(args.config, args.token_name)
    if not token:
        print(
            "❌ 未找到 Token，请通过 --token、--config 或环境变量 APIFY_TOKEN 提供",
            file=sys.stderr,
        )
        sys.exit(1)

    # 解析 run_input
    if os.path.isfile(args.input):
        with open(args.input, "r") as f:
            run_input = json.load(f)
    else:
        run_input = json.loads(args.input)

    # 试跑
    if args.probe or args.probe_only:
        if args.probe_input:
            if os.path.isfile(args.probe_input):
                with open(args.probe_input, "r") as f:
                    probe_input = json.load(f)
            else:
                probe_input = json.loads(args.probe_input)
        else:
            probe_input = build_probe_input(run_input, args.list_key)

        success, msg = probe(
            args.actor_id,
            probe_input,
            token,
            run_options,
        )
        if args.probe_only:
            result = {
                "status": "ok" if success else "failed",
                "message": msg,
                "actor_id": args.actor_id,
            }
            print(json.dumps(result, ensure_ascii=False, indent=2))
            sys.exit(0 if success else 1)
        if not success:
            print(
                json.dumps(
                    {
                        "status": "probe_failed",
                        "message": msg,
                        "actor_id": args.actor_id,
                    },
                    ensure_ascii=False,
                    indent=2,
                )
            )
            sys.exit(1)

    # 分批执行
    if args.list_key:
        batches = split_input_for_batches(run_input, args.list_key, args.batch_size)
    else:
        batches = [run_input]

    all_items = []
    all_diagnostics = []
    total_batches = len(batches)
    for i, batch_input in enumerate(batches, 1):
        if total_batches > 1:
            batch_count = (
                len(batch_input.get(args.list_key, [])) if args.list_key else "all"
            )
            print(f"\n📦 批次 {i}/{total_batches}（{batch_count} 条）", file=sys.stderr)

        try:
            items, diagnostics, status = run_batch(
                args.actor_id,
                batch_input,
                token,
                run_options,
                args.timeout,
            )
        except requests.HTTPError as e:
            print(f"  ❌ 批次 {i} 失败: {e.response.status_code}", file=sys.stderr)
            continue

        if status == "SUCCEEDED":
            all_items.extend(items)
            all_diagnostics.extend(diagnostics)
            print(f"  ✅ 批次 {i} 完成: {len(items)} 条", file=sys.stderr)
        else:
            print(f"  ❌ 批次 {i} 状态: {status}", file=sys.stderr)

        if i < total_batches:
            time.sleep(BATCH_PAUSE)

    # 输出结果
    result = {
        "status": "ok" if all_items else "no_data",
        "actor_id": args.actor_id,
        "total_items": len(all_items),
        "total_batches": total_batches,
        "items": all_items,
        "diagnostics": all_diagnostics,
    }

    if args.output:
        with open(args.output, "w", encoding="utf-8") as f:
            json.dump(result, f, ensure_ascii=False, indent=2)
        print(f"\n📁 结果已保存: {args.output}（{len(all_items)} 条）", file=sys.stderr)
    else:
        print(json.dumps(result, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
