# Section grounding prompt — `open_questions`

> A thin specialisation of the shared section-authoring prompt. It names ONE
> frozen-8 section, its title, and the slice it is grounded in. Run it against
> only this section's slice of the assembled project graph. (Frozen-8 canonical
> source: `../../../_shared/frozen-8-sections.md`.)

**section_key:** `open_questions`
**Section title:** Open questions & risks
**Purpose:** What is unresolved or carried as a known risk — never tidied away.

**Grounded ONLY in this slice:** orphaned requirements; deferred outcomes; pattern
overrides; open roadblocks; open requirement challenges; live risks & assumptions;
recorded scope expansions. Nothing else.

---

Author the **Open questions & risks** section of a solution-design document, grounded
only in the material below.

ORPHANED REQUIREMENTS: `${orphans}`
DEFERRED OUTCOMES: `${deferred_outcomes}`
PATTERN OVERRIDE (as a live trade-off): `${pattern_override}`
OPEN ROADBLOCKS: `${roadblocks}`
OPEN REQUIREMENT CHALLENGES: `${challenges}`
RECORDED SCOPE EXPANSIONS: `${expansions}`
LIVE RISKS & ASSUMPTIONS (RAID register): `${risks_assumptions}`

Surface every unresolved item plainly — orphans, deferrals, open roadblocks and
challenges, live risks and assumptions, recorded scope expansions. This section is the
home for anything that has no other home: do not tidy a tension away into silence.

INVARIANTS (non-negotiable, repeated in every section prompt):

- This is the ONLY source material. Do NOT invent risks or open items.
- If nothing is unresolved, say so plainly rather than manufacturing a concern.
- Preserve every backtick-quoted key verbatim.
- Plain professional house style — no product names, codenames, or jargon.
- This is the catch-all: a genuine item with no home in sections 1–7 belongs here as
  a carried item — never as a ninth section.
