---
name: recommend-component-patterns
description: Read project context plus the approved pattern library files and recommend only genuine fits (a small defensible set, or none); never invent pattern_keys; honest-empty routes to surface-solution-options.
one_liner: Match project needs to proven library patterns, or honestly none.
aliases: [pick a pattern, reuse architecture, find a proven design, what has worked before, off-the-shelf solution, recommend a tech stack, match requirements to components, reference architecture lookup]
when_to_use: Choosing a solution shape. The fastest route to a governed design is adopting an already-approved pattern — so before architecting anything custom, check what has already been built and validated.
output_kinds: [proposal, menu, halt]
deterministic_fallback: Read the pattern files directly and match on category / topology / data_placement keywords; present the candidates, recommend none if nothing fits.
suggested_tier: frontier
tier_reason: Capability resolution plus proven-vs-candidate judgement is high-stakes and shapes a human design commitment.
neighbours: Usually follows challenge/necessity-check (is this component even needed?). When nothing in the library fits, hands off to architect/surface-solution-options.
---

# recommend-component-patterns

Match a project's needs to the proven component patterns that genuinely fit — a
small, defensible shortlist a human accepts, overrides, or rejects — or honestly
recommend none and route to exploration.

The project already has business outcomes, derived requirements, attached NFRs,
and a sense of its deployment topology and data placement. The job here is **not**
to invent an architecture. It is to **retrieve** the patterns from the approved
library that genuinely fit, and hand a human a short, defensible shortlist.

> Retrieval, not generation. Every pattern named must already exist in
> `patterns/` — proven, PR-reviewed, evidence-backed, in date. This step retrieves
> and judges; it does not author new patterns.

## Purpose

From the approved component pattern library, recommend the patterns that
**genuinely fit** this project's domain, deployment constraints, and
data-placement needs.

This step recommends. A human accepts, overrides, or rejects each one. Nothing
here blocks — it is advisory. The value is that adopting an approved pattern is
the fastest route to a governed design: the pattern already carries its validated
NFRs, its evidence of having been built, and its caveats. Reuse beats invention.

If nothing in the library fits, that is a real and useful answer. Say so, and
route the project to exploration (`architect/surface-solution-options`) rather
than forcing a bad match.

## When to use

- A project's context is in hand (outcomes, requirements, NFRs, rough topology
  and data-placement intent) and a solution shape must be chosen.
- The goal is to know what has **already been validated and built** before
  committing to anything custom.
- A solution architecture is about to be written and a governed starting point is
  wanted instead of a blank page.

Do **not** use this to design a new pattern. If the fit is genuinely empty, that
is `architect/surface-solution-options`' job, and a newly-invented shape should
later be captured as a *candidate* pattern through the PR-reviewed contribution
flow — not minted here on the fly.

## Inputs

The user supplies (as markdown / context):

1. **Project context** — *Required.* Title, description, and the relevant
   downstream artefacts: derived requirements, attached NFRs, and any stated
   deployment topology and data-placement constraints (e.g. "in-region only",
   "on-prem mandated by client contract", "PII must not leave the regional
   boundary"). *If absent/unreadable/empty: HALT and ask where it is (per
   `_shared/grounding.md`); never invent a requirement, NFR, or constraint to
   match against.* Readable forms: a markdown file, an xlsx/csv path, a GitHub
   Project owner+number, a docs folder, or a pasted block.
2. **The pattern library** — *Required.* The files under `patterns/`. The LLM
   reads these `.md` files **directly**; each has YAML frontmatter (`pattern_key`,
   `name`, `category`, `intent`, `deployment_topology`, `data_placement`,
   `approval_status`, `attached_nfrs`, `valid_from`, `validity_check_months`,
   `sunset_at`, `evidence`, etc. — see `patterns/_schema/pattern.frontmatter.schema.json`)
   and a body (Summary, When to use / when NOT to, Attached NFRs, Trade-offs).
   *If `patterns/` is absent/unreadable: HALT and ask where the library is (per
   `_shared/grounding.md`); never invent a `pattern_key`. An empty-but-readable
   `patterns/` is **not** a halt — it is the honest-empty route (STEP 4): nothing
   to recommend, route to exploration.*
