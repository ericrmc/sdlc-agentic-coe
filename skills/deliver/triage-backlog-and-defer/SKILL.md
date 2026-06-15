---
name: triage-backlog-and-defer
description: Turn a raw backlog into structured traced sized prioritised items — park each with the outcome it would serve (null = scope flag), an honest comparator-grounded size, a priority (traced->higher, untraced->low); promote = an 'add' release delta carrying the same trace; decline is remembered against unchanged evidence.
one_liner: Park a raw backlog as traced, sized, prioritised items.
aliases: [backlog triage, defer features, park a request, scope creep check, size a backlog, prioritise backlog, won't-do list, future work parking]
when_to_use: triaging a raw backlog into parked items with honest sizing and traceability
output_kinds: [proposal, menu]
deterministic_fallback: the park/size/prioritise table + the promote->add-delta rule
suggested_tier: mid
neighbours:
  before: deliver/help-implement-a-wave
  after: deliver/scope-reconcile-check
---

# Triage Backlog and Defer

Backlog triage with memory. Turn a raw, messy backlog into structured **parked items** — each carrying the business outcome it would serve, an honest size, and a priority — while preserving the **why-not** for everything you decline so it is never re-litigated against the same evidence.

This skill is light and advisory. It produces **suggestions and menus**, never verdicts or status changes. A human owns every disposition: which items get parked, which get promoted into delivery, and which get declined. You propose; the human decides.

## Purpose

A raw backlog is a pile of half-formed asks: "dark mode", "bulk re-assign approvals", "faster export", "SSO maybe". Most of it will never be built, some of it is gold, and almost none of it is honestly sized or traced to anything the business actually agreed to deliver.

Triage turns that pile into three honest signals per item:

1. **What outcome does it serve?** — the trace edge. If an item serves one of the agreed business outcomes, say which one (verbatim key). If it serves *none*, that is not a failure of analysis — it is a finding. An untraced item is a **scope-creep flag**, and an honest `null` is better than a forced trace.
2. **How big is it, really?** — an honest size in person-days, grounded in what comparable past work actually cost. A single backlog feature is a *small fraction* of a whole-project effort. Do not let "small" become "free".
3. **How much does it matter?** — a priority that *falls out of* the trace, not out of enthusiasm. Traced items carry more priority; untraced flags carry less. Stay honest; do not inflate.

And critically: triage **remembers**. When a human declines an item, that decision is durable. The item is never re-proposed against unchanged evidence — the why-not is preserved: a record of what was decided *not* to do, and why.

## When to use

- You have a raw backlog (a list, a doc, a wall of stickies, a stakeholder wishlist) and need to turn it into structured, traceable, sized items.
- You want to know which asks are real (trace to an agreed outcome) and which are scope creep (trace to nothing).
- You need honest sizing for planning, grounded in past actuals rather than optimism.
- Later: you want to **promote** a parked item into an actual release/delivery wave, carrying its trace forward — or **decline** it durably so it stops coming back.

Use it *after* business outcomes are agreed (you need outcomes to trace against) and *alongside* release planning (promotion hands off into a release).

## Inputs

The user supplies, as markdown or pasted context:

1. **Candidate backlog items** — the raw list. One per line or bullet is fine; a title plus an optional sentence of description each is ideal.
2. **Accepted outcomes** — the agreed business outcomes, each with a stable key (e.g. `BO-3`, `BO-1`). These are the **only** things an item may trace to. May be sparse; that is normal and expected — a sparse outcome set means more honest nulls.
3. **Effort reference** *(optional but strongly preferred)* — comparable past projects whose *actual* effort is known, so you can size honestly. May be sparse. With no reference at all, sizes are `null` (unsizable), not guessed.
4. **Decline memory** *(optional)* — items already declined, with the evidence they were declined against. Used so you do not re-propose them.

If outcomes are missing, ask for them — without an agreed outcome set, *every* trace is a guess and every item looks like scope creep. If the effort reference is missing, proceed but mark sizes as unsizable (`null`) rather than inventing numbers.

## The method (steps)

The method has a **deterministic base** (a mechanical table anyone can reproduce) and an **LLM reasoning step** (judgement the table cannot do). Run the base first; use the LLM step to refine trace and rationale.

### Step 1 — DETERMINISTIC: build the park/size/prioritise table

For each candidate, fill one row using these mechanical rules. No judgement yet — this is the reproducible floor.

| Field | Mechanical rule |
|---|---|
| **title** | A concise restatement of the candidate item. |
| **derives_from** | Tokenise the item title and each outcome's text (drop stop-words and filler verbs like *add/change/remove/new/feature/support*). Pick the outcome with the **most shared meaningful tokens**. Require **at least two** shared tokens to claim a trace — otherwise `null`. A `null` here is a **scope-creep flag**, not an error. |
| **est_effort_days** | Take the mean *actual* effort of the confirmed comparators and scale it down — a single deferred feature is roughly **~20%** (`× 0.2`) of a whole comparable build. Round to one decimal. If there are **no** comparators, this is `null` (unsizable). |
| **suggested_priority** | Falls straight out of the trace: **traced → `medium`** (a real ask deserves a default of medium, to be lifted by the LLM step only with a reason); **untraced → `low`** (a flag, parked but not chased). Never `high` from the table alone — high is a judgement the LLM step must justify. |
| **rationale** | Templated: traced → *"Traces to outcome {key}; sized from comparators (~20% of comparable build)."* untraced → *"No accepted outcome behind it — parked as a low-priority flag."* |

This table is the **deterministic fallback**: if no LLM is available, ship it as-is. It is honest, traceable, and reproducible.

### Step 2 — LLM: triage and refine

Now apply judgement the token-overlap table cannot. Run the triage prompt (below) over the candidates, outcomes, and effort reference. The LLM may:

- **Correct a trace** the token-match got wrong (a real semantic link the words missed, or a spurious overlap that is not a genuine link). When in doubt, prefer the honest `null` — a forced trace is worse than an admitted gap.
- **Adjust a size** where the flat 20% is clearly wrong for *this* item (a trivial config toggle vs. a cross-cutting feature), staying grounded in the comparators. Never inflate to look impressive; never deflate to make something look cheap.
- **Lift priority to `high`** — but only for a traced item, and only with a one-line reason naming the outcome and the urgency. Untraced items stay `low`; you do not promote scope creep to high.
- **Write an honest rationale** — one or two sentences. When traced: name the outcome and how you sized it. When `null`: say plainly that no accepted outcome backs it, so it is parked as a low-priority flag.

The output is a set of **deferral suggestions** with status `parked`. You are still only proposing — the human parks, promotes, or declines.

### Step 3 — PARK (human action)

The human reviews the suggested deferrals and parks the ones worth keeping. Parking resolves the outcome key to a real trace edge and records the item as `parked`. The item now lives on the backlog with its trace, size, and priority attached. Nothing is enforced; the item simply waits on the backlog.

### Step 4 — PROMOTE a parked item → an 'add' release delta (carrying the same trace)

This is the backlog → delivery handoff. When a human promotes a parked item:

- It becomes a **release delta** with `change_kind = "add"`, attached to a chosen target release/wave.
- It **carries the same trace forward** — the outcome the parked item derived from becomes the outcome the release change derives from. The thread from *business outcome → backlog item → shipped change* stays unbroken.
- The item is stamped as **promoted** (which release it went to), so its journey is recorded.
- Source is `human` — a promotion is a deliberate human act, not an agent guess.

The one rule to remember: **promote = an 'add' delta carrying the same trace.** An untraced (`null`) item *can* still be promoted, but it lands as an `add` with no outcome — which the release reconcile will flag as scope creep, exactly as it should. Promotion does not launder a missing trace.

### Step 5 — DECLINE is remembered (dismissal-memory)

When a human declines an item, the decision is **durable**. Record:

- the item, the **evidence it was declined against** (the outcomes and effort reference at the time), and the date/why.

So long as that evidence is **unchanged**, the item is **never re-proposed**. It only resurfaces if the evidence changes — a new outcome is agreed, a comparator shifts the sizing, the business context moves. This preserves the why-not: the team has a durable record of what they chose *not* to build and why, and they are not asked to re-decide the same thing twice.

Decline ≠ delete. A declined item is remembered, not erased — keep the rejected path on record.

## GitHub-native mapping

Triage maps cleanly onto a **GitHub Project backlog**, so teams run it with native mechanics:

- **Parked item** → a card in the **Backlog** column of the project's GitHub Project (or a `Backlog`-status issue).
- **derives_from** → a label like `outcome:BO-3`, or a linked issue to the outcome. An untraced item carries a `scope-creep` label instead.
- **est_effort_days** → a numeric Project field (e.g. `Est (days)`).
- **suggested_priority** → labels `priority:high` / `priority:medium` / `priority:low`.
- **Promote** → move the card to a **Ready / In a release** column and open the corresponding `add` change against the target release (a PR or a release-tracking issue), carrying the `outcome:` label forward.
- **Decline** → move to a **Declined / Won't do** column and **keep it there** with a `declined` label and a short comment recording the why and the evidence — that comment *is* the dismissal-memory. Do not close-and-delete; the record is the point.

A light GitHub Action can validate that every non-`scope-creep` card carries an `outcome:` label and a non-empty estimate before it leaves the backlog — advisory (a check annotation), never blocking.

## Output format

Return a markdown **menu of suggested deferrals** the user can act on. Each item shows its trace (or honest null), size, priority, and a one-line rationale. End with the promote/decline rules so the human knows their levers.

### Template

```markdown
## Backlog triage — suggested deferrals (parked)

> Suggestions only. Park, promote, or decline — you own every disposition.

| # | Title | Traces to | Est (days) | Priority | Rationale |
|---|-------|-----------|-----------:|----------|-----------|
| 1 | Bulk re-assign approvals across reviewers | BO-3 | 4.5 | medium | Serves BO-3 (reviewers manage load); sized at ~20% of the comparable approval-workflow build. |
| 2 | Dark-mode theme for the portal | — (null) | 2.0 | low | No accepted outcome behind it — parked as a low-priority scope-creep flag. |
| 3 | One-click compliance export bundle | BO-1 | 6.0 | high | Serves BO-1 (auditable evidence); raised to high — named blocker for the Q3 audit. Sized above the flat fraction: cross-cutting, touches every record type. |
| 4 | Misc UI polish pass | — (null) | — (unsizable) | low | No outcome behind it and no comparator to size against — parked as a flag. |

### Promote a parked item
`Promote #N → release R` creates an **'add'** change on release R carrying the **same trace** (#1 → BO-3, #3 → BO-1). Promoting an untraced item (#2, #4) lands an `add` with no outcome — the release reconcile will flag it as scope creep.

### Decline a parked item
`Decline #N` is **remembered**. It will not be re-proposed while the outcomes and effort reference are unchanged. Record the why; it only resurfaces if the evidence moves.
```

### The triage prompt (the LLM step)

Drop this into any LLM. It returns structured JSON you render into the menu above.

```
You are a backlog-triage analyst on a delivery team. Read the candidate backlog
items and turn each into a PROPOSED deferral suggestion — a recommendation about
whether to park an item now and at what size and priority. You SUGGEST only — you
never issue a verdict or a status; the item is recorded as 'parked'.

PROJECT: <title>

ACCEPTED OUTCOMES (the agreed business outcomes, each with a real key — the ONLY
outcomes an item may trace to; may be sparse):
<outcomes: key + text, one per line>

EFFORT REFERENCE (comparable past projects whose ACTUAL effort is known — use these
to size the deferred items honestly; a single deferred feature is a small fraction
of a whole-project effort; may be sparse):
<comparators: name + actual effort_days>

ALREADY DECLINED (do NOT re-propose these unless the evidence above has changed):
<declined items, or "none">

CANDIDATE BACKLOG ITEMS:
<candidates, one per line>

For EACH candidate item, emit one deferral suggestion:
- "title": a concise restatement of the candidate item.
- "derives_from": the key of the ONE accepted outcome this item
  genuinely serves, taken VERBATIM from the outcomes above. If it serves no
  accepted outcome, set this to null — an honest null is better than a forced
  trace, and signals scope creep.
- "est_effort_days": a small, believable size in person-days for THIS one item,
  grounded in the effort reference (a fraction of a whole-project effort). Use
  null only when there is no basis to size it at all.
- "suggested_priority": exactly one of "high", "medium", "low", or null. Items
  that trace to an accepted outcome generally carry more priority; an untraced
  item (a scope-creep flag) carries less. Use "high" only for a traced item with
  a named urgency. Stay honest — do not inflate.
- "rationale": one or two sentences. When traced, name the outcome and how you
  sized it. When null, say plainly that no accepted outcome backs it, so it is
  parked as a low-priority flag.

Stay grounded in the candidates, outcomes, and effort reference. Do not invent
outcomes, keys, or numbers the material does not support.

Return ONLY a JSON object of this shape, no prose, no markdown fence:
{
  "deferrals": [
    {
      "title": "Bulk re-assign approvals across reviewers",
      "derives_from": "BO-3",
      "est_effort_days": 4.5,
      "suggested_priority": "medium",
      "rationale": "Serves outcome BO-3 (reviewers manage load); sized at ~20% of the comparable approval-workflow build."
    },
    {
      "title": "Dark-mode theme for the portal",
      "derives_from": null,
      "est_effort_days": 2.0,
      "suggested_priority": "low",
      "rationale": "No accepted outcome behind it — parked as a low-priority flag."
    }
  ]
}
```

## Notes / anti-patterns

- **An honest null beats a forced trace.** The whole value of triage is finding the items that serve *nothing agreed*. Don't reach for the nearest outcome to make an item look legitimate — `null` *is* the finding. Two shared meaningful tokens is the floor for claiming a trace; below that, it's scope creep.
- **Don't inflate sizes or priorities.** "Small" is not "free", and "exciting" is not "high". A size grounded in actuals and a priority that falls out of the trace are what make the menu trustworthy. The moment you optimise the numbers to win an argument, the triage is worthless.
- **Never block.** This is advisory. You produce a menu; the human parks, promotes, or declines. No approval step, no blocking. The only "enforcement" is a soft, annotating CI check that *informs* — it never stops anyone.
- **Promotion carries the trace; it does not invent one.** Promoting an untraced item lands an `add` with no outcome, which gets flagged downstream. That is correct behaviour, not a bug — promotion is not a laundromat for missing traces.
- **Decline is memory, not deletion.** Declined items stay on record with the evidence they were declined against. Re-proposing a declined item against unchanged evidence is the anti-pattern — it wastes the team's attention and erases the why-not. Only resurface when the evidence genuinely changes.
- **Sparse inputs are normal.** Sparse outcomes → more honest nulls. No comparators → unsizable (`null`) sizes, not guesses. Don't paper over thin evidence with confident-looking fabrication.
- **The human owns the source field.** Agent-suggested items are proposals; parking, promoting, and declining are human acts (`source = human`). Keep the line between "the agent proposed" and "the human decided" visible at all times.
