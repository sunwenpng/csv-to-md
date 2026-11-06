import contextlib
import io
import os
import tempfile
import unittest

from csv_to_md import escape_cell, main, rows_to_markdown


class EscapeCellTests(unittest.TestCase):
    def test_escapes_pipe(self):
        self.assertEqual(escape_cell("a|b"), "a\\|b")

    def test_converts_newlines(self):
        self.assertEqual(escape_cell("a\r\nb\nc"), "a<br>b<br>c")


class RowsToMarkdownTests(unittest.TestCase):
    def test_basic_table(self):
        result = rows_to_markdown([["name", "qty"], ["apple", "3"]])
        self.assertEqual(
            result,
            "| name | qty |\n| :--- | :--- |\n| apple | 3 |",
        )

    def test_right_alignment(self):
        result = rows_to_markdown([["a"], ["1"]], align="right")
        self.assertIn("| ---: |", result)

    def test_short_rows_are_padded(self):
        result = rows_to_markdown([["a", "b"], ["1"]])
        self.assertTrue(result.endswith("| 1 |  |"))

    def test_blank_rows_are_skipped(self):
        result = rows_to_markdown([["a"], [], ["1"]])
        self.assertEqual(len(result.splitlines()), 3)

    def test_empty_input_raises(self):
        with self.assertRaises(ValueError):
            rows_to_markdown([])

    def test_unknown_alignment_raises(self):
        with self.assertRaises(ValueError):
            rows_to_markdown([["a"]], align="middle")


class MainTests(unittest.TestCase):
    def test_reads_file_with_bom(self):
        with tempfile.TemporaryDirectory() as folder:
            path = os.path.join(folder, "data.csv")
            with open(path, "w", encoding="utf-8-sig", newline="") as handle:
                handle.write("name,qty\napple,3\n")

            output = io.StringIO()
            with contextlib.redirect_stdout(output):
                code = main([path])

        self.assertEqual(code, 0)
        self.assertTrue(output.getvalue().startswith("| name | qty |"))

    def test_missing_file_returns_error(self):
        errors = io.StringIO()
        with contextlib.redirect_stderr(errors):
            code = main(["does-not-exist.csv"])

        self.assertEqual(code, 1)
        self.assertIn("error:", errors.getvalue())


if __name__ == "__main__":
    unittest.main()
