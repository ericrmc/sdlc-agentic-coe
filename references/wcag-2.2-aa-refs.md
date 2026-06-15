# WCAG 2.2 Level AA — Citable Success-Criterion Reference List

Fixed, stable reference list cited by the `frontend-a11y-review` skill so that
accessibility findings carry a **stable `ref` id** rather than free-text. This mirrors
the design-review convention where every finding cites a thing the reader can act on
(an NFR, a pattern, a design section). For accessibility, the cited thing is a WCAG
success criterion from this list.

**Target conformance level: WCAG 2.2, Level AA.** This list is the definitive set of
ref ids for the review skill. Treat the `ref` column as a stable identifier — do not
rename ids, even when the short title is reworded. New criteria are appended; ids are
never reused.

> How to use: when `frontend-a11y-review` raises a finding, it MUST set
> `ref` to one of the ids below (e.g. `WCAG-1.4.3-contrast-minimum`). The "Manual test"
> column is the quick, tool-free check a reviewer can run against the UI or component
> markup the user supplied. These are manual heuristics, not a substitute for an
> automated axe/Lighthouse pass — they are what a human reviewer eyeballs.

---

## Core AA success criteria (minimum set)

| ref | SC | Level | Short title | One-line manual test |
| --- | --- | --- | --- | --- |
| `WCAG-1.1.1-non-text-content` | 1.1.1 | A | Non-text content | Every informative image, icon-button, and chart has a meaningful `alt`/`aria-label`; purely decorative images have empty `alt=""` so screen readers skip them. |
| `WCAG-1.3.1-info-and-relationships` | 1.3.1 | A | Info and relationships | Structure conveyed visually is also in the markup — real `<h1..h6>`, `<table>` with `<th>`, `<label for>`/`<fieldset><legend>`, lists as `<ul>/<ol>`, not just styled `<div>`s. |
| `WCAG-1.4.3-contrast-minimum` | 1.4.3 | AA | Contrast (minimum) | Body text has ≥ 4.5:1 contrast against its background; large text (≥ 18.66px bold or ≥ 24px) has ≥ 3:1. Sample the lightest text on its actual background. |
| `WCAG-1.4.11-non-text-contrast` | 1.4.11 | AA | Non-text contrast | UI component boundaries and states (input borders, focus rings, toggle on/off, icon glyphs that carry meaning) have ≥ 3:1 against adjacent colours. |
| `WCAG-2.1.1-keyboard` | 2.1.1 | A | Keyboard | Every interactive element is reachable and operable with Tab/Shift+Tab/Enter/Space/arrows alone — no mouse-only controls, no custom widget you can't trigger from the keyboard. |
| `WCAG-2.4.3-focus-order` | 2.4.3 | A | Focus order | Tabbing moves through controls in a logical, meaningful order that matches the visual/reading order; modals trap and restore focus correctly. |
| `WCAG-2.4.7-focus-visible` | 2.4.7 | AA | Focus visible | The currently focused element always shows a clearly visible focus indicator; check nothing has `outline: none` without a replacement. |
| `WCAG-2.5.8-target-size-minimum` | 2.5.8 | AA | Target size (minimum) | Pointer targets are at least 24×24 CSS px, or have ≥ 24px spacing to neighbouring targets (inline-text and UA-default exceptions aside). |
| `WCAG-3.3.1-error-identification` | 3.3.1 | A | Error identification | When input validation fails, the field in error is identified in text (not colour alone) and the error message describes what went wrong. |
| `WCAG-3.3.2-labels-or-instructions` | 3.3.2 | A | Labels or instructions | Every form control has a persistent visible label (placeholder is not a label); required fields and expected formats are stated up front. |
| `WCAG-4.1.2-name-role-value` | 4.1.2 | A | Name, role, value | Custom/composite widgets expose correct role, accessible name, and current state to assistive tech (e.g. `role`, `aria-expanded`, `aria-checked`, `aria-selected`). |
| `WCAG-4.1.3-status-messages` | 4.1.3 | AA | Status messages | Dynamic status updates (toasts, "saved", inline validation summaries, live result counts) are announced via a live region (`aria-live`/`role="status"`) without moving focus. |

---

## Notes for the reviewer

- **Level shown for context.** Several ids above are Level A criteria. They are
  included because AA conformance *requires* meeting all A criteria too — an AA review
  that ignores A is incomplete. The overall target remains **WCAG 2.2 AA**.
- **2.2-specific additions.** `WCAG-2.5.8-target-size-minimum` and
  `WCAG-3.3.1-error-identification` (with 2.2's strengthened guidance) are the ones
  teams most often miss when moving from 2.1 to 2.2. Flag target-size on dense toolbars,
  icon rows, and table action menus.
- **Contrast is the most common real finding.** When citing
  `WCAG-1.4.3-contrast-minimum` or `WCAG-1.4.11-non-text-contrast`, name the specific
  element and, if known, the foreground/background hex pair so the finding is actionable.
- **Don't invent ids.** If a genuine issue doesn't map to any id here, raise it as a
  general design-review finding with a descriptive `ref` (e.g.
  `design-section:accessibility`) rather than minting a fake `WCAG-x.x.x` id.
- **Advisory.** These findings inform the team; they do not block. Pair them
  with an automated scan (axe-core / Lighthouse / Pa11y) and, for anything user-facing
  and high-risk, real assistive-tech testing (NVDA, VoiceOver, keyboard-only).

## References

- W3C, *Web Content Accessibility Guidelines (WCAG) 2.2*, W3C Recommendation —
  the normative success-criteria text these ids point at.
- W3C, *How to Meet WCAG (Quick Reference)* — filterable techniques and failures per
  criterion, useful when turning a finding into a fix.
- W3C, *Understanding WCAG 2.2* — per-criterion intent, exceptions, and the precise
  thresholds summarised in the manual-test column above.
