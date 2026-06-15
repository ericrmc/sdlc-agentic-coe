---
name: recommend-component-patterns
description: Read project context plus the approved pattern library files and recommend only genuine fits (a small defensible set, or none); never invent pattern_keys; honest-empty routes to surface-solution-options.
when_to_use: Choosing a solution shape. The fastest route to a governed design is adopting an already-approved pattern — so before you architect anything bespoke, check what the Centre of Excellence has already built and validated.
output_kinds: [proposal, menu]
deterministic_fallback: Read the pattern files directly and match on category / topology / data_placement keywords; present the candidates, recommend none if nothing fits.
suggested_tier: opus
---

# recommend-component-patterns — retrieval, not generation

This is FORGE stage 4: the payoff. By now the project has business outcomes,
derived requirements, attached NFRs, and a sense of its deployment topology and
data placement. The job here is **not** to invent an architecture. It is to
**retrieve** the patterns from the approved CoE library that genuinely fit, and
hand a human a short, defensible shortlist to accept, override, or reject.

> Retrieval, not generation. Every pattern you name must already exist in
> `patterns/` — proven, PR-reviewed, evidence-backed, in date. You are a
> librarian with judgement, not an author.

## Purpose

From the approved Centre of Excellence pattern library, recommend the patterns
that **genuinely fit** this project's domain, deployment constraints, and
data-placement needs.

You recommend. A human accepts, overrides, or rejects each one. Nothing here is
a gate — it is advisory. The value is that adopting an approved pattern is the
fastest route to a governed design: the pattern already carries its validated
NFRs, its evidence of having been built, and its caveats. Reuse beats invention.

If nothing in the library fits, that is a real and useful answer. Say so, and
route the project to exploration (`surface-solution-options`) rather than
forcing a bad match.

## When to use

- You have a project's context (outcomes, requirements, NFRs, rough topology and
  data-placement intent) and need to choose a solution shape.
- You want to know what the CoE has **already validated and built** before
  committing to anything bespoke.
- You are about to write a solution architecture and want a governed starting
  point instead of a blank page.

Do **not** use this to design a new pattern. If the fit is genuinely empty, that
is `surface-solution-options`' job, and a newly-invented shape should later be
captured as a *candidate* pattern through the PR-reviewed contribution flow —
not minted here on the fly.

## Inputs

The user supplies (as markdown / context):

1. **Project context** — title, description, and the relevant downstream
   artefacts: derived requirements, attached NFRs, and any stated deployment
   topology and data-placement constraints (e.g. "in-region only", "on-prem
   mandated by client contract", "PII must not leave the regional boundary").
2. **The pattern library** — the files under `patterns/`. In v1 you read these
   `.md` files **directly**; each has YAML frontmatter (`pattern_key`, `name`,
   `category`, `intent`, `deployment_topology`, `data_placement`,
   `approval_status`, `attached_nfrs`, `valid_from`, `validity_check_months`,
   `sunset_at`, `evidence`, etc. — see `patterns/_schema/pattern.frontmatter.schema.json`)
   and a body (Summary, When to use / when NOT to, Attached NFRs, Trade-offs).

You do not need a database, a vector index, or a network call. The pattern files
are the library.

## The method — STEPS

### STEP 1 (DETERMINISTIC) — Load and present the candidate `patterns_block`

Read the files under `patterns/`. For each pattern, extract from its frontmatter
and build **one line** in this exact shape:

```
pattern_key | name | category | deployment_topology | data_placement — one-line summary
```

Concatenate these into the `patterns_block`. This is a mechanical step: no
judgement, no filtering yet. Every line corresponds to a real file, so every
`pattern_key` you can later return is guaranteed to be real.

**Filter out patterns that are not adoptable** before presenting them as genuine
candidates, but say why you excluded them:

- `approval_status: deprecated` → do not recommend; if one is the obvious shape,
  point at its `superseded_by` instead.
- `approval_status: candidate` → may be recommended, but you **must** flag that it
  is unreviewed (a draft, no human ratification yet) in the rationale.
- `approval_status: provisional` → recommendable; note it is "reviewed, use with
  care, evidence attached but not yet broadly proven."
- `sunset_at` in the past, or the computed next-review date (`valid_from +
  validity_check_months`) in the past → flag as **stale**; treat as a soft caveat,
  not a hard exclusion (the library is advisory, not gated).

If `patterns/` is empty, or every pattern is deprecated, stop here: there is
nothing to recommend. Go to the honest-empty route (STEP 4).

### STEP 2 (LLM) — Recommend genuine fits, with the recommend prompt

Run the recommendation reasoning over the project context and the
`patterns_block`. **The method, verbatim from the source `recommend_patterns.md`:**

> You are a solution architect on an internal managed-services delivery team.
> From a shared, global library of solution patterns, recommend the ones that
> genuinely fit this project. You recommend; a human architect accepts,
> overrides, or rejects each.
>
> Recommend **ONLY** patterns that are a genuine fit for this project's domain,
> deployment constraints, and data-placement needs. Prefer a **small, defensible
> set over a long list**; recommend **none** if nothing fits. Do **NOT** invent
> patterns or keys — every `pattern_key` you return MUST be one of the keys
> listed in the candidate block. For each recommendation give a **concrete
> rationale** grounded in the project context and the pattern's topology / data
> placement / **attached NFRs**. State the **trade-off or caveat** where one
> exists; **do not oversell.**

Concretely, for each pattern you keep, ask:

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
Two-to-three is a good shortlist; more than that usually means you are not
actually choosing.

### STEP 4 — Honest empty routes to exploration

If, after STEP 2, **nothing genuinely fits**, do not pad the list to look
productive. Recommend **none**, say plainly why the library does not cover this
project's shape, and route to **`surface-solution-options`** (FORGE stage:
explore the solution space, then capture any new shape as a candidate pattern
through the PR-reviewed contribution flow).

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
provenance, not a gate. (A pattern you did *not* recommend that the human pulls in
anyway is simply an `adopted-*` line — the ledger records what happened, not who
suggested it.)

