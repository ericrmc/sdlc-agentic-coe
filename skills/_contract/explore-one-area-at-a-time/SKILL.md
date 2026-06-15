---
name: explore-one-area-at-a-time
description: The organising meta-method — treat a solution space as progressively-surfacing domains (lenses over one graph), dispatch a narrowly-chartered agent per area, roll depth back into one source of truth. Use it when you are exploring a large solution space, authoring multi-section work, or deciding how to fan out.
one_liner: Fan out one narrow agent per surfaced area, recombine into one truth.
aliases: [divide and conquer, break a problem into parts, work one area at a time, parallel exploration, scope the work, split a big task, focus areas, fan out and merge]
when_to_use: exploring a large solution space; authoring multi-section work; deciding how to fan out
output_kinds: [proposal, question, menu]
deterministic_fallback: the BDAT/crosscutting/lifecycle domain checklist
suggested_tier: mid
neighbours: Pair with `_contract/parallel-agents` (the execution convention for the fan-out this method shapes) and `_contract/target-rule-output-kinds` (the advisory output rule every dispatched agent obeys). It organises work that lands in `architect/synthesise-solution-architecture`.
---

# explore-one-area-at-a-time — the domain-lens fan-out meta-method

Attack a large solution space by working one surfaced area at a time, each on its own narrow agent, then
recombining all of them into a single source of truth.

This is the organising method the other skills compose with. Each other skill (derive requirements, red-team,
identify capabilities, recommend components, design review, NFRs, convene a panel, synthesise the architecture)
is *one lens* you point at the space. This skill is the rule for **which lens to pick up next, how to scope the
agent that works it, and where its output goes** so that many parallel threads still leave behind exactly one
source of truth.

If you only remember one sentence, remember this:

> **A new area surfaces → explore it on its own, narrowly scoped, told what to ignore → roll its depth back
> into the one source-of-truth document, routed by section.**

That is the move real delivery makes, and it is the move to make when exploring any non-trivial solution space.
Do not enumerate everything upfront. Surface areas progressively and work them one at a time.

---

## Purpose

Stop one generalist pass from spreading itself thin across an entire solution space. Instead, **treat the space
as a set of domains** — each a *lens over the same underlying graph of outcomes, requirements, decisions, and
NFRs*, never a new container that owns its own copy of the work — and give each surfaced domain its own
**narrowly-chartered** focused agent that goes deep on exactly that area and ignores the rest.

The payoff is depth without fragmentation: specialists produce more thorough, less shallow exploration, and
because every domain rolls its findings back into **one** sectioned source-of-truth markdown (routed by a stable
section key), the result is "many threads, one truth" instead of N parallel documents that drift apart.

## When to use

- You are **exploring a large solution space** and a single pass would be shallow or would miss whole areas.
- You are **authoring multi-section work** (a solution-design doc, an options paper, an architecture write-up)
  and need to decide who writes which section and how to keep them coherent.
- You are **deciding how to fan out** — how many agents, scoped how, and how to recombine their output.
- A new concern just **surfaced** mid-exploration ("data residency was never considered") and you want to
  spin up a focused thread for it without re-planning the whole effort.

If the task is small enough for one pass, skip this — the overhead of chartering and routing is not worth it.

## Inputs

The user (or the calling workflow) supplies:

1. **A description of the solution space** — the business vision/outcomes and any derived requirements so far.
   Even a paragraph is enough to start; areas will surface as you go.
2. **The source-of-truth document** (or the intent to create one) — the single sectioned markdown file that all
   domain depth rolls back into. If it does not exist yet, this method says how to seed its sections.
3. **(Optional) areas already known** — domains the user already wants worked, or ones a previous pass surfaced.
4. **(Optional) a concurrency budget** — how many focused agents may run at once (default: **≤ 4**).

A complete list of areas is **not** needed. Surfacing them progressively is the point.

---

## The mental model: two orthogonal axes

Hold this picture. Everything below is one of these two axes, and the whole method is keeping them straight.

