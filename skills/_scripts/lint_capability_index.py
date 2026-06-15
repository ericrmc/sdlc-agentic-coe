#!/usr/bin/env python3
"""
lint_capability_index.py — keep the capability index and the capability files honest.

The capability library has two halves that must agree: the per-capability files
under capabilities/<domain>/<slug>.md (each with frontmatter carrying a
capability_key, aliases, and fulfilled_by) and capabilities/INDEX.md, the
alias-searchable lookup a need-first reader is pointed at first. This linter is
the one mechanical guard that the two never drift apart, and that the
capability <-> pattern links are bidirectional.

    python3 skills/_scripts/lint_capability_index.py            # lint the repo
    python3 skills/_scripts/lint_capability_index.py --root .    # explicit root

WHAT IT CHECKS (deterministic; standard library only — runs in CI with zero
`pip install`):

  CHECK 1  INDEX -> capability. Every INDEX.md row's capability_key resolves to a
           real capability file (the linked path exists AND its frontmatter
           capability_key matches the key the row cites). An entry that points at
           a missing key or a wrong path is a need-first lookup that 404s.

  CHECK 2  capability -> INDEX. Every alias declared in a capability's frontmatter
           `aliases` appears as an INDEX.md row pointing at that capability_key.
           An alias a reader would type but cannot find in the index is a buried
           capability.

  CHECK 3  Bidirectional capability <-> pattern links:
             (a) A capability's `fulfilled_by[].pattern_key` (any confidence) must
                 name a real pattern file. A PROVEN fulfilment additionally
                 requires that the pattern back-references the capability via its
                 own `fulfils: [CAP-...]` list (the reverse edge).
             (b) A pattern's `fulfils: [CAP-...]` must name a real capability, and
                 that capability must list the pattern in its `fulfilled_by`. A
                 pattern that claims to fulfil a capability the capability does not
                 acknowledge is a one-sided edge.

POSTURE: advisory CI, exactly like its siblings (lint_map_links.py,
lint_skill_references.py). It is wired into validate-skill-frontmatter.yml and
validate-capabilities.yml to SURFACE a drift with a red ✗ and a report; it never
blocks a merge. The structural gate for a capability is the CODEOWNERS architect
PR review — this linter only makes sure the reviewer reads a consistent library.

EXIT CODES
    0  every check passed
    1  at least one inconsistency was found — see the per-item report
    2  the linter could not run (e.g. no capabilities/ dir, INDEX.md missing)
"""

from __future__ import annotations

import argparse
import importlib.util
import os
import re
import sys
from pathlib import Path

CAPABILITIES_DIR_REL = "capabilities"
INDEX_REL = "capabilities/INDEX.md"
PATTERNS_DIR_REL = "patterns"

CAP_KEY_RE = re.compile(r"^CAP-[A-Z0-9]+(-[A-Z0-9]+)*$")

# One INDEX.md row: | <alias> | [`CAP-KEY`](relative/path.md) | <name> | <state> |
# We read the alias (col 1), the cited capability_key, and the linked path.
INDEX_ROW_RE = re.compile(
    r"^\|\s*(?P<alias>.+?)\s*\|\s*\[`(?P<key>CAP-[A-Z0-9-]+)`\]\((?P<path>[^)]+)\)\s*\|"
)


# --------------------------------------------------------------------------- #
# Frontmatter parsing — reuse the proven parser from the pattern linter (same
# directory), which already handles the `>` block scalars and nested
# list/inline-map shapes capability and pattern frontmatter use. Fall back to a
# minimal local parser only if that module cannot be loaded, so this linter
# stays runnable in isolation.
# --------------------------------------------------------------------------- #


def _load_shared_parser():
    here = Path(__file__).resolve().parent
    pf = here / "lint_pattern_frontmatter.py"
    if not pf.is_file():
        return None
    try:
        spec = importlib.util.spec_from_file_location("_coe_lint_pf", str(pf))
        mod = importlib.util.module_from_spec(spec)
        assert spec and spec.loader
        spec.loader.exec_module(mod)  # type: ignore[union-attr]
        return mod
    except Exception:
        return None


_PF = _load_shared_parser()


