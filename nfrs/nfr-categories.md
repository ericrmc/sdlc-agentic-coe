# NFR Coverage Categories

The six **canonical NFR coverage categories**, in fixed order. This is the
*assessment axis* — the checklist a project's requirement set is checked
against. Every coverage assessment returns exactly one result per category
below: addressed or not, in this order, with no category added, dropped, or
renamed.

These categories are **advisory**. They surface gaps and propose text to close
them; they never block, delete scope, or change a requirement's status. A human
accepts or dismisses every gap.

| # | category | one-line definition |
|---|----------|---------------------|
| 1 | `security` | Transport security, authentication, and secrets handling. |
| 2 | `availability` | Uptime SLA plus recovery objectives (RPO/RTO). |
| 3 | `performance` | Response-time / latency / throughput targets. |
| 4 | `data_residency` | Where data lives and the regional boundary it stays within. |
| 5 | `maintainability` | Test coverage, observability, logging, documentation. |
| 6 | `scalability` | Concurrency, load, horizontal scale, tenancy. |

## How these are used

These six names are the fixed vocabulary for two skills:

- **`nfr-coverage-check`** — assesses the requirement set and returns one item
  per category, in this order. Each item carries `category`, `addressed`,
  `requirement_ids` (the real ids that cover it, empty when none do),
  `suggested_text` (one concrete, numeric `NF` requirement to close the gap when
  `addressed` is false — otherwise null), and `note` (the category's one-line
  definition from the table above).
- **`red-team-requirements`** — when it raises a `missing_nfr` challenge (an
  entire category is uncovered, a set-level gap), the category name MUST be one
  of these six and nothing else.

Use only these six names. Do not invent categories, add none, drop none.

## Worked sample targets

To make each axis concrete, a sample measurable target per category. These are
illustrations of the *shape* of a good `NF` requirement (always carries a
number/target and the consequence of breach) — not mandates.

| category | sample measurable target |
|----------|--------------------------|
| `security` | All transport uses TLS 1.2+; secrets held in a managed vault, never in source or config; auth via the platform IdP with MFA enforced. |
| `availability` | 99.9% monthly uptime SLA; RPO <= 15 min, RTO <= 1 hour; documented and tested recovery runbook. |
| `performance` | p95 API response <= 500 ms at expected load; sustained throughput >= 50 req/s; defined degradation behaviour past that. |
| `data_residency` | All customer and project data — including backups and logs — remains within the designated regional boundary at all times. |
| `maintainability` | >= 80% test coverage on core logic; structured logging with correlation ids; metrics + alerting on the golden signals; current runbook + architecture doc. |
| `scalability` | Handles N concurrent tenants and a 3x load spike via horizontal scale with no code change; tenancy isolation documented. |

## Not to be confused with the pattern NFR kinds

The six categories above are the **coverage axis** — the lens for assessing
whether a *requirement set* is complete.

They are a **separate but related** vocabulary from the pattern `attached_nfr`
**KIND** list, which is the longer 11-value enumeration in
[`nfrs/nfr-kinds.md`](./nfr-kinds.md) (mirrored machine-side in
[`patterns/_schema/nfr-kinds.enum.txt`](../patterns/_schema/nfr-kinds.enum.txt),
the single source the schema and linter read). That list describes which NFR
concerns a reusable **component pattern** has been built and validated against —
a property of a pattern, not a coverage result on a project.

The six coverage categories are a **labelled subset of the eleven pattern
kinds** — a coarser assessment lens that rolls several kinds together. They map
onto the canonical kinds as follows (the kind names are the **hyphen** form —
`data-residency`, never `data_residency` — which is the one canonical spelling
the schema and pattern files use):

| coverage category (this file) | canonical pattern kind(s) it rolls up (`nfrs/nfr-kinds.md`) |
|---|---|
| `security` | `security` |
| `availability` | `availability` (+ `resilience` for recovery objectives) |
| `performance` | `performance` |
| `data_residency` | `data-residency` (+ `compliance`/`data-governance` where residency is a regulatory/catalogue obligation) |
| `maintainability` | `observability` + `operations` |
| `scalability` | `scalability` |

> **Spelling note.** This coverage axis keeps the `data_residency` (underscore)
> token only because the `nfr-coverage-check` and `red-team-requirements` skills
> parse it as a fixed category id. The **pattern** vocabulary is the canonical
> one, and it is **hyphenated** (`data-residency`). When you cross from coverage
> into a pattern's `attached_nfrs`, use the hyphen form — that is what the schema
> and linter enforce.

Keep them distinct:

- **coverage categories** (this file, 6 values) — the assessment axis for a
  project's requirements; a labelled subset/roll-up of the kinds below.
- **pattern NFR kinds** (`nfrs/nfr-kinds.md` + `patterns/_schema/nfr-kinds.enum.txt`,
  11 hyphenated values) — the canonical tag vocabulary on a component pattern's
  `attached_nfrs`, enforced by the schema and the pattern linter.
