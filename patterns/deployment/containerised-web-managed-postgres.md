---
pattern_key: PAT-WEBAPP-PG
name: Containerised web + managed Postgres
category: deployment
intent: "use WHEN a line-of-business app needs moderate throughput with strict data-residency so that a stateless web tier scales horizontally over a single managed relational state authority"
deployment_topology: Single-region container service (Kubernetes/ECS) + managed Postgres instance
data_placement: In-region managed relational DB; no cross-region replication by default
summary: Stateless web tier behind a load balancer with a managed relational store; horizontal scale-out; the DB is the single state authority.
approval_status: provisional
approved_by: "@architects"
approved_at: "2026-06-15"
valid_from: "2026-06-15"
validity_check_months: 12
constraints:
  - {statement: "DB connection pool (e.g. PgBouncer) required", enforced: hard}
attached_nfrs:
  - {kind: security, statement: "TLS 1.2+ in transit between tiers and to managed Postgres", acceptance_criterion: "All inter-tier and DB connections negotiate TLS 1.2 or higher"}
  - {kind: availability, statement: "99.9% monthly SLA via multi-AZ container placement", acceptance_criterion: "Containers placed across >=2 AZs; measured monthly availability >= 99.9%"}
  - {kind: data-residency, statement: "Data at rest stays in the declared region", acceptance_criterion: "Managed Postgres region setting matches the declared residency boundary"}
  - {kind: scalability, statement: "Horizontal container scaling with a DB connection pool", acceptance_criterion: "Web tier scales to N replicas behind the LB with pooled DB connections"}
evidence:
  - {title: "Self-service portal rebuild — design note recommending this pattern", url: "https://github.com/sdlc-agentic-coe/seed-corpus/blob/main/self-service-portal/solution-design.md", kind: doc, project: "self-service-portal-rebuild"}
---

# Containerised web + managed Postgres (`PAT-WEBAPP-PG`)

> Seed pattern, converted. **`approval_status: provisional`** — reviewed and usable with
> care; its evidence is a real design-note adoption pending a production reference build,
> at which point a CODEOWNER may promote it to `approved`. Advisory, not enforced — a
> recommendation to weigh against the project's requirements, not a gate to pass.

## Summary

Stateless web tier behind a load balancer with a managed relational store. Scale-out is
horizontal (container replicas); the DB is the single state authority. Suitable for
line-of-business apps with moderate throughput and strict data-residency.

The deployment topology is a **single-region container service** (e.g. Kubernetes, ECS)
plus a **managed Postgres instance**. Data placement is an **in-region managed relational
DB with no cross-region replication by default**, which is what makes this pattern a clean
fit when residency is contractual rather than best-effort.

## When to use

- **Line-of-business apps** — internal portals, self-service workflows, admin tooling, and
  similar CRUD-heavy applications where a relational store is the natural system of record.
- **Moderate throughput** — workloads served comfortably by a horizontally scaled web tier
  in front of a single managed relational database; you are not (yet) at a scale that forces
  data partitioning or a polyglot persistence story.
- **Strict data-residency** — the data must demonstrably stay inside a declared region. The
  default "no cross-region replication" posture makes the residency claim easy to assert and
  to verify against the managed Postgres region setting.

If throughput outgrows what one managed relational authority can serve, or the domain wants
to decouple producers from consumers, look at an event-driven / message-broker pattern
instead.

## Attached NFRs

The four NFRs travel with this pattern. Each kind maps to the closed 11-value NFR enum
(`security`, `availability`, `data-residency`, `scalability`).

| Kind | Statement | Acceptance criterion |
| --- | --- | --- |
| **security** | TLS 1.2+ in transit between tiers and to managed Postgres | All inter-tier and DB connections negotiate TLS 1.2 or higher |
| **availability** | 99.9% monthly SLA via multi-AZ container placement | Containers placed across >=2 AZs; measured monthly availability >= 99.9% |
| **data-residency** | Data at rest stays in the declared region | Managed Postgres region setting matches the declared residency boundary |
| **scalability** | Horizontal container scaling with a DB connection pool | Web tier scales to N replicas behind the LB with pooled DB connections |

## Trade-offs

- **The DB is the single state authority.** All durable state lives in the one managed
  Postgres instance. This keeps reasoning simple and makes the residency claim verifiable,
  but it also makes the database the consistency bottleneck and the thing you scale (read
  replicas, vertical sizing) when the web tier alone is no longer enough. There is no
  second source of truth to fall back on, so backup/restore and failover for that one
  instance carry the whole reliability story.
- **Connection pooling is mandatory.** Because the web tier scales horizontally (many
  container replicas) over a single database, raw per-replica connections will exhaust
  Postgres connection limits well before the web tier hits its own ceiling. A pooler
  (e.g. PgBouncer, or the managed service's built-in pooling) is a hard constraint, not a
  tuning nicety — it is the mechanism that lets "scale out the web tier" and "single DB
  authority" coexist.

## Evidence of having been built

- [Self-service portal rebuild — design note recommending this pattern](https://github.com/sdlc-agentic-coe/seed-corpus/blob/main/self-service-portal/solution-design.md)
  — the engagement that recommended and accepted this topology for an in-region managed
  Postgres deployment (the `evidence` entry in the frontmatter).

> **Note:** this is a real adoption-decision artefact, which is why the pattern is
> `provisional` rather than `candidate`. A full **production reference build / load-test
> report** is the evidence a CODEOWNER will attach to promote it to `approved`. Re-check
> validity by the next-review date the lifecycle Action computes from `valid_from +
> validity_check_months` (12 months) — it is advisory and never blocks adoption.

## References

- Converted verbatim-in-substance from seed pattern 1 (`solution_pattern`,
  "Containerised web + managed Postgres", category `deployment`) in the original
  SDLC-companion app.
- Real-world fit: the seed self-service-portal rebuild project recommended and accepted
  this pattern for an in-region (UK-South) managed Postgres deployment with a 99.9% SLA and
  ~400-user horizontal scaling target — the residency constraint was a hard contractual
  requirement, which is exactly the situation this pattern is built for.
