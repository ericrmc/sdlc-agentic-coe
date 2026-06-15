#!/usr/bin/env python3
"""concat_skills.py — the combined-bundle builder for the SDLC Agentic CoE.

This is a *deterministic* concatenator. It reads a small bundle manifest, joins
the named SKILL.md / pattern .md bodies into single clean-markdown files, and
writes them under ``generated/``. There is **no LLM step** — running it twice on
the same inputs produces byte-identical output, so the ``concat-patterns`` GitHub
Action can regenerate bundles on every push and the diff is always meaningful.

Why bundles exist
-----------------
The CoE keeps each skill and each component pattern as its own small,
PR-reviewable markdown file (good for authoring + review). But an LLM workflow
often wants the *whole* method in one paste-able file — e.g. the full adversarial
review pass, or the complete solution-design author + reconcile loop. This script
materialises those combined views without anyone hand-maintaining a giant file.

Everything written under ``generated/`` is marked ``linguist-generated`` (see the
repo ``.gitattributes``) and carries a DO-NOT-EDIT header. Edit the *sources*, not
the bundles.

Usage
-----
    python skills/_scripts/concat_skills.py            # build every bundle
    python skills/_scripts/concat_skills.py --check    # build, fail if out of date
    python skills/_scripts/concat_skills.py --manifest path/to/bundles.yml

The default manifest path is ``skills/_scripts/bundles.yml`` (a tiny YAML file).
If that file is absent, the built-in ``DEFAULT_BUNDLES`` below is used so the v1
bundles always build out of the box.

Manifest shape (YAML)
---------------------
    bundles:
      - out: combined/adversarial-review.combined.md
        title: Adversarial Review — combined pass
        intro: >
          Run these three skills in order to red-team a requirement set...
        parts:
          - skills/challenge/red-team-requirements/SKILL.md
          - skills/panel/design-review-findings/SKILL.md
          - skills/panel/red-team-and-dissent/SKILL.md

The script is intentionally dependency-light. YAML is parsed with PyYAML if it is
installed; otherwise a tiny built-in parser handles the simple subset this
manifest uses (so CI needs no extra install). Missing source files are reported
clearly and (unless ``--allow-missing``) cause a non-zero exit.
"""

from __future__ import annotations

import argparse
import datetime as _dt
import sys
from dataclasses import dataclass, field
from pathlib import Path

# ---------------------------------------------------------------------------
# Paths. Resolve relative to the repo root (two levels up from this file:
# skills/_scripts/concat_skills.py -> repo root), NOT the process CWD, so the
# Action and a local run behave identically regardless of where it is invoked.
# ---------------------------------------------------------------------------

_THIS = Path(__file__).resolve()
REPO_ROOT = _THIS.parents[2]          # .../sdlc-agentic-coe
SKILLS_DIR = REPO_ROOT / "skills"
GENERATED_DIR = REPO_ROOT / "generated"
DEFAULT_MANIFEST = SKILLS_DIR / "_scripts" / "bundles.yml"


# ---------------------------------------------------------------------------
# Bundle model.
# ---------------------------------------------------------------------------

@dataclass
class Bundle:
    out: str                      # path under generated/, e.g. combined/foo.md
    title: str
    intro: str = ""               # short prose shown under the header
    parts: list[str] = field(default_factory=list)  # source paths, repo-relative


