<!-- GENERATED FILE — DO NOT EDIT.
     Built by skills/_scripts/concat_skills.py from the sources listed below.
     Edit the source skill/pattern files and re-run the concat-patterns Action.
     This file is marked linguist-generated in .gitattributes. -->

# Adversarial Review — combined pass

> Generated bundle. Built 2026-06-16 by `skills/_scripts/concat_skills.py`.

A single paste-able file for the full advisory red-team pass over a project. Run the three skills in order: challenge the requirements, surface design-review findings (a11y/WCAG, risks, gaps — findings, never verdicts), then capture the strongest objections and the dissent that should be recorded even where the project proceeds. Everything here is advisory: it produces findings and a dissent register, not gates or approvals.

## Bundled sources

- `skills/challenge/red-team-requirements/SKILL.md`
- `skills/panel/design-review-findings/SKILL.md`
- `skills/panel/red-team-and-dissent/SKILL.md`


---

## Source: `skills/challenge/red-team-requirements/SKILL.md`

<details><summary>frontmatter</summary>

```yaml
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
```

</details>

## red-team-requirements

Pressure-test a requirement set for conflicts, gaps, and gold-plating.

This pass red-teams a *set* of requirements and surfaces the things a human keeps
missing — the unquantified NFR, the solution wearing a requirement's clothes, the two
clauses that quietly contradict each other, the scope nobody asked for.

It is **advisory**. It flags issues and poses questions. It cannot make a decision: it
never picks a winner between two conflicting requirements, never deletes or rejects
scope, never sets or changes any requirement's status. A human triages every challenge.

---

### Purpose

Given a project's current requirement set, produce **one dismissible challenge per
genuine issue**, each tagged with exactly one `kind` from a **closed 9-kind taxonomy**.
A challenge names the offending requirement(s) by their `REQ-<n>` key, states the problem
concretely, and proposes an action — but the verdict is always left to the human.

What this skill does:

- Reads the live requirement set (proposed + accepted `REQ-<n>` rows; edited/rejected are
  settled history and out of scope).
- Emits challenges of exactly nine kinds — no others. See **The method** below for the
  precise definitions and `references/challenge-kinds.md` for the closed vocabulary.
- Is **conservative on `conflicting` and `gold_plated`**: precision over recall. A false
  conflict or false gold-plating corrodes trust in the channel, so these only fire on a
  hard signal and stay silent on mere ambiguity.

What this skill **never** does:

- Pick a winner between two conflicting requirements. It *poses the disambiguation
  question* and names both REQ-<n> keys.
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

### When to use

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

### Inputs

The user supplies, as markdown or pasted context:

1. **Project title** — one line.
2. **Project context / vision** — the foreword / north star. Needed for `off_vision`;
   if it is terse or absent, the vision guard simply does not fire (no false steers).
3. **The requirement set** — the live proposed/accepted rows. Each row should carry, at
   minimum:
   - a **stable `REQ-<n>` key** (challenges reference rows by this key; a bare numeric
     index may be kept internally, but the citation key is `REQ-<n>`),
   - the **requirement text**,
   - ideally a **classify** tag (functional / non-functional — this is metadata, never
     part of the key) and, if known, a **`derives_from`** (the linked `BO-<n>` business
     outcome). `derives_from` sharpens `unquantified`, `orphan_value`, and `gold_plated`
     and the conflict overlap guard — but the skill degrades gracefully without it.

A minimal input block looks like:

```
PROJECT TITLE: Claims intake modernisation
PROJECT CONTEXT / VISION: Cut manual claim triage time in half while keeping
  every decision auditable for the regulator.

REQUIREMENTS:
REQ-8   (non-functional) The system must purge audit logs after 30 days.
REQ-12  (non-functional) The API should be fast.
REQ-14  (non-functional) The system must not purge audit logs.
REQ-21  (functional)     Provide a Kafka topic for downstream consumers.   (derives_from: none)
REQ-27  (functional)     The triage screen should be intuitive and easy to use.
```

---

### The method

The skill runs a **deterministic base** (a per-requirement and pairwise checklist that
fires on hard signals) and a **model reasoning step** (a critique prompt that reads the
whole set and emits structured challenges). Use both: the deterministic base is a
backstop that guarantees the obvious issues are never missed; the model step catches the
subtle, semantic ones. When they agree, confidence is high; when only the model fires,
treat it as a softer steer.

Both layers emit the **same nine kinds and the same JSON shape**, so their outputs merge.

#### The closed nine-kind taxonomy (reproduce these definitions precisely)

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
  heavy semantic overlap that is actually contested. Name BOTH keys: set `requirement_id`
  to the LOWER `REQ-<n>` and `contests` to the OTHER (higher) `REQ-<n>`. POSE the
  disambiguation question; NEVER choose a winner. Watch for SCOPED prohibitions that are
  NOT a true conflict (e.g. "must not retain logs CONTAINING card numbers" does not
  conflict with "retain logs 90 days") — do not flag those.
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

