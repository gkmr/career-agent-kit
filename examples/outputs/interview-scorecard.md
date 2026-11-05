# Interview scorecard (example output of skills/interview-coach)

Invented mock. Candidate: Dana Whitfield. Question from the mock set: "Should Veridane
build or buy hosted compute for builds?" Counts below come from
`python3 scripts/altitude_count.py`, not from judgment.

## Transcript (the answer as given)

> So I'd start by looking at the vendor landscape. There are a lot of good compute APIs
> out there, and we'd want to run a bake-off with maybe three vendors. We'd set up a
> scorecard in a spreadsheet, look at cold-start latency and cost per minute, and run an
> A/B test on a slice of builds. Then we'd pick the one with the best price and integrate
> it into the runner pipeline. At Quillstone we cut median build time 44%, so I know what
> good looks like. I think the main thing is to move fast and get something live in a
> quarter.

## Scorecard

```
INTERVIEW SCORECARD
Session: mock 2 | Role: VP Product, Developer Platform (Veridane, invented) | Interviewer: hiring manager (role only) | Scope: single Q&A

RATING SCALE (0-4)  0 not enough information  1 would likely filter  2 meets bar  3 strong for level  4 interviewer leans forward

| Dimension          | Score | Key evidence                                                      |
| Content            |   2   | "pick the one with the best price": a vendor choice, no bet        |
| Structure          |   2   | process list in order; no answer in the first sentence             |
| Delivery           |   3   | transcript only; complete sentences, low filler                    |
| Executive Presence |   2   | capped: F share 100% on a strategy question                        |
| Mission Fit        |   2   | no link to the JD crux (who owns the wait)                          |
| COMPOSITE          |  2.2  | Content 25 / Structure 20 / Delivery 20 / Presence 20 / Fit 15     |

THINKING AUDIT (counts, not adjectives)
  Question asked:   "Should Veridane build or buy hosted compute for builds?" -> playbook row: strategy, build vs buy
  Question match:   mismatched: answered "how would you pick a vendor", asked "should we own this"
  Altitude:         L 0 / F 3 / N 3, F share 100% -> tactical (gate: L at least 2x F)
  Investment test:  missing (never says whether owning compute moves the top line or only saves a fee)
  Repeatability:    none (no sentence on how Dana decides build vs buy in general)
  Coherence:        holds; reasons S 0 / T 1 ("move fast" is true, not strategic)
  Level read:       reads one level below the target: personal execution, no outcome through the org
  Claims:           1 number, 1 in ledger (claim_check: 0 fail)
  Diagnosis:        thinking gap
```

## Coaching memo

**Executive summary.** The answer is a competent vendor-selection plan, and that is the
problem: the question asked whether Veridane should own this capability at all. This is
a thinking gap, so another mock will not fix it. The single change: open with the
investment test and a one-line answer.

**STOP 1: process before position.**
- You said: "So I'd start by looking at the vendor landscape."
- Why it hurts: a VP answer leads with the call; the interviewer now waits through a
  process to find out whether you have one.
- Try this: "Buy the compute, build the scheduling."
- Why it is better: fixes question match and puts the answer in sentence one.

**START 1: the investment test.**
- What is missing: whether owning compute is an investment (moves the top line, protects
  a moat) or an expense (saves a fee).
- Add this: "Raw compute is an expense: every vendor rents the same machines, so building
  it saves a margin and protects nothing."

**START 2: the method sentence.**
- Add this: "When a capability is the same at every vendor, I buy it; when it encodes how
  our own developers work, I build it."
- Why it matters: it lets the interviewer picture you making the next build vs buy call
  at their company.

**CONTINUE 1: the proof point.**
- You said: "At Quillstone we cut median build time 44%."
- Why it works: a real number from the record, tied to the role. Keep it, and add the
  full ledger wording ("in 15 months while holding test pass rates").

## The rewrite (about 60 seconds spoken)

> Buy the compute, build the scheduling. Raw compute is an expense: every vendor rents the
> same machines, so building it saves a margin and protects nothing. The decision about
> which build runs where, and how fast, is the investment, because it protects the core
> business of developers who stay, and Veridane's own build data is a moat no vendor can
> sell. So I would contract two compute vendors behind one scheduling layer and put the
> platform team on caching and placement. -> When a capability is the same at every
> vendor, I buy it; when it encodes how our own developers work, I build it. At Quillstone
> we made the same split, and it is how we cut median build time 44% in 15 months while
> holding test pass rates. What would change my mind: if compute cost is where we lose
> deals, owning it becomes part of the decision.

After: L 3 / F 0 / N 4, strategic. claim_check: 2 numbers, 2 in ledger, 0 fail.

**Next action.** Want the hardest follow-up, and the pushback you have to hold without
adding justifications?