# The three v1 bundles, baked in so the repo builds with no manifest present.
# Every path below resolves to a REAL on-disk file (the named-category skill
# layout + the category-foldered pattern library); keep them in sync if a
# skill/pattern is moved or renamed. These bundle the method:
#   - adversarial review  = red-team requirements + design-review findings
#                            + red-team & dissent  (the advisory red-team pass)
#   - solution design     = synthesise architecture + the frozen-8 section
#                            reference + reconcile design-vs-requirements
#   - component patterns  = the whole component-pattern catalogue, one entry per
#                            category (deployment / integration / data).
DEFAULT_BUNDLES: list[Bundle] = [
    Bundle(
        out="combined/adversarial-review.combined.md",
        title="Adversarial Review — combined pass",
        intro=(
            "A single paste-able file for the full advisory red-team pass over a "
            "project. Run the three skills in order: challenge the requirements, "
            "surface design-review findings (a11y/WCAG, risks, gaps — findings, "
            "never verdicts), then capture the strongest objections and the "
            "dissent that should be recorded even where the project proceeds. "
            "Everything here is advisory: it produces findings and a dissent "
            "register, not gates or approvals."
        ),
        parts=[
            "skills/challenge/red-team-requirements/SKILL.md",
            "skills/panel/design-review-findings/SKILL.md",
            "skills/panel/red-team-and-dissent/SKILL.md",
        ],
    ),
    Bundle(
        out="combined/solution-design.combined.md",
        title="Solution Design — combined author + reconcile loop",
        intro=(
            "The end-to-end solution-architecture authoring method in one file. "
            "Start with the synthesise-solution-architecture skill (read the "
            "codebase + context, then author the document as the frozen-8 "
            "sections), keep the frozen-8 section reference alongside it so every "
            "section has a precise target, and close with "
            "reconcile-design-vs-requirements to check the authored design back "
            "against the requirement set. Advisory throughout — reconcile reports "
            "drift, it does not block."
        ),
        parts=[
            "skills/architect/synthesise-solution-architecture/SKILL.md",
            "references/frozen-8-sections.md",
            "skills/architect/reconcile-design-vs-requirements/SKILL.md",
        ],
    ),
    Bundle(
        out="combined/component-patterns.combined.md",
        title="Component patterns — combined catalogue",
        intro=(
            "The whole component-pattern library in one paste-able file, one entry "
            "per category (deployment / integration / data). Each entry keeps its "
            "own pattern_key, approval_status, validity / review-by metadata, "
            "attached NFRs and evidence in its frontmatter — read those before "
            "adopting. Superseded or deprecated patterns are still included so you "
            "can see what replaced what; check the status field. This is a "
            "generated view; PR-review and edit the individual pattern files, not "
            "this bundle."
        ),
        parts=[
            "patterns/deployment/containerised-web-managed-postgres.md",
            "patterns/integration/api-gateway-bff-managed-identity.md",
            "patterns/data/databricks-lakehouse-delta.md",
        ],
    ),
]


# ---------------------------------------------------------------------------
# Minimal YAML loading for the manifest (PyYAML if present; else a tiny parser
# for the small subset the manifest uses). Keeps CI dependency-free.
# ---------------------------------------------------------------------------

def _load_manifest(path: Path) -> list[Bundle]:
    """Parse the bundle manifest into Bundle objects.

    Falls back to DEFAULT_BUNDLES when the manifest file does not exist.
    """
    if not path.exists():
        return DEFAULT_BUNDLES

    text = path.read_text(encoding="utf-8")

    data = None
    try:
        import yaml  # type: ignore

        data = yaml.safe_load(text)
    except Exception:
        data = _tiny_yaml_bundles(text)

    if not data or "bundles" not in data:
        raise SystemExit(
            f"manifest {path} has no 'bundles:' key; "
            "expected a top-level 'bundles' list"
        )

    bundles: list[Bundle] = []
    for raw in data["bundles"]:
        bundles.append(
            Bundle(
                out=str(raw["out"]).strip(),
                title=str(raw.get("title", raw["out"])).strip(),
                intro=str(raw.get("intro", "")).strip(),
                parts=[str(p).strip() for p in raw.get("parts", [])],
            )
        )
    return bundles


def _tiny_yaml_bundles(text: str) -> dict:
    """A deliberately tiny parser for the exact manifest shape we document.

    Supports only:
      bundles:
        - out: <scalar>
          title: <scalar>
          intro: <scalar or '>' folded block>
          parts:
            - <scalar>
            - <scalar>

    This is NOT a general YAML parser; it exists so CI need not pip-install
    PyYAML. If your manifest grows beyond this shape, install PyYAML.
    """
    lines = text.splitlines()
    bundles: list[dict] = []
    cur: dict | None = None
    mode: str | None = None  # 'parts' or 'intro' when collecting multi-line
    intro_lines: list[str] = []

    def _flush_intro() -> None:
        nonlocal intro_lines, mode
        if cur is not None and intro_lines:
            cur["intro"] = " ".join(s.strip() for s in intro_lines).strip()
        intro_lines = []
        if mode == "intro":
            mode = None

    for raw in lines:
        line = raw.rstrip("\n")
        stripped = line.strip()
        if not stripped or stripped.startswith("#"):
            continue
        if stripped == "bundles:":
            continue

        indent = len(line) - len(line.lstrip(" "))

        # New bundle item.
        if stripped.startswith("- out:"):
            _flush_intro()
            cur = {"parts": []}
            cur["out"] = stripped.split(":", 1)[1].strip().strip("'\"")
            bundles.append(cur)
            mode = None
            continue

        if cur is None:
            continue

        # A bare list item — only meaningful while collecting parts.
        if stripped.startswith("- ") and mode == "parts":
            cur["parts"].append(stripped[2:].strip().strip("'\""))
            continue

        # While collecting a folded intro, deeper-indented lines are content.
        if mode == "intro" and not stripped.endswith(":") and ":" not in stripped[:24]:
            intro_lines.append(stripped)
            continue

        # key: value (or key: for a block that follows).
        if ":" in stripped:
            _flush_intro()
            key, _, val = stripped.partition(":")
            key = key.strip()
            val = val.strip()
            if key == "parts":
                mode = "parts"
            elif key in {"title", "out"}:
                cur[key] = val.strip("'\"")
                mode = None
            elif key == "intro":
                mode = "intro"
                if val and val not in {">", "|", ">-", "|-"}:
                    cur["intro"] = val.strip("'\"")
                    mode = None
            else:
                mode = None

    _flush_intro()
    return {"bundles": bundles}


