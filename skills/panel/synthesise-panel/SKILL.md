---
name: synthesise-panel
description: Cluster a panel transcript by node and signal and emit four proposal categories — gaps, value-to-carry, alternatives-to-weigh, risks/constraints; a genuine affirmative-vs-adversarial split becomes a human-owned decision; concur-only yields the honest empty case. Use when closing a panel (foldable into convene-a-panel) or synthesising any deliberation transcript.
one_liner: Cluster a deliberation transcript into four proposal categories.
aliases: [summarise panel, panel synthesis, deliberation summary, debate roundup, review wrap-up, consolidate findings, distil discussion, decision menu from debate]
when_to_use: closing a panel (foldable into convene-a-panel) or synthesising any deliberation transcript
output_kinds: [proposal, menu, halt]
deterministic_fallback: the four-category clustering skeleton
suggested_tier: mid
neighbours: usually follows panel/convene-a-panel (which produced the transcript); usually precedes panel/red-team-and-dissent (which records durable dissent from any split this surfaces).
---

# synthesise-panel

> Write the honest synthesis of a deliberation transcript: what it surfaced, and what it proposes a human now weigh. The synthesis proposes; the human disposes. Never imply a decision was made or scope was changed.

## Purpose

A deliberation panel produces a transcript: a set of contributions, each one voice answering one
question, each carrying a `signal` (the structured hint of what kind of move it made) and the real rows it
cited. The transcript is not the deliverable. The deliverable is a **synthesis** that:

1. opens with a one-line verdict on the panel's **posture** — did it find real tension, or did the lenses
   largely concur?
2. summarises each cluster of signal honestly, grounded in the cited rows;
3. emits the panel's yield as **four proposal categories**, each a menu item a human accepts or dismisses —
   not a verdict, not a report to admire.

The discipline that makes this trustworthy: the synthesis is *incapable of a verdict by construction*. It
only ever emits proposals. There is no path by which it resolves its own findings. A genuine
affirmative-vs-adversarial split is **not** auto-resolved — it is handed back to the human as a decision
with both sides' positions as the menu options. A lens that found nothing is the **honest empty case**, not
a gap — say so plainly. The synthesis never pretends the panel agreed when it did not, and never invents a
proposal the transcript does not support.

## When to use

- **Closing a panel.** This is the natural second half of convening a panel — fold it in, or run it
  standalone over a transcript that panel produced.
- **Synthesising any deliberation transcript** — any multi-voice exchange (a recorded design debate, a set
  of review comments tagged by stance) where you want to cluster the raw argument into a small, actionable
  menu of proposals rather than leave it as prose.

## Inputs

The user supplies, as markdown or structured text:

- **The panel contributions** — *Required.* For each: the voice (and its side, affirmative or adversarial),
  the question it answered, a one-line `stance_summary`, the argument body, and a `signal` from this closed
  set: `proposes_requirement`, `flags_gap`, `proposes_alternative`, `raises_risk`, `concurs`, `objects`. If
  the source transcript has no signal tags, infer one per contribution from its stance before clustering.
  *If absent/unreadable/empty:* HALT and ask for the transcript (per `skills/_shared/grounding.md` /
  `skills/_contract/grounding-no-absent-input`); never invent contributions, signals, or a posture to
  synthesise. See STEP 0.
- **The node each contribution touched** — *Required.* The outcome, requirement, section, challenge, or
  constraint it cited (its `surfaced_from`). This is the clustering key alongside the signal. *If absent on a
  contribution:* that contribution cannot be clustered to a proposal — name it as ungrounded and drop it,
  never back-fill a plausible node.
- **The questions and the panel cast** — *Optional.* So the synthesis can name which lens went silent and
  call that out as the honest empty case. *If absent:* proceed and omit the per-lens silence note; surface
  the gap as a `question`, never invent a cast.

You do not need a running system. A markdown transcript with stance + signal + cited node per contribution
is enough.

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

Per `skills/_contract/grounding-no-absent-input`: a missing transcript is the one absence that must HALT, not be improvised. The synthesis's whole value is fidelity to a real transcript — an "honest empty case" means *a lens in a real transcript had no signal*, never *there was no transcript at all*. Those are different outputs (the contract's "I read nothing" vs "I cannot read this").

## The method (a deterministic base plus a model step)

### STEP 0 — Verify the transcript is present (the grounding halt)

