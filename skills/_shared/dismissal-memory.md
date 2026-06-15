# Dismissal memory — a shared convention

> Canonical, portable convention. Quoted by `reconcile`, `roadblocks`, `triage`,
> `red-team-and-dissent`, and `advisory-governance-checklist`. When a skill says
> "honour dismissal memory", this is the contract it means.
>
> **Light and advisory.** Dismissal memory is an ergonomic, not a gate. It changes
> *what a skill bothers to re-surface*, never *what a human is allowed to do*. There
> is no state machine, no approval, no enforcement. A human can always re-open
> anything by hand.

## The one rule

> **A cue the human has already dismissed is NOT re-proposed against UNCHANGED
> evidence. It re-arms ONLY when the underlying evidence changes.**

That is the whole convention. Everything below is how to make it portable and
mechanical so that "unchanged" and "changed" are decided by a stable key, not by a
model's mood on a second pass.

### Why it exists

Experts work by recognition, so these skills surface *cues* (questions,
observations, proposals) — never commands. A cue is only useful if it is
**dismissible in one action and stays dismissed**. A cue that re-nags every run
against evidence the human already looked at and waved off trains the reader to
ignore the channel, and a channel that is ignored is worse than no channel.

The failure this prevents is the unconditional re-propose: a skill that recomputes
its findings each run and re-emits every one, so the same "Requirement R-014 has no
acceptance criterion — how will it be tested?" question reappears after the human
has deliberately deferred it. (In the app this was a literal duplicate-INSERT bug;
in a markdown workflow it is a wall of repeated notes that buries the one new thing.)

## The memory key — what makes a cue "the same cue"

Dismissal memory is **file-keyed**: every dismissible cue has a stable **key** — a
tuple of the handles the skill cites, deliberately **excluding free-text that a human
might reword**. Two runs produce "the same cue" iff they produce the same key. The
key is what gets remembered as dismissed; the key is what gets checked before
re-proposing.

The key must be:

- **Stable across a re-run** over unchanged evidence — same inputs → same key.
- **Stable across a cosmetic edit** of the underlying item — fixing a typo in a
  requirement's wording, or re-phrasing a risk's title, must NOT mint a new key and
  resurrect a dismissed cue. Key off **structural handles** (ids, stable keys,
  section labels, check kind), not off the prose.
- **Distinct between genuinely different cues** — two requirements that share a
  section must not collapse to one key; a stable item id or `req_key` keeps them apart.
- **Re-armed by a real change** — when the cited evidence *materially* changes
  (a new conflicting requirement, an invalidated assumption, an edited candidate),
  the key changes (or the dismissal is explicitly invalidated), so the cue is allowed
  to return. This is the deliberate, sanctioned exception to "stay dismissed".

### Canonical keys per skill

These are the tuples each skill cites. Use them verbatim so dismissal records are
portable between skills and across re-runs.

| Skill | Memory key (the tuple) | Re-arms when… |
|---|---|---|
| **reconcile** | `(check_kind, req_key, section_key, message)` | the section's source snapshot changes, a new requirement/outcome/NFR appears, a register item fires (invalidated assumption / realised risk), or a contest opens |
| **roadblocks** | `cited_evidence` (the constraint/source the roadblock is enumerated from) | the cited source material changes, or a new roadblock cites new evidence |
| **triage** | the **candidate text** (the detected change being triaged) | the underlying change is different — new or materially altered candidate text |
| **red-team-and-dissent** | `(target_id, line_of_attack)` — what is attacked + the angle | the target's content changes, or a new line of attack is raised against it |
| **advisory-governance-checklist** | `(check_id, scope_handle)` — which check, over which item | the scoped item changes such that the check would now read differently |

> **reconcile's key is derived from STABLE handles + a derived message only.** Build
> the `message` from `check_kind` + the cited handles (and, where needed, a stable
> item id) — **never** from the item's free-text statement/title. That keeps the key
> distinct between two items that share a handle, and stable across a "why" edit to
> either item. This is the exact discipline the reconcile engine uses: its proposals
> carry `(check_kind, section_key, req_key, message)` where `message` is composed from
> handles, so a reworded requirement does not resurrect a dismissed proposal.

## How it is kept — portably, in the downstream repo

There is no database and no service. Dismissal memory lives as a **small plain-text
note committed to the downstream project's own repo**, so it travels with the work,
diffs in PRs, and is readable by any LLM workflow or human.

Recommended location and format — a JSONL ledger, one dismissal per line:

```
.coe/dismissals.jsonl
```

```jsonl
{"skill":"reconcile","key":["requirement_no_acceptance_criterion","R-014","requirements_acceptance","Requirement R-014 has no acceptance criterion. How will it be tested?"],"dismissed_on":"2026-06-13","by":"erica","note":"deferred — AC lands with the spike in phase 2"}
{"skill":"roadblocks","key":["HLD §4 in-boundary-LLM constraint"],"dismissed_on":"2026-06-13","by":"erica","note":"accepted-as-grey; client read deferred"}
{"skill":"red-team-and-dissent","key":["pattern:event-sourcing","operational-complexity"],"dismissed_on":"2026-06-13","by":"sanjay","note":"team has ops bandwidth; dissent recorded, not blocking"}
```

A markdown table is an equally valid carrier if humans edit it by hand:

