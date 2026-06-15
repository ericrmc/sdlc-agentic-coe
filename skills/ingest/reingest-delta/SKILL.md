---
name: reingest-delta
description: Re-read a previously-staged source, diff it against the prior version (row-level for tabular sources), and surface ONLY what changed — a requirement reworded, an acceptance criterion altered, a ticket status flipped, a row added or dropped — as a proposal/question. Never silently overwrites an existing requirement; an unreadable re-read HALTs, never returns empty.
one_liner: Re-read a staged source, diff against the prior version, and surface only what changed — never silently overwrite.
aliases: [reingest, re-ingest a source, diff a source, what changed in the requirements, source delta, requirements drift, ticket status flipped, row-level diff, second pass ingest, update from a new export]
when_to_use: a source already staged and ingested has a new version, and you need to surface only the changes against the prior version rather than re-ingesting the whole thing
output_kinds: [proposal, question, halt]
deterministic_fallback: the delta readers in skills/ingest/_scripts/ (row-level set/diff keyed on source_ref + per-block sha256 from the prior staging) yield added / removed / changed / unchanged buckets with no model
suggested_tier: mid
tier_reason: the diff itself is a deterministic keyed set-comparison; the model only judges whether a textual change is material (a reworded requirement) or cosmetic (whitespace), and proposes how each change lands — it never decides the overwrite
neighbours:
  before: skills/ingest/stage-and-fingerprint (binds the new version to its prior staged record; routes here when source_ref matches and content_hash differs)
  after: skills/understand/classify-requirements (re-annotates the changed requirements; re-surfaces a now-stale source as a question)
---

# reingest-delta — surface only what changed, never silently overwrite

A staged source rarely arrives once. A stakeholder re-exports the spreadsheet, a board's tickets
move, a doc gets edited. Re-reading the whole thing and re-minting every requirement would either
duplicate the set under new keys or silently clobber human edits made since the first ingest. This
skill does neither: it **diffs the new version against the prior one** and surfaces **only the
delta** — what was added, removed, reworded, or had its status flipped — as a proposal a human
ratifies, with the genuinely ambiguous changes raised as questions.

The rule that governs it: **never silently overwrite.** A change to an already-ingested requirement
is a *proposed* change a human accepts in a diff, never an in-place mutation.

Its outputs are a **proposal** (the per-change update markdown), a **question** (a change that needs
a human call — a status flip, a moved locator), and a **halt** (the re-read itself is unreadable).
Those are the only output kinds: proposal, question, halt.

## When to use

- A source that was already staged and ingested has a **new version** (re-export, edited doc, moved
  tickets), and `stage-and-fingerprint` has bound it to its prior staged record.
- You want the **changes only**, mapped onto the existing requirements — not a fresh full ingest.

Do not use this for a first ingest (that is `ingest-source-to-requirements`) or for a brand-new
source with no prior version (there is nothing to diff against — stage and ingest it fresh).

## Inputs

| Input | Required | What it is — and the if-absent behaviour |
|---|---|---|
| **The new (re-staged) version** | **Required.** | The freshly-staged copy of the source. If absent/unreadable/empty: **HALT** (per `_shared/grounding.md`); never diff against a hypothetical. An unreadable re-read is **HALT — not empty** (see STEP 1), never a "nothing changed." |
| **The prior version + its fingerprints** | **Required.** | The previously-staged copy and its per-block sha256 / `source_ref` records. If absent: there is no baseline to diff — **HALT and ask for the prior staged record** (or route to a first ingest); never invent a baseline. |
| **The existing ingested requirements** | **Required.** | The current requirement markdown (with `source_ref`s) the delta lands on. If absent: **HALT** — a delta with nowhere to land is a full ingest; route to `ingest-source-to-requirements`. Never overwrite requirements you cannot read. |

## Grounding (quoted)

<!-- BEGIN grounding (byte-stable; do not edit a quoted copy — edit _shared/grounding.md) -->

**GROUNDING RULE — name the required inputs; an absent required input HALTs and asks, never assumes.**

A skill **names its required inputs** up front (its Inputs section marks each row Required or
Optional). Then:

