# The five deterministic checks

> The Step 1 deterministic floor of `reconcile-design-vs-requirements`. These are
> **pure functions of the text** — no model, no judgement, repeatable. They catch
> literal token mismatches; the semantic LLM pass (Step 2) catches the paraphrase /
> contradiction drift these structurally cannot see.
>
> Use **exactly** these five `check_kind` values and no others. Every finding is phrased
> as a **question** a human resolves. **Never** a verdict, never a status, never a
> pass/fail, never a merge gate.

Each check sets a specific `check_kind` and, where it has one, a `req_key` and/or
`section_key`. The eight `section_key`s are the frozen-8 (see
`../../_shared/frozen-8-sections.md`).

---

## 1. `outcome_no_design_coverage`

An outcome's `req_key` appears as a **literal token** in **no** current section body.

- Set `req_key` = the outcome's key; `section_key` = `null`.
- A freshly generated doc covers every outcome by construction, so in practice this is
  an **edit-drift guard**: it fires when a later edit dropped the reference.
- Question form: "Outcome `OUT-3` is not referenced in any current design section.
  Should the sections be regenerated or updated to cover it?"
- Evidence note: token "OUT-3" absent from all section bodies.

## 2. `requirement_no_acceptance_criterion`

A derived requirement has **zero** acceptance criteria.

- Set `req_key` = the requirement's key; `section_key` = `requirements_acceptance`.
- Question form: "Requirement `REQ-12` has no acceptance criterion. How will it be
  tested?"
- Evidence note: acceptance-criteria count = 0.

## 3. `nfr_unaddressed`

A pattern NFR or an NF requirement is **not reflected** in the `quality_nfrs` section
body: either its literal `req_key` is absent, or (for free-text NFRs) it has **fewer
than two keyword tokens** overlapping the section body.

- Set `req_key` = the NFR's key (`null` for a free-text pattern NFR);
  `section_key` = `quality_nfrs`.
- Question form: "NFR-1 (availability) does not appear to be reflected in the Quality
  attributes section. Is it addressed?"
- Evidence note: no keyword overlap between NFR text and the `quality_nfrs` body.
- (The two-keyword-overlap threshold is what the semantic pass exists to second-guess —
  an NFR addressed under different wording, e.g. "uptime and failover" for
  "availability", false-fires here and the LLM step reconciles it.)

## 4. `orphaned_requirement`

A requirement flagged as deriving from **no current outcome**
(`applies_status='orphaned'`).

- Set `req_key` = the requirement's key; `section_key` = `null`.
- Question form: "Requirement `REQ-7` derives from no current outcome. Should it be
  re-parented to an outcome, or retired?"
- Evidence note: `applies_status = orphaned`.

## 5. `section_stale`

A section whose **source data has changed since it was generated**.

- Set `section_key` = the section's key; `req_key` = `null`.
- **Under git, this check reads `git diff` / `git blame`, not a stored snapshot.** The
  original engine carried a persisted `generated_from` snapshot column (`{ids,
  max_version, count}` per source table) and diffed the live rows against it. **That
  persisted-staleness snapshot is dropped here** — in a git-backed CoE the question "did
  the data this section was built from change after the section was last written?" is
  answered directly by version control:
  - `git log -1 --format=%cI -- <section-file>` → when the section was last touched.
  - `git log -1 --format=%cI -- <requirements-source>` → when the source of truth last
    changed.
  - If the source moved **after** the section, the section is a candidate for
    `section_stale`.
  - `git blame` on the changed source lines shows *what* changed, to put in the
    question.
- Question form: "The requirements source was last changed in commit `a1b2c3d`
  (2026-06-12), after this section was last edited (2026-05-30). Should this section be
  regenerated to reflect the current requirements?"
- Evidence note: `git log` shows source changed after section; `git blame` attributes
  the change to the data-placement requirement.
- The semantic pass also raises a `section_stale` finding for a **cross-section
  contradiction** (two sections that cannot both be true) — the deterministic engine has
  no cross-section comparison, so that variant is the LLM step's alone.

---

## Dismissal memory (Step 3)

A finding's **identity is the tuple `(check_kind, req_key, section_key, message)`** — the
same dedup key the original engine uses. Because the message is derived from stable
handles (keys and item ids), not free text, it stays stable across a wording edit and
stays distinct between two items that share a handle. A finding the human already
dismissed against unchanged evidence is **not resurrected**. If the underlying evidence
changed (the message now reads differently because the data changed), it is a new finding
and may be raised.

## The hard rules

- **Never a verdict.** No "PASS", no "FAIL", no status column, no "blocks merge". If a
  sentence could be read as a ruling, rewrite it as a question.
- **Advisory, not a gate.** This produces a worklist. A CI job *may* run it and post the
  findings as a non-blocking comment, but it must not fail a build or block a PR.
- **Deterministic floor first.** Always run these five even when an LLM is available —
  they are the repeatable fallback and they make the semantic pass cheaper by
  pre-flagging the literal misses. If no model is available at all, these five are the
  whole skill.
- **Don't invent scope.** Only reference a `req_key` or `section_key` that appears
  verbatim in the inputs.
- **Stale = git, not a snapshot.** Do not reintroduce a persisted `generated_from`
  snapshot; cite the commit instead.
