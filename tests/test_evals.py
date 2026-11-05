"""The eval suite's own checks. Run from the repo root:

    python3 -m unittest discover -s tests -v
"""
import io
import json
import os
import re
import sys
import unittest
from contextlib import redirect_stdout

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(ROOT, "evals"))
import run_evals  # noqa: E402


class Suite(unittest.TestCase):
    def setUp(self):
        self.suite = run_evals.load_suite()

    def test_every_grader_separates_its_fixtures(self):
        buf = io.StringIO()
        bad = run_evals.self_test(self.suite, out=buf)
        self.assertEqual(bad, 0, buf.getvalue())

    def test_ids_are_unique_and_assertions_are_binary(self):
        ids = [e["id"] for e in self.suite["evals"]]
        self.assertEqual(len(ids), len(set(ids)))
        for ev in self.suite["evals"]:
            self.assertTrue(ev["assertions"], ev["name"])
            for a in ev["assertions"]:
                self.assertIn(a["judge"], ("script", "model", "docx"), a["name"])

    def test_script_assertions_have_a_grader(self):
        for ev in self.suite["evals"]:
            if any(a["judge"] == "script" for a in ev["assertions"]):
                self.assertIn("grader", ev, ev["name"])
                self.assertIn(ev["grader"]["name"], run_evals.GRADERS)
                for kind in ("pass", "fail"):
                    self.assertTrue(os.path.exists(os.path.join(ROOT, ev["fixtures"][kind])), ev["fixtures"][kind])

    def test_suite_uses_only_the_invented_candidate(self):
        text = json.dumps(self.suite)
        with open(os.path.join(ROOT, "examples", "claims-ledger.example.json"), encoding="utf-8") as fh:
            ledger = json.load(fh)
        employers = {r["employer"].split()[0] for r in ledger["roles"]}
        named = set(re.findall(r"\b(Quillstone|Tidewell|Corvane|Veridane)\b", text))
        self.assertTrue(named, "evals should use the invented candidate")
        self.assertTrue({"Quillstone", "Tidewell"} <= named | employers)

    def test_grade_mode(self):
        buf = io.StringIO()
        with redirect_stdout(buf):
            ok = run_evals.main(["--grade", "24", os.path.join(ROOT, "evals", "fixtures", "24-duties.pass.md")])
            bad = run_evals.main(["--grade", "24", os.path.join(ROOT, "evals", "fixtures", "24-duties.fail.md")])
            none = run_evals.main(["--grade", "1", os.path.join(ROOT, "evals", "fixtures", "24-duties.pass.md")])
        self.assertEqual((ok, bad, none), (0, 1, 2))


if __name__ == "__main__":
    unittest.main()
