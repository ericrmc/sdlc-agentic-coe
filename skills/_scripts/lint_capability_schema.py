#!/usr/bin/env python3
"""
lint_capability_schema.py — validate every capability file's frontmatter.

The schema half of the capability validation. It checks each
capabilities/<domain>/<slug>.md frontmatter against
capabilities/_schema/capability.frontmatter.schema.json — using the `jsonschema`
package (Draft 7) when it is installable, and falling back to an equivalent
standard-library structural check (the same v1 contract: required fields, the
closed capability_domain and NFR-kind enums, the >=2-aliases rule, and the
proven-fulfilment-needs-pattern_key+evidence rule) when it is not. Either way the
linter runs on a bare runner with python3 and nothing else.

    python3 skills/_scripts/lint_capability_schema.py            # lint the repo
    python3 skills/_scripts/lint_capability_schema.py --root .    # explicit root

It is the structural sibling of lint_capability_index.py (which checks the
INDEX <-> capability <-> pattern links). Both are advisory CI — surfaced by
validate-capabilities.yml, never a merge gate. The structural gate for a
capability is the CODEOWNERS architect PR review.

EXIT CODES
    0  every capability frontmatter is well-formed
    1  at least one is malformed — see the per-file report
    2  the linter could not run (no capabilities/ dir)
"""

from __future__ import annotations

import argparse
import importlib.util
import json
import re
import sys
from pathlib import Path

CAPABILITIES_DIR_REL = "capabilities"
SCHEMA_REL = "capabilities/_schema/capability.frontmatter.schema.json"
DOMAINS_REL = "capabilities/_schema/capability-domains.enum.txt"
NFR_ENUM_REL = "patterns/_schema/nfr-kinds.enum.txt"

REQUIRED_FIELDS = [
    "capability_key",
    "name",
    "capability_domain",
    "summary",
    "need_statement",
    "aliases",
    "fulfilled_by",
    "governance_nfrs",
    "valid_from",
    "approval_status",
]

NFR_KIND_FALLBACK = [
    "security", "availability", "performance", "data-residency", "observability",
    "resilience", "cost", "compliance", "scalability", "data-governance", "operations",
]
DOMAIN_FALLBACK = ["data", "compute", "integration", "runtime", "experience", "governance"]


def repo_root(explicit: str | None) -> Path:
    if explicit:
        return Path(explicit).resolve()
    return Path(__file__).resolve().parent.parent.parent


def _load_shared_parser():
    """Reuse the proven frontmatter parser from the pattern linter if present."""
    pf = Path(__file__).resolve().parent / "lint_pattern_frontmatter.py"
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
    if _PF is not None:
        try:
            return _PF.parse_frontmatter(text)
        except Exception:
            return None
    m = re.match(r"\A﻿?---[ \t]*\r?\n(.*?)\r?\n---[ \t]*\r?$",
                 text, re.DOTALL | re.MULTILINE)
    if not m:
        return None
    try:
        import yaml  # type: ignore

        d = yaml.safe_load(m.group(1))
        return d if isinstance(d, dict) else None
    except Exception:
        return None


def load_enum(path: Path, fallback: list[str]) -> list[str]:
    if path.is_file():
        vals = []
        for line in path.read_text(encoding="utf-8").splitlines():
            line = line.split("#", 1)[0].strip()
            if line:
                vals.append(line)
        if vals:
            return vals
    return list(fallback)


def discover_capability_files(root: Path) -> list[Path]:
    cap_dir = root / CAPABILITIES_DIR_REL
    if not cap_dir.is_dir():
        return []
    out: list[Path] = []
    for p in sorted(cap_dir.rglob("*.md")):
        if "_schema" in set(p.relative_to(cap_dir).parts):
            continue
        if p.name.lower() in {"readme.md", "index.md", "contributing.md"}:
            continue
        if p.name.startswith("_"):
            continue
        out.append(p)
    return out


def make_jsonschema_validator(root: Path):
    schema_path = root / SCHEMA_REL
    if not schema_path.is_file():
        return None
    try:
        import jsonschema  # type: ignore

        return jsonschema.Draft7Validator(json.loads(schema_path.read_text(encoding="utf-8")))
    except Exception:
        return None


