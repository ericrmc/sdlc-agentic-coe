---
name: scope-reconcile-check
description: Light advisory pass over a proposed release/change delta surfacing three drift questions (scope_creep = untraced add/change; dropped_requirement = a remove stranding the only live req under an outcome; breaks_outcome = an outcome no longer reflected in any section); never a blocking gate; dismissal-memory.
when_to_use: sanity-checking a proposed release for scope drift before it lands
output_kinds: [question]
deterministic_fallback: the three deterministic checks over the delta
suggested_tier: sonnet
---

# scope-reconcile-check

A light, advisory release pass. When someone proposes a release — a bundle of requirement changes (adds, changes, removes) headed for a downstream project — this skill walks the delta and surfaces **scope drift as questions a human resolves**. It never returns a verdict, a "fail", or a gate. It asks three questions and steps back.

## Purpose

Releases are where scope quietly drifts. A change sneaks in with no business outcome behind it. A removal strands the last requirement serving an outcome. A release reshapes work under an outcome the design no longer mentions. None of these are *errors* — each can be perfectly intentional — so this pass does not block anything. It produces **scope-assurance questions** so a human can confirm the drift was deliberate before the release lands.

The whole pass is biased toward the deterministic spine: the three checks are almost entirely mechanical set-arithmetic over the delta. The optional LLM step only *widens* one check's recall — it never overrides or escalates a deterministic result, and it never invents a blocking outcome.

## When to use

- Sanity-checking a proposed release/change delta for scope drift **before it lands**.
- After someone drafts a batch of requirement changes and wants a second pair of eyes on whether the scope still ties back to outcomes.
- As an advisory step in a release recipe — surface the questions, let the human disposition them, then proceed regardless of the answers.

Do **not** use this as a merge gate, an approval barrier, or a release stop. If a check fires and the human looks at it and shrugs, that is a valid, complete outcome. The questions are advisory.

## Inputs

The user supplies the proposed release delta plus enough project context to trace it. In any markdown/structured form:

1. **The change list** — one row per requirement delta in the release. Each row has:
   - `change_kind`: `add` | `change` | `remove`
   - `req_key`: the requirement being added/changed/removed (e.g. `REQ-014`)
   - `derives_from` (the *trace edge*): the outcome `req_key` this change serves, or **empty/null** if it traces to nothing. A null trace is a deliberate scope-creep signal, not a mistake to auto-fix.
   - `rationale` (optional): why the change is proposed.

2. **The outcomes** — the project's business outcomes, each with a `req_key` and short text.

3. **The current requirement set** — live requirements with their `req_key`, the outcome each `derives_from`, and whether each is already retired (so a `remove` can be tested against its surviving siblings).

4. **The current design sections** — the section bodies of the live solution design (titles + body text is enough). Used only as a literal-token corpus: "does outcome `OUT-3` appear anywhere in the current design text?"

5. **Dismissal memory** (optional) — a list of previously-dismissed questions, each keyed by `(check_kind, req_key, section_key, message)`. Any question matching a remembered key is suppressed so it does not nag again.

If sections or outcomes are missing, run what you can and say what was skipped — never fail the pass.

## The three checks

Each check is a **question**, never a verdict. Each carries no status. Each is keyed for dismissal on the tuple `(check_kind + req_key + section_key + message)` — so dismissing one question does not silence a *different* drift sharing the same requirement, and re-running after an unrelated edit does not resurrect a question the human already waved through.

### 1. `release_scope_creep` — an untraced add/change

For every change whose `change_kind` is `add` or `change` and whose trace edge (`derives_from`) is **empty/null**: the change has no business outcome behind it.

> Release change `{req_key or change_kind}` traces to no outcome. Is there a business outcome behind it, or is this scope creep?

A null trace is intentionally allowed at draft time — it is the deliberate signal this check exists to surface. The human either points it at an outcome or confirms it is wanted anyway.

### 2. `release_dropped_requirement` — a remove that strands an outcome

For every change whose `change_kind` is `remove`: find the outcome the removed requirement serves (its `derives_from`). Look at that outcome's other live children — requirements that derive from the same outcome, are not the one being removed, and are not already retired. If there are **none left**, removing this requirement leaves the outcome with no coverage.

> Removing `{req_key}` drops the only current requirement serving outcome `{outcome_key}`. Is that outcome being retired too?

This does not block the removal. It asks whether the outcome should follow the requirement out the door.

### 3. `release_breaks_outcome` — an outcome no longer reflected in any section

Collect the outcomes this release *touches* — every outcome named by some change's trace edge. For each touched outcome, check whether its `req_key` appears as a literal token anywhere in the current design section bodies. If it appears **nowhere**, the release is reshaping work under an outcome the design has gone quiet on.

