#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
lint_pattern_frontmatter.py — the portable pattern validator.

The same validator the `validate-patterns` GitHub Action calls AND a team runs
locally with no GitHub at all. Every check here is *deterministic* — there is no
LLM step, no network call, no database. Given a clean checkout of the Centre of
Excellence repo it parses every `patterns/**/*.md`, checks its YAML frontmatter
against the pattern schema and the closed enums, enforces the conditional
"evidence before promotion" and "deprecation points somewhere" rules, and refuses
to let a deprecated-and-still-adopted pattern be deleted.

It is intentionally **light and advisory** about *content* — it does not grade a
pattern's quality, judge its trade-offs, or gate a workflow. It only enforces the
structural contract that keeps the library legible and the downstream skills
(`recommend-component-patterns`, `propagate-pattern-nfrs`, the portfolio view)
able to trust what they read.

DESIGN: ZERO mandatory third-party dependencies.
    - YAML frontmatter is parsed with PyYAML if it is installed, otherwise with a
      small stdlib parser that handles the subset of YAML real pattern frontmatter
      uses (scalars, `>`/`|` block scalars, `key: value`, `- ` list items, and
      `- {inline: map}` entries). This means the validator runs on a bare CI
      runner or a developer laptop with `python3` and nothing else.
    - The JSON Schema (patterns/_schema/pattern.frontmatter.schema.json) is honored
      via the `jsonschema` package when both it and the file are present; otherwise
      the validator falls back to its own stdlib structural checks, which encode the
      same v1 contract. Either way the closed enums and conditional rules below are
      enforced.

USAGE
    # validate every pattern under the repo's patterns/ dir (auto-discovered):
    python3 skills/_scripts/lint_pattern_frontmatter.py

    # validate specific files (changed patterns):
    python3 skills/_scripts/lint_pattern_frontmatter.py patterns/foo.md patterns/bar.md

    # what the PR Action passes — changed/deleted path-list files + a markdown report:
    python3 skills/_scripts/lint_pattern_frontmatter.py \
        --changed-list changed_patterns.txt \
        --deleted-list deleted_patterns.txt \
        --format markdown \
        --output lint_report.md

    # point at a non-default repo root (e.g. from CI with a checkout elsewhere):
    python3 skills/_scripts/lint_pattern_frontmatter.py --repo-root "$GITHUB_WORKSPACE"

    # the never-delete-with-adoptions invariant needs the PR's deleted-file list.
    # In CI the Action computes it from the diff and passes it in; locally you can
    # too. Without it, that one check is skipped (announced, not silently dropped).
    python3 skills/_scripts/lint_pattern_frontmatter.py \
        --deleted-file patterns/old-thing.md --deleted-file patterns/gone.md

EXIT CODES
    0  every checked pattern passed
    1  at least one pattern (or the delete-invariant) failed — see per-file messages
    2  the validator could not run (e.g. no patterns/ dir, unreadable inputs)

The checks, in order (all deterministic):
    1. Parse YAML frontmatter from each patterns/**/*.md.
    2. Validate against patterns/_schema/pattern.frontmatter.schema.json:
       - required fields present
       - pattern_key matches ^PAT-[A-Z0-9]+(-[A-Z0-9]+)*$ (UPPER-KEBAB after PAT-).
         The cite-able key is independent of the (human-readable, lower-kebab)
         FILENAME — this validator does NOT require pattern_key == filename stem.
       - category    in {deployment, integration, data}
       - approval_status in {candidate, provisional, approved, deprecated}
       - valid_from / sunset_at parseable ISO dates
       - constraints[].enforced in {hard, soft}
    3. Every attached_nfrs[].kind in the closed 11-value enum, sourced from
       patterns/_schema/nfr-kinds.enum.txt or nfrs/nfr-kinds.md (with a built-in
       fallback so the validator still runs before those files land).
    4. CONDITIONAL:
       - approval_status in {provisional, approved} requires approved_by +
         approved_at + at least one evidence[] entry, each evidence entry a
         {title, url} mapping.
       - approval_status == deprecated requires superseded_by.
    5. The never-delete-with-adoptions invariant: a pattern referenced in
       adoptions/ledger.jsonl must not be deleted in the diff. The ledger is read
       via the ONE shared reader (iter_ledger_records) that the pattern-lifecycle
       workflow imports too, so both agree on what an adoption is.
