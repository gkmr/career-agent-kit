#!/usr/bin/env python3
"""altitude_count.py - count lever and feature sentences in a pitch, answer or summary.

A lever sentence works at the level of the bet: the business line, the moat, revenue or
margin, a decision and its trade-off, an outcome reached through an organization. A
feature sentence works at the level of the tactic: a capability, a tool, a process step,
a meeting cadence, a metric mechanic. Senior readers hear a draft full of feature
sentences as tactical, however strong the results inside it.

The gate: lever sentences outnumber feature sentences at least 2 to 1. That is the same
line as "features are at most a third of tagged sentences". Neutral sentences (no signal
either way) are reported but not counted, so filler cannot pad the lever side.

Method credit: the lever/feature split and the one-third line paraphrase a newsletter
essay by Nancy Chu on strategy-round altitude (2026-06-23). The duties lint paraphrases a
resume post by Simon Witten. See references/playbook.md for both.

Usage:
  python3 scripts/altitude_count.py pitch.md                  per-sentence tags and totals
  python3 scripts/altitude_count.py pitch.md --duties         also flag duties lines
  python3 scripts/altitude_count.py pitch.md --json           machine-readable
  python3 scripts/altitude_count.py pitch.md --gate           exit 1 if the ratio or duties check fails
  python3 scripts/altitude_count.py pitch.md --min-ratio 3    stricter ratio
  python3 scripts/altitude_count.py --calibrate tags.tsv      sentence<TAB>L|F|N, prints agreement

The lexicon is a starting point, not a classifier. Calibrate it on 40 hand-tagged
sentences from your own material; keep it only at 34 of 40 agreement or better, and fix
the lexicon, never the tags.

Python 3.8+, standard library only.
"""
from __future__ import annotations

import json
import re
import sys

LEVER = [
    r"\bbets?\b", r"\bbet on\b", r"\bmoats?\b", r"\btop[- ]?line\b", r"\bline of business\b",
    r"\bbusiness line\b", r"\bcore business\b", r"\bstrateg", r"\binvest(ment|ing|ed)?\b",
    r"\bexpense\b", r"\bdecid", r"\bdecisions?\b", r"\bP&L\b", r"\bARR\b", r"\brevenue\b",
    r"\bmargins?\b", r"\bunit economics\b", r"\bcost to serve\b", r"\bpric(e|es|ed|ing)\b",
    r"\bbusiness model\b",
    r"\bthrough (the |my |our |their )?(\w+ ){0,2}(org|organization|teams|PMs|leads|managers|directors)\b",
    r"\btrade-?offs?\b", r"\bfocus(ed)?\b", r"\bpriorit", r"\bmission\b", r"\bmarkets?\b",
    r"\bcustomers? (want|need|pay|buy|churn|stay|leave|trust)", r"\bretention\b", r"\bchurn\b",
    r"\bgrowth\b", r"\bgrew\b", r"\bscale\b", r"\blosses\b", r"\bcompetitive\b", r"\bwhy\b",
    r"\bportfolio\b", r"\bgo-to-market\b", r"\bstopped\b", r"\bkill(ed)?\b", r"\bsaid no\b",
]
FEATURE = [
    r"\bdashboards?\b", r"\bmeetings?\b", r"\bkpis?\b", r"\bokrs?\b", r"\bsprints?\b",
    r"\bbacklogs?\b", r"\broadmaps?\b", r"\bprocess(es)?\b", r"\bworkflows?\b", r"\btool(s|ing)?\b",
    r"\bfeatures?\b", r"\bbuttons?\b", r"\bscreens?\b", r"\bapis?\b", r"\bsdks?\b", r"\bpipelines?\b",
    r"(?<!business )(?<!operating )(?<!pricing )\bmodels?\b", r"\bprompts?\b", r"\bjira\b",
    r"\bnotion\b", r"\bslack\b", r"\bweekly\b", r"\bcadence\b", r"\bstandups?\b", r"\btickets?\b",
    r"\bspecs?\b", r"\bprds?\b", r"\ba/b\b", r"\bexperiments?\b", r"\binstrument", r"\bintegrat",
    r"\bmigrat", r"\bconfigur", r"\btemplates?\b", r"\bspreadsheets?\b", r"\bset up\b",
    r"\brolled out\b", r"\bautomat", r"\bclaude code\b", r"\bcursor\b", r"\bcodex\b",
]
LEVER_RX = [re.compile(p, re.I) for p in LEVER]
FEATURE_RX = [re.compile(p, re.I) for p in FEATURE]

DUTIES = re.compile(
    r"^\s*(?:[-*\u2022]\s*)?(?:[^:\n]{1,40}:\s*)?(responsible for|managed|oversaw|worked on|helped|supported|participated)\b",
    re.I)
WAS_RESPONSIBLE = re.compile(r"\b(i was|was|were) responsible for\b", re.I)
LED_NO_OUTCOME = re.compile(
    r"^\s*(?:[-*\u2022]\s*)?(?:[^:\n]{1,40}:\s*)?led\s+(a |an |the |my )?([\w-]+ ){0,3}?"
    r"(team|teams|org|organization|group|function|pms?|engineers?)\b", re.I)
OUTCOME = re.compile(
    r"(\d|%|\$|\bgrew\b|\bcut\b|\breduced\b|\bincreased\b|\braised\b|\bshipped\b|\blaunched\b|"
    r"\bclosed\b|\bresolved\b|\bfrom .+ to\b)", re.I)
SENTENCE_SPLIT = re.compile(r"(?<=[.!?])[\"')\]]?\s+(?=[A-Z0-9\"'(])")
LIST_ITEM = re.compile(r"^\s*(?:[-*\u2022]|\d{1,2}[.)])\s+")


