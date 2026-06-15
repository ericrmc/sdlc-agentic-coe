#!/usr/bin/env python3
"""
lint_skill_grounding.py — the grounding-contract linter (advisory, documentation-level).

This makes a SMALL, HONEST part of the no-fabrication keystone executable. The
keystone itself is a discipline (the GROUNDING RULE: a skill names its REQUIRED
inputs; an absent required input HALTs and asks where it is, never an invented
hypothetical) owned by:

    skills/_shared/grounding.md                         (the quotable rule)
    skills/_contract/grounding-no-absent-input/SKILL.md (the contract + halt exemplar)

This script checks TWO documentation-level facts on every skills/**/SKILL.md, and
is deliberately honest that it can do no more:

  CHECK A — stub citation.
      A skill that declares a REQUIRED input (its Inputs section marks a row
      Required, or carries an "if absent ... HALT" note) SHOULD quote the
      grounding stub. WARN when such a skill lacks the grounding citation
      (the byte-stable <!-- BEGIN grounding --> block, or a reference to
      _shared/grounding.md / grounding-no-absent-input). This is a DOCUMENTATION
      miss — the rule is not travelling in the skill's own bytes.

  CHECK B — halt wiring (a positive assertion).
      A skill that declares `halt` in output_kinds MUST wire a halt path in its
      body — an actual HALT step/line, not just the word in the frontmatter.
      WARN when `halt` is declared but no halt path is found.

WHAT THIS LINT IS NOT, STATED PLAINLY (so no one mistakes it for a guarantee):

    It checks for the STUB CITATION and the HALT WIRING. It does NOT, and a static
    check CANNOT, catch RUNTIME FABRICATION — a model inventing a requirement, a
    key, an NFR, or a source row mid-run. That is behaviour, not text. The real
    safeguard is the GROUNDING RULE plus the canonical halt exemplar in
    skills/_contract/grounding-no-absent-input/SKILL.md; this linter only catches
    the documentation miss (rule not cited) and the wiring miss (halt declared but
    not implemented). Saying it prevents fabrication would be false confidence
    about the safeguard itself.

POSTURE: advisory, like every check in this library. Findings here are WARN/NOTE
only — they NEVER change the exit code. The linter surfaces a documentation gap
for a human to close; it blocks nothing and gates nothing. (A --strict flag exists
for a contributor who wants the warnings to fail their own local run; CI runs it
without --strict so it stays purely advisory.)

USAGE:
    python3 skills/_scripts/lint_skill_grounding.py            # lint the repo
    python3 skills/_scripts/lint_skill_grounding.py --root .   # explicit root
    python3 skills/_scripts/lint_skill_grounding.py path/to/SKILL.md ...
    python3 skills/_scripts/lint_skill_grounding.py --strict   # warnings -> exit 1

Standard library only — runs in CI with zero `pip install`.
"""

from __future__ import annotations

import argparse
import os
import re
import sys
from dataclasses import dataclass, field
from typing import Iterable, Optional

# --------------------------------------------------------------------------- #
# Contract anchors (kept in lockstep with the grounding stub + contract skill) #
# --------------------------------------------------------------------------- #

# The byte-stable marker that opens the quoted grounding block. A skill that
# quotes the stub carries this verbatim (markers included).
GROUNDING_BEGIN_MARKER = "<!-- BEGIN grounding"

# Looser references that also satisfy "the rule is cited" even if a skill points
# at the contract rather than pasting the full block (e.g. an Inputs note that
# says "per _shared/grounding.md" or names the contract skill).
GROUNDING_CITATION_PATTERNS = (
    re.compile(r"_shared/grounding\.md", re.IGNORECASE),
    re.compile(r"\bgrounding-no-absent-input\b", re.IGNORECASE),
    re.compile(GROUNDING_BEGIN_MARKER.replace("(", r"\(")),
)

# Underscore internals (_contract / _shared / _scripts) are conventions, not
# runnable analysis skills. The grounding CONTRACT skill itself naturally carries
# the rule and the exemplar; we still scan _contract so the contract skill's own
# citation is verified, but we never demand a halt-wiring from a pure rule doc.
SKILL_FILENAME = "SKILL.md"

