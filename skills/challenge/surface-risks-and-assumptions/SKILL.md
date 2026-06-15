---
name: surface-risks-and-assumptions
description: Maintain a light markdown RAID register — surface the small set of load-bearing assumptions the plan depends on, deduped against the existing register (open and closed); agent proposes open, human disposes. Use this to ground a project's hidden dependencies.
one_liner: Name the load-bearing bets a plan depends on.
aliases: [assumptions, risk register, RAID, hidden dependencies, what could go wrong, risk log, assumption log]
when_to_use: grounding a project's hidden dependencies before/while you build
output_kinds: [proposal, question]
deterministic_fallback: the RAID register template + the dedupe exact-match backstop
suggested_tier: mid
neighbours: Usually follows challenge/red-team-requirements (conflicts/gaps already found) and precedes challenge/enumerate-roadblocks (immediate blockers).
---

# Surface Risks and Assumptions — the light RAID register

Surface the small set of load-bearing assumptions a plan depends on, deduped against the register; the agent proposes open items, a human disposes.

A RAID register is the small, honest list of things a plan is *betting on*. Most of those bets are invisible: nobody wrote them down because they felt obvious at the time. This skill drags the load-bearing ones into the light so that, when one turns out to be wrong, it surfaces on purpose instead of by accident.

It is **advisory: it does not block.** Nothing here stops a phase or demands a sign-off. The register sits beside the work and grounds it. The only discipline it enforces is a division of labour: **the agent proposes, the human disposes.**

## Purpose

Surface the small genuine set of **load-bearing ASSUMPTIONS** a delivery plan depends on — the things taken to be true that, if wrong, would change the plan. Assumptions are the default kind here, but the register is one kind-discriminated entity, so it also carries:

- **risk** — something that *might* happen (likelihood × impact + a mitigation), and
- **tech_debt** — a durable carried-forward concern from a design or review.

**Bias hard toward few.** A register with forty assumptions is a register nobody reads. The goal is the handful of genuine, grounded bets — prefer a short list of real ones over a long list of restated requirements. If the inputs are thin, return few or none. An empty register that everyone trusts beats a padded one everyone ignores.

The register stays light: no disposition workflow, no version-bound sign-off, no approval ceremony. There is a markdown file, a derive step, and a human who closes items out.

## When to use

- You are grounding a new or in-flight project and want its hidden dependencies named.
- A business case or solution design just landed and you want to surface what it quietly assumes.
- You are about to commit budget, pick a vendor, or schedule against a regulatory date and want the bet written down.
- Something in the plan changed and you want to re-check which old assumptions still hold.

It **coexists with roadblocks** (a panel- or design-surfaced blocker). A roadblock is loud and immediate; a register item is durable and tracked. When a roadblock is real and carried-forward, a human promotes it into a register risk — that promotion is the one-way bridge, never an automatic twin.

## Inputs

The user supplies, as markdown or plain context:

1. **Project title + description** — what is being built.
2. **Business case** — why; the demand/value/funding story.
3. **Context** — anything else grounding the plan: constraints, vendors, timelines, staffing.
4. **The existing register** (if one exists) — the current `references/raid-register.template.md` file, including items already **closed out** (validated / invalidated). This is essential: it is how the agent avoids re-proposing what was already dealt with.

If there is no register yet, start from the template in `references/raid-register.template.md`.

## The method

The method has a **deterministic base** (the register file and an exact-match dedupe that runs without any model) and one **LLM reasoning step** (the derive prompt). Keep them distinct: the model is the semantic deduper; the deterministic backstop only stops a word-for-word repeat slipping through.

### Step 1 — DETERMINISTIC: load (or create) the register

Open `references/raid-register.template.md` (copy it into the project if this is the first run). Parse the existing items into a list of `{kind, title, statement, status}`. You will need **all** of them — both `open` items and already-**closed-out** ones — for the dedupe. Closed-out items are not noise: re-proposing something a human already validated or invalidated is exactly the resurrection this step exists to prevent.

### Step 2 — LLM: derive the assumptions (the reasoning step)

Run the derive prompt below over the inputs. Pass in the existing register so the model dedupes **semantically, in-prompt** — it owns "this is the same underlying assumption, just re-phrased." Use the prompt **verbatim**:

> You are helping ground a delivery project. From the project's business case and context below, surface the key ASSUMPTIONS the project is implicitly DEPENDING ON — the things taken to be true that, if wrong, would change the plan. Think: market/demand assumptions, budget/licence-cost assumptions, resource/staff availability, vendor or integration availability, regulatory timelines, technical preconditions. Be specific and grounded in what is written — do NOT invent scope, and do NOT restate requirements as assumptions. Prefer a small set of genuine, load-bearing assumptions over a long list. If the inputs are thin, return few (or none).
>
> PROJECT: `${title}`
> `${description}`
>
> BUSINESS CASE:
> `${business_case}`
>
> CONTEXT:
> `${context}`
>
> ALREADY ON THE REGISTER — do NOT propose any of these again, neither a duplicate nor a re-phrasing of the SAME underlying assumption, whether it is still open or already closed out (validated/invalidated). Only return assumptions that are genuinely NEW relative to this list:
> `${existing_assumptions}`
>
> Return ONLY a JSON object of exactly this shape, no prose, no fence:
> ```json
> {
>   "assumptions": [
>     {
>       "title": "a short label for the assumption",
>       "statement": "one or two sentences stating what is assumed and what depends on it",
>       "category": "a short open category, e.g. market-scan, license-cost, resource-availability (optional)"
>     }
>   ]
> }
> ```

The seven lenses to think through — they are the whole point of the reasoning step, so do not skip any:

| Lens | Ask yourself |
|------|--------------|
| **Market / demand** | Are we assuming the users/volume/appetite are there? |
| **Budget / licence cost** | Are we assuming funding holds, or that a tool's price stays in range? |
| **Resource availability** | Are we assuming the people (skills, headcount, time) will be free when needed? |
| **Vendor / integration availability** | Are we assuming a third party, API, or upstream system exists and behaves? |
| **Regulatory timelines** | Are we assuming a rule, approval, or compliance date lands when we need it? |
| **Technical preconditions** | Are we assuming some platform, data, or capability is already in place? |

Each derived item is `{title, statement, category}`. **Be specific and grounded** — anchor every statement in something actually written in the inputs. The hard rule: **do NOT restate requirements as assumptions.** "The system must export to PDF" is a requirement; "we assume the licensed PDF library remains free for commercial use" is an assumption. The first describes what you will build; the second is a bet whose failure changes the plan.

### Step 3 — DETERMINISTIC: exact-match dedupe backstop

The model already removed semantic duplicates in Step 2. This step is the **zero-false-positive backstop** — it only catches a *verbatim* repeat that slipped through. For each proposed item, normalise its `title` and `statement` (lowercase, collapse whitespace) and drop it if the normalised string exactly matches the `title` or `statement` of **any** existing item (open or closed). Add survivors to the seen-set as you go so the batch does not duplicate itself. The normalisation:

```python
def _norm(s: str) -> str:
    return " ".join((s or "").lower().split())

seen_titles     = {_norm(i["title"])     for i in existing}   # open AND closed
seen_statements = {_norm(i["statement"]) for i in existing}

kept = []
for p in proposed:                      # assumptions only on this pass
    if _norm(p["title"]) in seen_titles or _norm(p["statement"]) in seen_statements:
        continue                        # verbatim repeat — skip
    seen_titles.add(_norm(p["title"]))
    seen_statements.add(_norm(p["statement"]))
    kept.append(p)
```

Do **not** make this a fuzzy lexical filter — the model owns semantic dedupe and a fuzzy backstop would fight it and silently swallow genuinely-new items. Exact-match only.

### Step 4 — Agent proposes `open`; the human disposes

Every kept item is written to the register with **`status: open`**. The agent never closes anything out. Disposition is a small, kind-validated vocabulary the **human** owns:

| Kind | Live state | Legal closeouts |
|------|-----------|-----------------|
| **assumption** | `open` | `validated` · `invalidated` |
| **risk** | `open` | `mitigated` · `avoided` · `accepted` · `realised` |
| **tech_debt** | `open` | `accepted` · `remediated` · `wont_fix` |

A closeout that is illegal for the item's kind is rejected — you cannot mark an assumption `mitigated`. When a human disposes, they append a one-line note and the date; the row is never deleted (history lives in the file). A **fired** closeout — `assumption → invalidated`, `risk → realised` — is a rework signal: surface it against everything that depended on the item.

### Step 5 — Derived-on-read revisit cadence (no scheduler)