def structural_errors(data: dict, domains: set[str], nfr_kinds: set[str]) -> list[str]:
    """The stdlib fallback: encode the same v1 contract the schema pins down."""
    errs: list[str] = []
    for field in REQUIRED_FIELDS:
        if field not in data or data[field] in (None, "", []):
            errs.append(f"missing required field '{field}'")
    dom = data.get("capability_domain")
    if dom is not None and dom not in domains:
        errs.append(f"capability_domain '{dom}' is not one of {sorted(domains)}")
    aliases = data.get("aliases")
    if isinstance(aliases, list) and len(aliases) < 2:
        errs.append("aliases must have >=2 entries (the findability seed)")
    fb = data.get("fulfilled_by")
    if isinstance(fb, list):
        for i, e in enumerate(fb, 1):
            if not isinstance(e, dict):
                continue
            if not e.get("confidence"):
                errs.append(f"fulfilled_by[{i}] is missing 'confidence'")
            if not e.get("note"):
                errs.append(f"fulfilled_by[{i}] is missing 'note'")
            if e.get("confidence") == "proven":
                if not e.get("pattern_key"):
                    errs.append(f"fulfilled_by[{i}] is proven but has no pattern_key")
                if not e.get("evidence"):
                    errs.append(f"fulfilled_by[{i}] is proven but carries no evidence")
    gn = data.get("governance_nfrs")
    if isinstance(gn, list):
        for i, e in enumerate(gn, 1):
            if not isinstance(e, dict):
                continue
            if e.get("kind") not in nfr_kinds:
                errs.append(f"governance_nfrs[{i}].kind '{e.get('kind')}' not in closed NFR enum")
            if not e.get("statement"):
                errs.append(f"governance_nfrs[{i}] is missing 'statement'")
            if not e.get("acceptance_criterion"):
                errs.append(f"governance_nfrs[{i}] is missing 'acceptance_criterion'")
    status = data.get("approval_status")
    if status in {"provisional", "approved"}:
        if not data.get("approved_by"):
            errs.append(f"approval_status '{status}' requires approved_by")
        if not data.get("approved_at"):
            errs.append(f"approval_status '{status}' requires approved_at")
    if status == "deprecated" and not data.get("superseded_by"):
        errs.append("approval_status 'deprecated' requires superseded_by")
    return errs


def main(argv: list[str]) -> int:
    ap = argparse.ArgumentParser(description="Validate capability frontmatter against the schema.")
    ap.add_argument("--root", default=None, help="repo root (default: inferred)")
    args = ap.parse_args(argv)

    root = repo_root(args.root)
    cap_files = discover_capability_files(root)

    print("=" * 70)
    print("lint_capability_schema — capability frontmatter validation")
    print("=" * 70)

    if not (root / CAPABILITIES_DIR_REL).is_dir():
        print(f"FAIL: no {CAPABILITIES_DIR_REL}/ directory under {root}.", file=sys.stderr)
        return 2
    if not cap_files:
        print("No capability files found — nothing to validate.")
        return 0

    validator = make_jsonschema_validator(root)
    mode = "jsonschema (Draft 7)" if validator is not None else "stdlib structural fallback"
    domains = set(load_enum(root / DOMAINS_REL, DOMAIN_FALLBACK))
    nfr_kinds = set(load_enum(root / NFR_ENUM_REL, NFR_KIND_FALLBACK))
    print(f"validation mode: {mode}")
    print("-" * 70)

    failures = 0
    for f in cap_files:
        rel = f.relative_to(root).as_posix()
        data = parse_frontmatter(f.read_text(encoding="utf-8"))
        errs: list[str] = []
        if not data:
            errs.append("no parseable YAML frontmatter")
        elif validator is not None:
            for e in sorted(validator.iter_errors(data), key=lambda e: list(e.path)):
                loc = "/".join(str(p) for p in e.path) or "<root>"
                errs.append(f"schema at '{loc}': {e.message}")
        else:
            errs = structural_errors(data, domains, nfr_kinds)
        if errs:
            failures += 1
            print(f"FAIL  {rel}")
            for e in errs:
                print(f"        - {e}")
        else:
            print(f"PASS  {rel}")

    print("-" * 70)
    print(f"Summary: {len(cap_files) - failures}/{len(cap_files)} capability file(s) "
          f"passed; {failures} failed.")
    return 1 if failures else 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