```markdown
<!-- .coe/dismissals.md — dismissed cues; a skill will not re-surface these against unchanged evidence -->
| skill | key | dismissed_on | by | note |
|---|---|---|---|---|
| reconcile | requirement_no_acceptance_criterion · R-014 · requirements_acceptance | 2026-06-13 | erica | deferred to phase 2 |
| triage | "vendor renamed the auth endpoint" | 2026-06-13 | erica | cosmetic; no design impact |
```

Pick one carrier per repo and keep it. JSONL is preferred for machine round-tripping;
markdown is fine for human-first teams.

### Fields

| Field | Meaning |
|---|---|
| `skill` | which skill owns this cue (namespaces the key) |
| `key` | the memory key tuple from the table above (array, or `·`-joined in markdown) |
| `dismissed_on` | ISO date — when a human waved it off |
| `by` | who dismissed it (provenance; this is a human call, never the skill's) |
| `note` | optional — the human's reason; useful, never required |

## The method — how a skill uses it (the deterministic spine)

Any skill that emits dismissible cues follows the same four steps:

1. **Compute** the cues for this run from the current evidence (the skill's normal job).
2. **Key** each cue: build its memory key from the stable handles in the table above
   — never from rewordable prose.
3. **Filter:** read `.coe/dismissals.jsonl` (or `.md`). For each computed cue, if its
   key is present in the ledger **and** the evidence behind that key is unchanged
   since `dismissed_on`, **drop it silently** — do not re-surface it. Otherwise keep it.
4. **Re-arm (the LLM reasoning step):** for a computed cue whose key *matches* a
   dismissal but whose **evidence has materially changed**, surface it again, and say
   so plainly — *"re-raising: the requirement this was dismissed against has changed."*
   Deciding whether a change is *material* (a reworded title is not; a new conflicting
   requirement is) is the one judgment call — make it conservatively and **show your
   reasoning**, because a false re-arm re-nags and a missed re-arm hides a real change.

Step 3 is mechanical (key match + evidence-snapshot compare). Step 4 is the reasoning
step — it is where "the evidence changed" is judged. Keep the spine deterministic so
the channel stays quiet; keep step 4 honest so a real change is never buried.

### How "evidence unchanged" is decided

Two portable techniques, in order of preference:

- **Snapshot compare (preferred where a snapshot exists).** Record, alongside the
  dismissal, a tiny snapshot of the evidence — e.g. the set of source ids + a
  count + a max-version, or a content hash of the cited text. On the next run,
  recompute the snapshot; if it differs, the cue re-arms. (This mirrors how reconcile
  decides a section is stale: it compares a recorded `generated_from` snapshot —
  `{ids, max_version, count}`, plus a status-aware variant for items with no version
  column — against the live one. Same idea, kept as a note instead of a column.)
- **Key-only (lightweight default).** When no snapshot is recorded, treat a present
  key as dismissed until a human removes the line. Cheaper, but it will not auto-re-arm
  on a content change — so prefer it only for cues whose evidence rarely changes
  silently, or pair it with step 4's reasoning pass.

## Re-arming — the sanctioned exception

Dismissal memory is **not** permanent suppression. The whole point is that it re-arms
when the world moves. A cue must return when:

- a **new** item enters scope that the cue would now cite (a fresh conflicting
  requirement, a newly-added NFR);
- an item the cue was dismissed against **fires** — e.g. an assumption flips to
  *invalidated* or a risk flips to *realised* (reconcile's rework findings), or a
  roadblock's cited source is revised;
- the **candidate text** in triage is materially different from the dismissed one;
- the human explicitly **removes the line** from the ledger.

Re-arming is honest, not noisy: re-surface with a one-line "why I'm raising this
again", so the reader sees it is a *change*, not a re-nag.

## Anti-patterns

- **Keying off free text.** If the key includes a requirement's prose or a risk's
  title, a typo fix resurrects a dismissed cue. Key off `req_key` / item id / section
  label / check kind. Compose any human-readable `message` from those handles.
- **Permanent suppression.** Treating a dismissal as "never show again, ever" hides
  real change. Always pair the key with an evidence check or the re-arm reasoning pass.
- **Silent re-arm.** Re-surfacing a previously-dismissed cue *without* saying it was
  dismissed-and-changed reads as the skill ignoring the human. Always flag the re-raise.
- **A skill writing its own dismissals.** Dismissal is a **human** action — the skill
  only *reads* the ledger and *respects* it. The skill never decides on its own that a
  cue is dismissed; `by` is always a person. (Mirrors the source rule: the agent
  proposes/questions; the human owns the disposition.)
- **A central/global store.** Dismissal memory belongs **in the downstream repo** with
  the work, not in a shared service — so it diffs, travels, and is auditable. Each
  project owns its own ledger.
- **Coupling to a gate.** Dismissal memory must stay advisory. It only affects what is
  re-surfaced; it never blocks, approves, or records a verdict.

## Drift guard

If you change a skill's cited handles, **update its row in the key table above** in the
same PR. The keys here are a shared contract: reconcile, roadblocks, triage,
red-team-and-dissent, and advisory-governance-checklist all read and write the same
ledger, so a key shape that drifts in one skill silently strands every dismissal made
under the old shape (they will all re-arm at once). Treat this table as the source of
truth for what "the same cue" means.
