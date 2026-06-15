#!/usr/bin/env python3
"""
lint_skill_target_rule.py — the target-rule / output-kinds linter.

This is docs/06 Principle VI (the TARGET RULE) and docs/09 Guardrail 1 made
executable. It is the script the `validate-skill-frontmatter` GitHub Action
calls on every PR, and it runs identically from a developer's shell:

    python3 skills/_scripts/lint_skill_target_rule.py            # lint the repo
    python3 skills/_scripts/lint_skill_target_rule.py --root .   # explicit root
    python3 skills/_scripts/lint_skill_target_rule.py path/to/SKILL.md ...

THE INVARIANT IT ENFORCES (the only thing that lets this Centre of Excellence
have NO enforcement gates and still be safe):

    Every agent / skill output is exactly one of
        proposal | question | menu | halt
    Never a status, verdict, colour, ranking, queue disposition, feasibility
    status, score, or assessment of a person.

The spec this script implements is owned by, and must stay in sync with,
    skills/_contract/target-rule-output-kinds/SKILL.md
Change the closed enum or the forbidden catalogue there first; this follows.

WHAT IT DOES (deterministic; no LLM step; dependency-light — standard library
only, so it runs in CI with zero `pip install`):

  STEP 1  Parse the YAML frontmatter from each skills/**/SKILL.md (a minimal
          built-in parser — no PyYAML dependency).
  STEP 2  Require the keys: name, description, when_to_use, output_kinds,
          deterministic_fallback.
  STEP 3  FAIL if output_kinds is not a NON-EMPTY SUBSET of
          {proposal, question, menu, halt}.
  STEP 4  FAIL if the body asserts a forbidden output token — scan for declared
          status / verdict / colour / ranking / score / disposition / feasibility
          output SHAPES (a verdict wearing one of the four kinds as a costume).
  STEP 5  When scanning a PATTERN file: FAIL if its frontmatter carries an
          agent-set approval_status (anything past `candidate`) or a validated_by
          that does not match the committing author per `git blame`. When blame is
          unavailable (shallow clone, not a repo, file untracked) this DOWNGRADES
          to an advisory note — never a hard fail on missing provenance alone.

It exits non-zero with a clear, line-referenced message on any FAIL. WARN and
NOTE never change the exit code: keeping it light/advisory, the linter catches
the SHAPE violation; a human still owns the call.

This linter is itself advisory CI: it comments and fails the check to prompt a
human fix. It is NOT a runtime gate and it blocks no downstream project.
"""

from __future__ import annotations

import argparse
import os
import re
import subprocess
import sys
from dataclasses import dataclass, field
from typing import Iterable, Optional

# --------------------------------------------------------------------------- #
# The contract (kept in lockstep with target-rule-output-kinds/SKILL.md)       #
# --------------------------------------------------------------------------- #

# The closed set. Nothing outside this is a legal output kind.
LEGAL_OUTPUT_KINDS = frozenset({"proposal", "question", "menu", "halt"})

# Required frontmatter keys on every SKILL.md.
REQUIRED_SKILL_KEYS = (
    "name",
    "description",
    "when_to_use",
    "output_kinds",
    "deterministic_fallback",
)

# The single legal climbing path for a pattern's approval_status. An *agent*
# (the author-component-pattern skill) only ever writes `candidate`; any value
# beyond that is a HUMAN ratification performed in a PR edit. So an
# approval_status past `candidate` that was committed by a non-human / by the
# same automated author who created the file is the smell we catch.
PATTERN_AGENT_SET_APPROVAL = "candidate"
PATTERN_APPROVAL_LADDER = ("candidate", "reviewed", "approved")

# Heuristic markers that a commit/author is an agent rather than a human
# ratifier. Matched case-insensitively against the git-blame author name/email.
AGENT_AUTHOR_MARKERS = (
    "claude",
    "anthropic",
    "[bot]",
    "github-actions",
    "actions@github",
    "noreply@anthropic",
    "agent",
    "automation",
)

