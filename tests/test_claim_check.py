"""Tests for scripts/claim_check.py. Run from the repo root:

    python3 -m unittest discover -s tests -v
"""
import copy
import io
import json
import os
import subprocess
import sys
import tempfile
import unittest
from contextlib import redirect_stdout

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(ROOT, "scripts"))
import claim_check as cc  # noqa: E402

LEDGER_PATH = os.path.join(ROOT, "examples", "claims-ledger.example.json")
LEDGER = cc.load_ledger(LEDGER_PATH)
OUTPUTS = os.path.join(ROOT, "examples", "outputs")


def run(text, ledger=LEDGER, surface="external"):
    findings, checked, matched = cc.check(text, ledger, surface)
    return findings


def fails(text, **kw):
    return {f.rule for f in run(text, **kw) if f.severity == "fail"}


def warns(text, **kw):
    return {f.rule for f in run(text, **kw) if f.severity == "warn"}


def with_status(claim_id, status):
    ledger = copy.deepcopy(LEDGER)
    for c in ledger["claims"]:
        if c["id"] == claim_id:
            c["status"] = status
    return ledger


class Tokens(unittest.TestCase):
    def kinds(self, text):
        return [(t.kind, t.value, t.plus) for t in cc.tokens(text)]

    def test_money_scales_are_equal(self):
        self.assertTrue(cc.same(cc.tokens("$18M")[0], cc.tokens("$18 million")[0]))

    def test_kinds(self):
        got = self.kinds("$63M ARR, 44%, 3.5x, 41,000+ teams, 2.1M builds, in 2021")
        self.assertEqual(got, [("money", 63e6, False), ("pct", 44.0, False), ("mult", 3.5, False),
                               ("count", 41000.0, True), ("count", 2.1e6, False), ("year", 2021.0, False)])

    def test_glued_tokens_are_skipped(self):
        self.assertEqual(cc.tokens("Q3 L7 1st 5G GPT-4 B2B v2 FY2025"), [])

    def test_hyphenated_count_is_kept(self):
        self.assertEqual(self.kinds("a 70-person org"), [("count", 70.0, False)])


class LedgerMembership(unittest.TestCase):
    def test_ledger_numbers_pass(self):
        self.assertEqual(fails("At Quillstone we grew the line from $18M to $63M ARR (3.5x)."), set())

    def test_unknown_number_fails(self):
        self.assertIn("unknown-number", fails("At Quillstone we grew ARR to $70M."))

    def test_scale_words_match(self):
        self.assertEqual(fails("At Quillstone we grew the line from $18 million to $63 million."), set())

    def test_qualifier_mismatch_warns(self):
        self.assertIn("qualifier", warns("At Quillstone the platform served 41,000 teams."))

    def test_non_claim_numbers_are_ignored(self):
        text = "Here is my 90-second pitch for the first 30 days, the top 3 risks and question 2."
        self.assertEqual(fails(text), set())

    def test_years_outside_the_record_warn(self):
        self.assertIn("unknown-year", warns("In 2009 I started my career."))
        self.assertEqual(warns("At Quillstone since 2021."), set())

    def test_spelled_out_numbers_are_not_checked(self):
        # documented limitation: write claims in digits
        self.assertEqual(fails("At Quillstone we tripled the line."), set())


class PrivateFigures(unittest.TestCase):
    def test_plan_target_fails_externally(self):
        self.assertIn("private-figure", fails("At Quillstone we are on track for $90M ARR."))

    def test_internal_surface_allows_it(self):
        self.assertNotIn("private-figure", fails("At Quillstone the plan is $90M ARR.", surface="internal"))


