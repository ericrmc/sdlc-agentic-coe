---
name: frontend-a11y-review
description: Review a front-end, component tree, or design draft and return a11y findings, each with a severity and a ref citing a fixed WCAG 2.2 AA success criterion from the shipped ref list (references/wcag-2.2-aa-refs.md); advisory only, never blocks.
one_liner: Accessibility-review a UI against WCAG 2.2 AA, citing fixed criteria.
aliases: [accessibility review, a11y audit, WCAG check, screen reader review, keyboard accessibility, contrast check, ADA review, inclusive design review]
when_to_use: a design review needs an accessibility lens (a named WCAG/a11y review)
output_kinds: [proposal, question, halt]
deterministic_fallback: the WCAG 2.2 AA success-criterion ref list as a manual audit checklist
suggested_tier: frontier
neighbours: |
  before: panel/design-review-findings — the broader design review whose accessibility pass this is
  after: architect/synthesise-solution-architecture — findings feed back into the durable design doc
---

# frontend-a11y-review

Review a running front-end, a component tree, or a design draft against WCAG 2.2 AA
and return accessibility findings, each citing a fixed success criterion. Advisory
only.

## Purpose

Produce a list of **accessibility FINDINGS** — observations a developer or designer
can act on, each carrying a severity and a citation. This is review, not a go/no-go:
it does **not** pass or fail the page, **not** certify conformance, and **not** block
a merge or a release. Surface what an experienced WCAG 2.2 AA auditor would flag,
citing the criterion that backs each call. A human triages.

Every finding cites a **fixed WCAG 2.2 AA success criterion** from the shipped
reference list (`references/wcag-2.2-aa-refs.md`), never a free-text ref.

The lens is narrow and concrete: can a person who relies on a keyboard, a screen
reader, a magnifier, voice control, or who has low vision or a cognitive disability
actually use this interface?

## When to use

