---
name: author-component-pattern
description: Author one reusable component pattern as a markdown file with CI-validated YAML frontmatter (the full lifecycle/provenance field set) and a body of summary + attached NFRs with honest trade-offs; the skill writes the file at approval_status candidate, the pattern PR review ratifies it.
one_liner: Capture one proven solution shape as a library pattern file.
aliases: [save a reusable design, write a pattern, document an architecture, add to the pattern library, capture what worked, reference architecture, golden path template, promote a solution]
when_to_use: Capturing a reusable solution shape as a pattern, or promoting an explored solution into the library. Use after a project has chosen a solution worth reusing — not to evaluate or recommend an existing one.
output_kinds: [proposal, halt]
deterministic_fallback: Fill the pattern frontmatter template + body skeleton from the chosen solution; leave summary/trade-offs as one-line stubs for a human to flesh out.
suggested_tier: frontier
tier_reason: Capturing a load-bearing reusable claim with measurable NFRs and an honest cost demands careful synthesis and judgement.
neighbours: Usually follows architect/surface-solution-options (an explored shape proves itself and is worth promoting). Hands off to library/author-capability (name the need the pattern fulfils) and library/pattern-library-curate (lifecycle health once it is in the library).
---

# author-component-pattern

## Purpose

Author exactly one reusable component pattern as a markdown file under `patterns/`
(YAML frontmatter validated in CI against
`patterns/_schema/pattern.frontmatter.schema.json`; body = summary + attached NFRs +
honest trade-offs). Light and advisory: a pattern is a recommendation with a track
record, not a mandate — a project may adopt, override-with-reason, or ignore it. The
skill writes the file at `approval_status: candidate`; a CODEOWNER PR review ratifies
it (the keystone enforced at STEP 3 and the COMPUTED/HUMAN-ONLY note below).

## When to use

- A project chose a **solution shape worth reusing** — a deployment topology, an
  integration approach, a data placement — and you want to capture it so the next
  project can find and adopt it instead of re-deriving it.
- You are **promoting an explored solution** (the output of
  `architect/surface-solution-options`, or a custom design that proved itself) into
  a library candidate through the PR-reviewed contribution flow.

Do **not** use this to:
- *Recommend* an existing pattern → that is `architect/recommend-component-patterns`.
- *Propagate* an adopted pattern's NFRs into a project → `architect/propagate-pattern-nfrs`.
- *Approve* a pattern → that is a human PR-review act; this skill cannot and must
  not set `approved`.
- Mint a pattern "on the fly" mid-design with no evidence it was ever built — a
  pattern with no built artefact is an idea, and ideas live in
  `architect/surface-solution-options`, not the library.

## Inputs

Gather these from the context handed to you, as markdown:

1. **The chosen solution** — *Required.* What was built (or proven): the deployment
   topology, the data placement, the components, and *why this shape over the
   alternatives*. This is the raw material for the `summary` and the trade-offs —
   STEP 2 synthesises the **entire** pattern from it, so without it there is nothing
   to capture. *If absent/unreadable/empty: HALT and ask where the built/proven
   solution is described (per `_shared/grounding.md`); never invent a topology, a
   data placement, or a trade-off the team never built.* Readable forms: a design
   doc or ADR, a repo/PR, a runbook, an `architect/surface-solution-options`
   output, or a pasted description of what was built and why.
2. **The category** — *Required.* One of `deployment | integration | data` (the closed
   enum that matches the `patterns/` folder names). *If absent: surface it as a
   `question` — the category is a closed three-way choice the human can make in one
   line; never guess it from the prose.*
3. **The quality bars it must always meet** — *Optional (recommended).* The NFRs, each
   with a `kind` from the **closed 11-value enum** (see `nfrs/nfr-kinds.md`), a
   `statement`, and a testable `acceptance_criterion`. If a quality bar has no way to
   be verified, it is a wish, not an NFR — make it measurable or drop it. *If absent:
   draft the NFRs only from the chosen solution above; never assert a quality bar the
   built shape does not actually carry.*
4. **The evidence it was built** — *Optional at `candidate`.* Links/artefacts (a repo,
   a PR, a runbook, a design doc, a deployed-service URL). Required only once the
   status is promoted past `candidate`; record what you are given and leave the slot
   honest if there is none yet — never fabricate a link.

No database or network call is needed. The pattern is a plain markdown file in a git
repo; the schema validation runs in CI on the PR.

## Grounding (quoted)

This skill synthesises the whole pattern from one required input — the chosen solution
(STEP 2) — so it carries the no-fabrication keystone (`skills/_contract/grounding-no-absent-input`):
no built artefact ⇒ no pattern; no evidence ⇒ no promotion; never fabricate a link.

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

## The frontmatter — the full v1 field set

