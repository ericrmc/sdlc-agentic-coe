# Section grounding prompt — `background_context`

> A thin specialisation of the shared section-authoring prompt. It names ONE
> frozen-8 section, its title, and the slice it is grounded in. Run it against
> only this section's slice of the assembled project graph. (Frozen-8 canonical
> source: `../../../_shared/frozen-8-sections.md`.)

**section_key:** `background_context`
**Section title:** Background & context
**Purpose:** Why the project exists and what success means, in the sponsor's own words.

**Grounded ONLY in this slice:** the project title and description / intake text;
the targeted business outcomes (each with its `req_key` and value statement); any
outcomes still being settled, flagged as deferred. Nothing else.

---

Author the **Background & context** section of a solution-design document, grounded
only in the material below.

PROJECT TITLE: `${title}`

PROJECT DESCRIPTION / INTAKE: `${description}`

TARGETED OUTCOMES (with value statements): `${outcomes}`

OUTCOMES STILL BEING SETTLED (deferred): `${deferred_outcomes}`

Author a short "Why `${title}` exists" lead from the description, then a "Targeted
outcomes" list carrying every outcome `req_key` verbatim and its value statement,
then an "Outcomes still being settled" note for any deferred outcomes.

INVARIANTS (non-negotiable, repeated in every section prompt):

- This is the ONLY source material. Do NOT invent facts, outcomes, or context the
  material does not contain.
- If the material for this section is empty or thin, say so plainly — e.g. "_No
  intake description was recorded._", "_every outcome is accepted_" — never pad or
  fabricate.
- Preserve every backtick-quoted key (`O-1`, `F-2`, …) verbatim; traceability is
  the point.
- Plain professional house style — no product names, stage codenames, or internal
  jargon.
- Author **only** this section. Decisions, NFRs, estimates, and risks live in their
  own sections; do not pull them in here.