3. **The capability index** — *Optional.* `capabilities/INDEX.md`, an alias-keyed
   lookup that resolves a plain-language need (e.g. "data warehouse", "run our
   agents in prod") to a canonical capability and its fulfilment state. *If
   absent: proceed against the raw pattern library (STEP 1); the index is a fast
   path, not a gate — never invent a `CAP-` key to stand in for it.*

No database, vector index, or network call is needed. The pattern files are the
library.

## Grounding (quoted)

This skill reads or writes a requirement, so it carries the no-fabrication keystone —
see the contract `skills/_contract/grounding-no-absent-input`. The "never invent a
`pattern_key`" rule throughout this skill (it appears in the description, STEP 1, STEP 2,
and the anti-patterns) is one **instance** of this contract, not a separate rule.

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

## The method — STEPS

### STEP 0 (DETERMINISTIC) — Locate / verify the required inputs (pre-model)

Before any reasoning, confirm the two Required inputs are present as a file-level fact:
the **project context** (something to match against) and the **pattern library**
(`patterns/`, the set of legal `pattern_key`s). This is mechanical — absent / unreadable /
empty — never a model judgement on "is this enough to work with."

- **Project context absent/unreadable/empty** → emit the clean HALT below and stop.
- **`patterns/` absent/unreadable** → HALT and ask where the library lives.
- **`patterns/` present but empty** (zero pattern files) → this is **not** a halt; it is
  the honest-empty route — go straight to STEP 4 and route to exploration.

```
HALT — required input missing.

I can't recommend patterns without the project context to match against, and I won't
invent requirements or constraints to stand in for it. Tell me where the project's
outcomes / requirements / NFRs / topology + data-placement constraints live and I'll
read them and recommend genuine fits — nothing is assumed until then.

I can read any of: a markdown file · an xlsx/csv path · a GitHub Project (owner + number)
· a docs folder · the rows pasted directly here. Which one, and where?
```

With both Required inputs present, proceed to resolve the need to a capability.

### STEP 0a (DETERMINISTIC) — Resolve the need to a capability

Before scanning patterns, resolve what the project actually needs into a named
capability. Read `capabilities/INDEX.md` and match the project's stated need
against the alias column (a non-expert phrasing like "transactional database" or
"agent hosting" resolves to a canonical `CAP-` key). Each capability records its
fulfilment state:

- **Proven fulfilment** — the capability names a `PAT-` pattern that has been
  proven against its governance floor. Carry that `pattern_key` into STEP 1 as a
  strong candidate.
- **OPEN (candidate-only)** — the capability has no proven pattern, only
  candidate components with open questions (spikes owed). There is no real
  `pattern_key` to recommend yet. This is the honest-empty signal early: name the
  capability, surface its candidates and open questions, and route to
  `architect/surface-solution-options` (see STEP 4). Do **not** mint a pattern.

If the need does not resolve to any capability in the index, proceed to STEP 1 on
the raw pattern library — the index is a fast path, not a gate.

> **Multi-agent option (advisory).** This step deepens with independent parallel
> agents: launch one sub-agent per candidate, at most 4 at a time, each a separate
> sub-agent. A failed sub-agent returns nothing and is never fatal — the
> deterministic base stands; merge what succeeded. (Claude Code: use the Task tool
> / subagents. Other tools: launch parallel model calls; or a matrix-strategy CI
> job.) Never required — it adds coverage and cuts single-pass bias. See
> `skills/_contract/parallel-agents`.

For a capability that is OPEN with several candidate components, fan out one agent
per candidate to probe its open questions in parallel, then synthesise a
per-candidate proven|still-candidate read for a human to ratify — preserving any
dissent on lock-in.

### STEP 1 (DETERMINISTIC) — Load and present the candidate `patterns_block`

Read the files under `patterns/`. For each pattern, extract from its frontmatter
and build **one line** in this exact shape:

```
pattern_key | name | category | deployment_topology | data_placement — one-line summary
```

Concatenate these into the `patterns_block`. This is a mechanical step: no
judgement, no filtering yet. Every line corresponds to a real file, so every
`pattern_key` that can later be returned is guaranteed to be real.

**Filter out patterns that are not adoptable** before presenting them as genuine
candidates, but say why each was excluded:

- `approval_status: deprecated` → do not recommend; if one is the obvious shape,
  point at its `superseded_by` instead.
- `approval_status: candidate` → may be recommended, but **must** be flagged as
  unreviewed (a draft, no human ratification yet) in the rationale.
- `approval_status: provisional` → recommendable; note it is "reviewed, use with
  care, evidence attached but not yet broadly proven."
- `sunset_at` in the past, or the computed next-review date (`valid_from +
  validity_check_months`) in the past → flag as **stale**; treat as a soft caveat,
  not a hard exclusion (the library is advisory).