# ---------------------------------------------------------------------------
# Body extraction. Pattern files carry YAML frontmatter; SKILL.md files do too.
# In a *combined* bundle we keep the human-readable body but lift the frontmatter
# into a compact, quoted block so the generated file stays clean markdown (no
# stray second '---' frontmatter fences that would confuse a markdown renderer).
# ---------------------------------------------------------------------------

def _split_frontmatter(text: str) -> tuple[str, str]:
    """Return (frontmatter_text_without_fences, body). Frontmatter is '' if none.

    Recognises a leading '---' ... '---' YAML block (the SKILL.md / pattern
    convention). A trailing-newline-terminated fence is required.
    """
    if text.startswith("---\n") or text.startswith("---\r\n"):
        # Find the closing fence.
        rest = text.split("\n", 1)[1] if "\n" in text else ""
        end = rest.find("\n---")
        if end != -1:
            fm = rest[:end].rstrip()
            after = rest[end + len("\n---"):]
            # Drop the rest of the closing fence line.
            after = after.split("\n", 1)[1] if "\n" in after else ""
            return fm, after.lstrip("\n")
    return "", text


def _demote_headings(body: str, levels: int = 1) -> str:
    """Push ATX headings down by ``levels`` so a part's H1 sits under the bundle.

    Lines inside fenced code blocks are left untouched (a leading '#' there is a
    comment / shell prompt, not a heading).
    """
    out: list[str] = []
    in_fence = False
    fence_marker = ""
    for line in body.splitlines():
        stripped = line.lstrip()
        if stripped.startswith("```") or stripped.startswith("~~~"):
            marker = stripped[:3]
            if not in_fence:
                in_fence = True
                fence_marker = marker
            elif stripped.startswith(fence_marker):
                in_fence = False
                fence_marker = ""
            out.append(line)
            continue
        if not in_fence and stripped.startswith("#"):
            hashes = len(stripped) - len(stripped.lstrip("#"))
            if 1 <= hashes <= 6:
                new_hashes = min(hashes + levels, 6)
                out.append("#" * new_hashes + stripped[hashes:])
                continue
        out.append(line)
    return "\n".join(out)


def _frontmatter_as_quote(fm: str) -> str:
    """Render extracted frontmatter as a fenced yaml block for reference.

    We keep it (patterns especially carry load-bearing validity/sunset/evidence
    metadata that a reader of the combined catalogue needs) but as a plain code
    block, not a live frontmatter fence.
    """
    if not fm.strip():
        return ""
    return "```yaml\n" + fm.strip() + "\n```\n"


# ---------------------------------------------------------------------------
# Rendering one bundle.
# ---------------------------------------------------------------------------

_GEN_BANNER = (
    "<!-- GENERATED FILE — DO NOT EDIT.\n"
    "     Built by skills/_scripts/concat_skills.py from the sources listed below.\n"
    "     Edit the source skill/pattern files and re-run the concat-patterns Action.\n"
    "     This file is marked linguist-generated in .gitattributes. -->\n"
)


def _today() -> str:
    return _dt.date.today().isoformat()


