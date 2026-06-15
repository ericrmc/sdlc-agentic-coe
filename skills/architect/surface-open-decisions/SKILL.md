---
name: surface-open-decisions
description: Surface the genuinely open ADR-style decisions where reasonable engineers disagree and the choice materially changes topology/cost/security/estimate; 2-3 options each with an honest buy/cost/break note; always >=1 data_placement; never pre-pick a winner.
when_to_use: identifying the contested architecture calls a project must resolve before build
output_kinds: [menu, question, halt]
deterministic_fallback: the four decision-kind buckets + the ADR template
one_liner: List the contested architecture calls a human must decide.
aliases: [open decisions, architecture decisions, ADR, decision menu, contested choices, trade-off options, key design choices, unresolved decisions]
suggested_tier: frontier
neighbours: "Usually follows architect/validate-solution-vs-requirements (the validated solution shape). Usually precedes panel/convene-a-panel (a balanced review of the design and its open calls)."
---

# surface-open-decisions

List the genuinely **OPEN** architecture choices — the ones where reasonable engineers
disagree and the answer materially changes the system. Frame each as a question with
credible options and honest trade-offs, then get out of the way so a human can choose. The
output is a menu of open decisions, not a recommendation.

## Purpose

Most "decisions" in a design doc are not decisions at all — they are settled facts written
up as choices. This skill does the opposite: it isolates the **few calls that are actually
contested** and where the contest matters.

A decision belongs on this list only if **both** are true:

1. **Reasonable engineers would disagree.** There is no obvious winner; competent people
   land on different options for defensible reasons.
2. **The choice materially changes** at least one of: **topology** (deployment shape,
   runtime model), **cost** (run-rate, build effort), **security evidence** (what must be
   proven to auditors / where regulated data lives), or **estimate** (it moves the number
   enough to matter).

If a choice fails both tests, it is an implementation detail — leave it out. This list
should be short. Three to six open decisions is a healthy project; twenty is noise.

Critically, this skill **does not pick winners**. It surfaces the question and lays out the
options even-handedly. The human ratifies the choice. Pre-picking a winner — even
implicitly, by phrasing one option more favourably — defeats the entire purpose: it
launders an opinion as analysis and robs the human of the actual decision.

## When to use

- A project brief / vision / requirements is heading toward solution architecture, and the
  contested calls need exposing **before** anyone designs around an unstated assumption.
- A design review keeps circling the same unresolved tension and it needs writing down as
  a first-class open question with options.
- An estimate is imminent and the number swings hard on a call nobody has consciously made
  yet.

Use it **early** — open decisions block downstream work. A `data_placement` decision, for
instance, drives the security-evidence story and often the whole hosting topology, so
leaving it implicit means the architecture is built on sand.

## Inputs

Supplied as markdown / free text:

- **Project title** and **description / brief / vision** — *Required.* The more concrete the
  scope, the sharper the decisions. This is the primary input. *If absent/unreadable/empty:
  HALT and ask for the project brief / vision (per `_shared/grounding.md`); never invent a
  project scope, a feature, or a regulatory regime to surface decisions over.* Readable forms:
  a markdown file, a docs folder, or a pasted brief.
- **Derived requirements, known constraints, a draft solution outline, or panel / design-review
  notes** — *Optional.* They sharpen the decisions. *If absent: proceed from the brief alone;
  never invent a requirement or constraint to manufacture a decision.*

Work **strictly within the scope the text implies.** Do not invent features, integrations,
regulatory regimes, or constraints the description does not support. If the brief never
mentions PII, still surface *where data lives* (that is always contested) — but frame it
from what the project actually handles, not from a compliance regime imagined into it. (This
is the no-fabrication keystone applied to scope — see
`skills/_contract/grounding-no-absent-input`.)

## Grounding (quoted)

This skill reasons over a project brief and (optionally) its requirements and constraints, so
it carries the no-fabrication keystone — see `skills/_contract/grounding-no-absent-input`. The
existing "work strictly within the scope the text implies; do not invent features,
integrations, regulatory regimes, or constraints" discipline is one **instance** of this
contract.

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

## The method (numbered steps)

### Step 0 — Locate / verify the required input (deterministic, pre-model)

Before drafting any decision, confirm the **project description / brief / vision** is present
as a file-level fact (absent / unreadable / empty). This is mechanical — never a judgement on
"is the brief detailed enough to find decisions in."

- **Brief absent/unreadable/empty** → emit the clean HALT below and stop. Surfacing
  "decisions" over an invented scope would launder fabrication as analysis.

```
HALT — required input missing.

I can't surface the open architecture decisions without a project brief to reason over, and
I won't invent a scope to manufacture decisions. Tell me where the brief / vision /
description lives and I'll surface the genuinely contested calls — nothing is assumed until
then.

I can read any of: a markdown file · a docs folder · the brief pasted directly here.
Which one, and where?
```

### Step 1 — Deterministic base: the four decision-kind buckets

Before drafting, hold these four `kind` buckets in mind. Every decision surfaced is
classified with **exactly one** kind from this controlled vocabulary. Reproduce these
one-line definitions verbatim — they are the load-bearing taxonomy:

- **`data_placement`** — where data (especially customer/PII) lives; residency / hosting tier
- **`architecture`** — deployment topology, runtime model, in-process vs async structure
- **`integration`** — authentication, external systems, identity, API contracts
- **`other`** — anything genuine that does not fit the three above

**ALWAYS include at least one `data_placement` decision.** Where data lives is *always*
contested and *always* drives security evidence and topology, so it is never absent from a
real project. If the brief seems to make it obvious, it has probably been under-thought —
surface the residency / hosting-tier question anyway.