# --------------------------------------------------------------------------- #
# Forbidden-output catalogue (the body scan, Step 4).                          #
#                                                                              #
# Each entry is (compiled-regex, human-readable explanation). These target     #
# declared OUTPUT SHAPES — text a skill says it EMITS — not mere discussion of #
# the anti-pattern. The whole forbidden catalogue is *about* these tokens, so  #
# we anchor on emit/output/return phrasing or unambiguous literal shapes       #
# (a RAG colour glyph, a bare "Similarity: 0.87") to avoid flagging the very   #
# prose that warns against them. Precision over volume: a noisy linter trains  #
# the human to ignore it, which is the same failure the TARGET RULE prevents.  #
# --------------------------------------------------------------------------- #

# A clause that means "this skill produces / returns / emits ...". Used to gate
# most token checks so we flag *declared outputs*, not warnings about them.
#
# CRITICAL precision discipline (this IS the precision-over-volume rule the
# source material enforces): the skill files in this library are *saturated* with
# the forbidden vocabulary because their whole job is to TEACH the rule — "emit no
# verdict", "❌ feasibility status", "you assign no status", legacy-code captions.
# A naive keyword scan flags all of that and floods false positives, which trains
# the human to ignore the linter — the exact failure (11 challenges, 6 spurious)
# the TARGET RULE exists to prevent. So the emit clause must be *affirmative*: an
# emit verb NOT immediately swallowed by a negation. And every match is then
# re-checked against a negation/anti-example window (see _suppressed_by_context).
_EMIT = r"(?:emit|emits|output|outputs|return|returns|produce|produces|set|sets|assign|assigns|stamp|stamps|report|reports)"

# A negation that turns an emit clause inert ("emit NO verdict", "produces no
# status", "never returns a score"). When one of these sits between the emit verb
# and the forbidden token, the clause is documentation of the rule, not a breach.
_NEG = r"(?:no|not|never|without|n't|zero)"

