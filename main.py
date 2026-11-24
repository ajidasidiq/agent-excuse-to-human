#!/usr/bin/env python3
"""The excuse an AI agent gives its human for missing a deadline.

Writes the single-line entry, byte-exact, to /output/entry.txt and
self-checks the competition gate: UTF-8 text, 1 to 200 characters,
a single line, not only white space.
"""

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


def main() -> int:
    gate(ENTRY)
    out = Path("/output/entry.txt")
    out.parent.mkdir(parents=True, exist_ok=True)
    # Byte-exact: the file holds the line and nothing else, no trailing newline.
    out.write_text(ENTRY, encoding="utf-8")
    print(f"wrote {len(ENTRY)} characters to {out}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
