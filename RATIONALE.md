# RATIONALE — the cross-cutting synthesis, and the guard

> Companion to [`CONTRIBUTING.md`](CONTRIBUTING.md) and [`ADR.md`](ADR.md).
> [`ADR.md`](ADR.md) owns the per-decision *why* (the slimmed survivor set of
> architectural records); [`CONTRIBUTING.md`](CONTRIBUTING.md) is the *how-to*;
> the routine field conventions live at the schema descriptions
> (`patterns/_schema`, `capabilities/_schema`) and are enforced by the linters.
> **This file is the part none of those carry: the cross-cutting synthesis — how the
> load-bearing invariants reinforce each other — and the guard that maps a tempting
> change to the property it would dissolve.**

You are the agent (or the human directing one) about to change something here. A line
that looks like a one-liner — rename a folder, add an output kind, make a check
blocking, set a status on a pattern — can quietly dissolve the one property that lets an
advisory library be safe without gates. **Read §6 (the guard) before a structural
change**, follow its `ADR-NNNN` into [`ADR.md`](ADR.md) for the full why /
alternatives / dissent, and if your change weakens an invariant, open it as a proposal
that names the invariant and its ADR and let a human rule.

This document obeys the library's no-fabrication rule: where a rationale is **not
recorded anywhere**, it says "confirm with maintainers" rather than inventing one.

---

## 1. What this library is, and where it came from

A **portable library of self-contained markdown `SKILL.md` files** an agent reads and
runs inside *any* LLM workflow — a coding agent, a plain prompt, a CI step. It is **not
an app and not a service**. It carries a PR-reviewed library of reusable component
**patterns** and the **capabilities** that bridge a plain-language need to a proven
pattern. Every output is light and advisory: the skills nudge, they never block.

**Where this came from (the pivot).** The proven method was **lifted out of a prior
internal delivery tool** — a bespoke app with hard architecture-review and approval
gates. The business would not support a custom app, so the *method* was preserved and
the *plumbing* (runtime, enforcement gates, central service) was dropped. The value is
the provider-agnostic reasoning, not the machinery that hosted it. That single fact
drives most of what follows, and it is why this library is gate-free by construction
(**ADR-0001**, the pivot; and the dropped-enforcement context behind **ADR-0002**).

This doc never names the old tool. Lineage to other entities was deliberately stripped
at de-narration because narrative about other systems drifts a reading agent off task,
and the instructions are written agent-first, standalone, and token-lean for exactly
that reason (**ADR-0010**).

---

## 2. The load-bearing invariants

These are the few rules that must not be broken without deep understanding. Each is
owned by an ADR (cited) where the full why / alternatives / dissent live; what follows
is the compact list plus the synthesis this doc exists to carry.

| Invariant | One-line statement | Owner |
|---|---|---|
| **2.1 TARGET RULE** (keystone) | Every output is exactly one of four kinds — `proposal` \| `question` \| `menu` \| `halt` — and **never** a verdict, score, RAG colour, ranking, disposition, or an assessment of a person. | **ADR-0003** |
| **2.2 Propose → ratify** | One ratification act only: a **human merging the PR**. The agent never merges, writes a "ratified" status, or auto-advances; the merge commit + PR thread *is* the audit record. | **ADR-0004** |
| **2.3 Advisory, not gated** | Every Action comments / may fail a check but **never blocks a merge**. `CODEOWNERS` is the *one* structural gate — human review required under `patterns/**` and `capabilities/**`. | **ADR-0002** |
| **2.4 Grounding / no fabrication** | A skill names its required inputs; an absent / unreadable / empty one becomes a typed `halt` (computed at STEP 0, before any model) — never an invented id, key, number, NFR, or AC. | **ADR-0005** |
| **2.5 Deterministic base + a model step** | Every skill has a no-LLM base that stands alone; the model is one line that only *deepens* it and is **never fatal**. Named by tier hint (`frontier` \| `mid` \| `light`) behind a seam — no model ids or vendor names. | **ADR-0006** |
| **2.6 Trace via fields, not in the key** | Parentage and relationships live in **fields** (`derives_from`, `fulfils_capability`, …) as portable `req_key` citations, never inside the key and never as foreign keys; rollups / RAG verdicts / maturity tallies are **recomputed on read**, never stored. | **ADR-0007** |
| **2.7 Anti-fatigue** | A re-run reviews only the **delta-since-last-green**; `dismissal-memory` re-arms only on changed evidence; **no** throughput, velocity, or per-person metric is computed or stored. | **ADR-0008** |

