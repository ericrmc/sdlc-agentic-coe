---
name: reconcile-design-vs-requirements
description: Advisory review of a solution-architecture doc against its source-of-truth requirements/outcomes/NFRs — five checks plus a semantic drift pass; every finding is a question; under git the stale-section check reads diff/blame; never blocks merge.
one_liner: Find where a design doc has drifted from its requirements.
aliases: [design drift check, design vs requirements review, requirements traceability, design coverage check, stale design sections, does the design still match, design consistency review]
when_to_use: checking a design doc still reflects its requirements after either side changed
output_kinds: [question, halt]
deterministic_fallback: the five deterministic checks (exact-token mismatches)
suggested_tier: frontier
neighbours: |
  Before: architect/synthesise-solution-architecture (authors the design doc this checks).
  After: architect/import-external-design (merge an external design back onto the doc).
---

# Reconcile design vs requirements

Find where a solution-architecture doc has drifted from its requirements, and surface
each drift as a question for a human to resolve.

## Purpose

A solution-architecture doc is a set of markdown **sections**. Its **source of truth** is
the project's requirements: business **outcomes**, the technical requirements derived from
them, the **non-functional requirements (NFRs)**, and the **acceptance criteria**. Over a
project's life either side moves — an outcome is added, a section is edited, an NFR is
inherited from a new pattern — and the two quietly drift apart.

This skill reads the design sections against the source of truth and surfaces **drift, gaps,
and contradictions as questions a human resolves**. Run it after either side changes.

One absolute rule:

> **PROPOSE and QUESTION. NEVER issue a verdict, a status, or a pass/fail.**

