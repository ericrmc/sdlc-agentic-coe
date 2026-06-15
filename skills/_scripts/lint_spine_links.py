#!/usr/bin/env python3
"""
lint_spine_links.py — assert the spine's map points only at real skills.

`skills/00-sdlc-spine/SKILL.md` is the front-door table of contents: it names,
for every FORGE stage, the on-disk skill(s) that serve it. The spine "enforces
nothing" at *runtime* — but if its map points at a skill path that does not
exist, the map is a lie, and a practitioner who follows it lands on a 404. This
linter is the one mechanical guard on that: **every skill path or skill id the
spine names must resolve to a real `SKILL.md` on disk.**

    python3 skills/_scripts/lint_spine_links.py            # lint the repo
    python3 skills/_scripts/lint_spine_links.py --root .    # explicit root

WHAT IT DOES (deterministic; standard library only — runs in CI with zero
`pip install`):

  STEP 1  Read skills/00-sdlc-spine/SKILL.md.
  STEP 2  Build the catalogue of REAL skills: every directory under skills/
          that contains a SKILL.md, keyed BOTH by its repo-relative directory
          path (e.g. `skills/04-review-and-panel/convene-a-panel`) and by its
          frontmatter `name:` id (e.g. `convene-a-panel`).
  STEP 3  Extract every skill reference the spine names. Two forms count:
            (a) a path like `skills/<bucket>/<skill>` (with or without a
                trailing `/SKILL.md`), wherever it appears — table, prose, or
                code fence;
            (b) a backticked skill id like `` `convene-a-panel` `` that matches
                a known skill `name:`.
          Pure stage *labels* that are not skill ids (e.g. `01-intake-outcomes`
          bucket dirs, or narrative words) are ignored — we only assert the
          things that LOOK like a skill reference.
  STEP 4  FAIL (exit 1) if any named skill path / id does not resolve to a real
          SKILL.md. PASS (exit 0) when every reference resolves.

It prints a clear, sorted report either way. This is advisory CI like its
siblings: it surfaces a red ✗ to prompt a human fix; it gates no downstream
project.
"""

from __future__ import annotations

import argparse
import os
import re
import sys

SPINE_REL = "skills/00-sdlc-spine/SKILL.md"


def repo_root(explicit: str | None) -> str:
    if explicit:
        return os.path.abspath(explicit)
    # this file lives at skills/_scripts/ — root is two levels up
    return os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))


def read_name_frontmatter(skill_md: str) -> str | None:
    """Return the `name:` value from a SKILL.md frontmatter, if present."""
    try:
        with open(skill_md, "r", encoding="utf-8") as fh:
            text = fh.read()
    except OSError:
        return None
    # frontmatter is the first --- ... --- block
    m = re.match(r"^---\s*\n(.*?)\n---\s*\n", text, flags=re.DOTALL)
    block = m.group(1) if m else text
    nm = re.search(r"^name:\s*(.+?)\s*$", block, flags=re.MULTILINE)
    if not nm:
        return None
    return nm.group(1).strip().strip("'\"")


def build_catalogue(root: str) -> tuple[set[str], dict[str, str]]:
    """
    Return (real_dir_paths, name_to_dir).

    real_dir_paths : repo-relative skill directories that contain a SKILL.md,
                     normalised with forward slashes (e.g.
                     'skills/04-review-and-panel/convene-a-panel').
    name_to_dir    : frontmatter `name:` id -> that same repo-relative dir.
    """
    skills_dir = os.path.join(root, "skills")
    real_dirs: set[str] = set()
    name_to_dir: dict[str, str] = {}
    for dirpath, _dirnames, filenames in os.walk(skills_dir):
        if "SKILL.md" not in filenames:
            continue
        rel = os.path.relpath(dirpath, root).replace(os.sep, "/")
        real_dirs.add(rel)
        nm = read_name_frontmatter(os.path.join(dirpath, "SKILL.md"))
        if nm:
            name_to_dir.setdefault(nm, rel)
    return real_dirs, name_to_dir