Before clustering, confirm a transcript was actually supplied — a file-level fact (absent / unreadable / empty), computed **before** any model reasoning, never a judgement on whether the transcript "looks rich enough". If there are **zero** contributions to read, emit the clean HALT below and **stop**. Do not synthesise from memory, do not invent a posture, do not manufacture a single proposal. A halt is a question, never a verdict.

```markdown
HALT — required input missing.

I can't synthesise a panel without the transcript it folds, and I won't invent contributions
to cluster. Point me at the deliberation and I'll cluster it into the four proposal categories.

I can read any of these:
  • a markdown panel transcript (per-contribution: voice, question, stance, body, signal, cited node)
  • the structured output of panel/convene-a-panel
  • a pasted set of review comments tagged by stance + signal

Where is the transcript? (Nothing is clustered or proposed until you point me at it.)
```

If the transcript is present, proceed to STEP 1. (A transcript that is present but where every lens
`concurs` is **not** a halt — that is the honest empty case, handled in STEP 1.)

### STEP 1 — Cluster the transcript by node + signal (deterministic base)

Group the contributions by the **node** they touched and read the **signal mix** within each cluster. This
is mechanical — it counts and clusters signals, it does not parse prose — so it runs with or without a model.
Map each cluster to one of exactly **four proposal categories**:

| signal pattern within a node cluster | proposal category | what it becomes |
|---|---|---|
| affirmative `proposes_requirement`, concurred across both sides | **value-to-carry** | a proposed requirement carrying that value |
| any `flags_gap` (a hole, a missing acceptance criterion, an unaddressed NFR, a thin section) | **gaps** | a challenge / push-back to address or dismiss |
| `proposes_alternative` with affirmative support | **alternatives-to-weigh** | a decision menu: the current shape vs the alternative |
| `raises_risk` / a hard constraint with no affirmative rebuttal | **risks/constraints** | a roadblock to retire or accept |
| a **split** — affirmative `proposes_requirement` against adversarial `objects` on the **same node** | **alternatives-to-weigh** (human-owned) | a decision menu whose options are literally the two sides' positions |
| `concurs` only, or no signal | *(nothing)* | the honest empty case — no proposal |

The four-category skeleton (the deterministic fallback) is:

```
GAPS                  — holes / tensions / unjustified lines the panel found, with no affirmative rebuttal
VALUE-TO-CARRY        — value the panel converged on that no current outcome yet holds
ALTERNATIVES-TO-WEIGH — cheaper / different shapes (incl. a genuine split → a human-owned decision menu)
RISKS / CONSTRAINTS   — hard constraints or failure modes that bound or invalidate a choice
```

Two rules are load-bearing here:

- **A genuine split is not auto-resolved.** When an affirmative voice proposes X on a node and an adversarial
  voice objects on the *same* node, the synthesis does not pick a winner. It emits a decision whose options
  are both sides' positions, so the human makes the call the panel could not. This is the honest move: never
  pretend the panel agreed when it did not.
- **`concurs` / `objects` alone produce no proposal.** An `objects` already lives on the challenge row the
  skeptic or minimalist was reading — the panel does not duplicate it. A pure `concurs` cluster proposes
  nothing; that is the empty case, not a gap.

