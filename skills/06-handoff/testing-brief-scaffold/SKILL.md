---
name: testing-brief-scaffold
description: Scaffold a paste-ready testing handoff brief from accepted outcomes -> derived requirements -> acceptance criteria; one 'PROVE: <criterion>' line per AC, a deterministic-browser-testing approach block, and a fenced prompt for a testing agent. Use when handing testing to a specialist/agent during the implementation-help stage. Scaffold, not store.
when_to_use: handing testing to a specialist/agent during the implementation-help stage
output_kinds: [proposal]
deterministic_fallback: the PROVE-line spine + approach block
suggested_tier: sonnet
---

# testing-brief-scaffold

A test lead's charter generator. You give it the chain you already have —
**accepted outcomes -> derived requirements -> acceptance criteria** — and it
hands back a paste-ready testing brief whose spine is one `PROVE: <criterion>`
line per acceptance criterion. That charter is the deliverable. You hand it to a
testing agent or a QA specialist; the specs and the results live in **their**
repo/CI, not here.

**Scaffold, not store.** This skill produces a charter and a prompt. It does not
run tests, hold test cases, or keep results. The downstream repo owns those.

## Purpose

During the implementation-help stage you reach a point where the build is real
enough to prove. You do not want to hand a tester a vague "please test it." You
want a charter: an explicit, traceable list of what must be proven, derived
straight from the outcomes the business accepted and the acceptance criteria you
already wrote. This skill composes that charter, wraps it in a deterministic
end-to-end testing approach, and emits a fenced prompt the tester can paste into
their own agent.

The charter is front and centre. Everything else (open questions, approach,
prompt) frames it.

## When to use

- You are handing testing to a specialist or a testing agent.
- You have accepted outcomes, the requirements derived from them, and acceptance
  criteria on those requirements.
- You want the test scope to be **traceable** — every test exists because an AC
  demanded it, and every AC traces up to an accepted outcome.

Do **not** use this to store test cases or track test runs. The moment a tester
picks up the charter, ownership of specs and results moves to their repo/CI.

## Inputs

The user supplies markdown / context describing the project's chain. Anything
present is used; anything missing degrades to an honest "None flagged." line
rather than an invention.

- **Project title + one-line intake/summary** — the header and the "in one
  breath" framing.
- **Accepted outcomes** — the business-level results that were accepted. Each
  has a key (e.g. `OUT-1`) and text. These seed the charter sections.
- **Derived requirements**, traced to their parent outcome — each has a key
  (e.g. `REQ-12`), a type (F / NFR / etc.), and text.
- **Acceptance criteria per requirement** — the testable statements. Each
  becomes exactly one `PROVE:` line.
- **Orphans** (optional) — requirements with no clear outcome to test against.
  These become open questions, not silent omissions.
- **Panel synthesis** (optional) — if a deliberation/red-team panel shaped the
  work, fold its synthesis in so the brief reflects it.

## The method (STEPS)

This is a two-pass method. **Step 3 is deterministic** and is the load-bearing
spine — it runs with no model and is the guaranteed fallback. **Step 4 is the
LLM enrich pass** — it sharpens prose but must keep every fact from Step 3.

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
agent**; the platform/process scaffolds testing, it does not run or store the
tests.

### 3. DETERMINISTIC STEP — build the PROVE-line spine (the charter)

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

This spine alone — open questions + charter + approach (Step 5's static block) —
is a complete, usable brief. The LLM pass is enrichment, never a prerequisite.

### 4. LLM STEP — enrich, keeping every fact

Hand the deterministic scaffold to a model with one instruction: sharpen and
enrich into a clear, paste-ready handoff **without losing or inventing a single
fact**. The enrich pass may:

- tighten wording and improve flow;
- group or annotate PROVE lines for readability (e.g. note edge cases implied by
  an AC) — but never drop an AC or merge two into one;
- fold in the panel synthesis if present, under a "From the panel" section;
- surface a risk the chain implies but does not state, **as an open question**,
  not as new scope.

Grounding contract for the model:

- Keep every fact in the scaffold; do not invent scope.
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
3. `## What to prove (test charter)` — the PROVE-line spine, front and centre.
4. `## Approach`
5. `## Handoff prompt (paste into a testing agent)` — fenced.
6. `## From the panel` — only if a synthesis was supplied.

A full worked template ships alongside this skill:
[`references/prove-line.template.md`](references/prove-line.template.md).

Concrete excerpt of the charter spine:

```markdown
## What to prove (test charter)

### OUT-1 — A practice lead can see at a glance which projects need attention
- `REQ-4` (F) Portfolio view shows one RAG health verdict per project
    - PROVE: a project with an open roadblock renders a red verdict
    - PROVE: a healthy project renders a green verdict
    - PROVE: the verdict is derived on read (no stale persisted score)
- `REQ-7` (NFR) The portfolio view loads in under 2s for 200 projects
    - PROVE: with 200 seeded projects the dashboard first paint is < 2s

### OUT-2 — Nothing decided is silently lost
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
  charter, specs and results belong to their repo/CI. No gate, no approval, no
  sign-off lives here.
- **Deterministic spine is the contract.** The LLM pass is a nicety. If in doubt,
  ship the deterministic charter. A plain, correct charter beats a polished,
  drifted one.