"""

from __future__ import annotations

import argparse
import json
import os
import re
import sys
from datetime import date, datetime
from pathlib import Path

# --------------------------------------------------------------------------- #
# Constants — the closed contract. Keep these in lockstep with
# author-component-pattern/SKILL.md and the schema file.
# --------------------------------------------------------------------------- #

CATEGORY_ENUM = {"deployment", "integration", "data"}
APPROVAL_STATUS_ENUM = {"candidate", "provisional", "approved", "deprecated"}
ENFORCED_ENUM = {"hard", "soft"}
# Optional reference_implementations[].kind enum — mirrors the schema's enum.
# ADVISORY ONLY. A reference_implementation is a "start here" forward pointer
# (an IaC repo / app skeleton / notebook / scaffold to clone from); it is NOT
# evidence and it NEVER gates approval. The promotion gate runs through
# evidence[] exclusively (see check_conditional_rules) — this field is
# deliberately validated for SHAPE here and is touched by NOTHING in the
# conditional/promotion rules. A working IaC repo strengthens confidence; if it
# is also a real build it is listed AGAIN under evidence[] (kind:repo), and that
# entry — not this one — promotes the pattern, through the existing door.
REFIMPL_KIND_ENUM = {"iac", "app", "notebook", "scaffold"}
# Optional evidence[].kind classifier — mirrors the schema's evidence.kind enum.
EVIDENCE_KIND_HINT = {
    "repo",
    "pull_request",
    "runbook",
    "adr",
    "dashboard",
    "load_test",
    "post_mortem",
    "doc",
}

# pattern_key shape — the SINGLE source is the schema regex. UPPER-KEBAB after the
# PAT- prefix, e.g. PAT-WEBAPP-PG. The key is cite-able and survives renames; the
# FILENAME stays human-readable lower-kebab and is NOT required to equal the key.
PATTERN_KEY_RE = re.compile(r"^PAT-[A-Z0-9]+(-[A-Z0-9]+)*$")

# The closed 11-value NFR `kind` enum. This is the *fallback*; the authoritative
# source is patterns/_schema/nfr-kinds.enum.txt (or nfrs/nfr-kinds.md), read at
# runtime so the enum lives in one editable place. Kept here verbatim so the
# validator still works before those files exist.
NFR_KIND_FALLBACK = [
    "security",
    "availability",
    "performance",
    "data-residency",
    "observability",
    "resilience",
    "cost",
    "compliance",
    "scalability",
    "data-governance",
    "operations",
]

# Fields every pattern must carry (the schema's "required"). Mirrors the REQUIRED
# table in author-component-pattern/SKILL.md.
REQUIRED_FIELDS = [
    "pattern_key",
    "name",
    "category",
    "intent",
    "deployment_topology",
    "data_placement",
    "summary",
    "approval_status",
    "valid_from",
    "attached_nfrs",
]

# approval_status values at or above which evidence/approval are required.
PROMOTED_STATUSES = {"provisional", "approved"}

SCHEMA_REL = "patterns/_schema/pattern.frontmatter.schema.json"
NFR_ENUM_REL = "patterns/_schema/nfr-kinds.enum.txt"
NFR_MD_REL = "nfrs/nfr-kinds.md"
ADOPTIONS_LEDGER_REL = "adoptions/ledger.jsonl"
PATTERNS_DIR_REL = "patterns"


# --------------------------------------------------------------------------- #
# Result accumulation — collect every problem per file, report them all at once
# so a contributor fixes the whole batch in one pass rather than whack-a-mole.
# --------------------------------------------------------------------------- #


class FileReport:
    """Errors (and informational notes) accumulated for a single file."""

    def __init__(self, path: str):
        self.path = path
        self.errors: list[str] = []
        self.notes: list[str] = []

    def error(self, msg: str) -> None:
        self.errors.append(msg)

    def note(self, msg: str) -> None:
        self.notes.append(msg)

    @property
    def ok(self) -> bool:
        return not self.errors


# --------------------------------------------------------------------------- #
# Frontmatter extraction + YAML parse (PyYAML if present, stdlib subset if not)
# --------------------------------------------------------------------------- #

_FRONTMATTER_RE = re.compile(
    r"\A﻿?---[ \t]*\r?\n(.*?\n?)^---[ \t]*\r?$",
    re.DOTALL | re.MULTILINE,
)


def extract_frontmatter_block(text: str) -> str | None:
    """Return the raw YAML between the leading `---` fences, or None if absent.

    Pattern files begin with a YAML frontmatter block delimited by `---` lines.
    Tolerates a leading BOM and CRLF line endings.
    """
    m = _FRONTMATTER_RE.match(text)
    if not m:
        return None
    return m.group(1)


def _try_pyyaml(block: str):
    try:
        import yaml  # type: ignore
    except Exception:
        return (False, None)
    try:
        return (True, yaml.safe_load(block))
    except Exception as exc:  # surface a parse error as a normal validation error
        raise FrontmatterParseError(f"PyYAML could not parse frontmatter: {exc}")


class FrontmatterParseError(Exception):
    pass


def _coerce_scalar(raw: str):
    """Best-effort scalar coercion for the stdlib fallback parser."""
    s = raw.strip()
    if s == "" or s == "~" or s.lower() == "null":
        return None
    if (len(s) >= 2) and s[0] in "\"'" and s[-1] == s[0]:
        return s[1:-1]
    low = s.lower()
    if low == "true":
        return True
    if low == "false":
        return False
    # leave numbers as strings unless clearly int/float — dates must stay strings
    if re.fullmatch(r"-?\d+", s):
        return int(s)
    if re.fullmatch(r"-?\d+\.\d+", s):
        return float(s)
    # strip a trailing inline comment on a plain scalar (e.g. `candidate   # note`)
    s = re.sub(r"\s+#.*$", "", s).strip()
    return s


def _parse_inline_map(s: str) -> dict:
    """Parse `{a: 1, b: two}` — the inline-map form used by attached_nfrs entries."""
    inner = s.strip()
    if inner.startswith("{") and inner.endswith("}"):
        inner = inner[1:-1]
    out: dict = {}
    # split on commas that are not inside quotes
    parts = re.split(r",(?=(?:[^\"']*[\"'][^\"']*[\"'])*[^\"']*$)", inner)
    for part in parts:
        part = part.strip()
        if not part:
            continue
        if ":" not in part:
            continue
        k, _, v = part.partition(":")
        out[k.strip().strip("\"'")] = _coerce_scalar(v)
    return out


def _stdlib_yaml_subset(block: str):
    """A small, forgiving YAML parser for the subset pattern frontmatter uses.

    Handles, by indentation:
      key: value
      key: >            (and `|`) folded/literal block scalars
      key:
        - scalar
        - {inline: map}
        - key: value     (a mapping list item over multiple lines)
      key:
        subkey: value    (a nested mapping)

    This is deliberately NOT a general YAML engine. It exists so the validator
    runs with zero pip installs. If PyYAML is available it is always preferred.
    """

    lines = block.splitlines()
    # strip trailing blank lines
    while lines and lines[-1].strip() == "":
        lines.pop()

    pos = 0
    n = len(lines)

    def indent_of(line: str) -> int:
        return len(line) - len(line.lstrip(" "))

    def is_blank_or_comment(line: str) -> bool:
        stripped = line.strip()
        return stripped == "" or stripped.startswith("#")

    def parse_block(min_indent: int):
        """Parse a mapping or list at >= min_indent; return (value, new_pos)."""
        nonlocal pos
        # decide mapping vs list by the first significant line at this indent
        while pos < n and is_blank_or_comment(lines[pos]):
            pos += 1
        if pos >= n:
            return ({}, pos)
        first = lines[pos]
        cur_indent = indent_of(first)
        if cur_indent < min_indent:
            return ({}, pos)

        if first.lstrip().startswith("- "):
            return parse_list(cur_indent)
        return parse_mapping(cur_indent)

    def parse_mapping(indent: int):
        nonlocal pos
        result: dict = {}
        while pos < n:
            line = lines[pos]
            if is_blank_or_comment(line):
                pos += 1
                continue
            cur = indent_of(line)
            if cur < indent:
                break
            if cur > indent:
                # unexpected deeper line without a key — bail to caller
                break
            stripped = line.strip()
            if stripped.startswith("- "):
                break  # a list under the same indent belongs to the parent
            if ":" not in stripped:
                pos += 1
                continue
            key, _, rest = stripped.partition(":")
            key = key.strip()
            rest = rest.strip()
            pos += 1
            if rest in (">", "|", ">-", "|-", ">+", "|+"):
                result[key] = parse_block_scalar(indent)
            elif rest == "":
                # nested mapping or list on following deeper lines
                child, _ = peek_child(indent)
                if child is None:
                    result[key] = None
                else:
                    result[key], _ = parse_block(indent + 1)
            else:
                if rest.startswith("{") or rest.startswith("["):
                    result[key] = _parse_inline_map(rest)
                else:
                    result[key] = _coerce_scalar(rest)
        return (result, pos)

    def peek_child(parent_indent: int):
        """Look ahead: is there a deeper line that is this key's child block?"""
        p = pos
        while p < n and is_blank_or_comment(lines[p]):
            p += 1
        if p >= n:
            return (None, p)
        if indent_of(lines[p]) > parent_indent:
            return (lines[p], p)
        return (None, p)

    def parse_list(indent: int):
        nonlocal pos
        items: list = []
        while pos < n:
            line = lines[pos]
            if is_blank_or_comment(line):
                pos += 1
                continue
            cur = indent_of(line)
            if cur < indent:
                break
            stripped = line.strip()
            if not stripped.startswith("- "):
                break
            content = stripped[2:].strip()
            pos += 1
            if content.startswith("{") or content.startswith("["):
                items.append(_parse_inline_map(content))
            elif ":" in content and not (
                content[0] in "\"'" and content.count(":") == 0
            ):
                # a mapping list item: first key inline, more keys on deeper lines
                item: dict = {}
                key, _, rest = content.partition(":")
                key = key.strip()
                rest = rest.strip()
                if rest in (">", "|", ">-", "|-"):
                    item[key] = parse_block_scalar(indent)
                elif rest == "":
                    child, _ = peek_child(indent)
                    if child is not None:
                        sub, _ = parse_block(indent + 2)
                        if isinstance(sub, dict):
                            item[key] = sub
                        else:
                            item[key] = sub
                else:
                    item[key] = (
                        _parse_inline_map(rest)
                        if rest.startswith("{")
                        else _coerce_scalar(rest)
                    )
                # consume any further deeper mapping lines belonging to this item
                more, _ = parse_trailing_map_keys(indent)
                item.update(more)
                items.append(item)
            else:
                items.append(_coerce_scalar(content))
        return (items, pos)

    def parse_trailing_map_keys(list_indent: int):
        """Consume `key: value` lines indented deeper than the `- ` marker."""
        nonlocal pos
        result: dict = {}
        marker_child_indent = list_indent + 2
        while pos < n:
            line = lines[pos]
            if is_blank_or_comment(line):
                pos += 1
                continue
            cur = indent_of(line)
            if cur < marker_child_indent:
                break
            stripped = line.strip()
            if stripped.startswith("- "):
                break
            if ":" not in stripped:
                pos += 1
                continue
            key, _, rest = stripped.partition(":")
            key = key.strip()
            rest = rest.strip()
            pos += 1
            if rest in (">", "|", ">-", "|-"):
                result[key] = parse_block_scalar(cur)
            elif rest == "":
                result[key] = None
            else:
                result[key] = (
                    _parse_inline_map(rest)
                    if rest.startswith("{")
                    else _coerce_scalar(rest)
                )
        return (result, pos)

    def parse_block_scalar(parent_indent: int) -> str:
        nonlocal pos
        collected: list[str] = []
        base_indent = None
        while pos < n:
            line = lines[pos]
            if line.strip() == "":
                collected.append("")
                pos += 1
                continue
            cur = indent_of(line)
            if cur <= parent_indent:
                break
            if base_indent is None:
                base_indent = cur
            collected.append(line[base_indent:])
            pos += 1
        # fold to a single space-joined string (good enough for validation needs)
        text = " ".join(s.strip() for s in collected if s.strip() != "")
        return text

    value, _ = parse_block(0)
    return value