# Every entry is (compiled-regex, explanation). A match is only a FAIL if it also
# survives the negation/anti-example context window (see scan_body_for_forbidden).
# Patterns are deliberately tight — they require an AFFIRMATIVE declared emission
# or an unambiguous literal asserted value, never a bare mention of the token.
FORBIDDEN_PATTERNS: tuple[tuple[re.Pattern[str], str], ...] = (
    # A RAG colour / health verdict assigned as a literal value to a field the
    # skill emits: `health: amber`, `status = "red"`, `rag: green`. A coloured
    # status value IS a verdict. (A discussion like 'there is no health: amber
    # field' is suppressed by the negation window.) The colour must be a quoted
    # or bare VALUE of the field — not the field merely mentioned in prose.
    (
        re.compile(
            r"""(?ix)
            \b(?:health|rag|status|verdict|rating)\s*[:=]\s*   # field assignment
            ["'`]?                                              # optional quote
            (?:🔴|🟠|🟡|🟢|red|amber|yellow|green)\b           # a RAG colour value
            """
        ),
        "a RAG colour / health verdict assigned as a value (a colour IS a verdict — emit cited facts and let the human read the colour)",
    ),
    # A feasibility STATUS asserted as a value on an option: "Option B: infeasible",
    # "Candidate A — feasible". Not the phrase "feasibility status" in prose (that
    # is almost always the skills forbidding it; the negation window handles it).
    (
        re.compile(
            r"""(?ix)
            \b(?:option|candidate)\s+\w+\s*[:—-]\s*   # "Option B:" / "Candidate A —"
            ["'`]?(?:in)?feasible\b                    # ... feasible / infeasible
            """
        ),
        "a feasibility status asserted on an option (enumerate & cite the roadblocks an option hits; the feasibility call is human-owned)",
    ),
    # An AFFIRMATIVE declared emission of a feasibility disposition. The emit verb
    # must NOT be negated (the _NEG guard forbids "emit no feasibility status").
    (
        re.compile(
            rf"""(?ix)
            \b{_EMIT}\s+
            (?!{_NEG}\b)                               # not "emit no ..."
            (?:a\s+|an\s+|the\s+)?
            feasibility\s+(?:status|disposition|verdict)\b
            """
        ),
        "a declared feasibility disposition output (enumerate & cite roadblocks; the feasibility call is human-owned)",
    ),
    # A bare similarity / quality SCORE asserted as a value: "Similarity: 0.87",
    # "Quality score = 7/10", "confidence: 85%". The retrieval TOOL computes the
    # number; a skill that prints the bare float as its answer has emitted a score.
    (
        re.compile(
            r"""(?ix)
            \b(?:similarity|quality|confidence|relevance|match)\s*(?:score)?\s*[:=]\s*
            ["'`]?(?:\d+(?:\.\d+)?\s*/\s*\d+|0?\.\d+|\d{1,3}\s*%)   # 0.87 | 7/10 | 85%
            """
        ),
        "a bare numeric score asserted as the answer (the tool computes the number; the skill narrates it into a proposal)",
    ),
    # A queue disposition / "probably-approve" lane — but only as an AFFIRMATIVE
    # declared output. "No probably-approve lane" / "never a recommended
    # disposition" are the skills forbidding it and are suppressed by the window.
    (
        re.compile(
            rf"""(?ix)
            \b{_EMIT}\s+
            (?!{_NEG}\b)
            (?:a\s+|an\s+|the\s+)?
            (?:probably[- ]approve|pre[- ]?approv\w*|recommended[- ]disposition|
               auto[- ]?approve\w*\s+lane)
            """
        ),
        "a declared queue disposition / probably-approve output (assemble & order the delta by consequence; never pre-dispose it)",
    ),
    # An AFFIRMATIVE declared emission of a verdict/ruling/disposition/ranking/
    # recommendation as the skill's output. Negation-guarded so "emit no verdict",
    # "produces no ranking", "never a recommendation" don't fire.
    (
        re.compile(
            rf"""(?ix)
            \b{_EMIT}\s+
            (?!{_NEG}\b)
            (?:a\s+|an\s+|the\s+)?
            (?:verdict|ruling|disposition|ranking|recommendation|grade)\b
            """
        ),
        "a declared verdict/ruling/disposition/ranking/recommendation output (only proposal|question|menu|halt are legal)",
    ),
    # An AFFIRMATIVE instruction to rank / star / mark-best a menu. The legal menu
    # is un-ranked. "No ranking", "cannot rank", "never starred" are suppressed.
    (
        re.compile(
            rf"""(?ix)
            (?:
              \b(?:{_EMIT}|present|show|order|sort)\s+
                  (?!{_NEG}\b)[^\n]{{0,20}}\bbest[- ]first\b
              |
              \bstar\s+(?!{_NEG}\b)(?:the\s+)?(?:best|favourite|favorite|preferred)\b
              |
              \bmark\s+(?!{_NEG}\b)(?:the\s+)?(?:best|recommended|preferred)\s+(?:option|candidate)\b
            )
            """
        ),
        "a ranked / starred menu output (a real menu is un-ranked and equal; 'do nothing' always present)",
    ),
    # An AFFIRMATIVE conflict / weakness / necessity ASSERTION emitted as a finding
    # (vs. the legal question naming both ids and asking "which assumption gives?").
    (
        re.compile(
            rf"""(?ix)
            \b{_EMIT}\s+
            (?!{_NEG}\b)
            [^\n]{{0,30}}\b
            (?:these\s+conflict|requirements?\s+conflict|is\s+gold[- ]plated|
               is\s+over[- ]engineered|is\s+unnecessary)\b
            """
        ),
        "a declared conflict/weakness/necessity ASSERTION (name both ids + the assumption and ASK 'which gives?' — never adjudicate)",
    ),
    # An AFFIRMATIVE assessment of a PERSON as an output (lenses flag missing
    # concerns, never people).
    (
        re.compile(
            rf"""(?ix)
            \b{_EMIT}\s+
            (?!{_NEG}\b)
            [^\n]{{0,20}}\bthe\s+(?:author|reviewer|developer|engineer)\s+
            (?:missed|failed|forgot|ignored|is\s+at\s+fault)\b
            """
        ),
        "a declared assessment of a person (target the blind spot — flag a missing CONCERN, never a missing/at-fault person)",
    ),
)


# --------------------------------------------------------------------------- #
# Findings                                                                     #
# --------------------------------------------------------------------------- #

FAIL = "FAIL"
WARN = "WARN"
NOTE = "NOTE"


@dataclass
class Finding:
    level: str  # FAIL | WARN | NOTE
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
    def fails(self) -> list[Finding]:
        return [f for f in self.findings if f.level == FAIL]

    @property
    def warns(self) -> list[Finding]:
        return [f for f in self.findings if f.level == WARN]

    @property
    def notes(self) -> list[Finding]:
        return [f for f in self.findings if f.level == NOTE]


