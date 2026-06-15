---
name: validate-solution-vs-requirements
description: Replay every requirement against the chosen solution's enforced constraints and surface only the friction — met|compromised|unmet computed from constraint replay, never a model verdict; each compromise walks the trace up to the outcome it dents.
one_liner: Replay requirements against a solution's constraints; surface the friction.
aliases: [solution validation, fit check, trade-off check, requirement coverage, constraint check, does the design meet the requirements, gap analysis]
when_to_use: a solution shape is chosen and must be validated back against the requirements
output_kinds: [question, proposal]
deterministic_fallback: the constraint-replay table (requirement x enforced constraint)
suggested_tier: frontier
neighbours: after architect/propagate-pattern-nfrs (which flows pattern NFRs into requirements); before architect/surface-open-decisions (which collects the contested calls). Constraints come from architect/recommend-component-patterns; the mirror over-reach check is challenge/necessity-check.
---

# validate-solution-vs-requirements — constraint replay + compromise flags

Validate a chosen solution back against the requirements and show only the friction.
Satisfied requirements settle and stay quiet; compromises surface, each one walking the
trace edge *up* to the business outcome and capability it dents. The flag is computed; a
verdict is never emitted.

## Purpose

A solution has been adopted — a pattern, or a narrowed-down shape. It carries **enforced
constraints**: the things it makes the design give up. *"All writes are async via the event
bus; no synchronous DB writes."* *"Single region only."* Those constraints are real, and
some requirements will collide with them.

This skill **replays every requirement against those enforced constraints** and tags each
one `met` | `compromised` | `unmet`. The defining discipline:

> **The flag is COMPUTED from the constraint replay. It is NEVER a model-emitted verdict.**

A requirement that needs `instant-write` colliding with a `hard` constraint that
`degrades_capability: instant-write` is **computed** to `compromised` (or `unmet`). The
model does not "decide" the requirement is compromised — the replay table does, mechanically,
by matching capability tags against what the constraint degrades. The model's only job is to
**phrase the resulting compromise as a grounded question** the human can rule on.

Two further disciplines, both load-bearing:

1. **Nothing is dropped without flagging.** Every compromise walks the trace edge *up* to
   the business outcome — and the capability above it — that it dents. Contested items stay
   **visible**, never quietly tidied away. This is the honesty contract: lead with the
   compromises, never filter to "accepted" and drop them.

2. **The flag is computed; the disposition is human.** `accept` or `reject` for each
   compromise is a **genuinely-human contested call**. This skill emits the compromise as a
   `question` naming *both* the requirement and the outcome it dents — it never accepts or
   rejects on the human's behalf, and it never says "this is fine."

There is **no pass/fail stamp** here. A validation pass that finds zero compromises is a
legitimate, non-failing outcome — it means the solution fits. The output is friction to rule
on, not a verdict.

## When to use

- A **solution shape is chosen** (an adopted pattern, or a narrowed shape) and it must be
  validated back against the requirements.
- You want to know **which requirements the solution can't fully honour** — before the
  prototype, while the trade-off is still cheap to surface.
- You want each trade-off **phrased as a question that names the outcome it costs**, so the
  human is ruling on a business consequence, not a technical detail in isolation.
- You are assembling the build handoff and need the **compromises for `OPEN-QUESTIONS.md`** —
  the unresolved and human-accepted trade-offs that the next human must see.

## Inputs (what you supply)

Provide, as markdown or plain context:

1. **The chosen solution's enforced constraints** — from the adopted pattern (its
   `pattern_constraint` rows) or the narrowed shape. Each constraint needs:
   - a stable key (e.g. `CON-ASYNC-WRITES-ONLY`),
   - a one-line `statement` ("All writes are async via the event bus; no synchronous DB writes"),
   - `enforced`: **`hard`** (cannot be waived) or **`soft`** (waiver = a recorded compromise),
   - `degrades_capability`: a machine hint — `instant-write` · `real-time` · `cross-region` ·
     `synchronous-read` · `single-region` — the capability the constraint takes away.

   ```
   CON-ASYNC-WRITES-ONLY  | hard | degrades: instant-write  | All writes are async via the event bus; no synchronous DB writes.
   CON-SINGLE-REGION      | hard | degrades: cross-region   | Data and compute live in one region; no cross-region replication.
   CON-CACHE-TTL-60S      | soft | degrades: real-time      | Read path is cached with a 60s TTL; reads may lag writes by up to 60s.
   ```