- **A required input that is absent, unreadable, or empty becomes a `halt`.** The halt asks
  the user *where the input is*, offering the formats ingestion can read (an xlsx/csv path, a
  GitHub Project owner+number, a docs folder, or a pasted block). It then **stops and waits.**
  It never assumes, invents, or reasons over a hypothetical — no invented id, key, number, NFR,
  requirement, acceptance criterion, file path, or source row.
- **Partial input is named, not patched.** When some required inputs are present and others are
  not, the skill **names exactly what is missing and asks for it** — it never silently proceeds
  on the part it has, and it never back-fills the gap with a plausible-looking guess.
- **An absent *optional* input proceeds honestly.** It is surfaced as a `question` or recorded
  as an explicit null — never padded with invented content to look complete.

**"I read nothing" and "I cannot read this" are different outputs.** An unreadable or
unsupported source HALTs (it asks for a readable form); it never returns an empty result, because
a silent-empty reads downstream as "the source had nothing in it" — a silent-proceed failure.

**A halt is a question, never a verdict.** A halt names the missing input and asks where it is.
It never smuggles a finding, an assumption, or a disposition for a human to rubber-stamp — no
"I halt because this is infeasible / too risky / out of scope." Those are JUDGMENTs the human
owns. The halt carries only: *what is required, what is missing, and the formats it can be read
from.*

<!-- END grounding -->

## Req-key scheme (quoted)

<!-- BEGIN req-key-conventions (byte-stable; do not edit a quoted copy — edit _shared/req-key-conventions.md) -->

**REQ-KEY SCHEME — one prefix per kind; parentage lives in fields, never in the key.**

| Key | Kind | Notes |
|---|---|---|
| `BO-<n>` | Business outcome | `BO-1`, `BO-2`, … one integer counter per project. |
| `REQ-<n>` | Requirement | Functional **or** non-functional. F/NF is `classify` metadata, **never part of the key**. |
| `CAP-<SLUG>` | Capability | Upper-kebab slug, e.g. `CAP-OLAP`. Established under `capabilities/`. |
| `PAT-<SLUG>` | Component pattern | Upper-kebab slug, e.g. `PAT-WEBAPP-PG`. Established under `patterns/`. |
| `DEC-<n>` | Decision | A contested call, an ADR, a recorded dissent. |
| `AC-<REQ>.<n>` | Acceptance criterion | **Optional child key**, e.g. `AC-REQ-7.1`. Use only when an AC needs its own citation target; otherwise an AC is just a line under its requirement. |

A key is plain text, optionally rendered as a markdown link to the file/anchor that
defines it. It needs no database, no id, no schema. Keys are **stable for the life of
the project** — renaming or renumbering one silently breaks every field that cites it.

**THE ONE NORMALISATION RULE.** Read the key scheme **from the target file; never assume
one.** When a source uses some other prefix (`OUT-`, `TR-`, `F-`, `NF-`, `O-`, `R-`, `D-`,
a bare integer, …), normalise on write to the scheme above — outcome → `BO-`, requirement
(F or NF) → `REQ-`, decision → `DEC-`, capability → `CAP-`, pattern → `PAT-` — **and
preserve the source's own identifier verbatim as a `source_ref` field**, so a re-read
matches on `source_ref` and not on a minted key that renumbers across schemes.

**TRACE VIA FIELDS, NEVER IN THE KEY.** All parentage and relationship is a field on the
artefact, naming the **stable key** of the thing it points at:

- `derives_from:` — the upstream node this artefact serves (the single trace edge). This is
  the **one** parentage field: an outcome's capability, a requirement's outcome, a derived
  NFR's pattern. (There is no separate `derives_from_outcome_key`; it is `derives_from`.)
- `fulfils_capability:` — the `CAP-<SLUG>` a requirement fulfils.
- `fulfilled_by:` — the `PAT-<SLUG>`(s) a capability is fulfilled by.
- `supersedes:` / `superseded_by:` — version succession between two keys of the same kind.
- `contests:` — the key this artefact contests (a conflict, a dissent).

`derives_from` is a **citation, never a verdict** — it records *what serves what*; it never
asserts a thing is necessary, sufficient, good, or done. Those are human calls.

