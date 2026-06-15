# WCAG 2.2 Level AA — citable success-criterion reference list

This is the **fixed, closed vocabulary** for the `frontend-a11y-review` skill. Every
accessibility finding's `ref` field MUST be one of the `ref` ids below (or a
`component:<name>` ref). It is also a **manual audit checklist**: walk it criterion by
criterion against the surface under review to guarantee coverage and to run the review
with no LLM at all (the deterministic fallback).

Each entry covers Level A and AA success criteria from WCAG 2.2 that are checkable on a
typical web/app front-end. Where a criterion only applies to audio/video/timed content,
mark it `info` and not-assessable when no such content is present.

- **ref** — the stable citation id to put in a finding (`WCAG-<num>-<slug>`).
- **title** — the official-ish short name of the criterion.
- **test** — a one-line, do-this check the reviewer applies to the input.

## Severity rubric (advisory)

Severity is by **user impact**, not criterion number:

- **high** — a user relying on assistive tech is *blocked* or content is *unusable*
  (keyboard trap, unreachable control, primary text below contrast, form unlabelled).
- **medium** — significant friction or a class of users degraded (no visible focus,
  colour-only state, undersized targets, missing landmarks).
- **low** — minor or cosmetic, or affects a narrow/decorative case.
- **info** — not a problem: criterion not applicable to this input, or a neutral note
  for traceability.

---

## 1. Perceivable

| ref | title | test |
|---|---|---|
| `WCAG-1.1.1-non-text-content` | Non-text content (A) | Every image/icon/control conveying meaning has an accessible name (`alt`, `aria-label`, etc.); purely decorative images are hidden (`alt=""` / `aria-hidden`). |
| `WCAG-1.2.2-captions` | Captions (prerecorded) (A) | Prerecorded video with audio has synchronised captions. (info if no media in input.) |
| `WCAG-1.2.4-captions-live` | Captions (live) (AA) | Live audio content has real-time captions. (info if no live media.) |
| `WCAG-1.2.5-audio-description` | Audio description (prerecorded) (AA) | Prerecorded video provides audio description of meaningful visuals. (info if no media.) |
| `WCAG-1.3.1-info-and-relationships` | Info and relationships (A) | Structure conveyed visually (headings, lists, tables, label↔field) is also in the markup/semantics, not faked with styling. |
| `WCAG-1.3.2-meaningful-sequence` | Meaningful sequence (A) | DOM/reading order matches the intended reading order; CSS reordering doesn't scramble screen-reader sequence. |
| `WCAG-1.3.4-orientation` | Orientation (AA) | Content isn't locked to portrait or landscape unless essential. |
| `WCAG-1.3.5-identify-input-purpose` | Identify input purpose (AA) | Inputs collecting user info use appropriate `autocomplete` tokens / input purposes. |
| `WCAG-1.4.1-use-of-color` | Use of color (A) | Colour is never the *only* means of conveying info, state, or distinction (errors, required, status, links-in-text). |
| `WCAG-1.4.3-contrast` | Contrast (minimum) (AA) | Text contrast ≥ 4.5:1 (≥ 3:1 for large text ≥18.66px bold / ≥24px). |
| `WCAG-1.4.4-resize-text` | Resize text (AA) | Text can scale to 200% without loss of content or function and without horizontal scrolling. |
| `WCAG-1.4.5-images-of-text` | Images of text (AA) | Text is real text, not a picture of text (except logos / essential). |
| `WCAG-1.4.10-reflow` | Reflow (AA) | Content reflows to a 320px-wide viewport with no two-dimensional scrolling (except data tables etc.). |
| `WCAG-1.4.11-non-text-contrast` | Non-text contrast (AA) | UI component boundaries, states, and meaningful graphics have ≥ 3:1 contrast against adjacent colours. |
| `WCAG-1.4.12-text-spacing` | Text spacing (AA) | No loss of content/function when line-height, letter/word/paragraph spacing are increased to the AA metrics. |
| `WCAG-1.4.13-content-on-hover-focus` | Content on hover or focus (AA) | Hover/focus-triggered content (tooltips, popovers) is dismissable, hoverable, and persistent. |

## 2. Operable

