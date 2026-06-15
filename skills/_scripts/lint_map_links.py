#!/usr/bin/env python3
"""
lint_map_links.py — assert the map points only at real skills.

`skills/MAP.md` is the front-door table of contents: it names, for every
category, the on-disk skill(s) a reader can jump to. The map enforces nothing at
runtime, but if it names a skill path that does not exist, the map is a lie and a
reader who follows it lands on a 404. This linter is the one mechanical guard on
that: every skill path or skill id the map names must resolve to a real
`SKILL.md` on disk.

    python3 skills/_scripts/lint_map_links.py            # lint the repo
    python3 skills/_scripts/lint_map_links.py --root .    # explicit root

WHAT IT DOES (deterministic; standard library only — runs in CI with zero
`pip install`):

  STEP 1  Read skills/MAP.md.
  STEP 2  Build the catalogue of REAL skills: every directory under skills/
          that contains a SKILL.md, keyed BOTH by its repo-relative directory
          path (e.g. `skills/challenge/red-team-requirements`), by its
          category-relative path (e.g. `challenge/red-team-requirements`), and
          by its frontmatter `name:` id (e.g. `red-team-requirements`).
  STEP 3  Extract every skill reference the map names. Three forms count:
            (a) a full path like `skills/<category>/<skill>` (with or without a
                trailing `/SKILL.md`), wherever it appears;
            (b) a category-relative path like `challenge/red-team-requirements`
                (the form the category table uses), whose first segment is a
                real category directory under skills/;
            (c) a backticked skill id like `` `red-team-requirements` `` that
                matches a known skill `name:`.
          Tokens that look like neither a real path nor a known skill id are
          narrative — they are ignored. Only things that LOOK like a skill
          reference are asserted.
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

MAP_REL = "skills/MAP.md"


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


def build_catalogue(
    root: str,
) -> tuple[set[str], set[str], dict[str, str]]:
    """
    Return (real_dir_paths, category_rel_paths, name_to_dir).

    real_dir_paths     : repo-relative skill directories that contain a
                         SKILL.md, normalised with forward slashes (e.g.
                         'skills/challenge/red-team-requirements').
    category_rel_paths : the same dirs with the leading 'skills/' stripped (e.g.
                         'challenge/red-team-requirements') — the form the
                         category table uses.
    name_to_dir        : frontmatter `name:` id -> the repo-relative dir.
    """
    skills_dir = os.path.join(root, "skills")
    real_dirs: set[str] = set()
    cat_rel: set[str] = set()
    name_to_dir: dict[str, str] = {}
    for dirpath, _dirnames, filenames in os.walk(skills_dir):
        if "SKILL.md" not in filenames:
            continue
        rel = os.path.relpath(dirpath, root).replace(os.sep, "/")
        real_dirs.add(rel)
        cat_rel.add(rel[len("skills/"):])
        nm = read_name_frontmatter(os.path.join(dirpath, "SKILL.md"))
        if nm:
            name_to_dir.setdefault(nm, rel)
    return real_dirs, cat_rel, name_to_dir


def category_dirs(root: str) -> set[str]:
    """The first-level directories under skills/ (the categories)."""
    skills_dir = os.path.join(root, "skills")
    out: set[str] = set()
    try:
        for entry in os.listdir(skills_dir):
            if os.path.isdir(os.path.join(skills_dir, entry)):
                out.add(entry)
    except OSError:
        pass
    return out


# A full skill PATH reference: skills/<category>/<skill> optionally /SKILL.md,
# allowing nested segments. Capture up to (and not including) any /SKILL.md.
PATH_RE = re.compile(
    r"(skills/[A-Za-z0-9][A-Za-z0-9._-]*(?:/[A-Za-z0-9][A-Za-z0-9._-]*)+?)"
    r"(?:/SKILL\.md)?"
)

# A category-relative reference: <category>/<skill> (the table form). The first
# segment must be a real category dir, so we validate that in extract_references
# rather than over-match arbitrary slash tokens here.
CAT_REL_RE = re.compile(
    r"(?<![A-Za-z0-9._/-])"
    r"([a-z_][a-z0-9_-]*/[a-z0-9][a-z0-9._-]*(?:/[a-z0-9._-]+)*)"
    r"(?:/SKILL\.md)?"
)

# A backticked token that could be a skill id, e.g. `red-team-requirements`.
TICK_RE = re.compile(r"`([a-z0-9][a-z0-9-]*[a-z0-9])`")


def extract_references(
    map_text: str,
    known_names: set[str],
    categories: set[str],
) -> tuple[set[str], set[str], set[str]]:
    """
    Return (full_path_refs, cat_rel_refs, id_refs).

    full_path_refs : every `skills/.../...`-shaped reference found (normalised,
                     no trailing /SKILL.md).
    cat_rel_refs   : every `<category>/<skill>`-shaped reference whose first
                     segment is a real category dir under skills/.
    id_refs        : every backticked token that matches a known skill `name:`.
                     (Backticked tokens that match nothing are narrative.)
    """
    full_path_refs: set[str] = set()
    for m in PATH_RE.finditer(map_text):
        ref = m.group(1).rstrip("/")
        full_path_refs.add(ref)

    cat_rel_refs: set[str] = set()
    for m in CAT_REL_RE.finditer(map_text):
        ref = m.group(1).rstrip("/")
        # skip anything already counted as a full skills/... path
        if ref.startswith("skills/"):
            continue
        first = ref.split("/", 1)[0]
        # Only treat as a skill reference if the first segment is a real
        # category. This keeps prose like 'go/no-go' or 'reads/writes' out.
        if first in categories:
            cat_rel_refs.add(ref)

    id_refs: set[str] = set()
    for m in TICK_RE.finditer(map_text):
        tok = m.group(1)
        if tok in known_names:
            id_refs.add(tok)
    return full_path_refs, cat_rel_refs, id_refs


def main(argv: list[str]) -> int:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--root", default=None, help="repo root (default: inferred)")
    args = ap.parse_args(argv)

    root = repo_root(args.root)
    map_path = os.path.join(root, MAP_REL)
    if not os.path.isfile(map_path):
        print(f"FAIL: map not found at {MAP_REL}", file=sys.stderr)
        return 2

    with open(map_path, "r", encoding="utf-8") as fh:
        map_text = fh.read()

    real_dirs, cat_rel, name_to_dir = build_catalogue(root)
    known_names = set(name_to_dir)
    categories = category_dirs(root)

    full_path_refs, cat_rel_refs, id_refs = extract_references(
        map_text, known_names, categories
    )

    # A full path ref resolves if it is a real skill directory (one that owns a
    # SKILL.md). Bare category dirs (skills/challenge) won't be in real_dirs
    # because they hold no SKILL.md of their own — but we only flag a ref as
    # broken if it has at least one segment past the category (i.e. it really
    # claims to be a skill). A two-segment category-only path is not a skill
    # claim, so we accept it iff the directory exists on disk.
    broken_paths: list[str] = []
    ok_paths: list[str] = []
    for ref in sorted(full_path_refs):
        abs_dir = os.path.join(root, ref)
        segs = ref.split("/")
        is_skill_claim = len(segs) >= 3
        if ref in real_dirs:
            ok_paths.append(ref)
        elif not is_skill_claim and os.path.isdir(abs_dir):
            ok_paths.append(ref)
        else:
            broken_paths.append(ref)

    # Category-relative refs (the table form): each must resolve to a real skill
    # dir under skills/.
    broken_cat: list[str] = []
    ok_cat: list[str] = []
    for ref in sorted(cat_rel_refs):
        if ref in cat_rel:
            ok_cat.append(ref)
        else:
            broken_cat.append(ref)

    # id refs always resolve (we only collected ones already in known_names),
    # but report them for transparency.
    ok_ids = sorted(id_refs)

    print("=" * 70)
    print("lint_map_links — map -> real SKILL.md resolution")
    print("=" * 70)
    print(f"map: {MAP_REL}")
    print(f"real skills on disk: {len(real_dirs)}")
    print(
        f"references found: {len(full_path_refs)} full-path, "
        f"{len(cat_rel_refs)} category-relative, "
        f"{len(id_refs)} known skill-id backticks"
    )
    print("-" * 70)

    for ref in ok_paths:
        print(f"  OK  path  {ref}")
    for ref in ok_cat:
        print(f"  OK  cat   {ref}  -> skills/{ref}")
    for tok in ok_ids:
        print(f"  OK  id    `{tok}`  -> {name_to_dir[tok]}")

    broken = broken_paths + [f"{r} (category-relative)" for r in broken_cat]
    if broken:
        print("-" * 70)
        print("BROKEN map references (no SKILL.md resolves):")
        for ref in broken:
            print(f"  ✗   {ref}")
        print("-" * 70)
        print(
            f"FAIL: {len(broken)} map reference(s) point at a path with "
            f"no SKILL.md. Repoint them at a real skill path."
        )
        return 1

    print("-" * 70)
    print("OK: every skill path/id the map names resolves to a real SKILL.md.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
