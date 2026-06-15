---
name: author-capability
description: Author one capability as a markdown file with CI-validated YAML frontmatter — a technology-free need, jargon-free aliases for findability, honest proven-vs-candidate fulfilments, and a measurable governance floor. The skill writes the file at approval_status candidate; the capability PR review ratifies it.
one_liner: Name a need and its proven-or-candidate fulfilments as a library file.
aliases: [add a capability, write a capability, name a need, requirements-to-components bridge, what fulfils this need, capability library entry, register a need, map a need to a pattern]
when_to_use: Naming a recurring system need as a first-class capability — the bridge between a requirement and the component patterns that fulfil it. Use when a need keeps recurring and deserves a stable name, or to record candidate fulfilments that owe a spike before any pattern exists.
output_kinds: [proposal]
deterministic_fallback: Fill the capability frontmatter template + body skeleton from the stated need; leave the need_statement, aliases, and governance floor as one-line stubs for a human to flesh out.
suggested_tier: frontier
tier_reason: Synthesising a technology-free need, jargon-free aliases, and an honest candidate-vs-proven read with a measurable governance floor is high-stakes findability and honesty work.
neighbours: Often follows library/author-component-pattern (name the need a new pattern fulfils) or architect/recommend-component-patterns (a need recurred with no capability to resolve it). Hands off to the capability PR review, and to architect/recommend-component-patterns which reads capabilities/INDEX.md to resolve needs.
---

# author-capability

> A capability is a promise about a need: this need recurs, here is what it means in
> plain words, here is what fulfils it today (with evidence) or what still owes a
> spike, and here is the minimum governance bar any fulfilment must clear. This skill
> writes that promise as one markdown file. It does **not** make it binding — a human
> reviewer (the CODEOWNERS capability review) turns a candidate into a blessed entry.

## Purpose

Author **exactly one** capability as a single markdown file under `capabilities/`, with
YAML frontmatter validated in CI against
`capabilities/_schema/capability.frontmatter.schema.json`, and a body of *the need +
fulfilments + governance floor*.

A capability is the named middle term the requirements-to-components chain needs: a
requirement cites a capability (`fulfils_capability: CAP-…`), and the capability cites the
pattern that fulfils it (`fulfilled_by[].pattern_key`). It is what lets a reader who can
name a need but not a technology find a proven shape — or see honestly that none exists yet.

The skill **writes the file at `approval_status: candidate`** and stops. It never sets a
fulfilment to `confidence: proven` and never advances `approval_status`. Both are human acts
in a PR review.

This is light and advisory. A capability records a need and its options; nothing is forced
on a downstream project.

## When to use

