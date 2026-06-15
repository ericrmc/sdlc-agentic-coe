---
name: propose-ratify-rhythm
description: The cross-cutting rhythm every stage obeys — human supplies, agent proposes, human ratifies/edits/overrides, advance — plus accept-high/derive-low and the de-enforcement mapping. Use it when authoring any stage skill, or when you need to know how a dropped governance gate maps to plain GitHub.
when_to_use: authoring any stage skill; understanding how the dropped gates map to GitHub
output_kinds: [proposal, question]
deterministic_fallback: the rhythm diagram + the de-enforcement mapping table
suggested_tier: haiku
---

# propose-ratify-rhythm — the human-disposes authoring contract

> This is a **contract**, not a tutorial. It binds every other skill in this repo. Where a stage
> skill and this file disagree, **this file wins** — open a PR against *this* file first; do not fork
> the rhythm. It carries forward the one principle the bespoke app held *by construction* — agents
> propose, humans dispose — and re-expresses it in GitHub-native, advisory mechanics with **zero
> enforcement gates**. Read it once before authoring; cite it from every stage skill's Notes.

---

## Purpose

The original `sdlc-companion` app enforced "agents propose, humans dispose" with a database
state-machine: a `workflow_state` column, `can_advance()` predicates returning HTTP 409 on illegal
moves, version-bound governance gates, and a `governance-panel` role that alone could dispose a
check. That machinery was the *enforcement*. The business will not run a bespoke app, so we lift the
**method** out and drop the **machine**. This file is the contract that keeps the method intact once
the machine is gone:

1. The **rhythm** every stage obeys, identically.
2. The **accept-high / derive-low** rule that says *which* artefacts a human ratifies and which an
   agent may auto-derive.
3. The **de-enforcement mapping** — a one-to-one table translating each old hard gate into its new
   light, advisory form.
4. The **canonical GitHub encoding** — where "ratify" actually happens now (a human merges a PR).
5. The **anti-fatigue guardrails**, restated as mechanics so a richly agent-driven repo never
   collapses into a rubber-stamp treadmill.

This skill is **mostly deterministic**: it emits diagrams and tables, not generated prose. There is
**no model call** in its critical path — the deterministic fallback *is* the rhythm diagram plus the
de-enforcement table, and that is the whole load-bearing payload.

---

## When to use

- **Authoring any stage skill** (`intake`, `outcomes`, `requirements`, `discovery`, `solution-patterns`,
  `decisions`, `estimate`, `technical-review`, `prototype-handoff`, …). Every one of them must end
  with a *proposal a human ratifies by merging a PR* — never an auto-applied advance. Use this file
  to get that shape right and to cite it.
- **Understanding how a dropped gate maps to GitHub** — when you remember the old app blocked on a
  `HOLD`, sent a project back from governance, or gated UAT behind a role, and you need its new,
  advisory equivalent.
- **Reviewing a PR that adds a stage skill** — check the new skill against §"The five anti-patterns"
  and the mapping table. A skill that emits a *status*, *verdict*, or *auto-advance* is wrong here.

Do **not** use this to re-introduce enforcement. There is no state machine in this repo. The only
gate is a human merging a PR, and that gate is held by GitHub, not by us.

---

## Inputs (what the human / authoring agent supplies)

- The **stage** being authored (its name + the artefact it produces).
- The artefact's **altitude** — is it a genuine human commitment (an *outcome*, the *solution shape*,
  a *contested call*) or is it *derived* beneath one of those? This decides whether the human
  ratifies it or an agent auto-derives it (see ACCEPT-HIGH / DERIVE-LOW).
- The **upstream artefact** it derives from (its `derives_from` `req_key`), if any — so the citation
  link can be written.

No project data, no repository, no model call is required to apply this contract.

---

## The method (numbered steps — the deterministic spine)

### Step 1 — Obey the rhythm. The agent never crosses a ratification gate.

