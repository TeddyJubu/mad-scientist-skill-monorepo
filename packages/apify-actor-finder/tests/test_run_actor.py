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
                ],
            ),
            patch.object(run_actor, "start_run", return_value=run),
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
        download_csv.assert_called_once_with(
            "secret-token",
            "dataset-1",
            "apify_results.csv",
        )


if __name__ == "__main__":
    unittest.main()
