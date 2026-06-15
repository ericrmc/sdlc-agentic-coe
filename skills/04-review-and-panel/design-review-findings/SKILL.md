---
name: design-review-findings
description: Read a design or solution-architecture draft (or a running front-end) and emit severity-tagged, citation-bearing FINDINGS over a built-in architecture checklist. Clamp out-of-set severity to info, default a missing ref, drop empty findings. Never approves or rejects — findings, not verdicts. Use when reviewing a design draft for concrete, actionable observations a panel would raise.
when_to_use: reviewing a design draft or a running front-end for concrete actionable findings
output_kinds: [proposal, question]
deterministic_fallback: the architecture checklist + the severity-clamp / default-ref / drop-empty harness
suggested_tier: opus
stage: 8
references:
  - references/architecture-checklist.md
---

# design-review-findings — the general review engine

## Purpose

Read a design draft — a solution-architecture document, a section bundle, or a
running front-end — and emit **concrete, actionable FINDINGS**: observations a
reviewer (or a governance panel) would raise, each tagged with a severity and a
citation to the exact thing it attaches to.

This skill is a **reviewer, not a judge**. It stays inside the material it was
given. It does not invent scope the text does not imply, it does not approve or
reject the design, and it produces no verdict and no gate disposition. A human
decides what to do with the findings. The skill's only job is to surface them
clearly, with enough specificity that a reader can act on each one.

This is the **general review engine**. The companion skill
`frontend-a11y-review` is a *specialisation* of this same engine: it carries a
WCAG success-criteria checklist instead of the architecture checklist, and cites
WCAG SCs in `ref`. Everything else — the finding shape, the severity set, the
validation harness — is shared. If you change the contract here, change it there
too.

## When to use

- A solution-architecture draft has been synthesised (FORGE stage 7) and you
  want a pass over it before it goes to a panel or to the author for revision.
- A front-end is running and you want a structured list of design concerns
  (for the a11y-specific variant, prefer `frontend-a11y-review`).
- Any time someone asks "what would a reviewer flag in this?" and wants a list
  they can triage, not a yes/no.

Do **not** use this to gate or block. There is no pass/fail here. If a process
needs a decision, that is a human's call downstream of these findings.

## Inputs

The user supplies, as markdown / context:

- **The design material** — the draft document, the section bundle, or a
  description of the running front-end. This is the substance to review.
- **Project context** (optional but recommended) — title and a short
  description, so findings stay anchored to what the project is actually for.
- **Attached NFRs / adopted patterns** (optional) — so a finding can cite a
  specific NFR (`NFR-availability`) or pattern (`pattern:containerised-web`)
  rather than a vague "the design".

If the material is empty, there is nothing to review — say so and stop. Do not
manufacture findings from nothing.

## The method (numbered STEPS)

The engine has a **deterministic spine** (steps 1, 3, 4) and an **LLM reasoning
step** (step 2). The spine is what makes the output trustworthy even when the
model is weak or unavailable; the LLM step is what makes it insightful.

### Step 1 — DETERMINISTIC: walk the architecture checklist

Before any open-ended reasoning, walk the built-in architecture checklist
(see `references/architecture-checklist.md`) against the draft. For each item,
ask: *does the draft state this, and is what it states adequate?* The checklist
is the floor — these are the things a managed-services governance panel will ask
about every single time, so a draft that is silent on one of them has a gap
worth a finding:

- **RPO / RTO** — recovery point and recovery time objectives. Is data-loss
  tolerance and recovery time stated, or unstated?
- **Encryption at rest** — is the at-rest posture for stored data declared?
- **RBAC between tiers** — is access control *between* the tiers (web → app →
  data) specified, not just at the edge?
- **Deployment topology / availability model** — how is it deployed, across how
  many zones/regions, with what availability target?
- **Secret rotation** — are credentials/keys rotated, and how?
- **Unclassified integrations** — are there integration points whose
  data-sensitivity, auth, or ownership is left unclassified?

A silent checklist item is typically a `medium` (or `high` if the project
context makes it load-bearing). A present-but-vague item is a `low` or `medium`.
A present-and-adequate item needs no finding (or an `info` note for
traceability).

### Step 2 — LLM: review for everything the checklist does not catch

Now reason openly over the draft for gaps, risks, unstated assumptions, and
missing specifications **beyond** the fixed checklist — the things specific to
*this* design. Use the review prompt below. Stay within the material; cite the
thing each finding attaches to. This is where the engine earns its keep: the
checklist catches the universal omissions, this step catches the
design-specific ones.

> **REVIEW PROMPT** (carry this to the model verbatim; fill the `${...}` slots):
>
> You are a design reviewer on an internal managed-services delivery team.
> Review the design draft below and produce FINDINGS — observations with a
> citation — NOT verdicts. You do not approve or reject the design; a human
> decides what to do with your findings.
>
> PROJECT: `${title}`
>
> DESCRIPTION / CONTEXT:
> `${description}`
>
> DESIGN DRAFT:
> `${design_content}`
>
> Identify gaps, risks, unstated assumptions, and missing specifications in THIS
> draft — things a governance panel would query (e.g. an unstated RPO/RTO,
> encryption-at-rest posture, RBAC between tiers, deployment-topology /
> availability model, secret rotation, unclassified integrations). Stay within
> the material in the draft and the project context; do not invent scope the
> text does not imply. Each finding must be a concrete observation a reader can
> act on, with a citation in `ref`.
>
> Assign each finding a severity from EXACTLY this set: `high`, `medium`, `low`,
> `info`. (`info` = a neutral note for traceability, not a problem.) Set `ref`
> to the thing the finding cites — for example an attached NFR
> (`NFR-availability`, `NFR-security`), a pattern (`pattern:containerised-web`),
> a design section (`design-section:integrations`), a comparator
> (`comparator:partner-integration-hub`), or a WCAG success criterion
> (`wcag:1.4.3`) when reviewing a front-end.
>
> Return ONLY a JSON object of exactly this shape, no prose, no markdown fence:
>
> ```json
> {
>   "findings": [
>     {"severity": "high", "text": "The observation and why it matters.", "ref": "NFR-availability"}
>   ]
> }
> ```