```
                    THE ONE SOURCE OF TRUTH
              (a sectioned, versioned design document)
                              │
   ┌──────────────────────────┼──────────────────────────┐
   │   AUTHORSHIP axis        │        TIME axis          │
   │   WHO fleshes out each   │   HOW the design moves    │
   │   section                │   from version to version │
   │   → one narrow agent     │   → a release is a named,  │
   │     per surfaced domain, │     dated change-control   │
   │     routed by section_key│     transaction            │
   └──────────────────────────┴──────────────────────────┘
```

- **AUTHORSHIP** — *who* authors a section's depth. One narrow agent per surfaced **domain**, each routed to the
  section it feeds by a stable `section_key`. This skill is mostly about this axis.
- **TIME** — *how* the design moves forward. A **release** is a named, dated change-control transaction: a
  bounded set of adds/changes/removes against the source of truth. The two axes meet here — *a release is a
  human-named trigger that surfaces or re-activates domains, each of which authors its slice of the delta.*

The two axes are orthogonal and compose. A domain says **where in the document** depth lands; a release says
**which dated transaction** a batch of changes belongs to. Keep them separate in your head and the method stays
simple.

### A domain is a LENS, not a container

This is the load-bearing rule. **A domain does not own requirements, NFRs, or decisions** — those already exist
and already trace to outcomes. A domain is a *named scope* = (a predicate over the graph) + (a target section) +
(a chartered agent). Every artefact a domain agent produces is a normal traced row, merely *tagged* with which
domain surfaced it. The graph stays single; the domain is a queryable facet over it.

Treat this as non-negotiable. The moment a domain starts owning its own private copy of requirements, the truth
is forked and reconciliation becomes a diff between two stores instead of an additive thread into one.

### The domain families

Domains **surface progressively** and are partly project-specific — there is no fixed checklist. But there is a
reliable starting roster, the deterministic fallback you seed before any creative surfacing:

| Family | Domains | Typical target section |
|---|---|---|
| **BDAT** (architecture) | Business · Data · Application · Technology | Business → business architecture; Data/App/Tech → application/solution architecture (data-governance NFRs to quality) |
| **Crosscutting** (concerns) | Security · Integration · Operability/observability · Cost | Mostly **quality NFRs**; interfaces to application architecture; contested calls to key decisions |
| **Lifecycle** (process) | Phases · UAT · Releases · Change management | Open questions / key decisions until a release entity exists |
| **Project-specific** (emergent) | e.g. real-time pricing, data residency, tenant isolation | Author-chosen at surface time; defaults to application architecture |

Note how **four crosscutting domains all route their NFRs into one section** (quality NFRs). Domains are
**many-to-one onto sections** — that is expected and safe (handled in Step 5). Never bind a surfacing, open-ended
set of domains one-to-one to a frozen, closed set of sections.

---

## The method (numbered steps)

This preserves a **deterministic base** (seed the standard roster, route by section, cap concurrency, roll up
additively) and one explicit **LLM reasoning step** (propose the next domains + their charters as a menu).

### Step 1 — Seed the standard roster (deterministic)

Before any creative surfacing, lay down the reliable starting domains from the families table: the four **BDAT**,
the four **crosscutting**, and a **lifecycle** placeholder. Mark each `surfaced` and assign each its default
target section. This is your floor — it works with zero model creativity and guarantees you never forget security
or cost.

### Step 2 — Surface the next domains as a menu (the LLM reasoning step)

This is the one genuinely generative step. **Read the solution space and propose the domains to surface next, and
the charter for each, as a MENU** — do not silently pick. For each proposed domain, output:

- **name + family** (bdat / crosscutting / lifecycle / project-specific),
- **why it surfaced now** — *cited to real facts in the space* (an outcome, a requirement, a constraint). Never a
  hunch; if you can't cite what surfaced it, don't propose it,
- **target section** it will roll up into,
- **a one-paragraph charter** — what this agent explores **and, crucially, what it IGNORES**.

Project-specific domains are exactly the ones a fixed roster can't predict ("this project has a real-time-pricing
concern the standard list doesn't cover — surface it?"). The human (or the calling workflow) picks from the menu;
surfacing a domain is a human/workflow decision, never the agent's unilateral verdict.

