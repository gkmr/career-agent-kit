# Claims ledger

Why it exists: background checks verify titles and dates first, and reference calls test
accomplishments. A candidate's documents drift over a search (each tailored version adds
a little), and the drift is what gets caught. The ledger is the one place where each fact
has a canonical wording, a status and a source. Every sendable draft is checked against it
by `scripts/claim_check.py`.

Your real ledger is private. Name it `claims-ledger.json` (the repo's `.gitignore` already
excludes that name) and start from `examples/claims-ledger.example.json`, which describes an
invented candidate.

## Shape

```json
{
  "as_of": "2026-10-01",
  "roles": [
    {"id": "quillstone", "employer": "Quillstone Cloud", "aliases": ["Quillstone"],
     "title": "Head of Product, Developer Platform", "start": 2021, "end": "Present",
     "dates_source": "offer letter"}
  ],
  "claims": [
    {"id": "platform-arr", "role": "quillstone", "kind": "growth", "public": true, "status": "verified",
     "text": "Grew the developer platform line from $18M to $63M ARR (3.5x)",
     "provenance": "FY2025 board deck; candidate-confirmed 2026-09-12"},
    {"id": "runners", "role": "quillstone", "kind": "launch", "public": true, "status": "pilot",
     "text": "Ran a 6-week pilot of hosted build runners with 12 design partners"}
  ],
  "forbidden": [
    {"id": "bookings-as-revenue", "pattern": "(revenue|ARR)\\b[^.\\n]{0,30}\\$80M", "severity": "fail",
     "reason": "the $80M is contract bookings, not revenue"},
    {"id": "pilot-as-launch", "pattern": "\\blaunched\\b[^.\\n]{0,40}hosted (build )?runners",
     "when": {"claim": "runners", "status": "pilot"}, "severity": "fail",
     "reason": "hosted runners ran as a pilot; it has not launched"}
  ],
  "anachronisms": [
    {"term": "MCP", "pattern": "\\bMCP\\b", "first_public": 2024, "source": "announced November 2024"}
  ],
  "non_claims": ["\\b\\d+ slides\\b"]
}
```

| Field | Meaning |
|---|---|
| `roles[]` | One per job. `employer` and `aliases` are how drafts name it; `start` and `end` are years (`end` may be `"Present"`) and are checked against any role header with a year range |
| `claims[].text` | The canonical external wording. Every number in it (money, percent, multiplier, count, year) is what drafts are allowed to say |
| `claims[].kind` | `growth` claims must name their role, employer or a tenure year in the sentence, its paragraph or its section header. Other kinds: `scale`, `deal`, `plan`, `launch`, anything descriptive |
| `claims[].public` | `false` marks an internal figure (a plan target, an unannounced number); it fails on external surfaces unless `--surface internal` |
| `claims[].status` | Free text used by `forbidden[].when`, for example `pilot` or `ga` |
| `claims[].proof` | Supporting fields such as `{"link": null}`; `forbidden[].unless_proof` skips a rule once any proof field is filled |
| `forbidden[]` | Regex patterns that must never appear, each with a reason; `when` limits a rule to one claim status |
| `anachronisms[]` | Terms that did not exist before `first_public`; using one inside a role that ended earlier fails |
| `non_claims[]` | Extra patterns for numbers that are not claims (plan lengths, slide counts). Defaults already cover durations in seconds, minutes and days, "top 5", "3 of 5", "L7", "Q3" and labels like "week 3" |

## Rules

1. The newest explicit confirmation from the candidate wins, and is written into the
   ledger with a date and the words used. Older resume text never reverts it.
2. Unknown status gets neutral wording. Proof is asked for, never invented (no customer
   name, link or date until the candidate supplies one).
3. External surfaces use public figures. Internal figures stay internal.
4. Metric types stay exact: bookings are not revenue, a pilot is not a launch, a plan target
   is not a result, and an org that includes contractors is not that many employees.
5. Work the candidate supported but did not author is described as supported.
6. A new product or protocol name gets an anachronism row the day it first appears in a
   draft.
7. When a check is wrong, fix the ledger or the gate, not the draft that exposed it.

## What the check does not do

- Spelled-out numbers ("tripled", "three teams") are not checked. Write claims in digits.
- Bare counts match by value. A "7" that means years passes if a 7 in the ledger means
  product leads; the tenure check catches the common "over N years" case.
- It cannot tell a true sentence from a false one when the sentence has no number and
  matches no forbidden pattern. That is the reference-check pre-flight's job.