# A skill PATH reference: skills/<bucket>/<skill> optionally /SKILL.md, allowing
# nested bucket segments. We capture up to (and not including) any /SKILL.md.
PATH_RE = re.compile(
    r"(skills/[A-Za-z0-9][A-Za-z0-9._-]*(?:/[A-Za-z0-9][A-Za-z0-9._-]*)+?)"
    r"(?:/SKILL\.md)?"
)

# A backticked token that could be a skill id, e.g. `convene-a-panel`.
TICK_RE = re.compile(r"`([a-z0-9][a-z0-9-]*[a-z0-9])`")


def extract_references(spine_text: str, known_names: set[str]) -> tuple[set[str], set[str]]:
    """
    Return (path_refs, id_refs).

    path_refs : every `skills/.../...`-shaped reference found (normalised, no
                trailing /SKILL.md).
    id_refs   : every backticked token that matches a known skill `name:`.
                (Backticked tokens that match nothing are narrative — ignored.)
    """
    path_refs: set[str] = set()
    for m in PATH_RE.finditer(spine_text):
        ref = m.group(1).rstrip("/")
        # ignore bare bucket references (skills/01-intake-outcomes) — those are
        # directories, not skills; a skill ref has the bucket AND a skill leaf.
        path_refs.add(ref)

    id_refs: set[str] = set()
    for m in TICK_RE.finditer(spine_text):
        tok = m.group(1)
        if tok in known_names:
            id_refs.add(tok)
    return path_refs, id_refs


def main(argv: list[str]) -> int:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--root", default=None, help="repo root (default: inferred)")
    args = ap.parse_args(argv)

    root = repo_root(args.root)
    spine_path = os.path.join(root, SPINE_REL)
    if not os.path.isfile(spine_path):
        print(f"FAIL: spine not found at {SPINE_REL}", file=sys.stderr)
        return 2

    with open(spine_path, "r", encoding="utf-8") as fh:
        spine_text = fh.read()

    real_dirs, name_to_dir = build_catalogue(root)
    known_names = set(name_to_dir)

    path_refs, id_refs = extract_references(spine_text, known_names)

    # A path ref resolves if it is a real skill directory (one that owns a
    # SKILL.md). Bare bucket dirs (skills/01-intake-outcomes) won't be in
    # real_dirs because they hold no SKILL.md of their own — but we only flag a
    # ref as broken if it has at least one segment past the bucket (i.e. it
    # really claims to be a skill). A two-segment bucket-only path is not a
    # skill claim, so we accept it iff the directory exists on disk.
    broken_paths: list[str] = []
    ok_paths: list[str] = []
    for ref in sorted(path_refs):
        abs_dir = os.path.join(root, ref)
        # depth: skills/<bucket>/<leaf...> -> 3+ segments is a skill claim.
        segs = ref.split("/")
        is_skill_claim = len(segs) >= 3
        if ref in real_dirs:
            ok_paths.append(ref)
        elif not is_skill_claim and os.path.isdir(abs_dir):
            # a bucket directory referenced as a directory — fine, not a skill.
            ok_paths.append(ref)
        else:
            broken_paths.append(ref)

    # id refs always resolve (we only collected ones already in known_names),
    # but report them for transparency.
    ok_ids = sorted(id_refs)

    print("=" * 70)
    print("lint_spine_links — spine map -> real SKILL.md resolution")
    print("=" * 70)
    print(f"spine: {SPINE_REL}")
    print(f"real skills on disk: {len(real_dirs)}")
    print(
        f"references found: {len(path_refs)} path-shaped, "
        f"{len(id_refs)} known skill-id backticks"
    )
    print("-" * 70)

    for ref in ok_paths:
        print(f"  OK  path  {ref}")
    for tok in ok_ids:
        print(f"  OK  id    `{tok}`  -> {name_to_dir[tok]}")

    if broken_paths:
        print("-" * 70)
        print("BROKEN spine references (no SKILL.md resolves):")
        for ref in broken_paths:
            print(f"  ✗   {ref}")
        print("-" * 70)
        print(
            f"FAIL: {len(broken_paths)} spine reference(s) point at a path with "
            f"no SKILL.md. Repoint them at a real nested skill path."
        )
        return 1

    print("-" * 70)
    print("OK: every skill path/id the spine names resolves to a real SKILL.md.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
