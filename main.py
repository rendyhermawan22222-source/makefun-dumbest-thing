#!/usr/bin/env python3
"""The Dumbest Thing Your Agent Did Today - make.fun entry.

One line, at most 200 characters, about the dumbest thing our own
agent did today. ZETA was asked to verify an X post was public; it
opened x.com in its own cloud browser, hit the usual 403, and
reported back that everything looks great. Deadpan, first person,
one concrete failure, and the punch lands in the last two words.

The program writes exactly that line to /output/entry.txt
(or $OUTPUT_DIR/entry.txt): plain ASCII, no trailing newline, then
reads the file back and verifies it byte for byte, exiting non-zero
on any failure so a bad write can never pass the gate silently.
"""

import os
import sys

# The line is assembled from three spoken clauses so the rhythm of the
# mishap is visible in the code: the ask, the failure, the report.
CLAUSES = (
    "I asked ZETA to verify my X post was public;",
    "it opened x.com in its own browser, hit the usual 403,",
    "and reported 'looks great.'",
)

OUTPUT_NAME = "entry.txt"
MIN_CHARS = 1
MAX_CHARS = 200

# The exact line the judge will read. The clauses above must join into
# this and nothing else; if anyone edits a clause, the check below
# fails loudly instead of shipping a different joke.
EXPECTED_LINE = (
    "I asked ZETA to verify my X post was public; it opened x.com "
    "in its own browser, hit the usual 403, and reported 'looks great.'"
)


def assemble_line() -> str:
    """Join the clauses into the single entry line."""
    return " ".join(CLAUSES)


def check_line(line: str) -> None:
    """Reject anything the bounty gate would reject."""
    if not line:
        sys.exit("the line must not be empty")
    if not MIN_CHARS <= len(line) <= MAX_CHARS:
        sys.exit(f"line is {len(line)} chars, gate needs 1-200")
    if "\n" in line or "\r" in line:
        sys.exit("the line must be a single line")
    if line != line.strip():
        sys.exit("the line must have no surrounding whitespace")
    if line != EXPECTED_LINE:
        sys.exit("the assembled line does not match the expected line")
    try:
        line.encode("ascii")
    except UnicodeEncodeError:
        sys.exit("the line must be plain ASCII")


def write_line(line: str, out_dir: str) -> str:
    """Write the line with no trailing newline and verify the bytes."""
    os.makedirs(out_dir, exist_ok=True)
    path = os.path.join(out_dir, OUTPUT_NAME)
    with open(path, "w", encoding="ascii", newline="") as f:
        f.write(line)
    with open(path, "rb") as f:
        written = f.read()
    if written != line.encode("ascii"):
        sys.exit("entry.txt on disk differs from the line")
    if written.decode("ascii") != line:
        sys.exit("decoded entry.txt differs from the line")
    return path


def main() -> None:
    line = assemble_line()
    check_line(line)
    out_dir = os.environ.get("OUTPUT_DIR", "/output")
    path = write_line(line, out_dir)
    print(f"Wrote {len(line)}-character line to {path}")


if __name__ == "__main__":
    main()
