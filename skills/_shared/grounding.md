# _shared/grounding.md — no fabrication: an absent required input HALTs and asks

> **This file is the single source of truth for the GROUNDING RULE.**
> Skills do not import it; they **quote the block below verbatim** into their own body.
> The `check-shared-stub-drift` GitHub Action (advisory, on every PR touching
> `skills/**`) diffs each skill's quoted copy against this file and fails the check
> if a single byte drifts. **Keep the canonical block byte-stable.** If the rule
> must change, change it *here first*, then re-quote into every skill in the same PR
> — never edit a quoted copy in place.

The no-fabrication keystone: an absent required input becomes a typed `halt` that asks where
the input is, never a silent guess. The block below is the source of truth; the wrapper around
it is author-facing only.

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
*if-absent* note on every Required row citing this contract (HALT and ask where it is; never
invent) and a proceed-and-surface note on each Optional row. The worked Inputs example lives
in the canonical exemplar — see Pointers.

## How the halt path is wired in the body

A skill that declares `halt` in `output_kinds` must contain a real halt step — not just the
quoted rule. The convention is an early step (usually **STEP 0 — locate / verify inputs**) that
computes input presence **before the model reasons** and emits the halt when a required input is
missing. The single canonical halt **exemplar** — a clean halt paired with a WRONG
verdict-smuggling counter-example, and the Inputs row form — lives in
`skills/_contract/grounding-no-absent-input/SKILL.md`. Copy that shape; do not re-author it.

It is **not** an enforcement gate, and no static check can stop a model inventing an input
mid-run — the companion lint (`skills/_scripts/lint_skill_grounding.py`) only checks that the
stub is cited and that a `halt`-declaring skill wires a halt path.

## Pointers

- The halt is one of exactly four legal output kinds and must carry no verdict —
  `skills/_shared/target-rule.md`.
- Keys an artefact is grounded against — `skills/_shared/req-key-conventions.md`.
- The edge a derived artefact carries to its upstream node — `skills/_shared/trace-edge.md`.
- The supply-input-then-re-run rhythm — `skills/_shared/propose-ratify.md`.
- Pinned to this file by `check-shared-stub-drift` (advisory CI; auto-discovers via `*.md`).
