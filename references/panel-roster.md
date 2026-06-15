# Panel Roster — the fixed balanced 5-lens panel

This is the definitive roster cited by the **convene-a-panel** skill. It defines the five lenses, which
side each sits on, the two rules that keep a panel honest, and the four fixed questions used in
feature-brief mode. Treat this file as the single source of truth: if convene-a-panel and this roster ever
disagree, this roster wins.

A panel is a **multi-voice review you run on a piece of work** — a requirement set, a solution shape, a
feature brief — where the same reasoning argues *with itself* out loud and you keep the proposals. It is
advisory. The panel proposes; the human disposes. Nothing here is a verdict or an approval. You can
run a panel at any point, ignore any output, and re-run it later.

---

## The five lenses

Each lens reads **every** question through one fixed stance. The stance is what makes the panel useful:
five takes on the same material, deliberately angled, rather than one averaged opinion. Three lenses are
**affirmative** (they build the case, widen it, make it real); two are **adversarial** (they attack it,
shrink it). That asymmetry is intentional — a panel should generate more than it kills, but never without
someone trying to kill it.

| lens | side | stance (how it reads every question) |
|---|---|---|
| `explorer` | affirmative | **Widens the frame.** "What is the bigger opportunity here? What are we not yet asking? What outcome could this serve that we haven't named?" |
| `solution_designer` | affirmative | **Argues the shape of the solution.** "What is the cleanest design that serves the outcome? Name the shape. Where does this naturally want to be built?" |
| `pragmatic_engineer` | affirmative | **Argues buildability.** "What actually ships? What is the buildable, operable, day-2 path? What's the simplest thing that works in production?" |
| `skeptic` | adversarial | **Red-teams the requirements.** "What is the hidden assumption? Where is the evidence? What fails at MVP, and what fails at scale? What are we taking on faith?" |
| `minimalist` | adversarial | **Argues for less.** "What can we cut and still serve the outcome? Is this needed at all, or is it gold-plating? What's the smaller version?" |

These five are a **closed set**. Do not invent a sixth lens for a session, and do not rename one. A closed
set is what makes the balance rule below simple to check and keeps every panel comparable to every other.

### Which lenses to seat for which work

You do not have to seat all five. Seat a balanced subset tuned to the stage. Common castings:

- **Requirements / outcomes work** → `explorer` + `solution_designer` (affirmative) vs `skeptic` +
  `minimalist` (adversarial). The explorer is most valuable here because the frame is still open.
- **Solution-design / architecture work** → `solution_designer` + `pragmatic_engineer` (affirmative) vs
  `skeptic` + `minimalist` (adversarial). Buildability and shape are the live questions.
- **A single feature brief** → seat all four named in feature-brief mode (see below), or the minimal
  balanced pair `solution_designer` vs `skeptic`.

When in doubt, seat two affirmative and two adversarial — the default balanced panel.

---

## The two rules

A panel is only worth running if it argues both sides honestly. Two rules guarantee that.

### 1. The BALANCE rule — at least one of each side must be seated

> **A seated panel MUST include `>= 1` affirmative lens AND `>= 1` adversarial lens.**

This is the panel's core invariant. A panel that came back all-affirmative is worthless — it's a cheer
squad. A panel that came back all-adversarial just kills everything. Either way you learned nothing the
material didn't already tell you.

When you cast a panel, **check the balance before you run it.** If your casting has no adversarial lens,
add the `skeptic` (the default red-teamer). If it has no affirmative lens, add the `solution_designer` (the
default builder). The default balanced panel — two affirmative, two adversarial — always satisfies this by
construction.

This rule is the lightweight analogue of "the system literally cannot express a one-sided result": you make
a one-sided panel structurally impossible by refusing to run one. There is no enforcement engine here —
it's a discipline you apply when you seat the panel, and it's the first thing a reviewer should check on any
panel output.

### 2. The HONESTY rule — a lens with no signal says so

> **A lens that has nothing real to say on a question MUST say "no signal" — it MUST NOT fabricate a
> position to fill the slot.**

Every lens is expected to answer every question, but "answering" includes the answer *"from my lens, there
is nothing here."* The `minimalist` looking at an already-lean requirement should say "nothing to cut — this
is the minimal version" and move on. The `skeptic` looking at a well-evidenced claim should say "the
evidence here is sound; no objection." Inventing a contrived objection or a strained opportunity just to
seem productive is the single worst failure mode of a panel — it floods the synthesis with noise and trains
the human to ignore the panel.

