---
name: build-agent-brief-scaffold
description: Scaffold a paste-ready prompt that guides a downstream developer agent to implement a change — grounded in a feature analysis (the traced delta + derives_from + real impacted files + affected acceptance criteria + the discipline boundary); a sibling of testing-brief-scaffold / design-studio-brief-scaffold composing the scaffold-then-handoff convention. HALT if the analysis is absent; never invent scope; returned code re-enters as references, not stored.
when_to_use: handing implementation of an analysed change to a downstream developer / build agent during the delivery stage
output_kinds: [proposal, halt]
deterministic_fallback: the deterministic section base (delta + traces + impacted files + AC) + the fenced developer-agent prompt
one_liner: Assemble a paste-ready build prompt for a developer agent from a grounded feature analysis.
aliases: [build brief, developer handoff, implementation brief, coding agent prompt, dev agent handoff, build agent prompt, hand the build to an agent, implementation handoff]
suggested_tier: mid
neighbours: |
  Before: deliver/intake-feature-change (produces the feature analysis this brief is grounded in) and deliver/scaffold-then-handoff (the convention this composes).
  After: deliver/testing-brief-scaffold (the testing handoff for the same change) and deliver/comparator-grounded-estimate (size the change against comparators).
---

# build-agent-brief-scaffold

Assemble a clear, paste-ready **implementation brief** for a downstream developer
(or build) agent — so the agent that writes the code gets everything it needs in
one document, grounded in a real feature analysis, and nothing it doesn't.

This is the **build** sibling of
[`testing-brief-scaffold`](../testing-brief-scaffold/SKILL.md) and
[`design-studio-brief-scaffold`](../design-studio-brief-scaffold/SKILL.md). All
three compose the [`scaffold-then-handoff`](../scaffold-then-handoff/SKILL.md)
convention: build a deterministic, fact-grounded section base first, then run an
optional model enrich pass that keeps every fact and invents no scope. This skill
supplies the build-specific section list; the convention supplies the shape and
the failure mode.

> **Scaffold, not build.** This produces a *prompt*. It does not write the code,
> open a PR, or touch the repo. The developer agent does that downstream; what it
> returns re-enters as **references** (a PR link / a commit), never stored here.

## When to use

- A change has been **analysed** (typically by `intake-feature-change`) — the
  delta is classified, traced to an outcome, and grounded in real impacted files —
  and you want to hand the build to a developer agent.
- You need the build prompt to carry the **trace** (`derives_from`), the **real
  files**, and the **affected acceptance criteria**, so the agent builds exactly
  the analysed scope and nothing more.

Do **not** use this to do the build, to invent scope the analysis did not contain,
or to size the work (that is `comparator-grounded-estimate`). This is the handoff,
not the build.

## Inputs

Supplied as markdown / context — typically the output of `intake-feature-change`:

1. **The feature analysis** — *Required.* The grounded change analysis: the
   classified `change_kind` delta(s), each delta's `derives_from` trace (or its
   honest null), the **real impacted files** (verified on disk by the upstream
   analysis), the **affected acceptance criteria**, and the discipline boundary.
   If absent/unreadable/empty: HALT and ask for the analysis, naming
   `intake-feature-change` as the skill that produces it (per
   `_shared/grounding.md`); never invent a delta, a trace, a file, or an
   acceptance criterion to fill the brief. A brief with no analysis behind it is a
   fabricated scope wearing a prompt — exactly what this skill must not emit.
   Readable forms: a markdown file, a docs folder, or the analysis pasted directly
   into the chat.
2. **Project title** — *Optional.* For the header. If absent: derive it from the
   analysis or render an honest placeholder line; never invent a different project.
3. **Repo / code-access pointer** — *Optional.* The repo path the developer agent
   works in, carried through from the analysis. If absent: surface it as an open
   question for the human to fill; never invent a path.
4. **Panel / red-team synthesis** — *Optional.* If a panel shaped the change, fold
   it in. If absent: render the honest "_none convened yet_" note, never invent one.

