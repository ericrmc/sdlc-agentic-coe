---
name: testing-brief-scaffold
description: Scaffold a paste-ready testing handoff brief from accepted outcomes -> derived requirements -> acceptance criteria; one 'PROVE: <criterion>' line per AC, a deterministic-browser-testing approach block, and a fenced prompt for a testing agent. Use when handing testing to a specialist/agent during the implementation-help stage. Scaffold, not store.
when_to_use: handing testing to a specialist/agent during the implementation-help stage
output_kinds: [proposal, halt]
deterministic_fallback: the PROVE-line charter + approach block
one_liner: Generate a traceable, paste-ready testing handoff brief.
aliases: [test plan, QA handoff, test charter, acceptance test brief, test handoff, testing instructions, what to test, hand testing to QA]
suggested_tier: mid
neighbours:
  before: skills/deliver/scaffold-then-handoff
  after: skills/deliver/design-studio-brief-scaffold
---

# testing-brief-scaffold

Generate a traceable, paste-ready testing handoff brief from a chain of
**accepted outcomes -> derived requirements -> acceptance criteria**. The brief's
load-bearing core is one `PROVE: <criterion>` line per acceptance criterion. That
charter is the deliverable; it is handed to a testing agent or a QA specialist,
and the specs and results then live in that downstream repo/CI.

**Scaffold, not store.** This skill produces a charter and a prompt. It does not
run tests, hold test cases, or keep results. The downstream repo owns those.

## Purpose

When a build is real enough to prove, a tester needs more than "please test it."
A charter is an explicit, traceable list of what must be proven, derived straight
from the outcomes the business accepted and the acceptance criteria already
written against them. This skill composes that charter, wraps it in a
deterministic end-to-end testing approach, and emits a fenced prompt the tester
pastes into their own agent.

The charter is front and centre. Everything else (open questions, approach,
prompt) frames it.

## When to use

- Testing is being handed to a specialist or a testing agent.
- Accepted outcomes exist, with requirements derived from them and acceptance
  criteria on those requirements.
- The test scope must be **traceable** — every test exists because an AC demanded
  it, and every AC traces up to an accepted outcome.

Do **not** use this to store test cases or track test runs. The moment a tester
picks up the charter, ownership of specs and results moves to their repo/CI.

## Inputs

Markdown / context describing the project's chain. Anything present is used;
anything missing degrades to an honest "None flagged." / "_No X yet_" line rather
than an invention.

- **Project title** — *Required.* The header and the "in one breath" framing. If
  absent/unreadable/empty: HALT and ask what project this is for (per
  `_shared/grounding.md`); never invent a project to brief. Readable forms: a
  markdown file, a docs folder, a GitHub Project owner+number, or a pasted block.
- **One-line intake/summary** — *Optional.* If absent: render the honest "no
  intake description" line, never an invented summary.
- **Accepted outcomes** — *Optional.* The business-level results that were
  accepted. Each has a key (e.g. `BO-1`) and text. These seed the charter
  sections. If absent: emit `_No accepted outcomes yet — accept outcomes upstream
  to seed the charter._`; never fabricate an outcome or scope.
- **Derived requirements**, traced to their parent outcome — *Optional.* Each has
  a key (e.g. `REQ-12`), a type (F / NFR / etc.), and text. If absent for an
  outcome: emit `_No derived requirements traced yet._`; never invent a `REQ-` key.
- **Acceptance criteria per requirement** — *Optional.* The testable statements;
  each becomes exactly one `PROVE:` line. If absent: render no PROVE line for that
  requirement; never invent a criterion to fill the charter.
- **Orphans** — *Optional.* Requirements with no clear outcome to test against.
  These become open questions, not silent omissions.
- **Panel synthesis** — *Optional.* If a deliberation/red-team panel shaped the
  work, fold its synthesis in so the brief reflects it.

