---
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
---

# Databricks Lakehouse + Delta Lake (`PAT-LAKEHOUSE-DELTA`)

> **`approval_status: provisional`** — reviewed and usable with care; its evidence is a real
> governed-lakehouse migration design pending a production reference build. This
> is a strong **data/AI-governance-aware exemplar**: governance, lineage, and access control are
> native to the platform rather than bolted on, and every attached NFR is phrased as a checkable
> acceptance criterion. Use it as the reference for how a regulated data/AI pattern should attach
> governance up front.

## Summary

Batch and streaming analytics on Delta Lake tables managed via Unity Catalog. Governance, lineage, and RBAC are Unity Catalog-native. Suitable for analytics, ML feature engineering, and regulated data products.

The deployment topology is a Databricks workspace (Unity Catalog) in a governed region, with Delta tables in cloud object storage. Data placement is the point of the pattern: Unity Catalog governs the data, PII is tagged at the column level, and no data leaves the Unity Catalog boundary.

## When to use

- **Analytics** — batch and streaming workloads over Delta tables where you want governed, lineage-tracked SQL and BI access rather than ungoverned extracts.
- **ML feature engineering** — building and serving feature tables where the same column-level governance must follow the data into training and inference.
- **Regulated data products** — any data product where residency, PII handling, and access control are auditable requirements, and where keeping data inside a single governed perimeter is a compliance asset rather than just an architectural preference.

Reach for this pattern when the *governance posture* is part of the requirement, not an afterthought — when "who can read which column, in which region, and can a model see it" must be answerable and enforceable.

## Attached NFRs

These four NFRs travel **with** the pattern, mapped to the closed enum (`data-governance`, `security`, `compliance`, `cost`). The fact that the pattern arrives pre-loaded with concrete, measurable governance NFRs is what makes it a good data/AI-governance exemplar.

| Kind | Statement | Acceptance criterion |
| --- | --- | --- |
| `data-governance` | Unity Catalog column-level PII tagging; row-level filter policies | PII columns carry UC tags and row-level policies are enforced |
| `security` | No external model call may read PII columns; governed perimeter enforced | External serving paths are denied access to PII-tagged columns |
| `compliance` | Workspace region must match data classification | Workspace region == declared data-classification region |
| `cost` | Cluster auto-termination; spot/preemptible workers for batch | Idle clusters auto-terminate; batch jobs use spot workers |

The `security` NFR ("no external model call may read PII columns") is the one that makes this an **AI-governance** pattern and not merely a data-governance one: it draws the perimeter around model access explicitly, so an LLM/ML serving path cannot exfiltrate tagged columns out of the governed boundary.

## When NOT to use

- Small, non-regulated, or single-tenant analytics where the operational weight of a governed Lakehouse exceeds the value of its governance.
- Workloads that genuinely need data to leave the Unity Catalog boundary — that conflicts with the data-placement premise and the `security` perimeter NFR.
- Pure low-latency transactional (OLTP) serving — this is an analytics/feature-engineering lakehouse, not an operational database.

## Trade-offs

- **Governance is Unity-Catalog-native.** This is the headline upside: tagging, lineage, and RBAC are properties of the platform, so the governance NFRs above are enforced *in place* rather than reconstructed in application code. The flip side is platform lock-in to Unity Catalog as the governance plane — the pattern assumes UC is your system of record for who-can-see-what.
- **Cost discipline is required.** Cluster compute is the dominant cost and it is easy to leave running. The `cost` NFR is not decorative: auto-termination on idle clusters and spot/preemptible workers for batch jobs are the difference between an economical lakehouse and a runaway bill. Treat the cost NFR as a build-time check, not an aspiration.
- **Residency couples region to classification.** The `compliance` NFR ties the workspace region to the declared data classification. That keeps you compliant but reduces deployment flexibility — multi-region or cross-region designs need a workspace (and governance scope) per region.
- **Perimeter is only as strong as the tags.** The `security` and `data-governance` NFRs both depend on PII actually being tagged at the column level. Untagged PII silently escapes the row-level/column-level policies, so column tagging has to be part of ingestion, not a later sweep.

## Example / artefacts

- [Governed-lakehouse EDW migration — solution design with UC governance NFRs](https://github.com/sdlc-agentic-coe/seed-corpus/blob/main/edw-migration/solution-design.md)
  — the recorded adoption-decision artefact (the `evidence` entry in the frontmatter). A
  CODEOWNER attaches a production reference build to promote this from `provisional` to `approved`.
- A representative real-world shape this pattern fits: migration of a ~10TB on-prem EDW to a Databricks Lakehouse on Unity Catalog with BI (e.g. Power BI) on top — a governed analytics estate rather than a lift-and-shift of ungoverned extracts.

## References

- Based on a governed-lakehouse migration design; provenance is the adoption-decision artefact in `evidence`.
- Unity Catalog: column/row-level access policies, tagging, and lineage.
- Delta Lake: ACID tables on cloud object storage for batch + streaming.

---

*Light/advisory. This pattern recommends and attaches NFRs; it does not gate. A downstream project adopts it by reference and is responsible for checking the four acceptance criteria during its own build. The lifecycle Action computes a next-review date from `valid_from + validity_check_months` (12 months) and opens an advisory revalidation issue when it arrives; it never blocks.*
