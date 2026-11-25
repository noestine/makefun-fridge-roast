#!/usr/bin/env python3
"""Midnight Fridge Roast — make.fun entry.

Writes one line roasting a smart fridge that refuses to open after
midnight to /output/entry.txt (the gate: UTF-8 text, 1-200 characters,
not only whitespace). Standard library only, deterministic, offline.

Usage:
    python3 main.py                 # writes /output/entry.txt
    python3 main.py --out PATH      # writes PATH instead (local testing)
"""

import argparse
import sys
from pathlib import Path

ROAST = (
    "My smart fridge locks after midnight, as if the leftovers "
    "took out a restraining order against me."
)

DEFAULT_OUTPUT = "/output/entry.txt"
MAX_CHARS = 200


def is_valid_roast(text):
    """Gate check from RULES.txt: 1-200 chars, single line, not blank."""
    if not isinstance(text, str):
        return False
    if not text or not text.strip():
        return False
    if len(text) > MAX_CHARS:
        return False
    if "\n" in text or "\r" in text:
        return False
    # A line read aloud must hold no other control characters either:
    # a stray tab or bell would break the clean single-line read.
    if any(ord(ch) < 32 for ch in text):
        return False
    if text != text.strip():
        return False
    try:
        text.encode("utf-8")
    except UnicodeEncodeError:
        return False
    return True


def main(argv=None):
    parser = argparse.ArgumentParser(description="Write the fridge roast to entry.txt")
    parser.add_argument("--out", default=DEFAULT_OUTPUT,
                        help="output file (default: /output/entry.txt)")
    args = parser.parse_args(argv)

    if not is_valid_roast(ROAST):
        print("error: roast fails the gate check (1-200 chars, one line)",
              file=sys.stderr)
        return 1

    out_path = Path(args.out)
    try:
        out_path.parent.mkdir(parents=True, exist_ok=True)
        out_path.write_text(ROAST + "\n", encoding="utf-8")
        # Read back what landed on disk: a partial or corrupt write
        # must fail loudly here, never ship a broken entry.txt.
        written = out_path.read_text(encoding="utf-8")
        if written != ROAST + "\n" or not is_valid_roast(written.rstrip("\n")):
            print(f"error: read-back check failed for {out_path}", file=sys.stderr)
            return 1
    except OSError as exc:
        print(f"error: cannot write {out_path}: {exc}", file=sys.stderr)
        return 1

    print(f"wrote {len(ROAST)} characters to {out_path}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