def render_bundle(bundle: Bundle, *, allow_missing: bool) -> tuple[str, list[str]]:
    """Return (markdown_text, missing_part_paths)."""
    missing: list[str] = []
    chunks: list[str] = []

    chunks.append(_GEN_BANNER)
    chunks.append(f"# {bundle.title}\n")
    chunks.append(
        f"> Generated bundle. Built {_today()} by "
        "`skills/_scripts/concat_skills.py`.\n"
    )
    if bundle.intro:
        chunks.append(bundle.intro.strip() + "\n")

    # A small table of contents listing the composing sources.
    chunks.append("## Bundled sources\n")
    for part in bundle.parts:
        chunks.append(f"- `{part}`")
    chunks.append("")  # blank line after the list

    # Each part: a clear separator, an H2 with the source path, optional
    # frontmatter-as-yaml-block, then the demoted body.
    for part in bundle.parts:
        src = REPO_ROOT / part
        chunks.append("\n---\n")
        if not src.exists():
            missing.append(part)
            chunks.append(f"## MISSING SOURCE: `{part}`\n")
            chunks.append(
                f"> The manifest references `{part}` but no such file exists at "
                "build time. Add the source or fix the manifest.\n"
            )
            continue

        raw = src.read_text(encoding="utf-8")
        fm, body = _split_frontmatter(raw)
        chunks.append(f"## Source: `{part}`\n")
        quoted = _frontmatter_as_quote(fm)
        if quoted:
            chunks.append("<details><summary>frontmatter</summary>\n")
            chunks.append(quoted)
            chunks.append("</details>\n")
        chunks.append(_demote_headings(body, levels=1).strip() + "\n")

    text = "\n".join(chunks).rstrip() + "\n"

    if missing and not allow_missing:
        for part in missing:
            print(f"  ! missing source: {part}", file=sys.stderr)

    return text, missing


# ---------------------------------------------------------------------------
# Driver.
# ---------------------------------------------------------------------------

def build(
    manifest_path: Path,
    *,
    check: bool,
    allow_missing: bool,
) -> int:
    """Build (or --check) every bundle. Return a process exit code."""
    bundles = _load_manifest(manifest_path)
    if not bundles:
        print("no bundles to build", file=sys.stderr)
        return 1

    any_missing = False
    any_stale = False
    wrote = 0

    for bundle in bundles:
        out_path = GENERATED_DIR / bundle.out
        text, missing = render_bundle(bundle, allow_missing=allow_missing)
        if missing:
            any_missing = True

        if check:
            existing = out_path.read_text(encoding="utf-8") if out_path.exists() else None
            if existing != text:
                any_stale = True
                print(f"  STALE: {bundle.out} (would change)", file=sys.stderr)
            else:
                print(f"  ok:    {bundle.out}")
            continue

        out_path.parent.mkdir(parents=True, exist_ok=True)
        out_path.write_text(text, encoding="utf-8")
        wrote += 1
        n_present = sum(1 for p in bundle.parts if (REPO_ROOT / p).exists())
        print(f"  wrote: {bundle.out}  ({n_present}/{len(bundle.parts)} sources)")

    if check:
        if any_stale:
            print(
                "\nBundles are out of date. Run "
                "`python skills/_scripts/concat_skills.py` and commit the result.",
                file=sys.stderr,
            )
            return 1
        print("\nAll bundles up to date.")
        # Missing sources are advisory under --check (a pattern may be mid-PR).
        return 0

    print(f"\nBuilt {wrote} bundle(s) into {GENERATED_DIR}.")
    if any_missing and not allow_missing:
        print(
            "One or more manifest sources were missing (see above). "
            "Pass --allow-missing to treat this as non-fatal.",
            file=sys.stderr,
        )
        return 2
    return 0


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(
        description="Concatenate CoE skills/patterns into generated/ bundles "
        "(deterministic; no LLM step)."
    )
    parser.add_argument(
        "--manifest",
        type=Path,
        default=DEFAULT_MANIFEST,
        help=f"bundle manifest YAML (default: {DEFAULT_MANIFEST.relative_to(REPO_ROOT)}; "
        "falls back to the built-in v1 bundles if absent)",
    )
    parser.add_argument(
        "--check",
        action="store_true",
        help="do not write; exit non-zero if any bundle is out of date "
        "(use in CI to enforce 'bundles committed')",
    )
    parser.add_argument(
        "--allow-missing",
        action="store_true",
        help="treat missing manifest sources as non-fatal "
        "(a placeholder section is emitted instead)",
    )
    args = parser.parse_args(argv)

    print(f"repo root:  {REPO_ROOT}")
    print(f"manifest:   {args.manifest}")
    print(f"output dir: {GENERATED_DIR}\n")

    return build(
        args.manifest,
        check=args.check,
        allow_missing=args.allow_missing,
    )


if __name__ == "__main__":
    raise SystemExit(main())
