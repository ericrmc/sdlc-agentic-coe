# adoptions/ledger.jsonl — the append-only adoption ledger

## What this is

The GitHub-native replacement for the old `pattern_adoption` table. One JSON
object per line; each line is ONE real adoption of a component pattern by ONE
downstream engagement (repo). This file IS the headline number behind a
pattern's "used in N engagements" and its computed maturity.

`ledger.jsonl` is **pure JSONL** — one JSON object per line, nothing else. No
comment lines, no header, no blanks. (That keeps it machine-readable: the
linter's never-delete-with-adoptions invariant and the `pattern-lifecycle`
maturity tally both parse it with the same reader, and a `// comment` header
would make every line unparseable JSON.) This README carries the prose; the
`.jsonl` carries only data.

## Rules (light + advisory — there is no gate, just honest provenance)

1. **Append via PR; never delete or rewrite in place.** An adoption is a fact
   that happened; history is not tidied. If a team later walks back a pattern,
   append a NEW line with disposition `overridden-out` and an `override_reason`
   — do not edit or remove the earlier line.
2. **Absent = adopted-by-zero, shown honestly.** A pattern with no lines here is
   not "untested by omission"; the lifecycle Action reports it as 0 engagements
   rather than hiding it. Honesty about non-adoption is itself signal.
3. **`overridden-out` lines count as real data, not failures.** They tell future
   engagements "this was considered and declined here, and why" — read alongside
   the clean adoptions in the pattern's "seen elsewhere" view.
4. **Counts are computed, never hand-edited into frontmatter.** The
   `pattern-lifecycle` Action (`.github/workflows/pattern-lifecycle.yml`) tallies
   this file: `COUNT(disposition LIKE 'adopted%')` drives maturity
   (experimental → emerging → battle-tested) and the "used in N engagements"
   badge.

## Line schema

| field | type | meaning |
| --- | --- | --- |
| `pattern_key` | string | the adopted pattern's stable key, e.g. `PAT-WEBAPP-PG` |
| `repo` | string | the downstream engagement repo, `owner/name` (its own GitHub project) |
| `disposition` | enum | `adopted-clean` \| `adopted-with-overrides` \| `overridden-out` |
| `at` | string | ISO-8601 date the adoption decision landed (PR merge date) |
| `override_reason` | string? | required when `disposition` != `adopted-clean`; one honest sentence |
| `override_count` | int? | optional; how many of the pattern's NFRs/constraints were waived |
| `note` | string? | optional retrospective, e.g. "shipped; SLA held" |

The maturity tally counts any `disposition` starting with `adopted` toward the
adoption count; `overridden-out` lines are kept as real data but do not count
toward maturity (a team that evaluated and declined is signal, not an adoption).

## Example line

```jsonl
{"pattern_key":"PAT-WEBAPP-PG","repo":"acme/citizen-portal","disposition":"adopted-clean","at":"2026-05-02","note":"shipped; SLA held"}
```

## Honest caveat

The maturity tally is only as complete as this file. Today an adoption is a fact
only if some downstream repo appended a line here via PR. A cross-org scan of
downstream repos to discover adoptions automatically is a deferred upgrade;
until then, absent == adopted-by-zero, shown honestly, never padded.