If `patterns/` is empty, or every pattern is deprecated, stop here: there is
nothing to recommend. Go to the honest-empty route (STEP 4).

### STEP 2 (LLM) — Recommend genuine fits

Run the recommendation reasoning over the project context and the
`patterns_block`. The instruction:

> From a shared, global library of solution patterns, recommend the ones that
> genuinely fit this project. The step recommends; a human architect accepts,
> overrides, or rejects each.
>
> Recommend **ONLY** patterns that are a genuine fit for this project's domain,
> deployment constraints, and data-placement needs. Prefer a **small, defensible
> set over a long list**; recommend **none** if nothing fits. Do **NOT** invent
> patterns or keys — every `pattern_key` returned MUST be one of the keys listed
> in the candidate block. For each recommendation give a **concrete rationale**
> grounded in the project context and the pattern's topology / data placement /
> **attached NFRs**. State the **trade-off or caveat** where one exists; **do not
> oversell.**

Concretely, for each pattern kept, ask:

- Does its `deployment_topology` match the project's stated topology? (e.g. don't
  recommend an on-prem cluster for an in-region managed-service project.)
- Does its `data_placement` satisfy the data-residency constraint? (e.g. reject
  a global multi-region store when "PII stays in-region" is a requirement.)
- Do its `attached_nfrs` cover the NFRs this project actually needs — and are
  there gaps the human should know about?

Ground each rationale in **topology / data_placement / attached_nfrs** — these
exact dimensions — not in vague vibes. Then name the trade-off honestly.

### STEP 3 (LLM) — Write the recommendation as the output menu

Produce the markdown menu (see Output format). A small set (1–3) is the norm.
Two-to-three is a good shortlist; more than that usually means the choice is not
actually being made.

### STEP 4 — Honest empty routes to exploration

If, after STEP 2 (or already at STEP 0a for an OPEN capability), **nothing
genuinely fits**, do not pad the list to look productive. Recommend **none**, say
plainly why the library does not cover this project's shape, and route to
**`architect/surface-solution-options`** — explore the solution space, then
capture any new shape as a candidate pattern through the PR-reviewed contribution
flow.

Honest emptiness is a first-class outcome. A confident "the library has nothing
for this — here's why, go explore" is more valuable than a forced match that the
human has to unpick later.

### STEP 5 — Override is a recorded escape hatch

A human may **accept**, **override**, or **reject** any recommendation. Override
is not silent: it is a recorded escape hatch with a **reason**. When a human
adopts or declines a pattern, append one pure-JSONL line to
`adoptions/ledger.jsonl` (see `adoptions/README.md` for the schema):

```jsonl
{"pattern_key": "PAT-WEBAPP-PG", "repo": "<owner/project>", "disposition": "overridden-out", "at": "2026-06-15", "override_reason": "Client contract mandates on-prem; managed-Postgres topology is disallowed for this engagement."}
```

`disposition` is the closed ledger enum — `adopted-clean` (adopted as-is),
`adopted-with-overrides` (adopted, with some NFRs/constraints waived — give an
`override_reason`), or `overridden-out` (recommended but the human declined it,
with an `override_reason`). The `pattern_key` is the pattern's UPPER-KEBAB key.
The ledger is the durable "why this / why not this" record; it is advisory
provenance. (A pattern that was *not* recommended but the human pulls in anyway is
simply an `adopted-*` line — the ledger records what happened, not who suggested
it.)

## Output format

Return a markdown menu. Concrete template:

