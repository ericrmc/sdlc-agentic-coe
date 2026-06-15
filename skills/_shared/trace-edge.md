# _shared/trace-edge.md — `derives_from` as a portable `req_key` citation

> **This file is the single source of truth for the TRACE EDGE.**
> Skills do not import it; they **quote the block below verbatim** into their own body.
> The `check-shared-stub-drift` GitHub Action (advisory, on every PR touching
> `skills/**`) diffs each skill's quoted copy against this file and fails the check
> if a single byte drifts. **Keep the canonical block byte-stable.** If the edge
> wording must change, change it *here first*, then re-quote into every skill in the
> same PR — never edit a quoted copy in place.

In a file-based library there are no rows and no database, so the edge is **a citation,
not a foreign key** — a stable `req_key` written into a sibling artefact, optionally as a
markdown link. It is the keystone thread that makes deriving-low-from-accepted-high
*safe*: every derived thing visibly points at the accepted thing above it.

---

## The canonical block (quote this verbatim)

<!-- BEGIN trace-edge (byte-stable; do not edit a quoted copy — edit _shared/trace-edge.md) -->

**TRACE EDGE — `derives_from` is a portable `req_key` citation, not a foreign key.**

Every derived artefact carries a `derives_from:` line naming the **stable `req_key`** of
the upstream node it serves. The edge is plain text — a key, optionally a markdown link
to the file/anchor that defines that key. It needs no database, no id, no schema:

```
derives_from: O-1
```

or, when the upstream node lives in another file:

```
derives_from: [O-1](../outcomes/OUTCOMES.md#o-1)
```

`req_key`s are short, human-readable, and **stable for the life of the project** — they
are the citation target, so renaming or renumbering one silently breaks every edge that
cites it. Conventional prefixes (advisory, not enforced):

- `C-*` business **C**apability
- `O-*` business **O**utcome
- `R-*` derived **R**equirement (technical / solution / NFR)
- `P-*` adopted **P**attern
- `D-*` **D**ecision / contested call / dissent

The edges compose into one directed **outcome-impact graph**:

```
capability  ->  outcome  ->  requirement  ->  pattern  ->  decision
   C-*            O-*           R-*            P-*          D-*
```

The graph is walkable in **both** directions, and both walks matter:

- **Downward = decomposition.** From a capability or outcome, follow `derives_from`
  *backwards* (find every artefact that cites this key) to see everything synthesised
  beneath it — the technical reqs, the NFRs, the pattern, the calls. This is how
  "accept HIGH, derive LOW" stays legible: the low artefacts are auto-applied, but each
  one names the high thing it serves.
- **Upward = impact.** From any node, follow its own `derives_from:` *forwards* to the
  outcome and capability it ultimately serves. This is how a failing or compromised node
  answers "what business outcome takes the hit, and which capability?" — the necessity
  check and the compromise/impact view both ride this walk.

**A rejected upstream node orphans its entire subtree.** If a human rejects outcome `O-1`,
every artefact whose `derives_from:` chain leads to `O-1` is now an **orphan** — it points
at nothing accepted. Orphans are not deleted and not errors; they are **surfaced, not
swept** (an orphan leads the open-questions handoff). This visible orphaning is what makes
auto-derivation safe: nothing technical can quietly survive the rejection of the business
reason it existed for.

**The edge is a citation, never a verdict.** `derives_from` records *what serves what*. It
never asserts that a requirement is necessary, sufficient, good, or done — those are human
calls. A node with a valid edge can still be cut; a node can be kept with its edge orphaned
and flagged. The edge informs the judgment; it never is the judgment.

<!-- END trace-edge -->

---

## How to quote it

In any `SKILL.md` (or artefact template) that walks, draws, or relies on the edge, paste
the block between the `BEGIN`/`END` markers above — markers included — into a section
titled **"Trace edge (quoted)"**. Do not reword, reorder, re-case, or re-punctuate it; the
drift check compares bytes between the markers.

```markdown
## Trace edge (quoted)

<!-- BEGIN trace-edge (byte-stable; do not edit a quoted copy — edit _shared/trace-edge.md) -->
...paste the canonical block exactly...
<!-- END trace-edge -->
```

## Worked example — one edge, both walks

An intake produces an outcome and the platform derives the technical view beneath it. Each
file carries its own `req_key` and, if derived, a `derives_from:` citation:

```markdown
<!-- outcomes/OUTCOMES.md -->
## O-1 — Search returns relevant results in under two seconds
req_key: O-1
derives_from: [C-2](../capabilities/CAPABILITIES.md#c-2)   <!-- serves the "Self-serve discovery" capability -->
```

```markdown
<!-- requirements/REQUIREMENTS.md -->
## R-7 — Full-text index with sub-200ms p95 query latency
req_key: R-7
derives_from: [O-1](../outcomes/OUTCOMES.md#o-1)
```

```markdown
<!-- patterns adopted; NFRs flow in as derived requirements -->
## R-12 — Cache layer (from adopted pattern)
req_key: R-12
derives_from: [P-3](../patterns/managed-search.md)         <!-- P-3 itself derives_from O-1 -->
```

- **Downward from `O-1`:** grep the repo for `derives_from:.*O-1` → `R-7`, `P-3`, and
  (transitively) `R-12`. That is the decomposition of the outcome.
- **Upward from `R-12`:** read its `derives_from:` → `P-3` → read *its* `derives_from:` →
  `O-1` → `C-2`. If `R-12`'s cache breaks, the impact walk lands on outcome `O-1` and
  capability `C-2`. That is the impact answer, computed from citations, not asserted.
- **Reject `O-1`:** `R-7`, `P-3`, and `R-12` are now orphans (their chain leads to a
  rejected node). They are flagged, not deleted.

In a file-based library, "walk the edge" is literally `grep -rn 'derives_from'` plus
following the cited keys. No tool is required; any agent or human can do it with a search.

## Who quotes / relies on this edge

This stub is a shared dependency. Each of these **quotes the canonical block** and relies on
the edge being present and stable:

| Skill | How it uses the edge |
|---|---|
| `understand/decompose-intake-to-outcomes` | **Writes** the edge — every derived requirement it emits carries a `derives_from:` to its accepted outcome (or capability). This is where edges are born. |
| `architect/propagate-pattern-nfrs` | On pattern adopt, emits each `attached_nfr` as a derived requirement with `derives_from:` the pattern key `P-*` — so adopted NFRs join the same graph. |
| `architect/validate-solution-vs-requirements` | **Walks upward** from each compromised/violated requirement to name the outcome and capability that degrade; reports impact by citation, never as a status. |
| `challenge/necessity-check` | Poses "necessary for which outcome?" by reading a component's `derives_from:` chain — answerable *only because* the edge exists; names both keys, hands the cut/keep call to the human. |
| `deliver/triage-backlog-and-defer` | Detects **orphans** (edges whose chain leads to a rejected/absent key) and leads the handoff with them; sorts the delta by deterministic edge facts, never by a recommended disposition. |

If you add a skill that derives, validates, cuts, or surfaces anything against an upstream
commitment, it should quote this block too.

## Why a citation and not a foreign key

A `derives_from_id` column distinct from a version chain is correct *for a database*. This
library runs in **any** LLM workflow that can read a file — Claude Code, a plain prompt, a CI
step, a coding agent pointed at the repo — so there is no row to reference and no id to
dereference at read time. A `req_key` citation survives being copied, diffed, PR-reviewed, and
grepped; a foreign key does not survive leaving its database. The trade is deliberate:
referential-integrity enforcement is given up (a key can be cited that no longer exists — that
is exactly an *orphan*, and it should be visible), in exchange for a portable edge that works
with `grep` and merges cleanly in a PR.

## Relationship to the rest of the library

- The **rhythm** these edges live inside — propose → ratify-by-merge — is
  `skills/_shared/propose-ratify.md`. An edge is proposed by an agent in a branch and
  ratified when the PR merges; a re-derivation is a fresh proposal, not a mutation.
- The **output discipline** that keeps the edge a citation and never a verdict is
  `skills/_shared/target-rule.md`. The edge targets the **RECORD** (it structures for
  reuse and impact-tracing); it must never be dressed up as a JUDGMENT.
- The **drift check** that pins quoted copies to this file is the
  `check-shared-stub-drift` GitHub Action.
- Both Actions are **advisory CI**: they comment and fail the *check* to prompt a human
  fix. Neither blocks a downstream project. The machine catches a broken or drifted edge;
  a human still owns every accept, cut, and override.

Keep it light. One stable key, one `derives_from:` line, walkable both ways — that is the
whole edge.
