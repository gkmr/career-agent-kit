# Executive question playbook

Methods are paraphrased in my own words; read the originals for the full argument.

Shared by all four skills. One row per question type: what the question really tests, and
the shape of an answer that clears the bar at Director or VP level. Never paste a row as a
script; rewrite the candidate's own material into the shape. Every row names its source,
and a method with no source does not go into a skill.

Sources are public writing by two practitioners: Nancy Chu's newsletter essays for product
leaders preparing for senior interviews (cited as **Chu** plus the essay date), and Simon
Witten's public posts on hiring senior leaders (cited as **Witten** plus the post's topic;
read as an archive on 2026-10-17). **Kit** marks a method from this repo. Neither author
reviewed or endorsed this kit; if a paraphrase gets a method wrong, the error is mine.

## Question types

| Question | What it really tests | Shape that clears the bar | Source |
|---|---|---|---|
| Tell me about yourself | Whether the opener is aimed at this team's need; connection as much as competence | One line of experience pointed at the team's stated problem, why this team now, and optionally a question back. 30 to 60 seconds, with present, past, future underneath | Chu 2026-10-06; Witten, tell me about yourself |
| Project you are most proud of | The standard you hold yourself to | Choose it for what it shows about your values and how you lead, not for its size; lead with the value | Chu 2026-08-18, 2026-04-16 |
| Greatest achievement | How you define success, how much was you, whether it transfers | Define success, separate your part from the team's, end on the method you would reuse | Witten, greatest achievement |
| A failure | Ownership and recovery | Most of the answer is what happened next: one decision you own, one behavior you changed since | Witten, failure |
| Conflict, disagreed with a manager, difficult stakeholder | Team vs company; speak up, keep the relationship, back the final call | Make it productive first: learn what the other leader is measured on and find the shared goal. Escalate only when you agree on the facts, still disagree, and neither of you can make the trade-off; go together, with options and the cost of each. Then commit fully, including to a call you argued against | Chu 2026-09-29; Witten, disagreeing with your manager; Witten, difficult stakeholders |
| Leadership style, high or low performer, letting someone go, promotion | One consistent way of leading across the team life cycle; the risk of the work, not only the skill of the person | Treat the team as a portfolio: hire, set up, grow, debug, manage out, learn, and feed what you learn back into hiring. Name the stage, answer from one philosophy, weigh how risky the work is (hand it over and stay close) | Chu 2026-10-20; Witten, leadership style |
| First 30 days | Understanding before changing | Learn the business, the people and the real problem; say what you would deliberately not touch yet | Witten, first 30 days |
| Strategy: should X do Y, build vs buy, enter a market | Altitude: the bet behind the metric | Open with investment vs expense. Four tests: fits the mission; strengthens the core business; builds on an existing strength; has a demand signal that feeds the core business. Pick the option with the strongest line to the core business and hold it under pushback instead of stacking up more reasons | Chu 2026-06-23, 2026-06-30, 2026-09-01 |
| Grow or 10x this product | Reimagine vs improve | 2x makes the same product somewhat better than its direct rivals. 10x starts from what the user is really there to do and competes with everything that meets that need. Propose bets only this company can make, then choose one | Chu 2026-08-11 |
| Product sense: design X for Y | The need before the features; coherence end to end | Name the need under the task (momentum, urgency, belonging, a purchase decision, recognition, clarity), say in one sentence what you would build for it, segment users from that crux, then features. Goal, user, problem and solution must not contradict each other | Chu 2026-07-14, 2026-08-25, 2026-09-08 |
| Metrics for an AI product | What the team controls now vs later evidence of value; two-sided loops | A funnel or a flywheel; define a correct outcome and count only those; add guardrails for the harms the main metric hides | Chu 2026-09-22 |
| How AI-native are you | A structure for thinking about AI, one level above tool demos | What AI should and should not do in this product, how you decide, how you take a capability to market. Tools are evidence, not the answer | Chu 2026-07-07 |
| Strategy into delivery | Turning ambition into results, not meetings and dashboards | The bet, the two or three moves, how the org knows it is working, and what you stopped | Witten, strategy into delivery |
| Three words, strengths, work style | Self-awareness, proof, relevance | Word, then evidence, then impact. One strength with a short case. Show that you adapt to the team rather than describing a preferred style | Witten, three words; Witten, strengths; Witten, work style |
| A contrarian belief about the industry | Independent, tested thinking rather than borrowed lines | The belief; what most people believe; why you see it differently; one example where you tested it; what it changes in how you work; stay open to being wrong | Witten, contrarian takes |
| You do not know the answer; critical feedback; everything is urgent | Judgment without ego | Say so plainly, say how you would find out, show the learning loop. For prioritization, give the decision rule rather than the list | Witten, not knowing the answer; Witten, critical feedback; Witten, prioritizing |
| Questions for us | The one part of the interview the candidate leads | Questions that surface the team's unsolved problem (from the JD crux decode); never comp or perks | Witten, questions for us |

