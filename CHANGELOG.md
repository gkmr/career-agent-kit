# Changelog

## 1.0.0 (2026-11-05)

First public release, built from the author's private career skills with all personal
data removed and an invented candidate in its place.

- Skills: `interview-coach` (scorecard with a thinking audit), `resume-tailor` (frame,
  JD crux, target-level test, claim freeze, gates), `linkedin-profile-optimizer` (three-beat
  About, change-not-duties), `job-loop-prep` (crux, pitch, one-pager, mock set,
  follow-through as proposed tasks through an optional adapter).
- `scripts/altitude_count.py`: lever, feature and neutral tags; the gate is levers at least
  2x features. Changed from the private version: sentences with no signal are now neutral
  instead of counting as levers; list items that wrap across lines stay one unit; duties
  lint catches "Label: Managed ..." bullets and "Led the product team" with no outcome.
- `scripts/claim_check.py`: new. Ledger membership for every number, private figures,
  growth bound to its role, misattribution, tenure spans, role dates, forbidden patterns
  (with status conditions and proof exemptions), anachronisms.
- `references/playbook.md`: methods from Nancy Chu and Simon Witten, paraphrased in my own words
  and credited by name and date.
- `evals/`: the resume-tailor suite ported to an invented candidate, 30 evals, with script
  graders proven on pass and fail fixtures.
- The invented candidate (developer tools) carries its own trap set: bookings stated as revenue,
  a pilot stated as a launch, contractors counted as employees, a plan target stated as a result.
- 75 unit tests and a 40-sentence calibration set (36 of 40 agreement, bar 34).
