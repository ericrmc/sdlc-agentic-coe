---
capability_key: CAP-AGENT-RUNTIME
name: Agent Runtime
capability_domain: runtime
summary: >
  The need to host and execute LLM agents with tool-calling in production, inside a governed
  boundary, so agent workloads run with managed identity, egress control, and session
  persistence. No proven fulfilment yet — three candidate platforms each owe a proving spike.
need_statement: "A system needs to host and execute LLM agents with tool-calling in production, inside a governed boundary, so that agent workloads run with managed identity, egress control, and session persistence."
aliases:
  - agent hosting
  - agent execution platform
  - LLM agent runtime
  - tool-calling runtime
  - agent orchestration host
  - run our agents in prod
fulfilled_by:
  - confidence: candidate
    note: "AWS AgentCore (vendor: AWS). A managed agent execution platform; no pattern_key yet — unproven for this need until a spike answers the open questions."
    open_questions:
      - "What are the tool-call concurrency limits, and do they fit fan-out workloads?"
      - "What VPC / egress controls keep in-boundary data in-boundary during tool calls?"
      - "What are the cold-start characteristics and the session-persistence model?"
  - confidence: candidate
    note: "Databricks Agent Bricks (vendor: Databricks). Agent hosting tied to the lakehouse governance plane; no pattern_key yet — unproven for this need until a spike answers the open questions."
    open_questions:
      - "How far does the data-catalogue governance reach into agent tool calls?"
      - "Is multi-agent fan-out supported, and at what concurrency?"
  - confidence: candidate
    note: "Microsoft Foundry (vendor: Microsoft). Agent hosting with identity-platform integration; no pattern_key yet — unproven for this need until a spike answers the open questions."
    open_questions:
      - "How deep is the managed-identity integration for tool-call authorisation?"
      - "Does the built-in model router create lock-in to a provider's models?"
governance_nfrs:
  - kind: security
    statement: "Agent egress and tool-call scope are governed; no unbounded external calls."
    acceptance_criterion: "Every outbound call and tool invocation is scoped to an allow-list; an unlisted egress attempt is denied and logged."
  - kind: operations
    statement: "Session persistence and cold-start behaviour are observable."
    acceptance_criterion: "Session state survives a restart and cold-start latency is exported as a metric."
  - kind: compliance
    statement: "Execution stays inside the boundary that matches the data classification."
    acceptance_criterion: "Agent runtime region == declared data-classification region; no execution leaves the boundary."
valid_from: "2026-06-15"
validity_check_months: 12
approval_status: candidate
---

# Agent Runtime (`CAP-AGENT-RUNTIME`)

> `approval_status: candidate` — there is **no proven fulfilment yet**. Three candidate
> platforms are recorded, each owing a proving spike. This is honest about the gap: do not
> read a candidate as a recommendation. A human promotes a candidate only after a spike.

## The need

A system needs to host and execute LLM agents with tool-calling in production, inside a
governed boundary, so that agent workloads run with managed identity, egress control, and
session persistence. This is the need behind "agent hosting", "an agent execution platform",
"a tool-calling runtime", or "run our agents in prod" — somewhere agents can run in
production without losing the identity, egress, and persistence guarantees a governed
workload requires.

Unlike `CAP-OLAP` and `CAP-OLTP`, this need has **no proven fulfilment**. The candidates
below are plausible but unproven; each one owes a spike before it can be recommended.

## How it is fulfilled

### Proven
- None yet. This is the honest state of the capability — the library does not pretend a
  candidate is a proven shape.

### Candidates (spikes owed)
Each is `confidence: candidate`, no `pattern_key`, unproven until a spike answers its open
questions. A spike's result is measured against the governance floor below.

- **AWS AgentCore** (vendor: AWS). Open questions:
  - What are the tool-call concurrency limits, and do they fit fan-out workloads?
  - What VPC / egress controls keep in-boundary data in-boundary during tool calls?
  - What are the cold-start characteristics and the session-persistence model?
- **Databricks Agent Bricks** (vendor: Databricks). Open questions:
  - How far does the data-catalogue governance reach into agent tool calls?
  - Is multi-agent fan-out supported, and at what concurrency?
- **Microsoft Foundry** (vendor: Microsoft). Open questions:
  - How deep is the managed-identity integration for tool-call authorisation?
  - Does the built-in model router create lock-in to a provider's models?

> **Multi-agent option (advisory).** This step deepens with independent parallel agents: launch one sub-agent per candidate, at most 4 at a time, each a separate sub-agent. A failed sub-agent returns nothing and is never fatal — the deterministic base stands; merge what succeeded. (Claude Code: use the Task tool / subagents. Other tools: launch parallel model calls; or a matrix-strategy CI job.) Never required — it adds coverage and cuts single-pass bias. See `skills/_contract/parallel-agents`.

Probing the three candidates in parallel — one agent per candidate, each answering that
candidate's open questions against the governance floor — produces a per-candidate
proven-or-still-candidate read for a human to ratify. Preserve dissent on lock-in: a
platform that fulfils the need but couples you to one vendor's models or governance plane is
a recorded trade-off, not a silent disqualifier.

## Governance floor

Any pattern fulfilling this capability must meet — or honestly waive — these bars. A spike
that cannot demonstrate them has not promoted the candidate.

- **security** — agent egress and tool-call scope are governed; no unbounded external calls.
  _Acceptance:_ every outbound call and tool invocation is scoped to an allow-list; an
  unlisted egress attempt is denied and logged.
- **operations** — session persistence and cold-start behaviour are observable.
  _Acceptance:_ session state survives a restart and cold-start latency is exported as a
  metric.
- **compliance** — execution stays inside the boundary that matches the data classification.
  _Acceptance:_ agent runtime region == declared data-classification region; no execution
  leaves the boundary.

## Aliases

Plain-language terms that resolve to this capability (these feed `capabilities/INDEX.md`):
agent hosting, agent execution platform, LLM agent runtime, tool-calling runtime, agent
orchestration host, run our agents in prod.

## Promotion

A candidate is promoted to proven only by a human PR that attaches spike evidence and a
fulfilling pattern meeting the governance floor above, then flips that fulfilment's
`confidence: proven` and advances `approval_status`. An agent never sets `confidence: proven`
or advances `approval_status`. Until then, this capability honestly reads `candidate`: a
named need with options, not an answer. See `CONTRIBUTING.md`.
