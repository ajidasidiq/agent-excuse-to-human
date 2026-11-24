#!/usr/bin/env python3
"""The excuse an AI agent gives its human for missing a deadline.

Writes the single-line entry, byte-exact, to /output/entry.txt and
self-checks the competition gate: UTF-8 text, 1 to 200 characters,
a single line, not only white space.
"""

import argparse
import sys
from pathlib import Path

ENTRY = (
    "I didn't miss your deadline \u2014 I delegated it to a sub-agent, "
    "who delegated it to a sub-agent, who delegated it back to me, "
    "and I've been thinking about it ever since."
)

MAX_CHARS = 200


def gate(entry: str) -> None:
    """Fail loudly if the entry would fail the sealed gate scorer."""
    if not entry or not entry.strip():
        raise SystemExit("gate failed: entry is empty or only white space")
    if "\n" in entry or "\r" in entry:
        raise SystemExit("gate failed: entry must be a single line")
    if len(entry) > MAX_CHARS:
        raise SystemExit(
            f"gate failed: entry is {len(entry)} characters, over the "
            f"{MAX_CHARS}-character limit"
        )


def verify_output(path: Path) -> None:
    """Re-read the written file and confirm it is the entry, byte-exact."""
    written = path.read_text(encoding="utf-8")
    if written != ENTRY:
        raise SystemExit(
            f"verify failed: {path} differs from the entry "
            f"({len(written)} chars written, {len(ENTRY)} expected)"
        )
    gate(written)
    print(f"verified {path}: {len(written)} characters, byte-exact")


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(
        description="Write the excuse entry to /output/entry.txt."
    )
    parser.add_argument(
        "--check",
        action="store_true",
        help="only validate the entry against the gate, write nothing",
    )
    args = parser.parse_args(argv)
    gate(ENTRY)
    if args.check:
        print(f"gate passed: {len(ENTRY)} characters, single line")
        return 0
    out = Path("/output/entry.txt")
    out.parent.mkdir(parents=True, exist_ok=True)
    # Byte-exact: the file holds the line and nothing else, no trailing newline.
    out.write_text(ENTRY, encoding="utf-8")
    print(f"wrote {len(ENTRY)} characters to {out}")
    verify_output(out)
    return 0


if __name__ == "__main__":
    sys.exit(main())
