---
name: propose-ratify-rhythm
description: The cross-cutting rhythm every skill obeys — a human supplies, an agent proposes, a human ratifies/edits/overrides, then the work advances — plus the accept-high/derive-low rule for what a human ratifies versus what an agent may auto-derive. Use it when authoring any skill, or to decide where ratification happens.
when_to_use: authoring or reviewing any skill; deciding what a human ratifies versus what an agent auto-derives
one_liner: A human proposes-then-ratifies rhythm every skill obeys.
aliases: [propose then ratify, human in the loop, who signs off, approval rhythm, accept high derive low, PR merge is the sign-off, agent proposes human disposes]
output_kinds: [proposal, question]
deterministic_fallback: the rhythm diagram + the accept-high/derive-low rule + the contract-compliance Notes block
suggested_tier: light
tier_reason: convention doc — no weighing, no model call in its critical path
neighbours:
  before: skills/_contract/target-rule-output-kinds (the four output kinds this rhythm carries)
  after: skills/MAP.md (where a human PR merge is named as the one ratify step)
---

# propose-ratify-rhythm — the authoring contract

Define the one rhythm every skill in this library follows: a human supplies, an agent proposes, a human ratifies, then the work advances. This is a **contract**, not a tutorial — it binds every other skill. Where a skill and this file disagree, this file wins; open a PR against this file rather than forking the rhythm. Read it once before authoring, and cite it from each skill's Notes.

It is **mostly deterministic**: it emits a diagram and tables, not generated prose. There is no model call in its critical path — the deterministic fallback is the rhythm diagram plus the accept-high/derive-low rule, and that is the whole load-bearing payload.

## Purpose

This contract keeps one principle intact across a richly agent-driven library: **agents propose, humans dispose.** It states four things plainly:

1. The **rhythm** every skill obeys, identically.
2. The **accept-high / derive-low** rule — which artefacts a human ratifies, and which an agent may auto-derive.
3. The **canonical encoding** — where "ratify" actually happens: a human merges a pull request.
4. The **anti-fatigue guardrails**, stated as mechanics so an agent-dense repo never collapses into a rubber-stamp treadmill.

## When to use

- **Authoring any skill.** Every skill must end with a *proposal a human ratifies by merging a PR* — never an auto-applied advance. Use this file to get that shape right and to cite it.
- **Deciding what a human ratifies versus what an agent derives.** Classify the skill's artefact as a genuine commitment (HIGH) or a synthesis beneath one (LOW). See accept-high / derive-low below.
- **Reviewing a PR that adds a skill.** Check it against the five anti-patterns. A skill that emits a *status*, *verdict*, or *auto-advance* is wrong here.

Do not use this to introduce enforcement. The only ratification gate is a human merging a PR, and that gate is held by the code host, not by any skill.

## Inputs (what the human or authoring agent supplies)

- The **skill** being authored — its name and the artefact it produces.
- The artefact's **altitude** — is it a genuine human commitment (an *outcome*, the *solution shape*, a *contested call*) or is it *derived* beneath one of those? This decides whether a human ratifies it or an agent auto-derives it.
- The **upstream artefact** it derives from (its `req_key`), if any — so the citation link can be written.

No project data, no repository, and no model call is required to apply this contract.

## The method (numbered steps — the deterministic base)

### Step 1 — Obey the rhythm. The agent never crosses a ratification gate.

Every skill, without exception, runs this loop. The human supplies or asks; the agent does work and **proposes**; the human ratifies, edits, or overrides; only then does the work advance. The agent's output carries **no ratified status, no merge, no advance** — it is always a typed *proposal* or *question*. The agent opens a PR; it does not merge it.

```
   ┌─────────────┐   supplies / asks         ┌──────────────────────────────┐
   │   HUMAN      │ ───────────────────────► │  AGENT does work + PROPOSES   │
   │  (supplies)  │                          │  → a typed proposal/question  │
   └─────────────┘                           │  → opens a PR (NEVER merges)  │
         ▲                                    └───────────────┬──────────────┘
         │                                                    │
         │  ratifies / EDITS / OVERRIDES                      │  proposal sits in the PR,
         │  (the human merges, edits, or                      │  awaiting a human
         │   closes the PR)                                   ▼
   ┌─────┴──────────────────────────────────────────────────────────────────┐
   │  HUMAN DISPOSES — merge = ratify · edit = amend the diff · close = reject │
   │            ── the ONLY thing that advances the work ──                    │
   └──────────────────────────────────┬───────────────────────────────────────┘
                                       │  on merge
                                       ▼
                                  ADVANCE (the next skill's PR can open)
```

