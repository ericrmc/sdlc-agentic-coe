---
name: reconcile-design-vs-requirements
description: Advisory review of a solution-architecture doc against its source-of-truth requirements/outcomes/NFRs — five checks plus a semantic drift pass; every finding is a question; under git the stale-section check reads diff/blame; never blocks merge.
when_to_use: checking a design doc still reflects its requirements after either side changed
output_kinds: [question]
deterministic_fallback: the five deterministic checks (exact-token mismatches)
suggested_tier: opus
---

# Reconcile design vs requirements

## Purpose

A solution-architecture doc is a set of markdown **sections**. Its **source of truth** is
the project's requirements: business **outcomes**, the technical requirements derived from
them, the **non-functional requirements (NFRs)**, and the **acceptance criteria**. Over a
project's life either side moves — an outcome is added, a section is edited, an NFR is
inherited from a new pattern — and the two quietly drift apart.

This skill reads the design sections against the source of truth and surfaces **drift, gaps,
and contradictions as questions a human resolves**. It is the assurance reviewer's pass over
the doc, run after either side changes.

It has one absolute rule, taken verbatim from the engine it is lifted from:

> **You PROPOSE and you QUESTION. You NEVER issue a verdict, a status, or a pass/fail.**

Every finding is phrased as an observation or a question ("... Is it addressed?", "Should it
be re-parented or retired?"). It never says "FAIL", never sets a status, never blocks a merge.
The human reading the findings decides what to do. This is advisory tooling, not a gate.

The method has two layers that have to stay distinct:

- A **deterministic step** — five exact-token checks. Cheap, repeatable, no model, no
  judgement. These catch literal mismatches (an outcome key that appears in no section body,
  a requirement with no acceptance criterion).
- A **semantic LLM step** — one reasoning pass that catches the **paraphrase / contradiction
  drift** the deterministic checks miss by construction (an outcome covered only by a
  reworded paragraph, an NFR addressed under different wording, two sections that contradict
  each other). The deterministic engine can only see literal token matches, so this layer is
  where the real value is.

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

1. **The design sections** — the markdown solution-architecture doc, ideally with stable
   `section_key`s (e.g. `background_context`, `requirements_acceptance`, `application_architecture`,
   `quality_nfrs`, `key_decisions`, `estimate_plan`, `open_questions`). If the doc is one file,
   split it on its top-level headings; each heading is a section.
2. **The source of truth**:
   - **Business outcomes** — each with a `req_key` and its text.
   - **Derived requirements** — each with a `req_key`, its text, and its acceptance-criteria
     count (or the criteria themselves).
   - **NFRs** — each with a `req_key` (where it has one) and its text; plus any NFRs the
     adopted pattern attaches.
   - **Orphan signal** (optional) — any requirement already flagged as deriving from no
     current outcome.
3. **Under git** (optional but preferred) — the repository, so the staleness check can read
   `git diff` / `git blame` instead of a stored snapshot. See the `section_stale` note below.

If a `req_key` or `section_key` is supplied, use it **verbatim** in findings. Never invent a
key that does not appear in the inputs.

## The method as numbered steps

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

   **Under git, this check reads `git diff` / `git blame`, not a stored snapshot.** The
   original engine carried a persisted `generated_from` snapshot column (`{ids, max_version,
   count}` per source table) and diffed the live rows against it. **That persisted-staleness
   snapshot is dropped here.** In a git-backed CoE the question "did the data this section was
   built from change after the section was last written?" is answered directly by version
   control:
   - `git log -1 --format=%cI -- <section-file>` → when the section was last touched.
   - `git log -1 --format=%cI -- <requirements-source>` → when the source of truth last
     changed.
   - If the source moved **after** the section, the section is a candidate for `section_stale`.
   - `git blame` on the changed source lines shows *what* changed, to put in the question.

   No snapshot column, no byte-for-byte snapshot recompute — just diff/blame. State this in
   the output when you raise a `section_stale` finding ("the requirements file was last
   changed in commit `<sha>` after this section was last edited").

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
  deterministic engine has no cross-section comparison; this is the semantic pass's job.
  Surface it as a `section_stale` finding against the section that contradicts the source of
  truth or the other section.

Use the **same five `check_kind` values** for semantic findings. Phrase every one as a
question. Only reference `req_key`/`section_key` values that appear verbatim in the inputs. If
everything is consistent, return no findings.

### Step 3 — Apply dismissal memory (do not re-nag)

If the user supplies a list of previously **dismissed** findings, do not re-raise any whose
identity matches. **Identity is the tuple `(check_kind, req_key, section_key, message)`** — the
same dedup key the original engine uses. Because the message is derived from stable handles
(keys and item ids), not from free text, it stays stable across a wording edit and stays
distinct between two items that share a handle. A finding the human already dismissed against
unchanged evidence is **not resurrected**. If the underlying evidence changed (the message now
reads differently because the data changed), it is a new finding and may be raised.

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

- **[outcome_no_design_coverage]** `req_key: OUT-3`
  Outcome OUT-3 ("reduce onboarding time to under a day") is not referenced in any current
  design section. Should the sections be regenerated or updated to cover it?
  _Evidence: token "OUT-3" absent from all section bodies._

- **[requirement_no_acceptance_criterion]** `req_key: REQ-12` · `section_key: requirements_acceptance`
  Requirement REQ-12 has no acceptance criterion. How will it be tested?
  _Evidence: acceptance-criteria count = 0._

- **[nfr_unaddressed]** `req_key: NFR-1` · `section_key: quality_nfrs`
  NFR-1 (availability) does not appear to be reflected in the Quality attributes section. Is
  it addressed?
  _Evidence: no keyword overlap between NFR text and the quality_nfrs body._

- **[section_stale]** `section_key: application_architecture`
  The requirements source was last changed in commit `a1b2c3d` (2026-06-12), after this
  section was last edited (2026-05-30). Should this section be regenerated to reflect the
  current requirements?
  _Evidence: `git log` shows source changed after section; `git blame` attributes the change
  to the data-placement requirement._

### Semantic observations

- **[nfr_unaddressed]** `req_key: NFR-1` · `section_key: quality_nfrs`
  NFR-1 asks for "availability", and the Quality section discusses "uptime targets and
  failover" without using that word — so the token check above may be a false alarm. Is NFR-1
  genuinely addressed by that wording?
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
- **Advisory, not a gate.** This skill produces a worklist. It must not be wired to fail a CI
  job or block a PR. (A CI job *may* run it and post the findings as a non-blocking comment.)
- **Deterministic floor first.** Always run the five token checks even when an LLM is
  available — they are the repeatable fallback and they make the semantic pass cheaper by
  pre-flagging the literal misses. If no model is available at all, the deterministic five are
  the whole skill.
- **Don't invent scope.** Reason only about the supplied outcomes/requirements/NFRs/sections.
  Never reference a `req_key` or `section_key` that is not in the inputs verbatim.
- **Stale = git, not a snapshot.** Do not reintroduce a persisted `generated_from` snapshot.
  Under version control the staleness question is answered by `git diff` / `git log` /
  `git blame` comparing when the section vs the source last changed. Cite the commit.
- **Respect dismissal memory.** Key it on `(check_kind, req_key, section_key, message)`. Don't
  re-nag a human about evidence they already looked at and dismissed and which has not changed.
  Derive the message from stable handles so the key survives a harmless rewording.
- **One fact, one place.** The checks assume each fact has exactly one home (an NFR is
  expected in `quality_nfrs`, nowhere else). If the doc duplicates a fact across sections, the
  `nfr_unaddressed` / coverage checks get noisier — note it, don't silently dedup.
- **Semantic pass is where the value is.** A reviewer is not needed to grep for a token. Spend
  the model budget on paraphrase coverage and cross-section contradiction — the things a
  deterministic engine structurally cannot see.

See `references/five-checks.md` for the verbatim definitions of the five deterministic checks.
