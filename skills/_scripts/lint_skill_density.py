#!/usr/bin/env python3
"""Advisory density check for SKILL.md bodies (ADR-0016, succinct over prose).

A skill is loaded WHOLE, every run, to do one task — every word is paid per-invocation.
This flags a skill whose PROSE body (the part under the author's control) has grown large
enough to warrant a tightening look. It measures the net body = total words minus the YAML
frontmatter minus every byte-stable quoted stub (the BEGIN/END blocks, which are mandatory,
multiplied across the library, and must stay verbatim). Embedded prompts, output templates,
and worked examples ARE counted — an over-long example or a re-embedded reference is exactly
the bloat the rule targets.

It is ADVISORY: it WARNs, it never fails a merge. Density is fine (closed taxonomies,
embedded prompts, multi-template outputs are justifiably long); RESTATEMENT is the target,
which a human spots on the flagged file. Pass --strict to make a WARN exit non-zero for a
local pass. A static word count cannot tell density from restatement — it only points.
"""
from __future__ import annotations

import argparse
import glob
import os
import sys

# Net-body threshold (words). ~average skill after stubs/frontmatter; a body past this is
# usually carrying a Notes-echo or a restated keystone (see ADR-0016 / the density audit).
THRESHOLD = 2500


def net_body_words(text: str) -> int:
    """Total words minus YAML frontmatter minus every byte-stable BEGIN/END stub block."""
    if text.startswith("---"):
        end = text.find("\n---", 3)
        if end != -1:
            text = text[end + 4:]
    kept, skipping = [], False
    for line in text.splitlines():
        if "<!-- BEGIN" in line:
            skipping = True
            continue
        if "<!-- END" in line:
            skipping = False
            continue
        if not skipping:
            kept.append(line)
    return len(" ".join(kept).split())


def discover(root: str) -> list[str]:
    return sorted(glob.glob(os.path.join(root, "skills", "**", "SKILL.md"), recursive=True))


def main(argv: list[str]) -> int:
    ap = argparse.ArgumentParser(description="Advisory SKILL.md density check (ADR-0016).")
    ap.add_argument("files", nargs="*", help="SKILL.md files (default: discover under skills/)")
    ap.add_argument("--repo-root", default=".")
    ap.add_argument("--threshold", type=int, default=THRESHOLD)
    ap.add_argument("--strict", action="store_true", help="exit non-zero if any file is flagged")
    args = ap.parse_args(argv)

    files = args.files or discover(args.repo_root)
    flagged = []
    for path in files:
        try:
            n = net_body_words(open(path, encoding="utf-8").read())
        except OSError as exc:
            print(f"  skip {path}: {exc}", file=sys.stderr)
            continue
        mark = "FLAG" if n > args.threshold else "ok  "
        if n > args.threshold:
            flagged.append((n, path))
        print(f"  {mark} {n:>5}w  {path}")

    print(
        f"\nDensity (advisory, ADR-0016): {len(flagged)}/{len(files)} skill bodies over "
        f"~{args.threshold}w net — a tightening look is suggested (density is fine; "
        f"restatement is the target). This never blocks a merge."
    )
    for n, path in sorted(flagged, reverse=True):
        print(f"  flag {n:>5}w  {path}")
    return 1 if (args.strict and flagged) else 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
