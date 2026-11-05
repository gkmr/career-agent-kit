---
name: job-loop-prep
description: "Interview loop kit for a named company and role: JD crux decode, a 90-second pitch that passes the altitude test, a strategy one-pager, a leave-behind, a mock question set from the shared playbook, and the post-onsite follow-through (a 48-hour artifact and thank-you notes) proposed as tasks. Use for 'prep my loop', 'onsite prep', 'interview kit for <company>', 'decode this JD'. Every number is frozen to the claims ledger."
---

# Job loop prep

Build the kit for one interview loop, the way a product team prepares a launch: a spec
(the JD crux), the launch artifacts (pitch, one-pager, leave-behind), a beta with outside
judges (the mock set, scored by interview-coach), and the post-launch follow-through.
Career-critical work: do it fully, or say exactly what is missing.

Paths below are relative to the kit's root. Installed as a standalone skill, copy
`references/` and `scripts/` next to this file.

## Frame

You need the company, the role, the loop stage, the interviewers' roles and the date. Ask
once, up front, for anything missing that changes the kit; proceed on the rest.

## Gather before building

Research first, format second. Sources: the JD; the candidate's claims ledger (every
number); the interviewers' public background (role, team, what they have written); the
company's own product and vocabulary; `references/playbook.md`. Never rely on memory for a
number.

## Step 0: JD crux decode

Read the JD bullet by bullet. For each of the top 6, one line: the problem the team cannot
solve yet, and the crux, the one input without which the others produce nothing ("ensure
teams operate efficiently" is about cohesion, not more planning; "own executive
communication for accountability" says accountability is not happening on its own and needs
a visible system plus an executive sponsor). A word repeated three or more times is the
hiring manager circling a pain; write the hypothesis. Then one assumption-busting line:
what this team assumes about the problem that the rest of the industry does not, said back
in plain language. Save as `jd-crux.md`. It is page one of the kit and the input to every
later step. (Nancy Chu, 2026-06-02.)

## Claim freeze

Every number in the kit matches the ledger wording. Every growth claim names the role it
happened in. Never say a result was achieved when the truth is that it was set up or
started. A claim not in the ledger is left out, or marked as needing a reference before it
is said out loud. Run:

```
python3 scripts/claim_check.py pitch.md claims-ledger.json
```

## Build four artifacts

1. **The pitch.** A 90-second opener in the playbook's "tell me about yourself" shape: one
   line of experience aimed at the JD crux, why this team now, and a question back (Nancy
   Chu, 2026-10-06). Plant decision rights early. Run the altitude test: lever sentences
   (the bet, the moat, the business line, the org outcome) at least 2x feature sentences
   (Nancy Chu, 2026-06-23):

   ```
   python3 scripts/altitude_count.py pitch.md --duties --gate
   ```

2. **The one-pager.** The strategy artifact in the company's own vocabulary. It opens with
   the investment case (does owning this move the top line or protect a moat, or does it
   only save a fee), then the two or three moves, then how the org would know it is working
   (Nancy Chu, 2026-06-30; Simon Witten, post on strategy into delivery). Wireframes in the body, frameworks in
   the appendix.
3. **The leave-behind.** One page they keep, built around the one question you want them
   arguing about after you leave, taken from the assumption-busting line in `jd-crux.md`.
4. **The mock set.** The 8 most likely questions for this loop and these interviewers. For
   each: its playbook row (what it really tests, the shape that clears the bar, the
   source), the candidate's story that fits, and the one method sentence for that story
   (Nancy Chu, 2026-04-18). Strategy and product sense prompts carry the four investment
   tests; conflict prompts carry the escalation shape; people-management prompts carry the
   portfolio model. Hand the set to interview-coach, which returns a scorecard with the
   thinking audit.

## Rehearse, do not just write

Every story gets a 30-second and a 2-minute version; the core stories also get 10
minutes. Say them out loud; reading is not rehearsing. For VP loops, each core story
narrates an outcome through the org, not only work that was the candidate's own (Nancy
Chu, 2026-07-21).

## Follow-through (adapters)

The follow-through is a list of proposed tasks, not actions. The skill never sends a
message or writes to a task manager itself. It emits one JSON object per line for an
optional adapter to apply:

```json
{"adapter": "tasks", "loop": "<company-role>", "kind": "post-onsite-artifact", "title": "Send the 48-hour follow-up artifact to the hiring manager", "due": "YYYY-MM-DD", "source": "post-onsite-48h.md"}
{"adapter": "tasks", "loop": "<company-role>", "kind": "thank-you", "title": "Thank-you note: <interviewer role>", "due": "YYYY-MM-DD"}
```

- **post-onsite-artifact**, due within 48 hours of the onsite: one page that answers the
  question the panel pushed hardest on, better than the room allowed. It passes the claim
  freeze like any other sendable draft.
- **thank-you**, due the day after: one per interviewer, each naming something specific
  from that conversation.

Adapter interface: read the JSON lines from stdin or a file, create one task per line in
the user's own tool, and print what was created. With no adapter configured, write the
lines to `followups.jsonl` and show them to the user. Draft any note the candidate will
send with a drafting skill that enforces their voice (for example drafting-harness), and
run its gates.

## Deliver

The artifacts as files (`jd-crux.md`, the pitch, the one-pager, the leave-behind, the mock
set, `followups.jsonl`), plus a five-line summary with the gate counts. A notification
adapter is optional and follows the same pattern: propose the message, never send it from
this skill.

## Outside check before delivery

Report each count in the summary:

- pitch: lever sentences at least 2x feature sentences, duties lines 0 (`altitude_count.py`)
- every sendable artifact: 0 claim_check failures
- `jd-crux.md`: one line per top-6 bullet, plus the repeated-word hypothesis and the
  assumption line
- mock set: a playbook row cited for every question
- no em dashes; no banned words

## Sources

Nancy Chu: 2026-04-18 (method sentence), 2026-06-02 (JD decode, assumption busting),
2026-06-23 (altitude), 2026-06-30 (four investment tests), 2026-07-21 (L7 vs L8+),
2026-09-29 (escalation), 2026-10-06 (tell me about yourself), 2026-10-20 (people
management). Simon Witten: posts on strategy into delivery, tell me about yourself, and
questions for us. Paraphrased with citations in `references/playbook.md`.

## Files

- `examples/outputs/`: a full kit for an invented candidate and an invented JD
  (`jd-crux.md`, `pitch.md`, `pitch-v0-before.md`, `mock-set.md`, `post-onsite-48h.md`,
  `followups.jsonl`).
