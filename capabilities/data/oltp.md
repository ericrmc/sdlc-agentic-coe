---
capability_key: CAP-OLTP
name: Online Transaction Processing (OLTP)
capability_domain: data
summary: >
  The need for a transactional system-of-record for a line-of-business application with
  strict data-residency, so operational reads and writes have a single in-region state
  authority. Fulfilled today by a containerised web + managed Postgres pattern.
need_statement: "A system needs a transactional system-of-record for a line-of-business application with strict data-residency, so that operational reads and writes have a single in-region state authority."
aliases:
  - transactional database
  - application database
  - operational store
  - system of record
  - managed Postgres
  - Lakebase / managed Postgres
  - CRUD backend
  - OLTP
fulfilled_by:
  - confidence: proven
    pattern_key: PAT-WEBAPP-PG
    note: "The managed-Postgres tier of this pattern IS the OLTP fulfilment: an in-region managed relational DB as the single state authority, with TLS-in-transit and data-residency NFRs already attached. No new pattern is needed for the proven seed."
    evidence:
      - {title: "Self-service portal rebuild — design note recommending this pattern", url: "https://github.com/sdlc-agentic-coe/seed-corpus/blob/main/self-service-portal/solution-design.md"}
  - confidence: candidate
    note: "Databricks Lakebase (managed Postgres). A future fulfilment to consider as it matures; recorded here so the candidate-vs-proven model is exercised for OLTP too."
    open_questions:
      - "Is it GA / mature enough for a line-of-business system-of-record OLTP workload?"
      - "How do its residency controls compare to a managed-Postgres service (region pinning, no cross-region replication by default)?"
governance_nfrs:
  - kind: data-residency
    statement: "Data at rest stays in the declared region."
    acceptance_criterion: "Managed store region == declared residency boundary; no cross-region replica configured."
  - kind: security
    statement: "TLS 1.2+ in transit to the store."
    acceptance_criterion: "All connections to the store negotiate TLS 1.2 or higher; verified by scan."
valid_from: "2026-06-15"
validity_check_months: 12
approval_status: provisional
approved_by: "@architects"
approved_at: "2026-06-15"
---

# Online Transaction Processing (OLTP) (`CAP-OLTP`)

> `approval_status: provisional` — reviewed, with one proven fulfilment carrying real
> evidence, pending a production reference build. A human advances it in PR review.

## The need

A system needs a transactional system-of-record for a line-of-business application with
strict data-residency, so that operational reads and writes have a single in-region state
authority. This is the need behind "a transactional database", "an application database",
"the system of record", "a CRUD backend", or "managed Postgres" — operational state with one
authoritative, in-region home.

OLTP is the operational counterpart to OLAP (`CAP-OLAP`): row-at-a-time reads and writes for
a running application, not analytical query over history. Naming the need technology-free
keeps the capability stable across a change of database product.

## How it is fulfilled

### Proven
- **`PAT-WEBAPP-PG`** — the managed-Postgres tier of this pattern is the OLTP fulfilment: an
  in-region managed relational database acting as the single state authority, with
  `data-residency` and `security` NFRs already attached. No separate pattern is needed — the
  existing pattern already carries this need. `confidence: proven`; evidence reuses the
  self-service-portal rebuild design cited on the pattern.

### Candidates (spikes owed)
- **Databricks Lakebase (managed Postgres)** — `confidence: candidate`, no pattern_key yet.
  A future fulfilment to watch as it matures. Open questions a spike must answer:
  - Is it GA / mature enough for a line-of-business system-of-record OLTP workload?
  - How do its residency controls compare to a managed-Postgres service (region pinning, no
    cross-region replication by default)?

## Governance floor

Any pattern fulfilling this capability must meet — or honestly waive — these bars.

- **data-residency** — data at rest stays in the declared region.
  _Acceptance:_ managed store region == declared residency boundary; no cross-region replica
  configured.
- **security** — TLS 1.2+ in transit to the store.
  _Acceptance:_ all connections to the store negotiate TLS 1.2 or higher; verified by scan.

## Aliases

Plain-language terms that resolve to this capability (these feed `capabilities/INDEX.md`):
transactional database, application database, operational store, system of record, managed
Postgres, Lakebase / managed Postgres, CRUD backend, OLTP.

## Promotion

This capability is `provisional`: its proven fulfilment carries a design-evidence artefact
but no production reference build yet, and Lakebase is a candidate owing a spike. Promoting
Lakebase to proven is a human PR that attaches spike evidence and a fulfilling pattern
meeting the governance floor, then flips `confidence: proven`. An agent never advances
`approval_status` or flips a fulfilment's `confidence`. See `CONTRIBUTING.md`.