def parse_frontmatter(text: str):
    """Return a dict from the file's frontmatter (PyYAML preferred, stdlib fallback).

    Raises FrontmatterParseError on a missing block or a non-mapping top level.
    """
    block = extract_frontmatter_block(text)
    if block is None:
        raise FrontmatterParseError(
            "no YAML frontmatter found (a pattern must begin with a '---' fenced block)"
        )
    used_pyyaml, data = _try_pyyaml(block)
    if not used_pyyaml:
        data = _stdlib_yaml_subset(block)
    if data is None:
        raise FrontmatterParseError("frontmatter block is empty")
    if not isinstance(data, dict):
        raise FrontmatterParseError(
            "frontmatter must be a YAML mapping (key: value), got "
            f"{type(data).__name__}"
        )
    return data


# --------------------------------------------------------------------------- #
# Date parsing (ISO 8601 calendar dates; tolerant of a full timestamp)
# --------------------------------------------------------------------------- #


def parse_iso_date(value) -> date | None:
    """Return a date for an ISO 'YYYY-MM-DD' (or full timestamp), else None.

    PyYAML may have already coerced a bare date to a datetime/date; handle both.
    """
    if isinstance(value, datetime):
        return value.date()
    if isinstance(value, date):
        return value
    if not isinstance(value, str):
        return None
    s = value.strip()
    if not s:
        return None
    # accept date-only or a leading date in a timestamp
    m = re.match(r"^(\d{4})-(\d{2})-(\d{2})", s)
    if not m:
        return None
    try:
        return date(int(m.group(1)), int(m.group(2)), int(m.group(3)))
    except ValueError:
        return None