### Step 3 — DETERMINISTIC: run the validation harness

Pass every finding from steps 1 and 2 through this harness. These three rules
are the trust boundary — apply them *verbatim*, they are non-negotiable. A model
will occasionally hand back a severity outside the set, a finding with no
citation, or an empty string; the harness makes the output safe regardless.

1. **Clamp out-of-set severity to `info`.** The allowed set is exactly
   `{high, medium, low, info}`. Any other value (e.g. `critical`, `warning`,
   `P1`, empty) becomes `info`. Lowercase and trim first.
2. **Default a missing `ref`.** If a finding has no citation (empty or absent
   `ref`), set it to `design`. A finding must always cite *something*; `design`
   is the catch-all that means "the draft as a whole".
3. **Drop empty-text findings.** Trim the text; if it is empty, discard the
   finding entirely. A finding with nothing to say is not a finding.

Reference implementation of the harness (the exact behaviour the source app
ships):

```python
ALLOWED = {"high", "medium", "low", "info"}

def normalise(findings):
    out = []
    for it in findings:
        if not isinstance(it, dict):
            continue
        text = str(it.get("text") or "").strip()
        if not text:                          # rule 3: drop empty-text
            continue
        severity = str(it.get("severity") or "").strip().lower()
        if severity not in ALLOWED:           # rule 1: clamp out-of-set → info
            severity = "info"
        ref = str(it.get("ref") or "").strip() or "design"   # rule 2: default ref
        out.append({"severity": severity, "text": text, "ref": ref})
    return out
```

### Step 4 — DETERMINISTIC: order and emit

Sort the surviving findings `high → medium → low → info` (most material first),
then render them in the output format below. If after the harness there are zero
findings, say so plainly — "no findings; the draft is clear on the checklist and
the material reviewed" — rather than inventing filler.

### Deterministic fallback

If the LLM step (step 2) is unavailable or returns nothing usable, the skill
still produces value: emit findings from the architecture checklist alone
(step 1), run them through the harness (step 3), and order/emit (step 4). The
checklist plus the harness *is* the floor of this skill — it never returns
nothing useful just because the model was unavailable.

## Output format

Return a markdown block the user can triage. Each finding is one row: a severity
tag, the citation it attaches to, and the observation. Findings only — no
verdict line, no "APPROVED / REJECTED", no gate status.

```markdown
## Design review findings — <project title>

_6 findings (1 high, 2 medium, 2 low, 1 info). Findings, not a verdict —
no approval or rejection is implied._

| Severity | Ref | Finding |
|----------|-----|---------|
| **high** | `NFR-availability` | The draft states a 99.9% uptime target but no RPO/RTO. With a single-region topology (design-section:deployment) that target is not credibly recoverable — name a recovery point and recovery time, or relax the SLA. |
| **medium** | `design-section:data` | No encryption-at-rest posture is declared for the primary datastore. A managed-services panel will ask; state the at-rest control and key custody. |
| **medium** | `design-section:integrations` | The partner feed integration is unclassified — its data sensitivity, auth mechanism, and ownership are not stated. Classify it before it reaches a panel. |
| **low** | `pattern:containerised-web` | RBAC between the web and app tiers is implied by the adopted pattern but not spelled out in this draft. Make the tier-to-tier access model explicit. |
| **low** | `design-section:operations` | Secret rotation is not mentioned. State whether credentials/keys rotate and on what cadence. |
| **info** | `comparator:partner-integration-hub` | The chosen topology mirrors the partner-integration-hub comparator; noting for traceability — no action implied. |
```

Keep each finding self-contained: *what* is missing or risky, *where* it
attaches (the `ref`), and *why it matters* / what to do. A reader should be able
to act on a single row without reading the others.

## Notes / anti-patterns

- **Findings, not verdicts.** This is the whole posture. The moment you write
  "this design is approved", "ready to ship", or "fails review", you have left
  the skill's lane. Surface concerns; let a human decide.
- **Stay in the material.** Do not invent requirements, scope, or
  infrastructure the draft does not imply. A finding about something that isn't
  in the draft and isn't on the checklist is noise. The checklist is the only
  licence to flag an *absence*; everything else must be grounded in text that
  is present.
- **Always cite.** Every finding carries a `ref`. "The design is weak" with no
  citation is useless and will be defaulted to `design` by the harness anyway —
  do better and name the section, NFR, pattern, comparator, or WCAG SC.
- **`info` is not a problem.** Use it for neutral traceability notes (a
  comparator match, a deliberate trade-off worth recording). Do not inflate an
  `info` into a `low` to pad the list, and do not bury a real `high` as `info`.
- **The harness is not optional.** Even when you trust the model, run step 3.
  It is cheap, it is deterministic, and it is what lets a downstream consumer
  trust the severity field and the ref field without re-validating.
- **Don't pad.** Zero findings is a legitimate, valuable result. An empty draft
  is "nothing to review", not "let me find six things".
- **This is the engine; specialise by swapping the checklist.** Front-end /
  WCAG review is the same engine with a WCAG checklist and `wcag:` refs — reach
  for `frontend-a11y-review` there rather than re-deriving the contract.
