---
name: propagate-pattern-nfrs
description: On adopting a pattern, place each attached NFR against the business outcome it best serves and emit it as a derived NF requirement traced to its parent; if no genuine fit, mark pattern-level; never drop/merge/reword/add NFRs.
one_liner: Trace an adopted pattern's NFRs onto the outcomes they serve.
aliases: [propagate NFRs, inherit quality requirements, attach pattern requirements, carry over non-functional requirements, map NFRs to outcomes, pattern quality bar, derive NFRs from a pattern]
when_to_use: a pattern was just adopted and its governed NFRs must flow into the project requirements
output_kinds: [proposal]
deterministic_fallback: emit each NFR verbatim as a pattern-level derived requirement
suggested_tier: mid
neighbours: After architect/surface-solution-options picks a pattern. Before architect/validate-solution-vs-requirements checks coverage.
---

# propagate-pattern-nfrs

Trace an adopted pattern's attached NFRs onto the business outcomes they serve, faithfully and without alteration.

## Purpose

A vetted component pattern is not just a recipe for *what* to build — it carries a
**governed quality bar**: the non-functional requirements (NFRs) the pattern is required to
always meet. Encryption at rest. p95 latency under 200ms. Exactly-once sync. WCAG 2.2 AA.
Those NFRs are the *evidence* that the pattern is production-grade, and they live in the
pattern's `attached_nfrs` frontmatter.

Adopting the pattern pulls its quality bar in with it. "This must be encrypted" is not
re-derived by hand on every reuse of an encrypted-store pattern — the pattern already
carries it. This skill performs that propagation: on adopting a pattern, each attached NFR
is placed against the **business outcome it most directly serves** and emitted as a
**derived non-functional requirement**, traced back to its parent outcome.

The discipline that makes this trustworthy is **faithfulness**. This is requirements
*tracing*, not requirements *authoring*. The only decision is **where each NFR hangs** —
never *whether* it applies, never its wording, never merging two into one, never inventing
a new one. The pattern's quality bar arrives intact or it does not arrive at all.

## When to use

Use this immediately after a pattern is **adopted** (a recommendation accepted, or chosen
directly) for a project that already has **accepted business outcomes**. The result is a
set of proposed NF requirement lines you fold into the project's `REQUIREMENTS.md`.

Do **not** use this to *evaluate* a pattern, to *recommend* one, or to write fresh NFRs
from scratch — those are different skills. This skill assumes the NFRs already exist and
have already been governed; its only job is to place and trace them.

## Inputs

The user supplies three things as markdown / context:

1. **The adopted pattern** — its `name` and its `attached_nfrs` list. Each NFR is a short
   line, optionally with a `kind` (e.g. `security`, `performance`, `reliability`,
   `accessibility`). Give them a stable **1-based index** in the order listed.
2. **The accepted business outcomes** — each with a **stable `req_key`** (e.g. `BO-1`,
   `BO-2`) and its outcome text. These `req_key`s are the **only valid parents**.
3. *(optional)* The project's `REQUIREMENTS.md` so the folded-in lines slot in cleanly.

If the pattern has no `attached_nfrs`, there is nothing to propagate — say so and stop.
If there are no accepted outcomes yet, every NFR comes back **pattern-level**
(`parent_key: null`); that is correct, not a failure.

## The method (THE method — preserve this exactly)

For each pattern NFR (each carrying its **1-based index**):

1. **Choose the single accepted OUTCOME whose `req_key` the NFR most directly serves**,
   and return that `req_key` as `parent_key`.
2. **If no accepted outcome is a genuine fit, return `parent_key: null`** — meaning the
   NFR applies **at the pattern level**, not fabricated under an outcome. A weak or
   forced association is not a fit; pattern-level is the honest answer.
3. **NEVER invent a `req_key`.** `parent_key` must be **exactly one** of the listed
   outcome `req_key`s, or `null`. Nothing else.
4. **Do NOT drop, merge, reword, or add NFRs.** Return **exactly one entry per NFR**,
   **preserving its index**. The count out equals the count in; the text out equals the
   text in.

