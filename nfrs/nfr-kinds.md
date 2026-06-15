# NFR Kinds — the closed `kind` vocabulary for pattern attached NFRs

This is the **closed 11-value vocabulary** used in the `kind` field of every entry in a
pattern's `attached_nfrs[]` list. A pattern attaches its governed non-functional
requirements as a small list of `{ kind, statement }` (optionally `acceptance_criterion`,
`measurable_target`) objects; the `kind` MUST be one of the eleven values below, spelled
exactly as shown (lowercase, hyphenated).

This file is the **human-readable mirror** of the machine-checked list at
[`patterns/_schema/nfr-kinds.enum.txt`](../patterns/_schema/nfr-kinds.enum.txt) — one
value per line, no glosses, the file the `validate-pattern-frontmatter` Action and the
`propagate-pattern-nfrs` / `nfr-coverage-check` skills read at runtime. **If the two ever
disagree, the `.enum.txt` file wins** (it is the source of truth the automation checks
against); keep this prose mirror in sync whenever the enum changes via PR.

---

## The eleven kinds

| `kind` | One-line gloss |
|---|---|
| `security` | Confidentiality, integrity, authn/authz, encryption in transit and at rest, network segmentation, secrets handling. |
| `availability` | Uptime / SLA targets, HA topology, single-point-of-failure elimination, failover and redundancy. |
| `performance` | Latency and throughput budgets (p95/p99, cold-start), response-time targets, capacity benchmarks. |
| `data-residency` | Where data physically lives at rest and is processed; in-region guarantees and region pinning. |
| `observability` | Logging, metrics, distributed tracing, correlation IDs, consumer-lag and health monitoring. |
| `resilience` | Behaviour under partial failure: retries, idempotency, at-least-once handling, dead-letter queues, graceful degradation. |
| `cost` | Spend efficiency: auto-termination, spot/preemptible use, right-sizing, cost-vs-RPS break-even, lifecycle/TTL to bound growth. |
| `compliance` | Regulatory and contractual obligations: data sovereignty, classification-to-region matching, approval/procurement gates, retention. |
| `scalability` | Ability to grow with load: horizontal scaling, statelessness, connection pooling, concurrency targets. |
| `data-governance` | Catalogued, classified, access-controlled data: PII tagging, column/row-level policies, governed perimeters around sensitive columns. |
| `operations` | Run-the-system concerns: patching, capacity planning, backup/restore, RACI for shared responsibility, runbooks. |

> **Closed set.** These eleven are exhaustive for now. A new kind is a deliberate,
> PR-reviewed change to *both* `patterns/_schema/nfr-kinds.enum.txt` and this file — not
> something an author invents inline. Pick the nearest existing kind before proposing a
> twelfth. (`data-residency` is the *physical-location* concern; `data-governance` is the
> *catalogue / classification / access-policy* concern; `compliance` is the *regulatory
> obligation* that may cite either.)

---

## Why it is closed (and how it got that way)

These kinds were **promoted from open-ended seed strings to a fixed list**. In the original
bespoke app the `attached_nfrs` column was free JSON, and the `kind` was whatever the seed
author happened to type. That worked for a demo but is hostile to automation: any two
patterns could spell the same concept differently (`"perf"` vs `"performance"`,
`"data residency"` vs `"data-residency"`), and a coverage check can't tell whether a
project's NFR set is missing *security* if "security" isn't a value it can count on.

Freezing the vocabulary buys two deterministic behaviours that the rest of the CoE depends on:

- **`propagate-pattern-nfrs`** — when a project adopts a pattern, this skill turns each
  `attached_nfrs[]` entry into a derived non-functional requirement on the project. A closed
  `kind` means the propagated requirement carries a *stable, groupable* category, so two
  patterns contributing `security` NFRs land in the same bucket instead of three near-synonyms.
- **`nfr-coverage-check`** — this skill compares a project's NFRs against the eleven kinds and
  reports which categories are unaddressed. It can only be deterministic if the universe of
  kinds is fixed and enumerable. An open string set makes "is *resilience* covered?" unanswerable.

Both run as plain markdown-reading skills and (where wired) as PR Actions, so determinism is
the whole point: the same inputs must always yield the same coverage verdict and the same
propagated set, with no model creativity in the `kind` field.

---

## Origin: the seed patterns

The eleven values are the **distinct `kind`s observed across the seed solution patterns** —
they were lifted directly from the patterns that ship as worked examples, not invented in the
abstract. The seeds, and the kinds each one attaches:

| Seed pattern | Kinds it attaches |
|---|---|
| Three-tier web app on managed Postgres | `security`, `availability`, `data-residency`, `scalability` |
| Event-driven ingestion (Kafka / broker) | `availability`, `security`, `observability`, `resilience` |
| Governed lakehouse (Unity Catalog) | `data-governance`, `security`, `compliance`, `cost` |
| Serverless API (CDN + functions + gateway) | `availability`, `performance`, `security`, `cost` |
| Client-managed on-prem / VM deployment | `compliance`, `availability`, `operations`, `security` |
| API-gateway + BFF (token / tracing) | `security`, `observability`, `availability`, `scalability` |

Taking the union of those rows yields exactly the eleven kinds above — every kind in the
vocabulary is *evidenced by at least one shipped pattern*, and every shipped pattern's `kind`s
are *all in the vocabulary*. That round-trip is the invariant the
`validate-pattern-frontmatter` Action enforces on every pattern PR: each `attached_nfrs[].kind`
must be a member of `patterns/_schema/nfr-kinds.enum.txt`, or the check fails the PR with the
offending value named.

---

## Example: an NFR block using the vocabulary

```yaml
attached_nfrs:
  - kind: security
    statement: "TLS 1.2+ in transit between tiers and to managed Postgres"
    acceptance_criterion: "All inter-tier connections present a cert chain to TLS >= 1.2; verified by scan"
  - kind: availability
    statement: "99.9% monthly SLA achievable with multi-AZ container placement"
    measurable_target: "99.9% monthly"
  - kind: data-residency
    statement: "Data at rest stays in declared region; verify managed Postgres region setting"
  - kind: scalability
    statement: "Horizontal container scaling; DB connection pool required (e.g. PgBouncer)"
```

Each entry propagates into an adopting project as one derived non-functional requirement,
grouped by its `kind`; the coverage check then reports this pattern as contributing toward
`security`, `availability`, `data-residency`, and `scalability` — and flags the other seven
kinds as still needing project-level attention if nothing else covers them.

---

## Maintaining the vocabulary

1. Open a PR that edits **both** [`patterns/_schema/nfr-kinds.enum.txt`](../patterns/_schema/nfr-kinds.enum.txt)
   (the machine list) and this file (the prose mirror) in the same change.
2. State in the PR description which existing kind was insufficient and why the nearest
   neighbour doesn't fit — the bar for a new kind is deliberately high.
3. A human reviews and merges. The change is **advisory, not gated**: no state machine blocks
   it, but the `validate-pattern-frontmatter` Action will start enforcing the new value against
   every pattern on the next PR, so land the enum change before any pattern that uses the new
   kind.
