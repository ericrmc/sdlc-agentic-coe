---
name: red-team-requirements
description: Adversarially critique a requirement set and emit one dismissible challenge per genuine issue over the closed 9-kind taxonomy (vague, unquantified, untestable, solution_shaped, orphan_value, conflicting, gold_plated, missing_nfr, off_vision); conservative on conflicting/gold_plated; never picks a winner, deletes scope, or sets status.
one_liner: Pressure-test a requirement set for conflicts, gaps, and gold-plating.
aliases: [requirements review, critique requirements, find conflicting requirements, requirements quality check, scope creep check, ambiguous requirements, missing NFR check, requirements sanity check]
when_to_use: pressure-testing a requirement set before solutioning — the highest-value review pass. Run it after requirements are derived and before identifying capabilities or recommending components.
output_kinds: [question, proposal]
deterministic_fallback: the 9-kind vocabulary as a manual review checklist
suggested_tier: frontier
tier_reason: adversarial judgement over a whole set, with strict precision discipline on conflict/gold-plating — strong reasoning required.
neighbours: runs after `understand/nfr-coverage-check` (requirements derived and NFR-checked); feeds `challenge/surface-risks-and-assumptions` and the rest of the challenge pass.
---

# red-team-requirements

Pressure-test a requirement set for conflicts, gaps, and gold-plating.

This pass red-teams a *set* of requirements and surfaces the things a human keeps
missing — the unquantified NFR, the solution wearing a requirement's clothes, the two
clauses that quietly contradict each other, the scope nobody asked for.

It is **advisory**. It flags issues and poses questions. It cannot make a decision: it
never picks a winner between two conflicting requirements, never deletes or rejects
scope, never sets or changes any requirement's status. A human triages every challenge.

---

## Purpose

Given a project's current requirement set, produce **one dismissible challenge per
genuine issue**, each tagged with exactly one `kind` from a **closed 9-kind taxonomy**.
A challenge names the offending requirement(s) by id, states the problem concretely,
and proposes an action — but the verdict is always left to the human.

What this skill does:

- Reads the live requirement set (proposed + accepted rows; edited/rejected are settled
  history and out of scope).
- Emits challenges of exactly nine kinds — no others. See **The method** below for the
  precise definitions and `references/challenge-kinds.md` for the closed vocabulary.
- Is **conservative on `conflicting` and `gold_plated`**: precision over recall. A false
  conflict or false gold-plating corrodes trust in the channel, so these only fire on a
  hard signal and stay silent on mere ambiguity.

What this skill **never** does:

- Pick a winner between two conflicting requirements. It *poses the disambiguation
  question* and names both ids.
- Delete, reject, or down-scope a requirement. For `gold_plated` it *asks whether the
  extra scope is justified*; it never removes it.
- Set, change, or advance any requirement's `status` / disposition / version. It only
  produces challenges; a human dismisses or addresses each one.
- Invent requirements that are not in the supplied set.

The mental model: a sharp, sceptical reviewer who annotates someone else's requirement
list in the margin with pointed questions, then hands it back — without holding the pen
on the requirements themselves.

> **Multi-agent option (advisory).** This step deepens with independent parallel agents:
> launch one sub-agent per objection (or per requirement cluster), at most 4 at a time,
> each a separate sub-agent. A failed sub-agent returns nothing and is never fatal — the
> deterministic base stands; merge what succeeded. (Claude Code: use the Task tool /
> subagents. Other tools: launch parallel model calls; or a matrix-strategy CI job.)
> Never required — it adds coverage and cuts single-pass bias. See
> `skills/_contract/parallel-agents`.

---

## When to use

- After requirements have been **derived from business vision/outcomes** and assessed
  (technical / solution / overlap), and **before** identifying capabilities, recommending
  components, or starting solution architecture.