2. **The requirement set** — the live derived requirements, each with:
   - a stable, cite-able `req_key` (e.g. `TR-022`),
   - its `text`,
   - its `capability_tags` — what the requirement *needs* (`instant-write`, `cross-region`,
     `real-time`, …). If tags are absent, infer them in the model step and **say you inferred them.**
   - its `derives_from` chain: the `outcome_key` (and `text`) it serves, and the
     `capability` (e.g. `CAP-CUSTOMER-SELF-SERVICE`) above that. **This is what each
     compromise walks up to.**

   ```
   TR-022 | needs: instant-write | "Confirmation shown the instant a change is saved"
          | serves OUT-3 "Customers complete account changes without calling support"
          | under CAP-CUSTOMER-SELF-SERVICE
   TR-031 | needs: cross-region  | "Records replicated to the DR region within 5 min"
          | serves OUT-7 "Service survives a regional outage"
          | under CAP-RESILIENCE
   ```

If there are no `req_key`s, say so and emit the deterministic replay table with empty keys —
do not invent ids.

## The method (STEPS)

The base is **deterministic** (the replay table); the model step only **phrases** the
computed compromises as grounded questions. Keep that separation — it is what keeps the flag
honest.

### Step 1 — DETERMINISTIC STEP: build the requirement × enforced-constraint replay table

This is the deterministic fallback and the base of the whole skill. For **every** requirement,
replay it against **every** enforced constraint and compute the cell:

For each `(requirement, constraint)` pair, the cell **clashes** when:

> `constraint.degrades_capability` ∈ `requirement.capability_tags`

Then compute the requirement's `satisfaction` flag from its clashes — **mechanically, by this
exact table, not by judgment**:

| The requirement's clashes…                                   | Computed flag  |
| ------------------------------------------------------------ | -------------- |
| collides with **no** enforced constraint                     | `met`          |
| collides only with **`soft`** constraint(s)                  | `compromised`  |
| collides with at least one **`hard`** constraint             | `unmet`        |
| has no `capability_tags` and none could be inferred          | `unevaluated`  |

A `soft` clash is `compromised` because a human *can* accept the degraded form (e.g. "instant"
relaxes to "≤2s"). A `hard` clash is `unmet` because the constraint cannot be waived — the
requirement, as written, cannot be honoured by this solution. **The flag is the output of this
table. The model never overrides it upward or downward.**

Render the full replay table (every requirement × the clashing constraints). This is the
reproducible, provider-independent floor: even with no model available, return every
requirement with its computed flag and the constraint key it clashed on.

### Step 2 — Keep only the friction; settle the rest

A requirement flagged `met` **settles** — it is reported as a count, not as a card. The output
leads with the **`compromised` and `unmet`** rows only. This is "show only the friction":
satisfied requirements are quiet; compromises are loud.

But quiet is **not dropped.** Every `met` requirement is still in the replay table (Step 1) and
still counted. Nothing is hidden — the friction is just what gets the cards.

### Step 3 — Walk each compromise UP the trace edge

For every `compromised`/`unmet` requirement, resolve its `derives_from` chain so the compromise
carries the **business consequence** with it:

```
requirement (TR-022)  →  outcome (OUT-3)  →  capability (CAP-CUSTOMER-SELF-SERVICE)
```

The compromise is *not* "TR-022 degrades." It is **"OUT-3 — *Customers complete account changes
without calling support* — takes the dent."** Every flag names the outcome and the capability it
costs. **Nothing is dropped without flagging; contested items stay visible.** A compromise with
no upstream outcome is itself a flag — surface it as an orphaned requirement, do not silently
drop it.

### Step 4 — MODEL STEP: phrase each compromise as a grounded question

The replay computed *which* requirements are compromised and *what* they dent. The model's job
is to phrase each one as a single **grounded question** that names **both the requirement and
the outcome**, states the constraint that caused it, and (for `soft`/`compromised`) names the
**degraded form** the human is being asked to accept. Run this prompt over the computed friction:

> COMPUTE FLAGS, NEVER VERDICTS. The `met`/`compromised`/`unmet` flags were already computed
> deterministically from the constraint replay — do not change them, re-rank them, or add a
> "looks fine / looks risky" assessment.
>
> CHOSEN SOLUTION CONSTRAINTS: `<constraints with enforced + degrades_capability>`
> COMPROMISED / UNMET REQUIREMENTS (with their computed flag, the clashing constraint, and the
> outcome + capability each derives from): `<the friction rows from Steps 1–3>`
>
> For EACH compromised/unmet requirement, write ONE `question` object with:
> - `req_key`, `flag` (verbatim — `compromised` or `unmet`; do not change it),
> - `constraint_key` — the enforced constraint it clashed on,
> - `outcome_key` + `outcome_text` — the outcome it dents (walked up the trace),
> - `capability` — the competency above that outcome,
> - `degraded_to` — for a `soft`/`compromised` clash, the relaxed form being proposed
>   (e.g. "instant → ≤2s"); for a `hard`/`unmet` clash, set this null,
> - `question` — one sentence naming the requirement AND the outcome AND the constraint,
>   ending in the human's call. Examples of the SHAPE (not the answer):
>   - compromised: "The pattern enforces async writes, so *TR-022 — instant confirmation* —
>     can only reach **≤2s**, denting *OUT-3 (customers self-serve without calling)*. Accept
>     the degraded ≤2s form, or reject this solution for this outcome?"
>   - unmet: "*CON-SINGLE-REGION* (hard) cannot satisfy *TR-031 — cross-region replication*,
>     which serves *OUT-7 (survive a regional outage)*. This outcome is **unmet** by this
>     solution as written — accept it as a known risk, or does the solution need to change?"
>
> Do NOT recommend which way to rule. Do NOT mark one compromise more important than another.
> Do NOT say a requirement is "fine" or a solution is "good enough." Return ONLY the JSON below.

```json
{
  "summary": { "evaluated": 14, "met": 11, "compromised": 2, "unmet": 1, "unevaluated": 0 },
  "compromises": [
    {
      "req_key": "TR-022",
      "flag": "compromised",
      "constraint_key": "CON-ASYNC-WRITES-ONLY",
      "outcome_key": "OUT-3",
      "outcome_text": "Customers complete account changes without calling support",
      "capability": "CAP-CUSTOMER-SELF-SERVICE",
      "degraded_to": "instant → ≤2s",
      "question": "The pattern enforces async writes, so TR-022 (instant confirmation) can only reach ≤2s, denting OUT-3 (customers self-serve without calling). Accept the degraded ≤2s form, or reject this solution for this outcome?"
    },
    {
      "req_key": "TR-031",
      "flag": "unmet",
      "constraint_key": "CON-SINGLE-REGION",
      "outcome_key": "OUT-7",
      "outcome_text": "Service survives a regional outage",
      "capability": "CAP-RESILIENCE",
      "degraded_to": null,
      "question": "CON-SINGLE-REGION (hard) cannot satisfy TR-031 (cross-region replication), which serves OUT-7 (survive a regional outage). This outcome is unmet by this solution as written — accept it as a known risk, or does the solution need to change?"
    }
  ]
}
```

### Step 5 — Hand the friction to the human; persist nothing

Each compromise is a `question` the human rules on by **accepting** (the degraded form becomes
the agreed reality, recorded) or **rejecting** (the solution must change for that outcome). This
skill **emits the questions and persists nothing.** The accept/reject is a separate human action
— a contested call — and the disposition is what gets recorded downstream (as a `decision` of
kind `compromise_accept` / `compromise_reject`, and an entry in `OPEN-QUESTIONS.md`). The skill
computes the flag; the human owns the call.

## Output format

Lead with the computed summary, then the **replay table** (the deterministic base), then the
**compromises as questions**. Met requirements are a count, not cards.

