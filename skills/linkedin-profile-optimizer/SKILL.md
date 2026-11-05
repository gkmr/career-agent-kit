---
name: linkedin-profile-optimizer
description: "LinkedIn profile work for senior product and technology leaders: frame selection, target-level headline, About section, Experience lines, skills and an action plan that fits in two hours. Use for 'optimize my LinkedIn', 'rewrite my headline', 'LinkedIn about section', 'what skills should I add', 'get more recruiter inbound', or a resume-to-LinkedIn consistency check. Every number is checked against the claims ledger and every Experience line against the duties lint before delivery."
---

# LinkedIn profile optimizer

For a senior candidate, LinkedIn is mostly a validation layer: many Director and VP roles
arrive through networks, referrals and search firms, and the profile has to pass a 30 to
60 second credibility check by someone with no shared context. The profile hooks; the
resume closes.

Paths below are relative to the kit's root. Installed as a standalone skill, copy
`references/` and `scripts/` next to this file.

## Why these rules exist

- Every former colleague can see the profile, so an overclaim is caught in public. The
  specificity ladder applies, and a LinkedIn Recommendation is the best defense for a Tier
  3 claim.
- There is one live profile, so the frame decision is binding for all targets at once.
- Recruiter search filters on titles. Pick titles from LinkedIn's autocomplete list so
  they map to a standard title, and stack promotions under one company entry.
- A stranger reads it in under a minute with no context, so the profile has to carry the
  level and the thinking explicitly. Colleagues fill in your depth from history;
  strangers cannot (Nancy Chu, 2026-04-22).
- Do not claim ranking effects you cannot cite. Advice here is about what a human reader
  sees, not about gaming an algorithm.

## Inputs

Profile data (a PDF export is best; pasted text works; a resume as a proxy, flagged), 1 to 3
target titles from live postings with their JDs, the claims ledger, and constraints
(private "open to work" acceptable? anything to mute? posting or passive?).

## Sequence

### Step 0: frame

Choose one: (A) operator-builder, (B) between full-time roles, (C) portfolio career. The
top three targets decide; if they are mixed, ask which cluster comes first. Headline, About
opener, current title, featured items and pinned skills all carry the frame.

### Step 1: target level and JD decode

1. Name the target level and the level the profile reads at now. Up to roughly L7 the
   profile narrates work that was yours; from L8 it narrates outcomes through
   organizations (Nancy Chu, 2026-07-21).
2. Decode the top three bullets of each target JD into problem and crux lines and save
   them as `jd-crux.md` (Nancy Chu, 2026-06-02). They drive the About opener and the
   pinned skills.
3. Write the test sentence: "A recruiter for <target role> reads the headline and the
   first About line and concludes <X>." X must equal the target role before anything else
   is touched. The real record carries the level, never an inflated title (Simon Witten,
   post on pitching at the target level).

### Step 2: audit

A table in recruiter-workflow order: title entry and standard title, keyword coverage,
role stacking, location (search); headline at the target level, photo, private "open to
work" (card); level read, duties-line count, scope and progression, About opener and
how-I-think line (full profile); a tailored resume exists (readiness). Flag title
problems first and the level read second.

### Step 3: headline

Formula: `<target-level standard title> | <domain plus one scale proof point>`. At most
220 characters, no "ex-", no buzzwords, no more than three identities. Any growth number
names where it happened (the claim freeze requires it). No placeholder metrics on a public
surface. Deliver three variants ranked by clarity.

### Step 4: About, in three beats

Under 1,000 characters, two or three short paragraphs:

1. **Aimed opener**: one line aimed at the problem the target teams are hiring to fix
   (from `jd-crux.md`), not a list of scope (Nancy Chu, 2026-10-06).
2. **Proof and the how-I-think line**: two or three what-changed results from the ledger,
   then one method sentence a stranger can picture at their company, for example "When a
   team is behind, I cut active projects before I add headcount; focus is usually the
   bottleneck." (Nancy Chu, 2026-04-18.)
3. **Why this problem, and an opening**: one line in the candidate's own voice that ends
   on an open door, not a list of asks.

No "I am a..." opener, no buzzwords, no em dashes. For VP targets, at least one sentence
narrates an outcome through the org.

### Step 5: Experience

For the top 3 or 4 roles: the standard title, a scope hook on line one, one or two
what-changed lines with JD keywords, promotions stacked, two to four lines per role.

**Change, not duties** (Simon Witten, post on resumes): rewrite any line that opens with
Responsible for, Managed, Oversaw, Worked on, Helped, Supported or Participated as what
changed (a number) for whom and how. Report "duties lines: n -> 0" from
`python3 scripts/altitude_count.py experience.md --duties`.

Early-stage credentials appear wherever they apply, and nowhere the ledger does not carry them.
A Tier 3 claim without a matching Recommendation gets "request a Recommendation from
<former colleague role>".

### Step 6: skills

Crux terms from the JD decode plus the JD's top three skills, checked against
autocomplete, 15 to 25 in total. Pin the three exact JD matches. Unpin legacy skills that
point at the old identity (for an AI product target, "Management Consulting" above
"Product Management" reads wrong) and ask three to five former colleagues to endorse the
pinned ones.

### Step 7: other sections

Patents and Publications (only what the candidate is named on, exactly as supplied),
Honors (say whose award it was), Projects, Featured, Organizations, Volunteering.

### Step 8: two-hour action plan

```
NOW (30 min):    test sentence; headline and first About line; standard titles; stack roles;
                 private "open to work"; location; photo.
THIS WEEK (60):  JD decode; About in three beats; duties lines -> 0; 15-25 skills;
                 scope lines; remove buzzwords and em dashes; claim check every number.
THEN STOP:       tailor the resume per target; five warm outreach messages; one recruiter
                 friend's review.
SKIP UNLESS DONE: banner; skills past 25; About character counting.
```

## Outside check before delivery

Run on the proposed copy and report the counts:

```
python3 scripts/claim_check.py linkedin.md claims-ledger.json
python3 scripts/altitude_count.py linkedin.md --duties
```

Then confirm: em dashes 0; banned words 0; placeholder metrics 0; headline at most 220
characters; About at most 1,000; the target title term in the headline and the first About
line; a method sentence present in About.

## Partial requests

Deliver the section asked for, and flag any critical issue elsewhere in one line.

## Never

Build without a frame and a test sentence; leave a title off the standard list; put a
placeholder metric on a public surface; add a Tier 5 claim; mirror the resume; leave a
headline that contradicts Experience; pin legacy skills; ship a duties line; print a
number, title, date or status the ledger does not carry.

## Files

- `references/playbook.md`, `references/claims-ledger.md`
- `scripts/altitude_count.py`, `scripts/claim_check.py`
- `examples/outputs/linkedin-about.md`: a worked headline and About for an invented candidate