# --------------------------------------------------------------------------- #
# Required-input detection (CHECK A trigger).                                  #
#                                                                              #
# We do not need a perfect parse of the Inputs prose — only a reliable signal  #
# that the skill DECLARES a required input, which is what makes the grounding   #
# citation expected. Three independent signals, ANY ONE is enough:              #
#   1. An explicit "Required" marker in the Inputs region (e.g. "*Required.*"). #
#   2. An if-absent / on-missing HALT-and-ask note anywhere in the body         #
#      (the exact shape the contract asks Required rows to carry).              #
#   3. A SINGLE-SOURCE SYNTHESIS clause — the body draws its WHOLE derived       #
#      artefact from one named input ("draft … from the chosen solution",       #
#      "from the stated need, fill …"). A skill that synthesises its entire      #
#      output from one input has, by definition, a required input — even when    #
#      the author forgot to decorate the Inputs row with a "Required" marker.    #
#      This signal closes the blind spot that let the author-* skills (whose     #
#      Inputs are an UNDECORATED numbered list) escape CHECK A.                  #
# --------------------------------------------------------------------------- #

# A Required-INPUT status marker — the decoration the contract asks each Required
# row to carry. Case-insensitive but deliberately TIGHT: it must look like a
# status marker decorating an input, NOT the bare word "required" inside a heading
# ("### CONDITIONALLY REQUIRED"), a table cell, or a field name
# ("open_required_checks"). So we require either markdown emphasis / a parenthetical
# directly wrapping the word, or an explicit "required input" / "input is required"
# phrase. We do NOT match a bare colon/dash/pipe followed by "required" (those are
# the false-positive shapes a heading or table column produces).
_REQUIRED_MARKER = re.compile(
    r"""(?ix)
    (?:
        (?:\*\*?|__?)\s*required\b           # *Required* / **Required** / _Required_ (emphasis)
      | \(\s*required\b                       # (required)
      | \brequired\s+input\b                  # "Required input"
      | \binput\b[^\n]{0,40}?\bis\s+required\b # "this input ... is required"
    )
    """
)

# An "if absent ... halt" / "if missing ... halt and ask" note — the if-absent
# clause the contract asks every Required row to carry. Its presence both signals
# a required input AND (separately) hints the halt is documented.
_IF_ABSENT_HALT = re.compile(
    r"""(?ix)
    \bif\s+(?:absent|missing|unreadable|empty|not\s+supplied|none)\b
    [^\n]{0,80}?
    \bhalt\b
    """
)

# A SINGLE-SOURCE SYNTHESIS clause — the body says it derives its WHOLE output from
# one named input. This is the structural tell of a required input that survives an
# author forgetting the "Required" decoration: an author/synthesis skill whose entire
# artefact is drafted "from the chosen solution" / "from the stated need" / "from the
# context you gathered" cannot run without that one input, so it HAS a required input.
#
# Deliberately TIGHT to stay false-positive-free across the library: the named source
# must be one of the closed "single brief" phrases (the noun an author-from-one-brief
# skill uses for its load-bearing input), AND it must sit next to a draft/synthesise/
# fill/derive verb — in either order ("draft … from the need" OR "from the need, draft
# …"). A bare mention of the word "synthesis" elsewhere (a neighbour reference, a
# DERIVE-LOW classification) does NOT match, because it is not paired with one of these
# named-source phrases. Verified to fire on exactly the two author-* skills and nothing
# else over skills/**/SKILL.md.
_SYNTH_NAMED_SOURCE = (
    r"(?:chosen\s+solution|stated\s+need|the\s+need\b|need\s+context"
    r"|context\s+you\s+gathered|context\s+handed)"
)
_SYNTH_VERB = (
    r"(?:draft|drafts|synthesis\w*|synthesise|synthesize|fill|fills|generate"
    r"|generates|derive|derives|capture|captures|author|authors|write|writes)"
)
_SINGLE_SOURCE_SYNTHESIS = re.compile(
    rf"""(?ix)
    (?:
        \b{_SYNTH_VERB}\b [^\n.]{{0,80}}? \bfrom\s+the\s+{_SYNTH_NAMED_SOURCE}
      | \bfrom\s+the\s+{_SYNTH_NAMED_SOURCE}\b [^\n]{{0,40}}? ,?\s* {_SYNTH_VERB}\b
    )
    """
)

# --------------------------------------------------------------------------- #
# Halt-wiring detection (CHECK B).                                             #
#                                                                              #
# A real halt path is more than the word "halt" sitting in output_kinds. We     #
# accept any of: an emphasised/heading HALT directive, a STEP 0 locate/verify    #
# inputs step, or an explicit "emit/return a halt" / "HALT —" instruction in the #
# body. We look only BELOW the frontmatter so the output_kinds line itself does  #
# not count as wiring.                                                          #
# --------------------------------------------------------------------------- #