Every finding is phrased as an observation or a question ("... Is it addressed?", "Should it
be re-parented or retired?"). It never says "FAIL", never sets a status, never blocks a merge.
The human reading the findings decides what to do. This is advisory tooling.

The method has two layers that stay distinct:

- A **deterministic step** — five exact-token checks. Cheap, repeatable, no model, no
  judgement. These catch literal mismatches (an outcome key that appears in no section body,
  a requirement with no acceptance criterion).
- A **semantic step** — one reasoning pass that catches the **paraphrase / contradiction
  drift** the deterministic checks miss by construction (an outcome covered only by a
  reworded paragraph, an NFR addressed under different wording, two sections that contradict
  each other). The token checks only see literal matches, so this layer is where the real
  value is.

Run the deterministic step first; it is the floor and the fallback. Run the semantic step on
top; it is the reason a reviewer was asked.

## When to use

- A design doc has been written or regenerated and you want to confirm it still reflects its
  requirements.
- A requirement, outcome, or NFR changed and you want to know which sections went stale.
- A section was hand-edited and you want to check the edit did not drift from the source of
  truth.
- Before a handover / review, as an advisory worklist of "things a human should confirm".

Do **not** use it as a merge gate. Findings inform; they do not block.

## Inputs

The user supplies (paste, attach, or point at files):

1. **The design sections** — *Required.* The markdown solution-architecture doc, ideally with
   stable `section_key`s (e.g. `background_context`, `requirements_acceptance`,
   `application_architecture`, `quality_nfrs`, `key_decisions`, `estimate_plan`,
   `open_questions`). If the doc is one file, split it on its top-level headings; each heading
   is a section. *If absent/unreadable/empty: HALT and ask where the design doc is (per
   `_shared/grounding.md`); never invent a section to reconcile.* Readable forms: a markdown
   file, a docs folder, or a pasted block.
2. **The source of truth** — *Required (at least one of outcomes / requirements / NFRs
   present).* It is the requirements the design is checked against:
   - **Business outcomes** — each with a `req_key` and its text.
   - **Derived requirements** — each with a `req_key`, its text, and its acceptance-criteria
     count (or the criteria themselves).
   - **NFRs** — each with a `req_key` (where it has one) and its text; plus any NFRs the
     adopted pattern attaches.

   *If the entire source of truth is absent: HALT and ask where the
   outcomes / requirements / NFRs live (per `_shared/grounding.md`); never invent a `req_key`
   or a requirement to check the design against. There is nothing to reconcile a design with
   no source of truth.*
3. **Orphan signal** — *Optional.* Any requirement already flagged as deriving from no current
   outcome. *If absent: skip the `orphaned_requirement` check; never fabricate an orphan flag.*
4. **Under git** — *Optional (but preferred).* The repository, so the staleness check can read
   `git diff` / `git blame` instead of a stored snapshot. See the `section_stale` note below.
   *If absent: the `section_stale` check degrades to "cannot determine from git" — never
   invent a commit sha or an edit date.*

If a `req_key` or `section_key` is supplied, use it **verbatim** in findings. Never invent a
key that does not appear in the inputs — this is the no-fabrication keystone applied to keys
(see `skills/_contract/grounding-no-absent-input`).

## Grounding (quoted)

This skill reasons over requirements, outcomes, NFRs, acceptance criteria, and design
sections, so it carries the no-fabrication keystone — see
`skills/_contract/grounding-no-absent-input`. The existing "reason only about the supplied
material; never invent a `req_key` / `section_key` that is not in the inputs verbatim"
discipline is one **instance** of this contract.

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

## The method as numbered steps

### Step 0 — Locate / verify the required inputs (deterministic, pre-model)

Before running any check, confirm the Required inputs are present as a file-level fact: the
**design sections** and **at least one** of the source-of-truth kinds (outcomes /
requirements / NFRs). This is mechanical — absent / unreadable / empty — never a judgement on
"is there enough to reconcile."

- **Design sections absent/unreadable/empty** → emit the clean HALT below and stop.
- **The entire source of truth absent** → HALT and ask where the outcomes / requirements /
  NFRs live. (A design with no requirements to check against has nothing to reconcile — that
  is a halt, not an empty "no drift found" result.)

```
HALT — required input missing.

I can't reconcile a design against its requirements without both the design doc and the
source-of-truth requirements, and I won't invent either. Point me at the missing side and
I'll surface the drift — nothing is assumed until then.

I can read any of: a markdown file · a docs folder · an xlsx/csv path · a GitHub Project
(owner + number) · the rows pasted directly here. Which one, and where?
```

### Step 1 — DETERMINISTIC: the five exact-token checks

Run these first. They are pure functions of the text — no model, no judgement, repeatable.
Each check sets a specific `check_kind` and, where it has one, a `req_key` and/or
`section_key`. Use **exactly** these five `check_kind` values and no others.

The full definitions live in `references/five-checks.md`; the summary:

1. **`outcome_no_design_coverage`** — an outcome's `req_key` appears as a literal token in
   **no** current section body. Set `req_key` = the outcome's key; `section_key` = null.
   (A freshly generated doc covers every outcome by construction, so in practice this is an
   *edit-drift guard*: it fires when a later edit dropped the reference.)

2. **`requirement_no_acceptance_criterion`** — a derived requirement has **zero** acceptance
   criteria. Set `req_key` = the requirement's key; `section_key` = `requirements_acceptance`.

3. **`nfr_unaddressed`** — a pattern NFR or an NF requirement is **not reflected** in the
   `quality_nfrs` section body: either its literal `req_key` is absent, or (for free-text
   NFRs) it has fewer than two keyword tokens overlapping the section body. Set `req_key` =
   the NFR's key (null for a free-text pattern NFR); `section_key` = `quality_nfrs`.

4. **`orphaned_requirement`** — a requirement flagged as deriving from no current outcome
   (`applies_status='orphaned'`). Set `req_key` = the requirement's key; `section_key` = null.

5. **`section_stale`** — a section whose source data has changed since it was generated.
   Set `section_key` = the section's key; `req_key` = null.

   **Under git, this check reads `git diff` / `git blame`, not a stored snapshot.** Version
   control answers the question "did the data this section was built from change after the
   section was last written?" directly:
   - `git log -1 --format=%cI -- <section-file>` → when the section was last touched.
   - `git log -1 --format=%cI -- <requirements-source>` → when the source of truth last
     changed.
   - If the source moved **after** the section, the section is a candidate for `section_stale`.
   - `git blame` on the changed source lines shows *what* changed, to put in the question.

   State this in the output when you raise a `section_stale` finding ("the requirements file
   was last changed in commit `<sha>` after this section was last edited").

Emit one finding per tension. Every message must read as a question.

### Step 2 — LLM: the semantic drift pass

The deterministic step only sees literal tokens, so it is blind to meaning. This step is one
reasoning pass over the same material, looking for the drift the tokens miss. Reason about
**only the supplied material** — do not invent scope.

Look specifically for:

- **An outcome covered only by paraphrase** — the outcome's *intent* is clearly addressed in
  a section, but its `req_key` never appears, so the deterministic `outcome_no_design_coverage`
  check would false-fire (or, conversely, the key appears but the section's content actually
  addresses a *different* intent). Surface it as a question: "Outcome X seems to be covered by
  the second paragraph of Application architecture, but its key is not cited there — is X
  genuinely addressed, or is that paragraph about something else?"
- **An NFR addressed under different wording** — e.g. the NFR says "availability" and the
  quality section talks about "uptime and failover" without the word "availability". The
  token check sees no overlap and flags `nfr_unaddressed`; semantically it *is* addressed.
  Surface the reconciliation as a question.
- **A requirement with no genuinely testable criterion** — it has an acceptance criterion on
  paper, but the criterion is not actually testable ("works well"). The token check is
  satisfied; the meaning is not.
- **A contradiction between two sections** — two sections that, read together, cannot both be
  true (one section says data stays on-prem, another describes a cloud-hosted store). The
  deterministic step has no cross-section comparison; this is the semantic pass's job.
  Surface it as a `section_stale` finding against the section that contradicts the source of
  truth or the other section.

Use the **same five `check_kind` values** for semantic findings. Phrase every one as a
question. Only reference `req_key`/`section_key` values that appear verbatim in the inputs. If
everything is consistent, return no findings.

### Step 3 — Apply dismissal memory (do not re-nag)

If the user supplies a list of previously **dismissed** findings, do not re-raise any whose
identity matches. **Identity is the tuple `(check_kind, req_key, section_key, message)`.**
Because the message is derived from stable handles (keys and item ids), not from free text, it
stays stable across a wording edit and stays distinct between two items that share a handle. A
finding the human already dismissed against unchanged evidence is **not resurrected**. If the
underlying evidence changed (the message now reads differently because the data changed), it is
a new finding and may be raised.

### Step 4 — Assemble the worklist

Collect all deterministic + semantic findings, drop the dismissed ones, and present them as
the output below. Order them deterministic-first (they are the firm floor), then semantic
(they need a human eye). Nothing here is a verdict; it is a worklist of questions.

## Output format

Return a markdown worklist. Each finding is a question with its `check_kind`, the key(s) it
points at, and a short evidence note. Group by check, deterministic before semantic. Never a
status, never a pass/fail, never a merge verdict.

Concrete template:

```markdown
## Reconcile findings — <doc / project name>

_Advisory only. Every item is a question for a human to resolve, not a verdict._
_Deterministic checks: N · Semantic observations: M · Dismissed (unchanged): K_

### Deterministic findings

- **[outcome_no_design_coverage]** `req_key: BO-3`
  Business outcome BO-3 ("reduce onboarding time to under a day") is not referenced in any
  current design section. Should the sections be regenerated or updated to cover it?
  _Evidence: token "BO-3" absent from all section bodies._

- **[requirement_no_acceptance_criterion]** `req_key: REQ-12` · `section_key: requirements_acceptance`
  Requirement REQ-12 has no acceptance criterion. How will it be tested?
  _Evidence: acceptance-criteria count = 0._

- **[nfr_unaddressed]** `req_key: REQ-9` · `section_key: quality_nfrs`
  Requirement REQ-9 (classify: nfr, kind=availability) does not appear to be reflected in the
  Quality attributes section. Is it addressed?
  _Evidence: no keyword overlap between the requirement text and the quality_nfrs body._

- **[section_stale]** `section_key: application_architecture`
  The requirements source was last changed in commit `a1b2c3d` (2026-06-12), after this
  section was last edited (2026-05-30). Should this section be regenerated to reflect the
  current requirements?
  _Evidence: `git log` shows source changed after section; `git blame` attributes the change
  to the data-placement requirement._

### Semantic observations

- **[nfr_unaddressed]** `req_key: REQ-9` · `section_key: quality_nfrs`
  Requirement REQ-9 (classify: nfr, kind=availability) asks for "availability", and the
  Quality section discusses "uptime targets and failover" without using that word — so the
  token check above may be a false alarm. Is REQ-9 genuinely addressed by that wording?
  _Evidence: paraphrase, not literal match._

- **[section_stale]** `section_key: application_architecture`
  Application architecture states data stays on-prem, while Key decisions records a chosen
  cloud-hosted store. These two sections appear to contradict each other — which is current?
  _Evidence: cross-section contradiction; no deterministic check compares sections._
```

If everything reconciles, say so plainly — "No drift, gaps, or contradictions found against
the supplied source of truth." — and return an empty findings list. An empty result is an
honest, valid outcome.

## Notes / anti-patterns

- **Never a verdict.** The single hard rule. No "PASS", no "FAIL", no status column, no
  "blocks merge". If a sentence could be read as a ruling, rewrite it as a question. The human
  owns the disposition.
- **Advisory only.** This skill produces a worklist. It must not be wired to fail a CI
  job or block a PR. (A CI job *may* run it and post the findings as a non-blocking comment.)
- **Deterministic floor first.** Always run the five token checks even when an LLM is
  available — they are the repeatable fallback and they make the semantic pass cheaper by
  pre-flagging the literal misses. If no model is available at all, the deterministic five are
  the whole skill.
- **Don't invent scope.** Reason only about the supplied outcomes/requirements/NFRs/sections.
  Never reference a `req_key` or `section_key` that is not in the inputs verbatim. (An absent
  *required* input HALTs and asks rather than being invented — see
  `skills/_contract/grounding-no-absent-input`.)
- **Stale = git, not a snapshot.** Under version control the staleness question is answered by
  `git diff` / `git log` / `git blame` comparing when the section vs the source last changed.
  Cite the commit; do not keep a separate snapshot of the source data.
- **Respect dismissal memory.** Key it on `(check_kind, req_key, section_key, message)`. Don't
  re-nag a human about evidence they already looked at and dismissed and which has not changed.
  Derive the message from stable handles so the key survives a harmless rewording.
- **One fact, one place.** The checks assume each fact has exactly one home (an NFR is
  expected in `quality_nfrs`, nowhere else). If the doc duplicates a fact across sections, the
  `nfr_unaddressed` / coverage checks get noisier — note it, don't silently dedup.
- **Semantic pass is where the value is.** A reviewer is not needed to grep for a token. Spend
  the model budget on paraphrase coverage and cross-section contradiction — the things a
  token check structurally cannot see.

See `references/five-checks.md` for the verbatim definitions of the five deterministic checks.