# --------------------------------------------------------------------------- #
# Minimal frontmatter parser (no PyYAML — the library must lint in CI with no  #
# pip install). Handles the small YAML subset our frontmatter actually uses:   #
#   key: scalar                                                                 #
#   key: [a, b, c]      (inline flow list)                                      #
#   key:                                                                         #
#     - a               (block list)                                            #
#     - b                                                                        #
# Quotes are stripped; everything else is kept as a raw string. This is        #
# deliberately small and predictable, not a general YAML engine.               #
# --------------------------------------------------------------------------- #

_FM_DELIM = re.compile(r"^---[ \t]*$")


@dataclass
class Frontmatter:
    present: bool
    raw: str
    data: dict[str, object]
    body_start_line: int  # 1-based line where the body begins (after closing ---)


def split_frontmatter(text: str) -> Frontmatter:
    lines = text.splitlines()
    if not lines or not _FM_DELIM.match(lines[0]):
        return Frontmatter(present=False, raw="", data={}, body_start_line=1)

    close_idx: Optional[int] = None
    for i in range(1, len(lines)):
        if _FM_DELIM.match(lines[i]):
            close_idx = i
            break
    if close_idx is None:
        # Opened a frontmatter fence but never closed it.
        return Frontmatter(present=False, raw="", data={}, body_start_line=1)

    raw = "\n".join(lines[1:close_idx])
    data = _parse_frontmatter_block(lines[1:close_idx])
    return Frontmatter(
        present=True, raw=raw, data=data, body_start_line=close_idx + 2
    )


def _strip_inline_comment(value: str) -> str:
    # Drop a trailing "  # comment" only when the # is preceded by whitespace and
    # the value isn't quoted around it. Conservative: keeps '#tags' inside text.
    if '"' in value or "'" in value:
        return value.strip()
    m = re.search(r"\s+#", value)
    if m:
        value = value[: m.start()]
    return value.strip()


def _unquote(value: str) -> str:
    value = value.strip()
    if len(value) >= 2 and value[0] == value[-1] and value[0] in "\"'":
        return value[1:-1]
    return value


def _parse_inline_list(value: str) -> list[str]:
    inner = value.strip()[1:-1].strip()  # drop [ ]
    if not inner:
        return []
    return [_unquote(part) for part in _split_top_level_commas(inner) if part.strip()]


def _split_top_level_commas(s: str) -> list[str]:
    out: list[str] = []
    buf: list[str] = []
    quote: Optional[str] = None
    for ch in s:
        if quote:
            buf.append(ch)
            if ch == quote:
                quote = None
        elif ch in "\"'":
            quote = ch
            buf.append(ch)
        elif ch == ",":
            out.append("".join(buf))
            buf = []
        else:
            buf.append(ch)
    if buf:
        out.append("".join(buf))
    return out


def _parse_frontmatter_block(block_lines: list[str]) -> dict[str, object]:
    data: dict[str, object] = {}
    i = 0
    n = len(block_lines)
    while i < n:
        line = block_lines[i]
        if not line.strip() or line.lstrip().startswith("#"):
            i += 1
            continue
        m = re.match(r"^([A-Za-z0-9_]+)\s*:\s*(.*)$", line)
        if not m:
            i += 1
            continue
        key, rest = m.group(1), m.group(2)
        rest_clean = _strip_inline_comment(rest)
        if rest_clean.startswith("[") and rest_clean.endswith("]"):
            data[key] = _parse_inline_list(rest_clean)
            i += 1
            continue
        if rest_clean == "":
            # Possible block list on following indented "- item" lines.
            items: list[str] = []
            j = i + 1
            while j < n:
                bl = block_lines[j]
                if re.match(r"^\s*-\s+", bl):
                    items.append(_unquote(_strip_inline_comment(re.sub(r"^\s*-\s+", "", bl))))
                    j += 1
                elif not bl.strip():
                    j += 1
                else:
                    break
            if items:
                data[key] = items
                i = j
                continue
            data[key] = ""
            i += 1
            continue
        data[key] = _unquote(rest_clean)
        i += 1
    return data


# --------------------------------------------------------------------------- #
# git blame helper (for the pattern provenance check, Step 5).                 #
# --------------------------------------------------------------------------- #

@dataclass
class BlameResult:
    available: bool
    author: str  # "Name <email>" lower-cased; "" when unavailable
    note: str = ""