_HALT_WIRING_PATTERNS = (
    # A bare "HALT" / "HALT —" directive line (the exemplar shape).
    re.compile(r"(?m)^\s*(?:[*_>#-]+\s*)?HALT\b"),
    # "HALT —" or "HALT:" mid-line (e.g. inside a code fence or sentence).
    re.compile(r"\bHALT\s*[—:-]"),
    # An imperative to emit/produce/return a halt as an output.
    re.compile(r"(?ix)\b(?:emit|emits|produce|produces|return|returns|raise|raises|is)\s+(?:a\s+|an\s+|the\s+)?halt\b"),
    # A "halt and ask / halt and stop" instruction (the contract's verb pair).
    re.compile(r"(?ix)\bhalts?\s+and\s+(?:ask|asks|stop|stops|wait|waits)\b"),
    # A STEP 0 locate/verify-inputs step — the conventional place the halt is wired.
    re.compile(r"(?ix)\bstep\s*0\b[^\n]{0,60}\b(?:locate|verify|check|confirm|ground|input|source|halt)\b"),
)

# --------------------------------------------------------------------------- #
# Findings (mirrors lint_skill_target_rule.py's shape for a consistent UX).    #
# --------------------------------------------------------------------------- #

WARN = "WARN"
NOTE = "NOTE"


@dataclass
class Finding:
    level: str  # WARN | NOTE
    path: str
    line: int  # 1-based; 0 if not line-specific
    message: str

    def render(self, root: str) -> str:
        rel = os.path.relpath(self.path, root) if self.path else "(repo)"
        where = f"{rel}:{self.line}" if self.line else rel
        return f"{self.level}  {where}\n      {self.message}"


@dataclass
class Report:
    findings: list[Finding] = field(default_factory=list)
    files_checked: int = 0

    def add(self, level: str, path: str, line: int, message: str) -> None:
        self.findings.append(Finding(level, path, line, message))

    @property
    def warns(self) -> list[Finding]:
        return [f for f in self.findings if f.level == WARN]

    @property
    def notes(self) -> list[Finding]:
        return [f for f in self.findings if f.level == NOTE]


# --------------------------------------------------------------------------- #
# Minimal frontmatter split (no PyYAML — must lint in CI with no pip install).  #
# We only need output_kinds and the body-start line, so this is intentionally   #
# tiny. Mirrors the parser shape in lint_skill_target_rule.py.                  #
# --------------------------------------------------------------------------- #

_FM_DELIM = re.compile(r"^---[ \t]*$")


@dataclass
class Split:
    present: bool
    frontmatter: str
    body: str
    body_start_line: int  # 1-based line where the body begins


def split_frontmatter(text: str) -> Split:
    lines = text.splitlines()
    if not lines or not _FM_DELIM.match(lines[0]):
        return Split(present=False, frontmatter="", body=text, body_start_line=1)
    close_idx: Optional[int] = None
    for i in range(1, len(lines)):
        if _FM_DELIM.match(lines[i]):
            close_idx = i
            break
    if close_idx is None:
        return Split(present=False, frontmatter="", body=text, body_start_line=1)
    fm = "\n".join(lines[1:close_idx])
    body = "\n".join(lines[close_idx + 1:])
    return Split(present=True, frontmatter=fm, body=body, body_start_line=close_idx + 2)


def parse_output_kinds(frontmatter: str) -> list[str]:
    """Pull the output_kinds values from the frontmatter, inline-list or block-list."""
    m = re.search(r"(?m)^output_kinds\s*:\s*(.*)$", frontmatter)
    if not m:
        return []
    rest = m.group(1).strip()
    # Strip a trailing inline comment outside of brackets.
    if rest.startswith("[") and rest.endswith("]"):
        inner = rest[1:-1]
        return [p.strip().strip("\"'") for p in inner.split(",") if p.strip()]
    if rest == "":
        # Block list: subsequent "  - value" lines.
        kinds: list[str] = []
        after = frontmatter[m.end():]
        for ln in after.splitlines():
            bm = re.match(r"^\s*-\s+(.*)$", ln)
            if bm:
                kinds.append(bm.group(1).strip().strip("\"'"))
            elif ln.strip() and not ln.startswith(" "):
                break
        return kinds
    # Single scalar.
    return [rest.strip("\"'")] if rest else []


# --------------------------------------------------------------------------- #
# The checks                                                                   #
# --------------------------------------------------------------------------- #

def _line_of(text: str, pat: re.Pattern[str]) -> int:
    m = pat.search(text)
    if not m:
        return 0
    return text.count("\n", 0, m.start()) + 1