class TenureBinding(unittest.TestCase):
    def test_unbound_growth_fails(self):
        self.assertIn("unbound-growth", fails("I grew the platform line from $18M to $63M ARR."))

    def test_growth_bound_in_sentence(self):
        self.assertEqual(fails("At Quillstone I grew the platform line from $18M to $63M ARR."), set())

    def test_growth_bound_by_paragraph(self):
        text = "I run the developer platform at Quillstone Cloud. We grew it from $18M to $63M ARR."
        self.assertEqual(fails(text), set())

    def test_growth_bound_by_section_header(self):
        text = "QUILLSTONE CLOUD    2021-Present\n- Platform line: grew ARR from $18M to $63M (3.5x)"
        self.assertEqual(fails(text), set())

    def test_misattributed_number(self):
        self.assertIn("misattributed", fails("At Tidewell I grew the platform line from $18M to $63M ARR."))

    def test_header_scope_ends_at_next_header(self):
        text = ("QUILLSTONE CLOUD    2021-Present\n- Grew ARR from $18M to $63M\n\n"
                "TIDEWELL SOFTWARE    2017-2021\n- Grew ARR from $18M to $63M")
        got = run(text)
        self.assertEqual([f.rule for f in got if f.severity == "fail"], ["misattributed", "misattributed"])
        self.assertTrue(all(f.line == 5 for f in got))

    def test_beyond_tenure(self):
        text = "TIDEWELL SOFTWARE    2017-2021\n- Raised trial-to-paid conversion from 22% to 41% over 6 years"
        self.assertIn("beyond-tenure", fails(text))

    def test_within_tenure(self):
        text = "TIDEWELL SOFTWARE    2017-2021\n- Raised trial-to-paid conversion from 22% to 41% over 3 years"
        self.assertNotIn("beyond-tenure", fails(text))

    def test_a_bullet_does_not_become_a_header(self):
        text = "- Raised Tidewell conversion from 22% to 41%\n- Platform used by 41,000+ teams"
        self.assertNotIn("misattributed", fails(text))


class RoleDates(unittest.TestCase):
    def test_matching_dates_pass(self):
        self.assertEqual(fails("QUILLSTONE CLOUD 2021-Present\nTIDEWELL SOFTWARE 2017-2021"), set())

    def test_wrong_start_fails(self):
        self.assertIn("role-dates", fails("Tidewell Software 2016-2021"))

    def test_en_dash_ranges_are_read(self):
        self.assertIn("role-dates", fails("Tidewell Software 2017\u20132022"))


class Forbidden(unittest.TestCase):
    def test_bookings_stated_as_revenue(self):
        self.assertIn("forbidden", fails("At Quillstone revenue grew to $80M."))
        self.assertIn("forbidden", fails("At Quillstone we reached $80M ARR."))

    def test_bookings_stated_as_bookings(self):
        self.assertEqual(fails("At Quillstone we signed $80M in multi-year contract bookings."), set())

    def test_contractors_counted_as_employees(self):
        self.assertIn("forbidden", fails("At Quillstone I managed 70 engineers."))
        self.assertNotIn("forbidden", fails("At Quillstone I led a 70-person org."))

    def test_pilot_counted_as_launch(self):
        self.assertIn("forbidden", fails("At Quillstone we launched hosted build runners."))
        self.assertEqual(fails("At Quillstone we ran a 6-week pilot of hosted build runners with 12 design partners."),
                         set())

    def test_status_condition_switches_rules(self):
        ga = with_status("runners", "ga")
        self.assertNotIn("forbidden", fails("At Quillstone we launched hosted build runners.", ledger=ga))
        self.assertIn("forbidden", fails("At Quillstone we ran a pilot of hosted build runners.", ledger=ga))

    def test_stale_title(self):
        self.assertIn("forbidden", fails("VP of Product at Quillstone Cloud."))

    def test_unless_proof_lifts_a_rule(self):
        ledger = copy.deepcopy(LEDGER)
        ledger["claims"].append({"id": "award", "role": "quillstone", "kind": "award", "text": "Industry award",
                                 "proof": {"link": None}})
        ledger["forbidden"].append({"id": "award-name", "pattern": "Golden Build Award", "unless_proof": "award",
                                    "severity": "fail", "reason": "no source for the award yet"})
        self.assertIn("forbidden", fails("Won the Golden Build Award.", ledger=ledger))
        ledger["claims"][-1]["proof"]["link"] = "https://example.com/award"
        self.assertNotIn("forbidden", fails("Won the Golden Build Award.", ledger=ledger))


