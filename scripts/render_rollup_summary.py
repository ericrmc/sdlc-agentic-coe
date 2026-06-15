#!/usr/bin/env python3
"""Render the portfolio rollup JSON as a GitHub job-summary markdown table.

Kept as a standalone script (rather than an inline heredoc in the workflow) so the
YAML block scalar stays valid — a `<<'PY'` heredoc body cannot be dedented to
column 0 inside a `run: |` step without breaking the YAML parse.

Usage: python scripts/render_rollup_summary.py <rollup.json>  # prints markdown to stdout
"""
from __future__ import annotations

import json
import sys

ICON = {"red": "🔴", "amber": "🟡", "green": "🟢"}


def main(path: str) -> int:
    data = json.load(open(path, encoding="utf-8"))
    rows = data.get("projects", [])
    print("| Project | Phase | Standing | Reasons |")
    print("|---|---|---|---|")
    for p in rows:
        reasons = "; ".join(p.get("reasons", [])) or "—"
        standing = p.get("standing", "?")
        print(
            f"| {p.get('name', '?')} | {p.get('phase', '?')} | "
            f"{ICON.get(standing, '')} {standing} | {reasons} |"
        )
    return 0


if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("usage: render_rollup_summary.py <rollup.json>", file=sys.stderr)
        raise SystemExit(2)
    raise SystemExit(main(sys.argv[1]))