### Step 3 — Charter each agent: scope IN, and scope OUT (deterministic)

For every domain you are about to work, write its **charter** before dispatching. A charter is the cure for the
generalist-spread-thin failure and the structural fix for context-starvation. It names:

- **In scope** — the slice of outcomes/requirements this agent authors against.
- **Out of scope (what to IGNORE)** — the explicit list of areas this agent must *not* wander into, because
  another domain owns them. The "ignore" list is what makes a specialist a specialist.
- **Grounding vs authoring** — the agent may *read* the whole space for context, but **authors only within its
  scope**. Full context for grounding; narrow mandate for output.

A charter without an explicit ignore-list is not a charter — it is a generalist with extra words.

### Step 4 — Dispatch, narrowly, capped (deterministic)

Dispatch **one focused agent per surfaced domain**, each given only its charter + scope slice. Constraints:

- **Cap concurrency at ≤ 4.** Surplus domains queue ("+N areas waiting"). The cap is a mechanical rate-limiter,
  not exhortation — it keeps the human's review channel from flooding.
- Each agent goes **deep on its one area** and emits **proposals / questions / cited facts — never verdicts**
  (see Step 6).
- Agents **do not duplicate cross-cutting keystone work.** There is one tracer (draws all edges), one classifier
  (tags all requirements), one validation pass — domain agents *feed* these, they don't re-implement them per
  domain.

### Step 5 — Roll up into ONE source of truth, routed by section_key (deterministic)

Each agent's depth rolls back into the single sectioned document, routed by its `section_key`. Make collisions
structurally impossible, not merely unlikely:

- **(a) Rows thread, they don't overwrite.** Every requirement/NFR/decision/roadblock a domain produces is a
  **new, additive row** traced to its parent outcome and tagged with the domain. Two domains touching the same
  outcome produce two distinct rows under it — never a merge conflict.
- **(b) Sections are generated from rows, not pasted by agents.** When several domains route to one section (the
  four crosscutting → quality NFRs), **no domain owns the section; the section owns the facts.** Regenerate the
  section by reading *all* current rows for it. Narrative contributions are merged deterministically — ordered by
  domain, each under its own sub-heading — append-only, never a clobber.
- **(c) Drift is caught, not hidden.** When a domain re-explores and its rows change, the section it feeds is now
  stale relative to what generated it. Flag it as a question — "this section was generated from data that has
  since changed; regenerate it?" — for a human to resolve. Reconciliation *is* the collision detector.

### Step 6 — Keep every output advisory (proposal / question / menu)

Domain agents emit exactly three kinds of thing, and **none of them is a verdict**:

- **proposals** — proposed requirements, NFRs, pattern signals, drafted decisions (a human accepts),
- **questions** — necessity challenges ("is this requirement actually needed?"), open questions (a human answers),
- **cited facts** — roadblocks/constraints with their evidence (a human dispositions).

This is advisory by construction. An agent produces no accepted/approved state; the human (or the downstream
review) decides. The method stays **light and advisory** — agents surface cues, a human dispositions every one.

### Step 7 — Re-surface and iterate