```markdown
## Solution validation — <project / solution name>

**Replay:** 14 requirements × 3 enforced constraints.
**Computed:** 11 met · 2 compromised · 1 unmet · 0 unevaluated.
_Flags computed from the constraint replay below — not assessed. Each compromise is a human call._

### Constraint replay (the deterministic base)

| req_key | requirement                          | needs         | clashes with         | enforced | flag         |
|---------|--------------------------------------|---------------|----------------------|----------|--------------|
| TR-022  | Instant confirmation on save         | instant-write | CON-ASYNC-WRITES-ONLY | hard*    | compromised  |
| TR-031  | Cross-region DR replication          | cross-region  | CON-SINGLE-REGION     | hard     | unmet        |
| TR-040  | Read freshness for dashboard         | real-time     | CON-CACHE-TTL-60S     | soft     | compromised  |
| TR-005  | OAuth2 on all API callers            | —             | —                    | —        | met          |
| …       | (11 met requirements settle — counted, not carded) |   |                      |          | met          |

> *TR-022: the async constraint is `hard`, but the requirement's "instant" can relax to a
> bounded "≤2s" — so a human may accept it as `compromised` rather than `unmet`. See the question.

### Friction to rule on (each walks up to the outcome it dents)

**TR-022 — compromised** · clashes `CON-ASYNC-WRITES-ONLY`
↑ dents **OUT-3** *Customers complete account changes without calling support* (CAP-CUSTOMER-SELF-SERVICE)
> The pattern enforces async writes, so **TR-022 (instant confirmation)** can only reach **≤2s**,
> denting **OUT-3**. **Accept the degraded ≤2s form, or reject this solution for this outcome?**

**TR-031 — unmet** · clashes `CON-SINGLE-REGION` (hard)
↑ dents **OUT-7** *Service survives a regional outage* (CAP-RESILIENCE)
> **CON-SINGLE-REGION (hard)** cannot satisfy **TR-031 (cross-region replication)**, which serves
> **OUT-7**. This outcome is **unmet** by this solution as written. **Accept it as a known risk,
> or does the solution need to change?**

_Computed flags, not verdicts. The 11 met requirements settle. Accepting or rejecting each
compromise is a human call — accepted compromises and unmet outcomes flow into `OPEN-QUESTIONS.md`
as recorded trade-offs and known risks. Nothing here is persisted by this skill._
```

If the replay finds **zero compromises**, say so plainly — "14 of 14 met; the solution honours
every requirement as written" — and emit no questions. That is a legitimate, non-failing outcome,
not a thin result to pad.

## Notes / anti-patterns

- **Compute the flag; never emit it as a verdict.** The flag is the output of the replay table in
  Step 1. The model phrases it; it never *decides* it. ❌ "I judge TR-022 to be acceptable." The
  legal move is the question that names the trade-off and hands the call to the human.
- **`hard` → `unmet`, `soft` → `compromised`. Don't soften a hard clash.** A `hard` constraint
  cannot be waived; a requirement colliding with it is `unmet`, full stop. The human may *accept
  the unmet outcome as a known risk* — but the requirement is not magically "compromised" because
  acceptance happened. Record the acceptance; keep the flag honest.
- **Walk up, always.** A compromise that doesn't name the outcome it dents is half a flag. The
  whole point of the trace edge is that the human rules on a *business consequence*, not a stray
  technical detail. ❌ "TR-022 degrades." ✅ "OUT-3 takes the dent because TR-022 degrades."
- **Nothing dropped without flagging.** Never quietly filter out a compromise to make the solution
  look cleaner. A requirement with no upstream outcome is itself flagged (orphaned), not deleted.
- **Met requirements settle; they don't vanish.** Report the met count and keep them in the replay
  table. "Show only the friction" means *lead with* the friction, not *erase* the rest.
- **Don't rank the compromises.** Two compromises are two equal questions. Ordering them
  "most severe first" smuggles a verdict. Order them by `req_key` or by appearance in the table —
  carry no signal in the order.
- **No accept/reject on the human's behalf.** This skill emits `question`s. It never writes
  `compromise_accept`, never marks an outcome "risk accepted," never edits a requirement. The
  disposition is a separate, recorded human action.
- **Zero compromises is success.** A solution that honours every requirement produces an empty
  friction list. Don't invent a marginal compromise to look thorough — an honest "it all fits" is
  the strongest result this skill can return.
- **Advisory, not blocking.** A pile of `unmet` requirements does not *block* the project. It hands
  the human a set of contested calls. The human decides whether to change the solution, accept the
  risks, or proceed — this skill never stops them.
```
