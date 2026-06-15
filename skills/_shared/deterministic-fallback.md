# Deterministic fallback — the no-LLM path + model-swap convention

> Shared convention. It applies to **every** skill in this repo.

Every skill runs **without a model first**. The LLM is an *enrichment*, never a
*dependency*. This is what makes the library portable: a skill works in a bare terminal
with no API key, and a model call — when one is available — only ever *deepens* the result.
A failed or unavailable model call falls back to the deterministic base and is **never
fatal**.

---

## The two halves every skill carries

**1. A deterministic base (the no-LLM path).**
A checklist, a regex, a fixed template, or a code skeleton that a human (or a script, or a
CI job) can run with zero model access and still get a *usable scaffold* out. It is allowed
to be shallow. It is not allowed to be empty.

**2. A one-line model swap (the deepening step).**
A single reasoning step — "ask a model to do X over the base's output" — that enriches the
scaffold into a finished artefact. It is optional, idempotent against the base, and it
degrades cleanly: if it errors, times out, returns junk, or there is no model at all, the
base's output stands.

> Rule of thumb: if the model step were removed, the skill should still produce something a
> reviewer would accept as a *draft*. If it cannot, the base is not strong enough yet.

---

## The `deterministic_fallback:` frontmatter field

Every **skill** carries this field in its YAML frontmatter. It is a one-line, plain-English
statement of what the reader gets when no model is in play — the contract a reader can rely on.

```yaml
---
name: decompose-intake-to-outcomes
description: Derive business outcomes + child requirements from a raw intake brief.
deterministic_fallback: >
  Splits the intake into sentences, promotes each to a BO-n outcome, and stubs one
  TR-n.1 child requirement per outcome from a fixed template. No model needed.
---
```

What makes a good value:

- **Concrete, not aspirational.** Name the actual mechanism (split / regex / template /
  skeleton), not "best-effort heuristics."
- **Honest about depth.** It is fine to say the fallback is shallow. Readers need to know
  whether the no-LLM output is shippable or merely a starting frame.
- **One line.** If it needs a paragraph, the base is doing too much — push detail into the
  skill body's numbered steps.

A skill **without** this field is incomplete. The frontmatter validator (see
`.github/workflows/`) flags a missing or empty `deterministic_fallback:` on PR — advisory,
not blocking.

---

## How a skill body wires the two halves

Keep the base and the model step as **separate, numbered steps** so a reader can stop after
the base. The canonical shape:

1. **(base)** Run the deterministic step — checklist / regex / template fill.
2. **(model, optional)** Hand the base's output to a model with a focused prompt to enrich,
   reorder, rewrite, or fill gaps.
3. **(merge)** Keep the model's output **only if** it is well-formed; otherwise keep step 1's
   output verbatim. Validate against the skill's controlled vocabulary / required fields
   before trusting it.

The merge step is where the "never fatal" guarantee lives. Treat any of these as *use the
base*:

- no model available (no CLI, no key, offline);
- the call errored or timed out;
- the reply did not parse, or was empty;
- the reply violated the skill's schema / controlled vocabulary (drop the bad item, keep the
  base's).

---

## The one-line model swap

Picking *which* model is also one line, with a fixed precedence — so deepening a skill never
means rewriting it:

1. a global pin (e.g. an env override that forces every step onto one model);
2. a per-call override passed by the caller;
3. the skill's default tier.

A **tier hint** — `frontier` / `mid` / `light` — is accepted anywhere a model reference is,
and resolved to a concrete model at call time. Cheap skills default to a small tier; authoring
and synthesis skills default to a large one. Swapping is editing one word.

> Provider-agnostic: the swap names a *tier*, not a vendor or a concrete model id. Any LLM
> workflow that can read this markdown wires its own backend behind the same three-line
> precedence.

---

## Worked example (shape only)

```text
Base (no model):
  - regex-split intake into sentences
  - promote each sentence → outcome `BO-1..n`
  - emit one child `TR-n.1` per outcome from the fixed template
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

- **Model-only skills.** A skill whose first step is "ask the model" with no base behind it.
  If the call fails, the user gets nothing. Always have a floor.
- **A fatal model step.** Letting a failed/empty/malformed reply raise instead of falling
  back. The model path must degrade, never break.
- **Trusting unvalidated output.** Splicing model text into the artefact without checking it
  against the skill's required fields / controlled vocabulary. Validate, then merge.
- **Hidden model dependency.** A `deterministic_fallback:` that claims a no-LLM path the body
  does not implement. The field is a contract — keep it true.
- **Vendor lock in the swap.** Hard-coding one provider or model id into the steps instead of
  naming a tier behind a one-line model seam.

---

## Why this matters

Light and advisory beats heavy and enforced. Because every skill degrades to a deterministic
scaffold, the library is safe to drop into any environment — a laptop with no key, a CI
runner, a locked-down enterprise box — and still earn its keep. Models, when present, make it
better. They are never the thing standing between a user and a usable result.
