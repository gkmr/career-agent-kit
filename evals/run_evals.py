#!/usr/bin/env python3
"""run_evals.py - run the script-graded part of the resume-tailor eval suite.

Two modes:

  python3 evals/run_evals.py
      Self-test. For every eval with a grader, the grader must PASS the eval's pass
      fixture and FAIL its fail fixture. This proves the outside judges work before you
      trust them on real output. Model- and docx-judged evals are listed, not run.

  python3 evals/run_evals.py --grade 24 my-resume.md
      Grade one real output against one eval's script grader.

Exit status: 0 when every grader separates its fixtures (or the graded output passes),
1 otherwise. Python 3.8+, standard library only, no network.
"""
from __future__ import annotations

import json
import os
import re
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(ROOT, "scripts"))
import altitude_count  # noqa: E402
import claim_check  # noqa: E402

SUITE = os.path.join(ROOT, "evals", "resume-tailor.evals.json")

BANNED = ["leverage", "ecosystem", "synergy", "spearhead", "navigate", "journey", "roadmap",
          "passionate", "highly skilled", "results-driven", "dynamic", "obsessed", "cutting-edge",
          "transformative", "world-class", "best-in-class", "robust", "hands-on"]
BANNED_RX = re.compile(r"\b(%s)\w*" % "|".join(re.escape(w) for w in BANNED), re.I)
EM_DASH = re.compile("\u2014|(?<=\\w) -- (?=\\w)|(?<=[A-Za-z])--(?=[A-Za-z])")
DOUBLE_SPACE = re.compile(r"\S  +\S")
DEGREE = re.compile(r"\b(B\.?A\.?|B\.?S\.?|B\.?Sc\.?|B\.?Eng\.?|BA|BS|Bachelor'?s?|A\.?B\.?)\b")
YEAR = re.compile(r"\b(19|20)\d{2}\b")
BULLET = re.compile(r"^\s*[-*\u2022]\s+")
METRIC = re.compile(r"\d|\bXX+\b|XX")
THROUGH_ORG = re.compile(
    r"\bthrough (the |my |our |their |a )?(\w+[- ]?){0,3}(org|organization|teams|leads|PMs|managers|directors)\b", re.I)
TEST_SENTENCE = re.compile(r"\bA recruiter for .+? reads .+? concludes .+", re.I)


def read(rel):
    with open(os.path.join(ROOT, rel), encoding="utf-8") as fh:
        return fh.read()


# ---------------------------------------------------------------- graders
# Each grader takes (text, grader_config) and returns (passed: bool, detail: str).

def g_claim_check(text, cfg):
    ledger = claim_check.load_ledger(os.path.join(ROOT, cfg.get("ledger", "examples/claims-ledger.example.json")))
    findings, checked, matched = claim_check.check(text, ledger)
    fails = [f for f in findings if f.severity == "fail"]
    return not fails, "%d fail (%s)" % (len(fails), ", ".join(sorted({f.rule for f in fails})) or "none")


def g_altitude(text, cfg):
    r = altitude_count.count(text, cfg.get("min_ratio", 2.0))
    return r["pass"], "L %d / F %d / N %d" % (r["L"], r["F"], r["N"])


def g_duties(text, cfg):
    hits = altitude_count.duties_lint(text)
    return not hits, "%d duties lines" % len(hits)


def g_text_hygiene(text, cfg):
    banned = BANNED_RX.findall(text)
    dashes = EM_DASH.findall(text)
    doubles = DOUBLE_SPACE.findall(text)
    ok = not banned and not dashes and not doubles
    return ok, "banned %d, em dashes %d, double spaces %d" % (len(banned), len(dashes), len(doubles))


def g_undergrad_year(text, cfg):
    bad = [l for l in text.splitlines() if DEGREE.search(l) and YEAR.search(l)
           and not re.search(r"\b(M\.?B\.?A|M\.?S|Ph\.?D|Master)", l, re.I)]
    return not bad, "%d degree lines with a year" % len(bad)


def g_xx_discipline(text, cfg):
    bullets = [l for l in text.splitlines() if BULLET.match(l)]
    metric = [l for l in bullets if METRIC.search(l)]
    xx = [l for l in metric if re.search(r"XX", l)]
    top_three = [l for l in bullets[:3] if re.search(r"XX", l)]
    share = len(xx) / len(metric) if metric else 0.0
    ok = share <= 0.25 and len(xx) <= 4 and not top_three
    return ok, "XX on %d of %d metric bullets, %d in the top 3" % (len(xx), len(metric), len(top_three))


