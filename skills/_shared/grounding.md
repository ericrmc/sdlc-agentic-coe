# _shared/grounding.md — no fabrication: an absent required input HALTs and asks

> **This file is the single source of truth for the GROUNDING RULE.**
> Skills do not import it; they **quote the block below verbatim** into their own body.
> The `check-shared-stub-drift` GitHub Action (advisory, on every PR touching
> `skills/**`) diffs each skill's quoted copy against this file and fails the check
> if a single byte drifts. **Keep the canonical block byte-stable.** If the rule
> must change, change it *here first*, then re-quote into every skill in the same PR
> — never edit a quoted copy in place.

This is the **no-fabrication keystone**. Everything that reads or writes a requirement
consumes it. A skill that reasons over an input it never actually read is the one failure
that turns an advisory library into a liability: a clean-looking proposal grounded in
nothing. The rule below makes the absence of a required input a **typed `halt`**, not a
silent guess — so a missing input stops the run and asks, instead of being invented.

---

## The canonical block (quote this verbatim)

<!-- BEGIN grounding (byte-stable; do not edit a quoted copy — edit _shared/grounding.md) -->

**GROUNDING RULE — name the required inputs; an absent required input HALTs and asks, never assumes.**

A skill **names its required inputs** up front (its Inputs section marks each row Required or
Optional). Then:

- **A required input that is absent, unreadable, or empty becomes a `halt`.** The halt asks
  the user *where the input is*, offering the formats ingestion can read (an xlsx/csv path, a
  GitHub Project owner+number, a docs folder, or a pasted block). It then **stops and waits.**
  It never assumes, invents, or reasons over a hypothetical — no invented id, key, number, NFR,
  requirement, acceptance criterion, file path, or source row.
- **Partial input is named, not patched.** When some required inputs are present and others are
  not, the skill **names exactly what is missing and asks for it** — it never silently proceeds
  on the part it has, and it never back-fills the gap with a plausible-looking guess.
- **An absent *optional* input proceeds honestly.** It is surfaced as a `question` or recorded
  as an explicit null — never padded with invented content to look complete.

**"I read nothing" and "I cannot read this" are different outputs.** An unreadable or
unsupported source HALTs (it asks for a readable form); it never returns an empty result, because
a silent-empty reads downstream as "the source had nothing in it" — a silent-proceed failure.

**A halt is a question, never a verdict.** A halt names the missing input and asks where it is.
It never smuggles a finding, an assumption, or a disposition for a human to rubber-stamp — no
"I halt because this is infeasible / too risky / out of scope." Those are JUDGMENTs the human
owns. The halt carries only: *what is required, what is missing, and the formats it can be read
from.*

<!-- END grounding -->

---

## How to quote it

In any `SKILL.md` that reads or writes a requirement, outcome, decision, capability, or pattern
— i.e. that has a Required input — paste the block between the `BEGIN`/`END` markers above,
markers included, into a section titled **"Grounding (quoted)"**. Do not reword, reorder,
re-case, or re-punctuate it; the drift check compares bytes between the markers.

```markdown
## Grounding (quoted)

<!-- BEGIN grounding (byte-stable; do not edit a quoted copy — edit _shared/grounding.md) -->
...paste the canonical block exactly...
<!-- END grounding -->
```

Then, in the skill's **Inputs** section, mark each row Required or Optional and add a one-line
*if-absent* note on every Required row that cites this contract:

```markdown
## Inputs

- **Accepted requirements file** — *Required.* If absent/unreadable/empty: HALT and ask where it
  is (per `_shared/grounding.md`); never invent requirements. Readable forms: a markdown file, an
  xlsx/csv path, a GitHub Project owner+number, a docs folder, or a pasted block.
- **Project context paragraph** — *Optional.* If absent: proceed and surface the gap as a
  `question`; never pad it with an invented context.
```

## How the halt path is wired in the body

A skill that declares `halt` in `output_kinds` must contain a real halt step — not just the
quoted rule. The convention is an early step (usually **STEP 0 — locate / verify inputs**) that
computes input presence **before the model reasons** and emits the halt when a required input is
missing. The single canonical halt **exemplar** — a clean halt paired with a WRONG
verdict-smuggling counter-example — lives in
`skills/_contract/grounding-no-absent-input/SKILL.md`. Copy that shape; do not re-author it.

## What this contract does NOT do

- It does **not** add an enforcement gate. The halt is an advisory output kind like any other;
  the human is the one who supplies the missing input and re-runs.
- It does **not**, by itself, prevent a model from inventing an input mid-run — that is runtime
  behaviour no static check can catch. The companion lint
  (`skills/_scripts/lint_skill_grounding.py`) is honest about this: it checks that the stub is
  **cited** and that a `halt`-declaring skill **wires a halt path**, not that the model never
  fabricates. The discipline is the rule + the exemplar; the lint catches the documentation miss.

## Relationship to the rest of the library

- The **output discipline** that makes `halt` one of exactly four legal kinds —
  **proposal, question, menu, halt** — and forbids a halt from carrying a verdict is
  `skills/_shared/target-rule.md` / `skills/_contract/target-rule-output-kinds`.
- The **rhythm** the halt lives inside — a human supplies the missing input, the agent re-runs
  and proposes — is `skills/_shared/propose-ratify.md`.
- The **keys** an ingested or derived artefact is grounded against (read the scheme from the
  target file; never assume one) are `skills/_shared/req-key-conventions.md`.
- The **edge** every derived artefact carries back to its accepted upstream node is
  `skills/_shared/trace-edge.md`.
- The **drift check** that pins quoted copies to this file is the `check-shared-stub-drift`
  GitHub Action (advisory). It auto-discovers this stub via `skills/_shared/*.md`; no workflow
  edit was needed to add it.

Keep it light. Name the required inputs; if a required one is absent, HALT and ask where it is —
never assume, never invent, never silently proceed. That is the whole rule.