Every stage, without exception, runs this loop. The human supplies or asks; the agent does work and
**proposes**; the human ratifies, edits, or overrides; only *then* does the work advance. The agent's
output carries **no ratified status, no merge, no advance** — it is always a typed *proposal* or
*question*. (This is the old app's `actor='agent'` rows-only invariant, re-expressed: the agent
opens a PR; it does not merge it.)

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
                                  ADVANCE (next stage's PR can open)
```

**The invariant, stated once:** an agent's contribution is *always* an unmerged proposal. The merge
is a human act. There is no code path — and must be no skill — in which an agent merges its own
proposal or stamps its own work "ratified." If a stage skill can advance without a human merge, it is
broken; fix the skill, not this contract.

### Step 2 — ACCEPT-HIGH / DERIVE-LOW. Decide what the human ratifies vs what the agent derives.

The human's attention is the scarce resource. Spend it only on **genuine commitments**:

- **ACCEPT-HIGH (human ratifies, item-aware):** business **outcomes**, the **solution shape**
  (the adopted pattern / chosen architecture), and **contested calls** (compromises, overrides,
  send-backs-now-challenges). These are few, human-sized, and load-bearing. A human merges these.
- **DERIVE-LOW (agent derives, auto-applied beneath an accepted parent):** technical requirements,
  NFRs, classifications, sensitivity tags, acceptance criteria, estimate arithmetic. These are
  **synthesis**, not commitments. The agent applies them automatically — *but only ever threaded to
  an already-accepted upstream node.*

**The trace edge makes derive-low safe.** Every derived artefact carries a `derives_from` citation:
a `req_key` written as a **markdown link** back to the outcome (or pattern) it serves — *a link, not a
foreign key.* The chain is `business capability → outcome → requirement → pattern → decision`.

```markdown
<!-- a derived requirement, threaded to its accepted outcome -->
- **REQ-031** Encrypt all PII at rest with AES-256.
  _derives_from:_ [OUT-004 — Protect customer data to meet residency obligations](../outcomes/OUT-004.md)
```

Because the link exists, a **rejected outcome visibly orphans its entire subtree** — close the PR
that would have accepted `OUT-004`, and every `derives_from: OUT-004` requirement is now a *dangling
citation* a reconcile step surfaces as an open question. That visible orphaning is the safety net
that lets agents auto-derive without a per-item gate. **Derive-low is not a gate bypass — it is
derive-from-accepted-upstream.** No upstream acceptance, no derivation stands.

> Authoring rule: when you author a stage skill, classify its artefact as HIGH or LOW *first*. HIGH →
> the skill ends in "open a PR a human merges." LOW → the skill ends in "auto-apply, threaded by a
> `derives_from` link, no PR needed" — and the skill must emit the link.

### Step 3 — Map every dropped gate to its advisory form. (The de-enforcement table.)

This is the heart of the pivot. Each old hard mechanism becomes a *lighter* thing. Nothing that
**blocked** in the app **blocks** here — blocking becomes *detection*, disposition becomes *a human
note*, role-gates become *advisory checklists*. Read every row as: **stop doing the left thing; do
the right thing instead.**

| # | Old app mechanism (enforced) | What it did | New advisory form (GitHub-native) |
|---|---|---|---|
| 1 | **`workflow_state` advance** + `can_advance()` → 409 | A DB predicate refused illegal transitions; state was the workflow. | **A human merges the PR.** The stage advances when, and only when, a person merges. There is no state column, no 409, no predicate. The PR's existence *is* the "in review" state; its merge *is* the advance. |
| 2 | **HOLD / blocking conflict** (a contradiction parks the project) | Detected requirement conflicts and *blocked* the advance until resolved. | **Detection-only — a challenge.** An agent posts the conflict as a PR review comment or a `challenge`-kind note ("REQ-012 and REQ-019 both claim the source of truth"). It is a *cue*, dismissible in one action. It never blocks the merge. The human resolves it or accepts the tension as known. |
| 3 | **Governance disposition / send-back** (`pass` / `pass_with_conditions` / `send_back` + `route_to_state`, the only backward transition) | A panel role disposed each gate; `send_back` routed the project to an earlier state and re-armed it, version-bound. | **Dropped.** No disposition vocabulary, no send-back routing, no version-bound gate. A reviewer who wants changes **requests changes on the PR** (or opens a follow-up PR). "Route to an earlier state" is just *the next PR touches that artefact.* Conditions become **review comments**; dissent becomes a recorded note in `OPEN-QUESTIONS.md`, not a blocking disposition. |
| 4 | **Role-gated UAT / governance** (`X-Actor-Role: governance-panel` required to dispose, else 403) | A specific role alone could pass the gate; others got 403. | **A light advisory checklist.** Ship a markdown checklist (`a11y / WCAG`, security lens, NFR coverage) the PR author and reviewers tick by hand. SRE and security are **lenses a reviewer adopts**, not provisioned seats. No role is *required*; no request is *refused*. CODEOWNERS may *request* a reviewer, but absence of a tick never blocks a merge. |
| 5 | **Auto-ratify / auto-transition** (the v1 requirements by-product: state advanced as a side-effect of the last per-item action) | The system advanced itself once the last item resolved — the one implicit transition. | **A human note.** There are no implicit transitions here. Where the app would have auto-advanced, a person writes one line in the PR ("requirements complete — merging") and merges. Nothing advances as a side-effect; every advance is a visible human act. |

**One sentence to carry:** *every place the old app said "the system enforces," this repo says "a human
merges a PR" — and every place it said "blocked," this repo says "flagged, advisory, dismissible."*

### Step 4 — Encode "ratify" canonically: the PR-merge IS the ratify.

There is exactly **one** ratification mechanism in this repo, and it is a GitHub PR merge. Spell it
out so every stage skill points at the same place:

- A stage's agent work lands as a **branch + pull request**. The PR body is the proposal.
- The PR template — [`.github/pull_request_template.md`](../../../.github/pull_request_template.md) —
  prompts the human for exactly the disposition the old app captured in a row: *what is being ratified,
  what upstream `req_key` it derives from, any override/dissent, the advisory checklist ticks.*
- **Merge = ratify.** **Edit the diff and merge = ratify-with-edits** (the old "edit → new version").
  **Request changes / close = reject or override** (the old "send-back," now just "the next PR").
- The merge commit + PR thread *is* the durable record — the append-only event log, re-homed in git
  history. No separate `event` table; `git log` and the PR timeline are the audit trail.

A stage skill must therefore **end by opening a PR**, never by writing a "ratified" status anywhere.
If a skill needs to record a human decision, it records it *in the PR the human merges* — nowhere else.

### Step 5 — Restate the anti-fatigue guardrails mechanically. (No model call needed.)

A repo this agent-dense will fatigue its humans unless these mechanics hold. They are not tone; they
are testable rules. Build them into every stage skill and the validating Action:

- **Delta-since-last-green.** A review/PR shows **only what changed since the last merged (green)
  state** — never the whole artefact re-listed. The reviewer reads a diff, not a wall. (GitHub gives
  this for free: the PR diff *is* the delta. Don't defeat it by regenerating whole files.)
- **Untouched = defer.** An item a human did not act on stays **deferred / unchanged** — never
  silently accepted, never force-resolved. An unreviewed proposal simply remains an open PR. Closing
  a tab is not consent.
- **Dismissal-memory.** A dismissed cue (a closed challenge comment, a `wontfix`/`dismissed` label)
  **must not re-prompt against unchanged evidence.** The skill keys a dismissal to the evidence hash;
  it re-raises only when the underlying artefact changes. Proactivity without dismissal-memory is
  self-defeating noise.
- **No acceptance-rate metric — anywhere.** Do not surface, compute, or store an
  acceptance-rate / merge-rate / gate-pass-rate / deviation-rate, nor its inverted "zero-deviation is
  a smell" twin. A gate optimised for throughput is worse than no gate. No Action may emit one; no
  dashboard may show one. Order any human queue by **deterministic facts** (consequence class,
  upstream criticality), never by a "probably-approve" suggestion.

These four are the difference between "richly agent-driven" and "rubber-stamp treadmill." A stage
skill that re-lists everything, auto-accepts the untouched, re-nags a dismissed cue, or scores
acceptance is in breach of this contract.

---

## Output format (what the user / authoring agent gets back)

Applying this skill yields **two deterministic artefacts** (no prose generation, no model call):

1. **The rhythm diagram** (Step 1) — drop it into the stage skill's "The method" section so every
   stage shows the same loop and the same "agent opens a PR, human merges" invariant.
2. **The de-enforcement mapping row** for the gate the stage replaces — cite the relevant row(s) from
   Step 3 in the stage skill's Notes, so a reader can see *which* old hard gate this stage softened
   and into what.

A stage skill authored against this contract should end with a Notes block shaped like this:

```markdown
## Notes / contract compliance
- **Rhythm:** human supplies → agent proposes (opens a PR) → human ratifies by **merging the PR**.
  The agent never merges. (See `_contract/propose-ratify-rhythm`, Step 1.)
- **Altitude:** this stage produces a *<HIGH commitment | LOW derived>* artefact. <If HIGH:> a human
  merges it. <If LOW:> it auto-applies, threaded by a `derives_from` link to <upstream req_key>; no PR.
- **De-enforcement:** replaces the old *<state advance | HOLD | governance disposition | role-gated
  UAT | auto-transition>* (mapping table row <#>) with *<a human merge | a detection-only challenge |
  a review comment | an advisory checklist | a human note>*.
- **Anti-fatigue:** shows only the delta-since-last-green; untouched = defer; dismissals are
  remembered against the evidence hash; **no acceptance-rate metric is emitted.**
```

That block is the **deterministic fallback** — if no model is available, copy it verbatim, fill the
angle-bracket slots from the stage's altitude classification (Step 2), and the contract is satisfied.

---

## Notes / anti-patterns

**The five anti-patterns** — reject any stage skill that does one of these:

1. **The self-merging agent.** An agent that stamps its own work "ratified," merges its own PR, or
   advances a stage without a human. The agent *only ever opens* the PR. (Breaks Step 1.)
2. **The orphan-blind derivation.** A derived (LOW) artefact emitted *without* a `derives_from`
   markdown link, or one threaded to an outcome that was never accepted. Derive-low is only safe
   *because* the link exists and a rejected parent visibly orphans the child. (Breaks Step 2.)
3. **The smuggled gate.** Re-introducing a `workflow_state`, a 409-style block, a HOLD, a
   `send_back` disposition, or a required role that *refuses* an action. We dropped these on purpose.
   Detection is allowed; blocking is not. (Breaks Step 3.)
4. **The verdict.** An agent emitting a *status*, *colour*, *ranking*, *feasibility verdict*,
   *recommended disposition*, or *assessment of a person*. Agent output is only ever **proposal,
   question, menu, or halt.** A pre-sorted "probably-approve" queue *is* a verdict — it scripts the
   gate. (Breaks Step 3 + Step 5.)
5. **The treadmill.** Re-listing whole artefacts instead of the delta, auto-accepting the untouched,
   re-nagging a dismissed cue, or surfacing an acceptance-rate. This is the exact fatigue failure the
   whole method exists to prevent. (Breaks Step 5.)

**On "send-back" specifically:** people will ask "but how do I send a project back to an earlier
stage?" The honest answer is *you don't route it — you open the next PR against the earlier
artefact.* There is no backward transition because there is no transition at all; there is only the
next human-merged change. A compromise, an override, or a piece of dissent is recorded as a note in
the PR and surfaced first in the handoff's `OPEN-QUESTIONS.md` — visible, not enforced.

**On the panel / governance role:** the old app's `governance-panel` was the *only* actor who could
dispose a gate. Here, governance is a **lens any reviewer adopts** and an **advisory checklist**, and
the "gate" is the same PR merge everyone else uses. Do not re-create a privileged disposing role; it
turns "reviewed" back into a blocking checkbox.

**Provider-agnostic.** Nothing here calls a specific model or runs only in one tool. The rhythm
diagram, the trace-link convention, the mapping table, and the guardrails are plain markdown +
GitHub mechanics — runnable in Claude Code, any LLM workflow that reads markdown, or by a human with
no agent at all. The contract holds whether or not a model is in the loop, because the load-bearing
gate is always a human merging a PR.
