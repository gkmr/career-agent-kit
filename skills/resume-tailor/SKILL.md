---
name: resume-tailor
description: "Executive resume tailoring for Director, VP and C-level product and technology leaders. Use when a resume and a target role appear together, or for 'tailor my resume', 'optimize for <company>', 'rewrite these bullets', 'ATS score', parallel versions for different targets, or claim checks (pilot vs launch, bookings vs revenue, team size scope, internal figures, anachronisms). Decodes the JD crux, sets a frame and a target-level test sentence, enforces a claims ledger, and verifies the result with scripted gates (claim_check.py, altitude_count.py) plus a layout checklist."
---

# Resume tailor

Tailor a senior candidate's resume to a target role so that it reads at the target level
and survives the background check and the reference call.

Paths below are relative to the kit's root. Installed as a standalone skill, copy
`references/` and `scripts/` next to this file.

## Why these rules exist

Executive resumes fail at reference check more often than at the keyword screen.
Candidates round up, reference calls round down, and offers disappear in the gap. Each
tailored version also tends to add a little without removing anything, so drift
compounds. The rules below put an outside judge (the claims ledger and two scripts)
between the model's draft and the send.

## Before anything: BLUF

Open every run with:

```
Goal: <2-3 sentences> | Frame: A, B or C | Target level + test sentence | Prior state | Plan | Risks | ETA
```

Risks always include: page count, placeholder metrics, missing JD keywords, and any claim
above Tier 2 that needs a reference. Get an explicit go-ahead before a major rewrite.
Never iterate, ship, then iterate again.

## Process

1. **Gather inputs.** Resume, the target JD (or JDs), LinkedIn export if any, and the
   claims ledger. Ask once, combined, for whatever is missing.
2. **Frame decision.** Read the candidate as (A) a shipping operator, (B) between
   full-time roles, or (C) a portfolio career (consulting or several part-time roles). If the targets are mixed, ask which
   cluster comes first. Parallel versions build from one base with small overrides.
3. **Source-of-truth sweep.** Titles from the offer letter or the candidate's
   confirmation; dates exact; contradictions asked about, never synthesized; gaps asked
   about, never papered over.
4. **Early-stage audit.** First product hires, early employees, founder roles, open-source
   projects other companies adopted. When present, surface them in the role header, the
   first bullet and one aggregate line. Never claim one the ledger does not carry.
5. **JD signal extraction.** Tier 1 terms (repeated, listed first, required) weigh 1.5x;
   Tier 2 qualifications 1.0x; Tier 3 nice-to-haves 0.5x.
6. **JD crux decode.** For the top 6 bullets, one line each: the problem the team cannot
   solve yet, and the crux (the one input without which the others produce nothing). A
   word repeated three or more times gets its own hypothesis. Save as `jd-crux.md`. The
   rationale maps each summary bullet and each top-3 role bullet to a crux. Keywords still
   drive the match score; the crux decides which proof point leads. (Method: Nancy Chu,
   2026-06-02; see `references/playbook.md`.)
7. **Target-level test.** Write the sentence "A recruiter for <target role> reads the
   tagline and the first summary sentence and concludes <X>." Rewrite the top of page one
   until X is the target role. The real titles and scope carry the level; never inflate a
   title or drop a true one. For VP and above, the summary narrates at least one outcome
   reached through the organization. (Simon Witten, post on pitching at the target
   level; Nancy Chu, 2026-07-21.)
8. **Reference-check pre-flight.** Place every claim on the specificity ladder (below).
   Tier 3 and up needs a named former colleague and fallback wording; Tier 5 is refused
   with a Tier 3 or 4 alternative.
9. **Content budget.** List additions, match them with removals, keep the line count
   net-zero. Warn at three or more additions and make the candidate prioritize.
10. **Claim freeze.** Every claim matches the ledger's status and wording; the newest
    explicit confirmation from the candidate wins and is recorded in the ledger with a
    date.
11. **Build.** Edit the candidate's chosen baseline in place when they have one (exact
    string replacements, layout untouched). Otherwise build fresh with your document
    tooling. This kit does not ship a .docx builder.
12. **Verify** (gates below), then **deliver**: the resume, a clean send copy with no
    version string in the filename or metadata, a rationale (crux mapping, test sentence,
    gate counts), a reference-defense note when Tier 3 claims exist, and a LinkedIn
    hand-off when LinkedIn data was provided.

## Specificity ladder

