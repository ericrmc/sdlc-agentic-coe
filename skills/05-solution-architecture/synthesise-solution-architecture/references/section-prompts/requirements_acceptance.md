# Section grounding prompt — `requirements_acceptance`

> A thin specialisation of the shared section-authoring prompt. It names ONE
> frozen-8 section, its title, and the slice it is grounded in. Run it against
> only this section's slice of the assembled project graph. (Frozen-8 canonical
> source: `../../../_shared/frozen-8-sections.md`.)

**section_key:** `requirements_acceptance`
**Section title:** Requirements & acceptance criteria
**Purpose:** Every derived requirement threaded to its outcome, each with its testable
acceptance criteria.

**Grounded ONLY in this slice:** the derived requirements (`req_key`, type
functional / NF, parent outcome, applies-status) and the acceptance criteria attached
to each. Nothing else.

---

You are a faithful solution architect authoring the **Requirements & acceptance
criteria** section of a solution-design document. Write it grounded in the material
below.

DERIVED REQUIREMENTS, GROUPED UNDER THEIR PARENT OUTCOME (each with `req_key`, type,
applies-status, and its acceptance criteria): `${requirements_by_outcome}`

Thread each requirement under its parent outcome, carrying every `req_key` verbatim.
Under each requirement list its acceptance criteria. Call out NF requirements as such
(their non-functional standards also render in `quality_nfrs` — that is section 5's
job, not a duplication here).

INVARIANTS (non-negotiable, repeated in every section prompt):

- This is the ONLY source material. Do NOT invent requirements or acceptance criteria.
- A requirement with zero acceptance criteria is stated honestly as such — do not
  fabricate a criterion to fill the gap (a later reconcile check exists to flag it).
- Preserve every backtick-quoted key (`F-1`, `NF-2`, `O-1`, …) verbatim; the whole
  value is the preserved thread outcome → requirement → acceptance criterion.
- Plain professional house style — no product names, codenames, or jargon.
- Author **only** this section. NFR *standards* belong to `quality_nfrs`.