| ref | title | test |
|---|---|---|
| `WCAG-2.1.1-keyboard` | Keyboard (A) | All functionality is operable by keyboard alone; no mouse-only controls. |
| `WCAG-2.1.2-no-keyboard-trap` | No keyboard trap (A) | Focus can move *into and out of* every component using the keyboard; no focus traps (modals especially). |
| `WCAG-2.1.4-character-key-shortcuts` | Character key shortcuts (A) | Single-character shortcuts can be turned off, remapped, or are active only on focus. |
| `WCAG-2.4.1-bypass-blocks` | Bypass blocks (A) | A skip link / landmarks let users bypass repeated blocks (nav) to reach main content. |
| `WCAG-2.4.2-page-titled` | Page titled (A) | The page/view has a descriptive, unique `<title>` / view title. |
| `WCAG-2.4.3-focus-order` | Focus order (A) | Tab order follows a logical, meaningful sequence that preserves meaning and operability. |
| `WCAG-2.4.4-link-purpose` | Link purpose (in context) (A) | Each link's purpose is clear from its text or immediate context (no bare "click here"). |
| `WCAG-2.4.6-headings-and-labels` | Headings and labels (AA) | Headings and labels describe their topic/purpose; heading hierarchy is sensible (no skipped levels without reason). |
| `WCAG-2.4.7-focus-visible` | Focus visible (AA) | A visible focus indicator is present for every keyboard-focusable element (no blanket `outline: none`). |
| `WCAG-2.4.11-focus-not-obscured` | Focus not obscured (minimum) (AA, new in 2.2) | When an element gets focus, it is not entirely hidden by sticky headers/footers or other overlapping content. |
| `WCAG-2.5.3-label-in-name` | Label in name (A) | A control's accessible name contains its visible label text (so voice control "click X" works). |
| `WCAG-2.5.7-dragging-movements` | Dragging movements (AA, new in 2.2) | Any drag operation has a single-pointer (tap/click) alternative. |
| `WCAG-2.5.8-target-size` | Target size (minimum) (AA, new in 2.2) | Interactive targets are ≥ 24×24 CSS px, or have adequate spacing / an equivalent. |

## 3. Understandable

| ref | title | test |
|---|---|---|
| `WCAG-3.1.1-language-of-page` | Language of page (A) | The page declares its language (`<html lang>`). |
| `WCAG-3.1.2-language-of-parts` | Language of parts (AA) | Passages in a different language declare their own `lang`. |
| `WCAG-3.2.1-on-focus` | On focus (A) | Receiving focus alone does not trigger an unexpected context change (no auto-submit on focus). |
| `WCAG-3.2.2-on-input` | On input (A) | Changing a setting/field value doesn't cause an unexpected context change unless the user was warned. |
| `WCAG-3.2.3-consistent-navigation` | Consistent navigation (AA) | Repeated navigation appears in the same relative order across views. |
| `WCAG-3.2.4-consistent-identification` | Consistent identification (AA) | Components with the same function are labelled/identified consistently. |
| `WCAG-3.3.1-error-identification` | Error identification (A) | Input errors are identified in text and the erroring field is described (not colour-only, not generic). |
| `WCAG-3.3.2-labels-or-instructions` | Labels or instructions (A) | Inputs have persistent labels/instructions (placeholder alone is not a label). |
| `WCAG-3.3.3-error-suggestion` | Error suggestion (AA) | When an error is detected and a fix is known, the suggestion is offered in text. |
| `WCAG-3.3.4-error-prevention` | Error prevention (legal/financial) (AA) | For legal/financial/data submissions, the action is reversible, checked, or confirmable. |
| `WCAG-3.3.7-redundant-entry` | Redundant entry (A, new in 2.2) | Info already entered in a process is auto-populated or selectable, not re-keyed (except where essential). |
| `WCAG-3.3.8-accessible-authentication` | Accessible authentication (minimum) (AA, new in 2.2) | Auth doesn't rely on a cognitive function test (e.g. remembering/transcribing) with no accessible alternative. |

## 4. Robust

| ref | title | test |
|---|---|---|
| `WCAG-4.1.2-name-role-value` | Name, role, value (A) | Every UI component exposes an accessible name, a correct role, and current state/value to assistive tech (custom widgets use proper roles / ARIA, not bare `<div>` click handlers). |
| `WCAG-4.1.3-status-messages` | Status messages (AA) | Status updates (toasts, validation, async results) are announced via roles/live regions without moving focus. |

---

## How to cite

- Put the `ref` id verbatim in a finding (e.g. `WCAG-2.4.7-focus-visible`).
- When the issue is really a reusable component's fault, you may instead use
  `component:<name>` (e.g. `component:date-picker`) so the fix lands on the component —
  but still name the breached criterion in the finding's message.
- Do **not** cite a `WCAG-x.y.z` id that is not in this file. If a criterion you need is
  missing, add it here via a human-reviewed PR rather than inventing the id.

## Using this list as the deterministic fallback

With no LLM available, run the review by hand: for each row, apply its `test` to the
surface, and where it fails, write a finding `severity — ref — message` using the
rubric above. The coverage is the list itself. This is the same checklist the LLM step
walks; the model just reasons about the harder, judgement-based criteria (focus order,
meaningful sequence, error suggestions, status messages) that a mechanical scan misses.

> Note: WCAG 2.2 added new criteria (2.4.11, 2.5.7, 2.5.8, 3.2.6 AAA n/a, 3.3.7, 3.3.8)
> and removed 4.1.1 Parsing. This list tracks the **2.2 AA** set; review its currency on
> the skill's `review_by` cadence and update via PR if W3C publishes a newer version.
