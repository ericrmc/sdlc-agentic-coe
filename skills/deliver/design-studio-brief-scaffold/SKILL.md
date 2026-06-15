---
name: design-studio-brief-scaffold
description: Scaffold a paste-ready design & branding brief for an external studio; capture a lean white-label brand baseline once and treat it as fixed constraints (reuse, don't re-derive); returned assets re-enter as references, not stored binaries. Use when handing UI/branding to an external design studio or design agent.
one_liner: Assemble a paste-ready design and branding brief for an external studio.
aliases: [design brief, branding brief, design studio handoff, UI design ask, brand guidelines brief, design agency brief, visual design brief, style guide request]
when_to_use: handing UI/branding to an external design studio or design agent
output_kinds: [proposal]
deterministic_fallback: the brand baseline + surfaces/deliverables section + studio prompt
suggested_tier: mid
neighbours: |
  Before: deliver/testing-brief-scaffold (the testing handoff scaffold).
  After: deliver/comparator-grounded-estimate (size the work against comparators).
---

# Design Studio Brief Scaffold

## Purpose

Assemble a clear, paste-ready **design & branding brief** for an external design studio (or design agent), so the people who do the professional design work get everything they need in one document — and nothing they don't.

This is a scaffold-and-handoff: the brief is assembled here, the studio does the professional design. The boundary is explicit:

- **The studio does the design.** Style guide, design tokens, key-surface mockups — that is their craft. The brief renders nothing.
- **The brief is a scaffold, not a deliverable.** It is a believable, project-aware starting point that the studio sharpens. It leads with open questions rather than pretending the design is decided.
- **Captured client brand is a FIXED constraint.** If the client already owns a brand (logo, palette, type, voice), capture it once into a lean *brand baseline* and treat it as a non-negotiable input. The studio **reuses** it; nobody **re-derives** it. Greenfield brands are the studio's to invent — owned brands are theirs to honour.
- **Returned assets re-enter as references, not binaries.** When the studio hands back a style guide / token file / mockups, the brief points at them (repo links, design-tool URLs, file references). It pastes no images and stores no binaries; the brief stays a lean pointer document.

Keep it light and advisory. The brief is a clear ask, not a contract enforced against the studio's output.

## When to use

Use this skill when UI, visual design, or branding is about to be handed to an **external** design studio or a design agent, and a single paste-ready brief is needed that:

- captures the client's white-label brand once and freezes it,
- states the surfaces and deliverables expected back,
- carries a fenced **studio prompt** that copies straight into the studio's intake (or into a design agent),
- and routes returned assets back in as references.

Do **not** use it to do the design directly, to produce mockups, or to approve the studio's work. This is the handoff, not the studio.

## Inputs

Supply whatever of the following you have. Thin inputs are fine — the brief will honestly say what is missing rather than invent it.

| Input | What it is | Notes |
|---|---|---|
| **Project title** | The name of the thing being designed | Required; used throughout. |
| **Intake / one-breath summary** | What the project is, in a sentence or two | "The project, in one breath." If absent, the brief says so. |
| **Brand baseline** | The client's white-label brand: name, voice/intent notes, and key tokens (logo, palette, type, do/don't) | See `references/brand-baseline.template.md`. If the client owns a brand, capture it here **once** and treat it as fixed. If empty, the project is greenfield branding until a brand is set. |
| **Accepted outcomes** | The "what we're building" bullets (business outcomes / accepted scope) | Optional. Gives the studio context for *why* the surfaces exist. |
| **Panel synthesis** | Any prior deliberation/red-team notes that should shape the brief | Optional. Folded in as "From the panel." |
| **Target surfaces** | Web / mobile / both, and the key screens | Optional. If absent, you ask the studio in the open questions. |

Supply these as markdown or a short context blob. Read what is relevant and ignore the rest.

## The method (steps)

The method has a **deterministic base** (Steps 1–4) that always runs and always produces a usable brief, and a **model enrich step** (Step 5) that sharpens the prose without changing the facts. The base assembles the scaffold; the model step sharpens it and falls back to the base on any error.

### Step 1 — Lead with open questions (deterministic)

Open the brief with the questions the studio must answer before it can start. Surface the unknowns first; do not bury them. Generate these from what is **missing or ambiguous** in the inputs, e.g.:

- No client/white-label brand captured yet → "Set the brand baseline before handing off, or confirm this is greenfield branding."
- No accepted outcomes → "The 'what we're building' section will be thin — confirm scope with the studio."
- Surfaces not stated → "Confirm target surfaces (web / mobile / both) and the key screens."
- Otherwise → "None flagged. Confirm scope + non-negotiables below with the studio."

These are questions to be *raised*, not silently resolved.

### Step 2 — Capture the brand baseline once, freeze it (deterministic)

Render the **Brand baseline (white-label)** section from the captured brand:

- If a brand is present: list the brand/client name, voice/intent/constraint notes, and each captured detail (palette, type, logo usage, do/don't). End with the standing instruction: **reuse, do not redesign** any brand the client already owns — treat the baseline as fixed constraints.
- If no brand is present: state honestly that this is **greenfield branding until a brand is set**, and the studio has latitude to invent.

The baseline is captured **once**. On regeneration reuse it exactly — never re-derive or "improve" a client-owned brand.

### Step 3 — Render the surfaces & deliverables section (deterministic)

Render the body section that does not depend on the model:

- **The project, in one breath** — the intake summary (or an honest "no intake description" line), plus the accepted-outcomes bullets if present.
- **Surfaces & deliverables expected** — name the concrete asks: a **style guide**, a **design-token set**, and **key-surface mockups** (web / mobile as applicable). State that returned assets re-enter as **references** (repo links / pointers), not stored binaries.

### Step 4 — Emit the paste-ready studio prompt (deterministic)

Emit a fenced **studio prompt** the user can copy straight into a design studio's intake or a design agent. It must:

- name the project,
- instruct the studio to treat the brand baseline as **fixed constraints** (reuse, don't re-derive),
- ask for the style guide + token set + key-surface mockups,
- and tell the studio to **raise the open questions, not silently resolve them**.

Keep it self-contained: someone pasting only the fenced block should still have a coherent ask.

### Step 5 — Model enrich pass (reasoning step, keeps the brand baseline)

Now sharpen. Take the deterministic scaffold from Steps 1–4 and enrich it into clear, professional, paste-ready prose. While enriching, you **must**:

- **Stay grounded.** Keep every fact in the scaffold. Do **not** invent brand details, colours, type, or client facts that were not captured.
- **Preserve the brand baseline exactly.** It is a fixed constraint; enrich the framing *around* it, never the brand itself.
- **Keep open questions leading** and the studio prompt paste-ready.
- **Fold in panel synthesis** if present, under a "From the panel" heading, as shaping context.

If anything goes wrong in this step — missing model, error, garbled output — **fall back to the deterministic scaffold from Steps 1–4**. The scaffold alone is a complete, shippable brief. The model step only makes it sharper, never load-bearing.

## Output format

The user gets back a single markdown brief. Concrete template:

```markdown
# Design & branding brief — {title}

> A scaffold to hand to a **design studio** (or design agent). The studio does the
> professional work — style guide, tokens, mockups. You do no rendering; returned
> assets re-enter as references, not stored binaries.

## Open questions (read first)

- No client/white-label brand captured yet — set the brand baseline below before handing off.
- Confirm target surfaces (web / mobile / both) and the key screens.
- _(or)_ None flagged. Confirm scope + non-negotiables below with the studio.

## Brand baseline (white-label)

- **Client / brand:** Northwind Health
- **Intent / voice / constraints:** Calm, clinical, trustworthy; avoid playful/consumer tone.
- **Palette:** #0B3D5B primary, #5BB8A5 accent, #F4F6F8 surface (client-owned — fixed).
- **Type:** Inter for UI, Source Serif for long-form (client-owned — fixed).
- **Logo:** wordmark only; clear-space = cap height; never recolour.
- **Reuse, do not redesign** any brand the client already owns; treat the above as fixed constraints.

## The project, in one breath

A white-label patient-intake portal for Northwind's outpatient clinics.

**What we're building (accepted outcomes):**
- `BO-1` Patients complete intake before arrival, reducing front-desk time.
- `BO-2` Clinicians see a structured summary on open.

## Surfaces & deliverables expected

- A **style guide** + a **design-token set** + **key-surface mockups** (web + mobile).
- Key surfaces: intake form, patient dashboard, clinician summary view.
- Returned assets re-enter via reference — we store **pointers** (repo links / design-tool URLs), not binaries.

## Studio prompt (paste into a design studio or design agent)

```
Design the brand-aligned UI for the Northwind Health patient-intake portal. Treat the
brand baseline above as FIXED constraints — reuse, do not re-derive the client's brand
(palette, type, logo are client-owned). Deliver a style guide, a design-token set, and
mockups for the key surfaces (intake form, patient dashboard, clinician summary), web and
mobile. Raise the open questions above — do not silently resolve them. Return assets as
links/pointers we can reference.
```

## From the panel

_The convened panel / prior review shaped this brief:_ (folded in if present, else omitted.)
```

Note the nested fence: the **studio prompt** is itself a fenced block inside the brief so it copies cleanly as one unit.

## Notes / anti-patterns

- **Don't render.** If you find yourself describing exact pixel layouts, choosing the client's colours, or producing mockups, stop — that is the studio's job. You scaffold the ask.
- **Don't re-derive an owned brand.** A captured brand baseline is a fixed constraint. "Improving" or regenerating a client's palette/type/logo is the most common failure mode — reuse it exactly.
- **Don't invent brand facts.** If a colour, font, or voice was not captured, leave it as an open question for the studio, not a fabricated value.
- **Don't store binaries.** Returned assets come back as references (pointers). The brief stays a lean document; images and token files live where the studio put them, linked.
- **Don't bury the unknowns.** Open questions lead. A brief that reads as "everything is decided" sets the studio up to silently guess.
- **Don't enforce.** This is advisory. The brief is a clear, paste-ready ask — not an approval enforced against the studio's output.
- **Thin inputs are fine.** A sparse brief that honestly says "no brand captured — greenfield" is more useful than a padded one that invents constraints.

## References

- `references/brand-baseline.template.md` — the lean white-label brand baseline you capture **once** and treat as fixed.
