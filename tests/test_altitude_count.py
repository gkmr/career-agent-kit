"""Tests for scripts/altitude_count.py. Run from the repo root:

    python3 -m unittest discover -s tests -v
"""
import io
import json
import os
import subprocess
import sys
import unittest
from contextlib import redirect_stdout

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(ROOT, "scripts"))
import altitude_count as ac  # noqa: E402

CALIBRATION = os.path.join(ROOT, "tests", "fixtures", "altitude-calibration.tsv")
OUTPUTS = os.path.join(ROOT, "examples", "outputs")


def read(path):
    with open(path, encoding="utf-8") as fh:
        return fh.read()


class Tagging(unittest.TestCase):
    def test_lever_sentence(self):
        self.assertEqual(ac.tag("We bet that build speed was the moat."), "L")

    def test_feature_sentence(self):
        self.assertEqual(ac.tag("We set up a weekly dashboard and a Jira workflow."), "F")

    def test_neutral_sentence_is_not_counted_as_lever(self):
        self.assertEqual(ac.tag("I joined in 2021."), "N")

    def test_ties_go_to_feature(self):
        self.assertEqual(ac.tag("The revenue dashboard."), "F")

    def test_business_model_is_not_a_feature(self):
        self.assertEqual(ac.tag("We changed the business model to price build minutes."), "L")

    def test_through_the_org_with_a_count(self):
        self.assertEqual(ac.tag("Cut build time through seven product leads."), "L")


class Units(unittest.TestCase):
    def test_list_items_stand_alone(self):
        text = "- Grew revenue 3x\n- Built a dashboard\n- Set up sprints"
        self.assertEqual(len(ac.units(text)), 3)

    def test_wrapped_list_item_is_one_unit(self):
        text = "1. Map the decision. List every place a customer\n   can be declined.\n2. Name one owner."
        self.assertEqual(ac.units(text), ["Map the decision.", "List every place a customer can be declined.",
                                          "Name one owner."])

    def test_headings_tables_and_code_are_skipped(self):
        text = "# Pitch\n\n| a | b |\n\n```\nweekly dashboard\n```\n\nWe bet on build speed."
        self.assertEqual(ac.units(text), ["We bet on build speed."])

    def test_bold_markup_is_ignored(self):
        self.assertEqual(ac.units("**Platform line:** grew revenue."), ["Platform line: grew revenue."])


class Ratio(unittest.TestCase):
    def test_two_to_one_passes(self):
        text = "We bet on build speed. Revenue grew. We built a dashboard."
        r = ac.count(text)
        self.assertEqual((r["L"], r["F"]), (2, 1))
        self.assertTrue(r["pass"])
        self.assertEqual(r["verdict"], "strategic")

    def test_below_two_to_one_fails(self):
        text = "We bet on build speed. We built a dashboard. We set up sprints."
        r = ac.count(text)
        self.assertFalse(r["pass"])
        self.assertEqual(r["verdict"], "tactical")

    def test_all_neutral_fails(self):
        self.assertFalse(ac.count("I joined in 2021. Thank you.")["pass"])

    def test_min_ratio_is_configurable(self):
        text = "We bet on build speed. Revenue grew. We built a dashboard."
        self.assertFalse(ac.count(text, min_ratio=3)["pass"])

    def test_neutral_filler_cannot_pad_the_lever_side(self):
        text = "We built a dashboard. Thanks. Great to meet you. Happy to chat."
        r = ac.count(text)
        self.assertEqual((r["L"], r["F"], r["N"]), (0, 1, 3))
        self.assertFalse(r["pass"])


class Duties(unittest.TestCase):
    def test_duties_verbs_fail(self):
        for line in ["- Responsible for the CI roadmap", "Managed a team of PMs",
                     "- **Platform:** Oversaw release operations", "Helped launch the app"]:
            self.assertEqual(len(ac.duties_lint(line)), 1, line)

    def test_was_responsible_for_inside_prose(self):
        hits = ac.duties_lint("I joined in 2021. I was responsible for the CI roadmap.")
        self.assertEqual(hits, ["I was responsible for the CI roadmap."])

    def test_led_needs_an_outcome(self):
        self.assertEqual(len(ac.duties_lint("- Led the product team")), 1)
        self.assertEqual(ac.duties_lint("- Led the product team that cut build time 44%"), [])

    def test_change_lines_pass(self):
        self.assertEqual(ac.duties_lint("- Platform line: grew ARR from $18M to $63M"), [])

    def test_duties_failure_fails_the_count(self):
        r = ac.count("Revenue grew. We bet on build speed.\n- Responsible for the roadmap", duties=True)
        self.assertFalse(r["pass"])