## Instruments that cut across questions

- **Question match.** Each question probes one dimension. A proud story is a values story,
  an impact story is a scale story, a hardest-problem story is a decomposition story, a
  conflict story is a trade-off story. The same project can answer any of them with a
  different aperture. (Chu 2026-04-16)
- **Altitude.** Tag every sentence as a lever (the bet, the moat, the business line, an
  outcome through the org, who decides) or a feature (a capability, tactic, process step,
  metric mechanic). When features pass about a third of tagged sentences the answer reads
  tactical; this kit's gate is levers at least 2x features. Counted by
  `scripts/altitude_count.py`. (Chu 2026-06-23)
- **Repeatability.** One sentence that states how you approach this class of problem, so
  the interviewer can picture you doing it at their company. Without it a win sounds like
  a one-time event. A twin test: would your former manager's reference describe it the
  same way? (Chu 2026-04-18; Witten, what your manager would say)
- **Coherence.** Lay the choices out in order (goal, user, problem, solution, metric).
  A later choice must not pull against an earlier one, and a reason that is true is not
  automatically strategic. (Chu 2026-08-25)
- **Level tells.** Up to roughly L7 the work you describe is still yours; from L8 the
  outcomes come through organizations you may not run directly. Senior candidates are
  turned down for answering at the manager level. (Chu 2026-07-21; Witten, Director and VP
  interviews)
- **JD decode.** Treat each JD bullet as a problem the team cannot solve yet. Find the
  crux: the one input without which the others produce nothing. A word repeated three or
  more times is the hiring manager circling a pain. Then name one assumption this team
  makes that the industry does not. (Chu 2026-06-02)
- **Context gap.** Colleagues fill in your depth from shared history; an interviewer or a
  profile reader gets only what you say, so the thinking has to be on the page.
  (Chu 2026-04-22)
- **Change, not duties.** The reader already knows what the job involves. They want what
  changed because you were there, so a line that opens "Responsible for" fails.
  (Witten, resumes)
- **Pitch at the target level.** A resume or profile pitched at your current level gets
  you considered for your current level. The level must be carried by the real record,
  never by an inflated title. (Witten, pitching at the target level; kit)
- **Dimming.** Audit stories for self-caveats about seniority, for the strongest material
  being skipped, and for managing the room's comfort at the cost of the point.
  (Chu 2026-04-13)
- **Thinking gap vs polish gap.** Vague feedback after many mock interviews usually
  signals a thinking gap. More mocks make it worse; calibrate against what good looks like
  at the target level first. (Chu 2026-04-09, 2026-04-10)
- **Weekly drill.** Once a week, explain one recent decision in a single sentence.
  (Chu 2026-05-12)

## Methods from this kit

- **Claim freeze.** Every number in a sendable draft appears in the claims ledger, growth
  claims name the role they happened in, internal figures never leave, and known traps
  fail by name. Checked by `scripts/claim_check.py`. Format: `references/claims-ledger.md`.
- **Specificity ladder.** Tier 1, direct ownership on the public record (a patent or paper
  the candidate is named on, a launch while in the role). Tier 2, led or shipped during
  tenure, verifiable. Tier 3, groundwork for something shipped later, defensible only with
  a named reference. Tier 4, scope attribution ("ran the org that shipped"). Tier 5,
  refused: claiming what you did not build, post-tenure work, or credit on something you
  are not named on.
- **Reference-check pre-flight.** For any claim above Tier 2: a named former colleague who
  can confirm it, tenure dates that cover the work, a public record that agrees, and
  softer fallback wording if the reference declines.
- **Frame decision.** Before writing, decide how the candidate should read: (A) a shipping
  operator, (B) between full-time roles, or (C) a portfolio career. Tagline, summary opener
  and leading title all carry the same frame.
