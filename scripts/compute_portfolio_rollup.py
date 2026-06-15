#!/usr/bin/env python3
"""compute_portfolio_rollup.py — derive the advisory portfolio RAG, one project per row.

This is the *compute* half of the portfolio-rollup Action (push_portfolio_to_board.py
is the projection half). It reads the tracked-project registry
(``portfolio/tracked-projects.yml``) and, for each downstream project, recomputes an
**advisory Red/Amber/Green standing** from the SAME transparent checklist the
``skills/library/portfolio-phase-health`` skill documents in
``references/rag-checklist.md``.

Discipline (follows that checklist and docs/portfolio-github-projects.md):

* **Derived-on-read, never a stored score.** The verdict is recomputed from scratch
  every run and written to a *throwaway* JSON artefact (git-ignored). Nothing is a
  persisted grade; nothing here gates anything.
* **Worst-of over a small fixed check set.** ``red if any red else amber if any amber
  else green`` — a transparent boolean fold, never a weighted number.
* **Reasons name every firing check.** ``reasons[]`` is the audit of the verdict.
* **Min-phase gating.** A check only fires at/beyond its min-phase on the
  ``prototype < mvp < pilot < production`` ladder.
* **Advisory facts are surfaced, not scored.** PII / automated-decision / critical-risk
  / roadblock counts ride along on every row but do NOT change the verdict in v1.
* **Degrade safely.** A missing/malformed signal falls back to its safe default; one
  bad project never crashes the rollup or fails another project's verdict.

It is dependency-light: PyYAML is used if importable, else a tiny built-in parser
covers the exact registry shape, so a scheduled CI run is green with or without the
``pip install pyyaml`` step.

Usage
-----
    python scripts/compute_portfolio_rollup.py
    python scripts/compute_portfolio_rollup.py --registry portfolio/tracked-projects.yml \
                                                --out generated/portfolio-rollup.json

Environment (optional, matching the workflow):
    TRACKED_PROJECTS_FILE   overrides the default registry path
    ROLLUP_OUT              overrides the default output path
"""

from __future__ import annotations

import argparse
import datetime as _dt
import json
import os
import sys
from pathlib import Path

# Resolve repo root relative to this file (scripts/ is at the repo root), not CWD,
# so the Action and a local run behave identically.
_THIS = Path(__file__).resolve()
REPO_ROOT = _THIS.parents[1]
DEFAULT_REGISTRY = REPO_ROOT / "portfolio" / "tracked-projects.yml"
DEFAULT_OUT = REPO_ROOT / "generated" / "portfolio-rollup.json"

# The phase ladder. Index drives min-phase gating. Unknown/absent -> prototype (0).
PHASE_ORDER = ["prototype", "mvp", "pilot", "production"]


def _phase_index(phase: str | None) -> int:
    try:
        return PHASE_ORDER.index(str(phase).strip().lower())
    except (ValueError, AttributeError):
        return 0  # default prototype — degrade safely


# ---------------------------------------------------------------------------
# Dependency-light YAML loading for the registry's exact shape.
# ---------------------------------------------------------------------------

def _load_registry(path: Path) -> list[dict]:
    """Return the list of project dicts from the registry, or [] if absent/empty."""
    if not path.exists():
        print(f"::warning::registry {path} not found — empty rollup", file=sys.stderr)
        return []
    text = path.read_text(encoding="utf-8")
    try:
        import yaml  # type: ignore

        data = yaml.safe_load(text) or {}
    except Exception:
        data = _tiny_yaml_projects(text)
    projects = data.get("projects") if isinstance(data, dict) else None
    return projects or []


def _coerce(val: str):
    """Coerce a scalar string to bool/int/str (the only types the registry uses)."""
    low = val.strip().strip("'\"")
    if low.lower() in {"true", "false"}:
        return low.lower() == "true"
    if low.lower() in {"null", "~", ""}:
        return None
    try:
        return int(low)
    except ValueError:
        return low


def _tiny_yaml_projects(text: str) -> dict:
    """A deliberately tiny parser for the exact registry shape we document.

    Supports only::

        projects:
          - name: <scalar>
            key: <scalar>
            ...

    Comments (``#``) and blank lines are skipped. Not a general YAML parser; if the
    registry grows beyond flat scalar fields per project, install PyYAML (the
    workflow already does).
    """
    projects: list[dict] = []
    cur: dict | None = None
    for raw in text.splitlines():
        # Strip trailing inline comments (none of our values contain '#').
        line = raw.split("#", 1)[0].rstrip()
        if not line.strip():
            continue
        stripped = line.strip()
        if stripped == "projects:":
            continue
        if stripped.startswith("- "):
            cur = {}
            projects.append(cur)
            stripped = stripped[2:].strip()  # the first key sits on the dash line
        if cur is None:
            continue
        if ":" in stripped:
            key, _, val = stripped.partition(":")
            cur[key.strip()] = _coerce(val)
    return {"projects": projects}


