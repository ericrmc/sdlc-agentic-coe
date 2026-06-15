# RATIONALE — why this library is shaped the way it is

> Companion to [`CONTRIBUTING.md`](CONTRIBUTING.md). `CONTRIBUTING.md` tells you
> *how* to add to the library; this file tells you *why* the architecture holds
> the shape it does, so you do not break a load-bearing decision by accident.

You are the agent (or the human directing one) about to make a change here. **Read
the section that touches your change before you make it.** A line that looks like a
one-liner — rename a folder, add an output kind, make a check blocking, set a status
on a pattern — can quietly dissolve the one property that lets an advisory library
be safe without gates.

**The canonical, atomic, status-tracked record of *why* each decision was made lives in
[`ADR.md`](ADR.md)** — the numbered log of immutable records `ADR-0001..N` (one owner per
decision; the library forbids two sources of truth for the same fact). This document does
not restate those whys; it **indexes** them. Its unique value is the cross-cutting
synthesis the ADRs do not carry: the load-bearing **invariants** (§2), the **lessons /
near-misses** (§4), the **honest limitations** (§5), and the **guard table** (§6) that maps
a tempting change to the property it would dissolve. Each invariant and decision-record row
cites the ADR that owns its rationale — read the ADR for the full *why*, *alternatives*, and
*dissent*; read this doc for *what it touches and what breaks*.

This document obeys the same no-fabrication rule as the library: every "why" below (and in
`ADR.md`) is evidenced in a file, a commit (`git log`), or the maintainers'
design-deliberation notes (referenced below as "the design doc" — an internal artefact held
with the maintainers, not shipped in this repo). Where a rationale is **not recorded
anywhere**, it says so — "rationale not recorded — confirm with maintainers" — rather than
inventing one.

---

## 1. Purpose, and how to use this doc

### What this library is

A **portable library of self-contained markdown `SKILL.md` files** (steps + YAML
frontmatter) that an agent reads and runs inside *any* LLM workflow — a coding agent,
a plain prompt, a CI step. It is **not an app and not a service**. It carries a
PR-reviewed library of reusable component **patterns** and the **capabilities** that
bridge a plain-language need to a proven pattern. Every output is light and advisory:
the skills nudge, they never block.
(`README.md` lines 3–5, 33–34; `DESIGN.md` §1–2.)

### Where this came from (the pivot)

The proven method here was **lifted out of a prior internal delivery tool** — a
bespoke application with hard architecture-review and approval gates. The business
would not support a custom app, so the *method* was preserved and the *plumbing*
(the runtime, the enforcement gates, the central service) was dropped. The value is
the provider-agnostic reasoning, not the machinery that used to host it. That single
fact drives most of what follows: an app couples a method to one runtime; a library
of files runs anywhere a file can be read.
(`DESIGN.md` §9; scaffold commit `1bffad7`.)

> This doc never names the old tool. Lineage to other entities was deliberately
> stripped at de-narration (`5877839`) because narrative about other systems drifts
> a reading agent off task — so this file stays de-narrated too.

### How to use this doc

1. About to make a structural change? Jump to **§6 "Before you make a major change"**
   first — it maps the tempting change to the invariant it touches and the `ADR-NNNN`
   that owns its rationale.
2. Then read the matching **invariant (§2)** or **decision-record index row (§3)**, and
   follow its `ADR-NNNN` citation into [`ADR.md`](ADR.md) for the full why / alternatives /
   dissent.
3. If your change weakens an invariant, that is not necessarily forbidden — but it
   *is* a deep change. Open it as a proposal, name the invariant **and its ADR** in the PR,
   and let a human rule.

---

## 2. The load-bearing invariants

These are the few rules that must not be broken without deep understanding — the
cross-cutting synthesis that is this doc's unique value. They are listed once in
`DESIGN.md` §2; each is owned by an ADR (cited in its heading) where the full why /
alternatives / dissent live. What follows here is the synthesis: how the invariants
reinforce each other and what breaks if one is weakened.

### 2.1 The TARGET RULE — four output kinds, never a verdict (ADR-0001)

**What it is.** Every agent output is exactly one of four kinds — `proposal` |
`question` | `menu` | `halt` — and **never** a status, verdict, colour, ranking,
score, feasibility call, disposition, or an assessment of a person. An agent targets
the **MODEL** (keep a cheap model on rails), the **RECORD** (structure for reuse), or
the **BLIND SPOT** (coverage/de-biasing) — never the **JUDGMENT**, which is the
human's call.
(`skills/_shared/target-rule.md` lines 15–46;
`skills/_contract/target-rule-output-kinds/SKILL.md`.)