As a domain is worked, **new areas surface from it** ("integration raised a data-residency question worth its
own thread"). Return to Step 2, propose the newly-surfaced domains as a menu, and pull each into exploration when
the human is ready. The board of areas grows over time; the full list was never needed upfront. Retire areas
that turn out not to matter (mark them `dismissed`, with memory, so they don't re-nag against unchanged
evidence).

---

## Output format

You return **two things**: (1) a **menu of domains to surface next** with charters (Step 2's output), and (2) as
each area is worked, its **rolled-up contribution** routed to a section. Templates below.

### Template A — the surfacing menu (what you hand back for a decision)

```markdown
## Domains to surface next — pick the ones to work now (≤4 at a time)

### 1. Security  ·  crosscutting  →  rolls into: Quality NFRs
**Surfaced because:** BO-2 ("handle PII for EU customers") + REQ-14 (stores user records) imply
access-control and data-protection obligations not yet covered by any worked area.
**Charter:** Explore authn/authz, data protection at rest/in transit, audit, and secrets handling for the
PII-handling paths. Produce NFRs and at most one contested-control decision.
*Ignore:* functional behaviour, UI, cost sizing, and deployment topology — other domains own those.

### 2. Real-time pricing  ·  project-specific  →  rolls into: Application architecture
**Surfaced because:** BO-1 + REQ-3..REQ-6 all describe sub-second price updates — a coherent area the
standard roster doesn't name.
**Charter:** Explore the pricing data flow, latency budget, and staleness handling. Produce requirements,
pattern signals, and one latency NFR (routed to Quality NFRs).
*Ignore:* billing, security (Security domain owns it), and historical reporting.

### 3. Cost  ·  crosscutting  →  rolls into: Quality NFRs (+ estimate)
**Surfaced because:** real-time + multi-region (BO-3) implies a non-trivial run-cost the space hasn't sized.
**Charter:** Explore run-cost drivers and a cost-ceiling NFR; run a scoped necessity check on the most
expensive proposed requirements. *Ignore:* implementation detail and security controls.

> Queued (over the ≤4 cap): Integration, Operability, Data — surface next round.
```

### Template B — a worked domain's roll-up (routed to one section)

```markdown
## Security  →  Quality NFRs   [proposal/question/cited-fact — advisory, not a verdict]

**Proposed NFRs** (each traced to an outcome via `derives_from`, classified `nfr-kind: security`, tagged `domain: security`):
- REQ-41 ← BO-2 · All PII encrypted at rest (AES-256) and in transit (TLS 1.2+).  *(proposal)*
- REQ-42 ← BO-2 · Authn via SSO; least-privilege authz on PII read paths.         *(proposal)*

**Questions** (a human answers):
- Is full audit logging (REQ-14) required for *read* access, or only writes? Affects cost.  *(necessity)*

**Cited facts / roadblocks** (a human dispositions):
- Roadblock: EU data residency forbids storing PII in the us-east region.  Evidence: BO-2, REG-1.

**Narrative contribution** (merged under its own sub-heading when Quality NFRs is regenerated):
> Security obligations stem from EU PII handling (BO-2). The controlling NFRs are REQ-41/REQ-42; the open
> question is read-audit scope, and the binding constraint is EU residency …
```

When several domains route to the same section, present each as its own sub-block (ordered, append-only) and
regenerate the section from all of them together — never one domain overwriting another.

---

## Notes / anti-patterns

- **Don't let a domain become a container.** The first sign of going wrong: a requirement "lives in the security
  domain" instead of "is tagged security and traces to BO-2." Tags are provenance, not ownership.
- **Don't dispatch a charter without an ignore-list.** "Explore security" with no "ignore X, Y, Z" produces a
  generalist. The ignore-list is what makes the agent narrow.
- **Don't bind domains 1:1 to sections.** Four crosscutting domains share the quality-NFR section. Many-to-one is
  correct; collisions are handled by additive rows + regenerate-from-rows, not by avoiding overlap.
- **Don't exceed the concurrency cap to "go faster."** ≤4 protects the human's review channel; flooding it with
  proposals is the failure mode, not the win.
- **Don't emit verdicts.** Proposals, questions, and cited facts only. The instant an agent emits "approved" or
  "done," it has crossed the advisory line.
- **Don't enumerate everything upfront.** Surface progressively (Steps 2 and 7). Forcing a complete domain list
  before starting is the generalist trap wearing a planning hat.
- **Don't duplicate the keystone passes per domain.** One tracer, one classifier, one validation — domains feed
  them. Re-running edge-drawing inside every domain agent fragments the graph.
- **Deterministic fallback:** with no model budget for Step 2's creative surfacing, just run the
  **BDAT / crosscutting / lifecycle checklist** (Step 1's roster) with default section routing. It is shallower —
  it can't surface novel project-specific domains — but it never forgets a standard concern, and the routing and
  roll-up steps work identically.

This is the organising method behind the rest of the library. When in doubt about *how* to attack a big space:
surface one area, charter it tightly (including what to ignore), work it, roll it into the one truth by section,
and repeat — many threads, one source of truth.