def parse_frontmatter(text: str) -> dict | None:
    """Return the YAML frontmatter as a dict, or None if it cannot be parsed."""
    if _PF is not None:
        try:
            return _PF.parse_frontmatter(text)
        except Exception:
            return None
    # Minimal local fallback: PyYAML if present, else a tiny line parser that
    # covers the fields this linter reads (capability_key, pattern_key, aliases,
    # fulfilled_by[].{confidence,pattern_key}, fulfils).
    block_m = re.match(r"\A﻿?---[ \t]*\r?\n(.*?)\r?\n---[ \t]*\r?$",
                       text, re.DOTALL | re.MULTILINE)
    if not block_m:
        return None
    block = block_m.group(1)
    try:
        import yaml  # type: ignore

        data = yaml.safe_load(block)
        return data if isinstance(data, dict) else None
    except Exception:
        pass
    return _tiny_parse(block)


def _tiny_parse(block: str) -> dict:
    """Stdlib fallback for the handful of fields this linter needs."""
    data: dict = {}
    lines = block.splitlines()
    i = 0
    n = len(lines)

    def indent(s: str) -> int:
        return len(s) - len(s.lstrip(" "))

    while i < n:
        line = lines[i]
        s = line.strip()
        if not s or s.startswith("#"):
            i += 1
            continue
        if indent(line) != 0 or ":" not in s:
            i += 1
            continue
        key, _, rest = s.partition(":")
        key = key.strip()
        rest = rest.strip()
        if rest in ("", ">", "|", ">-", "|-"):
            # collect an indented child block
            child = []
            j = i + 1
            while j < n and (lines[j].strip() == "" or indent(lines[j]) > 0):
                child.append(lines[j])
                j += 1
            if rest in (">", "|", ">-", "|-"):
                data[key] = " ".join(c.strip() for c in child if c.strip())
            else:
                data[key] = _parse_child_block(child)
            i = j
        else:
            if rest.startswith("[") and rest.endswith("]"):
                inner = rest[1:-1].strip()
                data[key] = [t.strip().strip("'\"") for t in inner.split(",") if t.strip()]
            else:
                data[key] = rest.strip("'\"")
            i += 1
    return data


def _parse_child_block(child: list[str]):
    """Parse an indented block as a list (of scalars or `- key: value` maps)."""
    items: list = []
    cur: dict | None = None
    cur_indent = None
    for raw in child:
        if not raw.strip() or raw.strip().startswith("#"):
            continue
        ind = len(raw) - len(raw.lstrip(" "))
        s = raw.strip()
        if s.startswith("- "):
            content = s[2:].strip()
            cur_indent = ind
            if content.startswith("{") and content.endswith("}"):
                items.append(_parse_inline(content))
                cur = None
            elif ":" in content:
                cur = {}
                k, _, v = content.partition(":")
                cur[k.strip()] = v.strip().strip("'\"")
                items.append(cur)
            else:
                items.append(content.strip("'\""))
                cur = None
        elif cur is not None and cur_indent is not None and ind > cur_indent and ":" in s:
            k, _, v = s.partition(":")
            cur[k.strip()] = v.strip().strip("'\"")
    return items


def _parse_inline(s: str) -> dict:
    inner = s.strip().lstrip("{").rstrip("}")
    out: dict = {}
    for part in re.split(r",(?=(?:[^\"']*[\"'][^\"']*[\"'])*[^\"']*$)", inner):
        part = part.strip()
        if ":" in part:
            k, _, v = part.partition(":")
            out[k.strip().strip("'\"")] = v.strip().strip("'\"")
    return out


# --------------------------------------------------------------------------- #
# Discovery
# --------------------------------------------------------------------------- #


def repo_root(explicit: str | None) -> Path:
    if explicit:
        return Path(explicit).resolve()
    return Path(__file__).resolve().parent.parent.parent


def discover_capability_files(root: Path) -> list[Path]:
    cap_dir = root / CAPABILITIES_DIR_REL
    if not cap_dir.is_dir():
        return []
    out: list[Path] = []
    for p in sorted(cap_dir.rglob("*.md")):
        parts = set(p.relative_to(cap_dir).parts)
        if "_schema" in parts:
            continue
        if p.name.lower() in {"readme.md", "index.md", "contributing.md"}:
            continue
        if p.name == "_TEMPLATE.md" or p.name.startswith("_"):
            continue
        out.append(p)
    return out


