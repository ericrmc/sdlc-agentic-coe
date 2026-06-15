# ADR — architectural decision log

This is the library's **canonical, append-only, status-tracked record of architectural
decisions**. Each record `ADR-NNNN` is immutable and self-contained: it states one
decision, the forces that produced it, what it gives and what breaks if changed, the
road-not-taken (including the real panel-vs-maintainer disagreements), and the in-repo
evidence for the why. A reader can open any single record and understand it without
reading the others.

This log is the **one owner** for each decision's why. `RATIONALE.md` narrates how the
decisions hang together and **cites** these records rather than restating them — the
library forbids two sources of truth for the same fact. To add a decision, append the
next number; nothing earlier is edited. To reverse a decision, append a **new** record
and mark the old one `Superseded by ADR-NNNN` — a record is never rewritten in place,
so the history of what was decided (and later undone) stays legible.

Every why here is evidenced in an in-repo file or a commit. Where a rationale was not
recorded anywhere, the record says so ("rationale not recorded — confirm with
maintainers") rather than inventing one.

## Status legend

- **Accepted** `<commit/date>` — in force; the decision holds.
- **Superseded by ADR-NNNN** — reversed or replaced; read the named successor for the
  current decision. This record stays for history.
- **Deprecated** — withdrawn with no direct successor.

## Index

| ID | Title | Status |
|---|---|---|
| ADR-0001 | The TARGET RULE — four output kinds (proposal \| question \| menu \| halt), never a verdict | Accepted (scaffolded 1bffad7, 2026-06-15) |
| ADR-0002 | Propose → ratify — the human-merged PR is the single ratification act and audit record | Accepted (scaffolded 1bffad7, 2026-06-15) |
| ADR-0003 | Advisory, not gated — Actions only comment/fail-a-check; CODEOWNERS is the one structural gate | Accepted (scaffolded 1bffad7, 2026-06-15) |
| ADR-0004 | Grounding / no fabrication — an absent, unreadable, or empty required input HALTs at STEP 0 | Accepted (580e236, 2026-06-16) |
| ADR-0005 | Deterministic base + one-line model step (tier hint behind a seam) — the model only deepens | Accepted (scaffolded 1bffad7, 2026-06-15) |
| ADR-0006 | Trace via fields, never in the key; relationships are portable req_key citations | Accepted (scaffolded 1bffad7, 2026-06-15) |
| ADR-0007 | Projections, not persistence — rollups, RAG verdicts, tallies are recomputed on read | Accepted (scaffolded 1bffad7, 2026-06-15) |
| ADR-0008 | Anti-fatigue — review only the delta-since-last-green; no throughput/per-person metric | Accepted (scaffolded 1bffad7, 2026-06-15) |
| ADR-0009 | Looser named skill categories, not a numbered scheme | Accepted (5877839, 2026-06-15) |
| ADR-0010 | Underscore-prefixed machinery folders separated from the runnable product | Accepted (scaffolded 1bffad7, 2026-06-15) |
| ADR-0011 | capabilities/ and patterns/ are top-level trees so the CODEOWNERS gate is path-addressable | Accepted (capabilities first-classed 5877839, 2026-06-15) |
| ADR-0012 | generated/ bundles are committed; portfolio-rollup.json is gitignored | Accepted (scaffolded 1bffad7, 2026-06-15) |
| ADR-0013 | Two navigation altitudes — a thin root ENTRYPOINT.md and the exhaustive skills/MAP.md | Accepted (scaffolded 1bffad7, 2026-06-15) |
| ADR-0014 | Skill category scheme is open — first-level dirs discovered dynamically | Accepted (discovery verified; ingest added 580e236, meta added c5ac713) |
| ADR-0015 | pattern_key (PAT-<UPPER-KEBAB>) is the stable cite-able id, decoupled from the filename | Accepted (scaffolded 1bffad7, 2026-06-15) |
| ADR-0016 | evidence[] is required once approval_status is provisional or approved | Accepted (scaffolded 1bffad7, 2026-06-15) |
| ADR-0017 | approval_status is a closed, human-only enum; an agent only ever writes candidate | Accepted (scaffolded 1bffad7, 2026-06-15) |
| ADR-0018 | maturity and adoption_count are forbidden as authored input — computed from the ledger | Accepted (scaffolded 1bffad7, 2026-06-15) |
| ADR-0019 | superseded_by is required when deprecated; staleness warns, never blocks | Accepted (scaffolded 1bffad7, 2026-06-15) |
| ADR-0020 | attached_nfrs[] each require kind + statement + acceptance_criterion | Accepted (scaffolded 1bffad7, 2026-06-15) |
| ADR-0021 | reference_implementations[] is additive-optional and held out of the promotion gate | Accepted (c5ac713, 2026-06-16) |
| ADR-0022 | The pattern validator is deterministic, dependency-light, advisory about content | Accepted (scaffolded 1bffad7, 2026-06-15) |
| ADR-0023 | Capabilities are first-class — the named middle term between requirements and patterns | Accepted (5877839, 2026-06-15) |
| ADR-0024 | capability_key is CAP-<UPPER-KEBAB>, a distinct namespace; parentage in fields | Accepted (5877839, 2026-06-15; aligned by canonical-key migration 1d55b80) |
| ADR-0025 | Bidirectional capability/pattern edges with link discipline, all by key-citation | Accepted (5877839, 2026-06-15) |
| ADR-0026 | The alias-searchable INDEX.md is the need-first entry point — ≥2 lay-synonym aliases | Accepted (5877839, 2026-06-15) |
| ADR-0027 | Proven-vs-candidate lives in fulfilled_by[].confidence | Accepted (5877839, 2026-06-15) |
| ADR-0028 | No agent sets confidence:proven or advances capability approval_status | Accepted (5877839, 2026-06-15) |
| ADR-0029 | Capability governance_nfrs draw kind from the same closed 11-kind NFR vocabulary | Accepted (5877839, 2026-06-15) |
| ADR-0030 | derive-capabilities emits two outputs — MATCHED proposals and PROPOSED-NEW menu | Accepted (5877839, 2026-06-15) |
| ADR-0031 | The eight solution-architecture section keys are a frozen, closed, ordered set | Accepted (scaffolded 1bffad7, 2026-06-15) |
| ADR-0032 | Accept-high / derive-low — humans ratify commitments; agents derive everything beneath | Accepted (scaffolded 1bffad7, 2026-06-15) |
| ADR-0033 | One canonical req-key scheme — exactly one prefix per kind | Accepted (1d55b80, 2026-06-16) — maintainer overrode the panel's lean recommendation |
| ADR-0034 | halt is the fourth output kind with the library's first working halt exemplar | Accepted (580e236, 2026-06-16) |
| ADR-0035 | Split each ingest skill into a deterministic no-model read and a separate model map | Accepted (580e236, 2026-06-16) |
| ADR-0036 | Ingest readers skip-never-raise — a content problem returns status="skipped" + reason | Accepted (580e236, 2026-06-16) |
| ADR-0037 | HALT-not-empty — an unreadable OR readable-but-empty source HALTs | Accepted (580e236, 2026-06-16) |
| ADR-0038 | Preserve the source's own id verbatim as source_ref; de-dup/diff on source_ref | Accepted (580e236, 2026-06-16) |
| ADR-0039 | GitHub Project ingest requires a pinned, timestamped snapshot, never a live board read | Accepted (580e236, 2026-06-16) |
| ADR-0040 | SharePoint is export-only — never live-fetch; HALT for a local export | Accepted (580e236, 2026-06-16) |
| ADR-0041 | Lift an acceptance criterion only when a source locator backs it; never synthesise it | Accepted (580e236, 2026-06-16) |
| ADR-0042 | Delegate controlled-vocab metadata to classify-requirements; never inline its enums | Accepted (580e236, 2026-06-16) |
| ADR-0043 | stage-and-fingerprint vaults the bytes byte-untouched as the source of record | Accepted (580e236, 2026-06-16) |
| ADR-0044 | Identity binding is proposed via deterministic signals, model only a tie-breaker | Accepted (580e236, 2026-06-16) |
| ADR-0045 | reingest-delta surfaces only the delta — never silently overwrites or auto-deletes | Accepted (580e236, 2026-06-16) |
| ADR-0046 | check-shared-stub-drift guards in-repo quoted _shared copies (quote-not-import) | Accepted (scaffolded 1bffad7, 2026-06-15) |
| ADR-0047 | Multi-agent fan-out is an advisory option capped at ≤4 concurrent; no framework | Accepted (scaffolded 1bffad7, 2026-06-15) |

---

## ADR-0001 — The TARGET RULE: four output kinds (proposal | question | menu | halt), never a verdict

**Status:** Accepted (scaffolded 1bffad7, 2026-06-15)

**Context.** An agent operating in any LLM workflow can emit text that *reads* as
authority — a status, a colour, a score, a feasibility call, a judgment of a person.
If an advisory library lets that authority leak out, a cheap model's confidence, or a
plain mistake, flows downstream as if a human ruled it. The library carries no runtime
to stop this, so the safety has to live in the *shape* of what an agent may emit.

**Decision.** Every agent output is exactly one of four kinds — `proposal` |
`question` | `menu` | `halt` — and **never** a status, verdict, colour, ranking, score,
feasibility call, disposition, or an assessment of a person. An agent targets the
**MODEL** (keep a cheap model on rails), the **RECORD** (structure for reuse), or the
**BLIND SPOT** (coverage / de-biasing) — never the **JUDGMENT**, which is the human's
call.

**Consequences.** This is *the principled reason the library needs no enforcement
gates*: because the output type forbids self-approval, the library can automate
aggressively without a blocking mechanism. The guarantee is checkable at author-time
and PR-time, on the type of the output. **What breaks if changed:** add any kind that
can self-approve (a verdict / score / RAG colour) and the entire gate-free rationale
collapses — an agent mistake would then flow into the design as authoritative fact, and
the library would *need* a blocking mechanism to stay safe.

**Alternatives / Dissent.** Enforcement / approval gates that block a downstream project
until a check passes — rejected as heavyweight. A fifth `recommendation` kind — rejected
as "the most seductive smuggler", a verdict in disguise; the legal move is an un-ranked
`menu` plus cited proposal facts.

**Evidence.** `skills/_shared/target-rule.md`;
`skills/_contract/target-rule-output-kinds/SKILL.md` ("Why an advisory library is safe
without a blocking mechanism"); commit `1bffad7`.

---

## ADR-0002 — Propose → ratify: the human-merged PR is the single ratification act and audit record

**Status:** Accepted (scaffolded 1bffad7, 2026-06-15)

**Context.** An agent does the heavy lifting, but a person must stay in control of the
project's direction. The question is where ratification lives, and whether it needs its
own machinery (a status field, an event store, a privileged role).

**Decision.** There is one and only one ratification act: a **human merging the PR**.
The agent opens the PR; it never merges its own work, writes a "ratified" status, or
auto-advances. The merge commit plus the PR thread **is** the durable, append-only audit
record — no separate event store.

**Consequences.** A person controls direction while the agent does the work, and mapping
ratify onto a GitHub merge adds *no extra machinery* — the commit log and PR timeline are
already the trail. **What breaks if changed:** a self-merging agent, an auto-applied
advance, or any persisted status that must flip before work proceeds reintroduces a
blocking gate and breaks the advisory-by-construction guarantee — the named anti-patterns
"the self-merging agent" and "the smuggled block". **Honest limit:** "PR-is-ratify is a
forced fit for in-session iteration" — intra-session work happens on the branch with no
ceremony, and "a human always disposes" is review culture, not code; a person can proceed
past an unread checkpoint and owns that.

**Alternatives / Dissent.** A separate governance-disposition machinery
(`pass` / `pass_with_conditions` / `send_back`) and a privileged disposing role —
rejected because it "turns reviewed back into a blocking checkbox". A separate event
store — rejected; the log is the trail.

**Evidence.** `skills/_shared/propose-ratify.md`;
`skills/_contract/propose-ratify-rhythm/SKILL.md`; `DESIGN.md` §2 invariant 2;
commit `1bffad7`.

---

## ADR-0003 — Advisory, not gated: Actions only comment / fail-a-check; CODEOWNERS is the one structural human gate

**Status:** Accepted (scaffolded 1bffad7, 2026-06-15)

**Context.** The method here was preserved while the enforcement plumbing of its
precursor was dropped: the business would not support hard architecture-review gates.
The library still needs *one* place where a human definitively ratifies a reusable asset
with its evidence and validity dates — but everywhere else the machine should catch the
*shape* and leave every *call* to a person.

**Decision.** Every GitHub Action is advisory: it comments and may fail a check to prompt
a human, but **never blocks a merge**. `CODEOWNERS` is the **only** structural gate — a
human architect's review is required to merge any change under `/patterns/**` or
`/capabilities/**`.

**Consequences.** A pattern or capability enters the shared library only when a human
reviews and merges its PR. The `CODEOWNERS` file records *why a pattern earns the one hard
gate*: it is "a load-bearing claim… the one artefact that can quietly do harm at scale" —
its NFRs propagate, its constraints replay during validation, its provenance legitimises a
fast-track. **What breaks if changed:** making Actions blocking reintroduces the
heavyweight gates the library was created to drop; removing the `CODEOWNERS` gate lets an
agent-proposed pattern enter the shared library unratified. **Honest limit:** "Advisory CI
can let a malformed pattern merge if a reviewer ignores a red check" — `CODEOWNERS` is the
single backstop, and the design openly reserves the right to flip `validate-patterns` to
required for the `patterns/**` tree alone. This is the one acknowledged escape hatch in the
no-gate stance.

**Alternatives / Dissent.** Required (blocking) CI checks — deliberately not used, except
the reserved option above. A privileged disposing governance role — rejected.

**Evidence.** `.github/CODEOWNERS`; `README.md`; `DESIGN.md` §1, §9; `CONTRIBUTING.md`
("The rules that hold everywhere"); commit `1bffad7`.

---

## ADR-0004 — Grounding / no fabrication: an absent, unreadable, or empty required input HALTs (computed at STEP 0)

**Status:** Accepted (580e236, 2026-06-16)

**Context.** A richly agent-driven, gate-free library has one remaining way to fail
catastrophically: produce a *clean-looking proposal grounded in nothing*. Input presence,
however, is a deterministic, pre-model file-level fact — knowable before any model reasons.

**Decision.** A skill names its **required** inputs; an absent / unreadable / empty
required input becomes a typed `halt` that asks where the input is (offering the formats
ingestion reads) and stops — **never** an invented hypothetical, id, key, number, NFR, or
acceptance criterion. The presence check runs at STEP 0, before any model. "I read nothing"
and "I cannot read this" are deliberately *different* outputs.

**Consequences.** The one way to fail catastrophically is closed cheaply, because the check
is a deterministic file-level fact, not a model judgment. A `halt` is a question, never a
verdict: it carries only what is required, what is missing, and the readable formats.
**What breaks if changed:** a halt that smuggles a finding or feasibility verdict ("I halt
because this is infeasible") is the marked-WRONG counter-example — it breaks both this rule
*and* the TARGET RULE. **Honest limit:** the lint checks only that a skill *cites* the stub
and *wires* a halt path; it "does not and cannot catch a model inventing an input mid-run",
which is runtime behaviour. The contract plus the halt exemplar are the real safeguard.

**Alternatives / Dissent.** Silently proceeding on partial input or back-filling a guess —
forbidden ("partial input is named, not patched"). Returning an *empty* result on an
unreadable source — forbidden, because silent-empty reads downstream as "the source had
nothing in it", a silent-proceed failure.

**Evidence.** `skills/_shared/grounding.md`;
`skills/_contract/grounding-no-absent-input/SKILL.md`; commit `580e236`.

---

## ADR-0005 — Deterministic base + a one-line model step (tier hint behind a seam): the model only deepens, never fatal

**Status:** Accepted (scaffolded 1bffad7, 2026-06-15)

**Context.** The library's value is provider-agnostic reasoning that must run anywhere a
file can be read — a bare terminal with no API key, a CI runner, a locked-down box. If a
skill depends on a live model call, it earns nothing in those environments and binds the
high-IP reasoning to one vendor.

**Decision.** Every skill carries a **deterministic, no-LLM base**
(checklist / regex / template / skeleton) plus a one-line model swap that only ever
*deepens* it. A failed, absent, or malformed model call is **never fatal** — the base
stands. The model is named only by a **tier hint** (`frontier` | `mid` | `light`) behind a
one-line seam; no model ids or vendor names appear anywhere.

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

## ADR-0006 — Trace via fields, never in the key; relationships are portable req_key citations, not foreign keys

**Status:** Accepted (scaffolded 1bffad7, 2026-06-15)

**Context.** Artefacts in this library are markdown files that get copied, diffed,
PR-reviewed, and grepped — and they must carry their parentage and relationships into *any*
file-reading workflow, with no database, id server, or schema to lean on.

**Decision.** Parentage and every relationship live in **fields** on the artefact
(`derives_from`, `fulfils_capability`, `fulfilled_by`, `supersedes` / `superseded_by`,
`contests`), never inside the key. `derives_from` is a **portable `req_key` citation**
(plain text, optionally a markdown link), not a foreign key.

**Consequences.** The citation survives being copied, diffed, reviewed, and grepped; a
foreign key does not survive leaving its database — so the edge stays portable into any
file-reading workflow. It is also what makes accept-high / derive-low safe: a derived row is
structurally a proposal threaded to an accepted parent, so rejecting an upstream node
*visibly orphans* its derived subtree rather than silently cascade-deleting it. **What breaks
if changed:** switching to foreign keys removes the orphaning safety property and breaks
portability (the edge stops working with grep or a plain prompt); putting parentage *in* the
key makes keys unstable, so re-parenting renumbers the key and breaks every citation.
**Honest limit:** renaming / renumbering a `req_key` "silently breaks every edge that cites
it" — citation stability is an *unguarded* assumption; nothing enforces referential integrity
but the lint and human review.

**Alternatives / Dissent.** A foreign-key / database edge — "correct for a database",
rejected because this library is file-based.

**Evidence.** `skills/_shared/req-key-conventions.md`; `skills/_shared/trace-edge.md`;
`DESIGN.md` §2; commit `1bffad7`.

---

## ADR-0007 — Projections, not persistence: rollups, RAG verdicts, release notes, maturity tallies are recomputed on read, never stored

**Status:** Accepted (scaffolded 1bffad7, 2026-06-15)

**Context.** A derived value that is stored as a field — a RAG colour, a score, an
acceptance-rate, a maturity tally — rots the moment the inputs under it change, and reads
back as a verdict an agent once asserted. The library wants neither a stale fact nor a
smuggled verdict.

**Decision.** Rollups, RAG verdicts, release notes, and pattern-maturity tallies are
**recomputed on read or in an Action**, never stored as a field that can rot. Staleness is
answered by `git diff` / `git blame`.

**Consequences.** A derived-on-read fact is kept honest — it is not a stored verdict an agent
asserted, which reinforces the TARGET RULE that an agent emits no verdict. **What breaks if
changed:** storing a RAG colour or score reintroduces a verdict (forbidden by the TARGET RULE)
*and* a value that can silently rot. This is why `portfolio-rollup.json` is gitignored — it is
a derived-on-read RAG projection, not a committed fact.

**Alternatives / Dissent.** Persisting a RAG colour, score, or acceptance-rate metric —
forbidden ("a check optimised for throughput is worse than none").

**Evidence.** `skills/_shared/trace-edge.md`; `DESIGN.md` §2 invariant 5;
`.gitignore` (`portfolio-rollup.json`); commit `1bffad7`.

---

## ADR-0008 — Anti-fatigue: review only the delta-since-last-green; dismissal-memory re-arms only on changed evidence; no throughput / per-person metric

**Status:** Accepted (scaffolded 1bffad7, 2026-06-15)

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
score**, a verdict wearing a number (forbidden by the TARGET RULE).

**Evidence.** `skills/_shared/dismissal-memory.md` (quoted by
`reconcile-design-vs-requirements`, `enumerate-roadblocks`, `triage-backlog-and-defer`,
`red-team-and-dissent`, `advisory-governance-checklist`); `DESIGN.md` §2 invariant 7;
commit `1bffad7`.

---

## ADR-0009 — Looser named skill categories (ingest / understand / challenge / architect / panel / deliver / library / meta), not a numbered scheme

**Status:** Accepted (5877839, 2026-06-15)

**Context.** A developer rarely runs the whole method end-to-end in one go and must find a
single skill *on its own*, by intent. A numbered scheme imposes a false fixed sequence the
library does not have — "a map, not a track".

**Decision.** Skills live under looser *named* categories — `ingest`, `understand`,
`challenge`, `architect`, `panel`, `deliver`, `library`, `meta` — **not** a numbered
scheme. Names describe purpose, so an agent finds a skill by intent.

**Consequences.** An agent finds a skill by what it is for, and the categories carry no
implied order. **What breaks if changed:** renaming or re-numbering a category breaks every
hardcoded part path in `skills/_scripts/bundles.yml` and `concat_skills.py` (the concat
Action's `--check` fails and committed bundles go stale), every cross-link in `MAP.md` /
`GETTING-STARTED.md` / `README.md` / `ENTRYPOINT.md`, and the named-as-purpose contract. The
lint itself tolerates a rename (categories are discovered dynamically), so the break is in
human navigation and bundle paths, not lint legality.

**Alternatives / Dissent.** A numbered category scheme — rejected because numbers imposed a
false fixed sequence the library rejects ("a map, not a track"); the restructure to named
categories is recorded in the commit message "Looser categories (numbers dropped)".

**Evidence.** `MAP.md` (View 2); `skills/_scripts/bundles.yml`; `concat_skills.py`;
commit `5877839`.

---

## ADR-0010 — Underscore-prefixed machinery folders (_contract/, _shared/, _scripts/) separated from the runnable product

**Status:** Accepted (scaffolded 1bffad7, 2026-06-15)

**Context.** The tree holds two different things: skills a reader actually runs, and the
authoring machinery behind them (the human-readable spec, the byte-stable quotable blocks,
the validators and concatenators the Actions run). Mixing them pollutes the map and confuses
a reading agent about what is runnable.

**Decision.** Authoring machinery lives in underscore-prefixed folders, separated from the
runnable product: `_contract/` (the human-readable spec per convention), `_shared/` (the
byte-stable quotable block skills paste in, which the drift check pins), and `_scripts/` (the
validators and concatenators the Actions run).

**Consequences.** The runnable product stays legible and the map only lists things a reader
runs. **What breaks if changed:** renaming `_shared/` or `_contract/` breaks the drift-guard
wiring (`check-shared-stub-drift` auto-discovers stubs via `SHARED_DIR.glob('*.md')`);
renaming `_scripts/` breaks every Action step; dropping the underscore makes the dir read as a
runnable category and pollutes the map.

**Alternatives / Dissent.** Rationale not recorded for any alternative folder layout — the
underscore-prefix convention is asserted as the separation mechanism; confirm with
maintainers.

**Evidence.** `DESIGN.md` §1, §5; the `check-shared-stub-drift` Action
(`SHARED_DIR.glob('*.md')`); commit `1bffad7`.

---

## ADR-0011 — capabilities/ and patterns/ are top-level trees, siblings of skills/, so the CODEOWNERS gate is path-addressable

**Status:** Accepted (capabilities first-classed 5877839, 2026-06-15)

**Context.** Patterns and capabilities are a different *kind* of asset from skills, with a
different governance model and lifecycle — and one of them carries the library's single hard
human gate. That gate is keyed off path prefixes, so the path layout is load-bearing.

**Decision.** `capabilities/` and `patterns/` are **top-level trees**, siblings of
`skills/`. The load-bearing reason is the gate: `CODEOWNERS` keys the one hard gate off the
path prefixes `/patterns/**` and `/capabilities/**` (last-match-wins). Top-level paths make
that gate addressable.

**Consequences.** The one structurally-required human review is path-addressable and
unambiguous. **What breaks if changed:** moving these trees under `skills/` (or renaming
them) breaks the hard gate — the `CODEOWNERS` lines no longer match, so the required human
review silently disappears and pattern / capability changes fall under the advisory
`/skills/**` route. It also breaks path-triggered Actions and every `fulfils_capability:` /
`fulfilled_by:` cite.

**Alternatives / Dissent.** Nesting capabilities / patterns under `skills/` — no source
records a counter-argument for nesting; the rationale for that road-not-taken is not
recorded, confirm with maintainers.

**Evidence.** `.github/CODEOWNERS` (`/patterns/**` and `/capabilities/**`, last-match-wins);
`DESIGN.md` §1, §6–7; commit `5877839`.

---

## ADR-0012 — generated/ bundles are committed; portfolio-rollup.json is gitignored (committed paste-one-file vs derived-on-read projection)

**Status:** Accepted (scaffolded 1bffad7, 2026-06-15)

**Context.** Two derived artefacts pull in opposite directions. A concatenated bundle is
useful to *commit* so an agent can load one paste-able file without first running the Action.
A portfolio RAG rollup is a derived-on-read projection that would rot if stored.

**Decision.** `generated/` bundles are **committed**; `portfolio-rollup.json` is
**gitignored**. Committing the bundles lets an agent load **one** paste-able file (the
wire-up in `GETTING-STARTED.md`); they are kept non-noisy via `.gitattributes`
(`linguist-generated -diff merge=ours`). `portfolio-rollup.json` is gitignored because it is a
derived-on-read RAG projection — the projections-not-persistence decision (ADR-0007).

**Consequences.** Any agent gets a paste-one-file path without running the Action, while no
rot-prone RAG score lands in git. **What breaks if changed:** un-committing the bundles breaks
the "paste one file" path for any agent that has not run the Action; hand-editing `generated/`
trips the concat `--check` (and `merge=ours` discards the edit on rebuild); committing
`portfolio-rollup.json` violates projections-not-persistence (a stored RAG score that rots).

**Alternatives / Dissent.** Treating both derived artefacts the same way (both committed, or
both ignored) — rejected because they answer different questions: one is a committed
paste-one-file convenience, the other a derived-on-read projection.

**Evidence.** `.gitattributes` (`linguist-generated -diff merge=ours`); `.gitignore`;
`GETTING-STARTED.md`; `DESIGN.md` §4; commit `1bffad7`.

---

## ADR-0013 — Two navigation altitudes: a thin root ENTRYPOINT.md and the exhaustive skills/MAP.md (the navigator's deterministic fallback)

**Status:** Accepted (scaffolded 1bffad7, 2026-06-15)

**Context.** Two reader needs sit at two altitudes: a newcomer who wants a thin front door
(use vs contribute), and an agent or reviewer who wants the exhaustive catalogue — which also
serves as a deterministic fallback when model-driven navigation is unavailable.

**Decision.** Keep both a thin root `ENTRYPOINT.md` and the exhaustive `skills/MAP.md`.
`ENTRYPOINT.md` is deliberately thin: it names only the two `meta/` skills (use vs
contribute) plus three deep links. `MAP.md` is the exhaustive catalogue *and* the navigator's
deterministic fallback ("it reads them, never replaces them").

**Consequences.** A reader enters at the right altitude, and the navigator has a deterministic
catalogue to fall back to. **What breaks if changed:** delete `ENTRYPOINT.md` and the "Start
here" links dangle and the two-doors-by-intent affordance is lost; delete `MAP.md` and no
skill breaks ("every skill stands alone") *but* the navigator loses its deterministic fallback
and the project-seed block disappears.

**Alternatives / Dissent.** A single navigation document — rejected because it cannot serve
both altitudes (thin front door vs exhaustive fallback) at once.

**Evidence.** `ENTRYPOINT.md`; `MAP.md`; `DESIGN.md` §1; commit `1bffad7`.

---

## ADR-0014 — Skill category scheme is open: first-level dirs under skills/ are discovered dynamically, no linter edit to add a group

**Status:** Accepted (discovery verified; ingest added 580e236, meta added c5ac713)

**Context.** A category scheme that is hardcoded in a linter re-couples adding a skill group
to editing a validator — friction every time the method grows. The scheme is meant to be open.

**Decision.** First-level directories under `skills/` are discovered **dynamically** —
`lint_map_links.category_dirs()` (lines 106–116) enumerates them at runtime — so adding a
skill group needs no linter edit.

**Consequences.** New groups slot in without touching validators — `ingest` (commit `580e236`)
and `meta` (commit `c5ac713`) were both added this way. **What breaks if changed:** hardcoding
a category enum re-couples the open scheme to a linter edit; a new top-level dir that is
*machinery* (not a category) must carry the underscore prefix or discovery treats it as a
runnable category.

**Alternatives / Dissent.** A fixed category enum in the linter — rejected; no source records
a counter-argument for a fixed enum beyond the friction it would add, so the road-not-taken
rationale is otherwise not recorded; confirm with maintainers.

**Evidence.** `lint_map_links.py` `category_dirs()` (lines 106–116); commits `580e236`,
`c5ac713`.

---

## ADR-0015 — pattern_key (PAT-<UPPER-KEBAB>) is the stable cite-able id, deliberately decoupled from the filename stem

**Status:** Accepted (scaffolded 1bffad7, 2026-06-15)

**Context.** The pattern key is what every bundle, retrieval, and supersede reference cites,
so it must survive a file being renamed for legibility. If the key were tied to the filename
stem, every rename would change the key and orphan its citations.

**Decision.** `pattern_key` (`PAT-<UPPER-KEBAB>`) is the stable cite-able id, deliberately
**not** required to equal the filename stem. The linter's `note_filename()` records the
pairing as a note, never an error.

**Consequences.** A file can be renamed for legibility without orphaning a citation.
**What breaks if changed:** tying the key to the filename makes every rename change the key
and orphan every reference that cited it; loosening the `PAT-<UPPER-KEBAB>` regex breaks
downstream skills that parse the key shape.

**Alternatives / Dissent.** Requiring `pattern_key` to equal the filename stem — rejected
because it would orphan citations on every rename.

**Evidence.** `patterns/_schema/pattern.frontmatter.schema.json`;
`lint_pattern_frontmatter.py` (`note_filename()`); commit `1bffad7`.

---

## ADR-0016 — evidence[] is required once approval_status is provisional or approved ("no evidence, no promotion")

**Status:** Accepted (scaffolded 1bffad7, 2026-06-15)

**Context.** The library's value is fast-tracking reuse of shapes with a *real track record*.
A pattern minted from an imagined shape that presents as blessed would poison that credibility,
because downstream skills trust `provisional` / `approved` to mean "proven".

**Decision.** `evidence[]` (proof it was BUILT) is **required** once `approval_status` is
`provisional` or `approved` — "no evidence, no promotion". The schema enforces this as an
`allOf` conditional; the linter enforces it in `check_conditional_rules`.

**Consequences.** A pattern cannot be promoted without proof it was built, so a
`provisional` / `approved` status reliably means "proven". **What breaks if changed:** dropping
the gate lets an unbuilt shape masquerade as blessed; fabricating a link to fill the slot is
explicitly forbidden ("leave it honestly empty").

**Alternatives / Dissent.** Allowing promotion without evidence — rejected; the gate protects
credibility against a pattern minted from an imagined shape.

**Evidence.** `patterns/_schema/pattern.frontmatter.schema.json` (`allOf` conditional);
`lint_pattern_frontmatter.py` (`check_conditional_rules`); commit `1bffad7`.

---

## ADR-0017 — approval_status is a closed, human-only enum (candidate → provisional → approved → deprecated); an agent only ever writes candidate

**Status:** Accepted (scaffolded 1bffad7, 2026-06-15)

**Context.** `approval_status` encodes human **trust**, not a machine-derivable fact — a human
PR review is what blesses a pattern. If an agent could advance it, an unreviewed shape would
present as blessed and the one human gate would be bypassed.

**Decision.** `approval_status` is a closed, **human-only** enum:
`candidate → provisional → approved → deprecated`. An agent only ever writes `candidate`.
"Writing `approved` is the single most damaging thing this skill could do."

**Consequences.** The bless step stays a human act; an agent's output always enters at
`candidate`. **What breaks if changed:** if an agent could set `provisional` / `approved`, an
unreviewed shape masquerades as blessed and the one human gate is bypassed.

**Alternatives / Dissent.** Letting an agent advance the status — rejected because the status
encodes human trust, not a machine fact.

**Evidence.** `patterns/_schema/pattern.frontmatter.schema.json`; `patterns/README.md`;
`author-component-pattern/SKILL.md`; commit `1bffad7`.

---

## ADR-0018 — maturity and adoption_count are forbidden as authored input — computed from adoptions/ledger.jsonl

**Status:** Accepted (scaffolded 1bffad7, 2026-06-15)

**Context.** A pattern that calls itself battle-tested with zero adoptions is lying.
"Maturity is arithmetic over the ledger" — a fact that should be computed, never asserted,
so that "used in N engagements" stays honest and adopted-by-zero stays visible.

**Decision.** `maturity` and `adoption_count` are **forbidden** as authored input (schema
`{"not":{}}`) and are **computed** from `adoptions/ledger.jsonl`. The ledger even counts teams
that *evaluated and chose otherwise* — non-adoption is signal.

**Consequences.** A pattern cannot self-declare a track record; the tally is honest and
adopted-by-zero is visible. **What breaks if changed:** if authorable, a pattern self-declares
"battle-tested" with no ledger behind it. The single shared ledger reader keeps the linter's
never-delete invariant and the maturity tally consistent; bypassing it splits the two
consumers' view of an adoption.

**Alternatives / Dissent.** Authoring maturity / adoption_count by hand — rejected because a
self-declared track record with no ledger behind it is a lie.

**Evidence.** `patterns/_schema/pattern.frontmatter.schema.json` (`{"not":{}}`);
`patterns/README.md`; `iter_ledger_records`; commit `1bffad7`.

---

## ADR-0019 — superseded_by is required when deprecated ("deprecate, never orphan"); staleness warns, never blocks; an adopted pattern is deprecated not deleted

**Status:** Accepted (scaffolded 1bffad7, 2026-06-15)

**Context.** A deprecated pattern that names no successor dead-ends every adopter who relied
on it. And in an advisory library, staleness should be a soft caveat, not a hard exclusion.

**Decision.** `superseded_by` is **required** when a pattern is `deprecated` ("deprecate,
never orphan"). Staleness signals (`validity_check_months`, `sunset_at`) **warn, never
block** — "a soft caveat, not a hard exclusion". A pattern with a ledger adoption is
**deprecated, not deleted** (`check_delete_invariant`), so provenance survives.

**Consequences.** Adopters are never dead-ended; staleness stays advisory; adoption history
is never destroyed. **What breaks if changed:** hard-blocking on stale / sunset turns the
advisory library into an enforcement gate; dropping the `deprecated ⇒ superseded_by` rule
dead-ends adopters; deleting an adopted pattern destroys its provenance.

**Alternatives / Dissent.** Hard-excluding stale patterns, or deleting a deprecated one —
both rejected: staleness is advisory, and an adopted pattern is deprecated not deleted so
provenance survives.

**Evidence.** `patterns/_schema/pattern.frontmatter.schema.json` (`validity_check_months`,
`sunset_at`); `lint_pattern_frontmatter.py` (`check_delete_invariant`); commit `1bffad7`.

---

## ADR-0020 — attached_nfrs[] each require kind + statement + acceptance_criterion (kind from the closed 11-value NFR enum)

**Status:** Accepted (scaffolded 1bffad7, 2026-06-15)

**Context.** A pattern's attached NFRs are "the heart of the reuse payoff": on adopt each
becomes a derivable requirement downstream, with its acceptance criterion copied unchanged.
"An NFR with no way to verify it is a wish, not a bar."

**Decision.** Each entry in `attached_nfrs[]` requires `kind` + `statement` +
`acceptance_criterion`, with `kind` drawn from the **closed 11-value NFR enum**.

**Consequences.** Every propagated NFR carries a way to verify it, and the closed enum keeps
downstream propagation / coverage skills able to branch on the 11 values. **What breaks if
changed:** dropping the required `acceptance_criterion` lets unverifiable wishes propagate
downstream as governed requirements; opening the enum breaks downstream skills that branch on
the 11 values.

**Alternatives / Dissent.** An open NFR vocabulary, or NFRs without an acceptance criterion —
both rejected: an unverifiable NFR is a wish, and an open enum breaks downstream branching.

**Evidence.** `patterns/_schema/pattern.frontmatter.schema.json`;
`patterns/_schema/nfr-kinds.enum.txt`; `lint_pattern_frontmatter.py`;
`propagate-pattern-nfrs/SKILL.md`; commit `1bffad7`.

---

## ADR-0021 — reference_implementations[] is additive-optional and held strictly out of the promotion gate (no gate-bleed)

**Status:** Accepted (c5ac713, 2026-06-16)

**Context.** A reference implementation answers a *different* question from `evidence[]`:
evidence = "was this BUILT?" (gates promotion, ADR-0016); a reference implementation = "what
do I start FROM?" (a forward "start here" pointer). The sharpest hazard is **gate-bleed** —
wiring a working IaC repo into promotion so a pattern is blessed on a forward link with no
proof it was built.

**Decision.** `reference_implementations[]` is additive-**optional** and held strictly **out
of the promotion gate** — advisory only. A reference impl that *is* a real build must ALSO be
listed under `evidence[]` (`kind:repo`), promoting "through the existing door, zero new gate
logic".

**Consequences.** A pattern can carry "start here" pointers without those pointers ever
promoting it; a real build still promotes through the one existing evidence door. **What breaks
if changed:** moving the field into `check_conditional_rules` / `PROMOTED_STATUSES` lets a
pattern be promoted on a forward link with no proof it was built — the gate-bleed failure. The
advisory-only contract is asserted in schema + linter + skill so a future contributor sees it
in all three.

**Alternatives / Dissent.** Wiring a reference implementation into the promotion gate —
rejected as gate-bleed. The design doc proposed a **six-value** `kind` enum
(`iac|app|notebook|scaffold|module|pipeline`) plus optional `repo_path` / `scaffold_cmd` /
`last_verified`; the shipped schema **narrowed to four** (`iac|app|notebook|scaffold`) and
dropped the extra fields. *The why of the narrowing is not recorded in any commit; confirm with
maintainers.*

**Evidence.** `patterns/_schema/pattern.frontmatter.schema.json`; `lint_pattern_frontmatter.py`
(kept out of `check_conditional_rules` / `PROMOTED_STATUSES`); commit `c5ac713`.

---

## ADR-0022 — The pattern validator is deterministic and dependency-light (stdlib fallback), advisory about content, sharing one ledger reader

**Status:** Accepted (scaffolded 1bffad7, 2026-06-15)

**Context.** The validator must run on a bare runner with just `python3` ("zero mandatory
third-party dependencies"), and it must enforce only the *structural* contract — content
quality is the human reviewer's job, and turning the linter into a content judge would make
the advisory library a gate.

**Decision.** The pattern validator is deterministic and dependency-light (PyYAML / jsonschema
optional, with a stdlib fallback), **light / advisory about content** (it enforces the
structural contract, not quality), and shares **one** ledger reader (`iter_ledger_records`)
with the lifecycle workflow.

**Consequences.** The run-anywhere promise holds, content judgment stays with the human, and
the never-delete invariant and the maturity tally read the ledger identically. **What breaks if
changed:** adding a hard dependency breaks the run-anywhere promise; making the linter judge
content turns advisory into a gate; forking the ledger parsing splits the two consumers' view of
an adoption.

**Alternatives / Dissent.** A validator with mandatory third-party dependencies, or one that
grades a pattern's quality — both rejected: "it does not grade a pattern's quality".

**Evidence.** `lint_pattern_frontmatter.py` (PyYAML / jsonschema optional); `iter_ledger_records`
(single shared reader); commit `1bffad7`.

---

## ADR-0023 — Capabilities are first-class: a PR-reviewed .md tree, the named middle term between requirements and patterns

**Status:** Accepted (5877839, 2026-06-15)

**Context.** The pattern library answered "what shape did we build", but nothing answered "what
*need* does a system have, and is there a proven shape for it yet". A need outlives the
component that fulfils it, and a reader who can name a need in plain language but not the
technology had no entry point.

**Decision.** Capabilities are **first-class** — a `.md` tree PR-reviewed like patterns,
sitting **between** requirements and patterns as the named middle term. The chain is:
outcome ← requirement (`fulfils_capability`) ← capability (`fulfilled_by`) ← pattern.

**Consequences.** A reader who can name a need but not the technology has a technology-free,
rename-surviving anchor, and `recommend-component-patterns` STEP 0 has the `fulfils_capability`
tag it assumes. **What breaks if changed:** removing the layer re-opens the gap
`derive-capabilities` closed — `recommend-component-patterns` STEP 0 assumes the tag exists but
no skill emits it, and the need is no longer a technology-free, rename-surviving anchor.

**Alternatives / Dissent.** Leaving the requirements→patterns gap unbridged — rejected because
nothing answered the "what need" question and the need outlives its component.

**Evidence.** `capabilities/README.md`; `derive-capabilities/SKILL.md`;
`recommend-component-patterns/SKILL.md` (STEP 0); commit `5877839`.

---

## ADR-0024 — capability_key is CAP-<UPPER-KEBAB>, a distinct namespace; parentage in fields, never the key

**Status:** Accepted (5877839, 2026-06-15; aligned by canonical-key migration 1d55b80)

**Context.** A capability key is the citation target for every requirement that fulfils it and
every pattern that back-references it, so it must survive renames — which means parentage cannot
live in the key.

**Decision.** `capability_key` is `CAP-<UPPER-KEBAB>`, a **distinct namespace**; parentage
lives in **fields**, never the key.

**Consequences.** The key survives renames and stays a stable citation target. **What breaks if
changed:** renaming silently breaks every `fulfils_capability` cite, every pattern `fulfils`
back-ref, and every INDEX row — key-citation, no foreign keys, nothing enforces integrity but
lint and review.

**Alternatives / Dissent.** Putting parentage in the key — rejected (it would make keys
unstable). The migration in commit `1d55b80` aligned this key to the one canonical scheme
(ADR-0033).

**Evidence.** `capabilities/_schema` (capability schema); `INDEX.md` rows; commits `5877839`,
`1d55b80`.

---

## ADR-0025 — Bidirectional capability/pattern edges with link discipline — fulfilled_by required (minItems 1), fulfils back-ref optional, all by key-citation

**Status:** Accepted (5877839, 2026-06-15)

**Context.** A capability *must* name how (or whether) it is fulfilled, but forcing a pattern
edit on every capability authoring would be friction with no payoff. Key-citation, not foreign
keys, is what keeps the edges portable.

**Decision.** Bidirectional edges with link discipline: a capability cites `fulfilled_by:`
(**required**, `minItems 1`); a pattern MAY cite `fulfils:` back (**optional**); a requirement
gains `fulfils_capability:` — all by **key-citation**, no foreign keys.

**Consequences.** The library stays portable (markdown in git), human-auditable (PR diff), and
dependency-free; `fulfilled_by` being mandatory means a capability always names how/whether it
is fulfilled, while the optional back-ref is reader convenience. **What breaks if changed:**
making the back-ref mandatory forces a pattern edit on every capability authoring; dropping
`fulfilled_by` removes the capability→component edge; real foreign keys break the
portable-markdown property the whole library rests on.

**Alternatives / Dissent.** A mandatory `fulfils` back-ref, or real foreign-key edges — both
rejected: the back-ref is reader convenience, and foreign keys break portability. *The why of
the `fulfils`-optional / `fulfilled_by`-required asymmetry beyond "reader convenience vs
load-bearing chain edge" is not further recorded; confirm with maintainers.*

**Evidence.** `capabilities/_schema` (capability schema); `patterns/_schema` (pattern
`fulfils`); the requirement `fulfils_capability` field; commit `5877839`.

---

## ADR-0026 — The alias-searchable INDEX.md is the need-first entry point — each capability requires ≥2 unique lay-synonym aliases

**Status:** Accepted (5877839, 2026-06-15)

**Context.** `capability_domain` is deliberately coarse, so it is *not* how a non-expert finds a
specific capability. The alias index is. "A capability with one alias is hard to find."

**Decision.** The alias-searchable `INDEX.md` is the first entry point for a need-first reader;
each capability requires **≥2** unique lay-synonym aliases. `lint_capability_index` enforces the
sync between the INDEX and the capability files.

**Consequences.** A non-expert finds a capability by a plain-language synonym, and the INDEX
stays in sync. **What breaks if changed:** dropping the ≥2 minimum or letting INDEX drift breaks
findability *and* breaks `derive-capabilities`, whose legal `CAP-` key set IS the INDEX rows — a
stale INDEX silently mis-routes MATCHED tags.

**Alternatives / Dissent.** Relying on the coarse `capability_domain` for findability, or
allowing a single alias — both rejected: the domain is too coarse, and one alias is hard to find.

**Evidence.** `capabilities/_schema`; `capability-domains.enum.txt`; `INDEX.md`;
`lint_capability_index`; commit `5877839`.

---

## ADR-0027 — Proven-vs-candidate lives in fulfilled_by[].confidence (proven requires pattern_key + evidence; candidate carries open_questions)

**Status:** Accepted (5877839, 2026-06-15)

**Context.** A fulfilment that is only a hunch must not read as a recommendation. Honesty about
proven-vs-candidate should be *enforced structurally*, mirroring the pattern
evidence-required-once-promoted rule (ADR-0016), not promised.

**Decision.** Proven-vs-candidate lives in `fulfilled_by[].confidence`: `proven` requires a
`pattern_key` + `evidence`; `candidate` carries `open_questions` and may name only a vendor in
`note`. The schema couples this with an `allOf`. "Do not read a candidate as a recommendation."

**Consequences.** A "proven" fulfilment cannot exist without a `pattern_key` and evidence, and
`recommend-component-patterns` relies on this — an OPEN (candidate-only) capability routes to
honest-empty rather than minting a pattern. **What breaks if changed:** removing the `allOf`
coupling lets a "proven" fulfilment exist with no `pattern_key` / evidence, so a hunch reads as
a recommendation.

**Alternatives / Dissent.** Letting `confidence:proven` stand without evidence — rejected;
honesty is enforced structurally, not promised.

**Evidence.** `capabilities/_schema` (`allOf`); `capabilities/README.md`;
`recommend-component-patterns/SKILL.md`; commit `5877839`.

---

## ADR-0028 — No agent sets confidence:proven or advances capability approval_status — promotion is a human PR

**Status:** Accepted (5877839, 2026-06-15)

**Context.** Promotion of a capability — declaring a fulfilment proven, or advancing its
approval status — is a human trust act, the one structural human review in an otherwise
gate-free library. If an agent could self-promote, a fabricated or unproven fulfilment would
present as a recommendation with no human in the loop.

**Decision.** No agent sets `confidence:proven` or advances `approval_status` — promotion is a
**human PR**. The schema "only makes sure the reviewer has the fields they need".

**Consequences.** Capability promotion stays a human act; an agent's output never self-promotes.
**What breaks if changed:** if an agent could self-promote, a fabricated / unproven fulfilment
presents as a recommendation with no human in the loop.

**Alternatives / Dissent.** Agent self-promotion of a capability — rejected; it honours the
propose-then-ratify, no-fabrication posture.

**Evidence.** `capabilities/_schema`; `capabilities/README.md`; commit `5877839`.

---

## ADR-0029 — Capability governance_nfrs (minItems 1) draw kind from the same closed 11-kind NFR vocabulary the patterns use

**Status:** Accepted (5877839, 2026-06-15)

**Context.** A capability's governance floor is what a human measures a candidate's spike result
against. If its NFR vocabulary diverged from the patterns' vocabulary, capability and pattern
NFRs could no longer be compared. "A floor a reviewer cannot check is a wish, not a bar."

**Decision.** `governance_nfrs` (`minItems 1`) carry the minimum measurable bar, with `kind`
drawn from the **same closed 11-kind NFR vocabulary** the patterns use.

**Consequences.** Capability and pattern NFRs stay comparable, and a reviewer always has a
checkable floor to measure a spike against. **What breaks if changed:** diverging the NFR enum
from `patterns/_schema/nfr-kinds.enum.txt` breaks the shared comparison; dropping
`acceptance_criterion` makes the floor uncheckable (a spike "passed" on vibes).

**Alternatives / Dissent.** A separate capability NFR vocabulary, or a floor with no
acceptance criterion — both rejected: divergence breaks comparison and an uncheckable floor is
a wish.

**Evidence.** `capabilities/_schema` (`governance_nfrs`); `patterns/_schema/nfr-kinds.enum.txt`
(shared vocabulary); commit `5877839`.

---

## ADR-0030 — derive-capabilities emits two outputs — MATCHED fulfils_capability proposals (real INDEX row) and PROPOSED-NEW (un-ranked menu cited to req_key)

**Status:** Accepted (5877839, 2026-06-15)

**Context.** Something has to close the one open edge — emit the `fulfils_capability` tag that
`recommend-component-patterns` assumes — without inventing a capability not grounded in a
requirement, and without authoring or promoting a capability (a human act).

**Decision.** `derive-capabilities` (mid tier) emits **two** outputs: **MATCHED**
(`fulfils_capability` proposals that resolve to a real INDEX row) and **PROPOSED-NEW** (an
un-ranked menu of unnamed needs, each cited to its `req_key`, routed to
`library/author-capability`). The legal `CAP-` set is the INDEX rows **fixed before
reasoning**, so a MATCHED tag is always real and a PROPOSED-NEW need always cites a requirement
*by construction*.

**Consequences.** "Never invent a capability not grounded in a requirement" is **structural**,
not a model promise, and the fast-path input for `recommend-component-patterns` exists.
**What breaks if changed:** if it invented `CAP-` keys or authored / promoted capabilities, the
no-fabrication keystone and the human gate both break; if it did not emit `fulfils_capability`,
the fast-path input disappears.

**Alternatives / Dissent.** Letting the skill author or promote a capability, or invent a
`CAP-` key — rejected; authoring / promotion is a human PR and the legal key set is fixed before
reasoning.

**Evidence.** `derive-capabilities/SKILL.md`; `INDEX.md` (legal `CAP-` set fixed before
reasoning); `library/author-capability`; commit `5877839`.

---

## ADR-0031 — The eight solution-architecture section keys are a frozen, closed, ordered set the architect skills never invent, rename, reorder, add to, or drop

**Status:** Accepted (scaffolded 1bffad7, 2026-06-15)

**Context.** Three skills touch the same solution architecture: a generator *emits* sections, a
reconcile step *looks for* sections, and an importer *maps onto* sections. If the section keys
could drift, those three would desync silently. One source of truth is required.

**Decision.** The **eight** solution-architecture section keys are a frozen, closed, ordered set
the architect skills do **not** invent, rename, reorder, add to, or drop — so the section a
generator emits, a reconcile step looks for, and an importer maps onto are the same eight in the
same order.

**Consequences.** The generator, reconcile, and import skills stay in lockstep on one section
vocabulary. **What breaks if changed:** renaming or reordering a key silently desyncs
`synthesise-solution-architecture`, `reconcile-design-vs-requirements`, and
`import-external-design`.

**Alternatives / Dissent.** An open or per-skill section set — rejected because it would let
the three consumers desync silently.

**Evidence.** `skills/_shared/frozen-8-sections.md`; `references/frozen-8-sections.md`;
`synthesise-solution-architecture`, `reconcile-design-vs-requirements`,
`import-external-design`; commit `1bffad7`.

---

## ADR-0032 — Accept-high / derive-low — humans ratify the few genuine commitments; agents derive and auto-apply everything beneath, each carrying a derives_from citation

**Status:** Accepted (scaffolded 1bffad7, 2026-06-15)

**Context.** The human's attention is the scarce resource. Asking a person to accept every
derived requirement is the fatigue failure the library exists to avoid — but auto-deriving
without a safety net would let an agent's synthesis stand with no human commitment above it.

**Decision.** Humans ratify only the few genuine commitments (business outcomes, the solution
shape, contested calls); agents **derive and auto-apply** everything beneath, each derived item
carrying a `derives_from` citation back to its accepted upstream node.

**Consequences.** The human spends attention only on load-bearing commitments. Derive-low is
**safe, not a bypass**, because of the trace edge (ADR-0006): a derived row is structurally a
proposal threaded to an *already-accepted* parent, so rejecting an upstream outcome *visibly
orphans* its derived subtree (a reconcile step surfaces the dangling citations) rather than
silently cascade-deleting it. **What breaks if changed:** emitting a derived (LOW) artefact
without a `derives_from` link, or threading it to an outcome never accepted ("orphan-blind
derivation"), removes the safety net — an agent's synthesis could then stand with no human
commitment above it.

**Alternatives / Dissent.** Per-item human acceptance of every derived requirement — rejected
as the fatigue failure the model exists to prevent. A foreign-key edge — rejected; the edge is a
plain-text citation in a file-based library.

**Evidence.** `propose-ratify-rhythm/SKILL.md` (Step 2); `target-rule-output-kinds/SKILL.md`
("derive-from-accepted-upstream"); `DESIGN.md` §2; commit `1bffad7`.

---

## ADR-0033 — One canonical req-key scheme — exactly one prefix per kind (BO-/REQ-/CAP-/PAT-/DEC-, optional AC-<REQ>.<n>) with the one normalisation rule

**Status:** Accepted (1d55b80, 2026-06-16) — maintainer overrode the panel's lean "bless-the-existing-set" recommendation

**Context.** Six incompatible key schemes were live across the skills (`BO-/TR-`, `F-/NFR-`,
`C-/O-/R-/P-/D-`, `OUT-/REQ-`, bare integers, `O-/R-`). The divergence "would have broken
provenance, the absent-input halt precondition, and re-ingest de-dup": ingest can't stamp
provenance to a stable key, a "HALT if no `O-*` keys" precondition fires spuriously on a valid
`BO-*` project, and re-ingest de-dup keys off a number that renumbers across schemes.

**Decision.** One canonical scheme — **exactly one prefix per kind**: `BO-<n>` (business
outcome), `REQ-<n>` (requirement, functional *or* non-functional — F/NF is `classify`
metadata, never in the key), `CAP-<SLUG>`, `PAT-<SLUG>`, `DEC-<n>`, plus the optional child key
`AC-<REQ>.<n>`. The **one normalisation rule**: read the key scheme **from the target file,
never assume one** (this kills a spurious halt — never argue a project out of its own valid
keys); when a source uses another prefix, normalise on write **and preserve the source's own
identifier verbatim as `source_ref`**, so a re-read de-dups on `source_ref`, not on a minted
key that renumbers across schemes.

**Consequences.** Provenance stamps to a stable key, the halt precondition stops firing
spuriously, and re-ingest de-dup is stable. The RAID register's `R-` / `A-` / `T-` ids are a
**separate namespace, deliberately untouched** (they name register rows, "a reading aid, not a
key"). **What breaks if changed:** reverting to per-stage prefixes re-opens the three failures;
renaming any prefix breaks every `derives_from` / `fulfils_capability` / `fulfilled_by` field
that cites a key; putting parentage back *in* the key makes keys unstable.

**Alternatives / Dissent.** **Real, recorded dissent.** A design panel **recommended the
leaner route** — "bless-the-existing-set + one normalisation rule", to avoid touching six
skills' worked examples. The maintainer **overrode** this at build time and chose a single
canonical scheme + full migration (commit `1d55b80`) for long-term coherence, migrating every
skill, worked example, reference, and the trace-edge block. Record both: the lean route was the
panel's recommendation; the clean single scheme was the maintainer's call. *Why uppercase
prefixes, why integer counters for `BO-/REQ-/DEC-` but slugs for `CAP-/PAT-`, and why
`AC-<REQ>.<n>` is the one place hierarchy is allowed in a key — not recorded; confirm with
maintainers.*

**Evidence.** `skills/_shared/req-key-conventions.md` (read the scheme from the target file;
preserve `source_ref` verbatim); commit `1d55b80`.

---

## ADR-0034 — halt is the fourth output kind with the library's first working halt exemplar — absent/unreadable/empty map to one question-shaped halt, applied additively not as a gate

**Status:** Accepted (580e236, 2026-06-16)

**Context.** `halt` was legal in the TARGET RULE (ADR-0001) but had **zero exemplar** —
verified, every skill used only `proposal` / `question` / `menu`. Halt-first skills (ingest,
navigator, feature intake) needed one reference shape so every halt looks the same and none
drift into smuggling a verdict.

**Decision.** `halt` is the fourth output kind, and the grounding contract carries the
library's **first working halt exemplar**. Absent / unreadable / empty all map to the **same**
halt, computed as a file-level fact at STEP 0 before any model runs. The *empty* case matters
most: a silent-empty reads downstream as "the source had nothing in it" — a silent-proceed
failure; "I read nothing" and "I cannot read this" are deliberately different outputs. A halt is
a **question, never a verdict** — it carries only what is required, what is missing, and the
readable formats. It is applied **additively, not as a gate**: mark Inputs Required / Optional,
quote the block, wire a STEP 0 halt path — "it stops this run and asks; the human supplies the
input and re-runs. Nothing downstream is blocked."

**Consequences.** Every halt-first skill has one reference shape to copy, so halts stay uniform
and verdict-free. **What breaks if changed:** the marked-WRONG counter-example invents
`REQ-1/REQ-2/REQ-3`, an uptime NFR, a "4–8 days" estimate, and "looks infeasible" — "a halt that
contains a finding is not a halt; it is a verdict with an apology attached"; that breaks both
this rule and the TARGET RULE.

**Alternatives / Dissent.** A halt that carries a finding or feasibility verdict — the
marked-WRONG counter-example, explicitly rejected. Applying halt as a downstream-blocking gate —
rejected; it is an advisory output kind.

**Evidence.** `skills/_contract/grounding-no-absent-input/SKILL.md` (first halt exemplar; STEP 0
file-level fact; marked-WRONG verdict counter-example); commit `580e236`.

---

## ADR-0035 — Split each ingest skill into a deterministic no-model read (locator + sha256) and a separate model map; the _scripts readers are a non-authoritative regenerable cache

**Status:** Accepted (580e236, 2026-06-16)

**Context.** Whether a requirement was *lifted* from a source or *fabricated* by a model should
be a structural fact, not a model promise. That only holds if the read is mechanical: a block
must carry a locator plus a hash of its own bytes, so a re-read proves the block unchanged and a
minted requirement walks back to the exact span.

**Decision.** Split each ingest skill into a **deterministic no-model read** (locator + sha256)
and a **separate model map**. The `skills/ingest/_scripts/` readers are a **non-authoritative,
regenerable cache** — the staged original is the source of truth.

**Consequences.** Lifted-vs-fabricated is a structural fact; reingest-delta has a deterministic
diff floor; AC provenance walks back to an exact span. **What breaks if changed:** if the reader
becomes authoritative (or the read folds into the model step), the locator + sha256 can no longer
prove a block unchanged, reingest-delta loses its deterministic diff floor, and AC provenance
degrades from a structural fact to a model claim.

**Alternatives / Dissent.** Folding the read into the model step, or treating the readers as
authoritative — both rejected; the read must stay mechanical and the staged original is the
source of truth.

**Evidence.** `skills/ingest/_scripts/projection.py`; `skills/ingest/_scripts/README.md`
(contract #1–2); commit `580e236`.

---

## ADR-0036 — Ingest readers skip-never-raise — a content problem returns status="skipped" + reason, never throws

**Status:** Accepted (580e236, 2026-06-16)

**Context.** The calling skill needs a single, swallow-proof signal it can turn into a HALT. An
uncaught raise either crashes the run or collapses the distinction between "I cannot read this"
and "I read nothing".

**Decision.** Ingest readers **skip-never-raise**: a content problem returns `status="skipped"`
plus a reason, never throws — "skip, never raise; halt, never empty".

**Consequences.** The skill always gets a clean signal to turn into a HALT, and unreadable vs
empty stay distinguishable. **What breaks if changed:** if a reader raises, the skill can't
reliably distinguish unreadable from empty, and the HALT-not-empty discipline (ADR-0037)
collapses into a silent-empty or a crash.

**Alternatives / Dissent.** Letting a reader raise on a content problem — rejected; an uncaught
raise crashes the run or collapses the unreadable-vs-empty distinction.

**Evidence.** `skills/ingest/_scripts/` readers; `skills/ingest/_scripts/README.md`;
commit `580e236`.

---

## ADR-0037 — HALT-not-empty — an unreadable OR readable-but-empty source HALTs; an empty requirement set is never a valid ingest output

**Status:** Accepted (580e236, 2026-06-16)

**Context.** A blank sheet, wrong tab, or whitespace paste can produce an empty-but-clean-looking
requirement set. A silent-empty reads downstream as "the source had nothing in it" — the
silent-proceed failure the grounding rule (ADR-0004) forbids. This near-miss slipped through once
in review.

**Decision.** **HALT-not-empty** — an unreadable OR readable-but-empty source HALTs; an empty
requirement set is **never** a valid ingest output.

**Consequences.** A blank or wrong source stops and asks instead of emitting a clean-looking
empty set. **What breaks if changed:** a blank sheet / wrong tab / whitespace paste produces an
empty-but-clean-looking requirement set that downstream skills treat as authoritative.

**Alternatives / Dissent.** Returning an empty result on an unreadable or empty source —
rejected; silent-empty is a silent-proceed failure.

**Evidence.** `skills/ingest/_scripts` (HALT path); the grounding contract; commit `580e236`.

---

## ADR-0038 — Preserve the source's own id verbatim as source_ref; de-dup/diff on source_ref (content hash), never the minted key

**Status:** Accepted (580e236, 2026-06-16)

**Context.** The minted key renumbers across the library's incompatible schemes, so de-duping on
it silently forks one source into two or drops a real new version. A `stage-and-fingerprint`
fingerprint on the source ROW did not cover this — it was on the row, not the emitted KEY.

**Decision.** Preserve the source's own id **verbatim** as `source_ref`; de-dup and diff on
`source_ref` (a content hash), **never** the minted key. `block_source_ref()` = locator +
sha256(block text).

**Consequences.** De-dup is stable across schemes — one source stays one source, and a genuine
new version is not dropped. **What breaks if changed:** keying de-dup on the minted key
reintroduces the duplicate-under-a-new-key hazard (forks) or drops a genuine new version, on any
project using more than one scheme — which the design verifies is the live state.

**Alternatives / Dissent.** De-duping on the minted key — rejected; it forks or drops on any
multi-scheme project.

**Evidence.** `skills/ingest/_scripts` (`block_source_ref()` = locator + sha256(block text));
commit `580e236`.

---

## ADR-0039 — GitHub Project ingest requires a pinned, timestamped snapshot (gh project item-list --format json), never a live board read

**Status:** Accepted (580e236, 2026-06-16)

**Context.** A live board is as stale-prone as any export: a field rename silently remaps
"acceptance", a column reorder shifts a locator. For a lifted AC's provenance to stay true, the
read must be against a pinned snapshot, not a moving board.

**Decision.** GitHub Project ingest requires a **pinned, timestamped snapshot**
(`gh project item-list --format json`), never a live board read. `ghproject.py` normalises gh's
nondeterministic ordering so two pulls of an unchanged board hash identically; each item becomes
its own one-row "sheet" so it rides the identical row-to-requirement path.

**Consequences.** Locators are stable and an unchanged board hashes the same twice.
**What breaks if changed:** a live read makes the locator unstable — a rename / reorder silently
remaps which cell an AC locator points at, so a lifted AC's provenance becomes a lie and
reingest-delta diffs against a moving baseline.

**Alternatives / Dissent.** A live board read — rejected; it makes the locator unstable and the
provenance a lie.

**Evidence.** `skills/ingest/_scripts/ghproject.py` (normalises gh ordering; each item a
one-row sheet); commit `580e236`.

---

## ADR-0040 — SharePoint is export-only — never live-fetch; HALT for a local export, stamp origin + exported_at + a soft staleness-unverified caveat

**Status:** Accepted (580e236, 2026-06-16)

**Context.** A live SharePoint fetch is an auth surface plus a stale-doc hazard. The library
would rather ingest a stale-prone source with its staleness *visible* than launder it away behind
a live connector.

**Decision.** SharePoint is **export-only** — never live-fetch. The skill HALTs asking for a
local export, then stamps `origin` + `exported_at` (or unknown) + a **soft**
staleness-unverified caveat. The caveat is a soft carry, never a hard exclusion.

**Consequences.** No auth surface; a stale-prone source still ingests but its staleness is
visible downstream rather than laundered away. **What breaks if changed:** a live fetch
reintroduces the auth surface and lets a 6-month-old doc ingest as a clean requirement with no
caveat.

**Alternatives / Dissent.** A live SharePoint connector — rejected as an auth + stale-doc
hazard; the HALT branch is the whole of SharePoint support.

**Evidence.** `skills/ingest` (SharePoint halt branch); `DESIGN.md` §9 (limitation);
commit `580e236`.

---

## ADR-0041 — Lift an acceptance criterion only when a source locator backs it; otherwise emit "Acceptance: — (absent in source; not synthesised)" — never synthesise GIVEN/WHEN/THEN

**Status:** Accepted (580e236, 2026-06-16)

**Context.** A synthesised acceptance criterion is "the single most damaging fabrication this
skill could make, because it reads downstream as a tested commitment". Lifted-vs-fabricated must
be a grep-able distinction.

**Decision.** Lift an acceptance criterion **only** when a source locator backs it; if absent,
emit `Acceptance: — (absent in source; not synthesised)`. **Never** synthesise a
GIVEN / WHEN / THEN.

**Consequences.** A missing AC is visibly marked rather than invented, and the
lifted-vs-fabricated split is grep-able. **What breaks if changed:** allowing synthesis makes a
fabricated AC indistinguishable from a lifted one — downstream skills treat it as a real tested
commitment and the grep-for-missing-locator check is defeated.

**Alternatives / Dissent.** Synthesising a GIVEN/WHEN/THEN where the source has none — rejected
as the most damaging fabrication the skill could make.

**Evidence.** `skills/ingest` (row-to-requirement map; grep-able lifted-vs-fabricated
distinction); commit `580e236`.

---

## ADR-0042 — Delegate controlled-vocab metadata to classify-requirements; never inline classify's enums (the drift check guards quoted prose blocks, not enum lists)

**Status:** Accepted (580e236, 2026-06-16)

**Context.** The byte-stable drift check guards MARKED PROSE BLOCKS (quoted stubs), **not** enum
lists. So inlining `classify-requirements`' closed sets where nothing pins them means they
silently drift, and the two skills end up annotating the same requirement with divergent
vocabulary.

**Decision.** Delegate controlled-vocab metadata to `classify-requirements`; do **not** inline
classify's enums — "one owner, cited — never a private copy".

**Consequences.** The controlled vocabulary has one owner, so it cannot drift between two copies.
**What breaks if changed:** inlining creates an unguarded second copy; when classify changes its
sets, the ingest copy drifts undetected and the two skills annotate the same requirement with
divergent vocab.

**Alternatives / Dissent.** Inlining classify's enums into the ingest skill — rejected; the
drift check does not guard enum lists, so the copy would drift silently.

**Evidence.** `skills/ingest` (delegates to `classify-requirements`; "one owner, cited");
commit `580e236`.

---

## ADR-0043 — stage-and-fingerprint vaults the bytes byte-untouched (no re-encoding/trim); the vaulted copy is the source of record for every locator and diff

**Status:** Accepted (580e236, 2026-06-16)

**Context.** Every locator and every reingest-delta diff is computed relative to the vaulted
original. Any normalisation on the way in shifts byte offsets, so existing locators point at the
wrong span and a future diff compares a cleaned copy against an uncleaned baseline.

**Decision.** `stage-and-fingerprint` vaults the bytes **byte-untouched** (no re-encoding, no
trim); the vaulted copy is the **source of record** for every locator and diff.

**Consequences.** Every locator and future diff stays valid against a stable baseline.
**What breaks if changed:** any normalisation shifts byte offsets, so existing locators point at
the wrong span and reingest-delta diffs a cleaned copy against an uncleaned baseline.

**Alternatives / Dissent.** Re-encoding or trimming the bytes on the way in — rejected; it
silently invalidates every downstream locator and future diff.

**Evidence.** `skills/ingest/stage-and-fingerprint`; commit `580e236`.

---

## ADR-0044 — Identity binding is proposed via deterministic signals (content_hash, source_ref), model only a tie-breaker; a renamed-file overlap is a QUESTION, never an auto-bind

**Status:** Accepted (580e236, 2026-06-16)

**Context.** A wrong auto-bind drops a real version (under-count) or forks one source into two
(the duplicate hazard). The hash IS the de-dup; the model is at most a tie-breaker, so a human
should ratify a binding the deterministic signals do not settle.

**Decision.** Identity binding is **proposed via deterministic signals** (`content_hash` exact,
`source_ref` identity), with the model only as a **tie-breaker** for a renamed file. A
renamed-file overlap is a **QUESTION**, never an auto-bind.

**Consequences.** A binding the signals do not settle goes to a human rather than being guessed.
**What breaks if changed:** auto-binding a renamed file silently routes a new version to a fresh
ingest (forking under new keys) or collapses two distinct sources into one.

**Alternatives / Dissent.** Auto-binding on a model guess for a renamed file — rejected; the
human ratifies the binding, the hash is the method and the model is only a tie-breaker.

**Evidence.** `skills/ingest` (identity binding); commit `580e236`.

---

## ADR-0045 — reingest-delta surfaces only the delta — never silently overwrites, never auto-deletes a removed row, treats a status flip as a scope QUESTION; unchanged rows carry forward

**Status:** Accepted (580e236, 2026-06-16)

**Context.** Re-reading and re-minting everything either duplicates the set under new keys or
clobbers human edits made since the first ingest. A removed `source_ref` is a source bug
candidate, not a decision; a status flip is a scope change a human should rule on.

**Decision.** `reingest-delta` surfaces **only the delta** — it never silently overwrites, never
auto-deletes a removed row, and treats a status flip as a scope **QUESTION**; unchanged rows
carry forward untouched.

**Consequences.** Human edits survive a re-ingest, a source-side drop is questioned rather than
acted on, and the unchanged set is not renumbered. **What breaks if changed:** silent overwrite
destroys human edits; auto-delete removes a requirement a source-side bug may have dropped;
re-minting unchanged rows duplicates / renumbers the whole set.

**Alternatives / Dissent.** Silently overwriting, auto-deleting a removed row, or re-minting
everything — all rejected; each destroys edits, drops real requirements, or duplicates the set.

**Evidence.** `skills/ingest/reingest-delta`; commit `580e236`.

---

## ADR-0046 — check-shared-stub-drift guards in-repo quoted _shared copies (quote-not-import) — edit the canonical stub first, then re-quote into every skill in the same PR

**Status:** Accepted (scaffolded 1bffad7, 2026-06-15)

**Context.** Each skill is markdown meant to run in *any* file-reading workflow — there is no
read-time import. A skill that references a rule it does not contain ships broken when copied out
alone, so each skill must *quote* the canonical `_shared` block verbatim. The cost is duplication,
which needs a drift guard.

**Decision.** `check-shared-stub-drift` guards the **in-repo quoted copies**: each skill quotes
the canonical `_shared` block (TARGET RULE, GROUNDING RULE, TRACE EDGE, req-key conventions)
verbatim between `BEGIN/END` markers, and the Action diffs each copy against the canonical file,
failing if a byte drifts. The working rule: **edit the canonical `_shared/*.md` first, then
re-quote into every skill in the same PR — never edit a quoted copy in place.**

**Consequences.** A skill copied out alone still carries its rules, and the drift guard keeps the
in-repo copies byte-identical to the canonical stub. **What breaks if changed:** the cost is named
in `DESIGN.md` §9 — "duplication is the price of zero-dependency portability… a skill copied out
loses that [drift] guard"; editing a quoted copy in place instead of the canonical stub diverges
the copies.

**Alternatives / Dissent.** A read-time import of the shared rule — rejected; there is no
read-time import in markdown meant to run anywhere, and an imported rule does not travel when a
skill is copied out alone. Duplication is the accepted price of zero-dependency portability.

**Evidence.** The `check-shared-stub-drift` Action (diffs each `BEGIN/END` copy against canonical
`_shared/*.md`); `DESIGN.md` §9; commit `1bffad7`.

---

## ADR-0047 — Multi-agent fan-out is an advisory option capped at ≤4 concurrent — one model call per persona/section/objection/candidate, a failed call returns None and is never fatal; no orchestration framework

**Status:** Accepted (scaffolded 1bffad7, 2026-06-15)

**Context.** The ~10 reasoning-heavy skills can deepen by running several independent model calls
(one per persona, section, objection, or candidate). But an unbounded fan-out floods the human's
review channel, and an orchestration framework would couple the library to heavy machinery it is
designed to avoid.

**Decision.** Multi-agent fan-out is an **advisory option, capped at ≤4 concurrent** — one
independent model call per persona / section / objection / candidate; a failed call returns
`None` and is **never fatal** (merge what succeeded). No orchestration framework. The cap is a
mechanical rate-limiter / legibility guard so the human's review channel does not flood.

**Consequences.** Reasoning-heavy skills can deepen without flooding review or adding a
framework; a failed call degrades gracefully. **What breaks if changed:** removing the cap floods
the human's review channel; making a failed call fatal breaks the never-fatal model posture
(ADR-0005). *The specific number 4 is asserted, not derived from a recorded measurement.*

**Alternatives / Dissent.** An orchestration framework (LangGraph / agent SDK) — rejected: "one
interface, one stub, one capped fan-out".

**Evidence.** `skills/_contract/parallel-agents/SKILL.md`; `DESIGN.md` §5; commit `1bffad7`.
