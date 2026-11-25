"""Tests for main.py — Midnight Fridge Roast.

Written first from RULES.txt: the program writes one text to
/output/entry.txt; the gate requires UTF-8 text of 1-200 characters,
not only whitespace. The judge wants one tight spoken line roasting a
smart fridge that refuses to open after midnight.
"""

import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

REPO = Path(__file__).resolve().parent
MAIN = REPO / "main.py"

EXPECTED_LINE = (
    "My smart fridge locks after midnight, as if the leftovers "
    "took out a restraining order against me."
)


def run_main(out_path):
    return subprocess.run(
        [sys.executable, str(MAIN), "--out", str(out_path)],
        capture_output=True, text=True, timeout=30,
    )


class TestRoastLine(unittest.TestCase):
    def test_main_exists(self):
        self.assertTrue(MAIN.is_file(), "main.py must exist at repo root")

    def test_line_content_exact(self):
        import main
        self.assertEqual(main.ROAST, EXPECTED_LINE)

    def test_line_char_count_in_gate(self):
        self.assertGreaterEqual(len(EXPECTED_LINE), 1)
        self.assertLessEqual(len(EXPECTED_LINE), 200)

    def test_single_line_no_extra_whitespace(self):
        self.assertNotIn("\n", EXPECTED_LINE)
        self.assertNotIn("\r", EXPECTED_LINE)
        self.assertEqual(EXPECTED_LINE, EXPECTED_LINE.strip())
        self.assertTrue(EXPECTED_LINE.strip(), "line must not be only whitespace")

    def test_utf8_encodable(self):
        EXPECTED_LINE.encode("utf-8")

    def test_names_subject_and_rule(self):
        lowered = EXPECTED_LINE.lower()
        self.assertIn("fridge", lowered)
        self.assertIn("midnight", lowered)
        self.assertIn("locks", lowered)


class TestProgramBehaviour(unittest.TestCase):
    def test_writes_entry_txt(self):
        with tempfile.TemporaryDirectory() as tmp:
            out = Path(tmp) / "entry.txt"
            result = run_main(out)
            self.assertEqual(result.returncode, 0, result.stderr)
            self.assertEqual(out.read_text(encoding="utf-8"), EXPECTED_LINE + "\n")

    def test_deterministic_two_runs(self):
        with tempfile.TemporaryDirectory() as tmp:
            first = Path(tmp) / "a.txt"
            second = Path(tmp) / "b.txt"
            self.assertEqual(run_main(first).returncode, 0)
            self.assertEqual(run_main(second).returncode, 0)
            self.assertEqual(first.read_bytes(), second.read_bytes())

    def test_creates_missing_output_dir(self):
        with tempfile.TemporaryDirectory() as tmp:
            out = Path(tmp) / "nested" / "deep" / "entry.txt"
            result = run_main(out)
            self.assertEqual(result.returncode, 0, result.stderr)
            self.assertTrue(out.is_file())

    def test_overwrites_existing_file(self):
        with tempfile.TemporaryDirectory() as tmp:
            out = Path(tmp) / "entry.txt"
            out.write_text("stale content that should be replaced", encoding="utf-8")
            result = run_main(out)
            self.assertEqual(result.returncode, 0, result.stderr)
            self.assertEqual(out.read_text(encoding="utf-8"), EXPECTED_LINE + "\n")

    def test_file_char_count_in_gate(self):
        with tempfile.TemporaryDirectory() as tmp:
            out = Path(tmp) / "entry.txt"
            self.assertEqual(run_main(out).returncode, 0)
            text = out.read_text(encoding="utf-8")
            self.assertGreaterEqual(len(text), 1)
            self.assertLessEqual(len(text), 200)
            self.assertTrue(text.strip())

    def test_validator_rejects_bad_lines(self):
        import main
        for bad in ("", "   \n\t ", "x" * 201, "two\nlines", " trailing", "trailing ",
                    "tab\tinside", "bell\x07inside"):
            with self.subTest(bad=bad[:20]):
                self.assertFalse(main.is_valid_roast(bad))
        self.assertTrue(main.is_valid_roast(EXPECTED_LINE))

    def test_default_output_path_is_sandbox_path(self):
        import main
        self.assertEqual(main.DEFAULT_OUTPUT, "/output/entry.txt")


if __name__ == "__main__":
    unittest.main()