def discover_pattern_files(root: Path) -> list[Path]:
    pat_dir = root / PATTERNS_DIR_REL
    if not pat_dir.is_dir():
        return []
    out: list[Path] = []
    for p in sorted(pat_dir.rglob("*.md")):
        parts = set(p.relative_to(pat_dir).parts)
        if "_schema" in parts:
            continue
        if p.name.lower() in {"readme.md", "index.md", "contributing.md"}:
            continue
        if p.name == "_TEMPLATE.md" or p.name.startswith("_"):
            continue
        out.append(p)
    return out


# --------------------------------------------------------------------------- #
# Index parsing
# --------------------------------------------------------------------------- #


def parse_index(index_text: str) -> list[tuple[str, str, str]]:
    """Return [(alias, capability_key, linked_path), ...] for every INDEX row."""
    rows: list[tuple[str, str, str]] = []
    for line in index_text.splitlines():
        m = INDEX_ROW_RE.match(line)
        if not m:
            continue
        alias = m.group("alias").strip()
        # Skip the header row's literal label / separator artefacts.
        if alias.lower().startswith("you might call"):
            continue
        rows.append((alias, m.group("key"), m.group("path").strip()))
    return rows


# --------------------------------------------------------------------------- #
# Main
# --------------------------------------------------------------------------- #