def blame_line_author(path: str, needle: str, root: str) -> BlameResult:
    """
    Return the git-blame author of the first line in `path` containing `needle`.
    Degrades to an advisory (available=False) when git/blame is unavailable —
    shallow clone, file untracked, not a repo, git missing — never a hard fail.
    """
    if not _git_available(root):
        return BlameResult(False, "", "git not available")
    # Find the line number of the needle in the file (1-based).
    try:
        with open(path, "r", encoding="utf-8") as fh:
            file_lines = fh.read().splitlines()
    except OSError as exc:
        return BlameResult(False, "", f"could not read file: {exc}")
    lineno = next(
        (idx + 1 for idx, ln in enumerate(file_lines) if needle in ln), None
    )
    if lineno is None:
        return BlameResult(False, "", f"line containing {needle!r} not found")
    try:
        out = subprocess.run(
            ["git", "blame", "-L", f"{lineno},{lineno}", "--porcelain", "--", path],
            cwd=root,
            capture_output=True,
            text=True,
            timeout=20,
        )
    except (OSError, subprocess.SubprocessError) as exc:
        return BlameResult(False, "", f"git blame failed: {exc}")
    if out.returncode != 0:
        msg = (out.stderr or "").strip().splitlines()
        hint = msg[0] if msg else f"exit {out.returncode}"
        return BlameResult(False, "", f"git blame unavailable ({hint})")
    name = email = ""
    for bl in out.stdout.splitlines():
        if bl.startswith("author "):
            name = bl[len("author "):].strip()
        elif bl.startswith("author-mail "):
            email = bl[len("author-mail "):].strip().strip("<>")
    if not name and not email:
        return BlameResult(False, "", "blame produced no author")
    return BlameResult(True, f"{name} <{email}>".strip().lower())


def _git_available(root: str) -> bool:
    try:
        out = subprocess.run(
            ["git", "rev-parse", "--is-inside-work-tree"],
            cwd=root,
            capture_output=True,
            text=True,
            timeout=10,
        )
    except (OSError, subprocess.SubprocessError):
        return False
    return out.returncode == 0 and out.stdout.strip() == "true"


def _looks_like_agent(author: str) -> bool:
    a = author.lower()
    return any(marker in a for marker in AGENT_AUTHOR_MARKERS)


# --------------------------------------------------------------------------- #
# The checks                                                                   #
# --------------------------------------------------------------------------- #

def lint_skill_file(path: str, root: str, report: Report) -> None:
    report.files_checked += 1
    try:
        text = open(path, "r", encoding="utf-8").read()
    except OSError as exc:
        report.add(FAIL, path, 0, f"could not read file: {exc}")
        return

    fm = split_frontmatter(text)

    # Step 1 — frontmatter must parse.
    if not fm.present:
        report.add(
            FAIL, path, 1,
            "no YAML frontmatter found (a SKILL.md must open with a '---' fenced "
            "frontmatter block declaring name/description/when_to_use/output_kinds/"
            "deterministic_fallback)",
        )
        return

    # Step 2 — required keys present.
    for key in REQUIRED_SKILL_KEYS:
        if key not in fm.data or _is_empty(fm.data[key]):
            report.add(
                FAIL, path, _key_line(text, key) or 1,
                f"required frontmatter key '{key}' is missing or empty "
                f"(every SKILL.md must declare: {', '.join(REQUIRED_SKILL_KEYS)})",
            )

    # Step 3 — output_kinds is a NON-EMPTY SUBSET of the closed set.
    if "output_kinds" in fm.data and not _is_empty(fm.data["output_kinds"]):
        kinds = _as_list(fm.data["output_kinds"])
        line = _key_line(text, "output_kinds") or 1
        if not kinds:
            report.add(
                FAIL, path, line,
                "output_kinds is empty — declare a non-empty subset of "
                "{proposal, question, menu, halt}",
            )
        else:
            illegal = [k for k in kinds if k not in LEGAL_OUTPUT_KINDS]
            if illegal:
                report.add(
                    FAIL, path, line,
                    f"output_kinds contains illegal kind(s) {illegal} — the only "
                    f"legal kinds are {sorted(LEGAL_OUTPUT_KINDS)}. "
                    f"'recommendation'/'verdict'/'status'/'score'/'ranking' are "
                    f"JUDGMENT wearing a costume; reshape into proposal|question|"
                    f"menu|halt and hand the call to the human.",
                )

    # Step 4 — scan the body for forbidden declared-output shapes.
    scan_body_for_forbidden(text, fm.body_start_line, path, report)