An item can carry a `review_cadence_days`. **Due-ness is computed when you read the register, not pushed by a timer.** There is no scheduler, no cron, no stored "is it due" flag to fall out of sync:

```
next_review_at = last_reviewed_at + review_cadence_days
due_for_review = (cadence set) AND (status is open) AND (now >= next_review_at)
```

Two human actions touch the clock, and they are distinct:
- **Re-review** re-arms the cadence (`last_reviewed_at = now`) and leaves status **unchanged** — "I looked, it still holds."
- **Closeout** changes status — "this bet resolved."

And the principle that makes the register honest over time: **a new widening fact retires an assumption and obliges re-proposal.** If something you learn makes an old assumption no longer safe, the human marks it `invalidated` and a fresh derive run (Step 2, with the now-closed item in the existing list) proposes the corrected one. The register tracks not just what you assumed, but what you *learned*.

## Output format

A single markdown file: `references/raid-register.template.md`, one table row per item, newest first. Concrete example after a derive run:

```markdown
# RAID Register — Project: Field Inspector Mobile App

> Advisory: does not block. Agent proposes `open`; a human disposes (validated/invalidated,
> mitigated/avoided/accepted/realised, accepted/remediated/wont_fix). Coexists with roadblocks.

| id | kind | title | statement | category | status | cadence (d) | last reviewed | source | disposed (note · date) |
|----|------|-------|-----------|----------|--------|-------------|---------------|--------|------------------------|
| A-1 | assumption | Offline sync window holds | We assume inspectors are offline ≤ 4h/day, so a 4h local cache covers a shift. If they go offline for full days, the sync model breaks. | technical-precondition | open | 90 | 2026-06-15 | agent | — |
| A-2 | assumption | Mapping licence stays free tier | We assume the OS mapping API's free tier (10k calls/day) covers projected usage; the budget carries no map-licence line. | license-cost | open | 60 | 2026-06-15 | agent | — |
| A-3 | assumption | Two field engineers available Q3 | We assume the two named field engineers are free for the Q3 rollout; the phase plan has no backfill. | resource-availability | invalidated | — | — | agent | one engineer reassigned to Ops · 2026-06-14 |
| R-1 | risk | Carrier coverage gaps in remote sites | Some inspection sites have no cell coverage; sync may stall for days. | likelihood: med / impact: high — mitigation: queue + manual export fallback | connectivity | open | 30 | 2026-06-15 | human (promoted from roadblock) | — |
```

Notes on the output:
- **id prefixes** (`A-`, `R-`, `T-`) are a light reading aid, not a key — the table is the store.
- For a **risk**, fold `likelihood / impact / mitigation` into the statement or category cell (assumptions leave them blank — they are risk-only).
- The **disposed** column holds the human's one-line note plus the ISO date; an open item shows `—`.
- A1/A2 above were *kept* by the derive run; A3 was already on the register and got **invalidated** by a human, so the next run will not re-propose it (Step 3 backstop + the model seeing it in `existing_assumptions`).

## Notes / anti-patterns

- **Advisory; it does not block.** If you find yourself blocking a phase on a register item, stop — promote it to a roadblock or just flag it. The register grounds; it does not enforce.
- **Restating requirements as assumptions** is the single most common failure. "The app must work offline" is a requirement. "We assume offline windows are ≤ 4h" is the bet underneath it. Only the bet belongs here.
- **Padding the list.** Ten weak assumptions bury the two that matter. Bias toward few; thin inputs earn a short (or empty) register.
- **The agent closing things out.** The agent proposes `open` and nothing else. A status of `validated`/`invalidated`/`mitigated`/… is a human judgement with a note and a date.
- **A fuzzy dedupe backstop.** The deterministic guard is exact-match only. The model owns semantic dedupe; a fuzzy filter would swallow genuinely-new items and you would never know.
- **Dropping closed items from the dedupe input.** You must pass *closed-out* items into the derive prompt and the exact-match seen-set, or every run resurrects bets a human already settled.
- **A scheduler for revisits.** Due-ness is derived on read. Do not add a cron; compute `due_for_review` when you open the file.
- **A parallel store for roadblocks.** A roadblock becomes a register item only by a human's one-way promotion. No automatic twin, no two-way sync.

Tone throughout: a grounding analyst. Name the bet plainly, anchor it in the evidence, keep the list short, and hand the verdict to the human.