**The invariant, stated once:** an agent's contribution is *always* an unmerged proposal. The merge is a human act. There is no skill in which an agent merges its own proposal or stamps its own work "ratified." If a skill can advance without a human merge, it is broken; fix the skill, not this contract.

### Step 2 — ACCEPT-HIGH / DERIVE-LOW. Decide what the human ratifies vs what the agent derives.

The human's attention is the scarce resource. Spend it only on **genuine commitments**:

- **ACCEPT-HIGH (human ratifies, item-aware):** business **outcomes**, the **solution shape** (the adopted pattern / chosen architecture), and **contested calls** (compromises, overrides, challenges). These are few, human-sized, and load-bearing. A human merges these.
- **DERIVE-LOW (agent derives, auto-applied beneath an accepted parent):** technical requirements, NFRs, classifications, sensitivity tags, acceptance criteria, estimate arithmetic. These are **synthesis**, not commitments. The agent applies them automatically — but only ever threaded to an already-accepted upstream node.

**The trace edge makes derive-low safe.** Every derived artefact carries a `derives_from` citation: a `req_key` written as a **markdown link** back to the outcome (or pattern) it serves — a link, not a foreign key. The chain is `business capability → outcome → requirement → pattern → decision`.

```markdown
<!-- a derived requirement, threaded to its accepted outcome -->
- **REQ-031** Encrypt all PII at rest with AES-256.
  _derives_from:_ [BO-004 — Protect customer data to meet residency obligations](../outcomes/BO-004.md)
```

Because the link exists, a **rejected outcome visibly orphans its entire subtree** — close the PR that would have accepted `BO-004`, and every `derives_from: BO-004` requirement is now a *dangling citation* a reconcile step surfaces as an open question. That visible orphaning is the safety net that lets agents auto-derive without a per-item check. **Derive-low is not a bypass — it is derive-from-accepted-upstream.** No upstream acceptance, no derivation stands.

> Authoring rule: classify the artefact as HIGH or LOW *first*. HIGH → the skill ends in "open a PR a human merges." LOW → the skill ends in "auto-apply, threaded by a `derives_from` link, no PR needed" — and the skill must emit the link.

### Step 3 — Encode "ratify" canonically: the PR merge IS the ratify.

There is exactly **one** ratification mechanism in this library, and it is a pull-request merge. Spell it out so every skill points at the same place:

- A skill's agent work lands as a **branch + pull request**. The PR body is the proposal.
- The PR template — [`.github/pull_request_template.md`](../../../.github/pull_request_template.md) — prompts the human for exactly the disposition to capture: *what is being ratified, what upstream `req_key` it derives from, any override or dissent, the advisory checklist ticks.*
- **Merge = ratify.** **Edit the diff and merge = ratify-with-edits.** **Request changes / close = reject or override** — there is no separate "send back" mechanism; the next change is simply the next PR against that artefact.
- The merge commit + PR thread *is* the durable record — an append-only event log living in version-control history. There is no separate event store; the commit log and the PR timeline are the audit trail.

A skill must therefore **end by opening a PR**, never by writing a "ratified" status anywhere. If a skill needs to record a human decision, it records it *in the PR the human merges* — nowhere else.

### Step 4 — Hold the anti-fatigue guardrails mechanically. (No model call needed.)

An agent-dense repo will fatigue its humans unless these mechanics hold. They are testable rules, not tone. Build them into every skill and the validating check:

- **Delta-since-last-merged.** A review or PR shows **only what changed since the last merged state** — never the whole artefact re-listed. The reviewer reads a diff, not a wall. (The code host gives this for free: the PR diff *is* the delta. Do not defeat it by regenerating whole files.)
- **Untouched = defer.** An item a human did not act on stays **deferred / unchanged** — never silently accepted, never force-resolved. An unreviewed proposal simply remains an open PR. Closing a tab is not consent.
- **Dismissal-memory.** A dismissed cue (a closed comment, a `wontfix` / `dismissed` label) **must not re-prompt against unchanged evidence.** Key a dismissal to the evidence hash; re-raise only when the underlying artefact changes. Proactivity without dismissal-memory is self-defeating noise.
- **No acceptance-rate metric — anywhere.** Do not surface, compute, or store an acceptance-rate / merge-rate / pass-rate / deviation-rate, nor its inverted "zero-deviation is a smell" twin. A check optimised for throughput is worse than none. Order any human queue by **deterministic facts** (consequence class, upstream criticality), never by a "probably-approve" suggestion.

