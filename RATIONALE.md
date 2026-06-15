# RATIONALE — why this library is shaped the way it is

> Companion to [`CONTRIBUTING.md`](CONTRIBUTING.md). `CONTRIBUTING.md` tells you
> *how* to add to the library; this file tells you *why* the architecture holds
> the shape it does, so you do not break a load-bearing decision by accident.

You are the agent (or the human directing one) about to make a change here. **Read
the section that touches your change before you make it.** A line that looks like a
one-liner — rename a folder, add an output kind, make a check blocking, set a status
on a pattern — can quietly dissolve the one property that lets an advisory library
be safe without gates. The decisions below record what each property is, *why* it
exists, what was considered instead, where a maintainer disagreed with a panel, and
**what breaks if you change it**.

This document obeys the same no-fabrication rule as the library: every "why" below is
evidenced in a file, a commit (`git log`), or the maintainers' design-deliberation notes
(referenced below as "the design doc" — an internal artefact held with the maintainers,
not shipped in this repo). Where a rationale is **not recorded anywhere**, it says so —
"rationale not recorded — confirm with maintainers" — rather than inventing one.

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
   first — it maps the tempting change to the invariant it touches.
2. Then read the matching **invariant (§2)** or **decision record (§3)**.
3. If your change weakens an invariant, that is not necessarily forbidden — but it
   *is* a deep change. Open it as a proposal, name the invariant in the PR, and let a
   human rule.

---

## 2. The load-bearing invariants

These are the few rules that must not be broken without deep understanding. They are
listed once in `DESIGN.md` §2; the *why* is expanded here.

