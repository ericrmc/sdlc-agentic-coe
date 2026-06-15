---
name: target-rule-output-kinds
description: The cross-cutting rule that keeps the library advisory by construction — every skill output is proposal|question|menu|halt, never a verdict; and the spec the CI linter enforces.
one_liner: Every agent output is proposal, question, menu, or halt — never a verdict.
aliases: [advisory output rule, no verdicts, output types, proposal not decision, agent must not decide, keep it advisory, output kinds, allowed agent outputs]
when_to_use: authoring or reviewing any skill or pattern; deciding what shape an agent output may take
output_kinds: [proposal, question]
deterministic_fallback: the four-kind enum + the forbidden-output list as a checklist
suggested_tier: light
neighbours: Pairs with `_contract/propose-ratify-rhythm` (the human ratifies what these outputs propose). Every authored skill picks its `output_kinds:` from this rule. Indexed in `skills/MAP.md`.
---

# target-rule-output-kinds — the lintable advisory invariant

> This is a **convention doc**, not a procedure. It has no model step. Its whole content is the `deterministic_fallback`: read the rule, check the output against the four-kind enum and the forbidden-output catalogue, ship. It is also the **specification** that the skill-frontmatter linter enforces on every PR.

## Purpose

Keep every agent output advisory by construction, so the library can automate aggressively without ever rubber-stamping a human decision.

The library is advisory: nothing an agent emits blocks a downstream project from moving. The one invariant that makes this safe instead of reckless is that **every agent output stays advisory by construction.** An advisory library cannot rubber-stamp, cannot mislabel a machine guess as a human ruling, and cannot let a cheap model's confidence leak out as authority — because the *shape* of what an agent is allowed to emit forbids it.

That shape is the TARGET RULE. This file states it once, quotably, and makes it lintable.

## When to use

- Authoring **any** `SKILL.md`: pick the `output_kinds:` from the closed set below.
- Authoring **any** pattern: confirm the frontmatter carries no agent-set `approval_status`.
- Reviewing a PR: this is the checklist a human (and the linter) runs against the change.

## The rule, stated once

> **Every agent output is exactly one of `proposal` | `question` | `menu` | `halt`.**
> **Never a status, a verdict, a colour, a ranking, a queue disposition, a feasibility status, a score, or an assessment of a person.**
> **Agents target the MODEL, the RECORD, or the BLIND SPOT — never the JUDGMENT.**

The three legal targets:

- **MODEL** — keep a cheap model on rails (decompose, classify, structure, trace).
- **RECORD** — structure something for defensibility and reuse (assemble a bundle, retrieve a pattern, narrate a cited fact).
- **BLIND SPOT** — coverage and de-biasing rituals (surface a conflict, name an adjacency, ask "which assumption gives?").

The one illegal target:

- **JUDGMENT** — the human's call. Whether it's good enough, whether it's feasible, whether it's approved, who's at fault, what colour the project is, what ranks first. The agent **never** touches this. It hands the human a typed thing to rule on.

### The four legal kinds

| Kind | What it is | What it must never smuggle |
|---|---|---|
| `proposal` | "Here is a derived/structured thing; accept, edit, or reject it." | A claim that it is already decided, validated, or approved. |
| `question` | "Here are two ids and the assumption beneath their tension — which gives?" | A built-in answer ("these conflict / this is weak / this is gold-plated"). |
| `menu` | "Here are N un-ranked, equal options; 'do nothing' is always one." | An order that implies a recommendation; a marked favourite. |
| `halt` | "This needs a human decision; I stop and wait." | A disposition for the human to rubber-stamp. |

## Why an advisory library is safe without a blocking mechanism

The classic fear: *if nothing blocks, an agent's mistake flows straight into the design as fact.* The TARGET RULE dissolves that fear without adding a blocking mechanism.

**Auto-derivation stays safe because every derived row remains a typed `proposal` threaded to an accepted upstream node.** When a skill derives technical requirements from a business outcome, or flows a pattern's attached NFRs into a project, those rows are not *facts the agent asserted* — they are *proposals against an upstream the human already accepted*. The trace edge (`derives_from`) is load-bearing: reject the upstream outcome and its entire derived subtree visibly orphans. This is the **derive-from-accepted-upstream** move. The human accepts the few genuine commitments (business outcomes, the solution shape, the contested calls); agents derive and auto-apply everything beneath — and everything beneath is structurally a proposal, never a ruling.

The result is rich, aggressive, fan-out automation **and** an advisory guarantee at the same time. The guarantee lives in the *type* of the output, checkable at author time and at PR time.

## The lintable frontmatter contract

Two clauses, both mechanically checkable:

1. **Every `SKILL.md` declares `output_kinds:`**, and every value is drawn **only** from the closed set:

   ```yaml
   output_kinds: [proposal, question, menu, halt]   # any subset; nothing else is legal
   ```

   A skill that declares `output_kinds: [verdict]`, `[status]`, `[score]`, `[ranking]`, `[recommendation]`, `[rag]`, or any token outside the four fails the lint. (`recommendation` is the most seductive smuggler — see below.)

