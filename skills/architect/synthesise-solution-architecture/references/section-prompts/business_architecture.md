# Section grounding prompt — `business_architecture`

> A thin specialisation of the shared section-authoring prompt. It names ONE
> frozen-8 section, its title, and the slice it is grounded in. Run it against
> only this section's slice of the assembled project graph. (Frozen-8 canonical
> source: `../../../_shared/frozen-8-sections.md`.)

**section_key:** `business_architecture`
**Section title:** Business architecture
**Purpose:** The accepted business outcomes and the commitments they represent.

**Grounded ONLY in this slice:** the outcomes (status, `req_key`, value statement);
a flag where an outcome has orphaned requirements hanging off it. Nothing else.

---

Author the **Business architecture** section of a solution-design document, grounded
only in the material below.

ACCEPTED OUTCOMES (status, key, value statement): `${outcomes}`

ORPHANED-SUBTREE SIGNAL (outcomes with requirements that derive from no current
outcome): `${orphan_signal}`

Render each accepted outcome as the commitment it represents, carrying its `req_key`
and status verbatim. Where an outcome carries an orphaned subtree, flag it plainly.

INVARIANTS (non-negotiable, repeated in every section prompt):

- This is the ONLY source material. Do NOT invent outcomes or commitments the
  material does not contain.
- If there are no woven outcomes, say so plainly — "_nothing recorded yet — no
  outcomes have been woven for this project._" — never fabricate.
- Preserve every backtick-quoted key verbatim.
- Plain professional house style — no product names, codenames, or jargon.
- Author **only** this section. Requirements & acceptance criteria are section 3's;
  do not duplicate them here.
