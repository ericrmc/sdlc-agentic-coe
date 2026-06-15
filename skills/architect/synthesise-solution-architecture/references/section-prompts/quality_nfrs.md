# Section grounding prompt — `quality_nfrs`

> A thin specialisation of the shared section-authoring prompt. It names ONE
> frozen-8 section, its title, and the slice it is grounded in. Run it against
> only this section's slice of the assembled project graph. (Frozen-8 canonical
> source: `../../../_shared/frozen-8-sections.md`.)

**section_key:** `quality_nfrs`
**Section title:** Quality attributes & NFRs
**Purpose:** The non-functional standards the build must hold — mostly inherited from
the adopted pattern.

**Grounded ONLY in this slice:** the adopted pattern's attached NFRs; any propagated
non-functional requirements (`req_type='NF'`) with their acceptance criteria. **This
is the ONLY home for NFRs.**

---

Author the **Quality attributes & NFRs** section of a solution-design document,
grounded only in the material below.

PATTERN-GOVERNED NFRs (the adopted pattern's attached NFRs): `${pattern_nfrs}`

PROPAGATED NON-FUNCTIONAL REQUIREMENTS (`req_type='NF'`, each with `req_key` and its
acceptance criteria): `${nf_requirements}`

Render the governed NFRs inherited from the pattern, then the propagated NF
requirements with their acceptance criteria, carrying every `req_key` verbatim. Use
the canonical NFR-kind vocabulary (hyphen form: `data-residency`, `audit-trail`, …)
as defined in `patterns/_schema/nfr-kinds.enum.txt` — do not coin synonyms.

INVARIANTS (non-negotiable, repeated in every section prompt):

- This is the ONLY source material. Do NOT invent NFRs or standards.
- **This is the single home for NFRs.** They must NOT also appear in
  `application_architecture` — that section carries pattern identity/topology only.
- If no NFRs are attached or propagated, say so plainly rather than inventing a
  standard.
- Preserve every backtick-quoted key verbatim.
- Plain professional house style — no product names, codenames, or jargon.
