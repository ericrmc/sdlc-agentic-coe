# Section grounding prompt — `application_architecture`

> A thin specialisation of the shared section-authoring prompt. It names ONE
> frozen-8 section, its title, and the slice it is grounded in. Run it against
> only this section's slice of the assembled project graph. (Frozen-8 canonical
> source: `../../../_shared/frozen-8-sections.md`.)

**section_key:** `application_architecture`
**Section title:** Application & solution shape
**Purpose:** The adopted pattern *as* the solution shape: identity, topology, data
placement, and why it was chosen.

**Grounded ONLY in this slice:** the settled component/solution pattern (name,
summary, deployment topology, data placement); the selection rationale; any pattern
override. **Identity / summary / topology / provenance ONLY — no NFRs here.**

---

You are a faithful solution architect authoring the **Application & solution shape**
section of a solution-design document. Write it grounded in the material below.

ADOPTED PATTERN (name, summary, deployment topology, data placement): `${pattern}`

SELECTION RATIONALE: `${recommendation_rationale}`

PATTERN OVERRIDE (chosen alternative + reason), if any: `${pattern_override}`

Present the adopted pattern *as* the solution shape: its identity and summary, its
deployment topology, its data placement, and the provenance (why it was chosen). If a
pattern was overridden, state the chosen alternative and the reason.

INVARIANTS (non-negotiable, repeated in every section prompt):

- This is the ONLY source material. Do NOT invent topology, placement, or rationale.
- **Render NO NFRs here.** The pattern's attached NFRs are section 5 (`quality_nfrs`)
  alone — duplicating them here makes a later "is this NFR addressed?" check
  ambiguous.
- If no pattern is settled, say so plainly rather than inventing a shape.
- Preserve every backtick-quoted key verbatim.
- Plain professional house style — no product names, codenames, or jargon.
