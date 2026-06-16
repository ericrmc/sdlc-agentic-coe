---
name: validate-solution-vs-requirements
description: Replay every requirement against the chosen solution's enforced constraints and surface only the friction — met|compromised|unmet computed from constraint replay, never a model verdict; each compromise walks the trace up to the outcome it dents.
one_liner: Replay requirements against a solution's constraints; surface the friction.
aliases: [solution validation, fit check, trade-off check, requirement coverage, constraint check, does the design meet the requirements, gap analysis]
when_to_use: a solution shape is chosen and must be validated back against the requirements
output_kinds: [question, proposal, halt]
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

An adopted solution carries **enforced constraints** — what it makes the design give up
(*"all writes async; no synchronous DB writes"*, *"single region only"*). This skill replays
every requirement against those constraints and tags each `met` | `compromised` | `unmet`.
The flag is **computed** by the Step-1 table (capability tag vs. what the constraint
degrades), never a model verdict; the model only phrases each compromise as a grounded
question the human rules on. Zero compromises is a legitimate, non-failing outcome.

## When to use

A solution shape is chosen (adopted pattern, or narrowed shape) and must be validated back
against the requirements — surfacing which it can't fully honour before the prototype, each
trade-off phrased as a question naming the outcome it costs, ready for `OPEN-QUESTIONS.md`.

## Inputs (what you supply)

Provide, as markdown or plain context:

1. **The chosen solution's enforced constraints** — *Required.* From the adopted pattern (its
   `pattern_constraint` rows) or the narrowed shape. *If absent/unreadable/empty: HALT and ask
   for the chosen solution's enforced constraints (per `_shared/grounding.md`); never invent a
   constraint, a `degrades_capability` hint, or an `enforced` level — a replay against
   fabricated constraints is a fabricated verdict.* Each constraint needs:
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

2. **The requirement set** — *Required.* The live derived requirements, each with:
   - a stable, cite-able `req_key` (e.g. `REQ-022`),
   - its `text`,
   - its `capability_tags` — what the requirement *needs* (`instant-write`, `cross-region`,
     `real-time`, …). If tags are absent, infer them in the model step and **say you inferred them.**
   - its `derives_from` chain: the `BO-<n>` business outcome (and `text`) it serves, and the
     `fulfils_capability` (e.g. `CAP-CUSTOMER-SELF-SERVICE`) above that. **This is what each
     compromise walks up to.**

   *If the requirement set is absent/unreadable/empty: HALT and ask where the derived
   requirements live (per `_shared/grounding.md`); never invent a `req_key` or a requirement to
   replay. There is nothing to validate with no requirements.* Readable forms: a markdown file,
   an xlsx/csv path, a GitHub Project owner+number, a docs folder, or a pasted block.

   ```
   REQ-022 | needs: instant-write | "Confirmation shown the instant a change is saved"
           | derives_from BO-3 "Customers complete account changes without calling support"
           | fulfils_capability CAP-CUSTOMER-SELF-SERVICE
   REQ-031 | needs: cross-region  | "Records replicated to the DR region within 5 min"
           | derives_from BO-7 "Service survives a regional outage"
           | fulfils_capability CAP-RESILIENCE
   ```

If the requirements are present but individual `req_key`s are missing, say so and emit the
deterministic replay table with empty keys — do not invent ids. (An entirely absent
requirement set HALTs per STEP 0, rather than producing an empty table — see
`skills/_contract/grounding-no-absent-input`.)

## Grounding (quoted)

This skill reads requirements and their `derives_from` chain, so it carries the no-fabrication
keystone — see `skills/_contract/grounding-no-absent-input`.

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

The base is **deterministic** (the replay table); the model step only **phrases** the
computed compromises as grounded questions. Keep that separation — it is what keeps the flag
honest.

### Step 0 — Locate / verify the required inputs (deterministic, pre-model)

Before building the replay table, confirm both Required inputs are present as a file-level
fact: the **chosen solution's enforced constraints** (one replay axis) and the **requirement
set** (the other). This is mechanical — absent / unreadable / empty — never a judgement on
"is the solution far enough along to validate."

- **Enforced constraints absent/unreadable/empty** → emit the clean HALT below and stop.
- **Requirement set absent/unreadable/empty** → HALT and ask where the derived requirements
  live.