# A markdown heading that opens the Inputs region (## Inputs, ### Inputs, "Inputs
# (what the user supplies)", etc.). CHECK A scopes its Required-marker scan to
# this region so a "required" describing the skill's OUTPUT artefacts (a pattern's
# conditionally-required frontmatter fields, an "advisory-check:required" label) is
# never mistaken for a Required INPUT declaration.
_INPUTS_HEADING = re.compile(r"(?im)^#{1,6}\s+inputs\b")
_ANY_HEADING = re.compile(r"(?m)^#{1,6}\s+\S")


def inputs_section(body: str) -> str:
    """Return the text of the Inputs section (heading -> next same-or-higher heading).

    Empty string when the skill has no Inputs heading. We bound the section at the
    next markdown heading of ANY level so we never bleed into 'The method' / 'Output
    format'. Conservative: if the section can't be isolated, callers fall back to
    the unambiguous if-absent-halt note, which is meaningful anywhere.
    """
    m = _INPUTS_HEADING.search(body)
    if not m:
        return ""
    start = m.end()
    nxt = _ANY_HEADING.search(body, start)
    return body[start:nxt.start()] if nxt else body[start:]


def declares_required_input(body: str) -> bool:
    """True if the skill signals at least one REQUIRED input.

    Three independent signals, ANY ONE suffices:
      1. A Required-INPUT status marker INSIDE the Inputs section (scoped so a
         'required' about the skill's outputs doesn't misfire); or
      2. An if-absent/on-missing HALT-and-ask note ANYWHERE in the body — that
         clause is unambiguous about an input regardless of where it sits; or
      3. A SINGLE-SOURCE SYNTHESIS clause — the body derives its whole output from
         one named input. A skill that drafts its entire artefact "from the chosen
         solution" / "from the stated need" HAS a required input even if its Inputs
         rows carry no "Required" decoration. This catches the author-* blind spot
         (an undecorated numbered Inputs list) without re-introducing false
         positives — the named-source phrasing is closed and verb-paired.
    """
    if _IF_ABSENT_HALT.search(body):
        return True
    if _SINGLE_SOURCE_SYNTHESIS.search(body):
        return True
    section = inputs_section(body)
    return bool(section and _REQUIRED_MARKER.search(section))


def cites_grounding(text: str) -> bool:
    """True if the skill quotes or references the grounding contract."""
    return any(p.search(text) for p in GROUNDING_CITATION_PATTERNS)


def has_halt_wiring(body: str) -> bool:
    """True if the body contains a real halt path (not just the frontmatter word)."""
    return any(p.search(body) for p in _HALT_WIRING_PATTERNS)


def lint_skill_file(path: str, root: str, report: Report) -> None:
    report.files_checked += 1
    try:
        text = open(path, "r", encoding="utf-8").read()
    except OSError as exc:
        report.add(NOTE, path, 0, f"could not read file: {exc}")
        return

    split = split_frontmatter(text)
    if not split.present:
        # Frontmatter presence is the target-rule linter's job; we only need the
        # split to scope the halt-wiring scan. Without it, scan the whole text.
        body = text
        kinds: list[str] = []
    else:
        body = split.body
        kinds = parse_output_kinds(split.frontmatter)

    rel = os.path.relpath(path, root)
    is_contract = f"{os.sep}_contract{os.sep}" in path + os.sep

    # CHECK A — stub citation when a required input is declared.
    if declares_required_input(body) and not cites_grounding(text):
        report.add(
            WARN, path,
            _line_of(text, _IF_ABSENT_HALT) or _line_of(text, _INPUTS_HEADING) or 1,
            "declares a REQUIRED input but does not cite the grounding contract. "
            "Quote the byte-stable block from `skills/_shared/grounding.md` in a "
            "'Grounding (quoted)' section (or, at minimum, add an if-absent note "
            "citing `_shared/grounding.md` on each Required input row). The "
            "no-fabrication rule must travel in the skill's own bytes. "
            "DOCUMENTATION miss — advisory.",
        )

    # CHECK B — positive assertion: halt declared => halt wired.
    if "halt" in [k.lower() for k in kinds]:
        if not has_halt_wiring(body):
            report.add(
                WARN, path,
                _line_of(split.frontmatter, re.compile(r"output_kinds")) or 1,
                "declares `halt` in output_kinds but no halt path is wired in the "
                "body. Add a real halt step (the convention is a 'STEP 0 — locate / "
                "verify inputs' that emits a clean HALT when a Required input is "
                "absent). Copy the canonical halt exemplar from "
                "`skills/_contract/grounding-no-absent-input/SKILL.md`. A declared "
                "halt with no halt path is the wiring miss this check exists to "
                "catch — advisory.",
            )
    elif declares_required_input(body) and not is_contract:
        # Not a failure: a Required-input skill may legitimately handle absence via
        # a `question` rather than a `halt`. Surface a NOTE so the author can
        # confirm the choice is deliberate, never a WARN.
        report.add(
            NOTE, path, 1,
            "declares a REQUIRED input but does NOT list `halt` in output_kinds. "
            "That can be correct (a missing input handled as a `question`), but "
            "confirm it is deliberate — the contract's default for an absent "
            "REQUIRED input is a `halt`. Advisory note, not a warning.",
        )

    if is_contract and not cites_grounding(text) and rel.endswith(
        os.path.join("grounding-no-absent-input", SKILL_FILENAME)
    ):
        # The grounding CONTRACT skill must carry the rule itself.
        report.add(
            WARN, path, 1,
            "the grounding contract skill itself does not quote the grounding "
            "block — it is the canonical home of the rule and must carry it "
            "verbatim. Advisory.",
        )


