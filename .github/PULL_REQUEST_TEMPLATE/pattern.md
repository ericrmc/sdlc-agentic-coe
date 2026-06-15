<!--
  PATTERN REVIEW PULL REQUEST
  Select this template with: ?template=pattern.md
  (e.g. https://github.com/<org>/<repo>/compare/main...your-branch?template=pattern.md&expand=1)

  Use this template for any PR that ADDS, CHANGES, SUPERSEDES, or DEPRECATES a
  component pattern under /patterns. For anything else (skills, actions, docs)
  use the default template.
-->

## What this PR does to the pattern library

<!-- One or two sentences. Which pattern file(s), and is this new / changed / superseding / deprecating? -->

- Pattern(s) touched: `patterns/...`
- Change type: <!-- new candidate | promote candidate→approved | edit approved | supersede | deprecate -->

---

## The ratification statement (read this first)

> **MERGING THIS PR IS THE RATIFICATION.** There is no separate gate, state
> machine, or governance disposition. When a human merges this PR, the pattern
> in its merged state is what the library asserts. No Action, bot, or agent
> ratifies a pattern — a reviewer does, by approving and merging.
>
> A pattern with **zero linked evidence can only be `status: candidate`**. It
> may live in the library as a candidate so people can find and discuss it, but
> it must not claim `active` until it carries artefacts proving it was built.

This is the human half of pattern governance. The Action on this PR validates
*shape* (frontmatter parses, enum values are legal, required fields present).
The Action does **not** and **must not** decide that a pattern is good, true,
or approved. That is what the checklist below is for.

---

## Reviewer checklist (architect / pattern steward)

Do not approve until every box that applies is ticked. If a box cannot be
ticked, the change is not ready, or the pattern drops to `candidate`.

### Evidence — a pattern is a claim that something was built

- [ ] **Evidence / artefacts-of-having-been-built are linked** in `evidence[]`
      (PR/commit, repo, running deployment, ADR, screenshot, test run, or
      retro). Each entry is a real, resolvable link — not "internal wiki" or
      "ask me".
- [ ] If `evidence[]` is **empty**, then `status` is `candidate` (and only
      `candidate`). A candidate with no evidence is fine; an `active` pattern
      with no evidence is not.

### Human ratification — no agent set the verdict

- [ ] **The status / approval was moved by a HUMAN in this PR.** No GitHub
      Action, bot, or agent set `status`, `validated_by`, or `validated_on`.
      (`validated_by` is a person's name/handle, never `github-actions[bot]`
      or an agent id.)
- [ ] `validated_on` is the date a human reviewed it — set in this PR, ISO
      format (`YYYY-MM-DD`).

### Validity window — patterns expire on purpose

- [ ] **`valid_from`** is set (ISO date the pattern became usable).
- [ ] **`review_by`** is set (ISO date this pattern must be re-checked). A
      pattern with no `review_by` never gets revisited and silently rots.
- [ ] **`sunset_on`** is set *if applicable* (a known end-of-life: a dependency
      reaching EOL, a platform being retired). Leave blank only if there is no
      known sunset — not because nobody thought about it.

### Supersede / deprecate — don't orphan adopters

- [ ] If this **replaces** an older pattern: `supersedes` on the new pattern and
      `superseded_by` on the old one **both** point at each other (no one-way
      link, no dangling key).
- [ ] The superseded pattern's `status` is moved to `superseded` (not deleted).
- [ ] **No pattern that has adoptions is being deleted.** Patterns with a
      track record are *deprecated or superseded in place*, never removed —
      deleting one breaks the provenance of every project that adopted it.
- [ ] If deprecating: `status: deprecated` and a `warnings[]` entry says what
      to use instead and why.

### NFRs — the closed enum

- [ ] **Every `attached_nfrs[].kind` is one of the 11 allowed values** (the
      Action checks this too, but confirm it reads sensibly):

      security · availability · performance · data-residency · observability ·
      resilience · cost · compliance · scalability · data-governance · operations

- [ ] Each attached NFR carries an `acceptance_criterion` (a testable "done"),
      so that on adoption it can flow into a downstream project as a real
      derived requirement — not a flat string.

### Sanity

- [ ] `status` is one of: `active` · `warning` · `superseded` · `deprecated`
      (`candidate` for not-yet-evidenced). It matches what the body claims.
- [ ] `constraints[]` and `warnings[]` honestly state what you give up by
      adopting this. A pattern that lists no tradeoffs is under-described.
- [ ] The body has a real **Example / artefacts** section pointing at the
      evidence above — a reviewer can see it was actually built.

---

## Evidence summary (for the reviewer's convenience)

<!--
  Paste the strongest 1-3 artefacts here so the reviewer doesn't have to dig.
  e.g.
    - Built in: <repo/PR link>
    - Running at: <deployment / dashboard link>
    - Retro / outcome note: <link> — "shipped; SLA held"
-->

-

---

## Notes for the reviewer

<!-- Context that helps the human decide: where it's been used, what's risky,
     what you're unsure about, what you deliberately left out of scope. -->

<!--
  Reminder for the author: this PR is the ratification. If you are not ready
  for the pattern to be asserted as `active`, set it to `candidate` and say so
  above — that is a normal, encouraged state, not a failure.
-->
