---
name: surface-open-decisions
description: Surface the genuinely open ADR-style decisions where reasonable engineers disagree and the choice materially changes topology/cost/security/estimate; 2-3 options each with an honest buy/cost/break note; always >=1 data_placement; never pre-pick a winner.
when_to_use: identifying the contested architecture calls a project must resolve before build
output_kinds: [menu, question]
deterministic_fallback: the four decision-kind buckets + the ADR template
suggested_tier: opus
---

# surface-open-decisions

Surface the genuinely **OPEN** architecture choices — the ones where reasonable
engineers disagree and the answer materially changes the system. Frame each as a
question with credible options and honest trade-offs, then get out of the way so a
human can choose. The output is a menu of open decisions, not a recommendation.

## Purpose

Most "decisions" in a design doc are not decisions at all — they are settled facts
written up as choices. This skill does the opposite: it isolates the **few calls that
are actually contested** and where the contest matters.

A decision belongs on this list only if **both** are true:

1. **Reasonable engineers would disagree.** There is no obvious winner; smart people
   land on different options for defensible reasons.
2. **The choice materially changes** at least one of: **topology** (deployment shape,
   runtime model), **cost** (run-rate, build effort), **security evidence** (what you
   must prove to auditors / where regulated data lives), or **estimate** (it moves the
   number enough to matter).

If a choice fails both tests, it is an implementation detail — leave it out. This list
should be short. Three to six open decisions is a healthy project; twenty is noise.

Critically, this skill **does not pick winners**. It surfaces the question and lays out
the options even-handedly. The human ratifies the choice. Pre-picking a winner — even
implicitly, by phrasing one option more favourably — defeats the entire purpose: it
launders an opinion as analysis and robs the human of the actual decision.

## When to use

- You have a project brief / vision / requirements and you are heading toward solution
  architecture, and you want to expose the contested calls **before** anyone designs
  around an unstated assumption.
- A design review or panel keeps circling the same unresolved tension and you want it
  written down as a first-class open question with options.
- You are about to estimate and you suspect the number swings hard on a call nobody has
  consciously made yet.

Use it **early** — open decisions gate downstream work. A `data_placement` decision, for
instance, gates the security-evidence story and often the whole hosting topology, so
leaving it implicit means the architecture is built on sand.

## Inputs

The user supplies, as markdown / free text:

- **Project title** and **description / brief / vision** — the more concrete the scope,
  the sharper the decisions. This is the primary input.
- Optionally: derived requirements, known constraints, a draft solution outline, or
  notes from a panel / design review.

You work **strictly within the scope the text implies.** Do not invent features,
integrations, regulatory regimes, or constraints the description does not support. If
the brief never mentions PII, you still surface *where data lives* (that is always
contested) — but you frame it from what the project actually handles, not from a
compliance regime you imagined.

## The method (numbered steps)

### Step 1 — Deterministic spine: the four decision-kind buckets

Before drafting, hold these four `kind` buckets in mind. Every decision you surface is
classified with **exactly one** kind from this controlled vocabulary. Reproduce these
one-line definitions verbatim — they are the load-bearing taxonomy:

- **`data_placement`** — where data (especially customer/PII) lives; residency / hosting tier
- **`architecture`** — deployment topology, runtime model, in-process vs async structure
- **`integration`** — authentication, external systems, identity, API contracts
- **`other`** — anything genuine that does not fit the three above

**ALWAYS include at least one `data_placement` decision.** Where data lives is *always*
contested and *always* gates security evidence and topology, so it is never absent from
a real project. If the brief seems to make it obvious, you have probably under-thought it
— surface the residency / hosting-tier question anyway.

Use the buckets as a coverage check: a project that surfaces only `architecture`
decisions has almost certainly missed an integration or data-placement call.

### Step 2 — LLM reasoning step: draft the open decisions

