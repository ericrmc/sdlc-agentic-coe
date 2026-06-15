#!/usr/bin/env python3
"""push_portfolio_to_board.py — project the advisory RAG onto the org Project board.

This is the *projection* half of the portfolio-rollup Action (compute_portfolio_rollup.py
is the compute half). It reads the throwaway rollup JSON and, for each tracked
downstream project, sets that project's card fields on the org-level GitHub Project
(Projects v2): **Phase**, **RAG** (the advisory standing), and **Reasons** (every
firing check).

DESIGN — why this is a safe, dry-run-by-default stub
----------------------------------------------------
* **PURE PROJECTION, never a gate.** It overwrites a board cell with a recomputed
  value (a cache of a derived-on-read fact, per docs/portfolio-github-projects.md).
  It stores no score and decides nothing.
* **DRY-RUN BY DEFAULT.** Out of the box it *echoes* the projection it would make and
  exits 0 — so a scheduled CI run is green with no org token, no ``gh`` CLI, and no
  network. You opt into real writes with ``--apply``.
* **Advisory jobs never hard-fail a schedule.** If ``--apply`` is set but ``gh`` is
  absent or ``GH_TOKEN`` is unset (the default GITHUB_TOKEN cannot see org Projects —
  see the workflow PREREQUISITE), it prints a warning and exits 0, it does not crash.
* Writing to an *org-level* Project needs a fine-grained PAT / App token with
  "Projects: read & write" (stored as PORTFOLIO_PROJECT_TOKEN). The actual
  ``gh project item-edit`` calls are sketched here and gated behind ``--apply`` so
  the wiring is documented and runnable without standing up that token first.

Usage
-----
    # dry run (default): echo the projection, write nothing, always green
    python scripts/push_portfolio_to_board.py --rollup generated/portfolio-rollup.json \
        --owner your-org --number 1

    # real write (requires gh + a PORTFOLIO_PROJECT_TOKEN with org project scope)
    python scripts/push_portfolio_to_board.py --rollup generated/portfolio-rollup.json \
        --owner your-org --number 1 --apply
"""

from __future__ import annotations

import argparse
import json
import os
import shutil
import sys
from pathlib import Path

_THIS = Path(__file__).resolve()
REPO_ROOT = _THIS.parents[1]
DEFAULT_ROLLUP = REPO_ROOT / "generated" / "portfolio-rollup.json"

_RAG_ICON = {"red": "🔴", "amber": "🟡", "green": "🟢"}


def _load_rollup(path: Path) -> list[dict]:
    if not path.exists():
        print(f"::warning::rollup {path} not found — nothing to project", file=sys.stderr)
        return []
    try:
        data = json.loads(path.read_text(encoding="utf-8"))
    except Exception as exc:
        print(f"::warning::could not read rollup {path}: {exc}", file=sys.stderr)
        return []
    return data.get("projects", []) if isinstance(data, dict) else []


def _projection_lines(projects: list[dict], owner: str, number: str) -> list[str]:
    """Render the human-readable projection (what each card's fields become)."""
    lines = [f"Org Project board: owner={owner} number={number}", ""]
    if not projects:
        lines.append("  (no tracked projects in the rollup)")
        return lines
    for p in projects:
        standing = p.get("standing", "?")
        reasons = "; ".join(p.get("reasons", [])) or "—"
        lines.append(
            f"  {_RAG_ICON.get(standing, '')} {p.get('name', '?')}  "
            f"→ Phase={p.get('phase', '?')}  RAG={standing}  Reasons=\"{reasons}\""
        )
    return lines


def _apply_to_board(projects: list[dict], owner: str, number: str) -> int:
    """Real projection path (gated behind --apply). Advisory: never hard-fails."""
    if shutil.which("gh") is None:
        print(
            "::warning::`gh` CLI not found — skipping board write (advisory job, not "
            "failing). Install gh or run without --apply for a dry run.",
            file=sys.stderr,
        )
        return 0
    if not os.environ.get("GH_TOKEN"):
        print(
            "::warning::GH_TOKEN not set — skipping board write (advisory job, not "
            "failing). Needs a token with org 'Projects: read & write' "
            "(PORTFOLIO_PROJECT_TOKEN); the default GITHUB_TOKEN cannot see org "
            "Projects. See the workflow PREREQUISITE.",
            file=sys.stderr,
        )
        return 0

    # The real write would resolve each tracked project's board item id, then set its
    # Phase / RAG / Reasons single-select + text fields, e.g.:
    #
    #   gh project item-edit --id <ITEM_ID> --project-id <PROJECT_ID> \
    #       --field-id <RAG_FIELD_ID> --single-select-option-id <opt-for-standing>
    #   gh project item-edit --id <ITEM_ID> --project-id <PROJECT_ID> \
    #       --field-id <REASONS_FIELD_ID> --text "<reasons joined>"
    #
    # Item/field id resolution (`gh project item-list`, `gh project field-list`) is
    # left to a follow-up so this stub stays runnable without a live org board; the
    # field contract is fixed in docs/portfolio-github-projects.md.
    import subprocess  # local import: only needed on the real-write path

    written = 0
    for p in projects:
        name = p.get("name", "?")
        # Verify connectivity once per project without mutating anything yet.
        proc = subprocess.run(
            ["gh", "project", "view", str(number), "--owner", owner, "--format", "json"],
            capture_output=True,
            text=True,
        )
        if proc.returncode != 0:
            print(
                f"::warning::could not read org Project {owner}#{number} for "
                f"{name!r} (advisory, not failing): {proc.stderr.strip()}",
                file=sys.stderr,
            )
            return 0
        # Real field writes go here once item/field ids are resolved (see above).
        print(f"  would set fields for {name!r} on {owner}#{number}")
        written += 1
    print(f"projected {written} project(s) onto {owner}#{number}.")
    return 0


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument(
        "--rollup",
        type=Path,
        default=Path(os.environ.get("ROLLUP_OUT", str(DEFAULT_ROLLUP))),
        help="rollup JSON written by compute_portfolio_rollup.py",
    )
    parser.add_argument("--owner", default=os.environ.get("PROJECT_OWNER", "your-org"))
    parser.add_argument("--number", default=os.environ.get("PROJECT_NUMBER", "1"))
    parser.add_argument(
        "--apply",
        action="store_true",
        help="actually write the org Project board (default: dry-run echo only). "
        "Requires gh + a PORTFOLIO_PROJECT_TOKEN with org project scope.",
    )
    args = parser.parse_args(argv)

    rollup = args.rollup if args.rollup.is_absolute() else REPO_ROOT / args.rollup
    projects = _load_rollup(rollup)

    mode = "APPLY" if args.apply else "DRY-RUN"
    print(f"push_portfolio_to_board [{mode}]")
    for line in _projection_lines(projects, args.owner, args.number):
        print(line)

    if not args.apply:
        print("\nDry run — wrote nothing. Pass --apply to project onto the board.")
        return 0

    print()
    return _apply_to_board(projects, args.owner, args.number)


if __name__ == "__main__":
    raise SystemExit(main())
