---
name: scope-reconcile-check
description: Light advisory pass over a proposed release/change delta surfacing three drift questions (scope_creep = untraced add/change; dropped_requirement = a remove stranding the only live req under an outcome; breaks_outcome = an outcome no longer reflected in any section); never a blocking gate; dismissal-memory.
one_liner: Surface scope-drift questions over a proposed release delta.
aliases: [scope drift check, release sanity check, scope creep finder, untraced change check, requirement traceability check, pre-release review, scope assurance]
when_to_use: sanity-checking a proposed release for scope drift before it lands
output_kinds: [question, halt]
deterministic_fallback: the three deterministic checks over the delta
suggested_tier: mid
neighbours: Comes after deliver/triage-backlog-and-defer (a promoted item becomes a release delta). Comes before deliver/scaffold-then-handoff (handing the settled scope to a build).
---

# scope-reconcile-check

Surface scope drift in a proposed release as questions a human resolves.

When someone proposes a release — a bundle of requirement changes (adds, changes, removes) headed for a downstream project — this skill walks the delta and surfaces scope drift as **questions**. It never returns a verdict, a "pass", a "fail", or a blocking decision. It asks three questions and steps back.

## Purpose

Releases are where scope quietly drifts. A change sneaks in with no business outcome behind it. A removal strands the last requirement serving an outcome. A release reshapes work under an outcome the design no longer mentions. None of these are *errors* — each can be perfectly intentional — so this pass blocks nothing. It produces **scope-assurance questions** so a human can confirm the drift was deliberate before the release lands.

The pass is biased toward a deterministic base: the three checks are almost entirely mechanical set-arithmetic over the delta. An optional model step only *widens* one check's recall — it never overrides or escalates a deterministic result, and it never invents a blocking finding.

## When to use

- Sanity-checking a proposed release/change delta for scope drift **before it lands**.
- After someone drafts a batch of requirement changes and wants a second pair of eyes on whether the scope still ties back to outcomes.
- As an advisory step in a release recipe — surface the questions, let the human disposition them, then proceed regardless of the answers.

Do **not** use this as a merge barrier, an approval requirement, or a release stop. If a check fires and the human looks at it and shrugs, that is a valid, complete outcome. The questions are advisory.

## Inputs

The user supplies the proposed release delta plus enough project context to trace it. In any markdown/structured form:

1. **The change list** — *Required.* One row per requirement delta in the release. Each row has:
   - `change_kind`: `add` | `change` | `remove`
   - `req_key`: the requirement being added/changed/removed (e.g. `REQ-014`)
   - `derives_from` (the *trace edge*): the outcome `req_key` this change serves, or **empty/null** if it traces to nothing. A null trace is a deliberate scope-creep signal, not a mistake to auto-fix.
   - `rationale` (optional): why the change is proposed.

   If absent/unreadable/empty: HALT and ask where the delta is (per `_shared/grounding.md`); never invent a change or a `req_key`. There is no release to reconcile when there is no delta — "I read nothing" is not the same as "there were no drift questions." Readable forms: a markdown file, an xlsx/csv path, a GitHub Project owner+number, or a pasted block.

2. **The outcomes** — *Optional.* The project's business outcomes, each with a `req_key` and short text. If absent: run what you can (scope-creep on null traces is still computable) and say plainly that outcome-coverage checks were skipped; never invent an outcome to trace to.

3. **The current requirement set** — *Optional.* Live requirements with their `req_key`, the outcome each `derives_from`, and whether each is already retired (so a `remove` can be tested against its surviving siblings). If absent: skip check 2 and say so; never invent a sibling requirement.

4. **The current design sections** — *Optional.* The section bodies of the live solution design (titles + body text is enough). Used only as a literal-token corpus: "does outcome `BO-3` appear anywhere in the current design text?" If absent: skip check 3 and say so; never invent a section.

5. **Dismissal memory** — *Optional.* A list of previously-dismissed questions, each keyed by `(check_kind, req_key, section_key, message)`. Any question matching a remembered key is suppressed so it does not nag again.

If outcomes, requirements, or sections are missing, run what you can and say what was skipped — never fail the pass. The **change list** is the one exception: with no delta there is nothing to reconcile, so its absence HALTs and asks rather than returning a misleading clean pass.

This skill reads requirements, outcomes, and design over a release delta, so it follows the GROUNDING contract — the absent **Required** input (the delta) HALTs and asks; the **Optional** inputs degrade honestly and are never invented. See `skills/_contract/grounding-no-absent-input`.

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

This is the one check the optional model step can widen (see below), because literal-token matching misses outcomes that the design *describes* without naming by key.

## The method (steps)

### Step 0 — Locate / verify the delta (deterministic, pre-model)