**The synthesis — how they reinforce each other (this doc's unique value).** The
TARGET RULE (§2.1) is the keystone: because the *shape* of an output forbids
self-approval, the library can automate aggressively without a blocking mechanism — so
propose→ratify (§2.2), advisory-not-gated (§2.3), and the absence of any throughput
score (§2.7) are not three separate stances but three faces of the same one. The two
remaining catastrophic failure modes a gate-free library still has are *clean output
grounded in nothing* and *a smuggled verdict*; grounding (§2.4) closes the first as a
deterministic pre-model fact, and §2.7's no-metric rule closes a number-shaped verdict.
The trace edge (§2.6) is what makes auto-derivation safe — a derived row is a proposal
threaded to an already-accepted parent, so rejecting upstream *visibly orphans* its
subtree rather than silently cascading (the accept-high / derive-low net, **ADR-0007**),
and a recomputed-on-read value is never a stored verdict an agent asserted, reinforcing
§2.1 again. The deterministic base (§2.5) is the reason all of the above is *portable*:
every guarantee holds in a bare terminal with no API key, because the model is an
enrichment, never a dependency.

---

## 3. Where the per-decision "why" lives (not here)

This document does **not** carry decision-record tables. The architectural, contested,
and hard-to-reverse decisions — and only those — are the numbered, status-tracked,
immutable records in [`ADR.md`](ADR.md). The **routine field and schema conventions**
(key shapes, enum values, required sub-fields, numeric bounds) are documented at the
schema descriptions in [`patterns/_schema`](patterns/_schema) and
[`capabilities/_schema`](capabilities/_schema) and in [`CONTRIBUTING.md`](CONTRIBUTING.md),
and are **enforced by the linters** — the lint *is* their guard, so they do not need to
be immortalised as status-tracked records. If you want the *why* of a decision, follow
its `ADR-NNNN` from §2 or §6; if you want the *shape* of a field, read the schema.

---

## 4. Lessons & near-misses — the durable "why-not" record

These bugs were caught by **adversarial review passes** before they shipped, recorded so
the same class of mistake is recognised next time. The reusable lesson runs through all
of them: **a mass change must own *every* file class, and an adversarial grep/lint pass
across all file types — including generated artefacts — is what catches the near-miss.**

| Near-miss caught | The lesson it teaches |
|---|---|
| A **governance-gate BYPASS on a backward re-open** (carried over from the precursor tool): a reopen that did not re-arm the gate let work bypass it (`open==0` passes). | A backward door (reopen / scope-change) must **re-arm** the gate (demote passed checks → pending), or it silently bypasses it. |
| A **pattern-key scheme that contradicted itself** across schema / linter / seeds — **0 of 3 seeds passed** before reconciliation. | A key scheme is a contract across *three* surfaces (schema, linter, seed examples); reconcile all three or none agree. Part of why the canonical-key migration was done as one clean scheme (**ADR-0011**). |
| A **front-door map naming a numbering scheme that did not match the tree.** | The index and the on-disk tree are one artefact in two places; a rename touches both. Part of why dynamic dir-discovery is load-bearing (**ADR-0009**). |
| **~12 skills citing reference files that were never authored.** | A cite is a promise; a reference-link lint must resolve every cited path against the on-disk tree. |
| **Lineage leaks left in pattern BODIES and the generated bundles** after a mass de-narration — *because no agent owned that file class.* | A mass change must enumerate **every** file class it touches — including `generated/` artefacts — and assign an owner to each. This is *the* recurring lesson, and the why behind the agent-first de-narration (**ADR-0010**). |
| An **ingest SILENT-EMPTY path**: a readable-but-empty source proceeding instead of halting — the exact failure grounding forbids. | "I read nothing" ≠ "I cannot read this" ≠ "I proceeded on nothing." HALT-not-empty exists because this slipped through once (§2.4, **ADR-0005**). |
| A **grounding-lint BLIND SPOT** that let two author skills with required inputs escape the check. | A lint's *coverage* is itself a thing to adversarially test — "which skills with required inputs does this check NOT see?" |
| A **placeholder reference-implementation URL note** computed but **swallowed** on a passing file. | An advisory note that is computed must also be *surfaced*; a note swallowed on the happy path is a note that does not exist. |

---

## 5. Honest limitations — state these plainly

These are real and recorded; do not let a future change paper over them with false
confidence.

- **A static grounding lint cannot catch a model inventing an input at runtime.** It
  checks only that a skill cites the stub and wires a halt path. The contract + the halt
  exemplar are the *real* safeguard; the lint catches the documentation miss and the
  wiring miss, nothing more (§2.4, **ADR-0005**).
- **PR-is-ratify is a forced fit for in-session iteration.** Intra-session work happens
  on the branch with no ceremony; "a human always disposes" is review culture, not code
  (§2.2, **ADR-0004**).
- **Advisory CI can let a malformed pattern merge** if a reviewer ignores a red check.
  `CODEOWNERS` is the single backstop; `validate-patterns` *may* be flipped to required
  for `patterns/**` only — the one reserved escape hatch in the no-gate stance (§2.3,
  **ADR-0002**).
- **`req_key` citation stability is unguarded.** Renaming/renumbering a key silently
  breaks every field that cites it; nothing enforces referential integrity but the lint
  and human review (§2.6, **ADR-0007**).
- **The deterministic base is allowed to be shallow.** The bar is only "a reviewer would
  accept the no-model output as a draft"; depth without a model is a known limitation,
  not a promise (§2.5, **ADR-0006**).
- **Computed fields (`maturity`, `adoption_count`) are never authored** — arithmetic over
  `adoptions/ledger.jsonl`, so a pattern cannot self-declare its track record — and the
  recomputation depends on downstream projects appending their adoption line; if they
  don't, the tally under-counts (an org-repo scan is deferred) (**ADR-0013**).
- **SharePoint and live boards are export-only**, by design, due to auth + stale-doc
  risk. There is no live connector; the HALT branch is the whole of that support
  (**ADR-0015**).
- **Large surface area** is the named cost of the de-narrated, category-spread design;
  mitigated by the map + persona table + `meta/navigator`, not eliminated.
- **No vector index.** Skills read pattern/capability files directly — fine for tens of
  files, a known ceiling that needs an index Action at hundreds.

---

## 6. Before you make a major change — the guard

If you are about to do something in the left column, read the invariant and the
`ADR-NNNN` in the right columns **first**. These are the changes most likely to dissolve
a load-bearing property by accident.

| Tempting change | Invariant it touches | Read first |
|---|---|---|
| Add a fifth output kind / let an agent emit a verdict, score, or RAG colour | TARGET RULE (§2.1) — the keystone | §2.1 · ADR-0003 |
| Let an agent merge its own PR, or persist a "ratified" status | Propose → ratify (§2.2) | §2.2 · ADR-0004 |
| Make an Action blocking, or remove the `CODEOWNERS` gate | Advisory-not-gated; the one structural gate (§2.3) | §2.3 · ADR-0002 |
| Move `patterns/` or `capabilities/` under `skills/`, or rename them | The one structural gate is path-keyed | §2.3 · ADR-0002, ADR-0009 |
| Let an ingest read return empty on an unreadable/empty source | HALT-not-empty; grounding (§2.4) | §2.4 · ADR-0005, ADR-0015 |
| Make a skill's first step "ask the model" (no deterministic floor) | Deterministic base + model step (§2.5) | §2.5 · ADR-0006 |
| Name a concrete model / vendor in a skill | Provider-agnostic seam (§2.5) | §2.5 · ADR-0006 |
| Put parentage *in* a key, or switch `derives_from` / fulfilment edges to foreign keys | Trace via fields; portable citation; orphaning net (§2.6) | §2.6 · ADR-0007, ADR-0011 |
| Change or revert the canonical key scheme | One canonical scheme (panel-vs-maintainer dissent recorded) | §2.6 · ADR-0011 |
| Persist a RAG colour / score, or add a throughput / per-person metric | Projections-not-persistence (§2.6); anti-fatigue (§2.7) | §2.6, §2.7 · ADR-0007, ADR-0008 |
| Re-surface a dismissed cue against unchanged evidence | Anti-fatigue dismissal-memory (§2.7) | §2.7 · ADR-0008 |
| Rename or re-number the skill folders | Named-as-purpose categories; open dynamic scheme | ADR-0009 |
| Author a pattern/capability as pre-approved (`provisional`/`approved`/`proven`); author `maturity`/`adoption_count` by hand | Human-only lifecycle; evidence-before-promotion; code computes maturity | ADR-0013 |
| Wire a "start here" reference implementation into the promotion gate | Gate-bleed; evidence is the only promotion door | ADR-0014 |
| Remove the capability layer, or break its requirements→components bridge | Capabilities are the named middle term | ADR-0012 |
| Reorder or rename a frozen solution-architecture section, or fold ingestion's deterministic read into the model step | Sequenced-trust foundation; structural lifted-vs-fabricated fact | ADR-0015 |
| Do a mass edit (de-narration, rename, vocab change) | Every-file-class ownership; adversarial grep pass | §4 · ADR-0010 |
| Present a static lint as a fabrication guarantee | Honest reach of the grounding lint | §2.4, §5 · ADR-0005 |

---

*Canonical per-decision record: [`ADR.md`](ADR.md) — the numbered, status-tracked log of
immutable records that owns the why / alternatives / dissent for every architectural
decision. Routine field and schema conventions are documented at the schema descriptions
([`patterns/_schema`](patterns/_schema), [`capabilities/_schema`](capabilities/_schema))
and in [`CONTRIBUTING.md`](CONTRIBUTING.md), and enforced by the linters. This file
carries only the cross-cutting synthesis (§2), the lessons / near-misses (§4), the honest
limitations (§5), and the guard (§6) — the part none of the others hold. Where a
rationale is not recorded in any of these, this document says so rather than inventing
one.*
