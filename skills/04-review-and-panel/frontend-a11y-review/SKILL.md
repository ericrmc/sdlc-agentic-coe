---
name: frontend-a11y-review
description: Review a front-end, component tree, or design draft and return a11y findings, each with a severity and a ref citing a fixed WCAG 2.2 AA success criterion from the shipped ref list (references/wcag-2.2-aa-refs.md); advisory only, never blocks.
when_to_use: a design review needs an accessibility lens (the brief's named WCAG/a11y review)
output_kinds: [proposal, question]
deterministic_fallback: the WCAG 2.2 AA success-criterion ref list as a manual audit checklist
suggested_tier: opus
---

# frontend-a11y-review

The accessibility lens of the review engine. This is the WCAG/a11y specialisation of
`design-review-findings`: same finding shape, same clamp-and-drop harness, same
advisory stance — but every finding must cite a **fixed WCAG 2.2 AA success
criterion** from the shipped reference list, not a free-text ref.

## Purpose

Review a running front-end, a component tree, or a design draft and return a list of
**accessibility FINDINGS** — observations a developer or designer can act on, each
carrying a severity and a citation. You are an accessibility reviewer, not a gate. You
do **not** pass or fail the page, you do **not** certify conformance, and you do **not**
block a merge or a release. You surface what an experienced WCAG 2.2 AA auditor would
flag, citing the criterion that backs each call. A human triages.

This mirrors the proven design-review behaviour (findings, not verdicts) but narrows
the lens to one thing: can a person who relies on a keyboard, a screen reader, a
magnifier, voice control, or who has low vision or a cognitive disability actually use
this interface?

## When to use

- A design review (the broader `design-review-findings` skill) needs an explicit
  accessibility pass — the brief's named "design review (e.g. WCAG/a11y)".
- A new component or screen is being added to a pattern's reference build and you want
  the a11y evidence before it is PR-reviewed as a validated pattern.
- A design draft / wireframe / Figma export is being reviewed pre-build and you want
  accessibility caught at the cheap end.
- Anytime someone asks "is this accessible?" and you want a citeable, reproducible
  answer instead of a vibe.

Do **not** use this to certify legal conformance or to issue a VPAT — automated +
LLM review finds *candidates*, it does not prove conformance. Say so.

## Inputs

The user supplies any one (or a mix) of:

- **A design draft** — the markdown/prose of the screen or flow under review.
- **A component tree** — JSX/HTML/template source, or a description of the component
  hierarchy and its states.
- **A rendered surface** — a screenshot, a DOM dump, an axe/Lighthouse export, or a
  description of what renders, plus the relevant markup if available.
- **Context (optional but useful)** — the project title, who the users are, any
  assistive-tech the audience is known to use, the design system / token set in play.

If you are handed only a screenshot, review what is visibly checkable (contrast,
focus order if shown, target size, text scaling) and **mark the rest as
not-assessable-from-this-input** rather than guessing.

## The method

The deterministic spine is the **fixed reference list** in
`references/wcag-2.2-aa-refs.md`. It does double duty: it is the closed set of refs you
are allowed to cite, AND it is a runnable manual audit checklist. The LLM step is the
review itself. Both are advisory.

1. **Load the fixed ref list (deterministic).** Read
   `references/wcag-2.2-aa-refs.md`. Every entry is a WCAG 2.2 Level AA success
   criterion with a stable `ref` id (e.g. `WCAG-1.4.3-contrast`), a short title, and a
   one-line test. This list is the **only** vocabulary you may put in a finding's
   `ref` field. If you cannot map an observation to one of these criteria (or to a
   named component, see step 5), it does not belong in this skill's output — note it
   as general design feedback for `design-review-findings` instead.

2. **Walk the checklist against the input (deterministic / mechanical first).** Go
   criterion by criterion through the ref list and apply its one-line test to the
   supplied material. Some are mechanically checkable from the input alone (contrast
   ratios, missing `alt`, missing labels, `lang`, target size, page title). Treat this
   pass as the audit checklist — it guarantees coverage and stops the review from
   only reporting the first few obvious issues.

3. **Run the accessibility review (LLM step).** For each place the input violates,
   under-specifies, or risks a criterion, draft a finding. Reason as an auditor: trace
   the keyboard path, imagine the screen-reader announcement, check the focus order,
   ask whether state changes are perceivable without colour or motion. Stay within the
   material supplied — do not invent components, states, or content the input does not
   imply. Each finding is a concrete, actionable observation, not "improve
   accessibility".

4. **Stamp each finding (the shared harness — identical to design-review-findings).**
   Apply the exact same clamp-and-drop rules the proven engine uses, so a11y findings
   slot into the same downstream surface as design findings:
   - **severity** — clamp to exactly one of `high | medium | low | info`. Anything
     else (or empty) defaults to **`info`**. (`info` = a neutral note for
     traceability — e.g. "criterion N/A for this input" — not a problem.)
   - **ref** — must be a criterion id from the fixed list, OR the named component the
     finding is about (e.g. `component:date-picker`). If a finding somehow has no ref,
     **drop it** — an a11y finding with no citation is exactly what this skill exists
     to prevent. (This is the one place the harness is *stricter* than the design-review
     parent, which defaults a missing ref to `design`. Here a missing/invalid ref is a
     drop, because the whole point is the citation.)
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
## Accessibility review (WCAG 2.2 AA lens) — advisory, not a gate

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

_Not a gate. Severities are advisory; a human owner triages and decides what to fix._
```

If a structured form is needed (to feed another tool), the same data is a JSON array of
`{severity, ref, message}` objects — but the harness rules above still apply: clamp the
severity, require a ref from the fixed list (or `component:<name>`), drop empty
messages, drop missing refs.

## Notes / anti-patterns

- **Advisory, never a gate.** No verdict, no pass/fail, no "blocks release". You produce
  findings; a human disposes. This is the same stance as the source `review_design`
  prompt ("produce FINDINGS … NOT verdicts … a human … disposes the gate") with the
  heavyweight gate stripped out — there is no gate here at all, only the human owner.
- **Cite, or stay silent.** The discipline of this skill is the fixed ref list. A
  finding with no WCAG citation (and no named component) is dropped. If you keep
  wanting to flag something with no criterion behind it, that is general design
  feedback — route it to `design-review-findings`, not here.
- **Do not invent criteria.** Only the ids in `references/wcag-2.2-aa-refs.md` are
  legal. If a real WCAG criterion you care about is missing from the list, propose
  adding it via PR (the list is human-reviewed) rather than citing an id that is not
  shipped.
- **Automated/LLM review finds candidates, not conformance.** Roughly a third to a half
  of WCAG failures are machine-detectable; the rest need human judgement and real AT
  testing. Never claim "WCAG AA conformant". Claim "reviewed against WCAG 2.2 AA; these
  are candidate findings".
- **Don't review what isn't there.** Stay within the supplied material. If the input is
  a screenshot, say which criteria you could not assess and emit them as `info`, rather
  than hallucinating markup.
- **Severity is impact, not pedantry.** Rank by who is blocked and how badly, not by the
  criterion's number or "how much it bugs you".
- **Reuse the harness.** This skill deliberately shares the design-review finding shape
  and clamp-and-drop rules so a11y findings and design findings render in the same place
  downstream. Keep them aligned; the only intentional divergence is the stricter
  missing-ref rule (drop, don't default).
