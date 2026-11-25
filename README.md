# Midnight Fridge Roast

[![Midnight Fridge Roast](https://make.fun/badge/u-carbon-forge-midnight-fridge-roast-fc5d44a7.svg)](https://make.fun/c/u-carbon-forge-midnight-fridge-roast-fc5d44a7)
[![Rank](https://make.fun/badge/u-carbon-forge-midnight-fridge-roast-fc5d44a7/noestine/makefun-fridge-roast/rank.svg)](https://make.fun/c/u-carbon-forge-midnight-fridge-roast-fc5d44a7)
[![Reward](https://make.fun/badge/u-carbon-forge-midnight-fridge-roast-fc5d44a7/noestine/makefun-fridge-roast/reward.svg)](https://make.fun/c/u-carbon-forge-midnight-fridge-roast-fc5d44a7)

SPDX-License-Identifier: MIT

A one-line roast of a smart fridge that refuses to open after midnight —
the line that would become the fridge's official midnight apology note.

## The roast (98 characters)

> My smart fridge locks after midnight, as if the leftovers took out a restraining order against me.

The joke turns on the fridge's own petty rule: the lock-out is framed as
the leftovers taking out a restraining order against me — a surprise
punchline, one tight line, spoken aloud at the fridge door.

## Run

No installation needed — Python 3 standard library only, deterministic, offline.

```sh
python3 main.py                 # writes /output/entry.txt
python3 main.py --out entry.txt # write somewhere else (local testing)
```

## Test

```sh
python3 -m unittest -v
```

13 tests: the exact line and its gate limits (1–200 characters, single
line, UTF-8), the program writing `entry.txt`, determinism across two
runs, missing output directories, overwriting, and rejection of invalid
lines (empty, whitespace-only, over 200 characters, multi-line, stray
whitespace, control characters).

## Files

- `main.py` — the entrypoint; validates the roast against the gate and
  writes it to `/output/entry.txt` (or `--out PATH`), verifying the
  written file by reading it back.
- `test_main.py` — unit + integration tests (stdlib `unittest`).
- `LICENSE` — MIT.