2. **No pattern frontmatter may carry an agent-set `approval_status`.** A pattern's lifecycle is human-owned and lives in PR-reviewed fields — `approval_status` (`candidate|provisional|approved|deprecated`), `approved_by`, `approved_at`, `valid_from`, `validity_check_months`, `sunset_at`, `superseded_by`. An agent never writes any of those. If a generated/proposed pattern arrives with an `approval_status:` key, or with `approved_by:` pointing at an agent, the lint fails. Validity is a human ratification with evidence attached, not a field a model sets.

## The forbidden-output catalogue

Concrete examples of what a skill must **never** emit. Each is a JUDGMENT wearing one of the four kinds as a costume.

- **A RAG colour / health verdict.** ❌ "Project status: 🔴 Red." A colour *is* a verdict. The legal move is a `menu` of cited facts ("3 outcomes unserved, 1 compromise unresolved") and let the human read the colour. Derive-on-read facts are fine; the colour is not.
- **A feasibility status.** ❌ "Option B: **infeasible**." / ❌ "This is feasible." The agent enumerates and **cites the roadblocks an option hits** (`proposal`); the *feasibility disposition* — "spike-agreed", "accepted-as-grey", "resolved-direction" — is human-owned. An agent-proposed feasibility status is a recommendation in disguise and is forbidden.
- **A ranking presented as a recommendation.** ❌ A "menu" of 4 architectures sorted best-first, or with one starred. A real `menu` is **un-ranked and equal** — alphabetical codenames so order carries no signal, "do nothing" always present as a first-class column. The moment order implies preference, it's a verdict.
- **A conflict assertion.** ❌ "Requirements R3 and R7 **conflict**." / ❌ "R3 is **weak**." The legal `question` names *both ids* and the *assumption beneath* and asks **"which assumption gives?"** — it never adjudicates. The channel width is the discipline: a critic that asserts conflicts ships spurious ones; a critic that surfaces the tension and asks does not.
- **A necessity verdict.** ❌ "Redis is **gold-plated**." The legal `question` names the component, the outcome, and the already-satisfied NFR, and asks "necessary, or cut?" The flag is computed; the human rules. Zero cuts is a legitimate outcome.
- **A score.** ❌ "Similarity: **0.87**." / ❌ "Quality score: 7/10." A retrieval *tool* computes similarity from real rows; the skill **narrates** it into a `proposal` and never emits the bare number as if it were the answer.
- **A queue disposition.** ❌ "Moved to **probably-approve** lane." Assemble and order the delta by deterministic consequence class; never pre-dispose it. No recommended-disposition lane.
- **An assessment of a person.** ❌ "The author missed the security concern." Lenses flag missing **concerns**, never missing **people**. Target the blind spot, never the human.

If an output reads like a decision someone could rubber-stamp, it has targeted the JUDGMENT. Reshape it into a `proposal` (a typed thing to accept/edit/reject), a `question` (a tension to rule on), a `menu` (equal options to choose among), or a `halt` (stop and wait) — and hand the call to the human.

## This skill is the spec

This document is the authoritative specification for two enforcement points. Both are **advisory CI** — they comment and fail the check to prompt a human fix; neither blocks a downstream project:

- **The skill-target-rule linter** — parses every `SKILL.md` frontmatter, asserts `output_kinds:` ⊆ `{proposal, question, menu, halt}`, and greps the body for forbidden-output tells (a literal RAG colour, "feasible/infeasible" as a status, a starred/ranked menu). Asserts no pattern frontmatter carries an agent-set `approval_status` or an agent in `approved_by`.
- **The skill-frontmatter validation check** — runs that linter on PR. A failure is a review signal for a human: the linter catches the *shape* violation; a human still owns the call.

The closed enum and the forbidden catalogue above are the contract. Change them here first; the linter and the CI check follow this file.

## Notes / anti-patterns

- **`recommendation` is not a fifth kind.** It is the most common smuggled verdict. If you feel the urge to "recommend," emit an un-ranked `menu` plus cited `proposal` facts and let the human recommend to themselves.
- **Don't proceduralise the calls the rule protects.** These are never an agent output: feasibility dispositions, evidence sufficiency, source credibility, stakeholder/political reads, RAG verdicts, the agenda, scope/exit/ethics calls, option selection, when to stop investigating, and when to break the procedure itself.
- **A zero-output review is success, not failure.** A critic that surfaces no accepted notes, a necessity check with zero cuts, an empty open-questions file — all legitimate, non-failing outcomes. Padding to look busy is itself a forbidden output.
- **Deterministic predicates are fine; readiness *verdicts* are not.** "≥40 words AND a 600ms settle" is a tripwire, not a judgment. "This looks ready" is a verdict. An agent never fires because it "feels ready."
- **The rule is for the builders, not the end user.** Naming output kinds is how the library stays honest; the person using a skill just experiences a calm collaborator that proposes, asks, offers, and occasionally stops to let them decide.