class Anachronism(unittest.TestCase):
    def test_term_after_role_ended_fails(self):
        self.assertIn("anachronism", fails("At Tidewell we built an MCP server for the CI product."))

    def test_term_in_a_current_role_passes(self):
        self.assertNotIn("anachronism", fails("At Quillstone we built an MCP server."))

    def test_term_under_a_header(self):
        self.assertIn("anachronism", fails("TIDEWELL SOFTWARE    2017-2021\n- Shipped a GPT-4 assistant for build logs"))


class Examples(unittest.TestCase):
    def test_sendable_examples_pass(self):
        for name in ["pitch.md", "resume.md", "linkedin-about.md", "post-onsite-48h.md"]:
            with open(os.path.join(OUTPUTS, name), encoding="utf-8") as fh:
                self.assertEqual(fails(fh.read()), set(), name)

    def test_first_draft_fails(self):
        with open(os.path.join(OUTPUTS, "pitch-v0-before.md"), encoding="utf-8") as fh:
            got = run(fh.read())
        rules = {f.rule for f in got if f.severity == "fail"}
        self.assertTrue({"unknown-number", "forbidden"} <= rules)
        reasons = " ".join(f.reason for f in got)
        self.assertIn("bookings", reasons)
        self.assertIn("pilot", reasons)


class LedgerLoading(unittest.TestCase):
    def test_claim_with_unknown_role_is_rejected(self):
        bad = {"roles": [], "claims": [{"id": "x", "role": "nowhere", "text": "$1M"}]}
        with tempfile.NamedTemporaryFile("w", suffix=".json", delete=False, encoding="utf-8") as fh:
            json.dump(bad, fh)
            path = fh.name
        try:
            with self.assertRaises(ValueError):
                cc.load_ledger(path)
        finally:
            os.unlink(path)


class CommandLine(unittest.TestCase):
    def run_cli(self, *args, stdin=None):
        return subprocess.run([sys.executable, os.path.join(ROOT, "scripts", "claim_check.py")] + list(args),
                              input=stdin, capture_output=True, text=True)

    def test_exit_codes(self):
        self.assertEqual(self.run_cli(os.path.join(OUTPUTS, "pitch.md"), LEDGER_PATH).returncode, 0)
        self.assertEqual(self.run_cli(os.path.join(OUTPUTS, "pitch-v0-before.md"), LEDGER_PATH).returncode, 1)
        self.assertEqual(self.run_cli("missing.md", LEDGER_PATH).returncode, 2)

    def test_stdin_and_json(self):
        r = self.run_cli("-", LEDGER_PATH, "--json", stdin="I grew ARR from $18M to $63M.")
        data = json.loads(r.stdout)
        self.assertEqual(data["numbers_checked"], 2)
        self.assertEqual({f["rule"] for f in data["findings"]}, {"unbound-growth"})

    def test_surface_flag_in_process(self):
        buf = io.StringIO()
        draft = os.path.join(tempfile.gettempdir(), "claim-check-surface-test.md")
        with open(draft, "w", encoding="utf-8") as fh:
            fh.write("At Quillstone the plan is $90M ARR.")
        try:
            with redirect_stdout(buf):
                self.assertEqual(cc.main([draft, LEDGER_PATH]), 1)
                self.assertEqual(cc.main([draft, LEDGER_PATH, "--surface", "internal"]), 0)
        finally:
            os.unlink(draft)


if __name__ == "__main__":
    unittest.main()
