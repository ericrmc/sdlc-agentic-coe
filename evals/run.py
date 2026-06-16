#!/usr/bin/env python3
"""Entrypoint evals — does a cold agent, pointed only at this repo, orient and run a skill
correctly? Each case feeds a prompt to an agent HARNESS (read-only) and grades the agent's
answer with DETERMINISTIC assertions — no judge model, no API key. It catches the regressions
a linter cannot: a rename that breaks navigation, a tightening pass that drops the grounding
halt, a skill whose output format drifts.

Harness-pluggable (the agent-first claim, tested against real harnesses):
  --harness claude   `claude -p --allowedTools Read Glob Grep`   (stdout is the answer)
  --harness codex    `codex exec --sandbox read-only -o <file>`  (final message)
  --harness cmd      $EVAL_HARNESS_CMD reads the prompt on stdin, prints the answer
Running a case INVOKES an agent, which needs that harness installed + its own auth — so this
is a local / on-demand suite, not a per-PR Action.

Usage:
  evals/run.py                         # all cases, claude harness
  evals/run.py --harness codex
  evals/run.py --case orientation
  evals/run.py --list
"""
from __future__ import annotations

import argparse
import json
import os
import re
import shlex
import subprocess
import sys
import tempfile
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
CASES = ROOT / "evals" / "cases"
RESULTS = ROOT / "evals" / "results"


def load_cases(only: str | None) -> list[dict]:
    cases = []
    for jf in sorted(CASES.glob("*.json")):
        c = json.loads(jf.read_text(encoding="utf-8"))
        c["id"] = c.get("id", jf.stem)
        pf = jf.with_suffix(".prompt.md")
        c["prompt"] = pf.read_text(encoding="utf-8") if pf.exists() else c.get("prompt", "")
        if not c["prompt"]:
            sys.exit(f"case {c['id']}: no prompt (need a {jf.stem}.prompt.md or a 'prompt' field)")
        if only is None or only == c["id"]:
            cases.append(c)
    return cases


def run_harness(harness: str, prompt: str, allowed_tools: list[str], timeout: int) -> str:
    """Invoke the agent read-only in the repo root; return its final answer text."""
    if harness == "claude":
        cmd = ["claude", "-p", "--allowedTools", *allowed_tools]
        r = subprocess.run(cmd, input=prompt, cwd=ROOT, capture_output=True, text=True, timeout=timeout)
        return r.stdout
    if harness == "codex":
        with tempfile.NamedTemporaryFile("r", suffix=".txt", delete=False) as tf:
            last = tf.name
        cmd = ["codex", "exec", "--sandbox", "read-only", "-o", last]
        r = subprocess.run(cmd, input=prompt, cwd=ROOT, capture_output=True, text=True, timeout=timeout)
        try:
            ans = Path(last).read_text(encoding="utf-8").strip()
        finally:
            os.unlink(last)
        return ans or r.stdout
    if harness == "cmd":
        tmpl = os.environ.get("EVAL_HARNESS_CMD")
        if not tmpl:
            sys.exit("--harness cmd needs $EVAL_HARNESS_CMD (a command that reads the prompt on stdin).")
        r = subprocess.run(shlex.split(tmpl), input=prompt, cwd=ROOT, capture_output=True, text=True, timeout=timeout)
        return r.stdout
    sys.exit(f"unknown harness: {harness}")


def grade(answer: str, asserts: dict) -> list[str]:
    """Return a list of failure messages (empty = pass). Substring checks are case-insensitive."""
    low = answer.lower()
    fails = []
    for s in asserts.get("contains", []):
        if s.lower() not in low:
            fails.append(f"missing required text: {s!r}")
    any_of = asserts.get("contains_any", [])
    if any_of and not any(s.lower() in low for s in any_of):
        fails.append(f"none of the expected alternatives present: {any_of}")
    for s in asserts.get("not_contains", []):
        if s.lower() in low:
            fails.append(f"contains forbidden text: {s!r}")
    for pat in asserts.get("regex", []):
        if not re.search(pat, answer, re.I | re.S):
            fails.append(f"regex did not match: {pat!r}")
    if not answer.strip():
        fails.append("empty answer (harness produced nothing — auth/tooling problem?)")
    return fails


def main() -> int:
    ap = argparse.ArgumentParser(description="Entrypoint evals (deterministic, key-free).")
    ap.add_argument("--harness", default="claude", choices=["claude", "codex", "cmd"])
    ap.add_argument("--case", default=None, help="run a single case id")
    ap.add_argument("--timeout", type=int, default=420)
    ap.add_argument("--list", action="store_true", help="list cases and exit")
    args = ap.parse_args()

    cases = load_cases(args.case)
    if args.list:
        for c in cases:
            print(f"  {c['id']:<22} [{c.get('category','-')}] {c.get('description','')}")
        return 0
    if not cases:
        sys.exit(f"no case matched {args.case!r}")

    outdir = RESULTS / args.harness
    outdir.mkdir(parents=True, exist_ok=True)
    report, passed = [], 0
    print(f"Entrypoint evals — harness={args.harness}, {len(cases)} case(s)\n")
    for c in cases:
        tools = c.get("allowed_tools", ["Read", "Glob", "Grep"])
        try:
            answer = run_harness(args.harness, c["prompt"], tools, args.timeout)
        except subprocess.TimeoutExpired:
            answer = ""
        except FileNotFoundError:
            sys.exit(f"harness '{args.harness}' not installed / not on PATH.")
        (outdir / f"{c['id']}.txt").write_text(answer, encoding="utf-8")
        fails = grade(answer, c.get("assert", {}))
        ok = not fails
        passed += ok
        print(f"  {'PASS' if ok else 'FAIL'}  {c['id']:<22} [{c.get('category','-')}]")
        for f in fails:
            print(f"          - {f}")
        report.append({"id": c["id"], "category": c.get("category"), "passed": ok, "failures": fails})

    (RESULTS / "report.json").write_text(
        json.dumps({"harness": args.harness, "passed": passed, "total": len(cases), "cases": report}, indent=2),
        encoding="utf-8")
    print(f"\n{passed}/{len(cases)} passed. Transcripts: {outdir}/  Report: {RESULTS}/report.json")
    return 0 if passed == len(cases) else 1


if __name__ == "__main__":
    raise SystemExit(main())