Use the buckets as a coverage check: a project that surfaces only `architecture` decisions
has almost certainly missed an integration or data-placement call.

### Step 2 — Model step: draft the open decisions

Now reason as a solution architect. For each genuinely open call, draft a decision with
this discipline (this is the heart of the skill; the prompt is in
`references/draft-decisions.prompt.md` and reproduced below):

- **Frame it as an open question.** Phrase it as a question the project must answer, not as
  a statement. "Where does customer data live, and which tier owns the residency
  guarantee?" — not "Host data in region X."
- **Give it 2-3 distinct, credible options.** Each option must be one a competent team
  could actually choose. No straw men. Two is fine; three is the ceiling — four means the
  real ones have not been thought through.
- **Write an honest trade-off note per option: what it buys, what it costs, what it
  breaks.** All three, every time. An option with only upside is a tell that the menu is
  steering. The note is where even-handedness lives or dies.
- **Do NOT pre-pick a winner.** Leave every option on the table. Never imply a chosen one —
  not by ordering, not by adjectives, not by giving one option a fuller note than the
  others. The human ratifies; the menu lays out the field.
- **Classify with one `kind`** from the Step 1 vocabulary.
- **Write an `agent_rationale`** that explains *why this decision is open now, what it
  drives, and how it relates to the other decisions* (e.g. sequencing — "this must be
  settled before the integration call, because auth options depend on where identity
  lives"). The rationale **explains the decision; it is not a recommendation** of which
  option to take. If the rationale reads like an argument for one option, rewrite it.

Stay strictly within scope (see Inputs). Surface the contested few, not the settled many.

### Step 3 — The human ratifies (the lightweight ADR)

The skill stops at the menu. The human reads the options, **chooses one, and records the
choice plus their rationale** — that record *is* a lightweight Architecture Decision
Record. The ADR is just a markdown file the human writes (or appends to a decisions log),
using `references/adr.template.md`. Recording the decision and its reasoning is the whole
ceremony — no enforced disposition, no blocking step. The value is the durable "we chose X
over Y because Z", not a workflow that holds the project until someone signs off.

A good ADR captures: the question, the option chosen, the options rejected (so the road not
taken is on record), and the rationale for the call. The skill produces the menu; the
human's pen produces the decision.

## Output format

Return a **menu of open decisions** as markdown. One block per decision, in this shape:

```markdown
## Open Decisions

### D1 — Where does customer data live, and which tier owns the residency guarantee?
**kind:** data_placement

- **Single managed region, vendor-hosted** — *buys:* fastest path to live, vendor owns the
  residency evidence and patching; *costs:* run-rate per environment, less control over
  data egress; *breaks:* hard if a future client demands in-country hosting the vendor
  doesn't offer.
- **Self-hosted in an own cloud account** — *buys:* full control of region and the audit
  trail, residency story is self-owned; *costs:* the security evidence and on-call become
  self-owned; *breaks:* slower to stand up, needs platform staffing that may not exist.

**agent_rationale:** Open now because nothing in the brief fixes a residency requirement,
yet this drives the entire security-evidence story and constrains the hosting topology in
D2. Should be settled first — D2 (runtime model) and D3 (identity integration) both inherit
constraints from where data is allowed to sit.

### D2 — Synchronous request/response or async job model for the heavy processing?
**kind:** architecture

- **In-process synchronous** — *buys:* simplest topology, easy to reason about and test;
  *costs:* ties up a worker per request, caps throughput; *breaks:* under long jobs or load
  spikes — requests time out.
- **Async queue + workers** — *buys:* absorbs spikes, decouples submit from compute, scales
  workers independently; *costs:* a queue/broker to run and monitor, more moving parts;
  *breaks:* adds eventual-consistency and retry semantics the UX must handle.

**agent_rationale:** Open now because the brief implies variable, possibly heavy workloads
but doesn't fix latency expectations. Drives the estimate (async is more build) and the
topology. Depends on D1 — an async tier may need its own data-at-rest placement.
```

Keep it to the contested few. Always include at least one `data_placement` decision. Every
option carries a buys / costs / breaks note. No option is flagged as the answer.

On request, also hand over a **filled `adr.template.md`** per decision to record — but leave
the *chosen option blank* for the human to complete.

## Notes / anti-patterns

- **Pre-picking a winner.** The cardinal sin. If the menu makes the answer obvious, it is a
  recommendation, not a decision menu. Watch for it in the subtle places: option order,
  loaded adjectives ("the robust option"), or one option's note being richer than its
  rivals'. Symmetry of effort across options is the test.
- **Padding the list with settled facts.** "REST or GraphQL" is not an open decision if the
  brief already implies one and the choice changes nothing material. Apply both tests
  (disagreement *and* materiality) ruthlessly. A short, sharp list beats a long, soft one.
- **Straw-man options.** Two real options beat three where one is there to be rejected.
  Every option must be one a competent team could defensibly choose.
- **One-sided trade-off notes.** Every option buys *and* costs *and* breaks something. If
  what an option breaks cannot be named, it is not yet understood well enough.
- **Inventing scope.** Don't conjure a GDPR regime, an SSO requirement, or a third-party
  integration the brief never mentions. Surface the data-placement question from what the
  project *actually* handles.
- **Smuggling a recommendation into `agent_rationale`.** The rationale explains *why the
  decision is open and what it drives* — it argues for the *question's importance*, never
  for an *answer*. If it reads like a case for option B, rewrite it.
- **Treating this as a blocking step.** It is advisory. It produces a menu and (optionally)
  an ADR stub. It never blocks the project, enforces a disposition, or demands sign-off —
  the durable record of the human's reasoning is the entire deliverable.
```
