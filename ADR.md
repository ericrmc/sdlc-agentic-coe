# ADR — architectural decision log

This is the library's **canonical, append-only, status-tracked record of architectural
decisions**. Each record `ADR-NNNN` is immutable and self-contained: it states one
decision, the forces that produced it, what it gives and what breaks if changed, the
road-not-taken (including the real panel-vs-maintainer disagreements), and the in-repo
evidence for the why. A reader can open any single record and understand it without
reading the others.

**This log was consolidated to the load-bearing decisions at its inception.** It records
only the decisions that are genuinely **architectural, contested, or hard-to-reverse /
load-bearing-for-safety** — the calls a future contributor must not undo without deep
understanding. The many **field-level conventions** (a key regex, a required frontmatter
slot, a closed enum, a lint rule, a folder-naming convention) are **not** immortalised
here: they live at the **schema descriptions** and in **`CONTRIBUTING.md`**, and the
**linters are their guard** — the lint *is* the enforcement, so a status-tracked record
would be a second source of truth for a fact a check already owns. From this point on the
log is **immutable and append-only**: the consolidation was a one-time housekeeping pass
on a day-old draft with no external adopters; supersession-not-rewrite applies to every
record from here.

This log is the **one owner** for each decision's why. `RATIONALE.md` narrates how the
decisions hang together and **cites** these records rather than restating them — the
library forbids two sources of truth for the same fact. To add a decision, append the
next number; nothing earlier is edited. To reverse a decision, append a **new** record
and mark the old one `Superseded by ADR-NNNN` — a record is never rewritten in place,
so the history of what was decided (and later undone) stays legible.

Every why here is evidenced in an in-repo file or a commit. Where a rationale was not
recorded anywhere, the record says so ("confirm with maintainers") rather than inventing
one.

## Status legend

- **Accepted** `<commit/date>` — in force; the decision holds.
- **Superseded by ADR-NNNN** — reversed or replaced; read the named successor for the
  current decision. This record stays for history.
- **Deprecated** — withdrawn with no direct successor.

## Index

| ID | Title | Status |
|---|---|---|
| ADR-0001 | A portable skill library, not an app (the pivot) | Accepted (1bffad7, 2026-06-15) |
| ADR-0002 | Advisory, not gated — no enforcement gates; CODEOWNERS the one structural gate on patterns/ + capabilities/ | Accepted (1bffad7, 2026-06-15) |
| ADR-0003 | The TARGET RULE — four output kinds, never a verdict (the principled enabler of gate-free) | Accepted (1bffad7, 2026-06-15) |
| ADR-0004 | Propose → ratify — a human merge is the only ratification | Accepted (1bffad7, 2026-06-15) |
| ADR-0005 | Grounding / no fabrication — an absent / unreadable / empty required input HALTs | Accepted (580e236, 2026-06-16) |
| ADR-0006 | Deterministic base + a one-line model step — a model call is never fatal (portability) | Accepted (1bffad7, 2026-06-15) |
| ADR-0007 | Trace via fields, never in the key; projections recomputed not persisted; accept-high / derive-low safety net | Accepted (1bffad7, 2026-06-15) |
| ADR-0008 | Anti-fatigue — delta-since-last-green, dismissal-memory, no throughput / per-person metric | Accepted (1bffad7, 2026-06-15) |
| ADR-0009 | Looser named categories, numbers dropped, open (dynamically-discovered) scheme | Accepted (5877839, 2026-06-15) |
| ADR-0010 | Agent-first voice + de-narration — instructions read by agents; standalone, token-lean | Accepted (5877839, 2026-06-15) |
| ADR-0011 | One canonical req-key scheme + full migration (records the panel-vs-maintainer dissent) | Accepted (1d55b80, 2026-06-16) |
| ADR-0012 | Capabilities are a first-class entity — the requirements-to-components bridge | Accepted (5877839, 2026-06-15) |
| ADR-0013 | Pattern lifecycle is human-owned — evidence-gated promotion, agent-writes-candidate-only, maturity computed | Accepted (1bffad7, 2026-06-15) |
| ADR-0014 | reference_implementations is advisory, held out of the promotion / evidence gate (no gate-bleed) | Accepted (c5ac713, 2026-06-16) |
| ADR-0015 | Grounding + ingestion were sequenced first, before the feature additions (the trust foundation) | Accepted (580e236 → c5ac713, 2026-06-16) |
| ADR-0016 | Succinct over prose — state each rule once, at its point of enforcement (token efficiency) | Accepted (2026-06-16) |

---

## ADR-0001 — A portable skill library, not an app (the pivot)

**Status:** Accepted (1bffad7, 2026-06-15)

**Context.** The proven method here was **lifted out of a prior internal delivery tool** —
a bespoke application with hard architecture-review and approval gates. The business would
not support a custom app, so the *method* was preserved and the *plumbing* (the runtime,
the enforcement gates, the central service) was dropped. The value is the
provider-agnostic reasoning, not the machinery that used to host it. An app couples a
method to one runtime; a library of files runs anywhere a file can be read. This is the
root premise the rest of the architecture rests on — it is why the enforcement gates were
dropped (the one structural gate that remains is recorded in ADR-0002) and why portability
became a first-class property (ADR-0006). *This pivot had no dedicated record in the
day-old draft: its why lives in `RATIONALE.md` §1 and is implicit in the prior records'
context. First-classing it here gives the root decision an owner.*

