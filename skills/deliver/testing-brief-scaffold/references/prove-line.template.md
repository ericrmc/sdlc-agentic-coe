# Testing handoff — {{PROJECT_TITLE}}

> A scaffold to sharpen, then hand to a **testing agent**. The process scaffolds
> testing — it does not run or store the tests. Specs and results live in the
> downstream repo/CI.

## Open questions (read first)

<!--
  Lead with what is unresolved. One bullet per orphan requirement (a requirement
  with no clear outcome to test against). If there are none, emit the single
  honest fallback line below.
-->
- `{{ORPHAN_KEY}}` has no clear outcome to test against — confirm intent.
- None flagged. Confirm the acceptance criteria below are complete + testable.

## What to prove (test charter)

<!--
  THE CHARTER. Walk accepted outcomes -> derived requirements -> acceptance
  criteria. Emit exactly one `PROVE:` line per acceptance criterion. Preserve
  every key, type, and text exactly — traceability depends on it.

  If there are no accepted outcomes, replace this whole section with:
  _No accepted outcomes yet — accept outcomes upstream to seed the charter._
-->

### {{OUTCOME_KEY}} — {{OUTCOME_TEXT}}
- `{{REQUIREMENT_KEY}}` ({{REQ_TYPE}}) {{REQUIREMENT_TEXT}}
    - PROVE: {{ACCEPTANCE_CRITERION_1}}
    - PROVE: {{ACCEPTANCE_CRITERION_2}}
- `{{REQUIREMENT_KEY_2}}` ({{REQ_TYPE}}) {{REQUIREMENT_TEXT_2}}
    - PROVE: {{ACCEPTANCE_CRITERION_3}}

<!-- If an outcome has no derived requirements yet: -->
### {{OUTCOME_KEY_2}} — {{OUTCOME_TEXT_2}}
- _No derived requirements traced yet._

## Approach

- **Framework:** deterministic browser end-to-end (Playwright recommended —
  auto-waiting, headless, brings the stack up itself).
- **Determinism:** run against seeded data with a deterministic stub; assert
  post-state, no fixed sleeps.
- **Scaffold, not store:** specs + reports live in the repo; the process does
  not store test cases or results.

## Handoff prompt (paste into a testing agent)

```
Write and run deterministic end-to-end browser tests for {{PROJECT_TITLE}}. Prove
each acceptance criterion in the test charter above. Use the recommended framework
and a seeded, deterministic environment. Report pass/fail per charter item; raise
product defects as findings — do not fix them.
```

## From the panel

<!--
  Optional. Include ONLY if a deliberation / red-team panel was convened and
  synthesised. Fold its synthesis in exactly as given. If no panel was convened,
  omit this section entirely.
-->
{{PANEL_SYNTHESIS}}

---

## Worked example (delete before handoff)

# Testing handoff — Portfolio leadership view

> A scaffold to sharpen, then hand to a **testing agent**. The process scaffolds
> testing — it does not run or store the tests. Specs and results live in the
> downstream repo/CI.

## Open questions (read first)

- `REQ-22` has no clear outcome to test against — confirm intent.

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

### BO-3 — Cost reporting (not yet derived)
- _No derived requirements traced yet._

## Approach

- **Framework:** deterministic browser end-to-end (Playwright recommended —
  auto-waiting, headless, brings the stack up itself).
- **Determinism:** run against seeded data with a deterministic stub; assert
  post-state, no fixed sleeps.
- **Scaffold, not store:** specs + reports live in the repo; the process does
  not store test cases or results.

## Handoff prompt (paste into a testing agent)

```
Write and run deterministic end-to-end browser tests for Portfolio leadership view.
Prove each acceptance criterion in the test charter above. Use the recommended
framework and a seeded, deterministic environment. Report pass/fail per charter
item; raise product defects as findings — do not fix them.
```