def g_level_read(text, cfg):
    n = len(THROUGH_ORG.findall(text))
    return n > 0, "%d through-the-org sentences" % n


def g_test_sentence(text, cfg):
    ok = bool(TEST_SENTENCE.search(text))
    return ok, "test sentence %s" % ("present" if ok else "missing")


def g_crux_file(text, cfg):
    lines = [l for l in text.splitlines() if re.match(r"^\s*\d+\.\s", l) and re.search(r"\bcrux\b", l, re.I)]
    assumption = bool(re.search(r"^\s*Assumption", text, re.M))
    return len(lines) >= 6 and assumption, "%d crux lines, assumption line %s" % (
        len(lines), "present" if assumption else "missing")


GRADERS = {
    "claim_check": g_claim_check, "altitude": g_altitude, "duties": g_duties,
    "text_hygiene": g_text_hygiene, "undergrad_year": g_undergrad_year,
    "xx_discipline": g_xx_discipline, "level_read": g_level_read,
    "test_sentence": g_test_sentence, "crux_file": g_crux_file,
}


# ---------------------------------------------------------------- runner

def load_suite(path=SUITE):
    with open(path, encoding="utf-8") as fh:
        return json.load(fh)


def self_test(suite, out=sys.stdout):
    rows, bad = [], 0
    unscripted = []
    for ev in suite["evals"]:
        g = ev.get("grader")
        if not g:
            judges = sorted({a.get("judge", "model") for a in ev["assertions"]})
            unscripted.append((ev["id"], ev["name"], "/".join(judges)))
            continue
        fn = GRADERS[g["name"]]
        ok_pass, d_pass = fn(read(ev["fixtures"]["pass"]), g)
        ok_fail, d_fail = fn(read(ev["fixtures"]["fail"]), g)
        good = ok_pass and not ok_fail
        bad += 0 if good else 1
        rows.append((ev["id"], ev["name"], g["name"], ok_pass, d_pass, ok_fail, d_fail, good))
    print("Script-graded evals: each grader must pass the pass fixture and fail the fail fixture\n", file=out)
    for i, name, g, okp, dp, okf, df, good in rows:
        print("%-4s %2d %-38s %-14s pass fixture: %-4s (%s) | fail fixture: %-4s (%s)" % (
            "ok" if good else "BAD", i, name, g, "pass" if okp else "fail", dp,
            "pass" if okf else "fail", df), file=out)
    scripted_assertions = sum(1 for ev in suite["evals"] for a in ev["assertions"] if a.get("judge") == "script")
    total_assertions = sum(len(ev["assertions"]) for ev in suite["evals"])
    print("\nNot run here (need a model, a human, or a rendered docx):", file=out)
    for i, name, judges in unscripted:
        print("     %2d %-38s judge: %s" % (i, name, judges), file=out)
    print("\n%d of %d evals script-graded, %d fixture checks, %d wrong. %d of %d assertions are script-judged."
          % (len(rows), len(suite["evals"]), 2 * len(rows), bad, scripted_assertions, total_assertions), file=out)
    return bad


def grade(suite, eval_id, path):
    ev = next((e for e in suite["evals"] if e["id"] == eval_id), None)
    if not ev or not ev.get("grader"):
        print("eval %s has no script grader" % eval_id, file=sys.stderr)
        return 2
    with open(path, encoding="utf-8") as fh:
        text = fh.read()
    ok, detail = GRADERS[ev["grader"]["name"]](text, ev["grader"])
    print("%s  eval %d %s: %s" % ("PASS" if ok else "FAIL", eval_id, ev["name"], detail))
    return 0 if ok else 1


def main(argv=None):
    argv = list(sys.argv[1:] if argv is None else argv)
    suite = load_suite()
    if argv[:1] == ["--grade"] and len(argv) == 3:
        return grade(suite, int(argv[1]), argv[2])
    if argv:
        print(__doc__)
        return 2
    return 1 if self_test(suite) else 0


if __name__ == "__main__":
    sys.exit(main())