# --------------------------------------------------------------------------- #
# Enum / schema source loading
# --------------------------------------------------------------------------- #


def load_nfr_kind_enum(repo_root: Path, report_sink: list[str]) -> list[str]:
    """Load the closed NFR-kind enum from its authoritative file, else fall back.

    Source priority:
      1. patterns/_schema/nfr-kinds.enum.txt  (one kind per line, '#'-comments ok)
      2. nfrs/nfr-kinds.md                    (extract `code`-fenced / list tokens)
      3. the built-in NFR_KIND_FALLBACK
    """
    enum_txt = repo_root / NFR_ENUM_REL
    if enum_txt.is_file():
        kinds: list[str] = []
        for line in enum_txt.read_text(encoding="utf-8").splitlines():
            line = line.split("#", 1)[0].strip()
            if line:
                kinds.append(line)
        if kinds:
            return kinds
        report_sink.append(f"{NFR_ENUM_REL} is present but empty; using fallback enum.")

    nfr_md = repo_root / NFR_MD_REL
    if nfr_md.is_file():
        text = nfr_md.read_text(encoding="utf-8")
        # pull tokens that look like kebab/word kinds out of inline-code or list lines
        found: list[str] = []
        for tok in re.findall(r"`([a-z][a-z0-9-]+)`", text):
            if tok in NFR_KIND_FALLBACK and tok not in found:
                found.append(tok)
        if found:
            return found
        report_sink.append(
            f"{NFR_MD_REL} found but no recognizable kind tokens; using fallback enum."
        )

    report_sink.append(
        "NFR-kind enum source not found "
        f"({NFR_ENUM_REL} / {NFR_MD_REL}); using the built-in 11-value fallback."
    )
    return list(NFR_KIND_FALLBACK)


def load_schema(repo_root: Path, report_sink: list[str]):
    """Return (validator_callable_or_None, schema_dict_or_None).

    If both the schema file AND the `jsonschema` package are present, returns a
    jsonschema validator. Otherwise returns (None, schema_or_None) and the caller
    uses the stdlib structural checks, which encode the same contract.
    """
    schema_path = repo_root / SCHEMA_REL
    schema = None
    if schema_path.is_file():
        try:
            schema = json.loads(schema_path.read_text(encoding="utf-8"))
        except Exception as exc:
            report_sink.append(f"{SCHEMA_REL} present but not valid JSON ({exc}); "
                               "using stdlib structural checks.")
            schema = None
    else:
        report_sink.append(
            f"{SCHEMA_REL} not found; using built-in stdlib structural checks "
            "(same v1 contract)."
        )

    if schema is not None:
        try:
            import jsonschema  # type: ignore

            validator = jsonschema.Draft7Validator(schema)
            return (validator, schema)
        except Exception:
            report_sink.append(
                "jsonschema package not installed; honoring the schema file via "
                "stdlib structural checks instead."
            )
    return (None, schema)


# --------------------------------------------------------------------------- #
# The validation checks
# --------------------------------------------------------------------------- #


