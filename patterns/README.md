# The Pattern Library

This directory is the **Centre of Excellence component-pattern library**: a small,
PR-reviewed set of *solution shapes that have actually been built*, captured as plain
markdown so any LLM workflow (or any human) can read them. A pattern is a recommendation
you can reach for with confidence — it carries the non-functional requirements (NFRs) it
implies, the constraints it makes you give up, and the evidence that it is real. The
library is **light and advisory**: a pattern recommends, attaches NFRs, and shows its
track record. It never gates a downstream project. Adopting a pattern is a human choice;
checking its acceptance criteria during the build is the adopting team's responsibility.

If you are here to *write* a pattern, jump to [How to author one](#3-how-to-author-one).
If you are here to *understand the rules of the road*, read on.

---

## 1. What a pattern is

**One `.md` file per pattern, at `patterns/<category>/<pattern_key-slug>.md`.** The
frontmatter **is** the schema — the YAML block at the top of each file is the structured
record; the markdown body is the human-readable explanation of the same facts. Everything
a tool needs to retrieve, rank, and reason about a pattern lives in that frontmatter; the
body exists so a person opening the file understands *why* before they adopt.

A pattern file therefore has two halves that must agree:

- **Frontmatter (the record):** `pattern_key`, `name`, `category`, `intent`, the
  approval-lifecycle fields, validity/sunset dates, `constraints`, and `attached_nfrs`.
  This is what an Action validates and what a retrieval step reads.
- **Body (the explanation):** `## Summary`, `## When to use / when not`,
  `## Attached NFRs`, `## Trade-offs`, `## Evidence of having been built`, `## References`.
  Each section restates a frontmatter fact in prose a colleague would actually say out loud.

Two ideas anchor the whole schema:

- **`intent` is the retrieval anchor.** It is written in the `use WHEN … so that …` shape
  (a real precondition, not a category restatement). It is the single line an agent reads
  to decide whether the pattern fits.
- **`attached_nfrs` are propagatable.** Each NFR is `{kind, statement, acceptance_criterion}`.
  The `acceptance_criterion` is the testable "done" — the field that lets an adopting
  project turn a pattern's NFR into a real, checkable requirement instead of a vague
  aspiration. (See the closed `kind` vocabulary in §5.)

See [`_TEMPLATE.md`](./_TEMPLATE.md) for the canonical, fully-commented frontmatter block.

---

## 2. The category folders

Patterns live under exactly **three** category folders. `category` in the frontmatter is a
closed enum matching the folder:

| Folder | `category` | What goes here | Seed exemplar |
| --- | --- | --- | --- |
| [`deployment/`](./deployment) | `deployment` | How and where the system runs: topology, hosting, residency posture. | `PAT-WEBAPP-PG` — containerised web + managed Postgres |
| [`integration/`](./integration) | `integration` | How components and teams talk: brokers, gateways, BFFs, event flows. | `PAT-APIGW-BFF` — API gateway + managed identity + BFF |
| [`data/`](./data) | `data` | Where data lives and how it is governed: lakehouse, catalogues, residency. | `PAT-LAKEHOUSE-DELTA` — Databricks Lakehouse + Delta Lake |

A pattern belongs to exactly one folder. If a shape feels like it spans two categories,
that is usually a sign it is really two patterns (one of which `supersedes`/composes the
other), or that the larger combined shape belongs in a concatenated skill assembled by an
Action — not a fourth category. The three-way split is deliberate and closed; widening it
is a CONTRIBUTING-level conversation, not a per-PR decision.

---

## 3. How to author one

Do not hand-craft frontmatter from memory. Two starting points, in order of preference:

1. **Copy [`_TEMPLATE.md`](./_TEMPLATE.md).** It contains the entire frontmatter block with
   an inline `REQUIRED | CONDITIONAL | OPTIONAL | COMPUTED` comment on every field, plus a
   body skeleton with worked examples for each section. Fill the REQUIRED fields; leave the
   COMPUTED ones out entirely (they are written into `generated/` by an Action, never by hand).

2. **Run the authoring skill:**
   [`skills/08-pattern-library/author-component-pattern`](../skills/08-pattern-library/author-component-pattern/SKILL.md).
   It takes a chosen, *already-built* solution shape and emits a pattern file at
   `approval_status: candidate` with the full lifecycle/provenance field set and a body of
   summary + attached NFRs + honest trade-offs. It is the right tool when promoting a
   solution a project actually explored into a reusable library entry. (For curating or
   re-reviewing the library as a whole, see the sibling
   [`pattern-library-curate`](../skills/08-pattern-library/pattern-library-curate/SKILL.md) skill.)

Either way, the author/skill leaves the pattern at `candidate`. **An agent never advances
`approval_status` beyond `candidate`.** Promotion is a human act in a PR review (§4).

Naming: the **filename** is a human-readable lower-kebab slug
(`containerised-web-managed-postgres.md`) and is chosen for legibility. The
**`pattern_key`** is the separate, cite-able identifier — UPPER-KEBAB and category-prefixed
by convention (`PAT-WEBAPP-PG`, `PAT-EVENT-BROKER`, `PAT-LAKEHOUSE-DELTA`), matching the
schema regex `^PAT-[A-Z0-9]+(-[A-Z0-9]+)*$`. The key is what a project cites and what an
Action concatenates by, so it must survive renames. The filename and the key are
deliberately **different shapes** — the linter validates the key's regex but does **not**
require it to equal the filename stem.

---

## 4. The lifecycle in brief

A pattern moves through a simple, **human-ratified** lifecycle. Nothing here is a state
machine that blocks downstream work — these are signals of trust and freshness, not gates.

```
   author/skill writes it          PR review (human)             time passes
   ───────────────────────►  candidate  ──────────────►  approved  ──────────►  (re-review / sunset)
                                  │  human attaches            │
                                  │  evidence + advances       │ maturity is COMPUTED
                                  ▼                            ▼ from adoption count (§6)
                            provisional                    deprecated ──► superseded_by: <key>
```

- **`approval_status`** is the closed, ordered enum — `candidate` → `provisional` →
  `approved` → `deprecated`. An author or agent leaves a new pattern at `candidate`. A
  **human reviewer advances it in a PR**, and only a human sets `approved_by` /
  `approved_at` and attaches `evidence` (artefact links proving it was built — a reference
  build, a runbook, a load-test report, the engagement it first shipped on). `approved` is
  the trusted fast-path; `provisional` means "reviewed, use with care, evidence attached."
- **Maturity is computed, not asserted** — see §6. `approval_status` is human trust;
  `maturity` is the track record. They are different axes and live in different places
  (frontmatter vs. `generated/`).
- **Validity & sunset make staleness visible (advisory).** `valid_from` +
  `validity_check_months` let an Action compute a next-review date into `generated/`; it
  **warns, never blocks**. `sunset_at` (optional) is the date after which a pattern should
  not be adopted for new work.
- **Supersede, don't orphan.** A replacement points back with `supersedes: <old_key>`; the
  old pattern points forward with `superseded_by: <new_key>` and moves to `deprecated`.
- **Never delete a pattern that has adoptions.** A pattern adopted by even one downstream
  project is provenance someone relied on; it is deprecated and superseded, never removed.
  Deleting it would hand a successor a tidied lie about what was actually built.

The full review/validation/promotion/sunset process — who reviews, what evidence is
required at each step, and how the PR gate is run — lives in
[`CONTRIBUTING.md`](../CONTRIBUTING.md). This section is the orienting summary; that file
is authoritative.

---

## 5. The NFR-kind vocabulary (closed)

Every entry in a pattern's `attached_nfrs` carries a `kind`, and `kind` is a **closed
enum** — exactly one of:

```
security · availability · performance · data-residency · observability ·
resilience · cost · compliance · scalability · data-governance · operations
```

These eleven values are the shared spine that lets NFRs flow cleanly from a pattern into a
downstream project as checkable requirements, and that lets the frontmatter-validation
Action reject typos and one-off kinds on PR. Do not invent new kinds in a pattern file. The
catalogue — each kind's intent plus sample measurable targets — is
[`nfrs/nfr-kinds.md`](../nfrs/nfr-kinds.md); that file is the source of truth for the
vocabulary, and the validator enforces it.

---

## 6. Provenance: maturity is computed, never asserted

The number that matters about a pattern is **how many real engagements adopted it** — and
that number is *tallied from evidence, not typed into a file as an opinion.*

- **Adoptions are recorded in [`adoptions/ledger.jsonl`](../adoptions/ledger.jsonl)** — one
  append-only JSON line per real adoption (which project adopted which `pattern_key`, when,
  with what disposition). The ledger includes teams that adopted *and* teams that evaluated
  and chose an alternative, because honesty about non-adoption is itself signal.
- **`maturity` is COMPUTED** from the adoption count — `experimental` → `emerging` →
  `battle-tested` — by an Action that writes it into `generated/`. It is **never** a field
  you hand-write in the source pattern. The same goes for `adoption_count` and
  `next_review_at`: derived facts, written by Actions, never opinions typed into the source.
- **Absent = adopted-by-zero, shown honestly.** A brand-new `candidate` pattern with no
  ledger entries is `experimental` / adopted-by-0, and the library shows it that way rather
  than padding the number or hiding the pattern. "Used in 0 engagements so far" is a true,
  useful fact — not an embarrassment to mask.

The discipline, stated once: a tool may *read* `maturity` and the adoption count to narrate
a recommendation; it may never *author* them. Approval is human; maturity is arithmetic over
the ledger. Neither is ever a model-emitted verdict.

---

## 7. Current seed patterns

The library seeds from the six original `solution_pattern` rows of the SDLC-companion app,
converted into this file-per-pattern shape. Two are converted and live today; the rest are
queued for conversion.

| `pattern_key` | Name | Category | Status | Notes |
| --- | --- | --- | --- | --- |
| `PAT-WEBAPP-PG` | Containerised web + managed Postgres | `deployment` | live (`provisional`) | Stateless web tier over a single managed relational state authority; strict in-region residency. 4 NFRs (`security`, `availability`, `data-residency`, `scalability`). |
| `PAT-APIGW-BFF` | API gateway + managed identity + backend-for-frontend | `integration` | live (`provisional`) | Cross-cutting concerns at the gateway; a BFF per client type; OIDC/Entra identity. Carries a worked **override** example. 4 NFRs (`security`, `observability`, `availability`, `scalability`). |
| `PAT-LAKEHOUSE-DELTA` | Databricks Lakehouse + Delta Lake | `data` | live (`provisional`) | Unity-Catalog-governed analytics/ML with column-level PII control; the **data/AI-governance exemplar**. 4 NFRs (`data-governance`, `security`, `compliance`, `cost`). |
| `PAT-EVENT-BROKER` | Event-driven microservices + message broker | `integration` | to convert | Services publish domain events to a durable broker; async, replayable, audit-friendly. NFRs: `availability`, `security`, `observability`, `resilience`. |
| `PAT-STATIC-SERVERLESS` | Static site + serverless API | `deployment` | to convert | CDN-served static frontend + scale-to-zero serverless backend for read-heavy/burst workloads. NFRs: `availability`, `performance`, `security`, `cost`. |
| `PAT-ONPREM-VM-NFS` | On-premises VM cluster + NFS shared storage | `deployment` | to convert | No-cloud / data-sovereignty deployments; client-managed infra, app layer only. NFRs: `compliance`, `availability`, `operations`, `security`. |

As patterns are converted, each lands in its category folder at `candidate` and is
promoted only when a human reviewer attaches real evidence in a PR (§4). The three live
exemplars are at **`provisional`** — reviewed and usable with care, each carrying a real
adoption-decision artefact as its `evidence`; a CODEOWNER promotes one to `approved` when a
production reference build is attached. That honest "provisional, not yet approved" state is
exactly what the lifecycle is designed to make visible.

---

> **The library in one sentence:** a pattern is one markdown file whose frontmatter *is*
> the record, written at `candidate`, human-ratified to `approved` by PR with attached
> evidence, carrying its NFRs and constraints as propagatable facts — with maturity computed
> from a real adoption ledger, never asserted. Light, advisory, honest. It recommends; it
> does not gate.