Validated against `patterns/_schema/pattern.frontmatter.schema.json`. Reproduce
**every** field below in the file you write (omit only the truly optional ones that
do not apply). The grouping tells you which the agent fills, which only a human
ever sets, and which the system computes.

### REQUIRED (always present)

| field | type | notes |
|---|---|---|
| `pattern_key` | string | stable, cite-able, UPPER-KEBAB after `PAT-` — `PAT-WEBAPP-PG` (matches `^PAT-[A-Z0-9]+(-[A-Z0-9]+)*$`). Survives renames; the stable token every recommendation cites. The **filename** is a separate human-readable lower-kebab slug and need NOT equal the key. |
| `name` | string | human title — "Containerised web + managed Postgres". |
| `category` | enum | `deployment` \| `integration` \| `data`. |
| `intent` | string | one sentence in the exact shape **"Use this WHEN … so that …"** — the retrieval anchor. |
| `deployment_topology` | string | where it runs — "Single-region container service (Kubernetes/ECS) + managed Postgres". |
| `data_placement` | string | where data lives — "In-region managed relational DB; no cross-region replication by default". |
| `summary` | string | 2–4 sentences: what the shape is and what it is for (body expands it). |
| `approval_status` | enum | `candidate` \| `provisional` \| `approved` \| `deprecated`. **HUMAN-ONLY.** The agent writes `candidate` and **NEVER** sets `approved`. |
| `valid_from` | date (ISO) | the day this pattern's claims start being true — author/promotion date. |
| `attached_nfrs` | list | each `{ kind, statement, acceptance_criterion }`; `kind` from the closed 11-value enum (`nfrs/nfr-kinds.md`). The governed quality bar `architect/propagate-pattern-nfrs` carries into adopting projects. |

### CONDITIONALLY REQUIRED (required once the status climbs — a human fills these)

| field | type | required when |
|---|---|---|
| `approved_by` | string | `approval_status` ≥ `provisional`. Who ratified it (a CODEOWNER). The agent never writes this. |
| `approved_at` | date (ISO) | `approval_status` ≥ `provisional`. When. |
| `evidence` | list of `{ title, url }` | `approval_status` ≥ `provisional`. The artefacts proving it was actually built — `title` + a real `url` (optional `kind`/`project`/`date`). No evidence, no promotion. |
| `superseded_by` | string (pattern_key) | `approval_status == deprecated`. Where adopters should go instead. Never deprecate a pattern that has adoptions without pointing somewhere. |

### OPTIONAL

| field | type | default | notes |
|---|---|---|---|
| `validity_check_months` | int | `12` | re-review cadence; CI/Actions can flag a pattern whose `valid_from + validity_check_months` is in the past as **stale** (a soft caveat, not a hard exclusion). |
| `sunset_at` | date (ISO) | — | the date the pattern stops being recommendable; a planned end-of-life. |
| `supersedes` | string (pattern_key) | — | the older pattern this replaces (the forward half of `superseded_by`). |
| `constraints` | list of `{ statement, enforced }` | — | what the pattern makes you give up; `enforced` ∈ `hard` (cannot be waived) \| `soft` (waiving it is a recorded compromise). Fuel for `architect/validate-solution-vs-requirements`. |
| `reference_implementations` | list of `{ kind, url, provisions, notes? }` | — | forward "start here" pointers (`kind` ∈ `iac` \| `app` \| `notebook` \| `scaffold`; real `url`; `provisions` free-text). ADVISORY: answers "what do I start from?", **never gates approval** — distinct from `evidence` ("was this built?"), which does. If you have no confirmed repo, write a marked placeholder (`https://github.com/ORG/REPLACE-ME-…`) for a CODEOWNER to replace; never fabricate a real-looking link. |

### COMPUTED — NEVER WRITE THESE

| field | derived from | notes |
|---|---|---|
| `maturity` | adoption count | `experimental` \| `emerging` \| `battle-tested`. An opinion the *evidence* earns, not one you assert. |
| `adoption_count` | `adoptions/ledger.jsonl` | `COUNT` of real adoptions. The headline "used in N engagements" number — never a model-emitted figure. |

> **The keystone (enforced at STEP 3):** the agent writes `approval_status: candidate`,
> never `approved`/`provisional`; leaves `approved_by`/`approved_at`/`evidence` blank-or-honest
> unless a human is explicitly promoting; and **never** writes `maturity`/`adoption_count`
> (computed). A pattern that calls itself `approved` or `battle-tested` with no human and no
> ledger behind it is the lie the PR review exists to catch.

## The closed NFR `kind` enum

The 11 values live in `nfrs/nfr-kinds.md` and are listed in the STEP 1 template comment.
The enum is closed: if a quality bar fits none, pick the closest or raise it with the
NFR-catalogue owner — never invent a twelfth (it breaks propagation/coverage checks).