**Why it is the keystone.** This is *the principled reason the library needs no
enforcement gates*. Because the **shape** of what an agent may emit forbids it from
self-approving, an advisory library cannot rubber-stamp, cannot mislabel a machine
guess as a human ruling, and cannot let a cheap model's confidence leak out as
authority. The advisory guarantee lives in the **type** of the output — checkable at
author-time and PR-time — so the library can automate aggressively *without* a
blocking mechanism.
(`skills/_contract/target-rule-output-kinds/SKILL.md` — "Why an advisory library is safe
without a blocking mechanism".)

**Alternatives considered.** Enforcement/approval gates that block a downstream
project until a check passes (the prior tool's model) — rejected as heavyweight. A
fifth `recommendation` kind — explicitly rejected as "the most seductive smuggler", a
verdict in disguise; the legal move is an un-ranked `menu` plus cited proposal facts
(`skills/_contract/target-rule-output-kinds/SKILL.md`).

**What breaks if you change it.** Add any output kind that can self-approve (a
verdict / score / RAG colour) and the *entire* rationale for being gate-free
collapses — an agent mistake would then flow into the design as authoritative fact,
the exact failure the rule dissolves. The library would then *need* a blocking
mechanism to stay safe.

### 2.2 Propose → ratify — the agent never ratifies its own work (ADR-0002)

**What it is.** One and only one ratification act: a **human merging the PR**. The
agent opens the PR; it never merges its own work, writes a "ratified" status, or
auto-advances. The merge commit + PR thread **is** the durable, append-only audit
record — no separate event store.
(`skills/_shared/propose-ratify.md` lines 22–26;
`skills/_contract/propose-ratify-rhythm/SKILL.md`; `DESIGN.md` §2 invariant 2.)

**Why.** "The agent never ratifies its own work" keeps a person in control of the
project's direction while the agent does the heavy lifting. Mapping ratify onto a
GitHub merge adds *no extra machinery*: the commit log + PR timeline are already the
trail.

**Alternatives / dissent.** A separate governance-disposition machinery
(`pass` / `pass_with_conditions` / `send_back`) and a privileged disposing role —
rejected because it "turns reviewed back into a blocking checkbox". A separate event
store — rejected; the log is the trail. **Honest limit recorded in `DESIGN.md` §9:**
"PR-is-ratify is a forced fit for in-session iteration" — intra-session work happens
on the branch with no ceremony, and "a human always disposes" is review culture, not
code; a person can proceed past an unread checkpoint and owns that
(`propose-ratify.md` "What this is NOT").

**What breaks if you change it.** A self-merging agent, an auto-applied advance, or
any persisted status that must flip before work proceeds reintroduces a blocking gate
and breaks the advisory-by-construction guarantee — these are the named anti-patterns
"the self-merging agent" and "the smuggled block".

### 2.3 Advisory, not gated — one structural human gate only (ADR-0003)

**What it is.** Every GitHub Action is advisory: it comments and may fail a check to
prompt a human, but **never blocks a merge**. `CODEOWNERS` is the **only** structural
gate — a human architect's review is required to merge any change under
`/patterns/**` or `/capabilities/**`.
(`.github/CODEOWNERS`; `README.md` lines 38, 56–58; `DESIGN.md` §1, §9;
`CONTRIBUTING.md` "The rules that hold everywhere".)

**Why.** Consistent with the keep-it-light pivot: the machine catches the *shape*; a
human still owns every *call*. A pattern/capability enters the shared library only
when a human reviews and merges its PR, carrying the validation, evidence, and
validity dates. The `CODEOWNERS` file itself records *why a pattern gets a hard gate*:
"A pattern is a load-bearing claim… the one artefact that can quietly do harm at
scale" — its NFRs propagate, its constraints replay during validation, its provenance
legitimises a fast-track.

**Alternatives / dissent.** Required (blocking) CI checks — deliberately not used,
*except* the noted option to flip `validate-patterns` to required for `patterns/**`
only. A privileged disposing governance role — rejected. **Honest limit (`DESIGN.md`
§9):** "Advisory CI can let a malformed pattern merge if a reviewer ignores a red
check" — `CODEOWNERS` is the single backstop, and the design openly reserves the right
to make `validate-patterns` blocking for the pattern tree alone. This is the one
acknowledged escape hatch in the no-gate stance.

**What breaks if you change it.** Making Actions blocking reintroduces the heavyweight
gates the pivot was created to drop. Removing the `CODEOWNERS` gate on
patterns/capabilities removes the one place a human ratifies a reusable asset with its
evidence and validity dates — an agent-proposed pattern could then enter the shared
library unratified.

### 2.4 Grounding / no fabrication — an absent required input HALTs (ADR-0004)

**What it is.** A skill names its **required** inputs; an absent/unreadable/empty
required input becomes a typed `halt` that asks where the input is (offering the
formats ingestion reads) and stops — **never** an invented hypothetical, id, key,
number, NFR, or acceptance criterion. "I read nothing" and "I cannot read this" are
deliberately *different* outputs.
(`skills/_shared/grounding.md` lines 11–47;
`skills/_contract/grounding-no-absent-input/SKILL.md`; commit `580e236`.)

**Why.** A richly agent-driven, gate-free library has one remaining way to fail
catastrophically: produce a *clean-looking proposal grounded in nothing*. This is the
one contract that stops it — and it is cheap, because **input presence is a
deterministic, pre-model file-level fact** (computed at STEP 0, before any model
reasons). A `halt` is a question, never a verdict: it carries only what is required,
what is missing, and the readable formats.

**Alternatives / dissent.** Silently proceeding on partial input or back-filling a
guess — forbidden ("partial input is named, not patched"). Returning an *empty* result
on an unreadable source — forbidden, because silent-empty reads downstream as "the
source had nothing in it", a silent-proceed failure. **Honest limit, stated in the
skill itself:** the lint (`lint_skill_grounding.py`) checks only that a skill *cites*
the stub and *wires* a halt path — it "does not and cannot catch a model inventing an
input mid-run", which is runtime behaviour. The contract + halt exemplar are the real
safeguard; "claiming otherwise would be false confidence about the safeguard itself".

**What breaks if you change it.** A halt that smuggles a finding/feasibility verdict
("I halt because this is infeasible") is the marked-WRONG counter-example — it breaks
both this rule *and* the TARGET RULE. Declaring `halt` in `output_kinds` without a
real halt-path step in the body is the exact gap the lint warns on.

### 2.5 Deterministic base + a one-line model step — never fatal (ADR-0005)

**What it is.** Every skill carries a **deterministic, no-LLM base**
(checklist/regex/template/skeleton) plus a one-line model swap that only ever *deepens*
it. A failed, absent, or malformed model call is **never fatal** — the base stands.
The model is named only by a **tier hint** (`frontier` | `mid` | `light`) behind a
one-line seam; no model ids or vendor names appear anywhere.
(`skills/_shared/deterministic-fallback.md`;
`skills/_contract/parallel-agents/SKILL.md` lines 33–41; `DESIGN.md` §2 invariant 3, §8.)

**Why.** This is what makes the library *portable*: a skill earns its keep in a bare
terminal with no API key, on a CI runner, or a locked-down box. The model is an
enrichment, never a dependency — so "light and advisory beats heavy and enforced" is
safe to drop into any environment. The tier-hint-behind-a-seam keeps the high-IP
reasoning portable across any harness: deepening or swapping a model is editing one
word, never rewriting the skill, and the harness binds a deterministic-stub backend or
any live backend in a one-line change.

**Alternatives / dissent.** A model-only skill whose first step is "ask the model" —
an anti-pattern ("if the call fails, the user gets nothing. Always have a floor").
Hard-coding a provider/model id — the "vendor lock in the swap" anti-pattern. Reaching
for an orchestration framework — rejected: "one interface, one stub, one capped
fan-out". **Honest limit:** the base "is allowed to be shallow" — the rule of thumb is
only that a reviewer would accept the no-model output "as a draft"; depth without a
model is a known limitation, not a promise.

**What breaks if you change it.** A hidden model dependency (a `deterministic_fallback`
field claiming a no-LLM path the body doesn't implement) makes the field a false
contract and breaks portability into no-key/CI/offline environments. Naming a concrete
model or vendor breaks the "runs in any harness" portability and the one-word swap.

### 2.6 Trace via fields, never in the key — and projections, not persistence (ADR-0006, ADR-0007)

**What it is.** Parentage and every relationship live in **fields** on the artefact
(`derives_from`, `fulfils_capability`, `fulfilled_by`, `supersedes`/`superseded_by`,
`contests`), never inside the key. `derives_from` is a **portable `req_key` citation**
(plain text, optionally a markdown link), not a foreign key — no database, no id, no
schema. Separately: rollups, RAG verdicts, release notes, and pattern-maturity tallies
are **recomputed on read or in an Action**, never stored as a field that can rot;
staleness is answered by `git diff` / `git blame`.
(`skills/_shared/req-key-conventions.md`; `skills/_shared/trace-edge.md`;
`DESIGN.md` §2.)

**Why.** The citation survives being copied, diffed, PR-reviewed, and grepped; a
foreign key does not survive leaving its database. This is what keeps the edge portable
into *any* file-reading workflow. It is also what makes **accept-high / derive-low**
safe (see §3.4): a derived row is structurally a proposal threaded to an accepted
parent, so rejecting an upstream node *visibly orphans* its derived subtree rather than
silently cascade-deleting it. And recomputing a derived value on read keeps it honest —
a derived-on-read fact is not a stored verdict an agent asserted (reinforcing the
TARGET RULE).

**Alternatives / dissent.** A foreign-key/database edge — "correct for a database",
rejected because the library is file-based. Persisting a RAG colour, score, or
acceptance-rate metric — forbidden ("a check optimised for throughput is worse than
none"). **Honest limit (`trace-edge.md`):** renaming/renumbering a `req_key` "silently
breaks every edge that cites it" — citation stability is an *unguarded* assumption
(nothing enforces referential integrity but the lint and human review).

**What breaks if you change it.** Switching to foreign keys removes the orphaning
safety property and breaks portability (the edge stops working with grep / a plain
prompt). Storing a RAG colour or score reintroduces a verdict (forbidden by the TARGET
RULE) *and* a value that can silently rot.

### 2.7 Anti-fatigue — delta-since-last-green, no throughput metric (ADR-0008)

**What it is.** A re-run reviews only what *changed since last green*; an untouched item is
deferred, not re-surfaced. A dismissed cue (`dismissal-memory`) re-arms **only on changed
evidence** — re-confirming an unchanged finding never re-nags. No acceptance-rate,
throughput, velocity, or per-person metric is computed or stored anywhere.
(`skills/_shared/dismissal-memory.md`, quoted by `reconcile-design-vs-requirements`,
`enumerate-roadblocks`, `triage-backlog-and-defer`, `red-team-and-dissent`,
`advisory-governance-checklist`; `DESIGN.md` §2 invariant 7.)

**Why.** A library that re-flags the same dismissed cue on every run trains its readers to
ignore it — review fatigue is how an advisory signal dies. Delta-since-last-green keeps the
human's attention on what is new; content-addressed dismissal-memory means a settled call
stays settled until the evidence under it moves. And a throughput/per-person metric is a
**smuggled score** — a verdict wearing a number (forbidden by the TARGET RULE, §2.1) — so
the library measures none.

**What breaks if you change it.** Re-surfacing a dismissed cue against unchanged evidence
reintroduces the fatigue the dismissal-memory exists to prevent. Adding an acceptance-rate
or throughput metric smuggles a score back in (it optimises a person/team and reads as a
verdict) — "a check optimised for throughput is worse than none".

---

## 3. Decision records — index over the ADRs

This section is a **navigable index**, not a second narration. The full why /
alternatives / dissent for each decision lives in the cited `ADR-NNNN` in
[`ADR.md`](ADR.md); each row here carries only a one-line gloss, the ADR citation, and the
**what-breaks-if-changed** pointer (the practical reason to read the ADR before touching
it). Grouped by area.

### 3.1 Folder structure & navigation

| Decision | One-line gloss → ADR | What breaks if changed |
|---|---|---|
| **Looser *named* categories** (`ingest` / `understand` / `challenge` / `architect` / `panel` / `deliver` / `library` / `meta`), **not** a numbered scheme. | Names describe purpose so a skill is found by intent — "a map, not a track". See **ADR-0009**. | Renaming/re-numbering a category breaks every hardcoded part path in `skills/_scripts/bundles.yml` + `concat_skills.py` (the concat Action's `--check` fails and committed bundles go stale), every cross-link in `MAP.md`/`GETTING-STARTED.md`/`README.md`/`ENTRYPOINT.md`, and the named-as-purpose contract. The lint itself tolerates a rename (`category_dirs()` discovers dirs dynamically) — so the break is in human navigation + bundle paths, not lint legality. |
| **Underscore-prefixed machinery folders**: `_contract/`, `_shared/`, `_scripts/`. | Separates authoring machinery from the runnable product. See **ADR-0010**. | Renaming `_shared/`/`_contract/` breaks the drift-guard wiring (`check-shared-stub-drift` auto-discovers stubs via `SHARED_DIR.glob('*.md')`); renaming `_scripts/` breaks every Action step. Dropping the underscore makes the dir read as a runnable category and pollutes the map. |
| **`capabilities/` and `patterns/` are TOP-LEVEL trees**, siblings of `skills/`. | A different governance kind; top-level paths make the one `CODEOWNERS` gate path-addressable. See **ADR-0011**. | Moving them under `skills/` (or renaming) breaks the hard gate — the `CODEOWNERS` lines no longer match, so the one structurally-required human review silently disappears and pattern/capability changes fall under the advisory `/skills/**` route. Also breaks path-triggered Actions and every `fulfils_capability:`/`fulfilled_by:` cite. |
| **`generated/` bundles are committed; `portfolio-rollup.json` is gitignored.** | Committed paste-one-file vs derived-on-read projection. See **ADR-0012**. | Un-committing the bundles breaks the "paste one file" path for any agent that hasn't run the Action. Hand-editing `generated/` trips the concat `--check` (and `merge=ours` discards the edit on rebuild). Committing `portfolio-rollup.json` violates projections-not-persistence (a stored RAG score that rots). |
| **Both `skills/MAP.md` (full index) AND a thin root `ENTRYPOINT.md`.** | Two reader altitudes — thin front door + exhaustive map (the navigator's deterministic fallback). See **ADR-0013**. | Delete `ENTRYPOINT.md` and the "Start here" links dangle + the two-doors-by-intent affordance is lost. Delete `MAP.md` and no skill breaks ("every skill stands alone") *but* the navigator loses its deterministic fallback and the project-seed block disappears. |
| **A new top-level skill group is auto-legal** — adding `skills/ingest/` or `skills/meta/` needed no linter edit. | The category scheme is open; first-level dirs are discovered dynamically. See **ADR-0014**. | Hardcoding a category enum re-couples the open scheme to a linter edit. A new top-level dir that is *machinery* (not a category) must carry the underscore prefix or discovery treats it as a runnable category. |

**Dissent / honest cost (folders).** `DESIGN.md` §9 names "Large surface area" — the
de-narrated, category-spread library has a real discovery cost, mitigated by the MAP
table + the GETTING-STARTED persona table + `meta/navigator`; a "core 10" subset was
floated for a lighter first adoption but not built. *No source records a counter-argument
for nesting capabilities/patterns under skills/, nor for a fixed category enum — rationale
not recorded for those; confirm with maintainers.*

### 3.2 Pattern schema & lifecycle

| Decision | One-line gloss → ADR | What breaks if changed |
|---|---|---|
| **`pattern_key` (`PAT-<UPPER-KEBAB>`) is the stable cite-able id, deliberately NOT required to equal the filename stem.** | A cite must survive a file rename, so the key is decoupled from the stem. See **ADR-0015**. | Tying the key to the filename makes every rename change the key and orphan every reference that cited it. Loosening the regex breaks downstream skills that parse the key shape. |
| **`evidence[]` (proof it was BUILT) is REQUIRED once `approval_status` is `provisional` or `approved`** ("No evidence, no promotion"). | The reuse value is a real track record; the gate protects credibility. See **ADR-0016**. | Dropping the gate lets an unbuilt shape masquerade as blessed — downstream skills trust `provisional/approved` to mean "proven". Fabricating a link to fill the slot is explicitly forbidden ("leave it honestly empty"). |
| **`approval_status` is a closed, HUMAN-ONLY enum**: `candidate → provisional → approved → deprecated`. An agent only ever writes `candidate`. | `approval_status` encodes human trust, not a machine-derivable fact. See **ADR-0017**. | If an agent could set `provisional`/`approved`, an unreviewed shape masquerades as blessed and the one human gate is bypassed. |
| **`maturity` and `adoption_count` are FORBIDDEN as authored input** (`{"not":{}}`) — COMPUTED from `adoptions/ledger.jsonl`. | Maturity is arithmetic over the ledger — computing it keeps "used in N engagements" honest. See **ADR-0018**. | If authorable, a pattern self-declares "battle-tested" with no ledger behind it. The single shared ledger reader keeps the linter's never-delete invariant and the maturity tally consistent; bypassing it splits the two consumers' view of an adoption. |
| **`superseded_by` is REQUIRED when `deprecated`; staleness (`validity_check_months`, `sunset_at`) warns, never blocks.** | "Deprecate, never orphan"; staleness is a soft caveat, not a hard exclusion. See **ADR-0019**. | Hard-blocking on stale/sunset turns the advisory library into an enforcement gate. Dropping the `deprecated ⇒ superseded_by` rule dead-ends adopters. |
| **`attached_nfrs[]` each require `kind` + `statement` + `acceptance_criterion`** (`kind` from the closed 11-value NFR enum). | On adopt each becomes a derivable, verifiable requirement — "an NFR with no way to verify it is a wish". See **ADR-0020**. | Dropping the required `acceptance_criterion` lets unverifiable wishes propagate downstream as governed requirements. Opening the enum breaks downstream propagation/coverage skills that branch on the 11 values. |
| **`reference_implementations[]` is additive-OPTIONAL and held strictly OUT of the promotion gate.** | A forward "start here" pointer, not proof-it-was-built; kept out to avoid gate-bleed. See **ADR-0021**. | Moving it into `check_conditional_rules`/`PROMOTED_STATUSES` lets a pattern be promoted on a forward link with no proof it was built — the gate-bleed failure the design guards against. The advisory-only contract is asserted in schema + linter + skill so a future contributor sees it in all three. |
| **The validator is deterministic, dependency-light** (PyYAML/jsonschema optional with a stdlib fallback) and **light/advisory about content**; it shares ONE ledger reader (`iter_ledger_records`) with the lifecycle workflow. | Runs on a bare `python3`, enforces only the structural contract, one shared ledger reader. See **ADR-0022**. | Adding a hard dependency breaks the run-anywhere promise. Making the linter judge content turns advisory into a gate. Forking the ledger parsing splits the two consumers' view of an adoption. |

**Dissent / uncertain (patterns).** The shipped `reference_implementations` sub-shape
(`{kind, url, provisions}` required + optional `notes`) narrowed the design doc's wider
proposed enum/fields — see **ADR-0021** for the decision and the unrecorded-narrowing
caveat. Separately, the specific numeric bounds (`validity_check_months` default 12,
min/max, length caps) are asserted, not derived from a recorded measurement.

### 3.3 Capability schema & the requirements→components bridge

| Decision | One-line gloss → ADR | What breaks if changed |
|---|---|---|
| **Capabilities are first-class** — a `.md` tree PR-reviewed like patterns, sitting **between** requirements and patterns as the named middle term. | The need (technology-free, rename-surviving) is the named middle term: outcome ← requirement ← capability ← pattern. See **ADR-0023**. | Removing the layer re-opens the gap `derive-capabilities` closed: `recommend-component-patterns` STEP 0 *assumes* the `fulfils_capability` tag exists but no skill emitted it. The need would no longer be a technology-free, rename-surviving anchor. |
| **`capability_key` is `CAP-<UPPER-KEBAB>`, a distinct namespace.** | A distinct citation namespace; parentage in fields, never the key. See **ADR-0024**. | Renaming silently breaks every `fulfils_capability` cite, every pattern `fulfils` back-ref, and every INDEX row (key-citation, no foreign keys — nothing enforces integrity but lint + review). |
| **Bidirectional edges with link discipline**: capability cites `fulfilled_by:` (REQUIRED, minItems 1); pattern MAY cite `fulfils:` back (optional); requirement gains `fulfils_capability:` — all by key-citation, no foreign keys. | `fulfilled_by` required (a capability must name how/whether it is fulfilled), back-ref optional; key-citation keeps it portable. See **ADR-0025**. | Making the back-ref mandatory forces a pattern edit on every capability authoring; dropping `fulfilled_by` removes the capability→component edge. Real foreign keys break the portable-markdown property the whole library rests on. |
| **The alias-searchable `INDEX.md` is the first entry point for a need-first reader** — each capability requires **≥2** unique lay-synonym aliases. | The alias index, not the coarse domain, is how a non-expert finds a capability. See **ADR-0026**. | Dropping the ≥2 minimum or letting INDEX drift breaks findability *and* breaks `derive-capabilities`, whose legal `CAP-` key set IS the INDEX rows — a stale INDEX silently mis-routes MATCHED tags. `lint_capability_index` enforces the sync. |
| **Proven-vs-candidate lives in `fulfilled_by[].confidence`** (`proven` requires `pattern_key` + `evidence`; `candidate` carries `open_questions` and may name only a vendor in `note`). | Honesty enforced structurally — "do not read a candidate as a recommendation". See **ADR-0027**. | Removing the `allOf` coupling lets a "proven" fulfilment exist with no `pattern_key`/evidence. `recommend-component-patterns` relies on this — an OPEN (candidate-only) capability routes to honest-empty rather than minting a pattern. |
| **No agent sets `confidence:proven` or advances `approval_status`** — promotion is a human PR. | The one structural human review for capabilities; honours propose-then-ratify. See **ADR-0028**. | If an agent could self-promote, a fabricated/unproven fulfilment presents as a recommendation with no human in the loop. |
| **`governance_nfrs` (minItems 1)** carry the minimum measurable bar, with `kind` drawn from the **same closed 11-kind NFR vocabulary** the patterns use. | The checkable floor a spike is measured against; shared NFR vocabulary keeps capability and pattern bars comparable. See **ADR-0029**. | Diverging the NFR enum from `patterns/_schema/nfr-kinds.enum.txt` breaks the shared comparison; dropping `acceptance_criterion` makes the floor uncheckable (a spike "passed" on vibes). |
| **`derive-capabilities` (mid tier) emits two outputs**: MATCHED (`fulfils_capability` proposals resolving to a real INDEX row) and PROPOSED-NEW (an un-ranked menu of unnamed needs, each cited to its `req_key`, routed to `library/author-capability`). | Legal `CAP-` set fixed (the INDEX) before reasoning, so MATCHED is always real and PROPOSED-NEW always cites a requirement by construction. See **ADR-0030**. | If it invented `CAP-` keys or authored/promoted capabilities, the no-fabrication keystone and the human gate both break. If it didn't emit `fulfils_capability`, `recommend-component-patterns`' fast-path input disappears. |

**Uncertain (capabilities).** The choice of the *six* `capability_domain` values
(`data, compute, integration, runtime, experience, governance`) and the asymmetry
(`fulfils` optional vs `fulfilled_by` required) are stated as facts but the explicit
reasoning beyond "reader convenience vs load-bearing chain edge" is **not recorded** —
confirm with maintainers. Same for `validity_check_months` default 12.

**Frozen solution-architecture sections (closed set).** The eight solution-architecture
section keys in `skills/_shared/frozen-8-sections.md` are a closed, ordered set the
architect skills do not invent, rename, reorder, add to, or drop — one source of truth so
the section a generator emits, a reconcile step looks for, and an importer maps onto are
the same eight in the same order. See **ADR-0031**. **What breaks:** renaming or
reordering a key silently desyncs `synthesise-solution-architecture`,
`reconcile-design-vs-requirements`, and `import-external-design`.

### 3.4 Accept-high / derive-low (the safety net under auto-derivation)

**Decision (gloss → ADR-0032).** Humans ratify only the few genuine commitments
(business outcomes, the solution shape, contested calls); agents **derive and auto-apply**
everything beneath, each derived item carrying a `derives_from` citation back to its
accepted upstream node. The human's attention is the scarce resource; derive-low is **safe,
not a bypass**, because of the trace edge (§2.6) — a derived row is a proposal threaded to
an *already-accepted* parent, so rejecting an upstream outcome *visibly orphans* its derived
subtree rather than silently cascading. See **ADR-0032** for the full why, the rejected
foreign-key / per-item-acceptance alternatives, and the dissent.

**What breaks if you change it.** Emitting a derived (LOW) artefact without a
`derives_from` link, or threading it to an outcome never accepted ("orphan-blind
derivation"), removes the safety net — an agent's synthesis could then stand with no
human commitment above it.

### 3.5 Canonical req-keys & trace-via-fields

**Decision (gloss → ADR-0033).** **One canonical scheme — exactly one prefix per kind**:
`BO-<n>` (business outcome), `REQ-<n>` (requirement, functional *or* non-functional — F/NF
is `classify` metadata, never in the key), `CAP-<SLUG>`, `PAT-<SLUG>`, `DEC-<n>`, and the
optional child key `AC-<REQ>.<n>`. Parentage and every relationship live in **fields**
(`derives_from` is the one trace edge). It replaced six incompatible live schemes that
would otherwise break provenance, the absent-input halt precondition, and re-ingest de-dup.
**ADR-0033 records the real panel-vs-maintainer dissent**: a design panel recommended the
leaner "bless-the-existing-set + one normalisation rule" route to avoid touching six skills'
worked examples; the maintainer **overrode** it for a single canonical scheme + full
migration (`1d55b80`). Read ADR-0033 for the full why and both sides of that call.

**The one normalisation rule (operational, owned by ADR-0033).** Read the key scheme
**from the target file; never assume one** (kills a spurious halt — never argue a project
out of its own valid keys). When a source uses another prefix, normalise on write **and
preserve the source's own identifier verbatim as `source_ref`**, so a re-read de-dups on
`source_ref`, not on a minted key that renumbers across schemes.

**`derives_from` is a citation, not a foreign key** — see §2.6. The RAID register's
`R-`/`A-`/`T-` ids are a **separate namespace, deliberately untouched** by the migration
(they name register rows, not graph artefacts — "a reading aid, not a key").

**What breaks if you change it.** Reverting to per-stage prefixes re-opens the three
failures the migration closed. Renaming any prefix breaks every `derives_from` /
`fulfils_capability` / `fulfilled_by` field that cites a key. Putting parentage back *in*
the key makes keys unstable — re-parenting renumbers the key and breaks every citation.

**Uncertain (keys).** Why uppercase prefixes; why integer counters for `BO-/REQ-/DEC-` but
upper-kebab slugs for `CAP-/PAT-`; why `AC-<REQ>.<n>` is the *one* place hierarchy is
allowed in a key (in tension with "parentage never in the key") — all **not recorded**;
confirm with maintainers.

### 3.6 Grounding / no-fabrication contract

Covered as invariant §2.4. The load-bearing decision that **`halt` is the fourth output
kind**, carried by the grounding contract as the library's **first working halt exemplar**
(absent / unreadable / empty all map to one question-shaped halt computed at STEP 0; a halt
is a question never a verdict; applied additively, not as a gate), is owned by **ADR-0034** —
read it for the full why, the marked-WRONG verdict counter-example, and the alternatives.

The history and dissent below are this doc's synthesis, not duplicated in the ADR:

**Sequencing decision (recorded history).** When five follow-ups were proposed
(capability-derivation, feature-intake, navigator, ingestion, the pattern
reference-implementation field), the maintainer **sequenced the no-fabrication grounding +
ingestion FIRST** as the trust foundation, before the others — so the rest stand on a
contract that already forbids ungrounded output. (Commits `580e236` then `c5ac713`.)

**Dissent (lint scope).** The design doc records a **red-team review (F3)** that pushed a
scope *correction* onto the grounding lint: its prior framing over-claimed; it was narrowed
to two documentation-level checks (cites-the-stub, wires-a-halt) and kept advisory. A
broader, enforcing lint was considered and **explicitly rejected** — "a model inventing an
input mid-run is a runtime behaviour no static lint catches".

### 3.7 Ingestion design

| Decision | One-line gloss → ADR | What breaks if changed |
|---|---|---|
| **Split each ingest skill into a deterministic no-model read (locator + sha256) and a separate model map**; the `skills/ingest/_scripts/` readers are a non-authoritative, regenerable cache. | A mechanical read makes lifted-vs-fabricated a structural fact; readers are a regenerable cache, not the source of truth. See **ADR-0035**. | If the reader becomes authoritative (or the read folds into the model step), the locator+sha256 can no longer prove a block unchanged, reingest-delta loses its deterministic diff floor, and AC provenance degrades from a structural fact to a model claim. |
| **Readers SKIP-never-raise** — a content problem returns `status="skipped"` + a reason, never throws ("Skip, never raise; halt, never empty"). | A single swallow-proof signal the skill turns into a HALT. See **ADR-0036**. | If a reader raises, the skill can't reliably distinguish unreadable from empty, and the HALT-not-empty discipline collapses into a silent-empty or a crash. |
| **HALT-not-empty** — an unreadable OR readable-but-empty source HALTs; an empty requirement set is never a valid ingest output. | A silent-empty reads downstream as "the source had nothing" — the silent-proceed failure grounding forbids. See **ADR-0037**. | A blank sheet / wrong tab / whitespace paste produces an empty-but-clean-looking requirement set that downstream skills treat as authoritative. |
| **Preserve the source's own id verbatim as `source_ref`; de-dup/diff on `source_ref` (content hash), never the minted key.** | The minted key renumbers across schemes, so de-dup on it forks or drops a version; de-dup on the content hash. See **ADR-0038**. | Keying de-dup on the minted key reintroduces the duplicate-under-a-new-key hazard (forks) or drops a genuine new version, on any project using more than one scheme — which the design verifies is the live state. |
| **GitHub Project: require a pinned, timestamped snapshot** (`gh project item-list --format json`), never a live board read. | A live board is stale-prone and shifts locators; a pinned snapshot hashes stably. See **ADR-0039**. | A live read makes the locator unstable: a rename/reorder silently remaps which cell an AC locator points at, so a lifted AC's provenance becomes a lie and reingest-delta diffs against a moving baseline. |
| **SharePoint is export-only** — never live-fetch; HALT asking for a local export, stamp `origin` + `exported_at` (or unknown) + a soft staleness-unverified caveat. | A live fetch is an auth + stale-doc hazard; staleness rides as a soft, visible caveat. See **ADR-0040**. | A live fetch reintroduces the auth surface and lets a 6-month-old doc ingest as a clean requirement with no caveat. |
| **Lift an acceptance criterion ONLY when a source locator backs it**; if absent, emit `Acceptance: — (absent in source; not synthesised)`. Never synthesise a GIVEN/WHEN/THEN. | Makes lifted-vs-fabricated a grep-able distinction; a synthesised AC reads downstream as a tested commitment. See **ADR-0041**. | Allowing synthesis makes a fabricated AC indistinguishable from a lifted one; downstream skills treat it as a real tested commitment and the grep-for-missing-locator check is defeated. |
| **Delegate controlled-vocab metadata to `classify-requirements`; do NOT inline classify's enums.** | "One owner, cited" — the drift check guards quoted prose blocks, not enum lists. See **ADR-0042**. | Inlining creates an unguarded second copy; when classify changes its sets, the ingest copy drifts undetected and the two skills annotate the same requirement with divergent vocab. |
| **`stage-and-fingerprint` vaults the bytes byte-untouched** (no re-encoding/trim); the vaulted copy is the source of record for every locator and diff. | The vaulted original is the baseline for every locator and diff; mutating it invalidates them. See **ADR-0043**. | Any normalisation shifts byte offsets, so existing locators point at the wrong span and reingest-delta diffs a cleaned copy against an uncleaned baseline. |
| **Identity binding is PROPOSED via deterministic signals** (content_hash exact, `source_ref` identity), model only as a tie-breaker for a renamed file; a renamed-file overlap is a QUESTION, never an auto-bind. | The hash is the de-dup, the model only a tie-breaker; a renamed-file overlap is a question, never an auto-bind. See **ADR-0044**. | Auto-binding a renamed file silently routes a new version to a fresh ingest (forking under new keys) or collapses two distinct sources into one. |
| **`reingest-delta` surfaces ONLY the delta** — never silently overwrites, never auto-deletes a removed row, treats a status flip as a scope QUESTION; unchanged rows carry forward untouched. | Re-minting everything duplicates or clobbers human edits; a removed `source_ref` is a question, not a decision. See **ADR-0045**. | Silent overwrite destroys human edits; auto-delete removes a requirement a source-side bug may have dropped; re-minting unchanged rows duplicates/renumbers the whole set. |

**Reuse boundary (recorded).** The deterministic readers are a degradable **fallback** —
the `_scripts` package drops into any cloned repo (stdlib only) and degrades to "paste the
rows" when no reader is wired — **never** a hard read-time dependency. Only three things
were authored fresh: the row-to-requirement prompt, the source-line format, and the
SharePoint halt branch. (The CSV adapter lives in a separate repo, out of scope here.)

**Uncertain (ingestion).** The choice of **sha256** specifically (vs another hash), the
GitHub-item de-dup keying on `content.number` per-repo rather than the global gh id, and
the exact locator grammars (`Sheet!A1:F1`, `para:N`, `line:N`, `item:<num>`, `csv!A1`) are
implemented consistently but their rationale is **not recorded** — confirm with maintainers.

### 3.8 Automation

Covered as invariant §2.3 (advisory, not gated; `CODEOWNERS` the one gate). Two
mechanical decisions to know before touching the Actions:

- **`check-shared-stub-drift` guards in-repo quoted copies only** (gloss → **ADR-0046**).
  Each skill *quotes* the canonical `_shared` block verbatim between `BEGIN/END` markers and
  the Action diffs each copy against the canonical file — quote-not-import because there is
  no read-time import in markdown that must run in any file-reading workflow; see ADR-0046
  for the full why and the named duplication trade. **Operational rule:** edit the canonical
  `_shared/*.md` first, then re-quote into every skill in the same PR — never edit a quoted
  copy in place.
- **Multi-agent fan-out is an advisory option, capped at ≤4 concurrent** (gloss →
  **ADR-0047**). One independent model call per persona/section/objection/candidate for the
  ~10 reasoning-heavy skills; a failed call returns `None` and is never fatal. The cap is a
  legibility guard — *the specific number 4 is asserted, not derived from a recorded
  measurement* — and an orchestration framework was rejected ("one interface, one stub, one
  capped fan-out"). See ADR-0047.

---

## 4. Lessons & near-misses — the durable "why-not" record

These bugs were caught by **adversarial review passes** before they shipped. They are
recorded here so the same class of mistake is recognised next time. The reusable lesson
runs through all of them: **a mass change must own *every* file class, and an adversarial
grep/lint pass across all file types — including generated artefacts — is what catches the
near-miss.**

| Near-miss caught | The lesson it teaches |
|---|---|
| A **governance-gate BYPASS on a backward re-open** (carried over from the precursor tool): a backward reopen that did not re-arm the gate let work bypass it (open==0 passes). | A backward door (reopen / scope-change) must **re-arm** the governance gate (demote passed checks → pending), or it silently bypasses it. |
| A **pattern-key scheme that contradicted itself** across schema / linter / seeds — **0 of 3 seeds passed** before reconciliation. | A key scheme is a contract across *three* surfaces (schema, linter, seed examples); reconcile all three or none agree. This is part of why the canonical-key migration (§3.5) was done as a clean single scheme. |
| A **front-door map naming a numbering scheme that did not match the tree.** | The index and the on-disk tree are one artefact in two places; a rename touches both. (Part of why dynamic `category_dirs()` discovery — §3.1 — is load-bearing.) |
| **~12 skills citing reference files that were never authored.** | A cite is a promise; a reference-link lint must resolve every cited path against the on-disk tree. |
| **Lineage leaks left in pattern BODIES and the generated bundles** after a mass de-narration — *because no agent owned that file class.* | A mass change must enumerate **every** file class it touches — including `generated/` artefacts — and assign an owner to each. This is *the* recurring lesson. |
| An **ingest SILENT-EMPTY path**: a readable-but-empty source proceeding instead of halting — the exact failure the grounding rule forbids. | "I read nothing" ≠ "I cannot read this" ≠ "I proceeded on nothing." HALT-not-empty (§3.7) exists because this slipped through once. |
| A **grounding-lint BLIND SPOT** that let two author skills with required inputs escape the check. | A lint's *coverage* is itself a thing to adversarially test — "which skills with required inputs does this check NOT see?" |
| A **placeholder reference-implementation URL note** that was computed but **swallowed** on a passing file. | An advisory note that is computed must also be *surfaced*; a note swallowed on the happy path is a note that does not exist. |

---

## 5. Honest limitations — state these plainly

These are real and recorded; do not let a future change paper over them with false
confidence.

- **A static grounding lint cannot catch a model inventing an input at runtime.**
  `lint_skill_grounding.py` checks only that a skill cites the stub and wires a halt path.
  The contract + the halt exemplar are the *real* safeguard; the lint catches the
  documentation miss and the wiring miss, nothing more. (Stated in the script's own
  docstring and the skill.)
- **SharePoint ingestion is export-only**, by design, due to auth + stale-doc risk. There
  is no live connector and the HALT branch is the whole of SharePoint support.
- **Computed fields (`maturity`, `adoption_count`) are never authored** — they are
  arithmetic over `adoptions/ledger.jsonl`. A pattern cannot self-declare its track record.
- **Pattern-maturity recomputation depends on downstream projects appending their adoption
  line.** If they don't, the tally under-counts; an org-repo scan upgrade is deferred.
  (`DESIGN.md` §9.)
- **Advisory CI can let a malformed pattern merge** if a reviewer ignores a red check.
  `CODEOWNERS` is the single backstop; `validate-patterns` *may* be flipped to required for
  `patterns/**` only — the one reserved escape hatch. (`DESIGN.md` §9.)
- **`req_key` citation stability is unguarded.** Renaming/renumbering a key silently breaks
  every field that cites it; nothing enforces referential integrity but the lint and human
  review. (`trace-edge.md`.)
- **The deterministic base is allowed to be shallow.** The bar is only "a reviewer would
  accept the no-model output as a draft"; depth without a model is a known limitation, not a
  promise. (`deterministic-fallback.md`.)
- **Large surface area** is the named cost of the de-narrated, category-spread design;
  mitigated by MAP + the persona table + `meta/navigator`, not eliminated. (`DESIGN.md` §9.)
- **No vector index.** Skills read pattern/capability files directly — fine for tens of
  files, a known ceiling that needs an index Action at hundreds. Relevant to any future
  retrieval change to `recommend-component-patterns` / `derive-capabilities`. (`DESIGN.md` §9.)

---

## 6. Before you make a major change — guard table

If you are about to do something in the left column, read the invariant and section in the
right columns **first**. These are the changes most likely to dissolve a load-bearing
property by accident.

| Tempting change | Invariant it touches | Read first (§ + ADR) |
|---|---|---|
| Rename or re-number the skill folders | Named-as-purpose categories; bundle paths; map links | §3.1 · ADR-0009, ADR-0014 |
| Move `patterns/` or `capabilities/` under `skills/`, or rename them | The one structural gate (`CODEOWNERS` path-keyed) | §2.3, §3.1 · ADR-0003, ADR-0011 |
| Add a fifth output kind / let an agent emit a verdict, score, or RAG colour | TARGET RULE (§2.1) — the keystone | §2.1 · ADR-0001 |
| Make an Action blocking (or remove the `CODEOWNERS` gate) | Advisory-not-gated (§2.3) | §2.3, §3.8 · ADR-0003 |
| Let an agent merge its own PR, or persist a "ratified" status | Propose → ratify (§2.2) | §2.2 · ADR-0002 |
| Author a pattern/capability as pre-approved (`provisional`/`approved`/`proven`) | Human-only lifecycle; evidence-before-promotion | §2.3, §3.2, §3.3 · ADR-0016, ADR-0017, ADR-0027, ADR-0028 |
| Author `maturity` / `adoption_count` by hand | Code computes, models do not | §3.2 · ADR-0018 |
| Change or revert the canonical key scheme | One canonical scheme (panel dissent recorded) | §3.5 · ADR-0033 |
| Put parentage *in* a key (e.g. `TR-<outcome>.<n>`) | Trace via fields, never in the key (§2.6) | §2.6, §3.5 · ADR-0006, ADR-0033 |
| Switch `derives_from` / fulfilment edges to foreign keys | Portable citation; orphaning safety net | §2.6, §3.4 · ADR-0006, ADR-0032 |
| Remove or edit a quoted `_shared` block in place | Quote-not-import; drift guard | §3.8 · ADR-0046 |
| Make a skill's first step "ask the model" (no deterministic floor) | Deterministic base + model step (§2.5) | §2.5 · ADR-0005 |
| Name a concrete model/vendor in a skill | Provider-agnostic seam | §2.5 · ADR-0005 |
| Let an ingest read return empty on an unreadable/empty source | HALT-not-empty; grounding (§2.4) | §2.4, §3.7 · ADR-0004, ADR-0037 |
| De-dup ingest on the minted key instead of `source_ref` | Duplicate-under-a-new-key hazard | §3.5, §3.7 · ADR-0038 |
| Synthesise an acceptance criterion with no source locator | Lifted-vs-fabricated structural distinction | §3.7 · ADR-0041 |
| Wire a "start here" reference implementation into the promotion gate | Gate-bleed; evidence is the only promotion door | §3.2 · ADR-0021 |
| Add a live SharePoint / live-board connector | Export-only; auth + stale-doc risk | §3.7, §5 · ADR-0039, ADR-0040 |
| Do a mass edit (de-narration, rename, vocab change) | Every-file-class ownership; adversarial grep pass | §4 |
| Present a static lint as a fabrication guarantee | Honest reach of the grounding lint | §2.4, §5 · ADR-0004, ADR-0034 |

---

*Canonical per-decision record: [`ADR.md`](ADR.md) — the numbered, status-tracked log of
immutable records `ADR-0001..N` that owns the why / alternatives / dissent for every
architectural decision this document indexes. Each invariant (§2), decision-record row (§3),
and guard-table entry (§6) cites the `ADR-NNNN` that owns its rationale; this doc carries
the cross-cutting synthesis (invariants, lessons, limitations, guard table) that the ADRs do
not. Evidence base: `ADR.md`, `README.md`, `DESIGN.md` (§1–9), `CONTRIBUTING.md`,
`.github/CODEOWNERS`, `.gitattributes`, the `skills/_shared/*.md` canonical stubs,
`skills/_contract/*` SKILLs, the `patterns/` and `capabilities/` schemas + linters, the
ingest `_scripts`, the commit history (`1bffad7`, `5877839`, `1d55b80`, `580e236`,
`c5ac713`), and the maintainers' internal design-deliberation notes ("the design doc", held
with the maintainers). Where a rationale is not recorded in any of these, this document says
so rather than inventing one.*