- A **need keeps recurring** across projects ("a data warehouse", "somewhere to run our
  agents") and deserves a stable, cite-able name so requirements can point at it and
  patterns can be matched to it.
- You want to **record candidate fulfilments honestly** — plausible vendor components that
  still owe a proving spike — before any pattern exists, so the gap is visible rather than
  silently unmet.
- You authored a new pattern and want to **name the need it fulfils** so a need-first reader
  can find it via `capabilities/INDEX.md`.

Do **not** use this to:
- *Author the component shape itself* → that is `library/author-component-pattern`.
- *Recommend a fulfilment for a specific project* → that is
  `architect/recommend-component-patterns`.
- *Promote a candidate to proven* → that is a human PR-review act with a spike behind it;
  this skill cannot and must not flip `confidence` or `approval_status`.

## Inputs

Gather these from the context handed to you, as markdown:

1. **The need** — what a system needs and why, stated **technology-free** ("a system needs
   to … so that …"). Name the problem, never the product.
2. **Lay aliases** — at least two plain-language terms a non-expert would type for this need
   ("data warehouse", "EDW", "reporting store"). These are the findability seed; they feed
   `capabilities/INDEX.md`.
3. **The fulfilments** — for each: the component, a `confidence` (`proven` or `candidate`),
   and a one-line `note`. A proven fulfilment names a `pattern_key` and build `evidence`; a
   candidate names a vendor in the note and lists the `open_questions` a spike must answer.
4. **The governance floor** — the minimum, **measurable** governance bars any fulfilling
   pattern must meet or honestly waive, each with a `kind` from the closed 11-value NFR enum,
   a `statement`, and a testable `acceptance_criterion`.

You need no database or network call. The capability is a plain markdown file; the schema
validation runs in CI on the PR.

## Target rule (quoted)

<!-- BEGIN target-rule (byte-stable; do not edit a quoted copy — edit _shared/target-rule.md) -->

**TARGET RULE — agents target the model, the record, or the blind spot, never the judgment.**

Every agent output is exactly one of four kinds:

- `proposal` — a derived or structured thing to accept, edit, or reject.
- `question` — a named tension and the assumption beneath it, for a human to rule on.
- `menu` — N un-ranked, equal options; "do nothing" is always one of them.
- `halt` — a stop; the agent waits for a human.

An agent output is **never** any of these (the forbidden-output list):

- a **status**
- a **verdict**
- a **colour**
- a **ranking**
- a **score**
- a **feasibility** call
- a **disposition**
- an **assessment of a person**

The three legal targets, and the one illegal one:

- **MODEL** — keep a cheap model on rails (decompose, classify, structure, trace).
- **RECORD** — structure something for defensibility and reuse (assemble, retrieve, cite).
- **BLIND SPOT** — coverage and de-biasing rituals (surface a conflict, name an adjacency, ask "which assumption gives?").
- **JUDGMENT** — the human's call: good-enough, feasible, approved, who's at fault, what colour, what ranks first. The agent **never** targets this; it hands the human a typed thing to rule on.

If an output reads like a decision someone could rubber-stamp, it has targeted the JUDGMENT. Reshape it into a `proposal`, a `question`, a `menu`, or a `halt`, and hand the call to the human.

<!-- END target-rule -->

## The frontmatter — the full v1 field set

Validated against `capabilities/_schema/capability.frontmatter.schema.json`. Reproduce every
required field in the file you write.

### REQUIRED (always present)

| field | type | notes |
|---|---|---|
| `capability_key` | string | stable, cite-able, UPPER-KEBAB after `CAP-` — `CAP-OLAP` (matches `^CAP-[A-Z0-9]+(-[A-Z0-9]+)*$`). Survives renames; the token every requirement and pattern cites. The **filename** is a separate human-readable lower-kebab slug. |
| `name` | string | human title — "Online Analytical Processing (OLAP)". |
| `capability_domain` | enum | `data` \| `compute` \| `integration` \| `runtime` \| `experience` \| `governance`. |
| `summary` | string | one paragraph: what the capability is, at a glance. |
| `need_statement` | string | **technology-free**, "a system needs to … so that …". The stable part — names the problem, not the product. |
| `aliases` | list (≥2) | lay synonyms a non-expert would type. **The findability seed** — these feed `capabilities/INDEX.md`. One alias is not findable. |
| `fulfilled_by` | list (≥1) | each `{ confidence, note, … }`. `proven` needs `pattern_key` + `evidence`; `candidate` carries `open_questions`. **The honest core.** |
| `governance_nfrs` | list (≥1) | each `{ kind, statement, acceptance_criterion }`; `kind` from the closed 11-value enum. The measurable floor any fulfilment must clear. |
| `valid_from` | date (ISO) | the day the capability was authored. |
| `approval_status` | enum | `candidate` \| `provisional` \| `approved` \| `deprecated`. **HUMAN-ONLY.** The agent writes `candidate`. |

### CONDITIONALLY REQUIRED (a human fills these on promotion)

| field | required when |
|---|---|
| `approved_by` | `approval_status` ≥ `provisional`. Who ratified it (a CODEOWNER). The agent never writes this. |
| `approved_at` | `approval_status` ≥ `provisional`. When. |
| `superseded_by` | `approval_status == deprecated`. Where a reader goes instead. |

### Inside `fulfilled_by[]`

| field | required when |
|---|---|
| `confidence` | always — `proven` or `candidate`. **The agent writes `candidate` and NEVER `proven`.** |
| `note` | always — one line on the fulfilment. |
| `pattern_key` | when `confidence: proven` (optional for a candidate — a candidate may name a vendor in `note`). |
| `evidence` | when `confidence: proven` — build evidence `{title, url}`, exactly as a promoted pattern carries. |
| `open_questions` | expected on a candidate — the spike questions that gate promotion. |

> **The one rule that protects the library's honesty:** the agent writes `approval_status:
> candidate` and every `fulfilled_by[].confidence: candidate`, and leaves the proven-only
> fields (`pattern_key` may be present for a known pattern, but `evidence` + `proven`) for a
> human who has a spike behind them. A capability that calls a fulfilment `proven` without a
> spike is exactly the lie the PR review exists to catch.

## The closed NFR `kind` enum (shared with patterns)

The 11 values, from `patterns/_schema/nfr-kinds.enum.txt`:

`security` · `availability` · `performance` · `data-residency` · `observability` ·
`resilience` · `cost` · `compliance` · `scalability` · `data-governance` · `operations`

The capability's `governance_nfrs` reuse this exact vocabulary so a fulfilling pattern's
`attached_nfrs` can be checked against the floor kind-for-kind. Do not invent a twelfth.

## The method — STEPS

### STEP 1 (DETERMINISTIC) — Lay down the frontmatter template + body skeleton

The deterministic base; runs with no model. Coin `capability_key` as a stable UPPER-KEBAB
key after `CAP-`, choose a human-readable lower-kebab filename slug under
`capabilities/<domain>/`, stamp `valid_from` to today, set `approval_status: candidate`, set
every `fulfilled_by[].confidence` you are unsure of to `candidate`, and fill every field you
have an input for. Never write `confidence: proven` or `approval_status` past `candidate`.

Copy the template from `capabilities/_TEMPLATE.md` and fill it. The required shape:

```yaml
---
capability_key: CAP-<UPPER-KEBAB>     # cite-able key, ^CAP-[A-Z0-9]+(-[A-Z0-9]+)*$ — NOT the filename
name: <human title>
capability_domain: <data|compute|integration|runtime|experience|governance>
summary: >
  <one paragraph: what the capability is, at a glance.>
need_statement: "a system needs to <do X> so that <Y>."   # technology-free — name the problem
aliases:                              # >=2; the findability seed feeding capabilities/INDEX.md
  - <lay synonym>
  - <lay synonym>
fulfilled_by:                         # >=1; proven-vs-candidate lives here
  - confidence: <proven|candidate>    # AGENT WRITES candidate; a human sets proven with a spike
    note: <one line on the fulfilment>
    # pattern_key: PAT-...            # REQUIRED when proven; optional for a candidate
    # evidence: [{title: ..., url: "https://..."}]   # REQUIRED when proven
    open_questions:                   # the spike questions a candidate must answer
      - <question>
governance_nfrs:                      # >=1; the measurable floor
  - kind: <one of the closed 11>
    statement: <the minimum governance bar>
    acceptance_criterion: <testable — e.g. "region == declared classification region">
valid_from: "<YYYY-MM-DD>"
validity_check_months: 12             # optional
approval_status: candidate            # HUMAN-ONLY to raise; agent writes candidate
# approved_by / approved_at — filled by a CODEOWNER at promotion
# superseded_by — filled only when deprecating
---
```

Then the body skeleton (headings, ready for STEP 2 to fill):

```markdown
# <name> (`CAP-<KEY>`)

## The need
## How it is fulfilled (### Proven / ### Candidates (spikes owed))
## Governance floor
## Aliases
## Promotion
```

### STEP 2 (LLM) — Draft the need, aliases, fulfilment honesty, and governance floor

The judgement step, the only one needing a model. From the context you gathered, draft:

- **`need_statement` + The need (body)** — the need, technology-free. Strip every product
  name out of the *need*; products belong only in `fulfilled_by`. A reader who has never
  heard of the eventual component should still recognise their problem here.
- **`aliases`** — at least two, ideally more — the plain words a non-expert types. These are
  the difference between a findable capability and a buried one. Think of every job title
  that would describe this need in a different vocabulary.
- **`fulfilled_by[]` — honest proven-vs-candidate** — for a proven fulfilment, name the
  pattern and why it fits and reuse its evidence. For a candidate, name the vendor in `note`,
  set `confidence: candidate`, and write the **`open_questions` a spike must answer** before
  it could be promoted. Be honest: if nothing is proven, say so — an all-candidate capability
  is a legitimate, valuable record of an unmet need.
- **`governance_nfrs` — the measurable floor** — each a `kind` + `statement` + **testable
  `acceptance_criterion`** ("region == declared classification region", not "is compliant").
  Mirror the quality of a strong pattern's attached NFRs: concrete and checkable. This floor
  is what a future spike result is judged against.

Use this drafting prompt:

```
A recurring system need should become a first-class capability. Write the NEED
(technology-free), the ALIASES (jargon-free synonyms), the FULFILMENTS (honest
proven-vs-candidate), and the GOVERNANCE FLOOR (measurable bars).

THE NEED (what a system needs and why):
<the need context>

KNOWN / CANDIDATE FULFILMENTS (component, vendor, proven|candidate, what is unproven):
<the fulfilments>

GOVERNANCE EXPECTATIONS (the minimum bars any fulfilment must meet):
<the governance context>

Write:
1. need_statement — "a system needs to … so that …", technology-free. No product names.
2. aliases — >=2 plain-language synonyms a non-expert would type. More is better.
3. fulfilled_by — for each: confidence (proven|candidate), a one-line note, and for a
   candidate the open_questions a spike must answer. Mark anything unproven as candidate.
   NEVER write confidence: proven without build evidence — leave that to a human + spike.
4. governance_nfrs — for each: kind (closed 11-enum), statement, a TESTABLE
   acceptance_criterion. Measurable, not aspirational.

Be honest about gaps. An all-candidate capability is a valid record of an unmet need.
```

> **Multi-agent option (advisory).** This step deepens with independent parallel agents: launch one sub-agent per candidate fulfilment, at most 4 at a time, each a separate sub-agent. A failed sub-agent returns nothing and is never fatal — the deterministic base stands; merge what succeeded. (Claude Code: use the Task tool / subagents. Other tools: launch parallel model calls; or a matrix-strategy CI job.) Never required — it adds coverage and cuts single-pass bias. See `skills/_contract/parallel-agents`.

One agent per candidate probes that candidate's `open_questions` against the governance
floor in parallel, then a synthesis produces a per-candidate proven-or-still-candidate read
for a human to ratify. Preserve dissent on lock-in: a fulfilment that meets the need but
couples you to one vendor is a recorded trade-off, not a silent disqualifier.

Merge STEP 2's prose into the STEP 1 skeleton and write the file with the `Write` tool at
`capabilities/<domain>/<filename-slug>.md`.

### STEP 3 — Update the index and hand off to the capability PR review

Add every alias to `capabilities/INDEX.md`, each pointing at this `capability_key` + name +
fulfilment state — the index is where a need-first reader is pointed first, so a capability
absent from it is a capability nobody finds.

The file is now a **candidate**. Open the PR yourself with the default PR template
(`.github/pull_request_template.md` — there is no capability-specific template), and
populate its fields from the capability you authored: the one-line proposal, the index
rows you added, and the self-check boxes you can honestly confirm. CI runs the capability
frontmatter schema validation and the index advisory linter. A CODEOWNERS architect reviews
the diff and merges — the one structural human review. Only at that merge does a fulfilment
climb to `confidence: proven` (with spike evidence and a fulfilling pattern that meets the
governance floor) or `approval_status` advance, in a commit the CODEOWNER owns. **You stop at
`candidate`.** The review flow is in `CONTRIBUTING.md`.

## Output format

You write **one file** at `capabilities/<domain>/<filename-slug>.md`, plus the matching index
rows. The capability files under `capabilities/data/` and `capabilities/runtime/` are the
gold standard for tone and honesty — read them before authoring. `CAP-OLAP` shows a clean
proven fulfilment; `CAP-AGENT-RUNTIME` shows the all-candidate, spikes-owed shape.

## Notes / anti-patterns

- **The agent stops at `candidate`.** Never write `approval_status: approved`/`provisional`
  and never write a fulfilment's `confidence: proven`. Both need a human and (for proven) a
  spike with evidence. Writing `proven` is the single most damaging thing this skill could do.
- **The need is technology-free.** Product names belong in `fulfilled_by`, never in
  `need_statement`. A need stated as a product is a recommendation in disguise and ages with
  the product.
- **Aliases are the findability seed — give at least two, ideally many.** A capability with
  one alias is one a non-expert never finds. Every job title that describes this need in a
  different vocabulary is a candidate alias.
- **Be honest about the gap.** An all-candidate capability with no proven fulfilment is a
  valid, valuable record of an unmet need with the spikes it owes. Do not fabricate a proven
  fulfilment to make a capability look finished.
- **Governance floor is measurable.** "Is compliant" is not an acceptance criterion; "region
  == declared classification region" is. The floor exists so a future spike result is
  judged, not asserted.
- **Stay inside the closed enums.** `capability_domain` ∈ the six in
  `capabilities/_schema/capability-domains.enum.txt`; NFR `kind` ∈ the 11 in
  `patterns/_schema/nfr-kinds.enum.txt`; `confidence` ∈ {proven, candidate};
  `approval_status` ∈ {candidate, provisional, approved, deprecated}.
- **`capability_key` is forever.** UPPER-KEBAB after `CAP-`, independent of the filename, the
  stable token every requirement and pattern cites. Changing it orphans every citation.
- **One file, then stop.** This skill authors exactly one capability. A second need is a
  second file and a second PR.
- **Keep the index in sync.** Every alias must appear in `capabilities/INDEX.md` pointing at
  a real `capability_key`; the advisory index linter fails if an alias is missing or an index
  entry points nowhere.
- **Light and advisory.** A capability records a need and its options; nothing is forced. The
  CODEOWNERS capability review is a human reading the diff and merging — the one structural
  human review — not an automated lock.
