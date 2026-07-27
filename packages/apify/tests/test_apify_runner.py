"""Offline tests for the Apify runner request contract."""

from __future__ import annotations

import argparse
import importlib.util
import io
import unittest
from contextlib import redirect_stderr
from pathlib import Path
from unittest.mock import patch

RUNNER_PATH = Path(__file__).parents[1] / "scripts" / "apify_runner.py"
SPEC = importlib.util.spec_from_file_location("apify_runner", RUNNER_PATH)
if SPEC is None or SPEC.loader is None:
    raise RuntimeError(f"Cannot load {RUNNER_PATH}")
apify_runner = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(apify_runner)


class FakeResponse:
    """Return a minimal successful Actor run."""

    def raise_for_status(self):
        return None

    def json(self):
        return {
            "data": {
                "id": "run-1",
                "defaultDatasetId": "dataset-1",
            }
        }


class ApifyRunnerTests(unittest.TestCase):
    def test_start_run_uses_headers_and_forwards_hard_charge_cap(self):
        with patch.object(
            apify_runner.requests,
            "post",
            return_value=FakeResponse(),
        ) as post:
            result = apify_runner.start_run(
                "xquik/x-tweet-scraper",
                {"maxItems": 2},
                "secret-token",
                "1.25",
            )

        self.assertEqual(result, ("run-1", "dataset-1"))
        post.assert_called_once_with(
            "https://api.apify.com/v2/actors/xquik~x-tweet-scraper/runs",
            json={"maxItems": 2},
            headers={
                "Authorization": "Bearer secret-token",
                "Content-Type": "application/json",
            },
            params={"maxTotalChargeUsd": "1.25"},
        )

    def test_positive_charge_cap_rejects_invalid_values(self):
        for value in ("not-a-number", "NaN", "0", "-1"):
            with (
                self.subTest(value=value),
                self.assertRaises(argparse.ArgumentTypeError),
            ):
                apify_runner.positive_charge_cap(value)

        self.assertEqual(apify_runner.positive_charge_cap("1.250"), "1.250")

    def test_probe_input_reduces_existing_list_and_scalar_caps(self):
        run_input = {
            "twitterHandles": ["nasa", "esa", "apify"],
            "maxItems": 30,
            "maxItemsPerTarget": 10,
            "outputMode": "compact",
        }

        result = apify_runner.build_probe_input(
            run_input,
            "twitterHandles",
        )

        self.assertEqual(result["twitterHandles"], ["nasa", "esa"])
        self.assertEqual(result["maxItems"], 2)
        self.assertEqual(result["maxItemsPerTarget"], 2)
        self.assertEqual(run_input["maxItems"], 30)

    def test_diagnostic_rows_do_not_make_probe_succeed(self):
        diagnostics = [
            {
                "resultType": "diagnostic",
                "status": "zero-output",
                "message": "No posts found",
            }
        ]

        with (
            patch.object(
                apify_runner,
                "start_run",
                return_value=("run-1", "dataset-1"),
            ),
            patch.object(apify_runner, "poll_run", return_value="SUCCEEDED"),
            patch.object(apify_runner, "get_dataset", return_value=diagnostics),
            redirect_stderr(io.StringIO()),
        ):
            success, message = apify_runner.probe(
                "xquik/x-tweet-scraper",
                {"maxItems": 2},
                "token",
            )

        self.assertFalse(success)
        self.assertIn("No posts found", message)

    def test_abort_logs_request_failures(self):
        stderr = io.StringIO()
        with (
            patch.object(
                apify_runner.requests,
                "post",
                side_effect=apify_runner.requests.RequestException("offline"),
            ),
            redirect_stderr(stderr),
        ):
            apify_runner.abort_run("run-1", "token")

        self.assertIn("run-1", stderr.getvalue())
        self.assertIn("offline", stderr.getvalue())


if __name__ == "__main__":
    unittest.main()
