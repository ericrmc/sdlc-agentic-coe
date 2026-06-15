# Section grounding prompt — `key_decisions`

> A thin specialisation of the shared section-authoring prompt. It names ONE
> frozen-8 section, its title, and the slice it is grounded in. Run it against
> only this section's slice of the assembled project graph. (Frozen-8 canonical
> source: `../../../_shared/frozen-8-sections.md`.)

**section_key:** `key_decisions`
**Section title:** Key decisions & trade-offs
**Purpose:** The genuinely contested calls — what was chosen, why, and the compromises
accepted.

**Grounded ONLY in this slice:** the ratified decisions (question, choice, rationale);
any pattern override recorded as an accepted trade-off. Nothing else.

---

You are a faithful solution architect authoring the **Key decisions & trade-offs**
section of a solution-design document. Write it grounded in the material below.

RATIFIED DECISIONS (question, choice, rationale): `${decisions}`

ACCEPTED TRADE-OFFS — pattern override (chosen alternative, reason), if any:
`${pattern_override}`

Render each ratified decision as the contested call it was: the question, the option
chosen, and the rationale for it. Record any pattern override as an accepted trade-off.

INVARIANTS (non-negotiable, repeated in every section prompt):

- This is the ONLY source material. Do NOT invent decisions or rationales.
- If no decisions have been ratified, say so plainly — "_No decisions have been
  ratified yet._" — never fabricate a decision to look thorough.
- An override's reason may legitimately appear here as an accepted trade-off AND in
  `open_questions` as a live trade-off where the material carries both senses; a plain
  fact otherwise has exactly one home.
- Preserve every backtick-quoted key verbatim.
- Plain professional house style — no product names, codenames, or jargon.