The full closed vocabulary — with the `requirement_id` / `contests` rules per kind —
is reproduced as a reference card in `references/challenge-kinds.md`.

#### The `conflicting` rules (read these carefully — this is where trust is won or lost)

`conflicting` is the most valuable and the most dangerous kind. A *false* conflict
corrodes trust in the entire channel. Apply these rules strictly:

1. **Name BOTH keys.** Set `requirement_id` to the **LOWER** `REQ-<n>` and `contests` to
   the **OTHER (higher)** `REQ-<n>`. Sorting the pair this way makes the challenge stable
   under input reordering and gives it a stable dismissal signature. For every *other*
   kind, omit `contests` or set it null.
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

#### `missing_nfr` is set-level

`missing_nfr` is the one kind that is **not about a single requirement**. It reports that
an entire NFR **category** is uncovered by the whole set. Therefore:

- Set `requirement_id` to **null**.
- Use ONLY these six category names: `security`, `availability`, `performance`,
  `data_residency`, `maintainability`, `scalability`.
- Emit at most one challenge per uncovered category. A category is "covered" if *any*
  live requirement's text addresses it.

#### Conservatism on `conflicting` and `gold_plated`

Precision over recall. **A false conflict corrodes trust** — and so does false
gold-plating. For both kinds:

- Fire only on a specific, hard signal.
- Stay **silent on mere ambiguity**. If you are unsure whether two requirements conflict,
  do not emit a `conflicting` challenge — at most note a heavy *overlap* as advisory.