- Any time a requirement set has churned and a fresh pressure test is wanted.
- As a recurring, idempotent pass — re-running it should produce the same challenges for
  the same text (clear prior open challenges, re-emit the fresh set, preserve the
  human's addressed/dismissed history).

Run it when the requirement set feels "done" — that is exactly when its blind spots are
most expensive to miss downstream.

---

## Inputs

The user supplies, as markdown or pasted context:

1. **Project title** — one line.
2. **Project context / vision** — the foreword / north star. Needed for `off_vision`;
   if it is terse or absent, the vision guard simply does not fire (no false steers).
3. **The requirement set** — the live proposed/accepted rows. Each row should carry, at
   minimum:
   - a **stable numeric `id`** (challenges reference rows by their real id),
   - the **requirement text**,
   - ideally a **type** (`F` functional / `NF` non-functional) and, if known, a
     **`value_outcome`** (the linked business outcome) and **`derives_from_id`** (parent
     requirement). These sharpen `unquantified`, `orphan_value`, and `gold_plated` and
     the conflict overlap guard — but the skill degrades gracefully without them.

A minimal input block looks like:

```
PROJECT TITLE: Claims intake modernisation
PROJECT CONTEXT / VISION: Cut manual claim triage time in half while keeping
  every decision auditable for the regulator.

REQUIREMENTS:
#8  [NF] The system must purge audit logs after 30 days.
#12 [NF] The API should be fast.
#14 [NF] The system must not purge audit logs.
#21 [F]  Provide a Kafka topic for downstream consumers.   (value_outcome: none)
#27 [F]  The triage screen should be intuitive and easy to use.
```

---

## The method

The skill runs a **deterministic base** (a per-requirement and pairwise checklist that
fires on hard signals) and a **model reasoning step** (a critique prompt that reads the
whole set and emits structured challenges). Use both: the deterministic base is a
backstop that guarantees the obvious issues are never missed; the model step catches the
subtle, semantic ones. When they agree, confidence is high; when only the model fires,
treat it as a softer steer.

Both layers emit the **same nine kinds and the same JSON shape**, so their outputs merge.

### The closed nine-kind taxonomy (reproduce these definitions precisely)

`kind` MUST be exactly one of these nine values — use no others:

- **`vague`** — references a control/term (e.g. CORS, an origin, a role) without naming
  the exact value, so it cannot be measured as written.
- **`unquantified`** — a non-functional goal stated with NO number/target (e.g. "fast",
  "secure", "scalable").
- **`untestable`** — a subjective quality ("user-friendly", "intuitive", "seamless",
  "easy to use") with no observable acceptance criterion.
- **`solution_shaped`** — names a mechanism/product/technology rather than the underlying
  need (solutioneering).
- **`orphan_value`** — no business outcome can be inferred; the requirement is not linked
  to value.
- **`conflicting`** — two requirements genuinely contradict: contradictory quantified
  targets on the same subject, mutually-exclusive constraints (e.g. on-prem vs
  cloud-only), OR a LITERAL OPPOSITE / negation (one forbids what the other requires on
  the same subject, e.g. "must purge logs after 30 days" vs "must not purge logs"), OR
  heavy semantic overlap that is actually contested. Name BOTH ids: set `requirement_id`
  to the LOWER id and `contests_id` to the OTHER (higher) id. POSE the disambiguation
  question; NEVER choose a winner. Watch for SCOPED prohibitions that are NOT a true
  conflict (e.g. "must not retain logs CONTAINING card numbers" does not conflict with
  "retain logs 90 days") — do not flag those.
- **`gold_plated`** — reaches for extra scope ("nice to have", "ideally", "as well as",
  "stretch goal") with no business outcome to justify it. ASK whether the extra
  capability is required; do not drop scope.
- **`missing_nfr`** — a SET-LEVEL gap: an entire NFR category is uncovered. Set
  `requirement_id` to null. Use ONLY these category names: `security`, `availability`,
  `performance`, `data_residency`, `maintainability`, `scalability`.
- **`off_vision`** — a requirement introduces a direction NOT reflected in the PROJECT
  VISION (the foreword) or the rest of the set — a possible unintended drift by someone
  who cannot see the whole picture. ADVISORY only: flag it as a light steer to confirm
  against the north star; it never blocks acceptance. Only emit this when a vision is
  present and the drift is real.

The full closed vocabulary — with the `requirement_id` / `contests_id` rules per kind —
is reproduced as a reference card in `references/challenge-kinds.md`.

### The `conflicting` rules (read these carefully — this is where trust is won or lost)

`conflicting` is the most valuable and the most dangerous kind. A *false* conflict
corrodes trust in the entire channel. Apply these rules strictly:

1. **Name BOTH ids.** Set `requirement_id` to the **LOWER** id and `contests_id` to the
   **OTHER (higher)** id. Sorting the pair this way makes the challenge stable under
   input reordering and gives it a stable dismissal signature. For every *other* kind,
   omit `contests_id` or set it null.
2. **Require a shared subject.** Two requirements only conflict if they are about the
   *same thing*. The deterministic base proves this via subject-token overlap (content
   words, stop-words and high-frequency domain words excluded, so "the system shall"
   does not count as a shared subject). Do not flag a "conflict" between requirements on
   unrelated topics.
3. **Require a scoped-prohibition guard on negations.** When one side forbids what the
   other mandates, check whether the prohibition is **scoped/conditional** — markers like
   *containing, when, unless, except, older than, raw, only, if*. A scoped prohibition is
   NOT a blanket opposite.
   - **DO flag**: `"must purge logs after 30 days"` vs `"must not purge logs"` — a true
     blanket opposite on the same subject.
   - **Do NOT flag**: `"must not retain logs CONTAINING card numbers"` vs `"retain logs
     90 days"` — the prohibition is scoped to a subset; the two can both hold.
   See `examples/conflicting-vs-scoped.md` for the few-shot demonstration.
4. **POSE the disambiguation; never choose.** The message asks *"Which requirement holds
   — or do they apply to different scopes?"* The suggested action says *"Reconcile the
   two (pick the binding rule or scope each). The agent does not choose a winner."* Do
   not assert which one is right.
5. **Fire only on a hard signal.** The hard triggers are: (a) contradictory
   quantified targets on the same subject+dimension (two different time magnitudes
   normalised to a common unit, or two different percentages, with ≥2 shared subject
   tokens); (b) mutually-exclusive constraints from a known hard-opposite list (on-prem
   vs cloud-only, multi-region vs single-region, synchronous vs asynchronous, stateless
   vs stateful, offline vs always-online); (c) explicit hard negation (must not / shall
   not / may not / is prohibited / is forbidden …) of the other's mandate on a shared
   subject (≥3 shared tokens, unscoped). Heavy *overlap* (many shared subject terms,
   same type, not a parent/child derive pair) is a softer, advisory signal — surface it
   as "may be duplicative or contested", do not assert a conflict.

### `missing_nfr` is set-level

`missing_nfr` is the one kind that is **not about a single requirement**. It reports that
an entire NFR **category** is uncovered by the whole set. Therefore:

- Set `requirement_id` to **null**.
- Use ONLY these six category names: `security`, `availability`, `performance`,
  `data_residency`, `maintainability`, `scalability`.
- Emit at most one challenge per uncovered category. A category is "covered" if *any*
  live requirement's text addresses it.

### Conservatism on `conflicting` and `gold_plated`

Precision over recall. **A false conflict corrodes trust** — and so does false
gold-plating. For both kinds:

- Fire only on a specific, hard signal.
- Stay **silent on mere ambiguity**. If you are unsure whether two requirements conflict,
  do not emit a `conflicting` challenge — at most note a heavy *overlap* as advisory.
- For `gold_plated`, only fire when there is explicit discretionary language ("nice to
  have", "ideally", "would be great", "as well as", "stretch goal", "if possible", …)
  AND, for purely *additive* reach ("as well as", "also support", "additionally
  support"), only when there is **no** captured `value_outcome` to back the extra scope.
  A well-grounded broad requirement stays silent.

### Step by step

**Step 1 — Scope the live set.** Take only requirements whose status is `proposed` or
`accepted`. Ignore edited/rejected rows. This is the set the critic reasons over for
every kind.

**Step 2 — Deterministic per-requirement pass (backstop).** For each live requirement,
walk the checklist and emit a challenge when a rule fires:
- `unquantified` — type is `NF` and the text states a goal with no number/target.
- `solution_shaped` — the text names a mechanism/product/technology instead of the need.
- `orphan_value` — no business outcome can be inferred (`value_outcome` empty).
- `vague` — references a control/term (e.g. CORS) without naming the exact value (e.g.
  CORS mentioned but no origin/method named).
- `untestable` — contains a subjective quality ("user-friendly", "intuitive", "easy to
  use", "seamless") with no acceptance criterion.

**Step 3 — Deterministic pairwise pass (backstop, conservative).** Over ordered-unique
pairs of live requirements, apply the `conflicting` triggers above with the shared-subject
gate and the scoped-prohibition guard. Emit one `conflicting` challenge per genuinely
conflicting pair, naming both ids (lower = `requirement_id`, higher = `contests_id`).

**Step 4 — Deterministic gold-plating pass (backstop, conservative).** For each live
requirement with discretionary language, emit a `gold_plated` challenge that asks whether
the extra scope is justified by the captured outcome. Apply the additive-language guard.

**Step 5 — Deterministic set-level passes (backstop).**
- `missing_nfr` — compute coverage over the six categories; emit one `missing_nfr`
  challenge (requirement_id null) per uncovered category.
- `off_vision` — only if a non-terse vision is present: flag any proposed requirement
  that introduces several subject tokens absent from both the vision and the accepted
  corpus, as a possible unintended drift. Advisory; never blocks.

**Step 6 — Model reasoning pass (the semantic critic).** Run the critique prompt below
over the full set. It catches the subtle issues the keyword backstop cannot: a conflict
phrased without the trigger words, a solution-shaped requirement using novel
terminology, a real but non-obvious vision drift. It emits the *same nine kinds* in the
*same JSON shape*.

**Step 7 — Merge and de-duplicate.** Combine the deterministic and model challenges. When
both fired the same kind on the same requirement(s), keep one (prefer the more specific
message). Present the merged list. Every challenge stays `open` until a human dismisses
or addresses it.

### The model step — the critique prompt

Use this prompt as written (substitute the bracketed inputs). It encodes the advisory
contract, the nine-kind constraint, and the exact output shape.

```
You red-team a project's current requirement set and surface dismissible CHALLENGES
for a human to triage. You are ADVISORY: you flag and pose questions; you NEVER pick a
winner, delete scope, or change any requirement's status. A human decides every
challenge.

PROJECT TITLE: [project_title]

PROJECT CONTEXT / VISION:
[project_context]

REQUIREMENTS (the live proposed/accepted set — reference rows by their real numeric id):
[requirements_block]

Produce one challenge per genuine issue you find. Each challenge has a `kind`, a
concrete `message`, a concrete `suggested_action`, and a `requirement_id`.

`kind` MUST be exactly one of these nine values (use no others):
- "vague" — references a control/term (e.g. CORS, an origin, a role) without naming the
  exact value, so it cannot be measured as written.
- "unquantified" — a non-functional goal stated with NO number/target (e.g. "fast",
  "secure", "scalable").
- "untestable" — a subjective quality ("user-friendly", "intuitive", "seamless", "easy
  to use") with no observable acceptance criterion.
- "solution_shaped" — names a mechanism/product/technology rather than the underlying
  need (solutioneering).
- "orphan_value" — no business outcome can be inferred; the requirement is not linked to
  value.
- "conflicting" — two requirements genuinely contradict: contradictory quantified
  targets on the same subject, mutually-exclusive constraints (e.g. on-prem vs
  cloud-only), OR a LITERAL OPPOSITE / negation (one forbids what the other requires on
  the same subject, e.g. "must purge logs after 30 days" vs "must not purge logs"), OR
  heavy semantic overlap that is actually contested. Name BOTH ids: set `requirement_id`
  to the LOWER id and `contests_id` to the OTHER (higher) id. POSE the disambiguation
  question; NEVER choose a winner. Watch for SCOPED prohibitions that are NOT a true
  conflict (e.g. "must not retain logs CONTAINING card numbers" does not conflict with
  "retain logs 90 days") — do not flag those.
- "gold_plated" — reaches for extra scope ("nice to have", "ideally", "as well as",
  "stretch goal") with no business outcome to justify it. ASK whether the extra
  capability is required; do not drop scope.
- "missing_nfr" — a SET-LEVEL gap: an entire NFR category is uncovered. Set
  `requirement_id` to null. Use ONLY these category names: security, availability,
  performance, data_residency, maintainability, scalability.
- "off_vision" — a requirement introduces a direction NOT reflected in the PROJECT
  VISION (the foreword at the top of this prompt) or the rest of the set — a possible
  unintended drift by someone who cannot see the whole picture. ADVISORY only: flag it as
  a light steer to confirm against the north star; it never blocks acceptance. Only emit
  this when a vision is present and the drift is real.

Rules:
- `requirement_id` is the real numeric id of the targeted requirement, taken from the
  list above; OR null for a set-level challenge (missing_nfr, or any genuinely set-wide
  gap).
- `message` is specific and references the real id(s) — never generic boilerplate.
- For a "conflicting" challenge ONLY, also set `contests_id` to the PARTNER requirement's
  real id (the other side of the pair). For every other kind, omit `contests_id` or set
  it null.
- `suggested_action` is concrete and actionable (what to add / restate / reconcile), and
  always leaves the verdict to the human.
- Be conservative on "conflicting" and "gold_plated": only fire on a hard signal. A false
  conflict or false gold-plating corrodes trust. Stay silent on mere ambiguity.
- Do not invent requirements that are not in the list. Do not change status.

Return ONLY a JSON object, no prose, of exactly this shape:
{
  "challenges": [
    {
      "kind": "unquantified",
      "message": "Requirement #12 states a non-functional goal with no number.",
      "suggested_action": "Add a target (e.g. p95 <= 500 ms) and the consequence of breach.",
      "requirement_id": 12
    },
    {
      "kind": "conflicting",
      "message": "Requirements #8 and #14 are direct opposites — #8 requires purging logs after 30 days; #14 forbids purging logs. Which holds, or do they apply to different scopes?",
      "suggested_action": "Reconcile the two (pick the binding rule or scope each). The agent does not choose a winner.",
      "requirement_id": 8,
      "contests_id": 14
    },
    {
      "kind": "missing_nfr",
      "message": "No requirement addresses DATA RESIDENCY.",
      "suggested_action": "Accept the suggested NFR for this category, or add your own.",
      "requirement_id": null
    }
  ]
}
```

---

## Output format

The user gets back a list of dismissible challenges. Render the merged set as a markdown
table (human-triage-friendly), and keep the raw JSON available for any tooling. Each row
is a challenge a human can **dismiss** (not a real issue / accepted as-is) or **address**
(they acted on it). The skill never sets a status — every challenge starts open.

### Template

```markdown
## Requirements red-team — <project title>

<N> challenges over <M> live requirements. Advisory only — triage each below.
The critic never picks a winner, drops scope, or changes any requirement's status.

| # | kind | targets | challenge | suggested action |
|---|------|---------|-----------|------------------|
| 1 | conflicting | #8 ↔ #14 | #8 requires purging audit logs after 30 days; #14 forbids purging audit logs. Direct opposites on the same subject. Which holds — or do they apply to different scopes? | Reconcile the two (pick the binding rule or scope each). The critic does not choose a winner. |
| 2 | unquantified | #12 | #12 ("the API should be fast") states a non-functional goal with no number. | Add a target (e.g. p95 ≤ 500 ms) and the consequence of breach. |
| 3 | solution_shaped | #21 | #21 names a mechanism (a Kafka topic) rather than the underlying need. | Restate as the need ("downstream systems must receive claim events within N s"); choose the mechanism at design time. |
| 4 | orphan_value | #21 | #21 has no linked business outcome (value_outcome is empty). | Link it to a business outcome or reconsider scope. |
| 5 | untestable | #27 | #27 uses subjective qualities ("intuitive", "easy to use") with no acceptance criterion. | Restate as an observable, testable condition (e.g. task completion in ≤ 3 clicks; SUS ≥ 80). |
| 6 | missing_nfr | (set-level) | No requirement addresses DATA RESIDENCY. | Add an NFR for data residency, or confirm it is out of scope for this project. |
```

And the machine-readable form (one object per challenge):

```json
{
  "challenges": [
    {
      "kind": "conflicting",
      "message": "Requirements #8 and #14 are direct opposites — #8 requires purging audit logs after 30 days; #14 forbids purging audit logs. Which holds, or do they apply to different scopes?",
      "suggested_action": "Reconcile the two (pick the binding rule or scope each). The agent does not choose a winner.",
      "requirement_id": 8,
      "contests_id": 14
    },
    {
      "kind": "unquantified",
      "message": "Requirement #12 states a non-functional goal with no number.",
      "suggested_action": "Add a target (e.g. p95 <= 500 ms) and the consequence of breach.",
      "requirement_id": 12
    },
    {
      "kind": "missing_nfr",
      "message": "No requirement addresses DATA RESIDENCY.",
      "suggested_action": "Add an NFR for this category, or confirm it is out of scope.",
      "requirement_id": null
    }
  ]
}
```

Field contract:
- `kind` — exactly one of the nine values.
- `message` — specific, references the real id(s), never boilerplate.
- `suggested_action` — concrete, and always leaves the verdict to the human.
- `requirement_id` — the real numeric id, or `null` for a set-level challenge.
- `contests_id` — present (the partner's id) **only** for `conflicting`; omitted/null
  otherwise. For a conflict, `requirement_id` is the LOWER id and `contests_id` the higher.

---

## Notes / anti-patterns

- **Never pick a winner.** For a `conflicting` challenge, pose "which holds, or do they
  apply to different scopes?" — do not assert which requirement is correct.
- **Never drop scope.** For `gold_plated`, *ask* whether the extra capability is
  justified by an outcome. Removing it is a human decision, taken elsewhere.
- **Never touch status.** This skill emits challenges only. It does not accept, reject,
  ratify, or advance any requirement — challenges are advisory annotations a human
  triages at their discretion.
- **Stay inside the closed vocabulary.** Only the nine kinds. If something doesn't fit a
  kind, it is probably not a challenge — resist inventing a tenth.
- **Conservatism beats coverage on `conflicting`/`gold_plated`.** A single false conflict
  teaches the human to ignore the channel. When unsure, downgrade to an advisory
  "overlap — may be duplicative or contested" note, or stay silent.
- **Respect the scoped-prohibition guard.** A prohibition qualified by *containing /
  when / unless / except / older than / raw / only / if* is scoped, not a blanket
  opposite — do not flag it as a conflict. (`examples/conflicting-vs-scoped.md`.)
- **`off_vision` needs a real vision.** If the project context is terse or absent, do not
  fire it — every NFR would look like a "new direction". Only flag genuine drift, and
  only as a light steer.
- **`missing_nfr` is the only null-target kind.** Don't attach it to a single
  requirement, and don't invent a category outside the six.
- **Idempotent re-runs.** Clear the prior *open* challenges and re-emit a fresh set;
  preserve the human's addressed/dismissed history. The same text should always produce
  the same challenges.
- **Don't invent requirements.** Only critique what is in the supplied set.