**Why this skill degrades rather than halts on the chain.** Only the **project
title** is a hard Required input (a brief needs a subject). The outcomes →
requirements → AC chain is *deliberately Optional*: this skill's whole value is
producing a thin-but-honest brief that leads with open questions and renders an
explicit empty-state for every gap, so a missing AC surfaces as a visible hole the
specialist sees — not a halt that stops the handoff. That honest-empty handling of
an absent input is exactly what the GROUNDING contract permits in place of a halt
(`skills/_shared/grounding.md`: "an absent *optional* input proceeds honestly … as
a question or an explicit null — never padded with invented content"). What it
never does is **invent scope** to look complete — every key, type, and text is
preserved verbatim or rendered as an honest empty-state. See
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

## The method (STEPS)

This is a two-pass method. **Step 3 is the deterministic base** — it runs with no
model and is the guaranteed fallback. **Step 4 is the model enrich pass** — it
sharpens prose but must keep every fact from Step 3.

### 0. Locate / verify the project (deterministic, pre-model)

Confirm the one hard **Required** input — the **project title** — is present as a
file-level fact. Absent, unreadable, or empty → emit the clean halt below and
**stop**. (The outcomes → requirements → AC chain is Optional and never halts: a
missing chain renders the honest empty-states in Steps 1 and 3, never an
invention.)

```markdown
HALT — required input missing.

I can't scaffold a testing handoff without knowing what project it is for, and I
won't invent one. Tell me the project and I'll pick up from there.

I can read any of these:
  • a markdown file path
  • a docs folder (markdown / text)
  • a GitHub Project (owner + project number)
  • the project title + chain pasted directly into the chat

Which one, and where? (Once I have the project I'll build the charter from whatever
chain is present and flag the rest as open questions — nothing is invented.)
```

The halt names the missing input and stops; it carries no charter, no PROVE line,
and no verdict. With the project title present, proceed to Step 1.

### 1. Lead with open questions

House style: the brief opens with what is unresolved, before what is known.

- For every orphan requirement, emit:
  `` - `<KEY>` has no clear outcome to test against — confirm intent.``
- If there are no orphans, emit one honest line:
  `- None flagged. Confirm the acceptance criteria below are complete + testable.`

A tester reads this section first and knows immediately where the scope is soft.

### 2. Frame the project in one breath

Header (`# Testing handoff — <title>`) and a short scaffold note making the
discipline explicit: this is a scaffold to sharpen and hand to a **testing
agent**; it scaffolds testing, it does not run or store the tests.

### 3. DETERMINISTIC STEP — build the PROVE-line charter

This is the heart of the skill and runs with no model. Walk the chain
top-down and emit the charter:

```
for each accepted OUTCOME:
    emit a charter section heading:  ### <OUT-KEY> — <outcome text>
    for each derived REQUIREMENT traced to that outcome:
        emit:  - `<REQ-KEY>` (<type>) <requirement text>
        for each ACCEPTANCE CRITERION on that requirement:
            emit:      - PROVE: <criterion text>
    if the outcome has no derived requirements:
        emit:  - _No derived requirements traced yet._
```

Rules that make it deterministic and honest:

- **One `PROVE:` line per acceptance criterion.** No merging, no inventing. The
  set of PROVE lines IS the test charter.
- If there are no accepted outcomes, do not fabricate scope — emit
  `_No accepted outcomes yet — accept outcomes upstream to seed the charter._`
- Preserve every key, type, and text verbatim. Traceability depends on the keys
  surviving untouched.

This deterministic base alone — open questions + charter + approach (Step 5's
static block) — is a complete, usable brief. The model pass is enrichment, never
a prerequisite.

### 4. MODEL STEP — enrich, keeping every fact

Hand the deterministic scaffold to a model with one instruction: sharpen and
enrich into a clear, paste-ready handoff **without losing or inventing a single
fact**. The enrich pass may:

- tighten wording and improve flow;
- group or annotate PROVE lines for readability (e.g. note edge cases implied by
  an AC) — but never drop an AC or merge two into one;
- fold in the panel synthesis if present, under a "From the panel" section;
- surface a risk the chain implies but does not state, **as an open question**,
  not as new scope.

Grounding contract for the model (an instance of the library's GROUNDING rule
quoted above — `skills/_contract/grounding-no-absent-input`):

- Keep every fact in the scaffold; do not invent scope. A missing AC stays an
  honest empty-state, never a fabricated criterion.
- Lead with open questions.
- Keep the test charter (PROVE lines) front and centre.
- Preserve "scaffold, not store" — specs and results live in the repo/CI.

If the model errors, is unavailable, or drifts off-scope, **ship the Step 3
deterministic scaffold as-is.** That is the `deterministic_fallback`.

### 5. Attach the approach block and the handoff prompt

Static, every time:

**Approach** — deterministic end-to-end browser testing:

- *Framework:* deterministic browser end-to-end (Playwright recommended —
  auto-waiting, headless, brings the stack up itself).
- *Determinism:* run against seeded data with a deterministic stub; **assert
  post-state, not fixed sleeps.**
- *Scaffold, not store:* specs + reports live in the repo; the process does not
  store test cases or results.

**Handoff prompt** — a fenced block the tester pastes into their own agent:

```
Write and run deterministic end-to-end browser tests for <title>. Prove each
acceptance criterion in the test charter above. Use the recommended framework
and a seeded, deterministic environment. Report pass/fail per charter item;
raise product defects as findings — do not fix them.
```

## Output format

A single markdown brief, ready to paste. Structure (in order):

1. `# Testing handoff — <title>` + the scaffold note.
2. `## Open questions (read first)`
3. `## What to prove (test charter)` — the PROVE-line charter, front and centre.
4. `## Approach`
5. `## Handoff prompt (paste into a testing agent)` — fenced.
6. `## From the panel` — only if a synthesis was supplied.

A full worked template ships alongside this skill:
[`references/prove-line.template.md`](references/prove-line.template.md).

Concrete excerpt of the charter:

```markdown
## What to prove (test charter)

### BO-1 — A practice lead can see at a glance which projects need attention
- `REQ-4` (F) Portfolio view shows one RAG health verdict per project
    - PROVE: a project with an open roadblock renders a red verdict
    - PROVE: a healthy project renders a green verdict
    - PROVE: the verdict is derived on read (no stale persisted score)
- `REQ-7` (NFR) The portfolio view loads in under 2s for 200 projects
    - PROVE: with 200 seeded projects the dashboard first paint is < 2s

### BO-2 — Nothing decided is silently lost
- `REQ-9` (F) Dismissed roadblocks are remembered and not re-raised
    - PROVE: a dismissed roadblock does not reappear after regeneration
```

## Notes / anti-patterns

- **Charter-first, always.** If a reader cannot find the PROVE lines in two
  seconds, the brief has failed. Open questions and approach frame the charter;
  they never bury it.
- **One AC, one PROVE line.** Do not collapse criteria to look tidy — each PROVE
  line is the trace from a test back to an accepted outcome. Collapsing breaks
  traceability.
- **Never invent scope.** Missing data degrades to "None flagged." or
  "_No accepted outcomes yet_", never to a guessed requirement. A risk you spot
  goes in *open questions*, not in the charter.
- **Assert post-state, never sleep.** The approach block is opinionated for a
  reason — fixed sleeps produce flaky charters. Auto-waiting + seeded data +
  post-state assertions are non-negotiable defaults.
- **Scaffold, not store.** This is light and advisory. It produces a charter and
  hands off. It is not a test-management system; the instant a tester takes the
  charter, specs and results belong to their repo/CI. No approval or sign-off
  lives here.
- **The deterministic base is the contract.** The model pass is a nicety. If in
  doubt, ship the deterministic charter. A plain, correct charter beats a
  polished, drifted one.