These four are the difference between "richly agent-driven" and "rubber-stamp treadmill." A skill that re-lists everything, auto-accepts the untouched, re-nags a dismissed cue, or scores acceptance is in breach of this contract.

## Output format (what the authoring agent gets back)

Applying this skill yields **two deterministic artefacts** (no prose generation, no model call):

1. **The rhythm diagram** (Step 1) — drop it into the skill's "The method" section so every skill shows the same loop and the same "agent opens a PR, human merges" invariant.
2. **A contract-compliance Notes block** — cite which altitude the skill produces and which guardrails apply.

A skill authored against this contract should end with a Notes block shaped like this:

```markdown
## Notes / contract compliance
- **Rhythm:** human supplies → agent proposes (opens a PR) → human ratifies by **merging the PR**.
  The agent never merges. (See `skills/_contract/propose-ratify-rhythm`, Step 1.)
- **Altitude:** this skill produces a *<HIGH commitment | LOW derived>* artefact. <If HIGH:> a human
  merges it. <If LOW:> it auto-applies, threaded by a `derives_from` link to <upstream req_key>; no PR.
- **Anti-fatigue:** shows only the delta-since-last-merged; untouched = defer; dismissals are
  remembered against the evidence hash; **no acceptance-rate metric is emitted.**
```

That block is the **deterministic fallback** — if no model is available, copy it verbatim, fill the angle-bracket slots from the skill's altitude classification (Step 2), and the contract is satisfied.

## Notes / anti-patterns

**The five anti-patterns** — reject any skill that does one of these:

1. **The self-merging agent.** An agent that stamps its own work "ratified," merges its own PR, or advances without a human. The agent *only ever opens* the PR. (Breaks Step 1.)
2. **The orphan-blind derivation.** A derived (LOW) artefact emitted *without* a `derives_from` markdown link, or one threaded to an outcome that was never accepted. Derive-low is only safe *because* the link exists and a rejected parent visibly orphans the child. (Breaks Step 2.)
3. **The smuggled block.** Re-introducing a status that *refuses* an action, a required role that blocks a merge, or any persisted state that must flip before work can advance. Detection is allowed; blocking is not. A reviewer who wants changes requests them on the PR. (Breaks Step 3.)
4. **The verdict.** An agent emitting a *status*, *colour*, *ranking*, *feasibility verdict*, *recommended disposition*, or *assessment of a person*. Agent output is only ever **proposal, question, menu, or halt.** A pre-sorted "probably-approve" queue *is* a verdict — it scripts the decision. (Breaks Step 3 + Step 4.)
5. **The treadmill.** Re-listing whole artefacts instead of the delta, auto-accepting the untouched, re-nagging a dismissed cue, or surfacing an acceptance-rate. This is the exact fatigue failure the method exists to prevent. (Breaks Step 4.)

**On sending work backward:** people ask "how do I send a project back to an earlier point?" The answer is *you open the next PR against the earlier artefact.* There is no backward transition because there is no transition at all; there is only the next human-merged change. A compromise, an override, or a piece of dissent is recorded as a note in the PR and surfaced in the handoff's open-questions record — visible, not enforced.

**On governance:** governance is a **lens any reviewer adopts** and an **advisory checklist**, and the ratify point is the same PR merge everyone else uses. Do not create a privileged disposing role; it turns "reviewed" back into a blocking checkbox. A human architect must still review every component-pattern and capability change — that CODEOWNERS review is the one structural human gate, a present go/no-go decision point, not an automated block.

**Provider-agnostic.** Nothing here calls a specific model or runs only in one tool. The rhythm diagram, the trace-link convention, and the guardrails are plain markdown plus code-host mechanics — runnable in any agent harness, any LLM workflow that reads markdown, or by a human with no agent at all. The contract holds whether or not a model is in the loop, because the load-bearing gate is always a human merging a PR.
