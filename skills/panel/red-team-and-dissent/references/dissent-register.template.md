# Dissent-register template

> When a human *declines* a red-team objection (keeps the proposal but wants the
> objection on record, or rejects the proposal outright), the objection does not
> evaporate — it becomes a durable **dissent record**: a titled "what was decided NOT
> to do, and why", with a human-owned reason and immutable provenance back to the
> objection. The register is **revisitable** and feeds **dismissal-memory** so the same
> idea is not silently re-proposed later.
>
> The call **always** stays with the human. The agent surfaces; the human disposes.
> This skill enforces nothing — there is no approval to grant.

## The record shape

```yaml
title:        # one line — what was decided NOT to do
kind:         # feature | requirement | solution | proposal | other
source:       # agent  -> recorded from a red-team objection (provenance below)
              # human  -> a standalone dissent a human added directly
reason:       # the durable WHY — HUMAN-OWNED, editable, the human owns every word
status:       # recorded  (default) | revisited  (re-opened for reconsideration)
provenance:   # only when source=agent
  objection_summary:  # the stance_summary that triggered this
  objection_lens:     # which persona raised it (skeptic, minimalist, …)
  proposal_ref:       # the ref from Step 1 (decision-0, req-0, …)
recorded_on:  # ISO date
```

## The two properties that make the register trustworthy

- **The human owns the WHY; the agent owns the provenance.** The `reason` (and `title`)
  are the human's words, editable forever. The *provenance* — which objection, which
  lens, which proposal — is **immutable** once recorded. Snapshot semantics: editing the
  reason never reaches back and mutates the original objection.
- **Never write-only.** A record can be **revisited** — flip `status: recorded →
  revisited` to re-open a declined item for reconsideration. The record, its WHY, and
  its discussion thread are **preserved** across the flip. Decision history is kept, not
  erased.

## Rendered example

```markdown
## Dissent: Do not co-locate rule evaluation on the read path

- **kind:** solution
- **source:** agent
- **status:** recorded
- **recorded_on:** 2026-06-15

**Why (human-owned):**
The read-path latency cost is accepted for v1 to ship the rules feature without
standing up a queue. Revisit if p95 regresses past the NFR target in staging.

**Provenance (immutable):**
- objection_lens: solution_designer
- proposal_ref: decision-0
- objection_summary: "rule evaluation on the read path spends the read-latency headroom"
```

## Appending to the register

Append the record to the project's **dissent register** — either one markdown file, or a
GitHub Issue using a dissent-record issue template:

- **As Issues:** `source` / `kind` / `status` become labels (`status:recorded`,
  `status:revisited`); the immutable provenance goes in a fenced block in the issue body;
  the human-owned WHY is the editable description; discussion threads naturally as issue
  comments. "Revisit" = re-open the issue (or flip the status label).

## Dismissal-memory (why the register exists)

Before a *new* proposal is surfaced, check it against the register. If it matches a
`recorded` dissent (same idea, same kind), do **not** present it fresh — surface the
prior dissent instead:

> ⤺ This looks like **{dissent.title}**, which was recorded as a dissent on
> {recorded_on} because: *{reason}*. Re-open it (set status → revisited) to reconsider,
> or leave it.

This is the whole point of preserving dissent: the project stops re-litigating settled
"no"s by accident, while keeping the door open to deliberately re-open any of them.

## Notes / anti-patterns

- **No verdict in a dissent.** A dissent records "this was chosen against, and why" — it
  is not a "rejected/blocked" ruling. The red-team that produced the objection never
  delivered a verdict either; the dissent is the human's recorded decision, advisory and
  reversible.
- **The provenance is immutable; the WHY is the human's.** Don't let an edit to the
  reason silently rewrite what was originally objected to. Snapshot the objection,
  lens, and `proposal_ref` at record time and never mutate them.
- **Always offer revisit.** A recorded "no" must be re-openable. Preserving dissent is
  about keeping the decision *and the ability to change it*, not freezing it.
- **Light and advisory.** Recording a dissent enforces nothing. Disposition, ordering,
  and re-opening are all human moves.
