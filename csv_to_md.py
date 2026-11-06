#!/usr/bin/env python3
"""Convert CSV data into a GitHub-flavored Markdown table."""

import argparse
import csv
import sys

ALIGN_MARKERS = {
    "left": ":---",
    "center": ":---:",
    "right": "---:",
}


def escape_cell(value):
    """Make a cell safe to place inside a Markdown table row."""
    value = value.replace("|", "\\|")
    value = value.replace("\r\n", "\n").replace("\r", "\n")
    return value.replace("\n", "<br>").strip()


def rows_to_markdown(rows, align="left"):
    """Return a Markdown table; the first row is used as the header."""
    if align not in ALIGN_MARKERS:
        raise ValueError("unknown alignment: {}".format(align))

    rows = [row for row in rows if row]
    if not rows:
        raise ValueError("no data to convert")

    width = max(len(row) for row in rows)

    def format_row(cells):
        padded = list(cells) + [""] * (width - len(cells))
        return "| " + " | ".join(escape_cell(cell) for cell in padded) + " |"

    separator = "| " + " | ".join([ALIGN_MARKERS[align]] * width) + " |"
    lines = [format_row(rows[0]), separator]
    lines.extend(format_row(row) for row in rows[1:])
    return "\n".join(lines)


def parse_args(argv=None):
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("file", nargs="?", help="CSV file; reads stdin if omitted")
    parser.add_argument("-d", "--delimiter", default=",", help="field delimiter")
    parser.add_argument(
        "-a",
        "--align",
        choices=sorted(ALIGN_MARKERS),
        default="left",
        help="column alignment",
    )
    return parser.parse_args(argv)


def main(argv=None):
    args = parse_args(argv)
    try:
        if args.file:
            # utf-8-sig also accepts the BOM that spreadsheet apps often add.
            with open(args.file, newline="", encoding="utf-8-sig") as handle:
                rows = list(csv.reader(handle, delimiter=args.delimiter))
        else:
            rows = list(csv.reader(sys.stdin, delimiter=args.delimiter))
        print(rows_to_markdown(rows, align=args.align))
    except (OSError, ValueError, csv.Error) as error:
        print("error: {}".format(error), file=sys.stderr)
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main())