**Decision.** The library is a **portable set of self-contained markdown skill files**
(`skills/**/SKILL.md`: steps + YAML frontmatter) an agent reads and runs inside *any* LLM
workflow — a
coding agent, a plain prompt, a CI step. It is **not an app and not a service**. The
method is preserved; the runtime, the enforcement gates, and the central service of its
precursor are deliberately dropped.

**Consequences.** The high-IP reasoning runs anywhere a file can be read, with no runtime
to host, no service to operate, and no vendor to bind to. The dropped enforcement plumbing
is what forces the safety to live in the *shape* of what an agent emits (ADR-0003) rather
than in a blocking mechanism, and what makes portability a load-bearing property (ADR-0006).
**What breaks if changed:** re-introducing a runtime or a central service re-couples the
method to one environment and re-opens the door to the hard gates the pivot exists to drop —
the whole gate-free, run-anywhere posture unwinds.

**Alternatives / Dissent.** Keeping (or rebuilding) the method as a gated application with
a central service — rejected: the business would not support a custom app, and an app binds
the reasoning to one runtime and one vendor. *No source records a counter-argument for
keeping the app beyond the business constraint; confirm with maintainers.*

**Evidence.** `RATIONALE.md` §1 ("Where this came from — the pivot": method lifted out of a
prior internal delivery tool; the runtime / enforcement gates / central service dropped);
`DESIGN.md` §9; scaffold commit `1bffad7`.

---

## ADR-0002 — Advisory, not gated: no enforcement gates; CODEOWNERS is the one structural gate on patterns/ and capabilities/

**Status:** Accepted (1bffad7, 2026-06-15)

**Context.** The method was preserved while the enforcement plumbing of its precursor was
dropped (ADR-0001): the business would not support hard architecture-review gates. The
library still needs *one* place where a human definitively ratifies a reusable asset with
its evidence and validity dates — but everywhere else the machine should catch the *shape*
and leave every *call* to a person.

**Decision.** Every GitHub Action is **advisory**: it comments and may fail a check to
prompt a human, but **never blocks a merge**. `CODEOWNERS` is the **only** structural gate —
a human architect's review is required to merge any change under `/patterns/**` or
`/capabilities/**`.

**Consequences.** A pattern or capability enters the shared library only when a human
reviews and merges its PR, carrying its validation, evidence, and validity dates. The
`CODEOWNERS` file itself records *why a pattern earns the one hard gate*: it is "a
load-bearing claim… the one artefact that can quietly do harm at scale" — its NFRs
propagate, its constraints replay during validation, its provenance legitimises a
fast-track. **What breaks if changed:** making Actions blocking reintroduces the heavyweight
gates the pivot exists to drop; removing the `CODEOWNERS` gate lets an agent-proposed
pattern enter the shared library unratified. **Honest limit:** "Advisory CI can let a
malformed pattern merge if a reviewer ignores a red check" — `CODEOWNERS` is the single
backstop, and the design openly **reserves the right to flip `validate-patterns` to
required for the `patterns/**` tree alone**. This is the one acknowledged escape hatch in
the no-gate stance.

**Alternatives / Dissent.** Required (blocking) CI checks — deliberately not used, except
the reserved `patterns/**` option above. A privileged disposing governance role — rejected.

**Evidence.** `.github/CODEOWNERS`; `README.md`; `DESIGN.md` §1, §9; `CONTRIBUTING.md`
("The rules that hold everywhere"); commit `1bffad7`.

---

## ADR-0003 — The TARGET RULE: four output kinds, never a verdict (the principled enabler of gate-free)

**Status:** Accepted (1bffad7, 2026-06-15)

**Context.** An agent operating in any LLM workflow can emit text that *reads* as
authority — a status, a colour, a score, a feasibility call, a judgment of a person. If an
advisory library lets that authority leak out, a cheap model's confidence, or a plain
mistake, flows downstream as if a human ruled it. The library carries no runtime to stop
this (ADR-0001), so the safety has to live in the *shape* of what an agent may emit.

**Decision.** Every agent output is exactly one of four kinds — `proposal` | `question` |
`menu` | `halt` — and **never** a status, verdict, colour, ranking, score, feasibility
call, disposition, or an assessment of a person. An agent targets the **MODEL** (keep a
cheap model on rails), the **RECORD** (structure for reuse), or the **BLIND SPOT**
(coverage / de-biasing) — never the **JUDGMENT**, which is the human's call.

**Consequences.** This is *the principled reason the library needs no enforcement gates*
(ADR-0002): because the output type forbids self-approval, the library can automate
aggressively without a blocking mechanism. The guarantee is checkable at author-time and
PR-time, on the type of the output. **What breaks if changed:** add any kind that can
self-approve (a verdict / score / RAG colour) and the entire gate-free rationale collapses —
an agent mistake would then flow into the design as authoritative fact, and the library
would *need* a blocking mechanism to stay safe.