<!-- END req-key-conventions -->

> The diff keys on **`source_ref`** above — the source's own identifier, preserved verbatim at first
> ingest. Matching on `source_ref` (not on the minted `REQ-<n>`, which renumbers across schemes) is
> what lets a re-read find the *same* requirement and propose a change to it, rather than minting a
> duplicate under a new key.

## The method (numbered steps)

### STEP 0 — confirm a prior version exists (deterministic, pre-model)

A delta needs a baseline. Confirm all three required inputs are present as a file-level fact: the
new staged version, the prior staged version + its fingerprints, and the existing ingested
requirements. Any one missing → **HALT** and name exactly what is missing (per the grounding rule).
A re-ingest with no prior version is not a delta — route it to `ingest-source-to-requirements` for a
first ingest. Never invent a baseline to diff against.

### STEP 1 — re-read the new version to blocks (deterministic; HALT-not-empty)

Run the same deterministic reader as ingest (`skills/ingest/_scripts/`) over the **new** staged
version, producing blocks with the same locator + sha256 shape. The prior version's blocks and their
sha256 are already on record from staging.

> **HALT — not empty.** If the new version exists but cannot be re-read (corrupt re-export,
> unsupported format), emit a halt that says "I cannot read this version" and asks for a readable
> form. **Never return "nothing changed."** A silent-empty re-read reads as *the source is
> unchanged*, which would hide a real update — a trust failure.

### STEP 2 — diff, keyed on source_ref + per-block sha256 (deterministic)

Compare the new blocks against the prior blocks, **keyed on `source_ref`**, sha256 deciding
changed-vs-unchanged. For tabular sources this is a **row-level** set comparison. Bucket every block:

- **unchanged** — same `source_ref`, same block sha256. Carried forward untouched; **not** re-minted,
  **not** re-proposed. (The whole point: a stable row is left alone.)
- **changed** — same `source_ref`, different block sha256. The requirement, an acceptance criterion,
  a rationale, or a status moved. Flagged for STEP 3.
- **added** — a `source_ref` present in the new version, absent in the prior. A new requirement.
- **removed** — a `source_ref` present in the prior version, absent in the new. The source dropped
  it — surface as a question (*confirm whether it was intentionally removed*), never auto-delete the
  ingested requirement.

This bucketing is mechanical and is the deterministic fallback. It needs no model.

### STEP 3 — characterise each change (the model step)

For each **changed** block, the model judges *what* changed and whether it is material, then proposes
how it lands — but **never writes the change in place.** Categories to name explicitly:

- **requirement reworded** — the `The system shall …` text moved. Show the before/after; propose it
  as an edit to the existing `REQ-<n>` (its key and `source_ref` stay; only the text changes).
- **acceptance criterion altered** — a GIVEN/WHEN/THEN changed. The **locator discipline still
  holds**: a changed AC must still carry a source locator; if the new version *removed* the AC, mark
  it **absent (was: …)** — never keep the old AC silently and never synthesise a replacement.
- **status flipped** — a ticket moved (e.g. `In Progress` → `Done`, `Open` → `Won't Do`). Surface as
  a **question**, because a status change often changes whether the requirement is still in scope —
  a human call, not an auto-update.
- **cosmetic only** — whitespace, reordering, a non-semantic edit. Name it as cosmetic and propose
  carrying it forward with no requirement change, so the reviewer is not asked to ratify noise.

A material change to an already-ingested requirement is always a **proposed diff**, never an in-place
overwrite. The human accepts it in the PR.

### STEP 4 — flag downstream artefacts whose cited locator moved

When a block's **locator** changed (a row moved, a heading renumbered), any downstream artefact that
cited the *old* locator now points at the wrong place. Surface these as questions: *"`REQ-7` cited
`sheet:Reqs!B12`; that content is now at `sheet:Reqs!B15` — confirm the citation."* Re-stamp the
`Source` line on the changed requirement (new locator, new sha256, new `received_at`), and re-surface
any `staleness-unverified` caveat — so a re-ingested-but-stale row does not launder clean.

### STEP 5 — propose the delta as a PR