- **48-hour follow-through.** Within two days of an onsite, send one artifact that answers
  the question the panel pushed hardest on, better than the room allowed.

## Sources

Nancy Chu, newsletter essays. One line each: the method as I use it here.

| Date | Title | Method, in my words |
|---|---|---|
| 2026-04-09 | Why top candidates fail, and how clear thinking changes everything | Vague feedback after many mocks points to a thinking gap, not a polish gap |
| 2026-04-10 | Why more practice wasn't the answer | Calibrate against the target level before practicing more |
| 2026-04-13 | Stop dimming your light in interviews | Remove self-caveats and lead with the strongest material |
| 2026-04-16 | Why "make it sound senior" keeps failing | Match the story to the dimension the question probes |
| 2026-04-18 | The pause that creates doubt in behavioral interviews | Add one sentence on how you handle this class of problem |
| 2026-04-22 | Why your colleagues see you as L6, but interviewers don't | Strangers get only what you say, so put the thinking on the page |
| 2026-05-12 | The decision you'd struggle to explain in one sentence | Practice stating one decision a week in one sentence |
| 2026-06-02 | How to read a job description better than 99% of other candidates | Read each bullet as an unsolved problem and find its crux |
| 2026-06-23 | Heading into a product strategy round? Start with your altitude | Frame the move as investment or expense; keep tactics under a third |
| 2026-06-30 | In a product sense interview, do this to sound more strategic | Test options against mission, core business, strength and demand |
| 2026-07-07 | How to answer "how AI native are you" without sounding junior | Answer one level above tools: what AI should do here and how you decide |
| 2026-07-14 | You don't need to prep hundreds of product sense questions | Start from the need under the task, then build from it |
| 2026-07-21 | How to ace your L7, L8, or L9 product leadership interview | From L8, narrate outcomes reached through organizations |
| 2026-08-11 | How to answer "10x Google Gemini" | Separate improving the product from reimagining the job it does |
| 2026-08-18 | "Tell me about a project you're most proud of" as a Director or VP | Pick the story for the values it shows, not its size |
| 2026-08-25 | The two gaps hiding in a strong product sense answer | Check that later choices do not contradict earlier ones |
| 2026-09-01 | What makes a "Should company X do Y?" answer strategic | Assume the company's goal and let it rank the options |
| 2026-09-08 | How to segment users in a Director or VP product sense interview | Segment from the crux; a 2x2 is an output, not a method |
| 2026-09-22 | How to answer AI product metrics interview questions | Count correct outcomes and add guardrails for hidden harms |
| 2026-09-29 | When to escalate a conflict, and how to do it gracefully | Escalate together, with options, only when the trade-off is stuck |
| 2026-10-06 | How to answer "tell me about yourself" in a Director, VP, or CPO interview | Aim the opener at the team's problem, say why this team, ask back |
| 2026-10-20 | How to answer people management interview questions | Treat the team as a portfolio across its whole life cycle |

Simon Witten, public posts on hiring senior leaders, read as an archive on 2026-10-17.
One line each, by topic.

| Topic | Method, in my words |
|---|---|
| Tell me about yourself | Present, past, future in under a minute |
| Greatest achievement | Define success, isolate your part, show it transfers |
| Failure | Spend the answer on what happened next |
| Disagreeing with your manager | Speak up, keep the relationship, back the final call |
| Difficult stakeholders | Solve the problem rather than blame the person |
| Leadership style | Real people, real situations, evidence of results |
| First 30 days | Understand the business before changing it |
| Strategy into delivery | The bet and the moves, not the meetings and dashboards |
| Three words | Each word carries evidence and impact |
| Strengths | Self-awareness, proof and relevance to this role |
| Work style | Show you adapt to the team |
| Contrarian takes | State the belief, the usual view, and how you tested yours |
| Not knowing the answer | Be honest and show how you would find out |
| Critical feedback | Take in the data without ego |
| Prioritizing | Give the decision rule |
| Questions for us | Use the one part you lead to surface their real problem |
| What your manager would say | Expect the reference check to test your story |
| Director and VP interviews | Senior candidates lose by answering at the manager level |
| Resumes | Write what changed because you were there, not the duties |
| Pitching at the target level | Pitch at the level you want, carried by the real record |
