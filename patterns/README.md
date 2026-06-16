# The Pattern Library

A PR-reviewed set of solution shapes that have actually been built, one markdown file per pattern; advisory, not enforced — the Anatomy table below gives each field's role.

Front doors: [`../GETTING-STARTED.md`](../GETTING-STARTED.md) · [`../skills/MAP.md`](../skills/MAP.md) · [`../capabilities/INDEX.md`](../capabilities/INDEX.md) (need-side sibling).

## Author a pattern

Run [`../skills/library/author-component-pattern`](../skills/library/author-component-pattern/SKILL.md) to emit a `candidate` file from an already-built shape, then open the PR with the pattern PR template (`.github/PULL_REQUEST_TEMPLATE/pattern.md`), populating each field from the pattern you authored. With no model available, fall back to [`_TEMPLATE.md`](./_TEMPLATE.md): every field carries an inline `REQUIRED | CONDITIONAL | OPTIONAL | COMPUTED` note and a worked body skeleton — fill the REQUIRED fields and omit the COMPUTED ones (Actions write those into `generated/`). To re-review the library, run [`../skills/library/pattern-library-curate`](../skills/library/pattern-library-curate/SKILL.md).

Either way the pattern lands at `approval_status: candidate`. An agent never advances past `candidate` — promotion is a human PR (see lifecycle below).

## Anatomy

One `.md` file per pattern at `patterns/<category>/<slug>.md`. The frontmatter **is** the schema (the structured record an Action validates and a retrieval step reads); the body explains the same facts for a human.

| Field | Role |
| --- | --- |
| `pattern_key` | Cite-able id, UPPER-KEBAB, `^PAT-[A-Z0-9]+(-[A-Z0-9]+)*$`. Survives renames; the filename slug is chosen for legibility and need not equal it. |
| `intent` | Retrieval anchor, written `use WHEN … so that …`. The one line that decides whether the pattern fits. |
| `attached_nfrs` | List of `{kind, statement, acceptance_criterion}`. The `acceptance_criterion` is the testable "done" that turns the NFR into a checkable requirement when a project adopts. `kind` is closed (see below). |
| `constraints` | What the shape makes you give up. |
| `fulfils` (optional) | `[CAP-…]` back-ref to the capabilities a pattern serves, so a reader sees the need behind it. |
| `evidence` | Artefact links `{title, url}` proving it was built (reference build, runbook, load test, first engagement). Required once a pattern reaches `provisional`. |

## Categories (closed enum)

A pattern belongs to exactly one folder; `category` matches the folder name. Widening the set is a CONTRIBUTING-level change, not a per-PR call.

| Folder | What goes here | Authored exemplar |
| --- | --- | --- |
| [`deployment/`](./deployment) | How and where the system runs: topology, hosting, residency. | `PAT-WEBAPP-PG` |
| [`integration/`](./integration) | How components and teams talk: brokers, gateways, BFFs, events. | `PAT-APIGW-BFF` |
| [`data/`](./data) | Where data lives and how it is governed: lakehouse, catalogues, residency. | `PAT-LAKEHOUSE-DELTA` |

## NFR kinds (closed, 11)

Every `attached_nfrs[].kind` is one of: `security`, `availability`, `performance`, `data-residency`, `observability`, `resilience`, `cost`, `compliance`, `scalability`, `data-governance`, `operations`. The single source is [`_schema/nfr-kinds.enum.txt`](./_schema/nfr-kinds.enum.txt); the catalogue with sample targets is [`../nfrs/nfr-kinds.md`](../nfrs/nfr-kinds.md). The validator rejects anything else.

## Lifecycle

`approval_status` is human trust; it is closed and ordered: `candidate` → `provisional` → `approved` → `deprecated`.

| Rule | Detail |
| --- | --- |
| Human-only promotion | A CODEOWNERS architect review is the one structural human gate — only a human advances status, sets `approved_by`/`approved_at`, and attaches `evidence` (required from `provisional` up). |
| Validity & sunset | `valid_from` + `validity_check_months` let an Action compute a next-review date; it warns, never blocks. `sunset_at` (optional) = stop adopting for new work after this date. |
| Supersede, don't orphan | Replacement adds `supersedes: <old_key>`; the old pattern adds `superseded_by: <new_key>` and moves to `deprecated`. |
| Never delete an adopted pattern | A pattern adopted even once is provenance someone relied on; deprecate and supersede, never remove. |

The authoritative who/what/when of review lives in [`../CONTRIBUTING.md`](../CONTRIBUTING.md).

## Maturity is computed, never asserted

`maturity` (`experimental` → `emerging` → `battle-tested`), `adoption_count`, and `next_review_at` are COMPUTED by an Action from the [`../adoptions/ledger.jsonl`](../adoptions/ledger.jsonl) tally into `generated/` — never hand-written (the schema forbids the fields; see [`../DESIGN.md`](../DESIGN.md) §6). A new `candidate` with no ledger entries shows as `experimental` / adopted-by-0, honestly. The ledger records teams that evaluated and chose otherwise too — non-adoption is signal.

## Fulfilling a capability

[`../capabilities/`](../capabilities) is the need side: a capability resolves a plain-language need to a fulfilling pattern via `fulfilled_by[]`, and a pattern MAY cite `fulfils: [CAP-…]` back. The edge model is in [capabilities/README.md](../capabilities/README.md).

## Authored patterns

These have a file under `patterns/<category>/` and carry an `approval_status`.

| `pattern_key` | Name | Category | `approval_status` |
| --- | --- | --- | --- |
| `PAT-WEBAPP-PG` | Containerised web + managed Postgres | `deployment` | `provisional` |
| `PAT-APIGW-BFF` | API gateway + managed identity + BFF | `integration` | `provisional` |
| `PAT-LAKEHOUSE-DELTA` | Databricks Lakehouse + Delta Lake | `data` | `provisional` |

## Planned — not yet authored

Reserved keys for recurring shapes worth capturing. No file exists for these yet; the key is held so a future author cites it consistently. To author one, run [`../skills/library/author-component-pattern`](../skills/library/author-component-pattern/SKILL.md) — it lands the file at `approval_status: candidate`, and a human attaches real evidence to promote it in a PR.

| `pattern_key` | Name | Category |
| --- | --- | --- |
| `PAT-EVENT-BROKER` | Event-driven microservices + message broker | `integration` |
| `PAT-STATIC-SERVERLESS` | Static site + serverless API | `deployment` |
| `PAT-ONPREM-VM-NFS` | On-premises VM cluster + NFS shared storage | `deployment` |