That is the entire decision: *which parent, or pattern-level* — placement only. Everything
about the NFR's content is load-bearing and untouchable.

### Steps to run it

1. **List the NFRs with their indices.** Number them 1..N in the order the pattern lists
   them. This index is the contract — it must survive to the output unchanged.
2. **List the outcomes with their `req_key`s.** These are your only legal parents, plus
   `null`.
3. **For each NFR, run the placement decision above.** Ask: *which one outcome does this
   quality bar most directly serve?* Match on the substance (a performance NFR serves the
   outcome about responsiveness; a security NFR serves the outcome about handling
   sensitive data). When two outcomes both plausibly fit, pick the **single most direct**
   one. When none genuinely fits, choose `null` — do not stretch.
4. **Record a one-line rationale per NFR** — why this outcome, or (when `null`) why it is
   genuinely pattern-level rather than tied to any one outcome.
5. **Emit the proposed requirement lines** (format below) and hand them to the human to
   fold into `REQUIREMENTS.md`.

### Deterministic step (run this when no LLM is available)

The placement decision is the only judgement call; everything else is mechanical. With no
model, fall back to a deterministic placement that **never fabricates a parent**:

- **Token-overlap tracer.** Lower-case each NFR and each outcome, drop stopwords, and
  count shared content tokens. Assign the NFR to the outcome with the **highest non-zero
  overlap**; ties break to the **earliest `req_key`**. If **no** outcome shares any
  content token, the NFR is **pattern-level** (`parent_key: null`).
- **Emit each NFR as a pattern-level derived requirement when nothing matches** — verbatim
  text, its index preserved, `parent_key: null`, rationale `"Governed by adopted pattern
  '<name>' (no outcome token-overlap; pattern-level)."`.

This is deliberately conservative: a weak match becomes pattern-level rather than a guess.
It guarantees the count-preserving, never-invent, never-reword invariants hold even with
zero reasoning.

### LLM step (the propagate prompt)

When a model is available, use it for the placement judgement only. Give it the pattern
name, the outcomes (with `req_key`s), and the indexed NFRs, and ask for placement:

```
A reusable architecture/governance PATTERN has been adopted. That pattern carries
non-functional requirements (NFRs) that must now be applied to the current project and,
where possible, traced to the specific business outcome each one best serves.

ADOPTED PATTERN: <pattern_name>

ACCEPTED BUSINESS OUTCOMES (each has a stable req_key — these are the ONLY valid parents):
<outcomes_block — one line per outcome: "BO-1: <outcome text>">

PATTERN NFRs TO PLACE (each has a 1-based index):
<nfrs_block — one line per NFR: "1. [<kind>] <nfr text>">

For each pattern NFR, choose the single accepted outcome whose req_key it most directly
serves, and return that outcome's exact req_key as parent_key. If no accepted outcome is
a genuine fit, return parent_key null — meaning the NFR applies at the pattern level
rather than to one outcome. NEVER invent a req_key: parent_key must be exactly one of the
listed outcome req_keys, or null. Do not drop, merge, reword, or add NFRs; return exactly
one entry per listed NFR index, preserving its index.

Return ONLY a JSON object of exactly this shape, no prose, no markdown fence:
{
  "nfrs": [
    {"index": 1, "parent_key": "BO-2", "agent_rationale": "why this outcome (or why pattern-level when parent_key is null)"}
  ]
}
```

**Validate the model's output before trusting it** — the invariants are not the model's to
break:

- Every returned `index` is one of the input indices, and **all** input indices are
  present (count preserved).
- Every `parent_key` is **exactly** a listed outcome `req_key` or **`null`** — anything
  else is a fabrication; reject and treat that NFR as pattern-level.
- No NFR text came back changed — you only consumed `index`, `parent_key`,
  `agent_rationale`; the **text stays the verbatim input NFR text**.

## Output format

Emit **proposed markdown requirement lines** — one per NFR, in index order. Each is a
derived **non-functional** requirement (`req_type: NF`), traced to its parent via a
`derives_from: <req_key>` citation (or marked pattern-level when `parent_key` is null).
The human folds these into the project's `REQUIREMENTS.md`; nothing is written for them.