- For `gold_plated`, only fire when there is explicit discretionary language ("nice to
  have", "ideally", "would be great", "as well as", "stretch goal", "if possible", …)
  AND, for purely *additive* reach ("as well as", "also support", "additionally
  support"), only when there is **no** captured `derives_from` outcome to back the extra
  scope. A well-grounded broad requirement stays silent.

#### Step by step

**Step 1 — Scope the live set.** Take only requirements whose status is `proposed` or
`accepted`. Ignore edited/rejected rows. This is the set the critic reasons over for
every kind.

**Step 2 — Deterministic per-requirement pass (backstop).** For each live requirement,
walk the checklist and emit a challenge when a rule fires:
- `unquantified` — classified non-functional and the text states a goal with no number/target.
- `solution_shaped` — the text names a mechanism/product/technology instead of the need.
- `orphan_value` — no business outcome can be inferred (`derives_from` empty).
- `vague` — references a control/term (e.g. CORS) without naming the exact value (e.g.
  CORS mentioned but no origin/method named).
- `untestable` — contains a subjective quality ("user-friendly", "intuitive", "easy to
  use", "seamless") with no acceptance criterion.

**Step 3 — Deterministic pairwise pass (backstop, conservative).** Over ordered-unique
pairs of live requirements, apply the `conflicting` triggers above with the shared-subject
gate and the scoped-prohibition guard. Emit one `conflicting` challenge per genuinely
conflicting pair, naming both keys (lower = `requirement_id`, higher = `contests`).

**Step 4 — Deterministic gold-plating pass (backstop, conservative).** For each live
requirement with discretionary language, emit a `gold_plated` challenge that asks whether
the extra scope is justified by the `derives_from` outcome. Apply the additive-language
guard.

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

#### The model step — the critique prompt

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

REQUIREMENTS (the live proposed/accepted set — reference rows by their real REQ-<n> key):
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
  heavy semantic overlap that is actually contested. Name BOTH keys: set `requirement_id`
  to the LOWER REQ-<n> and `contests` to the OTHER (higher) REQ-<n>. POSE the
  disambiguation question; NEVER choose a winner. Watch for SCOPED prohibitions that are
  NOT a true conflict (e.g. "must not retain logs CONTAINING card numbers" does not
  conflict with "retain logs 90 days") — do not flag those.
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
- `requirement_id` is the real REQ-<n> key of the targeted requirement, taken from the
  list above; OR null for a set-level challenge (missing_nfr, or any genuinely set-wide
  gap).
- `message` is specific and references the real REQ-<n> key(s) — never generic boilerplate.
- For a "conflicting" challenge ONLY, also set `contests` to the PARTNER requirement's
  REQ-<n> key (the other side of the pair). For every other kind, omit `contests` or set
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
      "message": "Requirement REQ-12 states a non-functional goal with no number.",
      "suggested_action": "Add a target (e.g. p95 <= 500 ms) and the consequence of breach.",
      "requirement_id": "REQ-12"
    },
    {
      "kind": "conflicting",
      "message": "Requirements REQ-8 and REQ-14 are direct opposites — REQ-8 requires purging logs after 30 days; REQ-14 forbids purging logs. Which holds, or do they apply to different scopes?",
      "suggested_action": "Reconcile the two (pick the binding rule or scope each). The agent does not choose a winner.",
      "requirement_id": "REQ-8",
      "contests": "REQ-14"
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

### Output format

The user gets back a list of dismissible challenges. Render the merged set as a markdown
table (human-triage-friendly), and keep the raw JSON available for any tooling. Each row
is a challenge a human can **dismiss** (not a real issue / accepted as-is) or **address**
(they acted on it). The skill never sets a status — every challenge starts open.

#### Template

```markdown
## Requirements red-team — <project title>

<N> challenges over <M> live requirements. Advisory only — triage each below.
The critic never picks a winner, drops scope, or changes any requirement's status.

| # | kind | targets | challenge | suggested action |
|---|------|---------|-----------|------------------|
| 1 | conflicting | REQ-8 ↔ REQ-14 | REQ-8 requires purging audit logs after 30 days; REQ-14 forbids purging audit logs. Direct opposites on the same subject. Which holds — or do they apply to different scopes? | Reconcile the two (pick the binding rule or scope each). The critic does not choose a winner. |
| 2 | unquantified | REQ-12 | REQ-12 ("the API should be fast") states a non-functional goal with no number. | Add a target (e.g. p95 ≤ 500 ms) and the consequence of breach. |
| 3 | solution_shaped | REQ-21 | REQ-21 names a mechanism (a Kafka topic) rather than the underlying need. | Restate as the need ("downstream systems must receive claim events within N s"); choose the mechanism at design time. |
| 4 | orphan_value | REQ-21 | REQ-21 has no linked business outcome (derives_from is empty). | Link it to a business outcome or reconsider scope. |
| 5 | untestable | REQ-27 | REQ-27 uses subjective qualities ("intuitive", "easy to use") with no acceptance criterion. | Restate as an observable, testable condition (e.g. task completion in ≤ 3 clicks; SUS ≥ 80). |
| 6 | missing_nfr | (set-level) | No requirement addresses DATA RESIDENCY. | Add an NFR for data residency, or confirm it is out of scope for this project. |
```

And the machine-readable form (one object per challenge):

```json
{
  "challenges": [
    {
      "kind": "conflicting",
      "message": "Requirements REQ-8 and REQ-14 are direct opposites — REQ-8 requires purging audit logs after 30 days; REQ-14 forbids purging audit logs. Which holds, or do they apply to different scopes?",
      "suggested_action": "Reconcile the two (pick the binding rule or scope each). The agent does not choose a winner.",
      "requirement_id": "REQ-8",
      "contests": "REQ-14"
    },
    {
      "kind": "unquantified",
      "message": "Requirement REQ-12 states a non-functional goal with no number.",
      "suggested_action": "Add a target (e.g. p95 <= 500 ms) and the consequence of breach.",
      "requirement_id": "REQ-12"
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
- `message` — specific, references the real REQ-<n> key(s), never boilerplate.
- `suggested_action` — concrete, and always leaves the verdict to the human.
- `requirement_id` — the real REQ-<n> key, or `null` for a set-level challenge.
- `contests` — present (the partner's REQ-<n> key) **only** for `conflicting`; omitted/null
  otherwise. For a conflict, `requirement_id` is the LOWER REQ-<n> and `contests` the higher.

---

### Notes / anti-patterns

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


---

## Source: `skills/panel/design-review-findings/SKILL.md`

<details><summary>frontmatter</summary>

```yaml
name: design-review-findings
description: Read a design or solution-architecture draft (or a running front-end) and emit severity-tagged, citation-bearing FINDINGS over a built-in architecture checklist. Clamp out-of-set severity to info, default a missing ref, drop empty findings. Never approves or rejects — findings, not verdicts. Use when reviewing a design draft for concrete, actionable observations a panel would raise.
one_liner: Emit severity-tagged, cited findings over a design draft.
when_to_use: reviewing a design draft or a running front-end for concrete actionable findings
aliases: [design review, architecture review, design critique, solution review, gap analysis, design feedback, review checklist, security review checklist]
output_kinds: [proposal, question]
deterministic_fallback: the architecture checklist + the severity-clamp / default-ref / drop-empty harness
suggested_tier: frontier
neighbours:
  before: panel/red-team-and-dissent — adversarial pressure-test that records dissent
  after: panel/frontend-a11y-review — the same engine with a WCAG checklist for front-ends
references:
  - references/architecture-checklist.md
```

</details>

## design-review-findings

### Purpose

Read a design draft — a solution-architecture document, a section bundle, or a
running front-end — and emit **concrete, actionable FINDINGS**: observations a
reviewer (or a governance panel) would raise, each tagged with a severity and a
citation to the exact thing it attaches to.

This skill is a **reviewer, not a judge**. It stays inside the material it was
given. It does not invent scope the text does not imply, it does not approve or
reject the design, and it produces no verdict. A human decides what to do with
the findings. The skill's only job is to surface them clearly, with enough
specificity that a reader can act on each one.

This is the **general review engine**. The companion skill `frontend-a11y-review`
is a *specialisation* of this same engine: it carries a WCAG success-criteria
checklist instead of the architecture checklist, and cites WCAG SCs in `ref`.
Everything else — the finding shape, the severity set, the validation harness —
is shared. A change to the contract here is a change there too.

### When to use

- A solution-architecture draft has been synthesised and a pass over it is
  wanted before it goes to a panel or to the author for revision.
- A front-end is running and a structured list of design concerns is wanted
  (for the a11y-specific variant, prefer `frontend-a11y-review`).
- Any time someone asks "what would a reviewer flag in this?" and wants a list
  they can triage, not a yes/no.

There is no pass/fail here, and nothing this skill emits blocks an advance. If a
process needs a decision, that is a human's call downstream of these findings.

### Inputs

The user supplies, as markdown / context:

- **The design material** — the draft document, the section bundle, or a
  description of the running front-end. This is the substance to review.
- **Project context** (optional but recommended) — title and a short
  description, so findings stay anchored to what the project is actually for.
- **Attached NFRs / adopted patterns** (optional) — so a finding can cite a
  specific NFR (`NFR-availability`) or pattern (`pattern:containerised-web`)
  rather than a vague "the design".

If the material is empty, there is nothing to review — say so and stop. Do not
manufacture findings from nothing.

> **Multi-agent option (advisory).** This step deepens with independent parallel
> agents: launch one sub-agent per candidate finding area (or per design
> section), at most 4 at a time, each a separate sub-agent. A failed sub-agent
> returns nothing and is never fatal — the deterministic base stands; merge what
> succeeded. (Claude Code: use the Task tool / subagents. Other tools: launch
> parallel model calls; or a matrix-strategy CI job.) Never required — it adds
> coverage and cuts single-pass bias. See `skills/_contract/parallel-agents`.

### The method (numbered STEPS)

The engine has a **deterministic base** (steps 1, 3, 4) and a **model reasoning
step** (step 2). The base is what makes the output trustworthy even when the
model is weak or unavailable; the model step is what makes it insightful.

#### Step 1 — DETERMINISTIC: walk the architecture checklist

Before any open-ended reasoning, walk the built-in architecture checklist
(see `references/architecture-checklist.md`) against the draft. For each item,
ask: *does the draft state this, and is what it states adequate?* The checklist
is the floor — these are the things a managed-services governance panel will ask
about every single time, so a draft that is silent on one of them has a gap
worth a finding:

- **RPO / RTO** — recovery point and recovery time objectives. Is data-loss
  tolerance and recovery time stated, or unstated?
- **Encryption at rest** — is the at-rest posture for stored data declared?
- **RBAC between tiers** — is access control *between* the tiers (web → app →
  data) specified, not just at the edge?
- **Deployment topology / availability model** — how is it deployed, across how
  many zones/regions, with what availability target?
- **Secret rotation** — are credentials/keys rotated, and how?
- **Unclassified integrations** — are there integration points whose
  data-sensitivity, auth, or ownership is left unclassified?

A silent checklist item is typically a `medium` (or `high` if the project
context makes it load-bearing). A present-but-vague item is a `low` or `medium`.
A present-and-adequate item needs no finding (or an `info` note for
traceability).

#### Step 2 — MODEL: review for everything the checklist does not catch

Now reason openly over the draft for gaps, risks, unstated assumptions, and
missing specifications **beyond** the fixed checklist — the things specific to
*this* design. Use the review prompt below. Stay within the material; cite the
thing each finding attaches to. This is where the engine earns its keep: the
checklist catches the universal omissions, this step catches the
design-specific ones.

> **REVIEW PROMPT** (carry this to the model verbatim; fill the `${...}` slots):
>
> Review the design draft below as a design reviewer on a managed-services
> delivery team and produce FINDINGS — observations with a citation — NOT
> verdicts. Do not approve or reject the design; a human decides what to do with
> the findings.
>
> PROJECT: `${title}`
>
> DESCRIPTION / CONTEXT:
> `${description}`
>
> DESIGN DRAFT:
> `${design_content}`
>
> Identify gaps, risks, unstated assumptions, and missing specifications in THIS
> draft — things a governance panel would query (e.g. an unstated RPO/RTO,
> encryption-at-rest posture, RBAC between tiers, deployment-topology /
> availability model, secret rotation, unclassified integrations). Stay within
> the material in the draft and the project context; do not invent scope the
> text does not imply. Each finding must be a concrete observation a reader can
> act on, with a citation in `ref`.
>
> Assign each finding a severity from EXACTLY this set: `high`, `medium`, `low`,
> `info`. (`info` = a neutral note for traceability, not a problem.) Set `ref`
> to the thing the finding cites — for example an attached NFR
> (`NFR-availability`, `NFR-security`), a pattern (`pattern:containerised-web`),
> a design section (`design-section:integrations`), a comparator
> (`comparator:partner-integration-hub`), or a WCAG success criterion
> (`wcag:1.4.3`) when reviewing a front-end.
>
> Return ONLY a JSON object of exactly this shape, no prose, no markdown fence:
>
> ```json
> {
>   "findings": [
>     {"severity": "high", "text": "The observation and why it matters.", "ref": "NFR-availability"}
>   ]
> }
> ```

#### Step 3 — DETERMINISTIC: run the validation harness

Pass every finding from steps 1 and 2 through this harness. These three rules
are the trust boundary — apply them *verbatim*, they are non-negotiable. A model
will occasionally hand back a severity outside the set, a finding with no
citation, or an empty string; the harness makes the output safe regardless.

1. **Clamp out-of-set severity to `info`.** The allowed set is exactly
   `{high, medium, low, info}`. Any other value (e.g. `critical`, `warning`,
   `P1`, empty) becomes `info`. Lowercase and trim first.
2. **Default a missing `ref`.** If a finding has no citation (empty or absent
   `ref`), set it to `design`. A finding must always cite *something*; `design`
   is the catch-all that means "the draft as a whole".
3. **Drop empty-text findings.** Trim the text; if it is empty, discard the
   finding entirely. A finding with nothing to say is not a finding.

Reference implementation of the harness:

```python
ALLOWED = {"high", "medium", "low", "info"}

def normalise(findings):
    out = []
    for it in findings:
        if not isinstance(it, dict):
            continue
        text = str(it.get("text") or "").strip()
        if not text:                          # rule 3: drop empty-text
            continue
        severity = str(it.get("severity") or "").strip().lower()
        if severity not in ALLOWED:           # rule 1: clamp out-of-set → info
            severity = "info"
        ref = str(it.get("ref") or "").strip() or "design"   # rule 2: default ref
        out.append({"severity": severity, "text": text, "ref": ref})
    return out
```

#### Step 4 — DETERMINISTIC: order and emit

Sort the surviving findings `high → medium → low → info` (most material first),
then render them in the output format below. If after the harness there are zero
findings, say so plainly — "no findings; the draft is clear on the checklist and
the material reviewed" — rather than inventing filler.

#### Deterministic fallback

If the model step (step 2) is unavailable or returns nothing usable, the skill
still produces value: emit findings from the architecture checklist alone
(step 1), run them through the harness (step 3), and order/emit (step 4). The
checklist plus the harness *is* the floor of this skill — it never returns
nothing useful just because the model was unavailable.

### Output format

Return a markdown block the user can triage. Each finding is one row: a severity
tag, the citation it attaches to, and the observation. Findings only — no
verdict line, no "APPROVED / REJECTED".

```markdown
## Design review findings — <project title>

_6 findings (1 high, 2 medium, 2 low, 1 info). Findings, not a verdict —
no approval or rejection is implied._

| Severity | Ref | Finding |
|----------|-----|---------|
| **high** | `NFR-availability` | The draft states a 99.9% uptime target but no RPO/RTO. With a single-region topology (design-section:deployment) that target is not credibly recoverable — name a recovery point and recovery time, or relax the SLA. |
| **medium** | `design-section:data` | No encryption-at-rest posture is declared for the primary datastore. A managed-services panel will ask; state the at-rest control and key custody. |
| **medium** | `design-section:integrations` | The partner feed integration is unclassified — its data sensitivity, auth mechanism, and ownership are not stated. Classify it before it reaches a panel. |
| **low** | `pattern:containerised-web` | RBAC between the web and app tiers is implied by the adopted pattern but not spelled out in this draft. Make the tier-to-tier access model explicit. |
| **low** | `design-section:operations` | Secret rotation is not mentioned. State whether credentials/keys rotate and on what cadence. |
| **info** | `comparator:partner-integration-hub` | The chosen topology mirrors the partner-integration-hub comparator; noting for traceability — no action implied. |
```

Keep each finding self-contained: *what* is missing or risky, *where* it
attaches (the `ref`), and *why it matters* / what to do. A reader should be able
to act on a single row without reading the others.

### Notes / anti-patterns

- **Findings, not verdicts.** This is the whole posture. The moment you write
  "this design is approved", "ready to ship", or "fails review", you have left
  the skill's lane. Surface concerns; let a human decide.
- **Stay in the material.** Do not invent requirements, scope, or
  infrastructure the draft does not imply. A finding about something that isn't
  in the draft and isn't on the checklist is noise. The checklist is the only
  licence to flag an *absence*; everything else must be grounded in text that
  is present.
- **Always cite.** Every finding carries a `ref`. "The design is weak" with no
  citation is useless and will be defaulted to `design` by the harness anyway —
  do better and name the section, NFR, pattern, comparator, or WCAG SC.
- **`info` is not a problem.** Use it for neutral traceability notes (a
  comparator match, a deliberate trade-off worth recording). Do not inflate an
  `info` into a `low` to pad the list, and do not bury a real `high` as `info`.
- **The harness is not optional.** Even when the model is trusted, run step 3.
  It is cheap, it is deterministic, and it is what lets a downstream consumer
  trust the severity field and the ref field without re-validating.
- **Don't pad.** Zero findings is a legitimate, valuable result. An empty draft
  is "nothing to review", not "let me find six things".
- **This is the engine; specialise by swapping the checklist.** Front-end /
  WCAG review is the same engine with a WCAG checklist and `wcag:` refs — reach
  for `frontend-a11y-review` there rather than re-deriving the contract.


---

## Source: `skills/panel/red-team-and-dissent/SKILL.md`

<details><summary>frontmatter</summary>

```yaml
name: red-team-and-dissent
description: From one or N persona lenses raise the single strongest objection to each emerging proposal (never a verdict, never kills it); a declined objection becomes a durable dissent record feeding dismissal-memory.
one_liner: Raise the strongest objection per proposal; record declined ones as durable dissent.
aliases:
  - devils advocate
  - play devil's advocate
  - poke holes
  - challenge a proposal
  - decision log of what was rejected
  - record why a proposal was declined
  - dissent register
  - objection log
when_to_use: adversarially stress-testing a proposal, or recording what was decided NOT to do and why
output_kinds: [question, proposal]
deterministic_fallback: the single-objection template + the dissent register template
suggested_tier: frontier
tier_reason: adversarial judgement plus a durable human-facing dissent record is high-stakes.
neighbours:
  before: panel/synthesise-panel — supplies the proposals a synthesised review surfaces
  after: panel/design-review-findings — turns surviving proposals into concrete findings
compose_with:
  - skills/_contract/parallel-agents   # fan one lens out over N
references:
  - references/dissent-register.template.md
```

</details>

## Red-team and Preserve-Dissent

Raise the single strongest objection to each emerging proposal, then turn any objection a human declines into a durable record of what was decided **not** to do, and why.

This skill does two jobs that belong together:

1. **Red-team** — from a named persona lens, raise the **one** thing most likely to
   make an emerging proposal the wrong call. Hard-hitting, specific, grounded — but
   it **never** delivers a verdict and **never** kills the proposal.
2. **Preserve-dissent** — when a human *declines* an objection (keeps the proposal),
   the objection doesn't evaporate. It becomes a durable **dissent record**: a titled
   "what was decided NOT to do, and why" with a human-owned reason and provenance back
   to the objection. The register is revisitable and feeds **dismissal-memory** so the
   same idea is not silently re-proposed later.

The call **always** stays with the human. The agent surfaces; the human disposes.

> **Multi-agent option (advisory).** This step deepens with independent parallel
> agents: launch one sub-agent per objection lens, at most 4 at a time, each a
> separate sub-agent. A failed sub-agent returns nothing and is never fatal — the
> deterministic base stands; merge what succeeded. (Claude Code: use the Task tool /
> subagents. Other tools: launch parallel model calls; or a matrix-strategy CI job.)
> Never required — it adds coverage and cuts single-pass bias. See
> `skills/_contract/parallel-agents`.

---

### Purpose

A panel or a fan-out generates *proposals* — a requirement, a decision, a roadblock, a
gap to close, a shape of the solution. Most of them are fine. A few are quietly wrong:
they over-reach, under-deliver, or carry a hidden risk that nobody named out loud.

The red-team's job is to name that risk **once, at full strength**, per proposal — and
then get out of the way. It does not have a kill switch. It produces exactly one
artefact per proposal: the strongest single objection, framed so a human can decide in
seconds whether to **keep** the proposal or **record a dissent**.

When the human keeps the proposal *over* an objection, that objection is the most
valuable thing in the room — the "this was considered and the other way was chosen"
that a future reader will want. So it is captured.

---

### When to use

- There are one or more **emerging proposals** (from a panel, a fan-out, a brainstorm,
  or a design pass) and they need stress-testing before they harden.
- The project is about to record **what was decided NOT to do** and the durable WHY,
  so it can be cited and is not re-litigated by accident.
- **Dismissal-memory** is wanted: a future proposal that matches a recorded dissent
  should surface that prior decision instead of arriving fresh.

Do **not** use this skill to *approve* anything. It has no "pass". A clean red-team
pass means "no strong objection surfaced" — not "this is blessed".

---

### Inputs (what you supply)

| Input | Required | Shape |
|---|---|---|
| `proposal(s)` | yes | Free-text or markdown. One proposal, or a list. Each carries: a one-line statement + enough grounding (facts, source) to object against. |
| `proposal_kind` | per proposal | One of `requirement \| decision \| roadblock \| gap \| solution-shape \| feature`. Drives the objection framing. |
| `lens(es)` | optional | One persona kind, or N. Defaults to `skeptic` then `minimalist`, alternating (see below). |
| `grounding` | recommended | The facts the objection must keep — the proposal's source, prior context, any objection-so-far to *deepen*. |

No database, panel, or session state is needed. A proposal pasted into a prompt is
enough.

#### The persona lenses

Each lens is a deliberate slant. Pick the one whose domain the proposal sits in, or
alternate the two default adversarial voices across a batch.

| Lens | Slant | Objects when… |
|---|---|---|
| `skeptic` | Red-teams the requirements | conflicting / unquantified / untestable / vague claims; unresolved tensions |
| `minimalist` | Argues for less | scope reaches beyond the captured outcome (gold-plating / over-reach) |
| `pragmatic_engineer` | Argues buildability | no acceptance criteria, missing NFR coverage, open roadblocks |
| `solution_designer` | Argues the shape | a pattern was overridden without a holding reason; a section is thin/stale |
| `explorer` | Argues for wider | orphaned value or an unexplored domain the proposal walks past |

The two **default adversarial voices** are `skeptic` and `minimalist` — alternate them
across a batch of proposals so the same objection is not heard in the same voice twice
in a row. The others are available when the proposal is clearly in their domain.

---

### The method

#### Step 1 — DETERMINISTIC: identify the emerging proposals (no model)

Walk the input and pick out only the things that are genuinely **proposals**. A
statement that merely *concurs* or *objects-to-something-else* is not an emerging
proposal — skip it. The four signal shapes that ARE proposals (and the kind each maps
to) are:

| The proposal is a… | …if it | objection kind |
|---|---|---|
| `gap` | flags a missing thing to close | `gap` |
| `requirement` | proposes adding a requirement / carrying value | `requirement` |
| `decision` | proposes an alternative to weigh | `decision` |
| `roadblock` | raises a risk that constrains the build | `roadblock` |

If there are **zero** proposals, stop and say so. The honest empty case is a result,
not a gap — do **not** invent an objection to have something to say.

Assign each surviving proposal a stable `proposal_ref` (`gap-0`, `req-0`, `decision-0`,
`roadblock-0`, …) and alternate the lens across the batch (`skeptic`, `minimalist`,
`skeptic`, …). This is fully deterministic — no model needed to get this far.

#### Step 2 — LLM: raise the single strongest objection per proposal

For each proposal, run the red-team prompt below from its assigned lens:

> You are the RED TEAM on a design deliberation, speaking from the **{persona_kind}**
> lens. Raise the single STRONGEST objection to the EMERGING proposal below — the one
> thing most likely to make it the wrong call. Be specific and hard-hitting. But you
> NEVER deliver a verdict and you NEVER kill the proposal: you surface the objection so
> a human can decide whether to keep the proposal or record it as a dissent (what was
> decided NOT to do, and why).
>
> **PROPOSAL KIND:** {proposal_kind}
>
> **THE EMERGING PROPOSAL + the objection so far** (deepen this — keep its facts):
> {grounding}
>
> Return ONLY a JSON object of exactly this shape, no prose, no fence:
> ```json
> {
>   "stance_summary": "one sharp sentence — your strongest single objection",
>   "body_md": "2-4 sentences making the objection concrete and grounded, ending by leaving the call to the human"
> }
> ```

Rules that make this a red-team and not a reviewer:

- **One** objection per proposal. Not three. The strongest single one.
- **Keep the proposal's facts.** This is deepening an objection, not re-describing the
  proposal or arguing a different point.
- **End by leaving the call to the human.** The last sentence of `body_md` hands the
  decision back: keep it, or record a dissent. No "therefore we should not…".
- **No verdict, no score, no kill.** "Wrong call" is a hypothesis being surfaced, not a
  ruling being issued.

#### Step 3 — Composable: one lens, or fan out over N

- **One lens:** run Step 2 once, with the assigned persona. Done.
- **N lenses (no panel machinery):** to hear several voices on the *same* proposal, run
  Step 2 once per lens and collect the objections. Issue the calls in parallel — one
  model call per (proposal × lens) — then gather, following the convention in
  `skills/_contract/parallel-agents`. No convened panel, roster, or session state is
  needed; the fan-out is just N independent red-team prompts.

Deduplicate honestly: if two lenses raise effectively the same objection, keep the
sharper wording and note both lenses agreed — don't pad the list to look thorough.

#### Step 4 — Human disposes: keep, or record a dissent (DETERMINISTIC)

Present each objection to the human with exactly two dispositions:

- **Keep the proposal** (objection acknowledged, proposal stands) → if the human keeps
  it *over* a real objection, offer to **record a dissent** capturing the objection so
  the decision is durable.
- **Record a dissent** (the project will NOT do this) → write a dissent record (Step 5).

Either way the human owns the outcome. The agent never auto-disposes.

#### Step 5 — DETERMINISTIC: a declined objection becomes a durable dissent record

When the human declines a proposal (or keeps one but wants the objection on record),
materialise a **dissent record** using `references/dissent-register.template.md`. The
shape is:

```yaml
title:        # one line — what was decided NOT to do
kind:         # feature | requirement | solution | proposal | other
source:       # agent  -> recorded from a red-team objection (provenance below)
              # human  -> a standalone dissent a human added directly
reason:       # the durable WHY — HUMAN-OWNED, editable, the human owns every word
status:       # recorded  (default) | revisited  (re-opened for reconsideration)
provenance:   # only when source=agent
  objection_summary:  # the stance_summary that triggered this
  objection_lens:     # which persona raised it
  proposal_ref:       # the ref from Step 1 (decision-0, req-0, …)
recorded_on:  # ISO date
```

Then append the record to the project's **dissent register** (one markdown file or a
GitHub Issue using the dissent-record issue template — see Notes). Two properties make
the register trustworthy:

- **The human owns the WHY.** The `reason` (and `title`) are editable forever. The
  *provenance* — which objection, which lens, which proposal — is **immutable** once
  recorded. Snapshot semantics: editing the reason never reaches back and mutates the
  original objection.
- **Never write-only.** A record can be **revisited** — flip `status: recorded →
  revisited` to re-open a declined item for reconsideration. The record, its WHY, and
  its discussion thread are **preserved** across the flip. Decision history is kept,
  not erased.

#### Step 6 — dismissal-memory: don't silently re-propose a dissent

Before a *new* proposal is surfaced, check it against the dissent register. If it
matches a `recorded` dissent (same idea, same kind), do **not** present it fresh —
surface the prior dissent instead:

> ⤺ This looks like **{dissent.title}**, which was recorded as a dissent on
> {recorded_on} because: *{reason}*. Re-open it (set status → revisited) to
> reconsider, or leave it.

This is the whole point of preserving dissent: the project stops re-litigating settled
"no"s by accident, while keeping the door open to deliberately re-open any of them.

---

### Output format

Two markdown artefacts are returned.

#### A. The objection(s) — one block per proposal

```markdown
### Red-team objection — `decision-0` (solution-shape)
**Lens:** solution_designer · **Disposition:** ⬚ keep proposal ⬚ record dissent

**Strongest objection:** Putting the rules engine behind the same sync HTTP path as
reads makes a 200ms rule evaluation a tail-latency tax on every page load.

The proposal reuses the existing request handler for rule evaluation, but rules fan
out to 3–5 downstream lookups; under the captured p95 target that path is already at
budget, so co-locating evaluation there spends the headroom the NFR set reserves for
reads. An async/queued evaluation keeps the read path clean at real cost to rule
freshness. Whether that trade is acceptable is the call to make here, not mine.
```

> Note: `body_md` is 2–4 sentences and its **last sentence hands the call back to the
> human**. There is no recommendation line, no score, no "verdict".

When N lenses are fanned out on one proposal, list the objections under the same
proposal header, sharpest first, with the agreeing lenses noted.

#### B. A recorded dissent — from `references/dissent-register.template.md`

```markdown
## Dissent: Do not co-locate rule evaluation on the read path

- **kind:** solution
- **source:** agent
- **status:** recorded
- **recorded_on:** 2026-06-15

**Why (human-owned):**
The read-path latency cost is accepted for v1 to ship the rules feature without
standing up a queue. Revisit if p95 regresses past the NFR target in staging.

**Provenance (immutable):**
- objection_lens: solution_designer
- proposal_ref: decision-0
- objection_summary: "rule evaluation on the read path spends the read-latency headroom"
```

---

### Notes / anti-patterns

- **No verdict, ever.** If the output contains "we should not", "rejected", "blocked",
  a score, or a pass/fail — it has stopped red-teaming. The strongest objection is a
  *hypothesis about why this could be wrong*, handed to a human. That's the whole
  contract.
- **One objection, full strength.** A list of five mild concerns is weaker than one
  sharp one. If there genuinely are two strong, *distinct* objections, that's a signal
  the proposal is two proposals — say so rather than diluting.
- **Keep the proposal's facts.** Deepen the objection; don't re-litigate a different
  point or restate the proposal back. The "objection so far" is given to *sharpen*, not
  replace.
- **The honest empty case is a result.** Zero proposals → zero objections. A lens with
  no real signal says "no strong objection from this lens" and proposes nothing. Never
  manufacture an objection to look diligent.
- **The human owns the WHY; the agent owns the provenance.** When recording a dissent,
  the reason/title are the human's words (editable forever); the link back to the
  objection, lens, and proposal_ref is immutable. Don't let an edit silently rewrite
  what was originally objected to.
- **The register is never write-only.** Always offer *revisit* — a recorded "no" must
  be re-openable. Preserving dissent is about keeping the decision *and the ability to
  change it*, not freezing it.
- **Check dismissal-memory before surfacing.** A new proposal that matches a recorded
  dissent should arrive *with* its prior dissent attached, not fresh. Silently
  re-proposing a settled "no" is the failure this skill exists to prevent.
- **Light and advisory.** This skill enforces nothing. It produces objections and
  records; disposition, ordering, and re-opening are all human moves. There is no
  approval to grant.

#### GitHub-native mechanics (optional)

- **Dissent register as Issues:** use a **dissent-record issue template** so each
  recorded dissent is a GitHub Issue. `source`/`kind`/`status` become labels
  (`status:recorded`, `status:revisited`); the immutable provenance goes in a fenced
  block in the issue body; the human-owned WHY is the editable description; discussion
  threads naturally as issue comments. "Revisit" = re-open the issue (or flip the
  status label).
- **Dismissal-memory as a check:** a lightweight Action on PRs/issues can grep new
  proposal text against open `status:recorded` dissent issues and post an advisory
  comment ("this resembles dissent #123") — advisory only, never a required check.