Before anything is parsed, confirm the one **Required** input — the change list — is present as a file-level fact. Absent, unreadable, or empty (zero rows) → emit the clean halt below and **stop**. Do not return a clean pass: with no delta there is nothing to reconcile, and a silent-empty would read downstream as "the release had no drift," which is false.

```markdown
HALT — required input missing.

I can't reconcile a release for scope drift without the change list (the delta), and I won't invent one. Tell me where the proposed release lives and I'll pick up from there.

I can read any of these:
  • an xlsx / csv file path
  • a GitHub Project (owner + project number)
  • a docs folder (markdown / text)
  • the change rows pasted directly into the chat

Which one, and where? (Nothing is checked until you point me at the delta; an absent outcome/requirement/design set just narrows which of the three checks can run, but the delta itself is the input there is no pass without.)
```

The halt names the missing input and stops; it carries no question, no finding, and no verdict. With the change list present, proceed to the deterministic base below.

### Deterministic base (do this first; it is mostly mechanical)

1. **Parse the delta.** Read the change list, outcomes, current requirements, and section bodies into plain structures. Build a lookup from requirement `req_key` → its `derives_from` outcome and retired flag, and a map outcome → its live child requirements.

2. **Run check 1 (`release_scope_creep`).** For each `add`/`change` with an empty trace edge, emit the scope-creep question.

3. **Run check 2 (`release_dropped_requirement`).** For each `remove`, find the outcome's surviving live siblings (exclude the one being removed and any already retired). If none survive, emit the dropped-requirement question.

4. **Run check 3 (`release_breaks_outcome`).** Build the set of outcomes touched by the delta's trace edges. Build the literal-token corpus of all current section bodies. For each touched outcome whose `req_key` does not appear in the corpus, emit the breaks-outcome question.

5. **Apply dismissal memory.** Drop any emitted question whose `(check_kind, req_key, section_key, message)` tuple is in the supplied dismissal list. Keep stable ordering: check 1, then 2, then 3.

### Model step (optional — semantic widening of check 3 only)

6. **Widen `breaks_outcome` recall.** Literal-token matching is brittle: a design section can fully address an outcome while never citing its `req_key`. For each touched outcome that check 3 flagged, read the outcome text against the section bodies and judge whether the outcome is *semantically* reflected even though its key is absent. If it clearly is, **soften the question** — note that the outcome appears addressed in prose under section "X" and ask only whether the trace reference should be added, rather than asking whether to regenerate. If it is genuinely absent in substance too, leave the question as-is.

   Constraints on this step:
   - It only ever **relaxes or annotates** a check-3 question. It never adds a new blocking finding, never touches checks 1 or 2, and never converts a question into a verdict.
   - With no model available, **skip step 6 entirely** — the deterministic three checks are the complete, valid fallback.

## Output format

Return advisory markdown: a short header, then one bullet per surviving question grouped by check, then a one-line reminder that none of this blocks the release. If nothing fired, say so plainly.

### Template

```markdown
## Scope-reconcile — {release title or id}

Three advisory drift questions over the proposed delta. None of these block the release — they are scope-assurance questions for a human to confirm or wave through.

### Scope creep (untraced adds/changes)
- **REQ-021** — Release change REQ-021 traces to no outcome. Is there a business outcome behind it, or is this scope creep?

### Dropped requirements (a removal stranding an outcome)
- **REQ-008** — Removing REQ-008 drops the only current requirement serving outcome BO-2. Is that outcome being retired too?

### Outcomes the design has gone quiet on
- **BO-5** — This release changes work under outcome BO-5, but BO-5 is not reflected in any current design section. Should the affected sections be regenerated?
  - _(semantic note: BO-5 appears to be addressed in prose under "Data retention" without citing its key — consider adding the trace reference rather than regenerating.)_

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
- **Check 3 is literal-token first.** Run the deterministic key-match before the model widening, and let the model only soften, never harden. An outcome described-but-not-keyed is a *weaker* finding, not a stronger one.
- **Dismissal memory is keyed on stable handles + message**, not on free-text rationale. Editing a change's rationale must not resurrect a dismissed question; dismissing a question about one requirement must not silence a different drift on the same requirement.
- **Touched-only for check 3.** Do not run breaks-outcome over every outcome in the project — only the outcomes this release's delta actually touches. Whole-project outcome coverage is a different (design-time) pass, not this release-scope one.
- **Degrade, don't fail.** Missing sections, missing outcomes, or no model available all reduce coverage — say what you skipped and return what you have. This pass never errors out. (This skill's instance of the library GROUNDING rule — `skills/_contract/grounding-no-absent-input`: the Optional inputs degrade honestly, but the one Required input — the change list / delta — halts and asks per Step 0, because there is no release to reconcile without it.)