# --------------------------------------------------------------------------- #
# Discovery + CLI (mirrors lint_skill_target_rule.py).                         #
# --------------------------------------------------------------------------- #

def find_skill_files(root: str) -> list[str]:
    skills_dir = os.path.join(root, "skills")
    base = skills_dir if os.path.isdir(skills_dir) else root
    found: list[str] = []
    for dirpath, _dirnames, filenames in os.walk(base):
        for fn in filenames:
            if fn == SKILL_FILENAME:
                found.append(os.path.join(dirpath, fn))
    return sorted(found)


def run(root: str, explicit_paths: Iterable[str]) -> Report:
    report = Report()
    explicit = list(explicit_paths)
    if explicit:
        for p in explicit:
            ap = os.path.abspath(p)
            if os.path.basename(ap) == SKILL_FILENAME:
                lint_skill_file(ap, root, report)
            # Non-SKILL paths are silently ignored: this linter only governs skills.
        return report
    for skill in find_skill_files(root):
        lint_skill_file(skill, root, report)
    return report


def _default_root() -> str:
    # skills/_scripts/lint_skill_grounding.py -> repo root is two dirs up.
    here = os.path.dirname(os.path.abspath(__file__))
    return os.path.abspath(os.path.join(here, "..", ".."))


def _print_report(report: Report, root: str, quiet: bool) -> None:
    out = sys.stderr
    for f in report.warns:
        print(f.render(root), file=out)
    if not quiet:
        for f in report.notes:
            print(f.render(root), file=out)
    n_warn, n_note = len(report.warns), len(report.notes)
    summary = (
        f"\ngrounding lint: {report.files_checked} file(s) checked · "
        f"{n_warn} WARN · {n_note} NOTE"
    )
    summary += (
        "\nThis lint checks the STUB CITATION and the HALT WIRING only. It does "
        "NOT — and a static check CANNOT — catch a model inventing an input "
        "mid-run. The real safeguard is the GROUNDING RULE + the halt exemplar in "
        "skills/_contract/grounding-no-absent-input/SKILL.md; this catches the "
        "documentation miss, nothing more."
    )
    if n_warn == 0 and not quiet:
        summary += "\n  — every Required-input skill cites the rule and wires its halt. ✓"
    print(summary, file=out)


def main(argv: Optional[list[str]] = None) -> int:
    parser = argparse.ArgumentParser(
        description=(
            "Lint SKILL.md grounding-contract wiring (stub citation + halt path). "
            "Advisory CI: WARN/NOTE only, never changes the exit code unless "
            "--strict is given. It checks DOCUMENTATION, not runtime fabrication."
        )
    )
    parser.add_argument(
        "paths",
        nargs="*",
        help="Specific SKILL.md files to lint. "
        "Default: discover skills/**/SKILL.md under --root.",
    )
    parser.add_argument(
        "--root",
        default=_default_root(),
        help="Repository root (default: the repo containing this script).",
    )
    parser.add_argument(
        "--quiet",
        action="store_true",
        help="Print only warnings (suppress notes and the clean-pass summary).",
    )
    parser.add_argument(
        "--strict",
        action="store_true",
        help="Exit non-zero if any WARN was found (default: advisory, always exit 0). "
        "CI runs WITHOUT this so the check stays purely advisory.",
    )
    args = parser.parse_args(argv)

    root = os.path.abspath(args.root)
    report = run(root, args.paths)
    _print_report(report, root, quiet=args.quiet)

    # Advisory by default: WARN/NOTE never change the exit code. --strict lets a
    # contributor opt into a failing local run.
    if args.strict and report.warns:
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
