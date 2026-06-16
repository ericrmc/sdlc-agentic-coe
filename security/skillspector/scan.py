#!/usr/bin/env python3
"""Run NVIDIA SkillSpector's STATIC scan over this repo's skills (no API key, no LLM).

SkillSpector (https://github.com/NVIDIA/SkillSpector, Apache-2.0) scans an agent skill for
prompt-injection, data-exfiltration, privilege-escalation, supply-chain, tool-misuse and
~12 other categories. Its STATIC analyzers (pattern + YARA + AST + taint + OSV) need no
model and no key — that is what this runs (`--no-llm`). The 3 SEMANTIC analyzers (an LLM
filters false positives + explains) are NOT run here; see this folder's README.md.

ADVISORY: this surfaces findings for a human to read; it is NOT a merge gate.

Bootstrapping: prefers `skillspector` already on PATH (CI), then `uv` (recommended — it
fetches a pinned Python 3.12 and the pinned tool, isolated, no pollution), then a local
venv. This script itself runs on any Python 3.8+ — it only orchestrates.

Usage:
  security/skillspector/scan.py                 # scan skills changed vs origin/main
  security/skillspector/scan.py --all           # scan every skill
  security/skillspector/scan.py --base <ref>    # diff base (default origin/main)
  security/skillspector/scan.py skills/x/y ...   # scan specific skill dir(s)
"""
from __future__ import annotations

import argparse
import json
import os
import shutil
import subprocess
import sys
from pathlib import Path

# SkillSpector has no PyPI release and no git tags, so we pin to an immutable COMMIT SHA and
# install from source. An upgrade = bump SKILLSPECTOR_REF after reviewing the diff (the scanner
# is itself a dependency surface: it pulls semgrep / YARA / langchain).
SKILLSPECTOR_VERSION = "2.1.4"  # human-readable version from its pyproject at the pinned ref
SKILLSPECTOR_REF = "cff7ecc4f2881d9e23ea4bb801a6353e1dbe39e6"
SKILLSPECTOR_SRC = f"git+https://github.com/NVIDIA/SkillSpector@{SKILLSPECTOR_REF}"
PY_VERSION = "3.12"
ROOT = Path(__file__).resolve().parents[2]
REPORTS = ROOT / "security" / "skillspector" / "reports"


def runner() -> list[str]:
    """The argv prefix that invokes `skillspector` (so we can append `scan ...`)."""
    if shutil.which("skillspector"):
        return ["skillspector"]
    if shutil.which("uv"):
        return ["uv", "tool", "run", "--quiet", "--python", PY_VERSION,
                "--from", SKILLSPECTOR_SRC, "skillspector"]
    venv = ROOT / "security" / "skillspector" / ".venv"
    exe = venv / ("Scripts" if os.name == "nt" else "bin") / "skillspector"
    if not exe.exists():
        py = next((p for p in (f"python{PY_VERSION}", "python3.13", "python3.12") if shutil.which(p)), None)
        if not py:
            sys.exit("ERROR: need `uv` (recommended) or Python 3.12/3.13 for SkillSpector "
                     f"{SKILLSPECTOR_VERSION}.\n  Install uv: curl -LsSf https://astral.sh/uv/install.sh | sh "
                     "(it fetches Python 3.12 for you), then re-run.")
        subprocess.run([py, "-m", "venv", str(venv)], check=True)
        subprocess.run([str(venv / "bin" / "pip"), "install", "--quiet", SKILLSPECTOR_SRC], check=True)
    return [str(exe)]


def all_skill_dirs() -> list[Path]:
    return sorted({p.parent for p in ROOT.glob("skills/*/*/SKILL.md")
                   if not p.relative_to(ROOT).parts[1].startswith("_")})


def changed_skill_dirs(base: str) -> list[Path]:
    try:
        out = subprocess.run(["git", "-C", str(ROOT), "diff", "--name-only", f"{base}...HEAD"],
                             capture_output=True, text=True).stdout
    except Exception:
        return []
    dirs = set()
    for line in out.splitlines():
        parts = line.split("/")
        if len(parts) >= 4 and parts[0] == "skills" and not parts[1].startswith("_"):
            d = ROOT / parts[0] / parts[1] / parts[2]
            if (d / "SKILL.md").exists():
                dirs.add(d)
    return sorted(dirs)


def finding_count(sarif: Path) -> int | None:
    try:
        d = json.loads(sarif.read_text(encoding="utf-8"))
        return sum(len(r.get("results", [])) for r in d.get("runs", []))
    except Exception:
        return None


def main() -> int:
    ap = argparse.ArgumentParser(description="SkillSpector static scan over the skills (advisory).")
    ap.add_argument("paths", nargs="*", help="specific skill dirs (default: changed vs --base)")
    ap.add_argument("--all", action="store_true", help="scan every skill")
    ap.add_argument("--base", default="origin/main", help="git diff base (default origin/main)")
    args = ap.parse_args()

    if args.paths:
        targets = [ROOT / p for p in args.paths]
    elif args.all:
        targets = all_skill_dirs()
    else:
        targets = changed_skill_dirs(args.base)
        if not targets:
            print(f"No changed skills vs {args.base}. (Use --all to scan everything.)")
            return 0

    ss = runner()
    REPORTS.mkdir(parents=True, exist_ok=True)
    print(f"SkillSpector {SKILLSPECTOR_VERSION} — static scan (--no-llm) over {len(targets)} skill(s)")
    print(f"reports: {REPORTS}/")
    worst, flagged, produced = 0, [], []
    for d in targets:
        rel = d.relative_to(ROOT)
        out = REPORTS / (str(rel).replace("/", "-") + ".sarif")
        rc = subprocess.run([*ss, "scan", str(d), "--no-llm", "--format", "sarif", "--output", str(out)],
                            stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL).returncode
        n = finding_count(out)
        if rc >= 2 or n is None:
            print(f"  ERROR      {rel}  (scan failed rc={rc})"); worst = 2
        elif n:
            print(f"  FINDINGS({n})  {rel}"); flagged.append(f"{rel} ({n})"); worst = max(worst, 1)
        else:
            print(f"  clean      {rel}")
        if out.exists():
            produced.append(out)

    # Merge per-skill SARIF into one document (for the Security tab / a single review file).
    merged = {"version": "2.1.0", "$schema": "https://json.schemastore.org/sarif-2.1.0.json", "runs": []}
    for p in produced:
        try:
            merged["runs"].extend(json.loads(p.read_text(encoding="utf-8")).get("runs", []))
        except Exception:
            pass
    (REPORTS / "skillspector.sarif").write_text(json.dumps(merged, indent=2), encoding="utf-8")

    print()
    if flagged:
        print(f"ADVISORY — SkillSpector flagged {len(flagged)} skill(s); read the SARIF in "
              f"{REPORTS}/ and judge each finding:")
        for f in flagged:
            print(f"  - {f}")
        print("(A static pattern flags for review; it is not proof of malice. This never blocks a merge.)")
    elif worst == 0:
        print("No static findings. (Advisory: a clean static scan is necessary, not sufficient.)")
    return worst


if __name__ == "__main__":
    raise SystemExit(main())
