---
# ============================================================================
# PATTERN FRONTMATTER — copy this whole block into your new pattern file.
# Every field below carries an inline comment: REQUIRED | CONDITIONAL |
# OPTIONAL | COMPUTED. Fill the REQUIRED ones; leave COMPUTED ones out
# entirely (they are written into generated/ by an Action, never by hand).
# This library is LIGHT and ADVISORY — nothing here gates a downstream
# project. approval_status is a human signal of trust, not an enforcement lock.
# ============================================================================

pattern_key: PAT-EXAMPLE-KEY   # REQUIRED. Stable, UPPER-KEBAB, cite-able, survives renames.
                               #   Prefix by category is conventional: PAT-WEBAPP-PG, PAT-EVENT-BROKER.
                               #   This is what a project cites and what an Action concatenates by.
name: ""                       # REQUIRED. Human title, e.g. "Containerised web + managed Postgres".
category: deployment           # REQUIRED. Closed enum: deployment | integration | data.
intent: "use WHEN ... so that ..."  # REQUIRED. One sentence in the WHEN/so-that shape.
                               #   This is the retrieval anchor — the line an agent reads to decide
                               #   if the pattern fits. Make the WHEN a real condition, not a category.
deployment_topology: ""        # CONDITIONAL. Required for category: deployment | integration.
                               #   The concrete shape: "Single-region container service + managed Postgres".
data_placement: ""             # CONDITIONAL. Required for category: data (and good practice for any
                               #   pattern that stores state). Where data lives + residency posture.
summary: ""                    # REQUIRED. One paragraph. Mirror the body ## Summary — this is the
                               #   embed/preview text retrieval shows before opening the file.

# ---- Approval lifecycle (HUMAN-ONLY field) --------------------------------
approval_status: candidate     # REQUIRED. Closed enum, ordered:
                               #   candidate    — drafted; an author/agent leaves it HERE.
                               #   provisional  — a human reviewed it; used with care, evidence attached.
                               #   approved     — a human blessed it; the trusted fast-path.
                               #   deprecated   — do not adopt; see superseded_by.
                               #   *** AN AGENT NEVER ADVANCES THIS BEYOND 'candidate'. ***
                               #   Promotion is a human act in a PR review (see CONTRIBUTING.md).
approved_by:                   # CONDITIONAL. Required once approval_status >= provisional.
                               #   The reviewer's name/handle. The owned human fact. Agent never sets it.
approved_at:                   # CONDITIONAL. Required once approval_status >= provisional. ISO date.
evidence: []                   # CONDITIONAL. Required once approval_status >= provisional.
                               #   [{title, url}] — links PROVING this was actually built, not theorised.
                               #   e.g. {title: "prod runbook", url: "https://..."}, {title: "load-test report", url: "https://..."}.
                               #   url must be a real URI; optional: kind, project, date.

# ---- Validity / sunset (dates make staleness visible, advisory only) ------
valid_from: "2026-06-15"       # REQUIRED. ISO date (quote it so it stays a string, matching the schema).
validity_check_months: 12      # REQUIRED. Re-review cadence in months. An Action computes the next
                               #   review date (valid_from + N months) into generated/; it warns, never blocks.
sunset_at:                     # OPTIONAL. ISO date after which this should not be adopted for new work.
supersedes:                    # OPTIONAL. pattern_key this replaces (the older pattern points forward via superseded_by).
superseded_by:                 # CONDITIONAL. Required when approval_status == deprecated. The pattern_key to use instead.

# ---- What the pattern carries downstream ----------------------------------
constraints: []                # OPTIONAL but recommended. [{statement, enforced: hard|soft}]
                               #   What adopting this pattern makes you GIVE UP. 'hard' = inherent, cannot be
                               #   waived without leaving the pattern; 'soft' = waiver is a recorded trade-off.
                               #   Be honest here — this is what an adopting team replays against their needs.
attached_nfrs: []              # OPTIONAL but recommended. [{kind, statement, acceptance_criterion}]
                               #   kind is a CLOSED enum (use exactly one of):
                               #     security | availability | performance | data-residency | observability |
                               #     resilience | cost | compliance | scalability | data-governance | operations
                               #   acceptance_criterion is the testable "done" — the field that lets an
                               #   adopting project turn this NFR into a real, checkable requirement.

