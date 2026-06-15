# Capability Index — start here if you know the NEED but not the technology

This is the alias-searchable lookup: the **first** place to come when you can name a need in
plain language ("a data warehouse", "somewhere to run our agents") but not the component that
fulfils it. Find your phrase in the left column; it resolves to a canonical capability and
its current fulfilment state on the right.

**How to read the fulfilment state:**

- **proven `PAT-…`** — a built, evidenced pattern fulfils this need today. Reach for it.
- **OPEN — N candidate(s), spikes owed** — no proven fulfilment yet; the candidates are
  plausible but unproven. Read the capability file for the spike questions before you commit.

A capability is the named middle term between a need and a component. The chain runs:
business outcome ← requirement (`fulfils_capability: CAP-…`) ← capability (`fulfilled_by` a
pattern) ← component pattern. This index is the entry to that chain from the need side.

---

## Alias → capability → fulfilment

| You might call it… | Capability | Name | Fulfilment state |
| --- | --- | --- | --- |
| data warehouse | [`CAP-OLAP`](data/olap.md) | Online Analytical Processing (OLAP) | **proven** — `PAT-LAKEHOUSE-DELTA` |
| data analytics platform | [`CAP-OLAP`](data/olap.md) | Online Analytical Processing (OLAP) | **proven** — `PAT-LAKEHOUSE-DELTA` |
| analytics store | [`CAP-OLAP`](data/olap.md) | Online Analytical Processing (OLAP) | **proven** — `PAT-LAKEHOUSE-DELTA` |
| EDW | [`CAP-OLAP`](data/olap.md) | Online Analytical Processing (OLAP) | **proven** — `PAT-LAKEHOUSE-DELTA` |
| reporting database | [`CAP-OLAP`](data/olap.md) | Online Analytical Processing (OLAP) | **proven** — `PAT-LAKEHOUSE-DELTA` |
| BI backend | [`CAP-OLAP`](data/olap.md) | Online Analytical Processing (OLAP) | **proven** — `PAT-LAKEHOUSE-DELTA` |
| big-data query | [`CAP-OLAP`](data/olap.md) | Online Analytical Processing (OLAP) | **proven** — `PAT-LAKEHOUSE-DELTA` |
| OLAP | [`CAP-OLAP`](data/olap.md) | Online Analytical Processing (OLAP) | **proven** — `PAT-LAKEHOUSE-DELTA` |
| transactional database | [`CAP-OLTP`](data/oltp.md) | Online Transaction Processing (OLTP) | **proven** — `PAT-WEBAPP-PG` |
| application database | [`CAP-OLTP`](data/oltp.md) | Online Transaction Processing (OLTP) | **proven** — `PAT-WEBAPP-PG` |
| operational store | [`CAP-OLTP`](data/oltp.md) | Online Transaction Processing (OLTP) | **proven** — `PAT-WEBAPP-PG` |
| system of record | [`CAP-OLTP`](data/oltp.md) | Online Transaction Processing (OLTP) | **proven** — `PAT-WEBAPP-PG` |
| managed Postgres | [`CAP-OLTP`](data/oltp.md) | Online Transaction Processing (OLTP) | **proven** — `PAT-WEBAPP-PG` |
| Lakebase / managed Postgres | [`CAP-OLTP`](data/oltp.md) | Online Transaction Processing (OLTP) | **proven** — `PAT-WEBAPP-PG` (Lakebase: candidate, spike owed) |
| CRUD backend | [`CAP-OLTP`](data/oltp.md) | Online Transaction Processing (OLTP) | **proven** — `PAT-WEBAPP-PG` |
| OLTP | [`CAP-OLTP`](data/oltp.md) | Online Transaction Processing (OLTP) | **proven** — `PAT-WEBAPP-PG` |
| agent hosting | [`CAP-AGENT-RUNTIME`](runtime/agent-runtime.md) | Agent Runtime | **OPEN** — 3 candidates, spikes owed |
| agent execution platform | [`CAP-AGENT-RUNTIME`](runtime/agent-runtime.md) | Agent Runtime | **OPEN** — 3 candidates, spikes owed |
| LLM agent runtime | [`CAP-AGENT-RUNTIME`](runtime/agent-runtime.md) | Agent Runtime | **OPEN** — 3 candidates, spikes owed |
| tool-calling runtime | [`CAP-AGENT-RUNTIME`](runtime/agent-runtime.md) | Agent Runtime | **OPEN** — 3 candidates, spikes owed |
| agent orchestration host | [`CAP-AGENT-RUNTIME`](runtime/agent-runtime.md) | Agent Runtime | **OPEN** — 3 candidates, spikes owed |
| run our agents in prod | [`CAP-AGENT-RUNTIME`](runtime/agent-runtime.md) | Agent Runtime | **OPEN** — 3 candidates, spikes owed |

---

## If your need is not here

The library does not yet name your need as a capability. Two honest moves:

1. Check [`skills/architect/recommend-component-patterns`](../skills/architect/recommend-component-patterns/SKILL.md)
   — it resolves a need to a capability first, then to a pattern, and tells you when nothing fits.
2. Propose a new capability with [`skills/library/author-capability`](../skills/library/author-capability/SKILL.md).
   It enters as a `candidate` via PR; a human architect promotes it.

Every alias in the table above is sourced from a capability file's `aliases` field. Keep them
in sync: an entry here must point at a real `capability_key`, and a capability's aliases must
all appear here.