def check_required_and_enums(data: dict, rep: FileReport, nfr_kinds: set[str]) -> None:
    """Steps 2 + 3: required fields, the closed enums, dates, NFR kinds."""

    # required fields present (and not empty)
    for field in REQUIRED_FIELDS:
        if field not in data or data[field] in (None, "", []):
            rep.error(f"missing required field '{field}'")

    # category
    cat = data.get("category")
    if cat is not None and cat not in CATEGORY_ENUM:
        rep.error(
            f"category '{cat}' is not one of {sorted(CATEGORY_ENUM)}"
        )

    # approval_status
    status = data.get("approval_status")
    if status is not None and status not in APPROVAL_STATUS_ENUM:
        rep.error(
            f"approval_status '{status}' is not one of {sorted(APPROVAL_STATUS_ENUM)}"
        )

    # pattern_key shape — UPPER-KEBAB after PAT-, validated against the schema regex
    # (the single source). The cite-able key; the filename stem is independent and
    # human-readable, so we do NOT require pattern_key == stem.
    pk = data.get("pattern_key")
    if isinstance(pk, str) and pk and not PATTERN_KEY_RE.match(pk):
        rep.error(
            f"pattern_key '{pk}' must match {PATTERN_KEY_RE.pattern} "
            "(UPPER-KEBAB after the PAT- prefix, e.g. PAT-WEBAPP-PG)"
        )

    # valid_from — required + parseable
    if "valid_from" in data and data["valid_from"] not in (None, ""):
        if parse_iso_date(data["valid_from"]) is None:
            rep.error(
                f"valid_from '{data['valid_from']}' is not a parseable ISO date "
                "(YYYY-MM-DD)"
            )

    # sunset_at — optional, but parseable when present
    if data.get("sunset_at") not in (None, ""):
        if parse_iso_date(data["sunset_at"]) is None:
            rep.error(
                f"sunset_at '{data['sunset_at']}' is not a parseable ISO date "
                "(YYYY-MM-DD)"
            )

    # constraints[].enforced in {hard, soft}
    constraints = data.get("constraints")
    if constraints is not None:
        if not isinstance(constraints, list):
            rep.error("constraints must be a list of {statement, enforced} entries")
        else:
            for i, c in enumerate(constraints, start=1):
                if not isinstance(c, dict):
                    rep.error(f"constraints[{i}] must be a mapping, got {type(c).__name__}")
                    continue
                enforced = c.get("enforced")
                if enforced is None:
                    rep.error(f"constraints[{i}] is missing 'enforced' (hard|soft)")
                elif enforced not in ENFORCED_ENUM:
                    rep.error(
                        f"constraints[{i}].enforced '{enforced}' is not one of "
                        f"{sorted(ENFORCED_ENUM)}"
                    )
                if not c.get("statement"):
                    rep.error(f"constraints[{i}] is missing a 'statement'")

    # attached_nfrs[].kind in the closed 11-value enum
    nfrs = data.get("attached_nfrs")
    if nfrs is not None:
        if not isinstance(nfrs, list):
            rep.error(
                "attached_nfrs must be a list of {kind, statement, acceptance_criterion}"
            )
        elif len(nfrs) == 0:
            rep.error(
                "attached_nfrs is empty — a pattern must carry at least one governed NFR"
            )
        else:
            for i, nfr in enumerate(nfrs, start=1):
                if not isinstance(nfr, dict):
                    rep.error(
                        f"attached_nfrs[{i}] must be a mapping, got {type(nfr).__name__}"
                    )
                    continue
                kind = nfr.get("kind")
                if kind is None:
                    rep.error(f"attached_nfrs[{i}] is missing 'kind'")
                elif kind not in nfr_kinds:
                    rep.error(
                        f"attached_nfrs[{i}].kind '{kind}' is not in the closed "
                        f"{len(nfr_kinds)}-value NFR enum {sorted(nfr_kinds)}"
                    )
                if not nfr.get("statement"):
                    rep.error(f"attached_nfrs[{i}] is missing a 'statement'")
                if not nfr.get("acceptance_criterion"):
                    rep.error(
                        f"attached_nfrs[{i}] is missing an 'acceptance_criterion' "
                        "(an NFR with no way to verify it is a wish, not a bar)"
                    )

    # reference_implementations[] — OPTIONAL forward pointers (a "start here"
    # IaC repo / app skeleton / notebook / scaffold to clone from). Validate
    # SHAPE + the kind enum here, and emit an ADVISORY staleness note. This block
    # is intentionally OUT of check_conditional_rules: a reference_implementation
    # is NOT evidence and NEVER gates approval — the promotion gate runs through
    # evidence[] alone. A real build is listed AGAIN under evidence[] (kind:repo)
    # and THAT entry promotes the pattern. So a malformed reference_implementation
    # is a structural error (it must be cite-able), but a placeholder/unverified
    # one is only an advisory note, never a promotion blocker.
    refimpls = data.get("reference_implementations")
    if refimpls is not None:
        if not isinstance(refimpls, list):
            rep.error(
                "reference_implementations must be a list of "
                "{kind, url, provisions} entries"
            )
        else:
            for i, ri in enumerate(refimpls, start=1):
                if not isinstance(ri, dict):
                    rep.error(
                        f"reference_implementations[{i}] must be a mapping, got "
                        f"{type(ri).__name__}"
                    )
                    continue
                kind = ri.get("kind")
                if kind is None:
                    rep.error(
                        f"reference_implementations[{i}] is missing 'kind' "
                        f"({'|'.join(sorted(REFIMPL_KIND_ENUM))})"
                    )
                elif kind not in REFIMPL_KIND_ENUM:
                    rep.error(
                        f"reference_implementations[{i}].kind '{kind}' is not one "
                        f"of {sorted(REFIMPL_KIND_ENUM)}"
                    )
                if not ri.get("url"):
                    rep.error(
                        f"reference_implementations[{i}] is missing a 'url' "
                        "(the link to the artefact to start from)"
                    )
                if not ri.get("provisions"):
                    rep.error(
                        f"reference_implementations[{i}] is missing 'provisions' "
                        "(what it targets — free-text, e.g. 'azure', 'aws')"
                    )
                # ADVISORY ONLY: flag an obvious placeholder / replace-me URL so a
                # CODEOWNER knows to swap it for the real repo before approval.
                # NEVER an error and NEVER a gate — a candidate pattern may carry a
                # placeholder reference_implementation; promotion runs through
                # evidence[], not this field.
                url = ri.get("url")
                if isinstance(url, str) and url:
                    low = url.lower()
                    if "replace-me" in low or "replace_me" in low or "/org/" in low:
                        rep.note(
                            f"reference_implementations[{i}].url '{url}' looks like a "
                            "placeholder — a CODEOWNER should replace it with the real "
                            "repo before approval (advisory; not evidence, not a gate)."
                        )