## Worked examples to match

Read the patterns already authored under `patterns/` before you write — they are the
gold standard for tone, granularity, and honest trade-offs:

| pattern_key | file | category | the load-bearing NFR (named honestly) |
|---|---|---|---|
| `PAT-WEBAPP-PG` | `patterns/deployment/containerised-web-managed-postgres.md` | deployment | data-residency (data at rest stays in declared region) |
| `PAT-APIGW-BFF` | `patterns/integration/api-gateway-bff-managed-identity.md` | integration | security (short-lived tokens; no raw service tokens to clients) |
| `PAT-LAKEHOUSE-DELTA` | `patterns/data/databricks-lakehouse-delta.md` | data | data-governance (Unity Catalog column-level PII tagging) |

Each names its trade-off in the body — the gateway as a SPOF; the single DB write
authority; UC platform lock-in — and none pretends the shape is free. Match that
honesty. `patterns/README.md` lists the full library state, including needs that are
planned but not yet authored.

## The method — STEPS

### STEP 0 — Locate / verify the required input (deterministic, pre-model)

Before laying down any template, confirm the one required input — **the chosen
solution** (what was built or proven) — is present as a file-level fact: absent /
unreadable / empty. This is mechanical; it is **never** a judgement on "is this
solution good enough to promote" (that is the human's call, and a verdict the rule
forbids a halt from carrying).

- **The chosen solution is absent/unreadable/empty** → emit the clean HALT below and
  stop. There is nothing to synthesise a pattern from, and a pattern minted with no
  built artefact behind it is an invented claim — the exact failure this contract
  exists to stop.
- **The category is missing but the solution is present** → do not halt; surface the
  category as a one-line `question` (it is a closed three-way choice), then proceed.
- **The chosen solution is present** → proceed to STEP 1.

```
HALT — required input missing.

I can't author a component pattern without the solution it captures, and I won't
invent a topology, a data placement, or a trade-off the team never built. Point me at
the built (or proven) solution and I'll capture it as a candidate pattern — with a diff
to review; nothing is added to the library until you accept it.

I can read any of: a design doc / ADR · a repo or PR · a runbook · an
`architect/surface-solution-options` output · the solution pasted directly here.
Which one, and where?
```

### STEP 1 (DETERMINISTIC) — Lay down the frontmatter template + body skeleton

This is the deterministic base; it runs with no model. Coin `pattern_key` as a stable
UPPER-KEBAB key after `PAT-` (e.g. `PAT-WEBAPP-PG`), choose a human-readable lower-kebab
**filename** slug independently (e.g. `containerised-web-managed-postgres.md`) under
`patterns/<category>/`, stamp `valid_from` to today, set `approval_status: candidate`,
and fill every field you have an input for. Leave human-only fields out (or honestly
blank) and **never** write `maturity` / `adoption_count`.

The template (write this exactly, filling the values):

```yaml
---
pattern_key: PAT-<UPPER-KEBAB>        # cite-able key, ^PAT-[A-Z0-9]+(-[A-Z0-9]+)*$ — NOT the filename
name: <human title>
category: <deployment|integration|data>
intent: "use WHEN <condition> so that <benefit>."
deployment_topology: <where it runs>
data_placement: <where data lives>
summary: >
  <2–4 sentences: what the shape is and what it is for.>
approval_status: candidate          # HUMAN-ONLY to raise; the agent writes candidate and NEVER approved
valid_from: "<YYYY-MM-DD>"          # today (quote it so it stays a string)
validity_check_months: 12           # optional; re-review cadence
# sunset_at: "<YYYY-MM-DD>"         # optional; planned end-of-life
# supersedes: [PAT-<OLDER-KEY>]     # optional; array of keys this replaces
attached_nfrs:
  - kind: <one of the closed 11>     # security|availability|performance|data-residency|observability|
    statement: <the quality bar>     #   resilience|cost|compliance|scalability|data-governance|operations
    acceptance_criterion: <how it is verified — testable>
  # ... one entry per governed NFR
constraints:                         # optional; what you give up
  - statement: <what the pattern forces>
    enforced: <hard|soft>
# reference_implementations:         # optional; forward "start here" pointers — ADVISORY, NOT evidence, never gates approval
#   - {kind: <iac|app|notebook|scaffold>, url: "https://...", provisions: "<azure|aws|...>", notes: "<optional; e.g. CODEOWNER replaces a placeholder URL before approval>"}
# --- filled by a human at promotion (approval_status >= provisional) — agent leaves blank ---
# approved_by: "@architects"
# approved_at: "<YYYY-MM-DD>"
# evidence:
#   - {title: <what the artefact is>, url: "https://...", kind: <repo|pull_request|runbook|adr|dashboard|load_test|post_mortem|doc>}
# --- filled only when deprecating ---
# superseded_by: PAT-<NEWER-KEY>
# --- COMPUTED, never write: maturity, adoption_count ---
---
```