```
HALT — required input missing.

I can't replay requirements against a solution without both the requirements and the
solution's enforced constraints, and I won't invent either — a replay against fabricated
inputs is a fabricated verdict. Point me at the missing side and I'll build the replay
table — nothing is assumed until then.

I can read any of: a markdown file · an xlsx/csv path · a GitHub Project (owner + number)
· a docs folder · the rows pasted directly here. Which one, and where?
```

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
requirement (REQ-022)  →  derives_from BO-3  →  fulfils_capability CAP-CUSTOMER-SELF-SERVICE
```

The compromise is *not* "REQ-022 degrades." It is **"BO-3 — *Customers complete account changes
without calling support* — takes the dent."** Every flag names the business outcome and the
capability it costs. **Nothing is dropped without flagging; contested items stay visible.** A
compromise with no upstream outcome is itself a flag — surface it as an orphaned requirement, do
not silently drop it.

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
> - `outcome_key` (a `BO-<n>` key) + `outcome_text` — the business outcome it dents (walked up
>   the trace),
> - `capability` — the competency above that outcome,
> - `degraded_to` — for a `soft`/`compromised` clash, the relaxed form being proposed
>   (e.g. "instant → ≤2s"); for a `hard`/`unmet` clash, set this null,
> - `question` — one sentence naming the requirement AND the outcome AND the constraint,
>   ending in the human's call. Examples of the SHAPE (not the answer):
>   - compromised: "The pattern enforces async writes, so *REQ-022 — instant confirmation* —
>     can only reach **≤2s**, denting *BO-3 (customers self-serve without calling)*. Accept
>     the degraded ≤2s form, or reject this solution for this outcome?"
>   - unmet: "*CON-SINGLE-REGION* (hard) cannot satisfy *REQ-031 — cross-region replication*,
>     which serves *BO-7 (survive a regional outage)*. This outcome is **unmet** by this
>     solution as written — accept it as a known risk, or does the solution need to change?"
>
> Do NOT recommend which way to rule. Do NOT mark one compromise more important than another.
> Do NOT say a requirement is "fine" or a solution is "good enough." Return ONLY the JSON below.

```json
{
  "summary": { "evaluated": 14, "met": 11, "compromised": 2, "unmet": 1, "unevaluated": 0 },
  "compromises": [
    {
      "req_key": "REQ-022",
      "flag": "compromised",
      "constraint_key": "CON-ASYNC-WRITES-ONLY",
      "outcome_key": "BO-3",
      "outcome_text": "Customers complete account changes without calling support",
      "capability": "CAP-CUSTOMER-SELF-SERVICE",
      "degraded_to": "instant → ≤2s",
      "question": "The pattern enforces async writes, so REQ-022 (instant confirmation) can only reach ≤2s, denting BO-3 (customers self-serve without calling). Accept the degraded ≤2s form, or reject this solution for this outcome?"
    },
    {
      "req_key": "REQ-031",
      "flag": "unmet",
      "constraint_key": "CON-SINGLE-REGION",
      "outcome_key": "BO-7",
      "outcome_text": "Service survives a regional outage",
      "capability": "CAP-RESILIENCE",
      "degraded_to": null,
      "question": "CON-SINGLE-REGION (hard) cannot satisfy REQ-031 (cross-region replication), which serves BO-7 (survive a regional outage). This outcome is unmet by this solution as written — accept it as a known risk, or does the solution need to change?"
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
| REQ-022 | Instant confirmation on save         | instant-write | CON-ASYNC-WRITES-ONLY | hard*    | compromised  |
| REQ-031 | Cross-region DR replication          | cross-region  | CON-SINGLE-REGION     | hard     | unmet        |
| REQ-040 | Read freshness for dashboard         | real-time     | CON-CACHE-TTL-60S     | soft     | compromised  |
| REQ-005 | OAuth2 on all API callers            | —             | —                    | —        | met          |
| …       | (11 met requirements settle — counted, not carded) |   |                      |          | met          |

> *REQ-022: the async constraint is `hard`, but the requirement's "instant" can relax to a
> bounded "≤2s" — so a human may accept it as `compromised` rather than `unmet`. See the question.

### Friction to rule on (each walks up to the outcome it dents)

**REQ-022 — compromised** · clashes `CON-ASYNC-WRITES-ONLY`
↑ dents **BO-3** *Customers complete account changes without calling support* (CAP-CUSTOMER-SELF-SERVICE)
> The pattern enforces async writes, so **REQ-022 (instant confirmation)** can only reach **≤2s**,
> denting **BO-3**. **Accept the degraded ≤2s form, or reject this solution for this outcome?**

**REQ-031 — unmet** · clashes `CON-SINGLE-REGION` (hard)
↑ dents **BO-7** *Service survives a regional outage* (CAP-RESILIENCE)
> **CON-SINGLE-REGION (hard)** cannot satisfy **REQ-031 (cross-region replication)**, which serves
> **BO-7**. This outcome is **unmet** by this solution as written. **Accept it as a known risk,
> or does the solution need to change?**

_Computed flags, not verdicts. The 11 met requirements settle. Accepting or rejecting each
compromise is a human call — accepted compromises and unmet outcomes flow into `OPEN-QUESTIONS.md`
as recorded trade-offs and known risks. Nothing here is persisted by this skill._
```

If the replay finds **zero compromises**, say so plainly — "14 of 14 met; the solution honours
every requirement as written" — and emit no questions. That is a legitimate, non-failing outcome,
not a thin result to pad.

## Notes / anti-patterns

- **A `hard` clash stays `unmet` even after acceptance.** A `hard` constraint cannot be waived,
  so the requirement is `unmet` — full stop. A human may *accept the unmet outcome as a known
  risk*, but that records a disposition; it does not relabel the flag `compromised`.
- **An orphaned requirement is itself a flag.** A compromise with no upstream outcome is surfaced
  as orphaned, never quietly filtered out to make the solution look cleaner.
- **Don't rank the compromises.** Two compromises are two equal questions; ordering them "most
  severe first" smuggles a verdict. Order by `req_key` or table appearance — no signal in order.
- **Advisory, not blocking.** A pile of `unmet` requirements hands the human contested calls; it
  never blocks the project or stops them from proceeding.
```