### 2.1 The TARGET RULE — four output kinds, never a verdict

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
(`SKILL.md` lines 56–62 "Why an advisory library is safe without a blocking
mechanism".)

**Alternatives considered.** Enforcement/approval gates that block a downstream
project until a check passes (the prior tool's model) — rejected as heavyweight. A
fifth `recommendation` kind — explicitly rejected as "the most seductive smuggler", a
verdict in disguise; the legal move is an un-ranked `menu` plus cited proposal facts
(`SKILL.md` line 104).

**What breaks if you change it.** Add any output kind that can self-approve (a
verdict / score / RAG colour) and the *entire* rationale for being gate-free
collapses — an agent mistake would then flow into the design as authoritative fact,
the exact failure the rule dissolves. The library would then *need* a blocking
mechanism to stay safe.

### 2.2 Propose → ratify — the agent never ratifies its own work

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

### 2.3 Advisory, not gated — one structural human gate only

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

### 2.4 Grounding / no fabrication — an absent required input HALTs

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

### 2.5 Deterministic base + a one-line model step — never fatal

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

### 2.6 Trace via fields, never in the key — and projections, not persistence

**What it is.** Parentage and every relationship live in **fields** on the artefact
(`derives_from`, `fulfils_capability`, `fulfilled_by`, `supersedes`/`superseded_by`,
`contests`), never inside the key. `derives_from` is a **portable `req_key` citation**
(plain text, optionally a markdown link), not a foreign key — no database, no id, no
schema. Separately: rollups, RAG verdicts, release notes, and pattern-maturity tallies
are **recomputed on read or in an Action**, never stored as a field that can rot;
staleness is answered by `git diff` / `git blame`.
(`skills/_shared/req-key-conventions.md`; `skills/_shared/trace-edge.md`;
`DESIGN.md` §2 invariants 4–5.)

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

### 2.7 Anti-fatigue — delta-since-last-green, no throughput metric

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

## 3. Decision records

Grouped by area. Each: the decision, why, alternatives, any dissent / road-not-taken,
and what breaks.

### 3.1 Folder structure & navigation

| Decision | Why | What breaks if changed |
|---|---|---|
| **Looser *named* categories** (`ingest` / `understand` / `challenge` / `architect` / `panel` / `deliver` / `library` / `meta`), **not** a numbered scheme. | A developer rarely runs the whole method in one go and must find a skill *on its own*; names describe purpose so an agent finds a skill by intent. Numbers imposed a false fixed sequence the library rejects — "a map, not a track" (`MAP.md` View 2). Restructure recorded in commit `5877839` ("Looser categories (numbers dropped)"). | Renaming/re-numbering a category breaks every hardcoded part path in `skills/_scripts/bundles.yml` + `concat_skills.py` (the concat Action's `--check` fails and committed bundles go stale), every cross-link in `MAP.md`/`GETTING-STARTED.md`/`README.md`/`ENTRYPOINT.md`, and the named-as-purpose contract. The lint itself tolerates a rename (`category_dirs()` discovers dirs dynamically) — so the break is in human navigation + bundle paths, not lint legality. |
| **Underscore-prefixed machinery folders**: `_contract/`, `_shared/`, `_scripts/`. | Separates authoring machinery from the runnable product. `_contract/` = human-readable spec per convention; `_shared/` = the byte-stable quotable block skills paste in (what the drift check pins); `_scripts/` = the validators/concatenators Actions run (`DESIGN.md` §1, §5). | Renaming `_shared/`/`_contract/` breaks the drift-guard wiring (`check-shared-stub-drift` auto-discovers stubs via `SHARED_DIR.glob('*.md')`); renaming `_scripts/` breaks every Action step. Dropping the underscore makes the dir read as a runnable category and pollutes the map. |
| **`capabilities/` and `patterns/` are TOP-LEVEL trees**, siblings of `skills/`. | A different *kind* of asset with a different governance model and lifecycle. The load-bearing reason is the gate: `CODEOWNERS` keys the one hard gate off the path prefixes `/patterns/**` and `/capabilities/**` (last-match-wins). Top-level paths make that gate addressable (`.github/CODEOWNERS`; `DESIGN.md` §1, §6–7). | Moving them under `skills/` (or renaming) breaks the hard gate — the `CODEOWNERS` lines no longer match, so the one structurally-required human review silently disappears and pattern/capability changes fall under the advisory `/skills/**` route. Also breaks path-triggered Actions and every `fulfils_capability:`/`fulfilled_by:` cite. |
| **`generated/` bundles are committed; `portfolio-rollup.json` is gitignored.** | Committing the concatenated bundles lets an agent load **one** paste-able file (the Cursor/Codex wire-up in `GETTING-STARTED.md`). They are made non-noisy via `.gitattributes` (`linguist-generated -diff merge=ours`). `portfolio-rollup.json` is gitignored because it is a derived-on-read RAG projection (the projections-not-persistence invariant). (`.gitattributes`; `.gitignore`; `DESIGN.md` §4.) | Un-committing the bundles breaks the "paste one file" path for any agent that hasn't run the Action. Hand-editing `generated/` trips the concat `--check` (and `merge=ours` discards the edit on rebuild). Committing `portfolio-rollup.json` violates projections-not-persistence (a stored RAG score that rots). |
| **Both `skills/MAP.md` (full index) AND a thin root `ENTRYPOINT.md`.** | Two reader needs at two altitudes: `ENTRYPOINT.md` is a deliberately-thin front door naming only the two `meta/` skills (use vs contribute) + three deep links; `MAP.md` is the exhaustive catalogue *and* the navigator's deterministic fallback ("it reads them, never replaces them"). (`ENTRYPOINT.md`; `MAP.md` lines 15, 17, 27; `DESIGN.md` §1.) | Delete `ENTRYPOINT.md` and the "Start here" links dangle + the two-doors-by-intent affordance is lost. Delete `MAP.md` and no skill breaks ("every skill stands alone") *but* the navigator loses its deterministic fallback and the project-seed block disappears. |
| **A new top-level skill group is auto-legal** — adding `skills/ingest/` or `skills/meta/` needed no linter edit. | The scheme is intentionally **open**: `lint_map_links.category_dirs()` discovers first-level dirs under `skills/` dynamically (verified, `lint_map_links.py:106–116`). This is why `ingest` (`580e236`) and `meta` (`c5ac713`) slotted in without touching validators. | Hardcoding a category enum re-couples the open scheme to a linter edit. A new top-level dir that is *machinery* (not a category) must carry the underscore prefix or discovery treats it as a runnable category. |

**Dissent / honest cost (folders).** `DESIGN.md` §9 names "Large surface area" — the
de-narrated, category-spread library has a real discovery cost, mitigated by the MAP
table + the GETTING-STARTED persona table + `meta/navigator`; a "core 10" subset was
floated for a lighter first adoption but not built. *No source records a counter-argument
for nesting capabilities/patterns under skills/, nor for a fixed category enum — rationale
not recorded for those; confirm with maintainers.*

### 3.2 Pattern schema & lifecycle

| Decision | Why | What breaks if changed |
|---|---|---|
| **`pattern_key` (`PAT-<UPPER-KEBAB>`) is the stable cite-able id, deliberately NOT required to equal the filename stem.** | The key is what every bundle, retrieval, and supersede reference cites, so it must survive renames; decoupling lets the file be renamed for legibility without orphaning a citation (`note_filename()` records the pairing as a note, never an error). (`patterns/_schema/pattern.frontmatter.schema.json`; `lint_pattern_frontmatter.py`.) | Tying the key to the filename makes every rename change the key and orphan every reference that cited it. Loosening the regex breaks downstream skills that parse the key shape. |
| **`evidence[]` (proof it was BUILT) is REQUIRED once `approval_status` is `provisional` or `approved`** ("No evidence, no promotion"). | The library's value is fast-tracking reuse of shapes with a *real track record*; the gate protects credibility against a pattern minted from an imagined shape. (schema `allOf` conditional; `lint_pattern_frontmatter.check_conditional_rules`.) | Dropping the gate lets an unbuilt shape masquerade as blessed — downstream skills trust `provisional/approved` to mean "proven". Fabricating a link to fill the slot is explicitly forbidden ("leave it honestly empty"). |
| **`approval_status` is a closed, HUMAN-ONLY enum**: `candidate → provisional → approved → deprecated`. An agent only ever writes `candidate`. | `approval_status` encodes human **trust**, not a machine-derivable fact — "a human PR review is what blesses a pattern". "Writing `approved` is the single most damaging thing this skill could do." (schema; `patterns/README.md`; `author-component-pattern/SKILL.md`.) | If an agent could set `provisional`/`approved`, an unreviewed shape masquerades as blessed and the one human gate is bypassed. |
| **`maturity` and `adoption_count` are FORBIDDEN as authored input** (`{"not":{}}`) — COMPUTED from `adoptions/ledger.jsonl`. | "Maturity is arithmetic over the ledger." A pattern that calls itself battle-tested with zero adoptions is lying; computing it keeps "used in N engagements" honest and makes adopted-by-zero visible. The ledger even counts teams that *evaluated and chose otherwise* — non-adoption is signal. (`patterns/README.md`; `iter_ledger_records`.) | If authorable, a pattern self-declares "battle-tested" with no ledger behind it. The single shared ledger reader keeps the linter's never-delete invariant and the maturity tally consistent; bypassing it splits the two consumers' view of an adoption. |
| **`superseded_by` is REQUIRED when `deprecated`; staleness (`validity_check_months`, `sunset_at`) warns, never blocks.** | "Deprecate, never orphan" — a deprecated pattern must name its successor so adopters are never dead-ended. Staleness is "a soft caveat, not a hard exclusion" (the advisory posture). The companion rule: a pattern with a ledger adoption is *deprecated, not deleted* (`check_delete_invariant`), so provenance survives. | Hard-blocking on stale/sunset turns the advisory library into an enforcement gate. Dropping the `deprecated ⇒ superseded_by` rule dead-ends adopters. |
| **`attached_nfrs[]` each require `kind` + `statement` + `acceptance_criterion`** (`kind` from the closed 11-value NFR enum). | These are "the heart of the reuse payoff" — on adopt each becomes a derivable requirement downstream (via `propagate-pattern-nfrs`), with the `acceptance_criterion` copied unchanged. "An NFR with no way to verify it is a wish, not a bar." (schema; `lint_pattern_frontmatter.py`.) | Dropping the required `acceptance_criterion` lets unverifiable wishes propagate downstream as governed requirements. Opening the enum breaks downstream propagation/coverage skills that branch on the 11 values. |
| **`reference_implementations[]` is additive-OPTIONAL and held strictly OUT of the promotion gate.** | It answers a *different* question from `evidence[]`: evidence = "was this BUILT?" (gates promotion); a reference implementation = "what do I start FROM?" (a forward "start here" pointer). The sharpest hazard flagged was **gate-bleed** — wiring a working IaC repo into promotion — so the field is advisory only. A reference impl that *is* a real build must ALSO be listed under `evidence[]` (`kind:repo`), promoting "through the existing door, zero new gate logic". (design doc §6/Q1; commit `c5ac713`.) | Moving it into `check_conditional_rules`/`PROMOTED_STATUSES` lets a pattern be promoted on a forward link with no proof it was built — the gate-bleed failure the design guards against. The advisory-only contract is asserted in schema + linter + skill so a future contributor sees it in all three. |
| **The validator is deterministic, dependency-light** (PyYAML/jsonschema optional with a stdlib fallback) and **light/advisory about content**; it shares ONE ledger reader (`iter_ledger_records`) with the lifecycle workflow. | It must run on a bare runner with just `python3` ("ZERO mandatory third-party dependencies"), and it enforces only the structural contract — "it does not grade a pattern's quality"; content quality is the human reviewer's job. One shared reader keeps the never-delete invariant and the maturity tally reading the ledger identically. | Adding a hard dependency breaks the run-anywhere promise. Making the linter judge content turns advisory into a gate. Forking the ledger parsing splits the two consumers' view of an adoption. |

**Dissent / road-not-taken (patterns).** The design doc proposed a **six-value**
`reference_implementations[].kind` enum (`iac|app|notebook|scaffold|module|pipeline`)
plus optional `repo_path`/`scaffold_cmd`/`last_verified`; the shipped schema **narrowed
to four** (`iac|app|notebook|scaffold`) and dropped the extra `repo_path`/`scaffold_cmd`/
`last_verified` fields. The shipped sub-shape is `{kind, url, provisions}` required plus an
optional `notes` — where the CODEOWNER placeholder-URL caveat lives (the §4 near-miss). *The
why of the narrowing is not recorded in any commit; confirm with maintainers.* The specific numeric
bounds (`validity_check_months` default 12, min/max, length caps) are asserted, not
derived from a recorded measurement.

### 3.3 Capability schema & the requirements→components bridge

| Decision | Why | What breaks if changed |
|---|---|---|
| **Capabilities are first-class** — a `.md` tree PR-reviewed like patterns, sitting **between** requirements and patterns as the named middle term. | The pattern library answers "what shape did we build"; nothing answered "what *need* does a system have, and is there a proven shape for it yet". The need outlives the component that fulfils it, so a reader who can name a need in plain language but not the technology has an entry point. Chain: outcome ← requirement (`fulfils_capability`) ← capability (`fulfilled_by`) ← pattern. (`capabilities/README.md`; commit `5877839`; `derive-capabilities/SKILL.md`.) | Removing the layer re-opens the gap `derive-capabilities` closed: `recommend-component-patterns` STEP 0 *assumes* the `fulfils_capability` tag exists but no skill emitted it. The need would no longer be a technology-free, rename-surviving anchor. |
| **`capability_key` is `CAP-<UPPER-KEBAB>`, a distinct namespace.** | The citation target for every requirement that fulfils it and every pattern that back-references it — it must survive renames; parentage lives in fields, never the key. (schema; commit `1d55b80`.) | Renaming silently breaks every `fulfils_capability` cite, every pattern `fulfils` back-ref, and every INDEX row (key-citation, no foreign keys — nothing enforces integrity but lint + review). |
| **Bidirectional edges with link discipline**: capability cites `fulfilled_by:` (REQUIRED, minItems 1); pattern MAY cite `fulfils:` back (optional); requirement gains `fulfils_capability:` — all by key-citation, no foreign keys. | Key-citation keeps the library portable (markdown in git), human-auditable (PR diff), dependency-free. `fulfilled_by` is mandatory because a capability *must* name how (or whether) it is fulfilled; the back-ref is optional reader-convenience. | Making the back-ref mandatory forces a pattern edit on every capability authoring; dropping `fulfilled_by` removes the capability→component edge. Real foreign keys break the portable-markdown property the whole library rests on. |
| **The alias-searchable `INDEX.md` is the first entry point for a need-first reader** — each capability requires **≥2** unique lay-synonym aliases. | `capability_domain` is deliberately coarse; the **alias index, not the domain**, is how a non-expert finds a specific capability. "A capability with one alias is hard to find." (schema; `capability-domains.enum.txt`; `INDEX.md`.) | Dropping the ≥2 minimum or letting INDEX drift breaks findability *and* breaks `derive-capabilities`, whose legal `CAP-` key set IS the INDEX rows — a stale INDEX silently mis-routes MATCHED tags. `lint_capability_index` enforces the sync. |
| **Proven-vs-candidate lives in `fulfilled_by[].confidence`** (`proven` requires `pattern_key` + `evidence`; `candidate` carries `open_questions` and may name only a vendor in `note`). | Mirrors the pattern "evidence-required-once-promoted" rule — honesty is *enforced structurally*, not promised. "Do not read a candidate as a recommendation." (schema `allOf`; `capabilities/README.md`.) | Removing the `allOf` coupling lets a "proven" fulfilment exist with no `pattern_key`/evidence. `recommend-component-patterns` relies on this — an OPEN (candidate-only) capability routes to honest-empty rather than minting a pattern. |
| **No agent sets `confidence:proven` or advances `approval_status`** — promotion is a human PR. | Honours the propose-then-ratify, no-fabrication posture; the schema "only makes sure the reviewer has the fields they need". This is the one structural human review in an otherwise gate-free library. | If an agent could self-promote, a fabricated/unproven fulfilment presents as a recommendation with no human in the loop. |
| **`governance_nfrs` (minItems 1)** carry the minimum measurable bar, with `kind` drawn from the **same closed 11-kind NFR vocabulary** the patterns use. | The floor is what a human measures a candidate's spike result against; sharing the vocabulary keeps capability and pattern NFRs comparable. "A floor a reviewer cannot check is a wish, not a bar." | Diverging the NFR enum from `patterns/_schema/nfr-kinds.enum.txt` breaks the shared comparison; dropping `acceptance_criterion` makes the floor uncheckable (a spike "passed" on vibes). |
| **`derive-capabilities` (mid tier) emits two outputs**: MATCHED (`fulfils_capability` proposals resolving to a real INDEX row) and PROPOSED-NEW (an un-ranked menu of unnamed needs, each cited to its `req_key`, routed to `library/author-capability`). | It closes the one open edge. The legal `CAP-` set is the INDEX rows **fixed before reasoning**, so a MATCHED tag is always real and a PROPOSED-NEW need always cites a requirement *by construction* — making "never invent a capability not grounded in a requirement" **structural**, not a model promise. | If it invented `CAP-` keys or authored/promoted capabilities, the no-fabrication keystone and the human gate both break. If it didn't emit `fulfils_capability`, `recommend-component-patterns`' fast-path input disappears. |

**Uncertain (capabilities).** The choice of the *six* `capability_domain` values
(`data, compute, integration, runtime, experience, governance`) and the asymmetry
(`fulfils` optional vs `fulfilled_by` required) are stated as facts but the explicit
reasoning beyond "reader convenience vs load-bearing chain edge" is **not recorded** —
confirm with maintainers. Same for `validity_check_months` default 12.

**Frozen solution-architecture sections (closed set).** The eight solution-architecture
section keys in `skills/_shared/frozen-8-sections.md` are a closed, ordered set the
architect skills do not invent, rename, reorder, add to, or drop. **Why frozen:** one
source of truth, so the section a generator *emits*, a reconcile step *looks for*, and an
importer *maps onto* are the same eight in the same order. **What breaks:** renaming or
reordering a key silently desyncs `synthesise-solution-architecture`,
`reconcile-design-vs-requirements`, and `import-external-design`.
(`skills/_shared/frozen-8-sections.md`; `references/frozen-8-sections.md`.)

### 3.4 Accept-high / derive-low (the safety net under auto-derivation)

**Decision.** Humans ratify only the few genuine commitments (business outcomes, the
solution shape, contested calls); agents **derive and auto-apply** everything beneath,
each derived item carrying a `derives_from` citation back to its accepted upstream node.
(`propose-ratify-rhythm/SKILL.md` Step 2; `target-rule-output-kinds/SKILL.md` line 60
"derive-from-accepted-upstream"; `DESIGN.md` §2 invariant 4.)

**Why.** The human's attention is the scarce resource, spent only on load-bearing
commitments. Derive-low is **safe, not a bypass**, because of the trace edge (§2.6): a
derived row is structurally a proposal threaded to an *already-accepted* parent, so
rejecting an upstream outcome *visibly orphans* its derived subtree (a reconcile step
surfaces the dangling citations). That visible orphaning is what lets agents auto-derive
without a per-item human check.

**Alternatives.** A foreign-key edge — rejected (file-based library; the edge is a
plain-text citation). Per-item human acceptance of every derived requirement — rejected
as the fatigue failure the model exists to prevent.

**What breaks if you change it.** Emitting a derived (LOW) artefact without a
`derives_from` link, or threading it to an outcome never accepted ("orphan-blind
derivation"), removes the safety net — an agent's synthesis could then stand with no
human commitment above it.

### 3.5 Canonical req-keys & trace-via-fields

**Decision.** **One canonical scheme — exactly one prefix per kind**: `BO-<n>`
(business outcome), `REQ-<n>` (requirement, functional *or* non-functional — F/NF is
`classify` metadata, never in the key), `CAP-<SLUG>`, `PAT-<SLUG>`, `DEC-<n>`, and the
optional child key `AC-<REQ>.<n>`. Parentage and every relationship live in **fields**
(`derives_from` is the one trace edge). (`skills/_shared/req-key-conventions.md`; commit
`1d55b80`.)

**Why.** Six incompatible schemes were live across the skills (`BO-/TR-`, `F-/NFR-`,
`C-/O-/R-/P-/D-`, `OUT-/REQ-`, bare integers, `O-/R-`). The divergence "would have broken
provenance, the absent-input halt precondition, and re-ingest de-dup": ingest can't stamp
provenance to a stable key, a "HALT if no `O-*` keys" precondition fires spuriously on a
valid `BO-*` project, and re-ingest de-dup keys off a number that renumbers across schemes.

> **DISSENT — real, recorded.** A design panel **recommended the leaner route**: its
> synthesis (design doc line 43) favoured a **"bless-the-existing-set + one normalisation
> rule"** approach, *to avoid touching six skills' worked examples*. The
> maintainer **overrode** this at build time and chose a single canonical scheme + full
> migration (commit `1d55b80`) for long-term coherence — migrating every skill, worked
> example, reference, and the trace-edge block. Record both: the lean route was the panel's
> recommendation; the clean single scheme was the maintainer's call.

**The one normalisation rule.** Read the key scheme **from the target file; never assume
one** (kills a spurious halt — never argue a project out of its own valid keys). When a
source uses another prefix, normalise on write **and preserve the source's own identifier
verbatim as `source_ref`**, so a re-read de-dups on `source_ref`, not on a minted key that
renumbers across schemes.

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

Covered as invariant §2.4. The additional load-bearing decisions:

- **`halt` is the fourth output kind**, and the grounding contract carries the library's
  **first working halt exemplar**. `halt` was legal in the TARGET RULE but had zero
  exemplar (verified: all skills used only proposal/question/menu). Halt-first skills
  (ingest, navigator, feature intake) needed one reference shape so every halt looks the
  same and none drift into smuggling a verdict.
  (`grounding-no-absent-input/SKILL.md`; design doc line 30.)
- **Absent / unreadable / empty all map to the same halt**, computed as a file-level fact
  at STEP 0 before any model runs. The *empty* case matters most: a silent-empty reads
  downstream as "the source had nothing in it" — a silent-proceed failure. "I read nothing"
  and "I cannot read this" are deliberately different outputs.
- **A halt is a question, never a verdict** — it carries only what is required, what is
  missing, and the readable formats. The marked-WRONG counter-example invents
  `REQ-1/REQ-2/REQ-3`, an uptime NFR, a "4–8 days" estimate, and "looks infeasible" —
  "a halt that contains a finding is not a halt; it is a verdict with an apology attached".
- **Applied additively, not as a gate** — mark Inputs Required/Optional, quote the block,
  wire a STEP 0 halt path. "A halt is an advisory output kind: it stops this run and asks;
  the human supplies the input and re-runs. Nothing downstream is blocked."

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

| Decision | Why | What breaks if changed |
|---|---|---|
| **Split each ingest skill into a deterministic no-model read (locator + sha256) and a separate model map**; the `skills/ingest/_scripts/` readers are a non-authoritative, regenerable cache. | Keeping the read mechanical makes **lifted-vs-fabricated a structural fact**, not a model promise: a block carries a locator + sha256 of its own bytes, so a re-read proves the block unchanged and a minted requirement walks back to the exact span. The staged original is the source of truth. (`projection.py`; `_scripts/README.md` contract #1–2.) | If the reader becomes authoritative (or the read folds into the model step), the locator+sha256 can no longer prove a block unchanged, reingest-delta loses its deterministic diff floor, and AC provenance degrades from a structural fact to a model claim. |
| **Readers SKIP-never-raise** — a content problem returns `status="skipped"` + a reason, never throws ("Skip, never raise; halt, never empty"). | The calling skill needs a single, swallow-proof signal it can turn into a HALT; an uncaught raise either crashes the run or collapses "I cannot read this" vs "I read nothing". | If a reader raises, the skill can't reliably distinguish unreadable from empty, and the HALT-not-empty discipline collapses into a silent-empty or a crash. |
| **HALT-not-empty** — an unreadable OR readable-but-empty source HALTs; an empty requirement set is never a valid ingest output. | A silent-empty reads downstream as "the source had nothing in it" — the silent-proceed failure the grounding rule forbids. (The exact near-miss caught in review; see §4.) | A blank sheet / wrong tab / whitespace paste produces an empty-but-clean-looking requirement set that downstream skills treat as authoritative. |
| **Preserve the source's own id verbatim as `source_ref`; de-dup/diff on `source_ref` (content hash), never the minted key.** | The minted key renumbers across the library's incompatible schemes, so de-duping on it silently forks one source into two or drops a real new version. `block_source_ref()` = locator + sha256(block text). The design doc (Q4b) records this as the fix for a hazard `stage-and-fingerprint` *claimed* but did not cover (its fingerprint was on the source ROW, not the emitted KEY). | Keying de-dup on the minted key reintroduces the duplicate-under-a-new-key hazard (forks) or drops a genuine new version, on any project using more than one scheme — which the design verifies is the live state. |
| **GitHub Project: require a pinned, timestamped snapshot** (`gh project item-list --format json`), never a live board read. | A live board is as stale-prone as any export — a field rename silently remaps "acceptance", a column reorder shifts a locator. `ghproject.py` normalises gh's nondeterministic ordering so two pulls of an unchanged board hash identically; each item becomes its own one-row "sheet" so it rides the identical row-to-requirement path. | A live read makes the locator unstable: a rename/reorder silently remaps which cell an AC locator points at, so a lifted AC's provenance becomes a lie and reingest-delta diffs against a moving baseline. |
| **SharePoint is export-only** — never live-fetch; HALT asking for a local export, stamp `origin` + `exported_at` (or unknown) + a soft staleness-unverified caveat. | A live fetch is an auth + stale-doc hazard (design doc F5). The caveat is a **soft** carry, never a hard exclusion — a stale-prone source still ingests but its staleness is *visible* downstream rather than laundered away. | A live fetch reintroduces the auth surface and lets a 6-month-old doc ingest as a clean requirement with no caveat. |
| **Lift an acceptance criterion ONLY when a source locator backs it**; if absent, emit `Acceptance: — (absent in source; not synthesised)`. Never synthesise a GIVEN/WHEN/THEN. | Makes lifted-vs-fabricated a *grep-able* distinction. A synthesised AC is "the single most damaging fabrication this skill could make, because it reads downstream as a tested commitment". | Allowing synthesis makes a fabricated AC indistinguishable from a lifted one; downstream skills treat it as a real tested commitment and the grep-for-missing-locator check is defeated. |
| **Delegate controlled-vocab metadata to `classify-requirements`; do NOT inline classify's enums.** | The byte-stable drift check guards MARKED PROSE BLOCKS (quoted stubs), **not enum lists** — inlining classify's closed sets where nothing pins them means they silently drift. "One owner, cited — never a private copy." (Design doc resolved Q4's open question in favour of delegate.) | Inlining creates an unguarded second copy; when classify changes its sets, the ingest copy drifts undetected and the two skills annotate the same requirement with divergent vocab. |
| **`stage-and-fingerprint` vaults the bytes byte-untouched** (no re-encoding/trim); the vaulted copy is the source of record for every locator and diff. | Every locator and reingest-delta diff is relative to the vaulted original; mutating it on the way in silently invalidates every downstream locator and future diff. | Any normalisation shifts byte offsets, so existing locators point at the wrong span and reingest-delta diffs a cleaned copy against an uncleaned baseline. |
| **Identity binding is PROPOSED via deterministic signals** (content_hash exact, `source_ref` identity), model only as a tie-breaker for a renamed file; a renamed-file overlap is a QUESTION, never an auto-bind. | A wrong auto-bind drops a real version (under-count) or forks one source into two (the duplicate hazard) — so the human ratifies the binding. The hash IS the de-dup; the model is a tie-breaker, not the method. | Auto-binding a renamed file silently routes a new version to a fresh ingest (forking under new keys) or collapses two distinct sources into one. |
| **`reingest-delta` surfaces ONLY the delta** — never silently overwrites, never auto-deletes a removed row, treats a status flip as a scope QUESTION; unchanged rows carry forward untouched. | Re-reading and re-minting everything either duplicates the set under new keys or clobbers human edits made since the first ingest. A removed `source_ref` is a question (a source bug, not a decision). | Silent overwrite destroys human edits; auto-delete removes a requirement a source-side bug may have dropped; re-minting unchanged rows duplicates/renumbers the whole set. |

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

- **`check-shared-stub-drift` guards in-repo quoted copies only.** Each skill *quotes* the
  canonical `_shared` block (TARGET RULE, GROUNDING RULE, TRACE EDGE, req-key conventions)
  verbatim between `BEGIN/END` markers; the Action diffs each copy against the canonical
  file and fails if a byte drifts. **Why quote, not import:** this is markdown meant to run
  in *any* file-reading workflow — there is no read-time import, and a skill referencing a
  rule it does not contain ships broken when copied out alone. The trade is named in
  `DESIGN.md` §9: "Duplication is the price of zero-dependency portability… a skill copied
  out loses that [drift] guard." **Edit the canonical `_shared/*.md` first, then re-quote
  into every skill in the same PR — never edit a quoted copy in place.**
- **Multi-agent fan-out is an advisory option, capped at ≤4 concurrent.** One independent
  model call per persona/section/objection/candidate, for the ~10 reasoning-heavy skills; a
  failed call returns `None` and is never fatal — merge what succeeded. The cap is a
  mechanical rate-limiter / legibility guard so the human's review channel doesn't flood —
  *the specific number 4 is asserted, not derived from a recorded measurement*. Frameworks
  (LangGraph / agent SDK) were rejected: "one interface, one stub, one capped fan-out."
  (`parallel-agents/SKILL.md`; `DESIGN.md` §5.)

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

| Tempting change | Invariant it touches | Read first |
|---|---|---|
| Rename or re-number the skill folders | Named-as-purpose categories; bundle paths; map links | §3.1 |
| Move `patterns/` or `capabilities/` under `skills/`, or rename them | The one structural gate (`CODEOWNERS` path-keyed) | §2.3, §3.1 |
| Add a fifth output kind / let an agent emit a verdict, score, or RAG colour | TARGET RULE (§2.1) — the keystone | §2.1 |
| Make an Action blocking (or remove the `CODEOWNERS` gate) | Advisory-not-gated (§2.3) | §2.3, §3.8 |
| Let an agent merge its own PR, or persist a "ratified" status | Propose → ratify (§2.2) | §2.2 |
| Author a pattern/capability as pre-approved (`provisional`/`approved`/`proven`) | Human-only lifecycle; evidence-before-promotion | §2.3, §3.2, §3.3 |
| Author `maturity` / `adoption_count` by hand | Code computes, models do not | §3.2 |
| Change or revert the canonical key scheme | One canonical scheme (panel dissent recorded) | §3.5 |
| Put parentage *in* a key (e.g. `TR-<outcome>.<n>`) | Trace via fields, never in the key (§2.6) | §2.6, §3.5 |
| Switch `derives_from` / fulfilment edges to foreign keys | Portable citation; orphaning safety net | §2.6, §3.4 |
| Remove or edit a quoted `_shared` block in place | Quote-not-import; drift guard | §3.8 |
| Make a skill's first step "ask the model" (no deterministic floor) | Deterministic base + model step (§2.5) | §2.5 |
| Name a concrete model/vendor in a skill | Provider-agnostic seam | §2.5 |
| Let an ingest read return empty on an unreadable/empty source | HALT-not-empty; grounding (§2.4) | §2.4, §3.7 |
| De-dup ingest on the minted key instead of `source_ref` | Duplicate-under-a-new-key hazard | §3.5, §3.7 |
| Synthesise an acceptance criterion with no source locator | Lifted-vs-fabricated structural distinction | §3.7 |
| Wire a "start here" reference implementation into the promotion gate | Gate-bleed; evidence is the only promotion door | §3.2 |
| Add a live SharePoint / live-board connector | Export-only; auth + stale-doc risk | §3.7, §5 |
| Do a mass edit (de-narration, rename, vocab change) | Every-file-class ownership; adversarial grep pass | §4 |
| Present a static lint as a fabrication guarantee | Honest reach of the grounding lint | §2.4, §5 |

---

*Evidence base: `README.md`, `DESIGN.md` (§1–9), `CONTRIBUTING.md`, `.github/CODEOWNERS`,
`.gitattributes`, the `skills/_shared/*.md` canonical stubs, `skills/_contract/*` SKILLs,
the `patterns/` and `capabilities/` schemas + linters, the ingest `_scripts`, the commit
history (`1bffad7`, `5877839`, `1d55b80`, `580e236`, `c5ac713`), and the maintainers'
internal design-deliberation notes ("the design doc", held with the maintainers). Where a
rationale is not recorded in any of these, this document says so rather than inventing one.*
