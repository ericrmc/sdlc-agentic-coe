#!/usr/bin/env python3
"""
lint_skill_references.py — assert every cited reference file actually exists.

A skill earns the right to be terse by pushing its long-form material into a
`references/` file beside it: a checklist, a template, a prompt, an enum. The
SKILL.md then cites that file (in its frontmatter `references:` list, or inline
in the body). The discipline (DESIGN convention D6): **every `references/<x>`
cited in any skills/**/SKILL.md MUST resolve to a real file on disk.** A cited
reference that does not exist is a dangling pointer — the skill promises depth
it does not deliver.

    python3 skills/_scripts/lint_skill_references.py            # lint the repo
    python3 skills/_scripts/lint_skill_references.py --root .   # explicit root

WHAT IT DOES (deterministic; standard library only — runs in CI with zero
`pip install`):

  STEP 1  Walk every skills/**/SKILL.md.
  STEP 2  Collect every `references/...` citation from BOTH:
            (a) the frontmatter `references:` YAML list, and
            (b) the body text (backticked or bare `references/<x>` tokens).
  STEP 3  Resolve each citation RELATIVE TO THE CITING SKILL'S OWN DIRECTORY
          (that is where a skill's `references/` folder lives). A citation that
          ends in `/` (a directory, e.g. `references/section-prompts/`) resolves
          if that directory exists.
  STEP 4  Report every citation as OK or MISSING. Exit 1 if any are missing,
          0 if all resolve.

NOTE ON POSTURE: this linter is advisory CI like its siblings. It is wired into
validate-skill-frontmatter.yml to SURFACE missing references (it never blocks a
merge). It is expected that, mid-build, some references are authored by a
different contributor and may still be missing — the script's job is to run
cleanly and name exactly which ones, not to be green at all costs.
"""

from __future__ import annotations

import argparse
import os
import re
import sys

# Matches references/<path> ONLY when it looks like an actual file or directory
# citation — i.e. it ends in a file extension (e.g. .md, .csv) OR a trailing
# slash (a directory citation, e.g. references/section-prompts/). This is what
# distinguishes a real pointer from incidental prose ("returned as
# references/pointers", where "references/pointers" means "references or
# pointers", not a file). Every genuine citation in this library carries an
# extension or a trailing slash, so this is safe and precise.
REF_RE = re.compile(
    r"references/[A-Za-z0-9][A-Za-z0-9._/-]*"
    r"(?:\.[A-Za-z0-9]+|/)"  # require a file extension OR a trailing slash
)


def repo_root(explicit: str | None) -> str:
    if explicit:
        return os.path.abspath(explicit)
    return os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))


def split_frontmatter(text: str) -> tuple[str, str]:
    """Return (frontmatter_block, body). Empty frontmatter if none present."""
    m = re.match(r"^---\s*\n(.*?)\n---\s*\n(.*)$", text, flags=re.DOTALL)
    if m:
        return m.group(1), m.group(2)
    return "", text


def citations_in(text: str) -> set[str]:
    """Every `references/...` token in the text, trailing punctuation trimmed."""
    out: set[str] = set()
    for m in REF_RE.finditer(text):
        ref = m.group(0)
        # Trim trailing prose punctuation that the char class may have eaten,
        # but KEEP a single trailing slash (it signals a directory citation).
        ref = ref.rstrip(".,;:)")
        if ref:
            out.add(ref)
    return out


def resolve(skill_dir: str, ref: str) -> bool:
    """A citation resolves relative to the citing skill's own directory."""
    target = os.path.join(skill_dir, ref)
    if ref.endswith("/"):
        return os.path.isdir(target)
    return os.path.exists(target)


def main(argv: list[str]) -> int:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--root", default=None, help="repo root (default: inferred)")
    args = ap.parse_args(argv)

    root = repo_root(args.root)
    skills_dir = os.path.join(root, "skills")

    skill_mds: list[str] = []
    for dirpath, _dirnames, filenames in os.walk(skills_dir):
        if "SKILL.md" in filenames:
            skill_mds.append(os.path.join(dirpath, "SKILL.md"))
    skill_mds.sort()

    total = 0
    missing: list[tuple[str, str]] = []  # (skill_rel, ref)
    ok = 0

    print("=" * 70)
    print("lint_skill_references — every cited references/<x> must resolve")
    print("=" * 70)

    for skill_md in skill_mds:
        skill_dir = os.path.dirname(skill_md)
        skill_rel = os.path.relpath(skill_md, root).replace(os.sep, "/")
        with open(skill_md, "r", encoding="utf-8") as fh:
            text = fh.read()
        fm, body = split_frontmatter(text)
        # Frontmatter and body both count toward D6.
        refs = citations_in(fm) | citations_in(body)
        if not refs:
            continue
        for ref in sorted(refs):
            total += 1
            if resolve(skill_dir, ref):
                ok += 1
            else:
                missing.append((skill_rel, ref))

    print(f"skills scanned: {len(skill_mds)}")
    print(f"references cited: {total}  ({ok} resolve, {len(missing)} missing)")
    print("-" * 70)

    if missing:
        print("MISSING references (cited but not on disk):")
        for skill_rel, ref in missing:
            citing_dir = os.path.dirname(skill_rel)
            print(f"  ✗  {skill_rel}")
            print(f"       cites: {ref}")
            print(f"       expected at: {citing_dir}/{ref}")
        print("-" * 70)
        print(
            f"FAIL: {len(missing)} cited reference(s) do not resolve. Author the "
            f"missing files (with real, grounded content) or fix the citation."
        )
        return 1

    print("OK: every cited references/<x> resolves on disk.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
