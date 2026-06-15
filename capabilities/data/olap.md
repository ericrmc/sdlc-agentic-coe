---
capability_key: CAP-OLAP
name: Online Analytical Processing (OLAP)
capability_domain: data
summary: >
  The need to answer analytical and BI queries over large historical datasets with
  governance and lineage, so regulated analytics and ML feature engineering stay inside
  an auditable perimeter. Fulfilled today by a governed lakehouse pattern.
need_statement: "A system needs to answer analytical and BI queries over large historical datasets, with governance and lineage, so that regulated analytics and ML feature engineering stay inside an auditable perimeter."
aliases:
  - data warehouse
  - data analytics platform
  - analytics store
  - EDW
  - reporting database
  - BI backend
  - big-data query
  - OLAP
fulfilled_by:
  - confidence: proven
    pattern_key: PAT-LAKEHOUSE-DELTA
    note: "A governed lakehouse fulfils this cleanly — its attached NFRs (data-governance, security, compliance, cost) already meet the governance floor; column-level access control and lineage are platform-native rather than bolted on."
    evidence:
      - {title: "Governed-lakehouse EDW migration — solution design with governance NFRs", url: "https://github.com/sdlc-agentic-coe/seed-corpus/blob/main/edw-migration/solution-design.md"}
governance_nfrs:
  - kind: data-governance
    statement: "Data is catalogued with column-level access control on sensitive columns; PII columns carry policies enforced at query time."
    acceptance_criterion: "Sensitive columns carry catalogue tags and access policies; a query by an unauthorised principal is denied at query time."
  - kind: compliance
    statement: "Processing region matches the data classification."
    acceptance_criterion: "Processing region == declared classification region."
  - kind: security
    statement: "No external or model-serving path may read sensitive columns."
    acceptance_criterion: "External serving paths are denied access to columns tagged sensitive."
valid_from: "2026-06-15"
validity_check_months: 12
approval_status: provisional
approved_by: "@architects"
approved_at: "2026-06-15"
---

# Online Analytical Processing (OLAP) (`CAP-OLAP`)

> `approval_status: provisional` — reviewed, with one proven fulfilment that carries real
> evidence, pending a production reference build. A human advances it in PR review.

## The need

A system needs to answer analytical and BI queries over large historical datasets, with
governance and lineage, so that regulated analytics and ML feature engineering stay inside
an auditable perimeter. This is the need behind every request for "a data warehouse", "an
EDW", "a reporting store", or "somewhere to run our BI" — the words differ, the need is one:
governed analytical query over a large, historical, often-sensitive dataset.

The need is stable; the component that fulfils it is not. Stating it technology-free is what
lets the same capability outlast a change of vendor.

## How it is fulfilled

### Proven
- **`PAT-LAKEHOUSE-DELTA`** — a governed lakehouse with catalogued, column-tagged tables
  fulfils this need. Its attached NFRs (`data-governance`, `security`, `compliance`, `cost`)
  already meet the governance floor below: column-level access control, lineage, and a model-
  access perimeter are properties of the platform, not application code. `confidence: proven`;
  the evidence is the governed-lakehouse EDW migration design already cited on the pattern.

## Governance floor

Any pattern fulfilling this capability must meet — or honestly waive — these bars. They are
measurable on purpose, so a reviewer can check a fulfilment rather than take it on faith.

- **data-governance** — data is catalogued with column-level access control on sensitive
  columns; PII columns carry policies enforced at query time.
  _Acceptance:_ sensitive columns carry catalogue tags and access policies; a query by an
  unauthorised principal is denied at query time.
- **compliance** — processing region matches the data classification.
  _Acceptance:_ processing region == declared classification region.
- **security** — no external or model-serving path may read sensitive columns.
  _Acceptance:_ external serving paths are denied access to columns tagged sensitive.

The `security` floor is what makes this a governed analytics capability and not merely a
fast query engine: the perimeter is drawn around model and external access explicitly, so an
analytics estate cannot quietly become an exfiltration path.

## Aliases

Plain-language terms that resolve to this capability (these feed `capabilities/INDEX.md`):
data warehouse, data analytics platform, analytics store, EDW, reporting database, BI
backend, big-data query, OLAP.

## Promotion

This capability is `provisional` because its one fulfilment carries a real design-evidence
artefact but no production reference build yet. Promotion to `approved` is a human PR that
attaches that build. An agent never advances `approval_status` or flips a fulfilment's
`confidence`. See `CONTRIBUTING.md`.