The **filename** is set independently from the key: choose a human-readable lower-kebab
slug (`containerised-web-managed-postgres.md`) — it does **not** need to equal `pattern_key`.

Then the body skeleton (headings, ready for STEP 2 to fill):

```markdown
# <name>

## Context / Problem
## Solution
## Attached NFRs (the governed quality bar)
## When to use / When NOT to
## Trade-offs (the honest cost)
## Evidence / artefacts
## Lifecycle (valid_from, review, sunset/supersede)
## References
```

### STEP 2 (LLM) — Draft the summary + trade-offs from the chosen solution

The judgement step, and the only one needing a model. From the chosen solution, draft
the `summary` + Context/Problem/Solution body grounded in *this* solution; a testable
`acceptance_criterion` per governed NFR; and the honest **Trade-offs** — name the one
load-bearing NFR/cost that most determines fit and the conditions under which the
pattern is the *wrong* choice. A pattern with no stated cost is incomplete. Use this
drafting prompt:

```
A delivery team built a solution worth reusing. Write the SUMMARY and TRADE-OFFS
for a library pattern capturing it, plus a testable acceptance_criterion for each
governed NFR.

CHOSEN SOLUTION (what was built and why this shape):
<the solution context>

GOVERNED NFRs (each: kind from the closed enum, the quality bar):
<the nfrs>

Write:
1. summary — 2–4 sentences: what the shape is and what it is for. Concrete, grounded
   in THIS solution. No marketing.
2. For each NFR — a testable acceptance_criterion (how a reviewer verifies it).
3. trade-offs — name the ONE load-bearing NFR / cost that most determines fit, and
   the conditions under which this pattern is the WRONG choice. Do NOT oversell. A
   pattern with no stated cost is incomplete.
4. when-NOT-to — at least one concrete situation where a project should pick
   something else.

Be evidence-aware: claim only what the built artefact supports. If a quality bar
cannot be verified, say so rather than asserting it.
```

Then merge STEP 2's prose into the STEP 1 skeleton and write the file with the
`Write` tool at `patterns/<category>/<filename-slug>.md` (a human-readable lower-kebab
filename — independent of the UPPER-KEBAB `pattern_key`).

### STEP 3 — Open the pattern PR (do not self-approve)

The file is now a **candidate**. Open the PR yourself with the pattern PR template
(`.github/PULL_REQUEST_TEMPLATE/pattern.md`, selected via
`?template=pattern.md&expand=1`). Populate each section of that template from the
pattern you authored — the change type, the evidence summary, and the reviewer-facing
notes; do not tick a reviewer-checklist box that asserts a human judgment. CI runs the
frontmatter schema validation (`pattern.frontmatter.schema.json`) and the stale/sunset
checks. A CODEOWNER reviews the diff, confirms the **evidence is real**, and merges.
Only at that human merge does the status climb past `candidate` — a CODEOWNER sets
`approval_status: provisional`/`approved`, `approved_by`, `approved_at`, and the
`evidence` list in their own commit. **You stop at `candidate`.** The review flow and
CODEOWNERS map are in `CONTRIBUTING.md`.

## Output format

This skill emits one of two kinds. When the chosen solution is missing it emits the
`halt` from STEP 0. When the solution is present it emits a `proposal`: **one file** at
`patterns/<category>/<filename-slug>.md` (e.g.
`patterns/deployment/containerised-web-managed-postgres.md`), shaped by the STEP 1
frontmatter template + body skeleton and filled by STEP 2. For a complete worked
target, match `patterns/deployment/containerised-web-managed-postgres.md` (PAT-WEBAPP-PG)
and the other files in the "Worked examples to match" table above.

## Notes / anti-patterns

Failure modes not already covered by a STEP or a frontmatter table (the candidate-stop,
computed-never-write, no-evidence-no-promotion, closed-enum, and testable-AC rules are
enforced there — see the COMPUTED/HUMAN-ONLY note, STEP 3, the NFR-enum section, and STEP 2):

- **`pattern_key` is forever.** UPPER-KEBAB (`^PAT-[A-Z0-9]+(-[A-Z0-9]+)*$`), survives
  renames, **independent of the filename** — changing it later orphans every citation.
- **One file, then stop.** A second shape is a second file and a second PR — do not bundle.
- **Deprecate, don't delete.** When a pattern is superseded, set `approval_status: deprecated`
  + `superseded_by` and point adopters onward — never delete a pattern that has adoptions;
  the provenance must survive.
