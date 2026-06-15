# Contributing

How to author, propose, and validate the two things this repository holds: **skills** (portable agent instructions, markdown + YAML frontmatter) and **patterns** (PR-reviewed, evidence-backed building blocks with a real lifecycle).

This is a **Centre of Excellence**, not an enforcement engine. There are no state-machine gates, no governance dispositions, no version-bound approval blocks. Everything here is **light and advisory** — the one and only hard gate is `CODEOWNERS` on `patterns/**`. Read that sentence twice; it is the governing posture of the whole repo.

If you only read one section, read **[3. Authoring a pattern](#3-authoring-a-pattern--the-full-lifecycle)** — the lifecycle is the part with real rules.

---

## 1. The propose → ratify convention

The whole repository runs on one convention, and it is deliberately the lightest possible one that GitHub already gives us for free:

> **An agent (or a person) opens a PR proposing markdown. A human reviews it. The merge IS the ratification.**

There is no separate "approve" button, no disposition record, no workflow row to flip. The git history *is* the record:

- **Propose** = open a PR that adds or edits a `.md` file. An agent can do this end-to-end; so can you.
- **Ratify** = a human merges the PR. That merge — its author, its timestamp, its commit — is the ratification. We never store an approval status that the merge doesn't already prove.
- **Edit / decline** = the human pushes changes to the branch, or closes the PR with a reason. A closed PR is itself a durable, searchable record of "we considered this and chose not to."

Three consequences fall out of this and are worth internalising:

1. **Agents never cross the gate.** An agent proposes; it never merges its own pattern PR. (Skills are lighter — see §2 — but the same instinct holds: an agent's output is always a *proposal* a human can take or leave.)
2. **The reviewer is named by `CODEOWNERS`, not by ceremony.** For patterns, `patterns/**` is owned by `@architects`, and branch protection requires that review before merge. That is the single hard gate in the system.
3. **CI is advisory.** The validation Actions (§3) annotate the PR — they help the reviewer and the author. A red check is a strong signal, not a lock. The human reviewer is always the decision-maker.

---

## 2. Authoring a SKILL

A skill is a portable instruction set for an agent: YAML frontmatter + a markdown body of numbered steps. It must run in **any** LLM workflow that can read markdown — Claude Code, a CI bot, a plain chat session. No tool is assumed; no provider is named.

Skills live under `skills/`. To add one, open a PR adding one `skills/<name>/SKILL.md`. There is no candidate/approved ceremony for skills — they are advice, the merge ratifies them, done.

### 2.1 Required frontmatter

```yaml
---
name: derive-requirements          # kebab-case, unique, matches the directory
description: >                     # ONE line: says WHEN to reach for this skill
  Decompose a business outcome into traceable technical requirements, each
  threaded back to the outcome it serves.
when_to_use: >                     # the trigger condition, in the user's words
  You have accepted business outcomes and need the technical detail beneath
  them, with a derives-from trace edge to each parent outcome.
output_kinds: [proposal, question] # subset of {proposal, question, menu, halt}
deterministic_fallback: >          # what the skill produces with NO model in the loop
  The numbered spine alone yields a structured requirements list with empty
  rationale fields and every row flagged needs-review; the model step only
  enriches and challenges.
suggested_tier: ba                 # OPTIONAL — who lands on this (delivery-lead | ba | architect | reviewer)
---
```

- **`name`** — kebab-case, unique, matches the directory name.
- **`description`** — exactly one line, and it must say **when** to use the skill, not what it is. "Decompose an outcome into traceable requirements" — not "A requirements skill."
- **`when_to_use`** — the trigger condition in plain terms, so a router (human or agent) can match a situation to the skill.
- **`output_kinds`** — a subset of the closed vocabulary `{proposal, question, menu, halt}`. This is **the target rule** (next section) made declarable. A skill that needs to emit a `status`, a `verdict`, a `score`, a `ranking`, or an assessment of a person has the wrong shape — there is no output kind for those, by design.
- **`deterministic_fallback`** — what the skill produces with the model removed. Every skill must degrade to *something useful* from its numbered spine alone.
- **`suggested_tier`** *(optional)* — which role this skill primarily serves. Advisory; it shapes where the skill surfaces, never who is allowed to run it.

### 2.2 The target rule (the one design constraint)

Every step a skill instructs the agent to take must produce one of exactly **four output kinds**:

| Kind | Means | Example |
|---|---|---|
| `proposal` | a typed suggestion a human can take, edit, or drop | "Here are 6 derived requirements; accept the outcome to apply them." |
| `question` | a cue naming its target, dismissible in one action | "Redis serves only 'sub-200ms search', already met — necessary, or cut?" |
| `menu` | rival options for a human to narrow | "Three candidate architectures; pick, merge, or kill." |
| `halt` | stop and hand back, because a precondition is missing | "No accepted outcome to derive from — stop." |

**Never** instruct an agent to emit a status, a verdict, a colour, a queue disposition, a feasibility ruling, a similarity score, a maturity grade, or a judgement of a person. Those are either human-owned commitments or values **computed in code** (an Action), never authored by a model. A skill *narrates* a computed number; it never invents one.

### 2.3 The deterministic spine + one-line model swap

Every skill body is a **numbered spine** that works without a model, plus a clearly marked **LLM reasoning step** that enriches it. Preserve both:

- The **deterministic spine** is the steps a script could run: read the inputs, apply the structural rules, assemble the output skeleton. This is what `deterministic_fallback` describes.
- The **model step** is the one (or few) steps that need judgement — challenging a weak requirement, drafting a rationale, surfacing an adjacent need. Mark it plainly (`> Model step:`).
- The **one-line swap** rule: a skill must be writable so that swapping which model runs the reasoning step is a one-line change for the operator — no provider name, no API shape, no SDK call baked into the markdown. The skill says *what* reasoning is wanted; the runtime supplies the model.

This mirrors the platform's own build-order invariant: the deterministic structure comes first; the model is wired last, so proposal volume never outruns the honest review.

### 2.4 Quote shared stubs — don't import — and the drift guard

Skills often share small fragments: the four output kinds, the closed NFR vocabulary, a standard provenance footer. **Quote** the fragment inline; do **not** invent an `import:` or `$ref:` mechanism. A skill must be self-contained — droppable into a chat with nothing else loaded.

The cost of quoting is **drift**: a quoted vocabulary can fall out of step with its source. The drift guard is twofold:

1. Mark a quoted block with a one-line provenance comment pointing at the source of truth — e.g. `<!-- quoted from nfrs/nfr-kinds.md — closed vocabulary -->`.
2. The `validate-skill-frontmatter` Action checks that `output_kinds` is a subset of the closed set and (advisory) flags quoted vocabularies that no longer match their source. It annotates; it does not block.

When the source changes, the PR that changes it should re-quote the dependents. Reviewers watch for this; CI reminds them.

### 2.5 Skill body shape

Body sections, in order: **Purpose**, **When to use**, **Inputs** (what markdown/context the user supplies), **The method** (numbered steps preserving the deterministic spine *and* the marked model step), **Output format** (a concrete template/example of the markdown the user gets back), **Notes / anti-patterns**. Provider-agnostic throughout.

---

## 3. Authoring a PATTERN — the full lifecycle

A **pattern** is a building block the firm has *actually built* — a reference solution shape carrying its governed NFRs, its constraints, and its evidence. Patterns are the economic payoff of this repo: adopt one and its NFRs travel with it. Because they carry that weight, patterns — and only patterns — have a real lifecycle and a real human gate.

Patterns live under `patterns/`, one `.md` file each, with rich YAML frontmatter (`pattern_key`, `name`, `category`, `approval_status`, `supersedes`/`superseded_by`, `constraints`, `attached_nfrs`, `evidence`, validity dates — see `patterns/_TEMPLATE.md` and the schema at `patterns/_schema/pattern.frontmatter.schema.json`). The lifecycle has four steps: **propose → validate → ratify → compute**.

### 3.1 PROPOSE

1. Open a **new-pattern issue** (`.github/ISSUE_TEMPLATE/new-pattern.yml`) describing the building block **and its evidence** — where it was built, what shipped, what held in production. A pattern with no built-thing behind it is a wish, not a pattern.
2. Open a PR adding **one** `patterns/<category>/<slug>.md` with `approval_status: candidate`. The filename is human-readable lower-kebab (e.g. `containerised-web-managed-postgres.md`); the `pattern_key` inside is the cite-able UPPER-KEBAB key and need **not** equal the filename.

```yaml
---
pattern_key: PAT-WEBAPP-PG          # UPPER-KEBAB after PAT-; matches ^PAT-[A-Z0-9]+(-[A-Z0-9]+)*$
name: Containerised web + managed Postgres
category: deployment                # deployment | integration | data
intent: "use WHEN a line-of-business app needs strict in-region residency so that a stateless web tier scales over one managed relational store"
deployment_topology: Single-region container service + managed Postgres instance
data_placement: In-region managed relational DB; no cross-region replication by default
summary: Stateless web tier over a managed relational store; horizontal scale-out; the DB is the single state authority.
approval_status: candidate          # candidate → provisional → approved → deprecated (HUMAN-only to advance)
valid_from: "2026-06-15"            # ISO date (quote it so it stays a string)
validity_check_months: 12           # drives the advisory revalidation issue (§4)
constraints:
  - statement: Data at rest stays in the declared region.
    enforced: hard                  # hard (cannot be waived) | soft (waiver = recorded compromise)
attached_nfrs:                      # the NFRs that travel on adopt — kinds from the closed enum (§7)
  - kind: security
    statement: TLS 1.2+ in transit between tiers and to managed Postgres.
    acceptance_criterion: All inter-tier connections present a cert chain to TLS >= 1.2; verified by scan.
  - kind: availability
    statement: 99.9% monthly SLA achievable with multi-AZ container placement.
    acceptance_criterion: Measured uptime >= 99.9% over a trailing 30-day window.
# --- filled by a human (CODEOWNER) at promotion to provisional/approved — see §5 ---
# approved_by: "@architects"        # who ratified it
# approved_at: "2026-06-15"         # ISO date of the human approval
# evidence:                         # required once approval_status >= provisional
#   - {title: "...", url: "https://..."}
# --- filled only when deprecating ---
# superseded_by: PAT-NEW-KEY        # required when approval_status == deprecated
# --- COMPUTED, never hand-write: maturity, adoption_count ---
---
```

> **A zero-evidence pattern can only ever be `candidate`.** This is the floor. You may propose with no evidence to start a conversation, but it cannot advance past candidate until evidence is attached (§5).

### 3.2 VALIDATE — the advisory CI checks

On every pattern PR, two Actions run. **Both are advisory** — they annotate the PR to help author and reviewer; neither one is a merge lock (the only lock is the human review, §3.3).

- **`validate-patterns`** — runs `skills/_scripts/lint_pattern_frontmatter.py` against `patterns/_schema/pattern.frontmatter.schema.json`: frontmatter is well-formed; `pattern_key` matches `^PAT-[A-Z0-9]+(-[A-Z0-9]+)*$`; `category` ∈ {deployment, integration, data}; every NFR `kind` is in the closed enum (`patterns/_schema/nfr-kinds.enum.txt`, mirrored in `nfrs/nfr-kinds.md`); `enforced` is `hard|soft`; dates are ISO; and the evidence-conditionality rule (§5) holds for the declared `approval_status`. It also enforces the never-delete-with-adoptions invariant.
- **`validate-skill-frontmatter`** — the **target rule** check on skills: nothing declares an out-of-vocabulary output kind. It keeps skills speaking the same closed language; it does not gate patterns.

A red check is a strong nudge to fix the file. It does not stop a human who has a reason to merge anyway — that is the advisory posture, on purpose.

### 3.3 RATIFY — the one hard gate

`CODEOWNERS` routes `patterns/**` to **`@architects`**. Branch protection **requires that review** before merge. This is the single hard gate in the entire repository.

- **The merge is the ratification.** When an architect merges, that merge commit is where `approval_status: approved` (or `provisional`), `approved_by`, and `approved_at` get written — in the human's hand, in the human's commit. No agent ever sets these.
- An architect may merge a pattern at `provisional` (built, evidenced, not yet broadly proven) or `approved` (battle-ready). They may also edit the branch first or close the PR with a reason — a declined pattern stays a searchable record.
- **Reminder of the floor:** a zero-evidence pattern can only be `candidate`. The architect cannot promote it past candidate in the merge without evidence in `evidence[]`.

### 3.4 COMPUTE — what runs after the merge

Two Actions run on merge to `main`. Both **compute** facts from the ledger and history; neither asks a model for an opinion.

- **`pattern-lifecycle`** computes **maturity** from `adoptions/ledger.jsonl` — `battle-tested` / `emerging` / `experimental` is a `COUNT` over real adoption lines, never a model-emitted grade. It also opens revalidation issues when the computed next-review date (`valid_from + validity_check_months`) is reached and flags patterns past `sunset_at` (§4).
- **`concat-patterns`** rebuilds the combined bundles — concatenating related patterns (by category, by adoption co-occurrence) into larger reference skill files under `bundles/`, so a downstream project can load one file instead of ten. This is purely mechanical assembly; it adds no judgement.

---

## 4. Validity, sunset, supersede

Patterns rot. A pattern that was right two years ago can quietly become the wrong default. The lifecycle keeps them honest with dates, not with a person remembering to check.

- **`valid_from` + `validity_check_months`** drive a **next-review date** (computed = `valid_from` + the interval; written only into `generated/`, never into the file). When it arrives, `pattern-lifecycle` opens a **revalidation issue** routed to `@architects`: "is this still the firm's way to build X? Re-confirm, update, or sunset." Revalidation is itself a propose→ratify cycle.
- **`sunset_at`** — past this date the pattern is **flagged** in listings and **stops being recommended** by any retrieval/skill that reads patterns. It is not deleted; it stops *appearing as the answer*.
- **Supersede never deletes.** When a newer pattern replaces an older one, set `superseded_by` on the old (and optionally `supersedes` on the new); the old pattern's `approval_status` becomes `deprecated`. The chain is navigable; history is intact. Anyone reading an old project's adoption can still find the exact pattern they adopted.
- **NEVER delete a pattern with adoptions.** If `adoptions/ledger.jsonl` has even one line for a pattern, that pattern is part of a real project's record. Deprecate it (`approval_status: deprecated` + `superseded_by`, optionally `sunset_at`) — never remove the file. Deleting an adopted pattern erases a downstream project's provenance, which is exactly the dishonesty this repo exists to prevent. (The `validate-patterns` linter and the weekly `pattern-lifecycle` housekeeping both enforce this.)

---

## 5. Evidence

`evidence[]` is the list of links to **artefacts proving the pattern was actually built** — not a description of how it would work. Each entry is a `{title, url}` object (with optional `kind`, `project`, `date`); `url` must be a real URI. Acceptable artefacts: a merged repo or PR, a deployed environment, a runbook, a load-test report, an architecture decision record, a postmortem that the pattern resolves, a recorded adoption-decision doc.

```yaml
evidence:
  - title: "acme-portal — stateless web tier + managed Postgres, shipped 2025-11"
    url: https://github.com/org/acme-portal
    kind: repo                       # optional: repo | pull_request | runbook | adr | dashboard | load_test | post_mortem | doc
  - title: "Load-test: 99.94% over trailing 30 days at 800 RPS"
    url: https://github.com/org/acme-portal/blob/main/perf/2025-11-results.md
    kind: load_test
```

**Evidence is conditionally required.** It is optional at `candidate` (you may propose to open a discussion), and **required (at least one `{title, url}` entry) once `approval_status` is `provisional` or higher**. The `validate-patterns` Action checks this conditionally and annotates. The floor restated: zero evidence ⇒ can only be `candidate`.

---

## 6. Adoption

Every time a downstream project really adopts a pattern, append **one line** to `adoptions/ledger.jsonl`. This append-only ledger *is* the "used in N engagements" number and the input to computed maturity — it is never a figure a model invents. The ledger is **pure JSONL** (one JSON object per line, no comment header — the prose lives in `adoptions/README.md`). Field names: `pattern_key` (UPPER-KEBAB, joins to the pattern), `repo`, `disposition`, `at` (ISO date); `override_reason` is required when `disposition != adopted-clean`.

```jsonl
{"pattern_key":"PAT-WEBAPP-PG","repo":"acme/acme-portal","disposition":"adopted-clean","at":"2025-11-03","note":"Direct fit; in-region residency required."}
{"pattern_key":"PAT-WEBAPP-PG","repo":"acme/borealis-bff","disposition":"adopted-with-overrides","at":"2026-02-10","override_reason":"Waived the 99.9% SLA NFR; single-AZ accepted by client.","override_count":1}
{"pattern_key":"PAT-WEBAPP-PG","repo":"acme/northwind-svc","disposition":"overridden-out","at":"2026-04-01","override_reason":"Client contract mandated on-prem; chose VM cluster instead."}
```

- **`disposition`** is one of `adopted-clean` | `adopted-with-overrides` | `overridden-out`; supply an `override_reason` for anything but a clean adoption.
- **`overridden-out` is kept on purpose** — honesty about who *declined* a pattern, and why, is signal. "3 adopted, 1 chose an alternative; read why" is more trustworthy than a count that hides the dissent. (Only `adopted*` lines count toward maturity.)
- **Lines are never deleted.** An absent pattern in the ledger means **adopted-by-zero** — a legitimate, recorded state (a curation smell the library agent can flag), not an error.

See `adoptions/README.md` for the full line schema and the maturity-tally rules.

---

## 7. The closed vocabularies

Three small fields are drawn from closed lists. Don't invent values inline — point at the source, and extend the source in its own PR if a value is genuinely missing.

- **NFR `kind`** — the single source is `patterns/_schema/nfr-kinds.enum.txt` (mirrored prose in `nfrs/nfr-kinds.md`): `security`, `availability`, `performance`, `data-residency`, `observability`, `resilience`, `cost`, `compliance`, `scalability`, `data-governance`, `operations`. The schema and the pattern linter both read it.
- **Skill `output_kinds`** — `{proposal, question, menu, halt}` (the target rule; §2.2). Fixed; not extensible without changing the target rule itself.
- **Pattern `category`, `approval_status`, `enforced`, ledger `disposition`** — from `patterns/_schema/pattern.frontmatter.schema.json` and `adoptions/README.md`. `category ∈ {deployment, integration, data}`; `approval_status ∈ {candidate, provisional, approved, deprecated}`; `enforced ∈ {hard, soft}`; `disposition ∈ {adopted-clean, adopted-with-overrides, overridden-out}`.

`validate-patterns` checks membership against these sources and annotates on drift.

---

## 8. Light-governance posture (read this last, keep it first)

This repo is a library of advice, not a control plane. The posture, stated plainly so no future contributor reintroduces the weight we deliberately dropped:

- **No enforcement gates.** No state machine, no governance disposition record, no version-bound approval block, no "send-back routing." Those belonged to the bespoke app we retired. Here, the merge is the ratification and the git history is the record.
- **CODEOWNERS on `patterns/**` is the one hard gate.** Everything else — every CI check — is **advisory**: it annotates the PR to help the human, and a human can always merge over a red check with a reason.
- **No acceptance-rate metric.** Nowhere does this repo count "% of patterns approved" or "% of cues accepted." A review that ratifies nothing is a legitimate outcome; a pattern adopted by zero projects is a recorded fact, not a failure. A library optimised for an approval rate is worse than no library.
- **Agents propose; humans ratify; code computes.** Maturity, adoption counts, validity dates — computed. Outcomes, approvals, contested calls — human. Status, verdict, ranking, score — never authored by a model. Keep that line, and the rest of the repo stays honest.

When in doubt, choose the lighter mechanism. The heaviest thing we keep is a human reading a pattern PR — and that is on purpose.