A clean "no signal" from an adversarial lens is a **positive result**, not a wasted seat: it means the work
survived that angle of attack. Record it as such. Honest silence beats manufactured dissent every time.

---

## Feature-brief mode — the four fixed questions

When the panel is run against a **single feature brief** (one feature, one document), it uses a fixed,
deterministic agenda of **four questions**. Each maps to one core concern, and the affirmative/adversarial
lenses answer each from their stance. This mode is the fast path: no question-derivation step, just the four
below, every time, so feature briefs are comparable across the portfolio.

| # | concern | the fixed question |
|---|---|---|
| 1 | **completeness** | "What does this brief leave unspecified? What outcome, acceptance criterion, edge case, or dependency is named nowhere here — and would someone building from this brief have to guess at?" |
| 2 | **risk** | "What breaks this — at MVP and at scale? What is the riskiest assumption, the failure mode, the thing we're taking on faith?" |
| 3 | **alternative** | "Is there a different or cheaper shape that still serves the same outcome? What's the path we haven't considered?" |
| 4 | **necessity** | "Is this actually needed for the outcome — or is it gold-plating? What could we cut, defer, or not build at all and still succeed?" |

How the lenses tend to answer (illustrative, not prescriptive):

- **Q1 completeness** — `explorer` and `solution_designer` surface what the brief should also cover; the
  `skeptic` names the unstated assumption.
- **Q2 risk** — owned by the `skeptic`; the `pragmatic_engineer` adds the operability risks.
- **Q3 alternative** — `explorer` and `solution_designer` propose the cheaper/different shape; the
  `minimalist` proposes the smaller one.
- **Q4 necessity** — owned by the `minimalist`; the `pragmatic_engineer` weighs in on what's worth the
  build cost.

Any lens may answer **"no signal"** on any of the four (the HONESTY rule applies in feature-brief mode too).
A brief that draws four clean "no concern" answers from the adversarial lenses is a strong brief.

---

## What the panel produces

A panel is a **source, not a destination.** Its job is to feed proposals into wherever you already track
work — it does not own its own backlog. After running, the facilitating reasoning **synthesises** the
contributions into a small set of proposals, each one a thing a human accepts or dismisses:

- **a requirement** the panel converged on that isn't captured yet,
- **a gap or push-back** — a hole, a tension, an unjustified line (the adversarial yield),
- **an alternative** — a cheaper or different shape worth a decision,
- **a constraint** — a hard limit the panel named that rules something out.

Where the affirmative and adversarial sides **split** on the same point, do **not** resolve it for the
human. Surface it as a decision with both positions stated — "two voices supported this; the minimalist
objected on cost." An honest panel never papers over a real disagreement; it hands it up as a choice the
human owns.

Every proposal should carry its **provenance** back to the contributions that produced it, so accepting one
is never a leap of faith — the human can read the argument behind it.

---

## Quick reference

```
LENSES (closed set of 5):
  affirmative:  explorer, solution_designer, pragmatic_engineer
  adversarial:  skeptic, minimalist

BALANCE rule:   a seated panel has >= 1 affirmative AND >= 1 adversarial
HONESTY rule:   a lens with no real signal says "no signal" — never fabricates

FEATURE-BRIEF mode (4 fixed questions):
  1. completeness — what's unspecified / has to be guessed?
  2. risk         — what breaks at MVP and at scale?
  3. alternative  — cheaper or different shape, same outcome?
  4. necessity    — actually needed, or gold-plating?

Advisory always: the panel proposes; the human disposes. No verdict, no approval.
```

---

## Notes and anti-patterns

- **Don't skip the balance check.** The most common way a panel goes wrong is quietly: someone seats three
  affirmative lenses "to move fast" and the panel rubber-stamps the work. Always confirm at least one
  adversarial seat before running.
- **Don't punish honest silence.** A "no signal" answer is a result. Resist the urge to re-prompt a lens
  until it produces an objection — that's how you manufacture noise.
- **Don't let the panel decide.** It has no verdict power by design. A split is a decision for the human,
  not something the panel resolves. Surface both sides.
- **Don't invent lenses.** The five are fixed so panels stay comparable and the balance rule stays trivial
  to check. If you find yourself wanting a "security lens" or a "cost lens," fold that concern into the
  `skeptic` (risk) or `minimalist` (cost) charter instead of adding a seat.
- **Don't treat a panel as a precondition.** It never blocks advancing. Run it to pressure-test where
  you are, take what's useful, and move on.