Now reason as a solution architect. For each genuinely open call, draft a decision with
this discipline (this is the heart of the skill; the prompt is in
`references/draft-decisions.prompt.md` and reproduced below):

- **Frame it as an open question.** Phrase it as a question the project must answer, not
  as a statement. "Where does customer data live, and which tier owns the residency
  guarantee?" — not "We will host data in region X."
- **Give it 2-3 distinct, credible options.** Each option must be one a competent team
  could actually choose. No straw men. Two is fine; three is the ceiling — if you have
  four, you have not thought hard enough about which are real.
- **Write an honest trade-off note per option: what it buys, what it costs, what it
  breaks.** All three, every time. An option with only upside is a tell that you are
  steering. The note is where even-handedness lives or dies.
- **Do NOT pre-pick a winner.** Leave every option on the table. Never imply a chosen one
  — not by ordering, not by adjectives, not by giving one option a fuller note than the
  others. The human ratifies; you lay out the field.
- **Classify with one `kind`** from the Step 1 vocabulary.
- **Write an `agent_rationale`** that explains *why this decision is open now, what it
  gates, and how it relates to the other decisions* (e.g. sequencing — "this must be
  settled before the integration call, because auth options depend on where identity
  lives"). The rationale **explains the decision; it is not a recommendation** of which
  option to take. If your rationale reads like an argument for one option, rewrite it.

Stay strictly within scope (see Inputs). Surface the contested few, not the settled many.

### Step 3 — The human ratifies (the lightweight ADR)

You stop at the menu. The human reads the options, **chooses one, and records the choice
plus their rationale** — that record *is* a lightweight Architecture Decision Record. In
this Centre-of-Excellence model the ADR is just a markdown file the human writes (or
appends to a decisions log), using `references/adr.template.md`. There is **no approval
gate, no state machine, no enforced disposition** — recording the decision and its
reasoning is the whole ceremony. The value is the durable "we chose X over Y because Z",
not a workflow that blocks until someone clicks ratify.

A good ADR captures: the question, the option chosen, the options rejected (so the road
not taken is on record), and the rationale for the call. The skill produced the menu; the
human's pen produces the decision.

## Output format

Return a **menu of open decisions** as markdown. One block per decision, in this shape:

```markdown
## Open Decisions

### D1 — Where does customer data live, and which tier owns the residency guarantee?
**kind:** data_placement

- **Single managed region, vendor-hosted** — *buys:* fastest path to live, vendor owns
  the residency evidence and patching; *costs:* run-rate per environment, less control
  over data egress; *breaks:* hard if a future client demands in-country hosting the
  vendor doesn't offer.
- **Self-hosted in our own cloud account** — *buys:* full control of region and the audit
  trail, residency story is ours to make; *costs:* we now own the security evidence and
  on-call; *breaks:* slower to stand up, needs platform staffing we may not have.

**agent_rationale:** Open now because nothing in the brief fixes a residency requirement,
yet this gates the entire security-evidence story and constrains the hosting topology in
D2. Should be settled first — D2 (runtime model) and D3 (identity integration) both
inherit constraints from where data is allowed to sit.

### D2 — Synchronous request/response or async job model for the heavy processing?
**kind:** architecture

- **In-process synchronous** — *buys:* simplest topology, easy to reason about and test;
  *costs:* ties up a worker per request, caps throughput; *breaks:* under long jobs or
  load spikes — requests time out.
- **Async queue + workers** — *buys:* absorbs spikes, decouples submit from compute,
  scales workers independently; *costs:* a queue/broker to run and monitor, more moving
  parts; *breaks:* adds eventual-consistency and retry semantics the UX must handle.

**agent_rationale:** Open now because the brief implies variable, possibly heavy
workloads but doesn't fix latency expectations. Gates the estimate (async is more build)
and the topology. Depends on D1 — an async tier may need its own data-at-rest placement.
```

Keep it to the contested few. Always include at least one `data_placement` decision.
Every option carries a buys / costs / breaks note. No option is flagged as the answer.

If the user asks, also hand them a **filled `adr.template.md`** per decision they want to
record — but leave the *chosen option blank* for them to complete.

### `references/adr.template.md`

```markdown
# ADR-<NNN>: <the open question, restated as a title>

- **Status:** Proposed | Accepted | Superseded by ADR-<NNN>
- **Date:** <YYYY-MM-DD>
- **Kind:** data_placement | architecture | integration | other
- **Deciders:** <names / roles>

## Context
<Why this decision is open now, and what it gates — drawn from the agent_rationale.
What changes downstream depending on which way this goes.>

## Options considered
| Option | Buys | Costs | Breaks |
|--------|------|-------|--------|
| <option A> | … | … | … |
| <option B> | … | … | … |

## Decision
<The option chosen. Filled in by the human, not the agent.>

## Rationale
<Why this option over the others. The road not taken stays on record above.>

## Consequences
<What now follows from this — new constraints, follow-on decisions, evidence we must produce.>
```

## Notes / anti-patterns

- **Pre-picking a winner.** The cardinal sin. If your menu makes the answer obvious, you
  have written a recommendation, not a decision menu. Watch for it in the subtle places:
  option order, loaded adjectives ("the robust option"), or one option's note being
  richer than its rivals'. Symmetry of effort across options is the test.
- **Padding the list with settled facts.** "REST or GraphQL" is not an open decision if
  the brief already implies one and the choice changes nothing material. Apply both gates
  (disagreement *and* materiality) ruthlessly. A short, sharp list beats a long, soft one.
- **Straw-man options.** Two real options beat three where one is there to be rejected.
  Every option must be one a competent team could defensibly choose.
- **One-sided trade-off notes.** Every option buys *and* costs *and* breaks something. If
  you can't name what an option breaks, you don't understand it well enough yet.
- **Inventing scope.** Don't conjure a GDPR regime, an SSO requirement, or a third-party
  integration the brief never mentions. Surface the data-placement question from what the
  project *actually* handles.
- **Smuggling a recommendation into `agent_rationale`.** The rationale explains *why the
  decision is open and what it gates* — it argues for the *question's importance*, never
  for an *answer*. If it reads like a case for option B, rewrite it.
- **Treating this as a gate.** It is advisory. It produces a menu and (optionally) an ADR
  stub. It never blocks the project, enforces a disposition, or demands sign-off — the
  durable record of the human's reasoning is the entire deliverable.
```

### `references/draft-decisions.prompt.md` (the LLM step, provider-agnostic)

You are a solution architect on a delivery team. Read the project below and surface the
genuinely OPEN decisions the project must resolve before build — the ADR-style choices
where reasonable engineers would disagree and where the choice materially changes
topology, cost, security evidence, or estimate.

Draft each decision as an open question with 2-3 distinct, credible options. Do NOT
pre-pick a winner — the human ratifies the choice, so leave every option on the table and
never imply a chosen one. Each option needs an honest trade-off note (what it buys, what
it costs, what it breaks). Stay strictly within the scope the project text implies; do not
invent features, integrations, or constraints the description does not support.

Classify every decision with one `kind` from EXACTLY this controlled vocabulary:
  - `data_placement` — where data (especially customer/PII) lives; residency / hosting tier
  - `architecture`   — deployment topology, runtime model, in-process vs async structure
  - `integration`    — authentication, external systems, identity, API contracts
  - `other`          — anything genuine that does not fit the three above

ALWAYS include at least one decision with kind `data_placement`.

Give each decision an `agent_rationale`: why it is open now, what it gates, and how it
relates to the other decisions (e.g. sequencing). The rationale explains the decision — it
is not a recommendation of which option to take.

Return a menu of decisions (markdown as shown in Output format above, or JSON of shape
`{"decisions": [{"kind", "question", "options": [{"label", "note"}], "agent_rationale"}]}`
if a downstream tool consumes it).