def check_conditional_rules(data: dict, rep: FileReport) -> None:
    """Step 4: the promotion/evidence and deprecation conditional requirements."""
    status = data.get("approval_status")

    if status in PROMOTED_STATUSES:
        if not data.get("approved_by"):
            rep.error(
                f"approval_status '{status}' requires 'approved_by' "
                "(who ratified it — a CODEOWNER; the agent never sets this)"
            )
        if not data.get("approved_at"):
            rep.error(
                f"approval_status '{status}' requires 'approved_at' (when it was ratified)"
            )
        elif parse_iso_date(data["approved_at"]) is None:
            rep.error(
                f"approved_at '{data['approved_at']}' is not a parseable ISO date "
                "(YYYY-MM-DD)"
            )
        evidence = data.get("evidence")
        if not isinstance(evidence, list) or len(evidence) == 0:
            rep.error(
                f"approval_status '{status}' requires at least one evidence[] entry "
                "(the artefacts proving it was built — repo/pull_request/runbook/adr/"
                "dashboard/load_test/post_mortem/doc). No evidence, no promotion."
            )
        else:
            for i, ev in enumerate(evidence, start=1):
                if not isinstance(ev, dict):
                    rep.error(
                        f"evidence[{i}] must be a mapping {{title, url}}, got "
                        f"{type(ev).__name__}"
                    )
                    continue
                if not ev.get("title"):
                    rep.error(
                        f"evidence[{i}] is missing a 'title' (what the artefact is)"
                    )
                if not ev.get("url"):
                    rep.error(
                        f"evidence[{i}] is missing a 'url' (the link to the artefact)"
                    )

    if status == "deprecated":
        if not data.get("superseded_by"):
            rep.error(
                "approval_status 'deprecated' requires 'superseded_by' — point "
                "adopters at where to go instead; never deprecate into a dead end"
            )


def note_filename(path: Path, data: dict, rep: FileReport) -> None:
    """Informational only. The cite-able key is `pattern_key` (UPPER-KEBAB); the
    FILENAME is independent and human-readable lower-kebab. We do NOT require
    pattern_key == filename stem — they are deliberately different shapes. This
    records the pairing as a note for legibility, never an error.
    """
    pk = data.get("pattern_key")
    if isinstance(pk, str) and pk:
        rep.note(f"pattern_key '{pk}' (file: {path.name})")


# --------------------------------------------------------------------------- #
# Step 5: the never-delete-with-adoptions invariant
# --------------------------------------------------------------------------- #


# Fields a ledger line may carry the adopted pattern_key under (canonical first).
LEDGER_KEY_FIELDS = ("pattern_key", "pattern", "adopted_pattern_key")


def iter_ledger_records(repo_root: Path, problems: list[str] | None = None):
    """THE one ledger reader. Yield (lineno, dict) for every JSON object in
    adoptions/ledger.jsonl, skipping blank lines and appending a message to
    `problems` for any line that is not valid JSON / not an object.

    This is the single shared parser used by BOTH this linter and the
    pattern-lifecycle workflow (which imports it), so the never-delete invariant
    and the maturity tally read the ledger identically. The ledger is PURE JSONL
    — one JSON object per line, no comment header (the prose lives in
    adoptions/README.md). A blank line is tolerated; anything else that fails to
    parse is reported, never silently dropped.
    """
    if problems is None:
        problems = []
    ledger = repo_root / ADOPTIONS_LEDGER_REL
    if not ledger.is_file():
        problems.append(
            f"{ADOPTIONS_LEDGER_REL} not found; treated as empty (adopted-by-zero)."
        )
        return
    for lineno, raw in enumerate(ledger.read_text(encoding="utf-8").splitlines(), 1):
        s = raw.strip()
        if not s:
            continue
        try:
            obj = json.loads(s)
        except json.JSONDecodeError as exc:
            problems.append(f"{ADOPTIONS_LEDGER_REL}:{lineno} is not valid JSON ({exc}).")
            continue
        if not isinstance(obj, dict):
            problems.append(f"{ADOPTIONS_LEDGER_REL}:{lineno} is not a JSON object; skipped.")
            continue
        yield lineno, obj


def ledger_pattern_key(obj: dict) -> str | None:
    """The adopted pattern_key carried by one ledger record, or None."""
    for field in LEDGER_KEY_FIELDS:
        val = obj.get(field)
        if isinstance(val, str) and val:
            return val
    return None


def load_adopted_pattern_keys(repo_root: Path, report_sink: list[str]) -> set[str]:
    """Return the set of pattern_keys that appear in adoptions/ledger.jsonl.

    Built on the shared `iter_ledger_records` reader. A pattern referenced here
    has real provenance that must survive a delete.
    """
    keys: set[str] = set()
    for _lineno, obj in iter_ledger_records(repo_root, report_sink):
        key = ledger_pattern_key(obj)
        if key:
            keys.add(key)
    return keys


def pattern_key_from_path(repo_root: Path, deleted_rel: str) -> str:
    """The pattern_key a deleted patterns/**/*.md file would have carried (its stem)."""
    return Path(deleted_rel).stem


def check_delete_invariant(
    repo_root: Path,
    deleted_files: list[str],
    adopted_keys: set[str],
    report_sink: list[str],
) -> list[str]:
    """Return a list of failure messages for any deleted-but-adopted pattern.

    A pattern that is referenced in the adoptions ledger must not be *deleted* in
    a diff — even if it is deprecated. Deprecate-don't-delete: the provenance has
    to survive. (Renames/moves should keep the file, just flip status; a true
    delete erases the record adopters point back to.)
    """
    if not deleted_files:
        report_sink.append(
            "no --deleted-file inputs supplied; the never-delete-with-adoptions "
            "check is skipped (CI supplies the diff's deleted paths)."
        )
        return []

    failures: list[str] = []
    for rel in deleted_files:
        rel_norm = rel.replace("\\", "/").lstrip("./")
        # only patterns/**/*.md deletions are in scope for this invariant
        if not (rel_norm.startswith(PATTERNS_DIR_REL + "/") and rel_norm.endswith(".md")):
            continue
        if "/_schema/" in rel_norm:
            continue
        key = pattern_key_from_path(repo_root, rel_norm)
        if key in adopted_keys:
            failures.append(
                f"{rel_norm}: DELETE BLOCKED — pattern '{key}' is referenced in "
                f"{ADOPTIONS_LEDGER_REL}; a pattern with adoptions must not be "
                "deleted. Deprecate it instead (approval_status: deprecated + "
                "superseded_by) so the provenance survives."
            )
    return failures