def lint_pattern_file(path: str, root: str, report: Report) -> None:
    """
    Pattern provenance check (Step 5). Patterns live under patterns/ and carry a
    human-owned lifecycle. An agent (the author skill) only ever writes
    approval_status: candidate. Anything past that — or a validated_by/author of
    that climb that isn't the human committer per git blame — is the smell.
    """
    report.files_checked += 1
    try:
        text = open(path, "r", encoding="utf-8").read()
    except OSError as exc:
        report.add(FAIL, path, 0, f"could not read file: {exc}")
        return

    fm = split_frontmatter(text)
    if not fm.present:
        # Patterns without frontmatter are a different lint's concern (schema);
        # the target-rule linter only governs the approval/provenance shape.
        return

    approval = str(fm.data.get("approval_status", "")).strip().lower()
    status = str(fm.data.get("status", "")).strip().lower()
    validated_by = str(fm.data.get("validated_by", "")).strip()

    # The author skill is allowed to set approval_status: candidate. Any climb
    # beyond candidate must be a human ratification — verify via git blame that a
    # human (not an agent) committed the line that set it.
    climbed = approval and approval != PATTERN_AGENT_SET_APPROVAL
    promoted_status = status in {"active"}  # "active" is the ratified public state

    if climbed or promoted_status:
        # Which frontmatter line carries the ratification we must attribute?
        needle = (
            f"approval_status:" if climbed else "status:"
        )
        blame = blame_line_author(path, needle, root)
        target = approval if climbed else f"status={status}"
        if not blame.available:
            report.add(
                NOTE, path, _key_line(text, needle.rstrip(":")) or 1,
                f"pattern carries a ratified {target!r}; could not verify the "
                f"committing author via git blame ({blame.note}). Advisory only — "
                f"a human reviewer must confirm a CODEOWNER (not an agent) ratified "
                f"this in the PR.",
            )
        elif _looks_like_agent(blame.author):
            report.add(
                FAIL, path, _key_line(text, needle.rstrip(":")) or 1,
                f"pattern's ratified {target!r} was committed by an apparent AGENT "
                f"author ({blame.author}). Ratification past 'candidate' is a HUMAN "
                f"act — a CODEOWNER edits the status in a PR with evidence attached. "
                f"An agent may only write approval_status: candidate.",
            )
        # else: a human committed it — legitimate, no finding.

    # validated_by must never name an agent (validity is a human ratification).
    if validated_by and _looks_like_agent(validated_by):
        report.add(
            FAIL, path, _key_line(text, "validated_by") or 1,
            f"validated_by points at an apparent agent ({validated_by!r}). Validity "
            f"is a human ratification with evidence attached, never a field a model "
            f"sets — name the human reviewer who confirmed the evidence.",
        )

    # An explicit agent-set approval_status key at all (beyond candidate) is also
    # caught structurally above; here we additionally flag the textbook smell of a
    # generated pattern arriving pre-approved without any blame story.
    if approval == "approved" and not validated_by:
        report.add(
            WARN, path, _key_line(text, "approval_status") or 1,
            "approval_status is 'approved' but validated_by is empty — a ratified "
            "pattern must name its human validator and carry evidence. Advisory.",
        )


