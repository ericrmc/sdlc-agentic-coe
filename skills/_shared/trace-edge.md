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
markdown link. That trade is deliberate: referential integrity is given up (a cited key can
stop existing — that is an *orphan*, and it should be visible) for an edge that survives
`grep`, diff, and PR review. The block below is the source of truth; the wrapper around it
is author-facing only.

---

## The canonical block (quote this verbatim)

<!-- BEGIN trace-edge (byte-stable; do not edit a quoted copy — edit _shared/trace-edge.md) -->

**TRACE EDGE — `derives_from` is a portable `req_key` citation, not a foreign key.**

Every derived artefact carries a `derives_from:` line naming the **stable `req_key`** of
the upstream node it serves. The edge is plain text — a key, optionally a markdown link
to the file/anchor that defines that key. It needs no database, no id, no schema:

```
derives_from: BO-1
```

or, when the upstream node lives in another file:

```
derives_from: [BO-1](../outcomes/OUTCOMES.md#bo-1)
```

`req_key`s are short, human-readable, and **stable for the life of the project** — they
are the citation target, so renaming or renumbering one silently breaks every edge that
cites it. Conventional prefixes (advisory, not enforced):

- `CAP-<SLUG>` business **C**apability
- `BO-*` business **O**utcome
- `REQ-*` derived **R**equirement (functional or non-functional; F/NF is classify metadata, not part of the key)
- `PAT-<SLUG>` adopted **P**attern
- `DEC-*` **D**ecision / contested call / dissent

The edges compose into one directed **outcome-impact graph**:

```
capability    ->  outcome  ->  requirement  ->  pattern        ->  decision
CAP-<SLUG>        BO-*          REQ-*            PAT-<SLUG>          DEC-*
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

**A rejected upstream node orphans its entire subtree.** If a human rejects outcome `BO-1`,
every artefact whose `derives_from:` chain leads to `BO-1` is now an **orphan** — it points
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

## Worked example (one edge, both walks)

```markdown
<!-- requirements/REQUIREMENTS.md -->
## REQ-7 — Full-text index with sub-200ms p95 query latency
req_key: REQ-7
classify: functional
derives_from: [BO-1](../outcomes/OUTCOMES.md#bo-1)
```

The walk is plain `grep`, no tooling: **down** — `grep -rn 'derives_from:.*BO-1'` lists every
artefact synthesised beneath `BO-1`; **up** — read `REQ-7`'s `derives_from:` to `BO-1` to name
the outcome it serves (and on to its `fulfils_capability:`); **reject `BO-1`** — that same down
set is now orphaned (flagged, not deleted).

## Pointers

- Quoted by skills that **write** the edge (intake decomposition, pattern-NFR propagation) and
  that **walk** it (solution validation, necessity check, backlog triage / orphan detection);
  each declares the dependency in its own frontmatter.
- The edge targets the **RECORD**, never a verdict — `skills/_shared/target-rule.md`.
- The propose → ratify-by-merge rhythm an edge lives inside — `skills/_shared/propose-ratify.md`.
- Pinned to this file by `check-shared-stub-drift` (advisory CI).