# --------------------------------------------------------------------------- #
# Optional: honor a jsonschema validator's findings as well
# --------------------------------------------------------------------------- #


def apply_jsonschema(validator, data: dict, rep: FileReport) -> None:
    """Fold any jsonschema errors into the file report (belt-and-braces).

    The stdlib checks above are authoritative; this adds whatever extra the
    repo's schema file pins down (e.g. additionalProperties, formats).
    """
    if validator is None:
        return
    try:
        errors = sorted(validator.iter_errors(data), key=lambda e: list(e.path))
    except Exception as exc:
        rep.note(f"jsonschema validation could not run: {exc}")
        return
    for err in errors:
        loc = "/".join(str(p) for p in err.path) or "<root>"
        rep.error(f"schema: at '{loc}': {err.message}")


# --------------------------------------------------------------------------- #
# Pattern file discovery
# --------------------------------------------------------------------------- #


def discover_pattern_files(repo_root: Path) -> list[Path]:
    patterns_dir = repo_root / PATTERNS_DIR_REL
    if not patterns_dir.is_dir():
        return []
    out: list[Path] = []
    for p in sorted(patterns_dir.rglob("*.md")):
        rel_parts = p.relative_to(patterns_dir).parts
        # skip the schema tree (patterns/_schema/**) — it is scaffolding, not a pattern.
        if "_schema" in set(rel_parts):
            continue
        # skip the copy-me scaffold (patterns/_TEMPLATE.md) and any other leading-
        # underscore scaffold file: these are intentionally incomplete (no name,
        # no NFRs) and must NOT be linted as real patterns, or the bare documented
        # command would never report green on a clean library.
        if p.name == "_TEMPLATE.md" or p.name.startswith("_"):
            continue
        # skip the prose docs that live beside the patterns.
        if p.name.lower() in {"readme.md", "contributing.md", "index.md"}:
            continue
        out.append(p)
    return out


# --------------------------------------------------------------------------- #
# Main
# --------------------------------------------------------------------------- #


def find_repo_root(start: Path) -> Path:
    """Walk up from `start` to the dir that contains a patterns/ folder (or a .git).

    Lets the script be invoked from anywhere and still locate the repo.
    """
    cur = start.resolve()
    for cand in [cur, *cur.parents]:
        if (cand / PATTERNS_DIR_REL).is_dir() or (cand / ".git").exists():
            return cand
    return start.resolve()


def validate_one(path: Path, ctx) -> FileReport:
    rep = FileReport(str(path))
    try:
        text = path.read_text(encoding="utf-8")
    except Exception as exc:
        rep.error(f"could not read file: {exc}")
        return rep
    try:
        data = parse_frontmatter(text)
    except FrontmatterParseError as exc:
        rep.error(str(exc))
        return rep

    check_required_and_enums(data, rep, ctx["nfr_kinds"])
    check_conditional_rules(data, rep)
    note_filename(path, data, rep)
    apply_jsonschema(ctx["schema_validator"], data, rep)
    return rep


def _read_path_list(list_path: str) -> list[str]:
    """Read a newline-separated list of file paths (one per line); blanks skipped.

    This is the shape the validate-patterns Action produces with `git diff
    --name-only` for the changed and deleted pattern sets.
    """
    p = Path(list_path)
    if not p.is_file():
        return []
    out: list[str] = []
    for line in p.read_text(encoding="utf-8").splitlines():
        s = line.strip()
        if s:
            out.append(s)
    return out


def render_report(
    fmt: str,
    reports: list["FileReport"],
    delete_failures: list[str],
    global_notes: list[str],
    quiet: bool,
) -> str:
    """Render the per-file results as plain text or GitHub-flavoured markdown."""
    failed = [r for r in reports if not r.ok]
    passed = [r for r in reports if r.ok]
    total = len(reports)
    n_failed = len(failed)
    lines: list[str] = []

    if fmt == "markdown":
        lines.append("### Pattern frontmatter lint")
        lines.append("")
        verdict = "clean" if not (n_failed or delete_failures) else "issues found"
        lines.append(
            f"**Summary:** {total - n_failed}/{total} pattern file(s) passed · "
            f"{n_failed} failed · {len(delete_failures)} delete-invariant "
            f"violation(s) — _{verdict}_."
        )
        lines.append("")
        if not quiet and global_notes:
            lines.append("<details><summary>Validator setup notes</summary>")
            lines.append("")
            for n in global_notes:
                lines.append(f"- {n}")
            lines.append("")
            lines.append("</details>")
            lines.append("")
        for r in failed:
            lines.append(f"- **FAIL** `{r.path}`")
            for e in r.errors:
                lines.append(f"  - {e}")
        for r in passed:
            if not quiet:
                lines.append(f"- **PASS** `{r.path}`")
                for note in r.notes:
                    lines.append(f"  - _(note)_ {note}")
        if delete_failures:
            lines.append("")
            lines.append("**Delete-invariant violations:**")
            for msg in delete_failures:
                lines.append(f"- {msg}")
        return "\n".join(lines) + "\n"

    # --- plain text ---------------------------------------------------------- #
    if not quiet and global_notes:
        lines.append("Validator setup notes:")
        for n in global_notes:
            lines.append(f"  - {n}")
        lines.append("")
    for r in failed:
        lines.append(f"FAIL  {r.path}")
        for e in r.errors:
            lines.append(f"        - {e}")
        for note in r.notes:
            lines.append(f"        (note) {note}")
    for r in passed:
        if not quiet:
            lines.append(f"PASS  {r.path}")
            for note in r.notes:
                lines.append(f"        (note) {note}")
    if delete_failures:
        lines.append("")
        lines.append("DELETE INVARIANT VIOLATIONS:")
        for msg in delete_failures:
            lines.append(f"  - {msg}")
    lines.append("")
    lines.append(
        f"Summary: {total - n_failed}/{total} pattern file(s) passed; "
        f"{n_failed} failed; {len(delete_failures)} delete-invariant violation(s)."
    )
    return "\n".join(lines) + "\n"