def scan_body_for_forbidden(
    text: str, body_start_line: int, path: str, report: Report
) -> None:
    lines = text.splitlines()
    fenced = _fenced_code_lines(lines)  # 1-based line numbers inside ``` blocks
    seen: set[tuple[int, str]] = set()  # dedupe (line, explanation)
    for pattern, explanation in FORBIDDEN_PATTERNS:
        for m in pattern.finditer(text):
            line_no = text.count("\n", 0, m.start()) + 1
            if line_no < body_start_line:
                continue  # frontmatter is governed structurally, not by this scan
            if line_no in fenced:
                # Inside a fenced code block: an illustrative template / pseudocode
                # (e.g. the deterministic `verdict = "red" if red ...` boolean spine
                # the portfolio skill teaches). That is a derived-on-read COMPUTATION
                # the source material explicitly blesses, not an agent asserting a
                # RAG verdict as its output. The legal output kind is governed by the
                # frontmatter check (Step 3); code samples are not prose declarations.
                continue
            if _suppressed_by_context(lines, line_no):
                # The match sits inside an anti-example / negated context — i.e.
                # prose that DOCUMENTS or FORBIDS the shape ("❌ ...", "never emit a
                # verdict", "no feasibility status", "instead of a ranking"). That
                # is the rule being taught, not broken. Suppressing it is the whole
                # precision-over-volume discipline: a linter that flags the very
                # sentences forbidding the anti-pattern trains the human to ignore
                # it, which is the failure the TARGET RULE exists to prevent.
                continue
            key = (line_no, explanation)
            if key in seen:
                continue
            seen.add(key)
            snippet = _line_at(lines, line_no)
            report.add(
                FAIL, path, line_no,
                f"forbidden output shape — {explanation}. Offending text: "
                f"{snippet.strip()!r}",
            )


# --------------------------------------------------------------------------- #
# Small helpers                                                                #
# --------------------------------------------------------------------------- #

# Cues that mark text as DOCUMENTING / FORBIDDING the anti-pattern rather than
# declaring an output the skill emits: explicit ❌ examples, negations, "instead
# of", "no <token>", legacy-code captions ("identical to the legacy ..."). When
# any of these appears in the sentence neighbourhood of a match, the match is the
# rule being taught, not broken.
_ANTI_EXAMPLE_CUE = re.compile(
    r"(?ix)(?:❌|✗|🚫|\bnever\b|\bforbidden\b|\bforbid(?:s|den)?\b|\bdo\s+not\b|"
    r"\bdon'?t\b|\bdoes\s*n'?t\b|\bcannot\b|\bcan'?t\b|\bmust\s+not\b|\bavoid\b|"
    r"\binstead\s+of\b|\bnot\s+a\b|\bno\s+\w+\b|\bwrong\b|\bbad\s+example\b|"
    r"\bcounter[- ]example\b|\blegacy\b|\bnever\s+a\b|\bnot\s+the\b|\bzero\b)"
)

# How many lines on each side of a match form its "sentence neighbourhood" for
# negation/anti-example suppression. A markdown sentence routinely wraps across a
# line, and a ❌ caption sits one line above its example, so ±1 is the right width.
_CONTEXT_WINDOW = 1


def _suppressed_by_context(lines: list[str], line_no: int) -> bool:
    lo = max(0, line_no - 1 - _CONTEXT_WINDOW)
    hi = min(len(lines), line_no + _CONTEXT_WINDOW)
    window = " ".join(lines[lo:hi])
    return bool(_ANTI_EXAMPLE_CUE.search(window))


_FENCE = re.compile(r"^\s*(?:```|~~~)")


def _fenced_code_lines(lines: list[str]) -> set[int]:
    """1-based line numbers that fall inside a fenced ``` / ~~~ code block."""
    inside = False
    fenced: set[int] = set()
    for idx, ln in enumerate(lines):
        if _FENCE.match(ln):
            inside = not inside
            fenced.add(idx + 1)  # the fence line itself is part of the block
            continue
        if inside:
            fenced.add(idx + 1)
    return fenced


def _line_at(lines: list[str], line_no: int) -> str:
    idx = line_no - 1
    if 0 <= idx < len(lines):
        return lines[idx]
    return ""


def _key_line(text: str, key: str) -> int:
    pat = re.compile(rf"^{re.escape(key)}\s*:", re.MULTILINE)
    m = pat.search(text)
    if not m:
        return 0
    return text.count("\n", 0, m.start()) + 1


def _is_empty(value: object) -> bool:
    if value is None:
        return True
    if isinstance(value, str):
        return value.strip() == ""
    if isinstance(value, (list, tuple, dict)):
        return len(value) == 0
    return False


def _as_list(value: object) -> list[str]:
    if isinstance(value, (list, tuple)):
        return [str(v).strip() for v in value if str(v).strip()]
    if isinstance(value, str):
        s = value.strip()
        if s.startswith("[") and s.endswith("]"):
            return _parse_inline_list(s)
        # single scalar -> one-element list
        return [s] if s else []
    return []


# --------------------------------------------------------------------------- #
# Discovery + CLI                                                              #
# --------------------------------------------------------------------------- #