# ---------------------------------------------------------------------------
# The checklist — mirrors references/rag-checklist.md exactly.
# ---------------------------------------------------------------------------

def _get_int(proj: dict, key: str, default: int = 0) -> int:
    v = proj.get(key, default)
    try:
        return int(v)
    except (TypeError, ValueError):
        return default


def _get_bool(proj: dict, key: str, default: bool = False) -> bool:
    v = proj.get(key, default)
    return bool(v) if isinstance(v, bool) else default


def evaluate_project(proj: dict) -> dict:
    """Apply the named checks and return one rollup row (verdict + reasons + facts).

    Every read degrades to a safe default; this function never raises on a row.
    """
    name = str(proj.get("name", "?"))
    phase = str(proj.get("phase", "prototype")).strip().lower()
    if phase not in PHASE_ORDER:
        phase = "prototype"
    pidx = _phase_index(phase)

    red: list[str] = []
    amber: list[str] = []

    # --- RED checks ---
    # gate_sent_back: any phase (prototype always).
    if _get_bool(proj, "gate_sent_back"):
        red.append("Advisory gate sent back")
    # required_checks_open: min-phase pilot (index 2).
    open_required = _get_int(proj, "open_required_checks")
    if pidx >= PHASE_ORDER.index("pilot") and open_required > 0:
        red.append(f"{open_required} required advisory check(s) open")

    # --- AMBER checks ---
    # record_incomplete: min-phase production (index 3).
    if pidx >= PHASE_ORDER.index("production") and not _get_bool(
        proj, "record_complete", default=True
    ):
        amber.append("Record incomplete at production")
    # decisions_drafted: min-phase mvp (index 1).
    drafted = _get_int(proj, "drafted_decisions")
    if pidx >= PHASE_ORDER.index("mvp") and drafted > 0:
        amber.append(f"{drafted} decision(s) still drafted")
    # design_drift: any phase (prototype always).
    open_reconcile = _get_int(proj, "open_reconcile_proposals")
    if open_reconcile > 0:
        amber.append("Design drift (reconcile proposals open)")

    standing = "red" if red else ("amber" if amber else "green")
    reasons = red + amber  # severity order: reds first

    # Advisory facts — surfaced, NEVER scored into the verdict in v1.
    facts = {
        "open_critical_risks": _get_int(proj, "open_critical_risks"),
        "open_roadblocks": _get_int(proj, "open_roadblocks"),
        "has_pii": _get_bool(proj, "has_pii"),
        "has_automated_decision": _get_bool(proj, "has_automated_decision"),
    }

    return {
        "name": name,
        "repo": proj.get("repo"),
        "phase": phase,
        "standing": standing,
        "reasons": reasons,
        "facts": facts,
    }


def build_rollup(projects: list[dict]) -> dict:
    rows = []
    for proj in projects:
        if not isinstance(proj, dict):
            continue
        try:
            rows.append(evaluate_project(proj))
        except Exception as exc:  # degrade safely — one bad row never sinks the run
            name = proj.get("name", "?") if isinstance(proj, dict) else "?"
            print(f"::warning::skipped malformed project {name!r}: {exc}", file=sys.stderr)
    summary = {
        "red": sum(1 for r in rows if r["standing"] == "red"),
        "amber": sum(1 for r in rows if r["standing"] == "amber"),
        "green": sum(1 for r in rows if r["standing"] == "green"),
    }
    return {
        "generated_at": _dt.datetime.now(_dt.timezone.utc).isoformat(timespec="seconds"),
        "note": (
            "Advisory derived-on-read RAG. Worst-of over the transparent checklist "
            "(references/rag-checklist.md). Not a stored score; gates nothing."
        ),
        "summary": summary,
        "projects": rows,
    }


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument(
        "--registry",
        type=Path,
        default=Path(os.environ.get("TRACKED_PROJECTS_FILE", str(DEFAULT_REGISTRY))),
        help="tracked-project registry YAML (default: portfolio/tracked-projects.yml)",
    )
    parser.add_argument(
        "--out",
        type=Path,
        default=Path(os.environ.get("ROLLUP_OUT", str(DEFAULT_OUT))),
        help="throwaway rollup JSON to write (default: generated/portfolio-rollup.json)",
    )
    args = parser.parse_args(argv)

    registry = args.registry if args.registry.is_absolute() else REPO_ROOT / args.registry
    out = args.out if args.out.is_absolute() else REPO_ROOT / args.out

    projects = _load_registry(registry)
    rollup = build_rollup(projects)

    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(json.dumps(rollup, indent=2) + "\n", encoding="utf-8")

    s = rollup["summary"]
    print(f"registry: {registry}")
    print(f"wrote:    {out}")
    print(
        f"projects: {len(rollup['projects'])}  "
        f"(red={s['red']} amber={s['amber']} green={s['green']})"
    )
    for row in rollup["projects"]:
        reasons = "; ".join(row["reasons"]) or "—"
        print(f"  - {row['name']}: {row['phase']} / {row['standing']}  [{reasons}]")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
