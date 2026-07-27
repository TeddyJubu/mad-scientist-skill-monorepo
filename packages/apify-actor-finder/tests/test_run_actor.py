"""Offline tests for safe CSV delivery."""

from __future__ import annotations

import csv
import importlib.util
import tempfile
import unittest
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


if __name__ == "__main__":
    unittest.main()
