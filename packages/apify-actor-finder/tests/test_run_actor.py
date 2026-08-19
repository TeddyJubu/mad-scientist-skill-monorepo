"""Offline tests for safe CSV delivery."""

from __future__ import annotations

import csv
import http.client
import importlib.util
import io
import tempfile
import unittest
from contextlib import redirect_stderr, redirect_stdout
from pathlib import Path
from unittest.mock import patch

RUNNER_PATH = Path(__file__).parents[1] / "scripts" / "run_actor.py"
SPEC = importlib.util.spec_from_file_location("actor_finder_runner", RUNNER_PATH)
if SPEC is None or SPEC.loader is None:
    raise RuntimeError(f"Cannot load {RUNNER_PATH}")
run_actor = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(run_actor)


class FakeResponse:
    """Return CSV content without a network request."""

    def __enter__(self):
        return self

    def __exit__(self, *_args):
        return False

    def read(self):
        return b"name,note,value\nalice,=1+1,-2\nbob,safe,@command\n"


class SafeCsvTests(unittest.TestCase):
    def test_start_run_uses_exact_pricing_ceiling(self):
        cases = (
            (20, None, {"waitForFinish": 60, "maxItems": 20}),
            (None, "1.25", {"waitForFinish": 60, "maxTotalChargeUsd": "1.25"}),
        )
        for max_items, max_charge, expected_params in cases:
            with (
                self.subTest(expected_params=expected_params),
                patch.object(
                    run_actor,
                    "apify_post",
                    return_value={"data": {"id": "run-1"}},
                ) as post,
            ):
                result = run_actor.start_run(
                    "secret-token",
                    "xquik~x-tweet-scraper",
                    {"maxItems": 2},
                    max_items,
                    max_charge,
                )

            self.assertEqual(result, {"id": "run-1"})
            post.assert_called_once_with(
                "secret-token",
                "/actors/xquik~x-tweet-scraper/runs",
                {"maxItems": 2},
                expected_params,
            )

    def test_start_run_rejects_missing_or_conflicting_pricing_caps(self):
        for max_items, max_charge in ((None, None), (20, "1.25")):
            with (
                self.subTest(max_items=max_items, max_charge=max_charge),
                self.assertRaisesRegex(ValueError, "exactly one"),
            ):
                run_actor.start_run("token", "actor", {}, max_items, max_charge)
        with self.assertRaises(run_actor.argparse.ArgumentTypeError):
            run_actor.positive_item_cap("0")
        with self.assertRaises(run_actor.argparse.ArgumentTypeError):
            run_actor.positive_charge_cap("NaN")

    def test_download_csv_neutralizes_spreadsheet_formulas(self):
        with tempfile.TemporaryDirectory() as directory:
            output = Path(directory) / "results.csv"
            with patch.object(
                run_actor.urllib.request,
                "urlopen",
                return_value=FakeResponse(),
            ) as urlopen:
                count = run_actor.download_csv(
                    "secret-token",
                    "dataset-1",
                    str(output),
                )

            with output.open(newline="", encoding="utf-8") as file:
                rows = list(csv.reader(file))

        self.assertEqual(count, 2)
        self.assertEqual(rows[1], ["alice", "'=1+1", "'-2"])
        self.assertEqual(rows[2], ["bob", "safe", "'@command"])
        request = urlopen.call_args.args[0]
        self.assertEqual(
            request.get_header("Authorization"),
            "Bearer secret-token",
        )
        self.assertEqual(
            urlopen.call_args.kwargs["timeout"],
            run_actor.HTTP_TIMEOUT,
        )

    def test_neutralizer_handles_leading_spaces(self):
        self.assertEqual(
            run_actor.neutralize_spreadsheet_formula("  +SUM(A1:A2)"),
            "'  +SUM(A1:A2)",
        )
        self.assertEqual(
            run_actor.neutralize_spreadsheet_formula("ordinary"),
            "ordinary",
        )

    def test_main_handles_incomplete_dataset_response(self):
        run = {
            "id": "run-1",
            "defaultDatasetId": "dataset-1",
            "status": "SUCCEEDED",
        }
        stderr = io.StringIO()
        with (
            patch.object(
                run_actor.sys,
                "argv",
                [
                    "run_actor.py",
                    "secret-token",
                    "xquik~x-tweet-scraper",
                    '{"maxItems": 2}',
                    "--max-total-charge-usd",
                    "1.25",
                ],
            ),
            patch.object(run_actor, "start_run", return_value=run) as start_run,
            patch.object(
                run_actor,
                "download_csv",
                side_effect=http.client.IncompleteRead(b"", 1),
            ) as download_csv,
            redirect_stdout(io.StringIO()),
            redirect_stderr(stderr),
            self.assertRaises(SystemExit) as raised,
        ):
            run_actor.main()

        self.assertEqual(raised.exception.code, 1)
        self.assertIn("Error downloading results", stderr.getvalue())
        start_run.assert_called_once_with(
            "secret-token",
            "xquik~x-tweet-scraper",
            {"maxItems": 2},
            None,
            "1.25",
        )
        download_csv.assert_called_once_with(
            "secret-token",
            "dataset-1",
            "apify_results.csv",
        )


if __name__ == "__main__":
    unittest.main()