def main(argv: list[str]) -> int:
    ap = argparse.ArgumentParser(
        description="Validate capabilities/INDEX.md <-> capability files <-> pattern links."
    )
    ap.add_argument("--root", default=None, help="repo root (default: inferred)")
    args = ap.parse_args(argv)

    root = repo_root(args.root)
    cap_dir = root / CAPABILITIES_DIR_REL
    index_path = root / INDEX_REL

    print("=" * 70)
    print("lint_capability_index — INDEX.md <-> capabilities/ <-> patterns/")
    print("=" * 70)

    if not cap_dir.is_dir():
        print(f"FAIL: no {CAPABILITIES_DIR_REL}/ directory under {root}.",
              file=sys.stderr)
        return 2
    if not index_path.is_file():
        print(f"FAIL: {INDEX_REL} not found.", file=sys.stderr)
        return 2

    # ---- load capability files --------------------------------------------- #
    cap_files = discover_capability_files(root)
    key_to_file: dict[str, Path] = {}          # CAP-KEY -> capability file
    key_to_aliases: dict[str, list[str]] = {}  # CAP-KEY -> declared aliases
    key_fulfilled_by: dict[str, list[dict]] = {}  # CAP-KEY -> fulfilled_by entries
    errors: list[str] = []

    for f in cap_files:
        rel = f.relative_to(root).as_posix()
        data = parse_frontmatter(f.read_text(encoding="utf-8"))
        if not data:
            errors.append(f"{rel}: could not parse YAML frontmatter")
            continue
        key = data.get("capability_key")
        if not isinstance(key, str) or not CAP_KEY_RE.match(key):
            errors.append(f"{rel}: missing or malformed capability_key '{key}'")
            continue
        if key in key_to_file:
            errors.append(
                f"{rel}: capability_key '{key}' is also defined in "
                f"{key_to_file[key].relative_to(root).as_posix()} — keys must be unique"
            )
            continue
        key_to_file[key] = f
        aliases = data.get("aliases")
        key_to_aliases[key] = [a for a in aliases if isinstance(a, str)] if isinstance(aliases, list) else []
        fb = data.get("fulfilled_by")
        key_fulfilled_by[key] = [e for e in fb if isinstance(e, dict)] if isinstance(fb, list) else []

    # ---- load pattern files (for the bidirectional link check) ------------- #
    pat_files = discover_pattern_files(root)
    pat_key_to_file: dict[str, Path] = {}
    pat_fulfils: dict[str, list[str]] = {}  # PAT-KEY -> [CAP-...] it claims to fulfil
    for f in pat_files:
        data = parse_frontmatter(f.read_text(encoding="utf-8"))
        if not data:
            continue
        pk = data.get("pattern_key")
        if not isinstance(pk, str) or not pk:
            continue
        pat_key_to_file[pk] = f
        fulfils = data.get("fulfils")
        if isinstance(fulfils, list):
            pat_fulfils[pk] = [c for c in fulfils if isinstance(c, str)]
        elif isinstance(fulfils, str) and fulfils:
            pat_fulfils[pk] = [fulfils]
        else:
            pat_fulfils[pk] = []

    # ---- parse the index --------------------------------------------------- #
    index_rows = parse_index(index_path.read_text(encoding="utf-8"))

    # ===================================================================== #
    # CHECK 1 — every INDEX row resolves to a real capability key + path.
    # ===================================================================== #
    check1_fail: list[str] = []
    index_alias_keys: set[tuple[str, str]] = set()  # (normalised alias, key)
    for alias, key, path in index_rows:
        index_alias_keys.add((alias.strip().lower(), key))
        if key not in key_to_file:
            check1_fail.append(
                f"INDEX row alias '{alias}' cites '{key}', which has no capability "
                f"file under {CAPABILITIES_DIR_REL}/"
            )
            continue
        # the linked path must resolve to the same capability the key names
        resolved = (index_path.parent / path).resolve()
        actual = key_to_file[key].resolve()
        if resolved != actual:
            check1_fail.append(
                f"INDEX row alias '{alias}' ({key}) links to '{path}', but {key} "
                f"lives at {key_to_file[key].relative_to(root).as_posix()}"
            )

    # ===================================================================== #
    # CHECK 2 — every capability alias appears in the INDEX for its key.
    # ===================================================================== #
    check2_fail: list[str] = []
    for key, aliases in key_to_aliases.items():
        for alias in aliases:
            if (alias.strip().lower(), key) not in index_alias_keys:
                check2_fail.append(
                    f"{key}: alias '{alias}' is declared in "
                    f"{key_to_file[key].relative_to(root).as_posix()} but has no "
                    f"row in {INDEX_REL} pointing at {key}"
                )

    # ===================================================================== #
    # CHECK 3 — bidirectional capability <-> pattern links.
    # ===================================================================== #
    check3_fail: list[str] = []
    # (a) capability -> pattern
    for key, entries in key_fulfilled_by.items():
        cap_rel = key_to_file[key].relative_to(root).as_posix()
        for e in entries:
            pk = e.get("pattern_key")
            conf = e.get("confidence")
            if not pk:
                continue  # a candidate may name only a vendor in `note`
            if pk not in pat_key_to_file:
                check3_fail.append(
                    f"{cap_rel}: {key} fulfilled_by names pattern '{pk}', which has "
                    f"no pattern file under {PATTERNS_DIR_REL}/"
                )
                continue
            if conf == "proven" and key not in pat_fulfils.get(pk, []):
                check3_fail.append(
                    f"{cap_rel}: {key} is proven-fulfilled by '{pk}', but "
                    f"{pat_key_to_file[pk].relative_to(root).as_posix()} does not "
                    f"back-reference it (add '{key}' to that pattern's fulfils:)"
                )
    # (b) pattern -> capability
    for pk, caps in pat_fulfils.items():
        pat_rel = pat_key_to_file[pk].relative_to(root).as_posix()
        for cap in caps:
            if cap not in key_to_file:
                check3_fail.append(
                    f"{pat_rel}: pattern {pk} fulfils '{cap}', which has no "
                    f"capability file under {CAPABILITIES_DIR_REL}/"
                )
                continue
            fulfilling = {e.get("pattern_key") for e in key_fulfilled_by.get(cap, [])}
            if pk not in fulfilling:
                check3_fail.append(
                    f"{pat_rel}: pattern {pk} claims to fulfil '{cap}', but "
                    f"{key_to_file[cap].relative_to(root).as_posix()} does not list "
                    f"{pk} in its fulfilled_by"
                )

    # ---- report ------------------------------------------------------------ #
    print(f"capability files: {len(key_to_file)}  "
          f"({', '.join(sorted(key_to_file)) or 'none'})")
    print(f"INDEX rows: {len(index_rows)}")
    print(f"pattern files: {len(pat_key_to_file)}")
    print("-" * 70)

    def _section(title: str, items: list[str]) -> None:
        if items:
            print(f"{title}:")
            for it in items:
                print(f"  ✗  {it}")
            print("-" * 70)

    _section("Parse / key errors", errors)
    _section("CHECK 1 — INDEX entry points at a missing capability key/path",
             check1_fail)
    _section("CHECK 2 — capability alias missing from INDEX.md", check2_fail)
    _section("CHECK 3 — capability <-> pattern link is one-sided", check3_fail)

    total = len(errors) + len(check1_fail) + len(check2_fail) + len(check3_fail)
    if total:
        print(f"FAIL: {total} capability-index inconsistency(ies). Fix the alias, "
              f"the INDEX entry, or the missing back-reference above (advisory — "
              f"never blocks a merge).")
        return 1

    print("OK: every INDEX entry resolves, every alias is indexed, and every "
          "capability <-> pattern link is bidirectional.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