Emit **only the delta** as a PR a human ratifies by merging: the changed requirements as proposed
edits, the added ones as new blocks (full ingest shape, via `ingest-source-to-requirements`), the
removed and status-flipped ones as questions. Unchanged requirements do not appear in the diff at
all. Then route the changed requirements through `classify-requirements` to re-annotate their shape
metadata and re-surface staleness.

## Output format

A delta report — buckets, then the proposed edits. Unchanged blocks are summarised by count only.

```markdown
# Re-ingest delta — intake-requirements.xlsx (v2026-06 vs v2026-05)

**Diffed on:** source_ref + per-block sha256 · row-level. **Baseline:** staged/…2026-05.xlsx

## Summary
- unchanged: 11   • changed: 3   • added: 1   • removed: 1

## Changed (proposed edits — ratify in the diff; nothing overwritten in place)

### REQ-7 — requirement reworded
- **source_ref:** JIRA-4821  (unchanged — same requirement, edited text)
- **before:** The system shall publish routes within 30 seconds.
- **after:**  The system shall publish routes within 10 seconds.   *(source: sheet:Reqs!E12)*
- Proposed: update REQ-7's text; re-run classify (quantified target changed).

### REQ-9 — acceptance criterion altered
- **source_ref:** JIRA-4830
- **before AC:** GIVEN … THEN within 5 min.  *(source: sheet:Reqs!E14)*
- **after AC:**  — (absent in new version)    <!-- AC removed upstream: flag absent, do not keep silently -->
- Question: the source removed this acceptance criterion — confirm whether it was intentional.

## Status-flipped (questions — a scope call, not an auto-update)
- REQ-12 (source_ref ENG-77): status In Progress → Won't Do. In scope still? Confirm.

## Removed (questions — never auto-deleted)
- REQ-15 (source_ref ROW-22): present in v2026-05, absent in v2026-06. Confirm the source dropped it.

## Added (full ingest shape, via ingest-source-to-requirements)
- new source_ref JIRA-4901 → propose REQ-18.

## Locator moves (citation check)
- REQ-7's content moved sheet:Reqs!B12 → B15; re-stamped its Source line; confirm any external citation.
```

### Deterministic fallback

The delta readers in `skills/ingest/_scripts/` produce the entire bucketing — unchanged / changed /
added / removed — with no model, by keying on `source_ref` and comparing per-block sha256. That set
diff is a legitimate, useful output on its own: it tells a human exactly which requirements moved,
without characterising *how*. The model step (STEP 3) only adds the before/after wording and the
material-vs-cosmetic call on top of that deterministic floor.

## Notes & anti-patterns

**Anti-patterns — reject these on sight:**

- **Silently overwriting a requirement.** A change is always a **proposed diff** a human ratifies,
  never an in-place mutation — human edits made since the first ingest must survive a re-ingest.
- **Re-minting unchanged requirements.** A stable row (same `source_ref`, same sha256) is carried
  forward untouched and never re-proposed; re-minting would duplicate it or renumber the set.
- **Auto-deleting a removed requirement.** A `source_ref` gone from the new version is a **question**
  (was it intentionally dropped?), never a silent delete — the source may have a bug, not a decision.
- **Synthesising a replacement AC.** If a re-export removed an acceptance criterion, mark it
  **absent (was: …)**; never keep the stale one silently and never invent a new one. The
  locator-present-or-absent discipline holds across re-ingests, not just the first.
- **"Nothing changed" on an unreadable re-read.** Unreadable → HALT — not empty (STEP 1). A
  silent-empty re-read hides a real update.
- **Diffing on the minted key.** The diff keys on `source_ref`; a `REQ-<n>` renumbers across schemes
  and would mismatch the same requirement against itself.

**Notes:**

- **Only the delta is the deliverable.** Unchanged requirements never enter the diff; the reviewer
  sees exactly what moved and nothing else.
- **Provenance is re-stamped, not lost.** A changed block gets a fresh `Source` line (new locator,
  sha256, `received_at`) and re-surfaces staleness; a moved locator flags downstream citations.
- **Advisory, never a gate.** The delta is a PR ratified by a merge; the halt stops *this run* and
  asks. Nothing here blocks a release. (See `skills/_contract/propose-ratify-rhythm`.)