> This release changes work under outcome `{outcome_key}`, but `{outcome_key}` is not reflected in any current design section. Should the affected sections be regenerated?

This is the one check the optional LLM step can widen (see below), because literal-token matching misses outcomes that the design *describes* without naming by key.

## The method (steps)

### Deterministic spine (do this first; it is mostly mechanical)

1. **Parse the delta.** Read the change list, outcomes, current requirements, and section bodies into plain structures. Build a lookup from requirement `req_key` → its `derives_from` outcome and retired flag, and a map outcome → its live child requirements.

2. **Run check 1 (`release_scope_creep`).** For each `add`/`change` with an empty trace edge, emit the scope-creep question.

3. **Run check 2 (`release_dropped_requirement`).** For each `remove`, find the outcome's surviving live siblings (exclude the one being removed and any already retired). If none survive, emit the dropped-requirement question.

4. **Run check 3 (`release_breaks_outcome`).** Build the set of outcomes touched by the delta's trace edges. Build the literal-token corpus of all current section bodies. For each touched outcome whose `req_key` does not appear in the corpus, emit the breaks-outcome question.

5. **Apply dismissal memory.** Drop any emitted question whose `(check_kind, req_key, section_key, message)` tuple is in the supplied dismissal list. Keep stable ordering: check 1, then 2, then 3.

### LLM step (optional — semantic widening of check 3 only)

6. **Widen `breaks_outcome` recall.** Literal-token matching is brittle: a design section can fully address an outcome while never citing its `req_key`. For each touched outcome that check 3 flagged, read the outcome text against the section bodies and judge whether the outcome is *semantically* reflected even though its key is absent. If it clearly is, **soften the question** — note that the outcome appears addressed in prose under section "X" and ask only whether the trace reference should be added, rather than asking whether to regenerate. If it is genuinely absent in substance too, leave the question as-is.

   Constraints on this step:
   - It only ever **relaxes or annotates** a check-3 question. It never adds a new blocking finding, never touches checks 1 or 2, and never converts a question into a verdict.
   - If you have no model available, **skip step 6 entirely** — the deterministic three checks are the complete, valid fallback.

## Output format

Return advisory markdown: a short header, then one bullet per surviving question grouped by check, then a one-line reminder that none of this blocks the release. If nothing fired, say so plainly.

### Template

```markdown
## Scope-reconcile — {release title or id}

Three advisory drift questions over the proposed delta. None of these block the release — they are scope-assurance questions for a human to confirm or wave through.

### Scope creep (untraced adds/changes)
- **REQ-021** — Release change REQ-021 traces to no outcome. Is there a business outcome behind it, or is this scope creep?

### Dropped requirements (a removal stranding an outcome)
- **REQ-008** — Removing REQ-008 drops the only current requirement serving outcome OUT-2. Is that outcome being retired too?

### Outcomes the design has gone quiet on
- **OUT-5** — This release changes work under outcome OUT-5, but OUT-5 is not reflected in any current design section. Should the affected sections be regenerated?
  - _(semantic note: OUT-5 appears to be addressed in prose under "Data retention" without citing its key — consider adding the trace reference rather than regenerating.)_

_3 questions surfaced, 0 suppressed by dismissal memory. Advisory only — disposition each and proceed._
```

### Clean pass

```markdown
## Scope-reconcile — {release title or id}

No scope-drift questions. Every add/change traces to an outcome, no removal strands an outcome, and every touched outcome is reflected in the current design. Advisory pass complete.
```

## Notes / anti-patterns

- **Never emit a verdict.** No "pass", "fail", "blocked", "approved". Every line is a question or an observation. If you find yourself writing a disposition, you have left this skill's job.
- **A null trace edge is a signal, not a bug.** Do not auto-attach an outcome to an untraced change. Surface it and let the human decide.
- **Removals never delete.** Check 2 asks about an outcome losing coverage; it does not propose erasing the trace edge. The retired requirement and its edge survive — only its live status changes.
- **Check 3 is literal-token first.** Run the deterministic key-match before the LLM widening, and let the LLM only soften, never harden. An outcome described-but-not-keyed is a *weaker* finding, not a stronger one.
- **Dismissal memory is keyed on stable handles + message**, not on free-text rationale. Editing a change's rationale must not resurrect a dismissed question; dismissing a question about one requirement must not silence a different drift on the same requirement.
- **Touched-only for check 3.** Do not run breaks-outcome over every outcome in the project — only the outcomes this release's delta actually touches. Whole-project outcome coverage is a different (design-time) pass, not this release-scope one.
- **Degrade, don't fail.** Missing sections, missing outcomes, or no model available all reduce coverage — say what you skipped and return what you have. This pass never errors out.
