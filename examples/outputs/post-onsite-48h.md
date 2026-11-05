# Post-onsite artifact (sent within 48 hours)

Example output of the job-loop-prep follow-through step. The panel pushed hardest on one
question; this note answers it better than the room allowed, in one page.

**To:** the hiring manager (forwardable to the panel)
**Subject:** Who owns the wait - a first-quarter sketch

Thank you for Tuesday. The question I keep coming back to is the one the head of
engineering asked: who should own the time a developer waits between commit and a
running build?

My answer, sketched for the first quarter:

1. **Weeks 1 to 4, map the wait.** List every step between commit and a running build,
   and who owns each step today. I expect more owners than steps.
2. **Weeks 5 to 8, name one owner per step.** Product owns the build path, engineering
   owns the latency budget, security signs the design review before build, not after.
3. **Weeks 9 to 12, one shared measure.** Paid adoption and build wait reported against
   the same definition of an active team, so neither goal can win by moving the other.

At Quillstone this is the split that let us cut median build time 44% in 15 months while
holding test pass rates. I would expect Veridane's version to differ in the details: two
segments, stricter enterprise buyers, and a hosted compute decision still open.

Happy to walk through it with the team.

Dana