> **Why the analysis is the one hard Required input.** Unlike its scaffold siblings
> (whose only Required input is a project title, because their value is a
> thin-but-honest brief that leads with open questions), this brief's entire
> substance — *what to build* — comes from the analysis. With no analysis there is
> no grounded scope, only invention. So an absent analysis **halts**; it does not
> degrade to a guessed feature. The skill never invents scope.

This skill reads a requirement, an acceptance criterion, and a delta trace, so it
follows the GROUNDING contract — an absent **Required** input HALTs and asks; it
is never invented or silently proceeded over. See
`skills/_contract/grounding-no-absent-input`.

## Grounding (quoted)

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

## The method (numbered STEPS)

Composes `scaffold-then-handoff`: **STEP 1 is the deterministic section base and
is the deliverable on its own; STEP 2 is the optional enrich pass that never gets
to lower the quality of STEP 1.** Plus a STEP 0 halt gate.

### STEP 0 — locate / verify the analysis (DETERMINISTIC, pre-model)

Confirm the one hard **Required** input — **the feature analysis** — is present as
a file-level fact (a real delta + trace + impacted files, not an empty stub).
Absent, unreadable, or empty → emit the clean halt below and **stop**. (Every
other input is Optional and never halts: a missing repo path becomes an open
question, a missing panel renders the honest "_none convened yet_" note — never an
invented fact.)

```markdown
HALT — required input missing.

I can't scaffold a build brief without the feature analysis it is grounded in, and
I won't invent the scope. Tell me where the analysis is and I'll pick up from there
— or, if the change hasn't been analysed yet, run `intake-feature-change` first to
classify the delta, trace it, and ground it in the real impacted files, then come
back.

I can read the analysis from any of these:
  • a markdown file path
  • a docs folder (markdown / text)
  • the analysis pasted directly into the chat

Which one, and where? (Nothing is briefed until I can read the analysed scope — I
will not hand a developer agent an invented feature.)
```

The halt names the missing input and stops; it carries no delta, no file, and no
verdict. With the analysis present, proceed to STEP 1.

### STEP 1 — build the deterministic section base (the deliverable)

Assemble the brief from the analysis facts only — no model call, no invention.
Per the `scaffold-then-handoff` contract: **open questions lead**, **every section
renders with an honest fallback**, and the brief carries a **fenced paste-ready
prompt**. The build-specific sections, in order:

1. **Open questions (read first).** Every null trace from the analysis ("`<delta>`
   has no accepted outcome behind it — confirm scope before building"), any missing
   repo path, any absent acceptance criterion. If none: `None flagged. Confirm the
   deltas + impacted files below.`
2. **What to build — the traced deltas.** One row per delta: `change_kind`, the
   delta text, its `derives_from` trace (or the honest null), the **real impacted
   files** (copied unchanged from the analysis — every one already on disk), and
   the **affected acceptance criteria**. Preserve every key, file path, and AC
   verbatim; render an honest empty-state where the analysis had a gap, never an
   invented one.
3. **Discipline boundary.** State it plainly for the developer agent: implement
   only the analysed scope; raise anything outside it as a finding, do not silently
   expand; do not change scope without a new analysis; returned code re-enters as a
   **reference** (PR link / commit), not a stored blob.
4. **From the panel / red-team.** Fold in the synthesis if present, else the honest
   "_none convened yet_" note.

### STEP 2 — emit the fenced developer-agent prompt (DETERMINISTIC)

Emit a fenced **build prompt** the user pastes straight into a developer / build
agent. Paste-ready means no placeholders. It must:

- name the project and the repo pointer (or carry the open question if absent);
- point at the "what to build" deltas above it and instruct the agent to implement
  **exactly** that scope — each delta traced to its outcome and its acceptance
  criteria;
- state the discipline boundary (build only the analysed scope; raise out-of-scope
  work as a finding; do not change scope without a new analysis);
- instruct the agent to return its work as a **PR / commit reference**, prove each
  affected acceptance criterion, and **not** mark the change done — disposition is
  the human's.

### STEP 3 — optional model enrich pass (prose only)

Hand the STEP 1 base to a model to sharpen the prose into a warmer, clearer brief.
Per `scaffold-then-handoff`, this is *prose enhancement, not re-authoring*, and is
an instance of the library GROUNDING rule (`_contract/grounding-no-absent-input`):

- **Keep every fact** — same deltas, same traces, same files, same acceptance
  criteria. **Invent no scope** — no new delta, no new file, no AC the analysis did
  not contain. **Lead with open questions.** Keep the prompt paste-ready.
- **Fall back to the base on ANY error.** A model failure returns the STEP 1 base
  unchanged. The enrich pass can only improve; it never blocks or degrades.

## Output format

A single markdown brief, ready to paste. Concrete template (the nested fence keeps
the build prompt copyable as one unit):

```markdown
# Build handoff — <project title> · <the change, in one line>

> A scaffold assembled from the feature analysis, grounded in real impacted files.
> Hand this to a developer / build agent. This scaffolds the build — it does not
> write the code or open the PR; returned code re-enters as a reference.

## Open questions (read first)
- `patch: fix timezone drift` has no accepted outcome — confirm scope before building.
- _(or)_ None flagged. Confirm the deltas + impacted files below.

## What to build (traced deltas)

| change_kind | delta | traces to | impacted files (on disk) | affects AC |
|-------------|-------|-----------|--------------------------|------------|
| add    | CSV export on the approvals dashboard | BO-2 | `app/dashboard/export.py`, `app/routes.py` | AC-2.1 |
| change | widen the audit retention to 7y       | BO-4 | `app/audit/retention.py`                    | AC-4.3 |

## Discipline boundary
- Implement only the analysed scope above. Raise anything outside it as a finding —
  do not silently expand. Do not change scope without a new analysis.
- Return your work as a **PR / commit reference**; prove each affected acceptance
  criterion. Do not mark the change done — disposition is the human's.

## Build prompt (paste into a developer / build agent)
```
Implement the traced deltas in the "What to build" table above for <project> in
<repo path>. Build exactly that scope — each delta serves its traced outcome and
its acceptance criteria; do not add scope. Touch the impacted files listed (extend
them as the analysis implies, on disk). Prove each affected acceptance criterion.
Raise anything outside the analysed scope as a finding — do not silently expand it.
Return your work as a PR / commit reference; do not mark the change done.
```

## From the panel / red-team
_No panel convened + synthesised yet. Convene it to shape this brief, then regenerate._
```

## Notes / anti-patterns

- **Never invent scope.** The analysis is the only source of *what to build*. No
  analysis → halt (STEP 0), never a guessed feature. A missing delta, file, or AC
  stays an honest empty-state, never a fabricated one. (This skill's instance of
  the library GROUNDING rule — `skills/_contract/grounding-no-absent-input`.)
- **Scaffold, not build.** This emits a prompt; the developer agent writes the
  code. Do not implement, open a PR, or touch the repo here.
- **Carry the trace through.** The `derives_from` trace and the affected acceptance
  criteria travel into the prompt so the agent builds the right scope and proves it
  — and the null trace travels as an open question, never silently dropped.
- **Impacted files are the analysis's, on disk.** Preserve them verbatim from the
  upstream analysis (which verified them against the real tree); never add a file
  the analysis did not ground.
- **Returned code re-enters as a reference.** A PR link / a commit — never a stored
  blob. The brief stays a lean pointer document.
- **The deterministic base is the contract.** The enrich pass is a nicety; on any
  model error, ship the STEP 1 base. A plain, correct brief beats a polished,
  drifted one.
- **Propose, never dispose.** The brief and its prompt carry no approval state; the
  developer agent does not mark the change done. Disposition is a human act.