# ---- COMPUTED — DO NOT hand-write. Lives in generated/, written by Actions:
#   maturity         — experimental | emerging | battle-tested (derived from adoption_count)
#   adoption_count   — COUNT of recorded adoptions across downstream projects
#   next_review_at   — valid_from + validity_check_months
# These are derived facts, never opinions typed into the source file.
# ============================================================================
---

# <name> (`PAT-EXAMPLE-KEY`)

> Status badge is driven by `approval_status` above. While it reads `candidate`,
> this pattern is a draft proposal — usable as a reference, not yet a trusted fast-path.

## Summary

One paragraph, plain prose. What the pattern IS, the shape of the solution, and the
single condition under which it is the right reach-for. Keep it to what you would say
out loud to a colleague deciding whether to open the rest of this file. Mirror the
`summary:` frontmatter line so retrieval previews and the body agree.

_Example:_ Stateless web tier behind a load balancer with a managed relational store.
Scale-out is horizontal (container replicas); the DB is the single state authority.
Suitable for line-of-business apps with moderate throughput and strict data-residency.

## When to use / when not

**Use this when**
- <the real precondition that makes this the right call — e.g. "moderate throughput, strict in-region data-residency, a single team owning state">
- <a second concrete fit signal>

**Do NOT use this when** _(the trustworthy "avoid-when" cues — be specific, this is where the file earns its keep)_
- <a condition under which this pattern actively hurts — e.g. "high-throughput event fan-out across many teams → reach for an event-driven pattern instead">
- <a hard constraint clash — e.g. "no-cloud / data-sovereignty mandate → see an on-prem pattern">

## Attached NFRs

> One bullet per `attached_nfrs` entry, restating its **kind**, **statement**, and
> **acceptance_criterion**. These are what flow into an adopting project as checkable
> requirements — keep them measurable. Delete this note and fill in real rows.

- **security** — TLS 1.2+ in transit between tiers and to the managed store.
  _Acceptance:_ all inter-tier connections present a cert chain at TLS ≥ 1.2; verified by scan.
- **availability** — 99.9% monthly SLA achievable with multi-AZ placement.
  _Acceptance:_ rolling 30-day measured availability ≥ 99.9%; failover exercised in game-day.
- **data-residency** — data at rest stays in the declared region.
  _Acceptance:_ managed store region setting matches the project's residency tag; evidenced in config.
- **scalability** — horizontal scaling with a DB connection pool.
  _Acceptance:_ a connection pool (e.g. PgBouncer) sits in front of the store; pool sizing documented.

## Trade-offs

Name the **load-bearing NFR** — the one thing this pattern is really betting on — and be
honest about what it costs. Do not oversell. State each `constraints` entry plainly:
what you give up, and whether it is `hard` (inherent) or `soft` (waivable as a recorded
trade-off). A reader should leave this section knowing the sharpest edge before they adopt.

- **Load-bearing bet:** <the single NFR/property everything else depends on — e.g. "the DB is the one state authority; this pattern lives or dies on that store's availability">
- **Constraint (hard):** <statement> — cannot be waived without leaving the pattern.
- **Constraint (soft):** <statement> — waivable, but the waiver is a trade-off you should record.
- **Honest downside:** <the failure mode or cost a fan-favourite write-up would gloss over>

## Evidence of having been built

> Links proving this is a real, built thing — not a whiteboard idea. Required content
> once a human moves `approval_status` to `provisional`/`approved`; keep mirroring
> `evidence:` in the frontmatter. While `candidate`, list whatever exists so far.

- [prod runbook / architecture doc](https://...)
- [load-test or SLO report](https://...)
- [reference repo or IaC module](https://...)
- [the engagement it was first shipped on](https://...)

## References

- <links to source patterns, vendor docs, or the internal design note this builds on>

---

_Review, validation, promotion, and sunset for this pattern follow the process in
[`CONTRIBUTING.md`](../CONTRIBUTING.md) — a human advances `approval_status` in a PR
review; agents and authors leave it `candidate`._