- **Tier 1, direct ownership on the record**: a patent or paper on which the candidate is
  named, exactly as they supply it; a public launch while the candidate held the role.
- **Tier 2, led or shipped during tenure, verifiable**: "Led <named system>", where tenure
  dates and the public record agree.
- **Tier 3, groundwork for something shipped later**: "Laid foundations for <system>
  carried forward by <team>". Needs a named reference whose tenure overlaps.
- **Tier 4, scope attribution**: "Ran the 70-person org that shipped <category of work>".
  Honest, low differentiation.
- **Tier 5, refused**: claiming to have built what you did not, post-tenure work, credit
  on an artifact you are not named on.

## Gates

Scripted (run them; paste the counts in the rationale):

```
python3 scripts/claim_check.py resume.md claims-ledger.json        # claim freeze
python3 scripts/altitude_count.py summary.md --duties --gate       # altitude and duties
```

| Gate | Rule | How |
|---|---|---|
| Claim ledger | Every number in the ledger; no forbidden pattern; no private figure; growth bound to its role; role dates match | `claim_check.py` (fail) |
| Anachronism | No term inside a role block that became public after the role ended | `claim_check.py` (fail) |
| Duties | No bullet opens with Responsible for, Managed, Oversaw, Worked on, Helped, Supported, Participated; no "Led <team>" without an outcome | `altitude_count.py --duties` (fail) |
| Summary altitude | Lever sentences at least 2x feature sentences in the summary | `altitude_count.py` (warn) |
| Level read | VP and above: one summary sentence narrates an outcome through the org | regex in `evals/run_evals.py` (warn) |
| Text | Zero em dashes, zero banned words, zero double spaces | `evals/run_evals.py` graders |
| Placeholder metrics | XX metrics on at most 25% of metric bullets and at most 4; never on the top 3 bullets, public figures or team sizes | `evals/run_evals.py` grader |
| Education | No undergraduate graduation year | `evals/run_evals.py` grader |
| Layout (checklist) | 2 pages or fewer in the target viewer; body 10.5 to 11 pt; one font family; margins 0.45 to 0.75 in; exact line spacing; tab stops, not spaces or layout tables; 700 to 1,300 words | by hand or your docx tooling |
| Frame | Tagline, summary opener and leading role title carry one frame, at the target level | judgment |
| Match | JD match at least 9.5 of 10 per JD, weighted by tier | judgment, shown as a table |

Banned words: leverage, ecosystem, synergy, spearhead, navigate, journey, roadmap,
passionate, highly skilled, results-driven, dynamic, obsessed, cutting-edge,
transformative, world-class, best-in-class, robust, hands-on. Banned punctuation: em dashes.

## Content rules

- No invention, no title inference, no date rounding, no contradictory synthesis, no Tier
  5 claims, no duties bullets, no undergraduate year.
- Active voice, outcomes over activities, telegraphic bullets; the summary is prose.
- Every number carries what it measures, whose it is and the scope. Check the math
  ($18M to $63M is 3.5x, which is 250% growth, not 350%).
- Public figures on external surfaces; internal figures stay in the ledger.
- Metric types stay exact: bookings are not revenue, a pilot is not a launch, a plan
  target is not a result, and an org that includes contractors is not that many employees.
- Work the candidate supported but did not author is described as supported, never as
  their own.
- Concurrent part-time roles never sit above the main role.
- Summary at the level of the bet: name the business line, the moat, the org outcome.
  Tools belong in role bullets and the skills row; one tooling sentence in the summary is
  fine when it is the JD's own vocabulary.

## Lessons that earned a rule

- Decode the JD before matching it: keyword matching alone produces a high score and a
  resume that reads like everyone else's.
- Change, not duties: the reader knows the job; they want what changed because you were
  there.
- Pitch at the target level and let the record carry it.
- Fix the gate, not the resume: when a check misses or misfires, change the ledger or the
  script so it never happens again.

## Never

Ship without the claim freeze; build without a frame and a test sentence; inflate a title
to pass the level test; mirror the resume onto LinkedIn; add without removing; silently
ship at three pages.

## Files

- `references/playbook.md`, `references/claims-ledger.md`
- `scripts/claim_check.py`, `scripts/altitude_count.py`
- `evals/resume-tailor.evals.json` and `evals/run_evals.py`: the eval suite for this skill
- `examples/outputs/resume.md`, `examples/outputs/jd-crux.md`: worked outputs for an invented candidate