Every emitted proposal carries its **provenance back into the transcript** — the contribution(s) that
produced it — and a short rationale that names the split where there was one ("two voices supported this; the
minimalist objected on cost — recorded as the trade-off below"). Accepting a proposal is then never a leap of
faith: the human can open the contributions behind it.

> **Multi-agent option (advisory).** This step deepens with independent parallel agents: launch one sub-agent per cluster (or per lens whose contributions you are weighing), at most 4 at a time, each a separate sub-agent. A failed sub-agent returns nothing and is never fatal — the deterministic base stands; merge what succeeded. (Claude Code: use the Task tool / subagents. Other tools: launch parallel model calls; or a matrix-strategy CI job.) Never required — it adds coverage and cuts single-pass bias. See `skills/_contract/parallel-agents`.

### STEP 2 — Write the synthesis (the model reasoning step)

With the clusters and their four-category mapping in hand, write `synthesis_md`. This is the depth a model
brings over the skeleton: it weighs arguments rather than just counting signals, and it phrases each cluster
honestly against the cited rows. Use this prompt:

> Close a design-deliberation panel. The panel has argued the design with itself, each lens reading a real
> finding. Write the synthesis: a clear, honest narrative of what the panel surfaced and what it proposes a
> human should now weigh. **The synthesis proposes; the human disposes — never imply a decision was made or
> scope was changed.**
>
> You are given the panel contributions (each with its `signal` and cited rows), the cluster summary (what
> the signals add up to), and the proposals already bound to real rows. Describe these faithfully; do not
> invent others.
>
> Write `synthesis_md` as markdown:
> - Open with a **one-line verdict on the panel's overall posture** — did it find real tension, or did the
>   lenses largely concur?
> - Summarise **each cluster** of signal honestly, grounded in the cited rows — name the gaps, the orphaned
>   value, the alternatives, the risks. **If a lens had no open signal, that is the honest empty case, not a
>   gap; say so plainly.**
> - Where the panel **split**, present both sides' positions as the options of a human-owned decision — do
>   not resolve it.
> - Close by stating that each proposal lands on its home view stamped with this session's provenance, for a
>   human to accept or dispose. **Do not pre-decide any of them.**
> - Stay strictly within the provided material. Add no scope the contributions do not support; reference no
>   row not listed.

The model emits `synthesis_md` (the narrative) plus, optionally, a sharper one-line description for each
listed proposal keyed by its reference. It invents no new proposal and cites no row outside the transcript.

## Output format

The user gets back a `synthesis_md` document and the four-category proposal menu. Concrete template:

```markdown
## Panel synthesis

**Posture:** the panel found real tension on the data-retention shape; elsewhere the lenses largely concurred.

### Gaps
- **No acceptance criteria on REQ-12 / REQ-19** (pragmatic_engineer, `missing_acceptance_criteria`).
  Two requirements have no way to verify them. → *raised as a challenge to address or dismiss.*
- **NFR coverage gap: availability** (pragmatic_engineer). No availability target is captured for the
  always-on outcome. → *challenge.*

### Value-to-carry
- **Carry the audit-trail value into the design** (explorer, `orphaned`). The panel converged on an
  orphaned requirement no current outcome holds; proposed as a new requirement threaded to BO-3.

### Alternatives-to-weigh
- **Retention: 90-day purge vs indefinite-with-tiering** — a genuine split. The solution_designer
  proposed indefinite tiering; the minimalist objected on cost and operability. **Not resolved by the
  panel** — recorded as a decision menu with both positions for you to pick.
- **Pattern override on the queue choice** (solution_designer, `pattern_override`). The chosen
  alternative departed from the recommended pattern; weigh whether the compromise still holds.

### Risks / constraints
- **Roadblock: vendor API rate limit at scale** (skeptic, `open_roadblocks`). Bounds the ingest design;
  retire or accept it.

### Honest empty case
- The **minimalist** found no scope reaching beyond the captured outcome on this run — no gold-plating to
  cut. That is the empty case, not a gap.

---

Each proposal above lands on its home view stamped with this session's provenance, for you to accept or
dispose. Nothing here is decided.
```

When folded into a tool/agent pipeline, the same content also serializes as a structured menu: a list of
proposals, each `{ category, summary, cited_rows, provenance, options? }`, where `options` is present only
for alternatives-to-weigh (and is mandatory for a split — both sides' positions).

## Notes / anti-patterns

- **Never imply a decision.** No "the panel decided / recommends adopting." It *proposes*; it *surfaces*; it
  *weighs*. The human disposes. Close every synthesis by saying so.
- **Never auto-resolve a split.** A real affirmative-vs-adversarial disagreement on the same node is the most
  valuable thing the panel produced — hand it back as a decision menu with both positions, do not pick a
  winner and bury the dissent.
- **Never dress up silence as a gap.** A lens with no open signal is the honest empty case. Saying "the
  minimalist found nothing to cut" is a *result*, not a failure to find work. Inventing a gap to fill the
  slot is the anti-pattern.
- **Never invent a proposal or cite a row the transcript does not contain.** Stay strictly within the
  contributions. The synthesis is faithful or it is worthless.
- **`concurs` and `objects` alone propose nothing.** Agreement needs no menu item; an objection already lives
  on the row it reads. Only the four productive signals (`flags_gap`, `proposes_requirement`,
  `proposes_alternative`, `raises_risk`) cluster into proposals.
- **Keep provenance.** Every proposal points back to the contribution(s) behind it and names any split as a
  trade-off, so accepting it is never a leap of faith.
- **Light and advisory.** No approval step blocks anything. The synthesis is a source of proposals, not a
  destination. Each proposal re-enters the normal flow on its own home view, accepted or dismissed exactly as
  any other proposal of its kind. The four output kinds stay in force: every emission is a proposal, a
  question, a menu, or a halt — and a human PR merge is the only ratify step.
