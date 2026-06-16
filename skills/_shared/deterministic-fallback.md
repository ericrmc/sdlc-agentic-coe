# Deterministic fallback — the no-LLM path + model-swap convention

> Shared convention. It applies to **every** skill in this repo.

Every skill runs **without a model first**: the LLM is enrichment, never a dependency, so the
skill works in a bare terminal with no key and a failed model call is never fatal. Rule of
thumb: if the model step were removed, the base should still produce something a reviewer
would accept as a *draft* — shallow is allowed, empty is not.

---

## The `deterministic_fallback:` frontmatter field

Every **skill** carries this field in its YAML frontmatter. It is a one-line, plain-English
statement of what the reader gets when no model is in play — the contract a reader can rely on.

```yaml
---
name: decompose-intake-to-outcomes
description: Derive business outcomes + child requirements from a raw intake brief.
deterministic_fallback: >
  Splits the intake into sentences, promotes each to a BO-<n> outcome, and stubs one
  REQ-<n> child requirement per outcome (derives_from: BO-<n>) from a fixed template.
  No model needed.
---
```

A good value is **concrete** (name the mechanism — split / regex / template / skeleton, not
"best-effort heuristics"), **honest about depth** (say so when shallow), and **one line** (if it
needs a paragraph the base is doing too much). A skill without this field is incomplete; the
frontmatter validator (see `.github/workflows/`) flags a missing/empty value on PR — advisory.

---

## How a skill body wires the two halves

Keep base and model as **separate, numbered steps** so a reader can stop after the base:

1. **(base)** Run the deterministic step — checklist / regex / template fill.
2. **(model, optional)** Hand the base's output to a model with a focused prompt to enrich,
   reorder, rewrite, or fill gaps.
3. **(merge)** Keep the model's output **only if** it validates against the skill's required
   fields / controlled vocabulary; otherwise keep step 1's output verbatim.

The merge step is where "never fatal" lives. Treat any of these as *use the base*:

- no model available (no CLI, no key, offline);
- the call errored or timed out;
- the reply did not parse, or was empty;
- the reply violated the skill's schema / controlled vocabulary (drop the bad item, keep the
  base's).

**Which model is also one line**, fixed precedence so deepening never means rewriting: global
pin → per-call override → the skill's default tier. A **tier hint** (`frontier` / `mid` /
`light`) is accepted anywhere a model reference is and resolved at call time — cheap skills
default small, authoring/synthesis large; swapping is editing one word. The swap names a
*tier*, not a vendor or model id, so any backend wires behind the same precedence.

---

## Worked example (shape only)

```text
Base (no model):
  - regex-split intake into sentences
  - promote each sentence → outcome `BO-1..n`
  - emit one child `REQ-<n>` per outcome (derives_from: BO-<n>) from the fixed template
  → usable draft, zero model calls

Model swap (optional, one line):
  - ask a `mid`-tier model to rewrite the outcomes as value statements and add up to
    3 real child requirements per outcome

Merge:
  - validate every returned req_key + type against the base's keys
  - keep model output if well-formed; else keep the base's draft
  - a per-outcome failure drops that item, never the whole run
```

---

## Anti-patterns

- **Model-only** — a first step of "ask the model" with no base floor behind it.
- **Fatal model step** — a failed/empty/malformed reply raising instead of falling back.
- **Unvalidated merge** — splicing model text in without checking required fields / vocabulary.
- **Hidden dependency** — a `deterministic_fallback:` claiming a no-LLM path the body lacks.
- **Vendor lock** — hard-coding a provider or model id instead of naming a tier.
