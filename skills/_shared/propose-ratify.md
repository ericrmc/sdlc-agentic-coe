# propose -> ratify (canonical)

> This is the one canonical statement of the rhythm that every skill follows.
> Skills **quote** this file rather than re-describing it, so the wording cannot drift.
> If you are editing the rhythm, edit it **here** and let the quotes follow.

## The rhythm

Every skill follows the same shape, end to end:

```
human supplies / asks  ->  an AGENT does work and PROPOSES  ->  a human ratifies / edits / overrides  ->  proceed
```

- The **human supplies** the input the skill needs (a vision, a draft, a codebase pointer, a decision question).
- The **agent proposes** — it explores, drafts, recommends, red-teams, estimates. Its output is always a *proposal*: a draft requirement, a recommended pattern, a flagged finding, a suggested estimate. The agent's output is never the final word.
- The **human ratifies** — accepts, edits, overrides, or rejects the proposal. Deviations (an override of a recommended pattern, a rejection with a reason) are captured as *data*, not discarded.
- Then you **proceed**.

This is advisory, not enforced. Nothing in this repo blocks you from moving on. There is no enforced ordering and no governance disposition. The rhythm is a habit the skills make easy to follow, not a wall.

## The one invariant worth keeping

**The agent never ratifies its own work.**

An agent may propose, draft, recommend, estimate, flag, and red-team. A human accepts, edits, overrides, or rejects. That separation is the whole point — it is what keeps a person in control of the project's direction while letting the agent do the heavy lifting. Everything else here is light and advisory; this one line is the load-bearing principle.

## Advisory checkpoint wording

Where a skill wants to mark a natural pause — a point where a person really should look before the project moves on — it states it in exactly this advisory form:

> **Checkpoint (advisory): a human should confirm _X_ before proceeding.**

e.g. *"...confirm the requirement set reflects the business outcomes before deriving the
technical view."* These are prompts — they never error, set a status, or refuse to continue;
a person can proceed past an unread checkpoint and own that.

## PR-merge IS the ratify

In a GitHub-native repo **the pull request is the ratification surface** — the agent's work
lands as a proposal in a branch/PR, and **merging that PR is the ratify step**, in the open,
with history. No extra machinery:

| Rhythm step | GitHub-native mechanic |
|---|---|
| human supplies / asks | an issue, a discussion, or the prompt to a skill |
| agent proposes | a branch + draft PR carrying the agent's output (requirements, patterns, findings, architecture sections) |
| human ratifies / edits / overrides | PR review comments, requested changes, edits to the diff |
| **proceed** | **merging the PR** — the merge is the ratify |
| deviation captured as data | the PR description / review thread / an `override:` note in the merged file |

The same applies to **component patterns**: a pattern joins the library only when a human
merges its PR — the agent opens it, only a person merges. Re-running a skill simply produces a
fresh proposal to ratify by merge.

Keep it light. Propose, then ratify-by-merge.
