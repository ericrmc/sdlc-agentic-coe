<!-- GENERATED FILE — DO NOT EDIT.
     Built by skills/_scripts/concat_skills.py from the sources listed below.
     Edit the source skill/pattern files and re-run the concat-patterns Action.
     This file is marked linguist-generated in .gitattributes. -->

# Component patterns — combined catalogue

> Generated bundle. Built 2026-06-15 by `skills/_scripts/concat_skills.py`.

The whole component-pattern library in one paste-able file, one entry per category (deployment / integration / data). Each entry keeps its own pattern_key, approval_status, validity / review-by metadata, attached NFRs and evidence in its frontmatter — read those before adopting. Superseded or deprecated patterns are still included so you can see what replaced what; check the status field. This is a generated view; PR-review and edit the individual pattern files, not this bundle.

## Bundled sources

- `patterns/deployment/containerised-web-managed-postgres.md`
- `patterns/integration/api-gateway-bff-managed-identity.md`
- `patterns/data/databricks-lakehouse-delta.md`


---

## Source: `patterns/deployment/containerised-web-managed-postgres.md`

<details><summary>frontmatter</summary>

```yaml
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
fulfils: [CAP-OLTP]
constraints:
  - {statement: "DB connection pool (e.g. PgBouncer) required", enforced: hard}
attached_nfrs:
  - {kind: security, statement: "TLS 1.2+ in transit between tiers and to managed Postgres", acceptance_criterion: "All inter-tier and DB connections negotiate TLS 1.2 or higher"}
  - {kind: availability, statement: "99.9% monthly SLA via multi-AZ container placement", acceptance_criterion: "Containers placed across >=2 AZs; measured monthly availability >= 99.9%"}
  - {kind: data-residency, statement: "Data at rest stays in the declared region", acceptance_criterion: "Managed Postgres region setting matches the declared residency boundary"}
  - {kind: scalability, statement: "Horizontal container scaling with a DB connection pool", acceptance_criterion: "Web tier scales to N replicas behind the LB with pooled DB connections"}
evidence:
  - {title: "Self-service portal rebuild — design note recommending this pattern", url: "https://github.com/sdlc-agentic-coe/seed-corpus/blob/main/self-service-portal/solution-design.md", kind: doc, project: "self-service-portal-rebuild"}
```

</details>

## Containerised web + managed Postgres (`PAT-WEBAPP-PG`)

> **`approval_status: provisional`** — reviewed and usable with
> care; its evidence is a real design-note adoption pending a production reference build,
> at which point a CODEOWNER may promote it to `approved`. Advisory, not enforced — a
> recommendation to weigh against the project's requirements, not a gate to pass.

### Summary

Stateless web tier behind a load balancer with a managed relational store. Scale-out is
horizontal (container replicas); the DB is the single state authority. Suitable for
line-of-business apps with moderate throughput and strict data-residency.

The deployment topology is a **single-region container service** (e.g. Kubernetes, ECS)
plus a **managed Postgres instance**. Data placement is an **in-region managed relational
DB with no cross-region replication by default**, which is what makes this pattern a clean
fit when residency is contractual rather than best-effort.

### When to use

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

### Attached NFRs

The four NFRs travel with this pattern. Each kind maps to the closed 11-value NFR enum
(`security`, `availability`, `data-residency`, `scalability`).

| Kind | Statement | Acceptance criterion |
| --- | --- | --- |
| **security** | TLS 1.2+ in transit between tiers and to managed Postgres | All inter-tier and DB connections negotiate TLS 1.2 or higher |
| **availability** | 99.9% monthly SLA via multi-AZ container placement | Containers placed across >=2 AZs; measured monthly availability >= 99.9% |
| **data-residency** | Data at rest stays in the declared region | Managed Postgres region setting matches the declared residency boundary |
| **scalability** | Horizontal container scaling with a DB connection pool | Web tier scales to N replicas behind the LB with pooled DB connections |

### Trade-offs

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

### Evidence of having been built