```markdown
## Pattern recommendations — <Project Title>

**Need resolved to:** <CAP-key + name> (proven by <PAT-key> | OPEN: <N> candidates, spikes owed) — _via capabilities/INDEX.md_
**Candidate library scanned:** <N> patterns (<a> active, <b> warning, <c> superseded/deprecated — excluded).

### Recommended (accept / override / reject each)

#### 1. Containerised web + managed Postgres  `PAT-WEBAPP-PG`
- **Status:** provisional · valid from 2026-06-15 · next review 2027-06-15 (in date)
- **Fit:** topology = single-region container service; data_placement = in-region managed DB.
- **Rationale:** Matches the in-region data-residency requirement (REQ-12) and the
  confirmed comparators' deployment topology. The managed-Postgres tier keeps
  operational overhead low for an internal service. Its attached NFRs already
  cover TLS-in-transit (`security`) and 99.9% availability (`availability`).
- **Trade-off / caveat:** Provisional, not yet `approved` — evidence is an adoption
  decision, not a production reference build. It also does not by itself satisfy an
  RPO target; the pattern leaves backup/recovery to the adopting project. Surface
  RPO explicitly in the design or it will be a gap.

#### 2. API gateway + managed identity + BFF  `PAT-APIGW-BFF`
- **Status:** provisional · valid from 2026-06-15 · next review 2027-06-15 (in date)
- **Fit:** matches the project's multi-client (web/mobile/partner) auth-consolidation need.
- **Rationale:** Consolidates auth, rate-limiting, and tracing at one tier; the BFF
  reshapes responses per client (covers `security` + `observability`).
- **Trade-off / caveat:** The gateway is a SPOF — mitigate with active-active. **Do not
  adopt if a client policy forbids extra service tiers** (see this pattern's own worked
  override example).

### Considered but not recommended
- `PAT-LAKEHOUSE-DELTA` — a governed analytics lakehouse; only relevant if the project
  has a regulated data/ML estate, which this engagement does not.

### Excluded (not adoptable)
- _(example)_ a `deprecated` pattern — point at its `superseded_by` key instead.

### If you disagree
Override or reject any item above with a reason — it will be recorded in
`adoptions/ledger.jsonl` as your decision and rationale.
```

If nothing fits, the body is short and honest:

```markdown
## Pattern recommendations — <Project Title>

**Need resolved to:** <CAP-key + name — OPEN, no proven fulfilment yet>.
**Candidate library scanned:** <N> patterns. **Recommended: none.**

No approved pattern fits this project's shape: it needs <X topology> with
<Y data-placement>, and the closest library patterns (`a`, `b`) assume
<incompatible constraint>. Forcing a match would mislead the design.

**Next step → `architect/surface-solution-options`.** Explore the solution space,
and if a new shape emerges, propose it as a *candidate* pattern through the
PR-reviewed contribution flow so the next project can reuse it.
```

## Notes / anti-patterns

- **Never invent a `pattern_key`.** Every key emitted must trace to a real file
  under `patterns/`. The deterministic STEP 1 exists precisely so the set of
  legal keys is fixed before reasoning. Wanting to recommend something that isn't
  in the library is the honest-empty signal (STEP 4), not licence to make one up.
  This is the no-fabrication keystone applied to pattern keys — see
  `skills/_contract/grounding-no-absent-input`.
- **Don't oversell.** Every recommendation states its trade-off or caveat. A
  recommendation with no caveat is usually one not thought hard enough about —
  surface the cost, the assumption, or the gap.
- **Prefer a small set.** One well-defended pattern beats five hedged ones. A long
  list defers the choice rather than making a recommendation.
- **None is a valid answer.** Recommending nothing and routing to exploration is a
  confident, correct outcome — not a failure.
- **Respect status and dates.** `deprecated` patterns are not recommended (point at
  `superseded_by`); `candidate` patterns carry an "unreviewed draft" caveat;
  `provisional` carries a "reviewed, use with care" caveat; stale (past `sunset_at`
  or the computed next-review date) patterns are flagged as soft caveats. This is
  advisory.
- **You recommend; the human disposes.** Acceptance, override, and rejection are
  the human's. The only obligation is that the override path is recorded with a
  reason in `adoptions/ledger.jsonl`.
- **Retrieval is grounded in real rows.** Any similarity or fit claim is computed
  from and cited to actual pattern frontmatter — never emitted from the model's
  imagination. See `references/retrieval-not-generation.md`.

## v1 scope and the scaling ceiling

The LLM reads the pattern `.md` files **directly** — there is no vector index, no
embedding store, no retrieval service. This is deliberate: it keeps the library
portable (plain markdown in a git repo), human-auditable (a PR diff shows exactly
what changed), and dependency-free (runs in any LLM workflow that can read files).

**The ceiling:** reading every pattern file into context does not scale past
roughly a few dozen patterns. Once the library outgrows the context window, this
step needs a real retrieval layer — embed each pattern's frontmatter + summary,
index it, and retrieve top-K candidates before STEP 2's reasoning. Until then,
direct reads are correct and honest. At the ceiling, the fix is a retrieval index
*feeding* this same prompt — the method does not change, only how the
`patterns_block` is assembled.

---

### Companion reference

Ship and read `references/retrieval-not-generation.md` alongside this skill:
similarity and fit are computed from and cited to real pattern rows, never
emitted by the model; and honest emptiness routes to exploration rather than
fabricating a fit.