Give each line a stable key of the form `NFR-<pattern-slug>-<index>` so re-running is
idempotent and the provenance (which pattern, which NFR index) is legible at a glance.

### Template

```markdown
### Propagated NFRs — from pattern: <pattern-name>
<!-- Source: attached_nfrs on the adopted pattern. Tracer placement only — texts verbatim. -->

- **NFR-<pattern-slug>-1** [NF] (<kind>) <verbatim NFR text>
  - derives_from: BO-2
  - rationale: <why this outcome>
- **NFR-<pattern-slug>-2** [NF] (<kind>) <verbatim NFR text>
  - derives_from: (pattern-level — no single outcome is a genuine fit)
  - rationale: <why pattern-level>
```

### Concrete example

Adopted pattern **`encrypted-offline-store`** with `attached_nfrs`:

```yaml
attached_nfrs:
  - { kind: security,     text: "Data at rest is encrypted with AES-256; keys are never written to disk in plaintext." }
  - { kind: reliability,  text: "Queued offline writes sync exactly once with no duplicates when connectivity returns." }
  - { kind: performance,  text: "The local store answers reads in under 50ms at p95 with 10k records." }
```

Accepted outcomes:

```
BO-1: Field technicians can complete inspections with zero connectivity.
BO-2: Customer records are protected to the company's data-handling standard.
```

Proposed output:

```markdown
### Propagated NFRs — from pattern: encrypted-offline-store
<!-- Source: attached_nfrs on the adopted pattern. Tracer placement only — texts verbatim. -->

- **NFR-encrypted-offline-store-1** [NF] (security) Data at rest is encrypted with AES-256; keys are never written to disk in plaintext.
  - derives_from: BO-2
  - rationale: Directly serves the outcome of protecting customer records to the data-handling standard.
- **NFR-encrypted-offline-store-2** [NF] (reliability) Queued offline writes sync exactly once with no duplicates when connectivity returns.
  - derives_from: BO-1
  - rationale: The zero-connectivity inspection outcome depends on reliable sync-on-reconnect.
- **NFR-encrypted-offline-store-3** [NF] (performance) The local store answers reads in under 50ms at p95 with 10k records.
  - derives_from: (pattern-level — no single outcome is a genuine fit)
  - rationale: A store-internal latency bar that underpins both outcomes rather than serving one; placing it under either would overstate the link.
```

Three NFRs in, three out — same order, same text, each with a parent or an honest
pattern-level mark.

## Notes / anti-patterns

- **This is a doc-emit, not a state write.** The output is a **proposal** — markdown lines
  a human reviews and folds into `REQUIREMENTS.md`. Nothing is auto-applied; nothing is
  written into project state. Light and advisory.
- **No orphan-by-fabrication.** When no outcome matches, do **not** fall back to attaching
  the NFR to the *first* accepted outcome. A forced parent is a lie about traceability. The
  honest fallback is **pattern-level** (`parent_key: null`) — surface it as such; never
  invent a link to make the trace look complete.
- **Placement is the only freedom.** You choose the parent (or `null`). You do **not**
  touch whether the NFR applies, its wording, its count, or its index. If you feel the
  urge to "improve" an NFR's wording or split one into two, stop — that is a separate,
  human-owned change to the pattern itself, not a propagation.
- **Count is a contract.** N NFRs in, N requirement lines out. If your output has a
  different count, you dropped, merged, or invented one — all forbidden.
- **Index is provenance.** Preserve each NFR's 1-based index into its `req_key`
  (`NFR-<slug>-<index>`). It lets a reviewer walk straight back from the project
  requirement to the exact pattern NFR it came from, and makes re-runs idempotent.
- **Pattern-level NFRs are first-class, not leftovers.** An NFR with `parent_key: null`
  still enters the requirements — it just hangs off the pattern's adoption rather than one
  outcome. Surface it plainly so the human can decide if it later wants a parent; do not
  bury or discard it.
- **Re-running is safe.** Stable keys mean a second pass over the same pattern produces the
  same lines; the human replaces rather than accumulates. Adopting a *second* pattern adds
  its own slug-namespaced block alongside the first.