def main(argv: list[str]) -> int:
    parser = argparse.ArgumentParser(
        description=(
            "Validate pattern frontmatter for the SDLC Centre of Excellence. "
            "Deterministic, dependency-light, runs locally or from CI."
        )
    )
    parser.add_argument(
        "files",
        nargs="*",
        help="specific patterns/**/*.md files to validate (default: all under patterns/)",
    )
    parser.add_argument(
        "--repo-root",
        default=None,
        help="repo root (default: auto-detected by walking up to a patterns/ dir)",
    )
    parser.add_argument(
        "--deleted-file",
        action="append",
        default=[],
        dest="deleted_files",
        help=(
            "a path deleted in the PR diff (repeatable); enables the "
            "never-delete-with-adoptions invariant. CI computes these from the diff."
        ),
    )
    parser.add_argument(
        "--changed-list",
        default=None,
        help=(
            "path to a newline-separated file of changed pattern paths to validate "
            "(what the validate-patterns Action passes from `git diff --name-only`). "
            "Merged with any positional files; if neither is given, all patterns/ "
            "files are discovered."
        ),
    )
    parser.add_argument(
        "--deleted-list",
        default=None,
        help=(
            "path to a newline-separated file of deleted pattern paths (feeds the "
            "never-delete-with-adoptions invariant). Merged with any --deleted-file."
        ),
    )
    parser.add_argument(
        "--format",
        choices=["text", "markdown"],
        default="text",
        help="report format (default: text). 'markdown' is what the PR comment uses.",
    )
    parser.add_argument(
        "--output",
        default=None,
        help="write the report to this file (in addition to stdout).",
    )
    parser.add_argument(
        "--quiet",
        action="store_true",
        help="suppress the informational (non-error) notes",
    )
    args = parser.parse_args(argv)

    # --- merge positional files with --changed-list ------------------------- #
    file_args = list(args.files)
    if args.changed_list:
        file_args.extend(_read_path_list(args.changed_list))
    # --- merge --deleted-file with --deleted-list --------------------------- #
    deleted_args = list(args.deleted_files)
    if args.deleted_list:
        deleted_args.extend(_read_path_list(args.deleted_list))

    # --- locate the repo ---------------------------------------------------- #
    if args.repo_root:
        repo_root = Path(args.repo_root).resolve()
    elif file_args:
        repo_root = find_repo_root(Path(file_args[0]).resolve().parent)
    else:
        repo_root = find_repo_root(Path(__file__).resolve().parent)

    global_notes: list[str] = []

    # --- load the contract sources (schema + enums + adoptions) ------------- #
    nfr_kinds = set(load_nfr_kind_enum(repo_root, global_notes))
    schema_validator, _schema = load_schema(repo_root, global_notes)
    adopted_keys = load_adopted_pattern_keys(repo_root, global_notes)

    ctx = {
        "nfr_kinds": nfr_kinds,
        "schema_validator": schema_validator,
    }

    # --- pick the files to validate ----------------------------------------- #
    if file_args:
        files = []
        for f in file_args:
            p = Path(f)
            if not p.is_absolute():
                p = (repo_root / f).resolve() if not p.exists() else p.resolve()
            files.append(p)
    else:
        # A --changed-list that resolved to zero paths means "the PR touched no
        # pattern files" — validate nothing, exit clean (not "scan everything").
        files = [] if args.changed_list is not None else discover_pattern_files(repo_root)

    def _emit(report_text: str) -> None:
        sys.stdout.write(report_text)
        if args.output:
            try:
                Path(args.output).write_text(report_text, encoding="utf-8")
            except OSError as exc:
                print(f"WARNING: could not write --output {args.output}: {exc}",
                      file=sys.stderr)

    if not files and not deleted_args:
        patterns_dir = repo_root / PATTERNS_DIR_REL
        if args.changed_list is not None:
            # explicit empty changed-set: nothing to do, clean.
            _emit("OK: no changed pattern files to validate (nothing to do).\n")
            return 0
        if not patterns_dir.is_dir():
            print(
                f"ERROR: no patterns/ directory found under {repo_root}. "
                "Nothing to validate.",
                file=sys.stderr,
            )
            return 2
        _emit(f"OK: no pattern files found under {patterns_dir} (nothing to validate).\n")
        return 0

    # --- run per-file checks ------------------------------------------------ #
    reports = [validate_one(p, ctx) for p in files]

    # --- the never-delete-with-adoptions invariant -------------------------- #
    delete_failures = check_delete_invariant(
        repo_root, deleted_args, adopted_keys, global_notes
    )

    # --- report ------------------------------------------------------------- #
    report_text = render_report(
        args.format, reports, delete_failures, global_notes, args.quiet
    )
    _emit(report_text)

    n_failed = sum(1 for r in reports if not r.ok)
    if n_failed or delete_failures:
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