- A broader design review needs an explicit accessibility pass (a named "design
  review (e.g. WCAG/a11y)").
- A new component or screen is being added to a pattern's reference build and you want
  the a11y evidence before it is PR-reviewed as a validated pattern.
- A design draft / wireframe / Figma export is being reviewed pre-build and you want
  accessibility caught at the cheap end.
- Anytime someone asks "is this accessible?" and you want a citeable, reproducible
  answer instead of a vibe.

Do **not** use this to certify legal conformance or to issue a VPAT — automated +
LLM review finds *candidates*, it does not prove conformance. Say so.

## Inputs

**At least one surface under review is *Required*** — any one (or a mix) of the
first three rows below. *If absent/unreadable/empty:* when **none** of a design
draft, a component tree, or a rendered surface is supplied, there is nothing to
audit — HALT and ask which UI to review (per `skills/_shared/grounding.md` /
`skills/_contract/grounding-no-absent-input`); never invent markup, components, or
a screen to flag a11y issues against. See step 0.

- **A design draft** — *Required (one of three).* The markdown/prose of the screen
  or flow under review.
- **A component tree** — *Required (one of three).* JSX/HTML/template source, or a
  description of the component hierarchy and its states.
- **A rendered surface** — *Required (one of three).* A screenshot, a DOM dump, an
  axe/Lighthouse export, or a description of what renders, plus the relevant markup
  if available.
- **Context** — *Optional* (useful) — the project title, who the users are, any
  assistive-tech the audience is known to use, the design system / token set in
  play. *If absent:* proceed; review the surface on its own terms — never invent an
  audience or a token set to cite.

If you are handed only a screenshot, that **is** a valid surface (do not halt):
review what is visibly checkable (contrast, focus order if shown, target size, text
scaling) and **mark the rest as not-assessable-from-this-input** as `info` rather
than guessing. Partial-but-present is named honestly, never patched (per the
contract). The halt is reserved for *no surface at all*.

## Grounding (quoted)

<!-- BEGIN grounding (byte-stable; do not edit a quoted copy — edit _shared/grounding.md) -->

**GROUNDING RULE — name the required inputs; an absent required input HALTs and asks, never assumes.**

A skill **names its required inputs** up front (its Inputs section marks each row Required or
Optional). Then:

- **A required input that is absent, unreadable, or empty becomes a `halt`.** The halt asks
  the user *where the input is*, offering the formats ingestion can read (an xlsx/csv path, a
  GitHub Project owner+number, a docs folder, or a pasted block). It then **stops and waits.**
  It never assumes, invents, or reasons over a hypothetical — no invented id, key, number, NFR,
  requirement, acceptance criterion, file path, or source row.
- **Partial input is named, not patched.** When some required inputs are present and others are
  not, the skill **names exactly what is missing and asks for it** — it never silently proceeds
  on the part it has, and it never back-fills the gap with a plausible-looking guess.
- **An absent *optional* input proceeds honestly.** It is surfaced as a `question` or recorded
  as an explicit null — never padded with invented content to look complete.

**"I read nothing" and "I cannot read this" are different outputs.** An unreadable or
unsupported source HALTs (it asks for a readable form); it never returns an empty result, because
a silent-empty reads downstream as "the source had nothing in it" — a silent-proceed failure.

**A halt is a question, never a verdict.** A halt names the missing input and asks where it is.
It never smuggles a finding, an assumption, or a disposition for a human to rubber-stamp — no
"I halt because this is infeasible / too risky / out of scope." Those are JUDGMENTs the human
owns. The halt carries only: *what is required, what is missing, and the formats it can be read
from.*

<!-- END grounding -->

Per `skills/_contract/grounding-no-absent-input`: a missing surface HALTs; a partial
surface (a screenshot alone) proceeds and marks the unassessable criteria as `info`.
Both are the contract's honesty rule — name the gap, never fabricate markup to fill
it.

## The method

The deterministic base is the **fixed reference list** in
`references/wcag-2.2-aa-refs.md`. It does double duty: it is the closed set of refs you
are allowed to cite, AND it is a runnable manual audit checklist. The model step is the
review itself. Both are advisory.

0. **Verify a surface is present (deterministic — the grounding halt).** Before loading the
   ref list, confirm at least one surface (a design draft, a component tree, or a rendered
   surface) was actually supplied — a file-level fact (absent / unreadable / empty) computed
   **before** any model reasoning, never a judgement on whether it "looks reviewable". If
   **none** is present, emit the clean HALT below and **stop** — do not invent markup or a
   screen to audit. A halt is a question, never a verdict.

   ```markdown
   HALT — required input missing.

   I can't run an accessibility review without a UI to review, and I won't invent markup
   to flag. Tell me where the surface is and I'll audit it against WCAG 2.2 AA.

   I can read any of these:
     • a design draft / wireframe of the screen or flow (markdown or prose)
     • a component tree (JSX / HTML / template source) or a description of the hierarchy
     • a rendered surface — a screenshot, a DOM dump, or an axe / Lighthouse export

   Where is the UI? (No findings are produced until you point me at a real surface.)
   ```

   A screenshot **alone** is a valid surface — proceed and mark the unassessable criteria as
   `info` (step 4); the halt is only for *no surface at all*. If a surface is present, continue.

1. **Load the fixed ref list (deterministic).** Read
   `references/wcag-2.2-aa-refs.md`. Every entry is a WCAG 2.2 Level AA success
   criterion with a stable `ref` id (e.g. `WCAG-1.4.3-contrast`), a short title, and a
   one-line test. This list is the **only** vocabulary you may put in a finding's
   `ref` field. If you cannot map an observation to one of these criteria (or to a
   named component, see step 5), it does not belong in this skill's output — note it
   as general design feedback for `panel/design-review-findings` instead.

2. **Walk the checklist against the input (deterministic / mechanical first).** Go
   criterion by criterion through the ref list and apply its one-line test to the
   supplied material. Some are mechanically checkable from the input alone (contrast
   ratios, missing `alt`, missing labels, `lang`, target size, page title). Treat this
   pass as the audit checklist — it guarantees coverage and stops the review from
   only reporting the first few obvious issues.

3. **Run the accessibility review (model step).** For each place the input violates,
   under-specifies, or risks a criterion, draft a finding. Reason as an auditor: trace
   the keyboard path, imagine the screen-reader announcement, check the focus order,
   ask whether state changes are perceivable without colour or motion. Stay within the
   material supplied — do not invent components, states, or content the input does not
   imply. Each finding is a concrete, actionable observation, not "improve
   accessibility".

4. **Stamp each finding (clamp and drop).** Apply these rules so a11y findings slot
   into the same downstream surface as design findings:
   - **severity** — clamp to exactly one of `high | medium | low | info`. Anything
     else (or empty) defaults to **`info`**. (`info` = a neutral note for
     traceability — e.g. "criterion N/A for this input" — not a problem.)
   - **ref** — must be a criterion id from the fixed list, OR the named component the
     finding is about (e.g. `component:date-picker`). If a finding has no ref,
     **drop it** — an a11y finding with no citation is exactly what this skill exists
     to prevent.
   - **message** — the observation and why it matters; **drop the finding if empty**.
   - De-dupe: one finding per (ref, target) — do not emit the same criterion against
     the same element twice.

5. **Citing.** Prefer the WCAG criterion id as the ref (it is the durable, portable
   citation). When the finding is really about a specific reusable component, you may
   cite `component:<name>` so the fix lands on the component, not the page — but still
   name the criterion it breaches in the message. Never invent a `WCAG-x.y.z` id that
   is not in the ref list.

6. **Map severity by user impact, not by criterion number.** A contrast miss on body
   text that nobody can read is `high`; a contrast miss on a disabled decorative label
   may be `low`. Blocking the keyboard path entirely (a focus trap, an unreachable
   control) is `high`. Use the severity rubric in the ref-list header.

## Output format

Return findings as markdown the user can paste into a review thread, an issue, or a
pattern's evidence file. Each finding is one bullet: **severity** — *ref* — message.
Group by severity, highest first. Lead with a one-line, explicitly-advisory framing.

```markdown
## Accessibility review (WCAG 2.2 AA lens) — advisory

Reviewed: Checkout — payment step (design draft v3). This is an advisory accessibility
review against WCAG 2.2 AA; it surfaces candidate issues for a human to triage and does
not certify conformance.

### High
- **high** — `WCAG-1.4.3-contrast` — The "Pay now" button uses #8AB4F8 text on a
  #FFFFFF fill at ~2.4:1; AA requires 4.5:1 for this text size. The primary action is
  effectively unreadable for low-vision users.
- **high** — `WCAG-2.1.1-keyboard` — The custom card-number field captures focus and
  the expiry field cannot be reached by Tab; keyboard-only users cannot complete the
  form (focus trap).

### Medium
- **medium** — `WCAG-4.1.2-name-role-value` — The "remove item" control is a `<div>`
  with a click handler and no role or accessible name; screen readers announce nothing
  actionable.
- **medium** — `WCAG-2.4.7-focus-visible` — Focus styling is removed globally
  (`outline: none`) with no visible replacement; sighted keyboard users lose their
  place.
- **medium** — `WCAG-2.5.8-target-size` — The quantity stepper buttons render at ~18px;
  AA minimum is 24×24 CSS px (or adequate spacing).

### Low
- **low** — `component:price-summary` — The discount line communicates "applied" with
  colour only (green text). Also satisfies the message of `WCAG-1.4.1-use-of-color`;
  add an icon or text marker.

### Info
- **info** — `WCAG-1.2.2-captions` — No audio/video in this draft; captions criterion
  is not assessable from this input.

_Severities are advisory; a human owner triages and decides what to fix._
```

If a structured form is needed (to feed another tool), the same data is a JSON array of
`{severity, ref, message}` objects — but the rules above still apply: clamp the
severity, require a ref from the fixed list (or `component:<name>`), drop empty
messages, drop missing refs.

## Notes / anti-patterns

- **Advisory.** No verdict, no pass/fail, no "blocks release". You produce findings; a
  human disposes.
- **Cite, or stay silent.** The discipline of this skill is the fixed ref list. A
  finding with no WCAG citation (and no named component) is dropped. If you keep
  wanting to flag something with no criterion behind it, that is general design
  feedback — route it to `panel/design-review-findings`, not here.
- **Do not invent criteria.** Only the ids in `references/wcag-2.2-aa-refs.md` are
  legal. If a real WCAG criterion you care about is missing from the list, propose
  adding it via PR (the list is human-reviewed) rather than citing an id that is not
  shipped.
- **Automated/LLM review finds candidates, not conformance.** Roughly a third to a half
  of WCAG failures are machine-detectable; the rest need human judgement and real AT
  testing. Never claim "WCAG AA conformant". Claim "reviewed against WCAG 2.2 AA; these
  are candidate findings".
- **Don't review what isn't there.** Stay within the supplied material — the
  no-fabrication rule of `skills/_contract/grounding-no-absent-input` applied to a present
  surface. If the input is a screenshot, say which criteria you could not assess and emit
  them as `info`, rather than hallucinating markup. No surface at all is the step-0 HALT.
- **Severity is impact, not pedantry.** Rank by who is blocked and how badly, not by the
  criterion's number or "how much it bugs you".
- **Keep the finding shape aligned with the design review.** This skill shares the
  `panel/design-review-findings` finding shape and clamp-and-drop rules so a11y
  findings and design findings render in the same place downstream. The only
  intentional divergence is the stricter missing-ref rule (drop, don't default).
