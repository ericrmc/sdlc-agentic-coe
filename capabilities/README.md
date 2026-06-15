# The Capability Library

A capability is the **named middle term** between a plain-language need and the component
patterns that fulfil it. The pattern library answers "what shape did we build"; this library
answers "what need does a system have, and is there a proven shape for it yet". One `.md`
file per capability, at `capabilities/<domain>/<slug>.md`, PR-reviewed like patterns.

If you can name a need but not the technology, **start at [`INDEX.md`](INDEX.md)** — the
alias-searchable lookup that resolves "data warehouse" or "run our agents in prod" to a
capability and its current fulfilment.

---

## What a capability is

Two halves that must agree:

- **Frontmatter (the record):** `capability_key`, `name`, `capability_domain`,
  `need_statement` (technology-free), `aliases` (the findability seed), `fulfilled_by` (the
  components, each with a `confidence`), `governance_nfrs` (the minimum bar), and the
  lifecycle fields. Validated against
  [`_schema/capability.frontmatter.schema.json`](_schema/capability.frontmatter.schema.json).
- **Body (the explanation):** the need in plain words, how it is fulfilled, the governance
  floor, the aliases, and the promotion rule.

To author one, run [`../skills/library/author-capability/SKILL.md`](../skills/library/author-capability/SKILL.md); with no model available, fall back to [`_TEMPLATE.md`](_TEMPLATE.md).

## Proven vs candidate — the honest core

The distinction lives entirely in `fulfilled_by[].confidence`:

| | proven | candidate |
| --- | --- | --- |
| `pattern_key` | **required** | optional (may name a vendor in `note`) |
| `evidence` | **required** (build evidence) | omitted |
| `open_questions` | omitted | the spike questions that gate promotion |
| who sets it | a human, in PR review | the author/agent |

An agent writes `candidate` and **never** flips a fulfilment to `proven` or advances
`approval_status`. Promotion is a human PR that attaches spike evidence and a fulfilling
pattern meeting the governance floor.

## The three edges (key-citation, no foreign keys)

1. **requirement → capability** — a derived requirement adds `fulfils_capability: CAP-…`.
2. **capability → component** — `fulfilled_by[].pattern_key` cites the fulfilling pattern.
3. **component → capability** (optional back-ref) — a pattern may add `fulfils: [CAP-…]` so
   a reader on the pattern sees the need it serves.

The chain: outcome ← requirement (`fulfils_capability`) ← capability (`fulfilled_by`) ←
pattern.

## The governance floor

Every capability carries `governance_nfrs`: the minimum, **measurable** bar any fulfilling
pattern must meet or honestly waive. The `kind` is one of the same closed 11 NFR kinds the
patterns use ([`../patterns/_schema/nfr-kinds.enum.txt`](../patterns/_schema/nfr-kinds.enum.txt)).
A candidate's spike result is judged against this floor.

## Domains

The closed `capability_domain` enum
([`_schema/capability-domains.enum.txt`](_schema/capability-domains.enum.txt)):
`data` · `compute` · `integration` · `runtime` · `experience` · `governance`.

## Authored capabilities

| capability | domain | fulfilment |
| --- | --- | --- |
| [`CAP-OLAP`](data/olap.md) | data | proven — `PAT-LAKEHOUSE-DELTA` |
| [`CAP-OLTP`](data/oltp.md) | data | proven — `PAT-WEBAPP-PG` (Lakebase: candidate) |
| [`CAP-AGENT-RUNTIME`](runtime/agent-runtime.md) | runtime | OPEN — 3 candidates, spikes owed |

## How to author one

Run [`../skills/library/author-capability/SKILL.md`](../skills/library/author-capability/SKILL.md),
add the aliases to [`INDEX.md`](INDEX.md), then open the PR with the default PR template
(`.github/pull_request_template.md`), populating each field from the capability you authored.
The contribution flow is in [`../CONTRIBUTING.md`](../CONTRIBUTING.md). A capability enters as a
`candidate` via PR; a CODEOWNERS architect promotes it — the one structural human review.