## Output format

Return a markdown menu. Concrete template:

```markdown
## Pattern recommendations — <Project Title>

**Candidate library scanned:** <N> patterns (<a> active, <b> warning, <c> superseded/deprecated — excluded).

### Recommended (accept / override / reject each)

#### 1. Containerised web + managed Postgres  `PAT-WEBAPP-PG`
- **Status:** provisional · valid from 2026-06-15 · next review 2027-06-15 (in date)
- **Fit:** topology = single-region container service; data_placement = in-region managed DB.
- **Rationale:** Matches the in-region data-residency requirement (R-NF-03) and the
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

**Candidate library scanned:** <N> patterns. **Recommended: none.**

No approved pattern fits this project's shape: it needs <X topology> with
<Y data-placement>, and the closest library patterns (`a`, `b`) assume
<incompatible constraint>. Forcing a match would mislead the design.

**Next step → `surface-solution-options`.** Explore the solution space, and if a
new shape emerges, propose it as a *candidate* pattern through the PR-reviewed
contribution flow so the next project can reuse it.
```

## Notes / anti-patterns

- **Never invent a `pattern_key`.** Every key you emit must trace to a real file
  under `patterns/`. The deterministic STEP 1 exists precisely so the set of
  legal keys is fixed before you reason. If you find yourself wanting to
  recommend something that isn't in the library, that's the honest-empty signal
  (STEP 4), not licence to make one up.
- **Don't oversell.** Every recommendation states its trade-off or caveat. A
  recommendation with no caveat is usually one you haven't thought hard enough
  about — surface the cost, the assumption, or the gap.
- **Prefer a small set.** One well-defended pattern beats five hedged ones. If
  your list is long, you are deferring the choice, not making a recommendation.
- **None is a valid answer.** Recommending nothing and routing to exploration is
  a confident, correct outcome — not a failure.
- **Respect status and dates.** `deprecated` patterns are not recommended (point at
  `superseded_by`); `candidate` patterns carry an "unreviewed draft" caveat;
  `provisional` carries a "reviewed, use with care" caveat; stale (past `sunset_at`
  or the computed next-review date) patterns are flagged as soft caveats. This is
  advisory, never a hard gate.
- **You recommend; the human disposes.** Acceptance, override, and rejection are
  the human's. Your only obligation is that the override path is recorded with a
  reason in `adoptions/ledger.jsonl`.
- **Retrieval is grounded in real rows.** Any similarity or fit claim is computed
  from and cited to actual pattern frontmatter — never emitted from the model's
  imagination. See `references/retrieval-not-generation.md`.

## v1 scope and the scaling ceiling

In v1 the LLM reads the pattern `.md` files **directly** — there is no vector
index, no embedding store, no retrieval service. This is deliberate: it keeps the
library portable (plain markdown in a git repo), human-auditable (a PR diff shows
exactly what changed), and dependency-free (runs in any LLM workflow that can
read files).

**The ceiling:** reading every pattern file into context does not scale past
roughly a few dozen patterns. Once the library outgrows the context window, this
step needs a real retrieval layer — embed each pattern's frontmatter + summary,
index it, and retrieve top-K candidates before STEP 2's reasoning. Until then,
direct reads are correct and honest. When you hit the ceiling, the fix is a
retrieval index *feeding* this same prompt — the method does not change, only how
the `patterns_block` is assembled.

---

### Companion reference

Ship and read `references/retrieval-not-generation.md` alongside this skill:
similarity and fit are computed from and cited to real pattern rows, never
emitted by the model; and honest emptiness routes to exploration rather than
fabricating a fit.