**Alternatives / Dissent.** A fifth `recommendation` kind — rejected as "the most seductive
smuggler", a verdict in disguise; the legal move is an un-ranked `menu` plus cited proposal
facts. Enforcement / approval gates that block a downstream project until a check passes
(the precursor tool's model) — rejected as heavyweight.

**Evidence.** `skills/_shared/target-rule.md`;
`skills/_contract/target-rule-output-kinds/SKILL.md` ("Why an advisory library is safe
without a blocking mechanism"); commit `1bffad7`.

---

## ADR-0004 — Propose → ratify: a human merge is the only ratification

**Status:** Accepted (1bffad7, 2026-06-15)

**Context.** An agent does the heavy lifting, but a person must stay in control of the
project's direction. The question is where ratification lives, and whether it needs its own
machinery (a status field, an event store, a privileged role).

**Decision.** There is one and only one ratification act: a **human merging the PR**. The
agent opens the PR; it never merges its own work, writes a "ratified" status, or
auto-advances. The merge commit plus the PR thread **is** the durable, append-only audit
record — no separate event store.

**Consequences.** A person controls direction while the agent does the work, and mapping
ratify onto a GitHub merge adds *no extra machinery* — the commit log and PR timeline are
already the trail. **What breaks if changed:** a self-merging agent, an auto-applied
advance, or any persisted status that must flip before work proceeds reintroduces a blocking
gate and breaks the advisory-by-construction guarantee — the named anti-patterns "the
self-merging agent" and "the smuggled block". **Honest limit:** "PR-is-ratify is a forced
fit for in-session iteration" — intra-session work happens on the branch with no ceremony,
and "a human always disposes" is review culture, not code; a person can proceed past an
unread checkpoint and owns that.

**Alternatives / Dissent.** A separate governance-disposition machinery
(`pass` / `pass_with_conditions` / `send_back`) and a privileged disposing role — rejected
because it "turns reviewed back into a blocking checkbox". A separate event store — rejected;
the log is the trail.

**Evidence.** `skills/_shared/propose-ratify.md`;
`skills/_contract/propose-ratify-rhythm/SKILL.md`; `DESIGN.md` §2 invariant 2; commit
`1bffad7`.

---

## ADR-0005 — Grounding / no fabrication: an absent, unreadable, or empty required input HALTs

**Status:** Accepted (580e236, 2026-06-16)

**Context.** A richly agent-driven, gate-free library has one remaining way to fail
catastrophically: produce a *clean-looking proposal grounded in nothing*. Input presence,
however, is a deterministic, pre-model file-level fact — knowable before any model reasons.

**Decision.** A skill names its **required** inputs; an absent / unreadable / empty required
input becomes a typed `halt` that asks where the input is (offering the formats ingestion
reads) and stops — **never** an invented hypothetical, id, key, number, NFR, or acceptance
criterion. The presence check runs at **STEP 0, before any model**. "I read nothing" and "I
cannot read this" are deliberately *different* outputs.

**Consequences.** The one way to fail catastrophically is closed cheaply, because the check
is a deterministic file-level fact, not a model judgment. A `halt` is a question, never a
verdict: it carries only what is required, what is missing, and the readable formats. **What
breaks if changed:** a halt that smuggles a finding or feasibility verdict ("I halt because
this is infeasible") is the marked-WRONG counter-example — it breaks both this rule *and* the
TARGET RULE (ADR-0003). **Honest limit:** the lint checks only that a skill *cites* the stub
and *wires* a halt path; it "does not and cannot catch a model inventing an input mid-run",
which is runtime behaviour. The contract plus the halt exemplar are the real safeguard.

**Alternatives / Dissent.** Silently proceeding on partial input or back-filling a guess —
forbidden ("partial input is named, not patched"). Returning an *empty* result on an
unreadable source — forbidden, because silent-empty reads downstream as "the source had
nothing in it", a silent-proceed failure.

**Evidence.** `skills/_shared/grounding.md`;
`skills/_contract/grounding-no-absent-input/SKILL.md`; commit `580e236`.

---

## ADR-0006 — Deterministic base + a one-line model step; a model call is never fatal (portability)

**Status:** Accepted (1bffad7, 2026-06-15)

**Context.** The library's value is provider-agnostic reasoning that must run anywhere a
file can be read — a bare terminal with no API key, a CI runner, a locked-down box (the
portability the pivot bought, ADR-0001). If a skill depends on a live model call, it earns
nothing in those environments and binds the high-IP reasoning to one vendor.

**Decision.** Every skill carries a **deterministic, no-LLM base**
(checklist / regex / template / skeleton) plus a one-line model swap that only ever *deepens*
it. A failed, absent, or malformed model call is **never fatal** — the base stands. The model
is named only by a **tier hint** (`frontier` | `mid` | `light`) behind a one-line seam; no
model ids or vendor names appear anywhere.

**Consequences.** The skill is portable: the model is an enrichment, never a dependency, so
"light and advisory" is safe to drop into any environment, and deepening or swapping a model
is editing one word, not rewriting the skill. The harness binds a deterministic-stub backend
or any live backend in a one-line change. **What breaks if changed:** a hidden model
dependency (a `deterministic_fallback` field claiming a no-LLM path the body does not
implement) makes the field a false contract and breaks portability into no-key / CI / offline
environments; naming a concrete model or vendor breaks the "runs in any harness" property and
the one-word swap. **Honest limit:** the base "is allowed to be shallow" — the bar is only
that a reviewer would accept the no-model output "as a draft".

**Alternatives / Dissent.** A model-only skill whose first step is "ask the model" — an
anti-pattern ("if the call fails, the user gets nothing. Always have a floor"). Hard-coding a
provider / model id — the "vendor lock in the swap" anti-pattern. An orchestration framework —
rejected: "one interface, one stub, one capped fan-out".

**Evidence.** `skills/_shared/deterministic-fallback.md`;
`skills/_contract/parallel-agents/SKILL.md`; `DESIGN.md` §2 invariant 3, §8; commit `1bffad7`.

---

## ADR-0007 — Trace via fields, never in the key; projections recomputed not persisted; accept-high / derive-low safety net

**Status:** Accepted (1bffad7, 2026-06-15)

**Context.** Artefacts in this library are markdown files that get copied, diffed,
PR-reviewed, and grepped — and they must carry their parentage and relationships into *any*
file-reading workflow, with no database, id server, or schema to lean on. Two coupled
problems follow: how a relationship is expressed (a portable citation, not a foreign key),
and what to do with values *derived* from those relationships (a rollup, a RAG colour, a
maturity tally) that would rot if stored. And the same trace edge is what makes it safe for
agents to auto-derive everything beneath the few human-ratified commitments
(**accept-high / derive-low**).

**Decision.** Parentage and every relationship live in **fields** on the artefact
(`derives_from`, `fulfils_capability`, `fulfilled_by`, `supersedes` / `superseded_by`,
`contests`), **never inside the key**; `derives_from` is a **portable `req_key` citation**
(plain text, optionally a markdown link), not a foreign key. Rollups, RAG verdicts, release
notes, and pattern-maturity tallies are **recomputed on read or in an Action**, never stored
as a field that can rot (staleness is answered by `git diff` / `git blame`). Humans ratify
only the few genuine commitments (business outcomes, the solution shape, contested calls);
agents **derive and auto-apply** everything beneath, each derived item carrying a
`derives_from` citation back to its accepted upstream node.

**Consequences.** The citation survives being copied, diffed, reviewed, and grepped; a
foreign key does not survive leaving its database — so the edge stays portable. A
derived-on-read value is kept honest: it is not a stored verdict an agent asserted, which
reinforces the TARGET RULE (ADR-0003). **The trace edge is what makes accept-high /
derive-low SAFE:** a derived row is structurally a proposal threaded to an *already-accepted*
parent, so rejecting an upstream node *visibly orphans* its derived subtree (a reconcile step
surfaces the dangling citations) rather than silently cascade-deleting it — so the human
spends attention only on load-bearing commitments without losing the net. **What breaks if
changed:** switching to foreign keys removes the orphaning safety property and breaks
portability (the edge stops working with grep or a plain prompt); putting parentage *in* the
key makes keys unstable, so re-parenting renumbers the key and breaks every citation; storing
a RAG colour or score reintroduces a verdict (forbidden by the TARGET RULE) *and* a value that
can silently rot — which is why `portfolio-rollup.json` is gitignored; emitting a derived
(LOW) artefact without a `derives_from` link, or threading it to an outcome never accepted
("orphan-blind derivation"), removes the safety net. **Honest limit:** renaming / renumbering
a `req_key` "silently breaks every edge that cites it" — citation stability is an *unguarded*
assumption; nothing enforces referential integrity but the lint and human review.

**Alternatives / Dissent.** A foreign-key / database edge — "correct for a database",
rejected because this library is file-based. Persisting a RAG colour, score, or
acceptance-rate metric — forbidden ("a check optimised for throughput is worse than none").
Per-item human acceptance of every derived requirement — rejected as the fatigue failure the
model exists to prevent.

**Evidence.** `skills/_shared/req-key-conventions.md`; `skills/_shared/trace-edge.md`;
`DESIGN.md` §2 (invariants 5 + 7-area); `.gitignore` (`portfolio-rollup.json` is a
derived-on-read RAG projection); `skills/_contract/propose-ratify-rhythm/SKILL.md` (Step 2);
`skills/_contract/target-rule-output-kinds/SKILL.md` ("derive-from-accepted-upstream");
commit `1bffad7`.

---

## ADR-0008 — Anti-fatigue: delta-since-last-green, dismissal-memory, no throughput / per-person metric

**Status:** Accepted (1bffad7, 2026-06-15)

**Context.** A library that re-flags the same dismissed cue on every run trains its readers
to ignore it — review fatigue is how an advisory signal dies. And any throughput or
per-person number measures a person or team and reads as a verdict.

**Decision.** A re-run reviews only what *changed since last green*; an untouched item is
deferred, not re-surfaced. A dismissed cue (`dismissal-memory`) re-arms **only on changed
evidence** — re-confirming an unchanged finding never re-nags. No acceptance-rate,
throughput, velocity, or per-person metric is computed or stored anywhere.

**Consequences.** The human's attention stays on what is new, and a settled call stays
settled until the evidence under it moves (dismissal-memory is content-addressed). **What
breaks if changed:** re-surfacing a dismissed cue against unchanged evidence reintroduces the
fatigue the mechanism exists to prevent; adding an acceptance-rate or throughput metric
smuggles a score back in (it optimises a person / team and reads as a verdict) — "a check
optimised for throughput is worse than none".

**Alternatives / Dissent.** A throughput / per-person metric — rejected as a **smuggled
score**, a verdict wearing a number (forbidden by the TARGET RULE, ADR-0003).

**Evidence.** `skills/_shared/dismissal-memory.md` (quoted by
`reconcile-design-vs-requirements`, `enumerate-roadblocks`, `triage-backlog-and-defer`,
`red-team-and-dissent`, `advisory-governance-checklist`); `DESIGN.md` §2 invariant 7; commit
`1bffad7`.

---

## ADR-0009 — Looser named categories, numbers dropped, open (dynamically-discovered) scheme

**Status:** Accepted (5877839, 2026-06-15)

**Context.** A developer rarely runs the whole method end-to-end in one go and must find a
single skill *on its own*, by intent. A numbered scheme imposes a false fixed sequence the
library does not have — "a map, not a track". A category scheme hardcoded in a linter would
also re-couple adding a skill group to editing a validator — friction every time the method
grows; the scheme is meant to be open.

**Decision.** Skills live under looser *named* categories — `ingest`, `understand`,
`challenge`, `architect`, `panel`, `deliver`, `library`, `meta` — **not** a numbered scheme;
names describe purpose so an agent finds a skill by intent. The scheme is **open**:
first-level directories under `skills/` are **discovered dynamically**
(`lint_map_links.category_dirs()`, lines 106–116), so adding a skill group needs no linter
edit.

**Consequences.** An agent finds a skill by what it is for, the categories carry no implied
order, and new groups slot in without touching validators — `ingest` (commit `580e236`) and
`meta` (commit `c5ac713`) were both added this way. **What breaks if changed:** renaming or
re-numbering a category breaks every hardcoded part path in `skills/_scripts/bundles.yml` and
`concat_skills.py` (the concat Action's `--check` fails and committed bundles go stale), and
every cross-link in `MAP.md` / `GETTING-STARTED.md` / `README.md` / `ENTRYPOINT.md` — the
lint tolerates a rename (dirs are discovered dynamically), so the break is in human
navigation and bundle paths, not lint legality. A new top-level dir that is *machinery* (not
a category) must carry the underscore prefix or discovery treats it as a runnable category.

**Alternatives / Dissent.** A numbered category scheme — rejected because numbers imposed a
false fixed sequence the library rejects ("a map, not a track"); the restructure is recorded
in the commit message "Looser categories (numbers dropped)". A fixed category enum in the
linter — rejected for the friction it would add; *no source records a counter-argument for a
fixed enum beyond that friction — confirm with maintainers.*

**Evidence.** `MAP.md` (View 2); `skills/_scripts/bundles.yml`; `concat_skills.py`;
`lint_map_links.py` `category_dirs()` (lines 106–116, dirs discovered dynamically so adding a
group needs no linter edit); commits `5877839` ("Looser categories (numbers dropped)"),
`580e236` (ingest added), `c5ac713` (meta added).

---

## ADR-0010 — Agent-first voice + de-narration: instructions read by agents, standalone and token-lean

**Status:** Accepted (5877839, 2026-06-15)

**Context.** These files are read and run by **agents**, not narrated for a human audience.
Narrative *about other systems* drifts a reading agent off task, and prose that assumes
surrounding context breaks when a single skill is copied out alone. The library deliberately
strips lineage to other entities and writes in a de-narrated, present-tense, token-lean
voice. *This had no dedicated record in the day-old draft: it is asserted in `RATIONALE.md`
§1 and §4 and enforced by lint, not captured as its own ADR. First-classing it gives the
voice an owner; flag to maintainers that no prior record carried its full why.*

**Decision.** Skills and library prose are written **agent-first**: de-narrated (lineage to
other entities deliberately stripped), present-tense, standalone (a skill carries its own
rules so it survives being copied out alone), and token-lean. No narrative about other
systems and no story-framing.

**Consequences.** A reading agent stays on task and a skill copied out alone still makes
sense. **What breaks if changed:** re-narrating drifts a reading agent off task and re-couples
a skill to surrounding context it may not have. The recurring lesson is that a **mass
de-narration must own *every* file class** — the §4 near-miss caught "lineage leaks left in
pattern BODIES and the generated bundles after a mass de-narration" because no agent owned
that file class; a mass change must enumerate every file class it touches, including
`generated/` artefacts.

**Alternatives / Dissent.** Keeping human-narrative framing or lineage to prior systems —
rejected: narrative about other systems drifts a reading agent off task. *The de-narration is
asserted and lint-enforced rather than argued in a prior record; confirm with maintainers for
any why beyond "narrative drifts a reading agent off task".*

**Evidence.** `RATIONALE.md` §1 ("Lineage to other entities was deliberately stripped at
de-narration because narrative about other systems drifts a reading agent off task");
`RATIONALE.md` §4 (the de-narration near-miss: a mass change must own every file class,
including generated bundles); commit `5877839` ("Looser categories (numbers dropped)" /
de-narration pass).

---

## ADR-0011 — One canonical req-key scheme + full migration (records the panel-vs-maintainer dissent)

**Status:** Accepted (1d55b80, 2026-06-16) — maintainer overrode the panel's lean recommendation

**Context.** Six incompatible key schemes were live across the skills (`BO-/TR-`, `F-/NFR-`,
`C-/O-/R-/P-/D-`, `OUT-/REQ-`, bare integers, `O-/R-`). The divergence "would have broken
provenance, the absent-input halt precondition, and re-ingest de-dup": ingest can't stamp
provenance to a stable key, a "HALT if no `O-*` keys" precondition fires spuriously on a valid
`BO-*` project, and re-ingest de-dup keys off a number that renumbers across schemes.

**Decision.** One canonical scheme — **exactly one prefix per kind**: `BO-<n>` (business
outcome), `REQ-<n>` (requirement, functional *or* non-functional — F/NF is `classify`
metadata, never in the key), `CAP-<SLUG>`, `PAT-<SLUG>`, `DEC-<n>`, plus the optional child
key `AC-<REQ>.<n>`. The **one normalisation rule**: read the key scheme **from the target
file, never assume one** (this kills a spurious halt — never argue a project out of its own
valid keys); when a source uses another prefix, normalise on write **and preserve the
source's own identifier verbatim as `source_ref`**, so a re-read de-dups on `source_ref`,
not on a minted key that renumbers across schemes. (This reinforces trace-via-fields,
ADR-0007.)

**Consequences.** Provenance stamps to a stable key, the halt precondition stops firing
spuriously, and re-ingest de-dup is stable. The RAID register's `R-` / `A-` / `T-` ids are a
**separate namespace, deliberately untouched** (they name register rows, "a reading aid, not
a key"). **What breaks if changed:** reverting to per-stage prefixes re-opens the three
failures; renaming any prefix breaks every `derives_from` / `fulfils_capability` /
`fulfilled_by` field that cites a key; putting parentage back *in* the key makes keys
unstable.

**Alternatives / Dissent.** **Real, recorded dissent.** A design panel **recommended the
leaner route** — "bless-the-existing-set + one normalisation rule", to avoid touching six
skills' worked examples. The maintainer **overrode** this at build time and chose a single
canonical scheme + full migration (commit `1d55b80`) for long-term coherence, migrating every
skill, worked example, reference, and the trace-edge block. Record both: the lean route was
the panel's recommendation; the clean single scheme was the maintainer's call. *Unrecorded:
why uppercase prefixes, why integer counters for `BO-/REQ-/DEC-` but slugs for `CAP-/PAT-`,
and why `AC-<REQ>.<n>` is the one place hierarchy is allowed in a key (in tension with
"parentage never in the key") — confirm with maintainers.*

**Evidence.** `skills/_shared/req-key-conventions.md` (read the scheme from the target file;
preserve `source_ref` verbatim); commit `1d55b80`.

---

## ADR-0012 — Capabilities are a first-class entity: the requirements-to-components bridge

**Status:** Accepted (5877839, 2026-06-15)

**Context.** The pattern library answered "what shape did we build", but nothing answered
"what *need* does a system have, and is there a proven shape for it yet". A need outlives the
component that fulfils it, and a reader who can name a need in plain language but not the
technology had no entry point — and `recommend-component-patterns` STEP 0 *assumes* a
`fulfils_capability` tag that no skill emitted.

**Decision.** Capabilities are **first-class** — a `.md` tree PR-reviewed like patterns (and
so under the one `CODEOWNERS` gate, ADR-0002), sitting **between** requirements and patterns
as the named middle term. The chain is: outcome ← requirement (`fulfils_capability`) ←
capability (`fulfilled_by`) ← pattern.

**Consequences.** A reader who can name a need but not the technology has a technology-free,
rename-surviving anchor, and `recommend-component-patterns` STEP 0 has the
`fulfils_capability` tag it assumes. **What breaks if changed:** removing the layer re-opens
the gap `derive-capabilities` closed — `recommend-component-patterns` STEP 0 assumes the tag
exists but no skill emits it, and the need is no longer a technology-free, rename-surviving
anchor.

**Alternatives / Dissent.** Leaving the requirements→patterns gap unbridged — rejected
because nothing answered the "what need" question and the need outlives its component.

**Evidence.** `capabilities/README.md`; `derive-capabilities/SKILL.md`;
`recommend-component-patterns/SKILL.md` (STEP 0 assumes the `fulfils_capability` tag); commit
`5877839`.

---

## ADR-0013 — Pattern lifecycle is human-owned: evidence-gated promotion, approval_status agent-writes-candidate-only, maturity computed not authored

**Status:** Accepted (1bffad7, 2026-06-15)

**Context.** The library's value is fast-tracking reuse of shapes with a *real track record*,
and the bless step is the one structural human gate (ADR-0002). Three failures threaten it: a
pattern minted from an imagined shape promoted with no proof it was built; an agent advancing
the trust status so an unreviewed shape presents as blessed; and a pattern self-declaring a
track record it does not have. All three are the same principle — promotion is a human act
backed by evidence, not a machine assertion.

**Decision.** The pattern lifecycle is **human-owned**. (1) `evidence[]` (proof it was BUILT)
is **required** once `approval_status` is `provisional` or `approved` — "no evidence, no
promotion". (2) `approval_status` is a **closed, human-only enum**
(`candidate → provisional → approved → deprecated`); an agent **only ever writes
`candidate`** — "writing `approved` is the single most damaging thing this skill could do".
(3) `maturity` and `adoption_count` are **forbidden as authored input** (`{"not":{}}`) and
**computed** from `adoptions/ledger.jsonl` — maturity is arithmetic over the ledger, and the
ledger even counts teams that *evaluated and chose otherwise* (non-adoption is signal).

**Consequences.** A `provisional` / `approved` status reliably means "proven", the bless step
stays a human act, and a pattern cannot self-declare a track record (adopted-by-zero stays
visible). **What breaks if changed:** dropping the evidence gate lets an unbuilt shape
masquerade as blessed; letting an agent set `provisional` / `approved` bypasses the one human
gate; making `maturity` authorable lets a pattern self-declare "battle-tested" with no ledger
behind it. The single shared ledger reader keeps the never-delete invariant and the maturity
tally consistent; bypassing it splits the two consumers' view of an adoption.

**Alternatives / Dissent.** Allowing promotion without evidence — rejected; the gate protects
credibility against a pattern minted from an imagined shape ("leave it honestly empty", never
fabricate a link). Letting an agent advance the status — rejected; the status encodes human
trust, not a machine fact. Authoring `maturity` / `adoption_count` by hand — rejected; a
self-declared track record with no ledger behind it is a lie.

**Evidence.** `patterns/_schema/pattern.frontmatter.schema.json` (`allOf` conditional; closed
human-only enum; `{"not":{}}` on `maturity` / `adoption_count`); `lint_pattern_frontmatter.py`
(`check_conditional_rules`); `patterns/README.md`;
`author-component-pattern/SKILL.md` ("Writing `approved` is the single most damaging thing
this skill could do"); `adoptions/ledger.jsonl` + `iter_ledger_records` (maturity is
arithmetic over the ledger; non-adoption is signal); commit `1bffad7`.

---

## ADR-0014 — reference_implementations is advisory, held out of the promotion / evidence gate (no gate-bleed)

**Status:** Accepted (c5ac713, 2026-06-16)

**Context.** A reference implementation answers a *different* question from `evidence[]`:
evidence = "was this BUILT?" (gates promotion, ADR-0013); a reference implementation = "what
do I start FROM?" (a forward "start here" pointer). The sharpest hazard is **gate-bleed** —
wiring a working IaC repo into promotion so a pattern is blessed on a forward link with no
proof it was built.

**Decision.** `reference_implementations[]` is additive-**optional** and held strictly **out
of the promotion gate** — advisory only. A reference impl that *is* a real build must ALSO be
listed under `evidence[]` (`kind:repo`), promoting "through the existing door, zero new gate
logic".

**Consequences.** A pattern can carry "start here" pointers without those pointers ever
promoting it; a real build still promotes through the one existing evidence door. **What
breaks if changed:** moving the field into `check_conditional_rules` / `PROMOTED_STATUSES`
lets a pattern be promoted on a forward link with no proof it was built — the gate-bleed
failure. The advisory-only contract is asserted in schema + linter + skill so a future
contributor sees it in all three.

**Alternatives / Dissent.** Wiring a reference implementation into the promotion gate —
rejected as gate-bleed. The design doc proposed a **six-value** `kind` enum
(`iac|app|notebook|scaffold|module|pipeline`) plus optional `repo_path` / `scaffold_cmd` /
`last_verified`; the shipped schema **narrowed to four** (`iac|app|notebook|scaffold`) and
dropped the extra fields. *Why the narrowing is not recorded in any commit; confirm with
maintainers.*

**Evidence.** `patterns/_schema/pattern.frontmatter.schema.json`; `lint_pattern_frontmatter.py`
(kept out of `check_conditional_rules` / `PROMOTED_STATUSES`); commit `c5ac713`.

---

## ADR-0015 — Grounding + ingestion were sequenced first, before the feature additions (the trust foundation)

**Status:** Accepted (580e236 → c5ac713, 2026-06-16)

**Context.** When five follow-ups were proposed (capability-derivation, feature-intake,
navigator, ingestion, the pattern reference-implementation field), the order they shipped in
was itself a decision. A feature built on top of a contract that does not yet forbid
ungrounded output inherits that gap; a feature built after it stands on a contract that
already forbids it.

**Decision.** The maintainer **sequenced the no-fabrication grounding + ingestion FIRST** as
the **trust foundation**, before the others — so the rest stand on a contract that already
forbids ungrounded output. The grounding contract carries the library's **first working halt
exemplar**: `halt` is the fourth output kind (legal in the TARGET RULE, ADR-0003, but until
then with zero exemplar), applied **additively, not as a gate** — it stops this run and asks;
the human supplies the input and re-runs; nothing downstream is blocked.

**Consequences.** Every later feature (capabilities, ingestion mechanics, the
reference-implementation field) was authored against a contract that already forbids
ungrounded output, and every halt-first skill has one reference shape to copy so halts stay
uniform and verdict-free. **What breaks if changed:** building a feature before the grounding
contract would let it inherit the silent-proceed gap; treating a halt as a downstream-blocking
gate, or letting it carry a finding / feasibility verdict, breaks both grounding (ADR-0005)
and the TARGET RULE. *The ~11 ingestion-mechanics decisions (split-read-from-model-map,
skip-never-raise, HALT-not-empty, `source_ref` de-dup, pinned-snapshot, export-only,
locator-backed AC, delegated vocab, byte-untouched vault, identity-binding, reingest-delta)
are the bodies of work that were sequenced first, but they are field-level / contract
mechanics that now live at the schema descriptions, the `skills/ingest/_scripts/` README, and
`CONTRIBUTING.md` — the lint and the readers are their guard. This record owns the
**sequencing** decision, not each mechanic.*

**Alternatives / Dissent.** A halt that carries a finding or feasibility verdict — the
marked-WRONG counter-example (invents `REQ-1/2/3`, an uptime NFR, a "4–8 days" estimate, and
"looks infeasible"): "a halt that contains a finding is not a halt; it is a verdict with an
apology attached" — explicitly rejected. Building the feature additions before the trust
foundation — rejected; they were deliberately sequenced after it.

**Evidence.** Commit order is the record: the grounding contract + ingest layer landed in
`580e236`, and the feature additions (capability-derivation, feature-intake, navigator,
reference-implementations) followed in `c5ac713` — so the later work stands on a contract
that already forbids ungrounded output. `skills/_contract/grounding-no-absent-input/SKILL.md`
(the library's first working halt exemplar; halt is the fourth output kind applied additively,
not as a gate).

## ADR-0016 — Succinct over prose: state each rule once, at its point of enforcement

**Status:** Accepted (2026-06-16)

**Context.** A skill is loaded **whole, every run, to do one task** — every word is paid
per-invocation. A density audit (2026-06-16) found the 47 skills average ~2,900 words and
27 carry *structural* bloat (not one-off): Notes/anti-patterns that negate each numbered
STEP; the keystone rule restated 4–5× (frontmatter + Purpose + STEP + prompt + Notes);
Purpose-as-essay; the grounding/trace stub re-narrated right after it is quoted; a closed
vocabulary restated 3–4×; a skill re-embedding its own reference's full content; two worked
examples where one suffices. The top targets alone hold ~10k words of removable duplication.
This **sharpens** the de-narration / agent-first decision (**ADR-0010**): that decision moved
the *why* out of the files (into the ADRs + RATIONALE); this one governs what is *left* in a
file once the why leaves.

**Decision.** **State each rule once, at its point of enforcement; cite it elsewhere; never
re-narrate the frontmatter or a byte-stable quoted stub.** CUT: step-negating anti-patterns,
Purpose essays, pre-stub connective paragraphs, post-stub HALT re-narration, keystone
restatements, the duplicated multi-agent block, second worked examples, a skill that embeds
its own reference. KEEP (load-bearing, never cut): frontmatter; the byte-stable quoted stubs
*verbatim*; the literal HALT; the numbered STEPS; the embedded model **prompt verbatim**; the
OUTPUT template; controlled vocab / closed enums; the deterministic base; **one** tight
worked example. Density is fine; **restatement** is the target. (Per-class cut/keep test:
`skills/_scripts/lint_skill_density.py` header + the audit.)

**Consequences.** Lower per-invocation token cost on the hottest path (skills) and a higher
signal-to-noise for the reading agent. The advisory guard `lint_skill_density.py` flags a
skill body over **~2,500 words** (excluding frontmatter + byte-stable stubs) for a tightening
look — **warn, never block**. **What breaks if ignored:** skills drift back to ~4k-word
essays, every invocation pays for prose the frontmatter / ADRs already own, and the reading
agent's attention dilutes.

**Alternatives / Dissent.** A **hard word cap** — rejected: some skills are *justifiably*
dense (closed taxonomies, embedded prompts, multi-template outputs), so a cap punishes
density, not restatement. **Trimming the byte-stable quoted stubs** to save words — rejected:
they are mandatory (drift-guarded, quoted verbatim), and trimming one forces a re-quote
everywhere.

**Evidence.** The density audit (2026-06-16; 78 files, 27 bloated); sharpens ADR-0010;
`skills/_scripts/lint_skill_density.py` (the advisory guard); the per-class cut/keep standard.