def clean(line: str) -> str:
    line = re.sub(r"`[^`]*`", " ", line)
    line = re.sub(r"\*\*|__", "", line)
    line = re.sub(r"^\s*>\s?", "", line)
    return line


def units(text: str):
    """Split text into taggable units: list items stand alone; prose is split into sentences.

    Markdown headings, table rows and code fences are skipped: they are labels, not claims.
    """
    out, para = [], []
    in_fence = False

    def flush():
        if para:
            flat = re.sub(r"\s+", " ", " ".join(para)).strip()
            out.extend(s.strip() for s in SENTENCE_SPLIT.split(flat) if len(s.strip()) > 2)
            para.clear()

    for raw in text.splitlines():
        if raw.strip().startswith("```"):
            in_fence = not in_fence
            flush()
            continue
        if in_fence:
            continue
        line = clean(raw)
        if not line.strip() or re.match(r"^\s*#", line) or re.match(r"^\s*\|", line):
            flush()
            continue
        if LIST_ITEM.match(line):
            flush()  # a list item starts its own unit and runs until the next item or a blank line
            para.append(LIST_ITEM.sub("", line))
            continue
        para.append(line)
    flush()
    return out


def tag(sentence: str) -> str:
    """L (lever), F (feature) or N (neutral). Ties with any signal go to F."""
    lever = sum(1 for rx in LEVER_RX if rx.search(sentence))
    feature = sum(1 for rx in FEATURE_RX if rx.search(sentence))
    if lever == 0 and feature == 0:
        return "N"
    return "L" if lever > feature else "F"


def duties_lint(text: str):
    """Lines or sentences that describe a job instead of a change.

    Flags a line that opens with a duties verb (Responsible for, Managed, Oversaw, Worked
    on, Helped, Supported, Participated), any sentence with "was responsible for", and
    "Led <team noun>" with no outcome in the same line.
    """
    hits = []
    for line in text.splitlines():
        stripped = clean(line).strip()
        if not stripped or stripped.startswith("#"):
            continue
        if DUTIES.search(stripped):
            hits.append(stripped)
            continue
        if LED_NO_OUTCOME.search(stripped) and not OUTCOME.search(stripped):
            hits.append(stripped)
            continue
        for sentence in SENTENCE_SPLIT.split(stripped):
            if WAS_RESPONSIBLE.search(sentence):
                hits.append(sentence.strip())
    return hits


def count(text: str, min_ratio: float = 2.0, duties: bool = False) -> dict:
    tags = [(tag(s), s) for s in units(text)]
    lever = sum(1 for t, _ in tags if t == "L")
    feature = sum(1 for t, _ in tags if t == "F")
    neutral = len(tags) - lever - feature
    tagged = lever + feature
    ratio = (lever / feature) if feature else (float("inf") if lever else 0.0)
    passed = lever > 0 and (feature == 0 or lever >= min_ratio * feature)
    result = {
        "L": lever, "F": feature, "N": neutral,
        "ratio": None if ratio == float("inf") else round(ratio, 2),
        "min_ratio": min_ratio,
        "F_share": round(feature / tagged, 2) if tagged else 0.0,
        "verdict": "strategic" if passed else "tactical",
        "pass": passed,
        "tags": tags,
    }
    if duties:
        result["duties_lines"] = duties_lint(text)
        result["pass"] = result["pass"] and not result["duties_lines"]
    return result


def calibrate(path: str):
    rows = []
    with open(path, encoding="utf-8") as fh:
        for raw in fh:
            if raw.startswith("#") or "\t" not in raw:
                continue
            sentence, want = raw.rstrip("\n").rsplit("\t", 1)
            rows.append((sentence, want.strip().upper()))
    misses = [(s, w, tag(s)) for s, w in rows if tag(s) != w]
    return len(rows) - len(misses), len(rows), misses


def main(argv=None) -> int:
    argv = list(sys.argv[1:] if argv is None else argv)
    if not argv or argv[0] in ("-h", "--help"):
        print(__doc__)
        return 2
    if "--calibrate" in argv:
        agree, total, misses = calibrate(argv[argv.index("--calibrate") + 1])
        print("agreement %d/%d" % (agree, total))
        for s, want, got in misses:
            print("  MISS want %s got %s: %s" % (want, got, s[:90]))
        return 0 if total and agree * 40 >= 34 * total else 1
    min_ratio = 2.0
    if "--min-ratio" in argv:
        min_ratio = float(argv[argv.index("--min-ratio") + 1])
    paths = [a for i, a in enumerate(argv) if not a.startswith("--") and
             (i == 0 or argv[i - 1] != "--min-ratio")]
    if not paths:
        print("altitude_count.py: no input file", file=sys.stderr)
        return 2
    path = paths[0]
    if path == "-":
        text = sys.stdin.read()
    else:
        with open(path, encoding="utf-8") as fh:
            text = fh.read()
    res = count(text, min_ratio, duties="--duties" in argv)
    if "--json" in argv:
        out = dict(res)
        out["tags"] = [{"tag": t, "sentence": s} for t, s in res["tags"]]
        print(json.dumps(out, indent=2))
    else:
        for t, s in res["tags"]:
            print("%s  %s" % (t, s))
        ratio = "no feature sentences" if res["ratio"] is None else "ratio %.1f" % res["ratio"]
        print("\nL %d / F %d / N %d  %s (need %.1f)  F share %d%%  -> %s"
              % (res["L"], res["F"], res["N"], ratio, min_ratio, round(res["F_share"] * 100), res["verdict"]))
        if "duties_lines" in res:
            print("duties lines: %d" % len(res["duties_lines"]))
            for d in res["duties_lines"]:
                print("  %s" % d)
    if "--gate" in argv:
        return 0 if res["pass"] else 1
    return 0


if __name__ == "__main__":
    sys.exit(main())