- [Self-service portal rebuild — design note recommending this pattern](https://github.com/sdlc-agentic-coe/seed-corpus/blob/main/self-service-portal/solution-design.md)
  — the engagement that recommended and accepted this topology for an in-region managed
  Postgres deployment (the `evidence` entry in the frontmatter).

> **Note:** this is a real adoption-decision artefact, which is why the pattern is
> `provisional` rather than `candidate`. A full **production reference build / load-test
> report** is the evidence a CODEOWNER will attach to promote it to `approved`. Re-check
> validity by the next-review date the lifecycle Action computes from `valid_from +
> validity_check_months` (12 months) — it is advisory and never blocks adoption.

### References

- Provenance: a real in-region managed-Postgres deployment design; see the adoption-decision
  artefact linked in `evidence`.
- Real-world fit: a self-service-portal rebuild project recommended and accepted
  this pattern for an in-region (UK-South) managed Postgres deployment with a 99.9% SLA and
  ~400-user horizontal scaling target — the residency constraint was a hard contractual
  requirement, which is exactly the situation this pattern is built for.


---

## Source: `patterns/integration/api-gateway-bff-managed-identity.md`

<details><summary>frontmatter</summary>

```yaml
pattern_key: PAT-APIGW-BFF
name: API gateway + managed identity + backend-for-frontend
category: integration
intent: "use WHEN a multi-client product portfolio needs consolidated auth/rate-limiting/observability so that a gateway + per-client BFF mediates all auth and downstream calls"
deployment_topology: API gateway (APIM/Kong) fronting microservices; BFF layer per client type; Entra/OIDC for identity
data_placement: No client receives raw service tokens; the BFF mediates all auth flows and downstream calls
summary: Consolidates cross-cutting concerns at the gateway; a BFF reshapes responses per client; suitable for multi-client (web/mobile/partner) portfolios.
approval_status: provisional
approved_by: "@architects"
approved_at: "2026-06-15"
valid_from: "2026-06-15"
validity_check_months: 12
evidence:
  - {title: "Multi-client web project — recorded gateway/BFF adoption decision (with override)", url: "https://github.com/sdlc-agentic-coe/seed-corpus/blob/main/multi-client-web/adoption-decision.md", kind: doc, project: "multi-client-web"}
constraints:
  - {statement: "BFF must be stateless; session affinity disabled", enforced: hard}
attached_nfrs:
  - {kind: security, statement: "All tokens short-lived; refresh-token rotation mandatory", acceptance_criterion: "Access tokens expire <=1h; refresh rotation enforced"}
  - {kind: observability, statement: "Distributed tracing through gateway and BFF; correlation IDs required", acceptance_criterion: "Every request carries a correlation ID traced end-to-end"}
  - {kind: availability, statement: "Gateway is a SPOF; active-active with health checks required", acceptance_criterion: "Gateway runs active-active across >=2 nodes with health checks"}
  - {kind: scalability, statement: "BFF stateless; session affinity disabled at the gateway", acceptance_criterion: "BFF instances are interchangeable; no sticky sessions"}
```

</details>

## API gateway + managed identity + backend-for-frontend (`PAT-APIGW-BFF`)

> Integration pattern. **`approval_status: provisional`** — reviewed and usable with care; its
> evidence is a real recorded adoption decision (including the worked override below) pending a
> production reference build. **Advisory, not enforced** — recommend it, adopt it, or override it
> with a recorded reason. Nothing in this Centre of Excellence blocks a project from choosing
> otherwise; it only asks that the *why* be written down.

### Summary

Consolidates cross-cutting concerns (auth, rate limiting, observability) at the gateway. A backend-for-frontend (BFF) aggregates and reshapes service responses per client. Suitable for multi-client (web, mobile, partner) product portfolios.

The deployment topology is an **API gateway (APIM / Kong) fronting microservices**, with a **BFF layer per client type**, and **Entra/OIDC for identity**. On data placement: **no client receives raw service tokens; the BFF mediates all auth flows and downstream calls.**

### When to use

Reach for this pattern when you have a **multi-client product portfolio** — web, mobile, and partner clients consuming the same underlying services — and you want one place to enforce authentication, rate limiting, and observability rather than re-implementing those concerns in every service.

- **Use it WHEN:** several client types share a backend and each needs a slightly different response shape; cross-cutting auth/rate-limiting/tracing should be consolidated; clients must never hold raw service tokens.
- **Use it WHEN:** identity is centralised (Entra/OIDC) and you want the gateway + BFF to mediate every downstream call so the client surface stays thin.

### Attached NFRs

These four NFRs ride with the pattern. Adopt the pattern and you inherit them; each carries a measurable acceptance criterion so a downstream project can check it later. Kinds are drawn from the closed enum: `security`, `observability`, `availability`, `scalability`.

| Kind | Statement | Acceptance criterion |
|---|---|---|
| `security` | All tokens are short-lived; refresh-token rotation mandatory | Access tokens expire `<=1h`; refresh rotation enforced |
| `observability` | Distributed tracing through gateway and BFF; correlation IDs required | Every request carries a correlation ID traced end-to-end |
| `availability` | Gateway is a SPOF; active-active with health checks required | Gateway runs active-active across `>=2` nodes with health checks |
| `scalability` | BFF must be stateless; session affinity disabled at the gateway | BFF instances are interchangeable; no sticky sessions |

### Trade-offs

- **The gateway is a single point of failure.** Everything flows through it, so an outage takes the whole portfolio down. *Mitigate with active-active* across at least two nodes with health checks (see the `availability` NFR). This is the price of consolidating cross-cutting concerns in one tier.
- **A BFF per client type adds tiers to run and review.** More services means more deployment surface, more network paths, and — in regulated shops — more security review. That cost is real and is exactly what the override example below pushes back on.
- **Statelessness is non-negotiable for scale.** The BFF must hold no session state and session affinity must be disabled at the gateway (the `scalability` NFR + the hard constraint), otherwise instances stop being interchangeable and you lose horizontal scaling.

### Adoption & overrides

This pattern is **recommended, never mandated**. A project may adopt it as-is, adopt it partially, or decline it — and declining is a first-class, honest signal as long as the reason is recorded. The Centre of Excellence values a well-reasoned non-adoption as much as an adoption: it tells the next team *why* the obvious choice was the wrong one here.

#### Worked override example (real, from the seed corpus)

A multi-client web project mapped cleanly onto this pattern — **Azure Application Gateway + Entra SSO**, with a BFF layer that would have neatly separated the admin and customer views. The agent recommended it. But the client could not take it:

- **Recommended:** API gateway + managed identity + BFF (this pattern).
- **Blocker:** the **client IT security policy prohibited a separate BFF service tier** (additional service tiers triggered a separate network-level security review the client would not sanction).
- **Chosen alternative:** **"path-prefix routing within a single container (no separate BFF service), `/admin` protected by an Entra role claim at the application layer."**

So instead of a dedicated BFF service, the admin and customer surfaces live in one container, separated by path prefix, with `/admin` gated by an Entra role claim at the application layer rather than at a network tier. The security intent (only admins reach admin) is preserved; the tier count is reduced to satisfy the policy.

#### How this gets recorded

This override would be recorded in **`adoptions/ledger.jsonl`** as one line with **`disposition: overridden-out`** and the reason above — a ready demonstration of capturing *why a recommended pattern was declined*:

```jsonl
{"pattern_key": "PAT-APIGW-BFF", "repo": "acme/citizen-portal", "disposition": "overridden-out", "at": "2026-06-13", "override_reason": "Client IT security policy prohibits additional service tiers that require separate network-level security review; chose path-prefix routing within a single container (/admin protected by an Entra role claim at the application layer).", "override_count": 1}
```

(This is exactly the line already recorded in `adoptions/ledger.jsonl` for this pattern.)

Nothing here blocks the project — the ledger line *is* the governance: lightweight, append-only, and honest about what was not adopted and why.

### Example / artefacts

- **Reference topology:** Azure Application Gateway (L7, WAF) → microservices, with a per-client BFF and Entra/OIDC identity. The gateway holds auth, rate limiting, and tracing; the BFF reshapes responses per client and is the only thing that ever touches raw service tokens.
- **Evidence of adoption:** see the `evidence` entry in this file's frontmatter — the recorded gateway/BFF adoption decision (with override) on the multi-client web engagement. Patterns in this library are PR-reviewed by a human; a CODEOWNER attaches a production reference build to promote this from `provisional` to `approved`.
- **Override evidence:** the worked example above, drawn from the seed corpus, is the artefact for the non-adoption path — it shows the `overridden-out` ledger shape end to end.

### References

- Closed NFR kind vocabulary: `nfrs/nfr-kinds.md` (this pattern attaches `security`, `observability`, `availability`, `scalability`).
- Adoption ledger: `adoptions/ledger.jsonl` (append-only; `disposition` ∈ `adopted-clean` | `adopted-with-overrides` | `overridden-out`) — see `adoptions/README.md`.
- Validity: re-reviewed every `validity_check_months` (12). When retired, set `approval_status: deprecated` + `superseded_by: <key>`, and optionally a `sunset_at` date — the pattern is deprecated, never deleted, because it has a recorded adoption.


---

## Source: `patterns/data/databricks-lakehouse-delta.md`

<details><summary>frontmatter</summary>

```yaml
pattern_key: PAT-LAKEHOUSE-DELTA
name: Databricks Lakehouse + Delta Lake
category: data
intent: "use WHEN building analytics / ML feature engineering on regulated data so that Unity Catalog governs data with column-level PII control inside a governed perimeter"
deployment_topology: Databricks workspace (Unity Catalog) in a governed region; Delta tables in cloud object storage
data_placement: Unity Catalog governs data; PII tagged at column level; no data leaves the Unity Catalog boundary
summary: Batch and streaming analytics on Delta Lake tables managed via Unity Catalog; governance, lineage, and RBAC are UC-native.
approval_status: provisional
approved_by: "@architects"
approved_at: "2026-06-15"
valid_from: "2026-06-15"
validity_check_months: 12
fulfils: [CAP-OLAP]
constraints:
  - {statement: "No external model call may read PII columns", enforced: hard}
  - {statement: "Cluster auto-termination required", enforced: soft}
evidence:
  - {title: "Governed-lakehouse EDW migration — solution design with UC governance NFRs", url: "https://github.com/sdlc-agentic-coe/seed-corpus/blob/main/edw-migration/solution-design.md", kind: doc, project: "edw-lakehouse-migration"}
attached_nfrs:
  - {kind: data-governance, statement: "Unity Catalog column-level PII tagging; row-level filter policies", acceptance_criterion: "PII columns carry UC tags and row-level policies are enforced"}
  - {kind: security, statement: "No external model call may read PII columns; governed perimeter enforced", acceptance_criterion: "External serving paths are denied access to PII-tagged columns"}
  - {kind: compliance, statement: "Workspace region must match data classification", acceptance_criterion: "Workspace region == declared data-classification region"}
  - {kind: cost, statement: "Cluster auto-termination; spot/preemptible workers for batch", acceptance_criterion: "Idle clusters auto-terminate; batch jobs use spot workers"}
```

</details>

## Databricks Lakehouse + Delta Lake (`PAT-LAKEHOUSE-DELTA`)

> **`approval_status: provisional`** — reviewed and usable with care; its evidence is a real
> governed-lakehouse migration design pending a production reference build. This
> is a strong **data/AI-governance-aware exemplar**: governance, lineage, and access control are
> native to the platform rather than bolted on, and every attached NFR is phrased as a checkable
> acceptance criterion. Use it as the reference for how a regulated data/AI pattern should attach
> governance up front.

### Summary

Batch and streaming analytics on Delta Lake tables managed via Unity Catalog. Governance, lineage, and RBAC are Unity Catalog-native. Suitable for analytics, ML feature engineering, and regulated data products.

The deployment topology is a Databricks workspace (Unity Catalog) in a governed region, with Delta tables in cloud object storage. Data placement is the point of the pattern: Unity Catalog governs the data, PII is tagged at the column level, and no data leaves the Unity Catalog boundary.

### When to use

- **Analytics** — batch and streaming workloads over Delta tables where you want governed, lineage-tracked SQL and BI access rather than ungoverned extracts.
- **ML feature engineering** — building and serving feature tables where the same column-level governance must follow the data into training and inference.
- **Regulated data products** — any data product where residency, PII handling, and access control are auditable requirements, and where keeping data inside a single governed perimeter is a compliance asset rather than just an architectural preference.

Reach for this pattern when the *governance posture* is part of the requirement, not an afterthought — when "who can read which column, in which region, and can a model see it" must be answerable and enforceable.

### Attached NFRs

These four NFRs travel **with** the pattern, mapped to the closed enum (`data-governance`, `security`, `compliance`, `cost`). The fact that the pattern arrives pre-loaded with concrete, measurable governance NFRs is what makes it a good data/AI-governance exemplar.

| Kind | Statement | Acceptance criterion |
| --- | --- | --- |
| `data-governance` | Unity Catalog column-level PII tagging; row-level filter policies | PII columns carry UC tags and row-level policies are enforced |
| `security` | No external model call may read PII columns; governed perimeter enforced | External serving paths are denied access to PII-tagged columns |
| `compliance` | Workspace region must match data classification | Workspace region == declared data-classification region |
| `cost` | Cluster auto-termination; spot/preemptible workers for batch | Idle clusters auto-terminate; batch jobs use spot workers |

The `security` NFR ("no external model call may read PII columns") is the one that makes this an **AI-governance** pattern and not merely a data-governance one: it draws the perimeter around model access explicitly, so an LLM/ML serving path cannot exfiltrate tagged columns out of the governed boundary.

### When NOT to use

- Small, non-regulated, or single-tenant analytics where the operational weight of a governed Lakehouse exceeds the value of its governance.
- Workloads that genuinely need data to leave the Unity Catalog boundary — that conflicts with the data-placement premise and the `security` perimeter NFR.
- Pure low-latency transactional (OLTP) serving — this is an analytics/feature-engineering lakehouse, not an operational database.

### Trade-offs

- **Governance is Unity-Catalog-native.** This is the headline upside: tagging, lineage, and RBAC are properties of the platform, so the governance NFRs above are enforced *in place* rather than reconstructed in application code. The flip side is platform lock-in to Unity Catalog as the governance plane — the pattern assumes UC is your system of record for who-can-see-what.
- **Cost discipline is required.** Cluster compute is the dominant cost and it is easy to leave running. The `cost` NFR is not decorative: auto-termination on idle clusters and spot/preemptible workers for batch jobs are the difference between an economical lakehouse and a runaway bill. Treat the cost NFR as a build-time check, not an aspiration.
- **Residency couples region to classification.** The `compliance` NFR ties the workspace region to the declared data classification. That keeps you compliant but reduces deployment flexibility — multi-region or cross-region designs need a workspace (and governance scope) per region.
- **Perimeter is only as strong as the tags.** The `security` and `data-governance` NFRs both depend on PII actually being tagged at the column level. Untagged PII silently escapes the row-level/column-level policies, so column tagging has to be part of ingestion, not a later sweep.

### Example / artefacts

- [Governed-lakehouse EDW migration — solution design with UC governance NFRs](https://github.com/sdlc-agentic-coe/seed-corpus/blob/main/edw-migration/solution-design.md)
  — the recorded adoption-decision artefact (the `evidence` entry in the frontmatter). A
  CODEOWNER attaches a production reference build to promote this from `provisional` to `approved`.
- A representative real-world shape this pattern fits: migration of a ~10TB on-prem EDW to a Databricks Lakehouse on Unity Catalog with BI (e.g. Power BI) on top — a governed analytics estate rather than a lift-and-shift of ungoverned extracts.

### References

- Based on a governed-lakehouse migration design; provenance is the adoption-decision artefact in `evidence`.
- Unity Catalog: column/row-level access policies, tagging, and lineage.
- Delta Lake: ACID tables on cloud object storage for batch + streaming.

---

*Light/advisory. This pattern recommends and attaches NFRs; it does not gate. A downstream project adopts it by reference and is responsible for checking the four acceptance criteria during its own build. The lifecycle Action computes a next-review date from `valid_from + validity_check_months` (12 months) and opens an advisory revalidation issue when it arrives; it never blocks.*
