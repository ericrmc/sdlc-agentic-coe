# Brand baseline template (white-label)

> The lean **white-label brand baseline** you capture **once** and treat as a **fixed
> constraint**. If a client already owns a brand (logo, palette, type, voice), capture it
> here once and hand it to the studio as a non-negotiable input. The studio **reuses** it;
> nobody **re-derives** it. On regeneration you reuse the baseline verbatim — you never
> "improve" a client-owned brand.
>
> If the client owns no brand, the project is **greenfield branding until a brand is
> set** — leave the fields as open questions for the studio to invent, not as fabricated
> values.
>
> Grounded in the source app's handoff brand shape (`name`, `notes`, `details`):
> `backend/app/services/handoff_agent.py`.

## The fields

| Field | What it is | Notes |
|---|---|---|
| **Client / brand name** | The white-label client whose brand this is | If empty → greenfield until set. |
| **Intent / voice / constraints** | The brand's tone and any standing do/don'ts in a sentence or two | The `notes`. E.g. "Calm, clinical, trustworthy; avoid playful/consumer tone." |
| **Palette** | Key colours, client-owned and fixed | Primary / accent / surface. Mark `(client-owned — fixed)`. |
| **Type** | Typefaces for UI and long-form | Mark `(client-owned — fixed)`. |
| **Logo** | Usage rules — wordmark/mark, clear-space, recolour rules | E.g. "wordmark only; clear-space = cap height; never recolour." |
| **Do / Don't** | Any explicit brand constraints to honour | Optional; capture only what the client stated. |

## The template

```markdown
## Brand baseline (white-label)

- **Client / brand:** <client name, or: _No brand captured — greenfield until a brand is set._>
- **Intent / voice / constraints:** <tone + standing do/don'ts, or omit if greenfield>
- **Palette:** <#primary, #accent, #surface — (client-owned — fixed)>
- **Type:** <UI face, long-form face — (client-owned — fixed)>
- **Logo:** <usage rule — e.g. wordmark only; clear-space = cap height; never recolour>
- **Do / Don't:** <any explicit constraints to honour>
- **Reuse, do not redesign** any brand the client already owns; treat the above as fixed constraints.
```

## Worked example

```markdown
## Brand baseline (white-label)

- **Client / brand:** Northwind Health
- **Intent / voice / constraints:** Calm, clinical, trustworthy; avoid playful/consumer tone.
- **Palette:** #0B3D5B primary, #5BB8A5 accent, #F4F6F8 surface (client-owned — fixed).
- **Type:** Inter for UI, Source Serif for long-form (client-owned — fixed).
- **Logo:** wordmark only; clear-space = cap height; never recolour.
- **Reuse, do not redesign** any brand the client already owns; treat the above as fixed constraints.
```

## Greenfield (no brand captured)

When no brand is present, the section is honest about it — the studio has latitude to
invent:

```markdown
## Brand baseline (white-label)

- _No brand captured. This is greenfield branding until a brand is set — the studio has
  latitude to invent a palette, type, and logo, and to propose a voice._
```

## The rules

- **Captured once, frozen.** A client-owned brand is a fixed constraint. "Improving" or
  regenerating a client's palette / type / logo is the most common failure mode — reuse it
  verbatim.
- **Don't invent brand facts.** If a colour, font, or voice was not captured, leave it as
  an open question for the studio, not a fabricated value.
- **Don't store binaries.** Returned assets (style guide, token file, mockups) re-enter as
  **references / pointers** (repo links, design-tool URLs), not pasted images or stored
  binaries. The brief stays a lean pointer document.
- **Light and advisory.** The baseline is a clear ask handed to the studio, not an approval
  you enforce against their output.