def find_skill_files(root: str) -> list[str]:
    skills_dir = os.path.join(root, "skills")
    base = skills_dir if os.path.isdir(skills_dir) else root
    found: list[str] = []
    for dirpath, _dirnames, filenames in os.walk(base):
        for fn in filenames:
            if fn == "SKILL.md":
                found.append(os.path.join(dirpath, fn))
    return sorted(found)


def find_pattern_files(root: str) -> list[str]:
    patterns_dir = os.path.join(root, "patterns")
    if not os.path.isdir(patterns_dir):
        return []
    found: list[str] = []
    for dirpath, _dirnames, filenames in os.walk(patterns_dir):
        # Skip schema / template scaffolding directories.
        if os.sep + "_" in dirpath + os.sep:
            continue
        for fn in filenames:
            if fn.endswith(".md") and not fn.startswith("_"):
                found.append(os.path.join(dirpath, fn))
    return sorted(found)


def classify_explicit_path(path: str) -> str:
    norm = os.path.normpath(path)
    parts = norm.split(os.sep)
    if os.path.basename(norm) == "SKILL.md":
        return "skill"
    if "patterns" in parts:
        return "pattern"
    if "skills" in parts:
        return "skill"
    # Default: treat a bare .md as a pattern only if it has pattern frontmatter.
    return "pattern"


def run(root: str, explicit_paths: Iterable[str]) -> Report:
    report = Report()
    explicit = list(explicit_paths)

    if explicit:
        for p in explicit:
            ap = os.path.abspath(p)
            kind = classify_explicit_path(ap)
            if kind == "skill":
                lint_skill_file(ap, root, report)
            else:
                lint_pattern_file(ap, root, report)
        return report

    for skill in find_skill_files(root):
        lint_skill_file(skill, root, report)
    for pattern in find_pattern_files(root):
        lint_pattern_file(pattern, root, report)
    return report


def main(argv: Optional[list[str]] = None) -> int:
    parser = argparse.ArgumentParser(
        description=(
            "Lint SKILL.md / pattern frontmatter against the TARGET RULE "
            "(docs/06 Principle VI). Advisory CI: fails on a SHAPE violation; a "
            "human still owns the call."
        )
    )
    parser.add_argument(
        "paths",
        nargs="*",
        help="Specific SKILL.md or pattern .md files to lint. "
        "Default: discover skills/**/SKILL.md and patterns/**/*.md under --root.",
    )
    parser.add_argument(
        "--root",
        default=_default_root(),
        help="Repository root (default: the repo containing this script).",
    )
    parser.add_argument(
        "--quiet",
        action="store_true",
        help="Print only failures (suppress the clean-pass summary).",
    )
    args = parser.parse_args(argv)

    root = os.path.abspath(args.root)
    report = run(root, args.paths)

    _print_report(report, root, quiet=args.quiet)

    # Only FAIL findings change the exit code. WARN/NOTE keep it advisory.
    return 1 if report.fails else 0


def _default_root() -> str:
    # skills/_scripts/lint_skill_target_rule.py -> repo root is two dirs up.
    here = os.path.dirname(os.path.abspath(__file__))
    return os.path.abspath(os.path.join(here, "..", ".."))


def _print_report(report: Report, root: str, quiet: bool) -> None:
    out = sys.stderr
    for f in report.fails:
        print(f.render(root), file=out)
    if not quiet:
        for f in report.warns:
            print(f.render(root), file=out)
        for f in report.notes:
            print(f.render(root), file=out)

    n_fail, n_warn, n_note = len(report.fails), len(report.warns), len(report.notes)
    summary = (
        f"\ntarget-rule lint: {report.files_checked} file(s) checked · "
        f"{n_fail} FAIL · {n_warn} WARN · {n_note} NOTE"
    )
    if n_fail:
        summary += (
            "\nThe TARGET RULE is the one invariant that lets this Centre of "
            "Excellence have no gates and stay safe. Fix the shape above, or "
            "(if the linter is wrong) refine the catalogue in "
            "skills/_contract/target-rule-output-kinds/SKILL.md — that file owns "
            "the spec, this script follows it."
        )
    elif not quiet:
        summary += "  — all outputs stay advisory (proposal|question|menu|halt). ✓"
    print(summary, file=out)


if __name__ == "__main__":
    raise SystemExit(main())