class Calibration(unittest.TestCase):
    def test_lexicon_agrees_with_hand_tags(self):
        agree, total, misses = ac.calibrate(CALIBRATION)
        self.assertEqual(total, 40)
        self.assertGreaterEqual(agree, 34, "lexicon fell below 34/40: %s" % misses)

    def test_misses_never_inflate_levers(self):
        # Known gaps miss toward N (not counted) or, on a tie, toward F. A miss that adds a
        # lever the hand tag did not have would let a tactical draft pass, so it fails here.
        _, _, misses = ac.calibrate(CALIBRATION)
        for sentence, want, got in misses:
            self.assertNotEqual(got, "L", sentence)


class Examples(unittest.TestCase):
    def test_pitch_passes_and_first_draft_fails(self):
        self.assertTrue(ac.count(read(os.path.join(OUTPUTS, "pitch.md")), duties=True)["pass"])
        before = ac.count(read(os.path.join(OUTPUTS, "pitch-v0-before.md")), duties=True)
        self.assertFalse(before["pass"])
        self.assertEqual(len(before["duties_lines"]), 1)

    def test_sendable_examples_pass(self):
        for name in ["resume.md", "linkedin-about.md", "post-onsite-48h.md"]:
            self.assertTrue(ac.count(read(os.path.join(OUTPUTS, name)), duties=True)["pass"], name)


class ScorecardDrift(unittest.TestCase):
    """The counts quoted in the worked scorecard must be what the script says today."""

    def blockquotes(self, text):
        blocks, cur = [], []
        for line in text.splitlines():
            if line.startswith(">"):
                cur.append(line.lstrip("> ").replace("-> ", ""))
            elif cur:
                blocks.append(" ".join(cur))
                cur = []
        if cur:
            blocks.append(" ".join(cur))
        return blocks

    def test_quoted_counts_match(self):
        card = read(os.path.join(OUTPUTS, "interview-scorecard.md"))
        before, after = self.blockquotes(card)[:2]
        b, a = ac.count(before), ac.count(after)
        self.assertIn("L %d / F %d / N %d, F share %d%%" % (b["L"], b["F"], b["N"], round(b["F_share"] * 100)), card)
        self.assertIn("After: L %d / F %d / N %d" % (a["L"], a["F"], a["N"]), card)
        self.assertFalse(b["pass"])
        self.assertTrue(a["pass"])


class CommandLine(unittest.TestCase):
    def run_cli(self, *args):
        return subprocess.run([sys.executable, os.path.join(ROOT, "scripts", "altitude_count.py")] + list(args),
                              capture_output=True, text=True)

    def test_gate_exit_codes(self):
        self.assertEqual(self.run_cli(os.path.join(OUTPUTS, "pitch.md"), "--gate").returncode, 0)
        self.assertEqual(self.run_cli(os.path.join(OUTPUTS, "pitch-v0-before.md"), "--gate").returncode, 1)

    def test_json_output(self):
        r = self.run_cli(os.path.join(OUTPUTS, "pitch.md"), "--json", "--duties")
        data = json.loads(r.stdout)
        self.assertEqual(data["duties_lines"], [])
        self.assertGreaterEqual(data["L"], 2 * data["F"])

    def test_calibrate_flag(self):
        r = self.run_cli("--calibrate", CALIBRATION)
        self.assertEqual(r.returncode, 0)
        self.assertIn("agreement", r.stdout)

    def test_min_ratio_flag_and_in_process_main(self):
        buf = io.StringIO()
        with redirect_stdout(buf):
            code = ac.main([os.path.join(OUTPUTS, "pitch.md"), "--min-ratio", "10", "--gate"])
        self.assertEqual(code, 1)
        self.assertIn("need 10.0", buf.getvalue())


if __name__ == "__main__":
    unittest.main()
