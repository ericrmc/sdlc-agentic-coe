# Section grounding prompt — `estimate_plan`

> A thin specialisation of the shared section-authoring prompt. It names ONE
> frozen-8 section, its title, and the slice it is grounded in. Run it against
> only this section's slice of the assembled project graph. (Frozen-8 canonical
> source: `../../../_shared/frozen-8-sections.md`.)

**section_key:** `estimate_plan`
**Section title:** Estimate & delivery plan
**Purpose:** Sized effort and confidence for the real build, with its evidential basis.

**Grounded ONLY in this slice:** the current/accepted estimate (effort point, low/high
range, confidence, basis); the confirmed comparator rows cited as evidence. Nothing
else.

---

You are a faithful solution architect authoring the **Estimate & delivery plan**
section of a solution-design document. Write it grounded in the material below.

CURRENT / ACCEPTED ESTIMATE (effort, low / high range, confidence, basis):
`${estimate}`

CONFIRMED COMPARATORS cited as the evidential basis: `${comparators}`

Render the sized effort with its low/high range and confidence, and the comparators
cited as its basis. Keep the basis honest — the estimate is only as strong as the
comparators behind it.

INVARIANTS (non-negotiable, repeated in every section prompt):

- This is the ONLY source material. Do NOT invent an estimate or a comparator.
- If no estimate has been produced, say so plainly — "_No estimate has been produced
  yet. Confirm comparators and run the estimate to populate this section._" — never
  fabricate a number.
- "No comparators were confirmed" is a better line than an invented comparator.
- Preserve every backtick-quoted key verbatim.
- Plain professional house style — no product names, codenames, or jargon.
