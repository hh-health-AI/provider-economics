import contextlib
import io
import json
import sys
import unittest
from pathlib import Path
from unittest.mock import patch

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "scripts"))
import ma_enrollment as ma


class EnrollmentTests(unittest.TestCase):
    def run_summary(self, plans, enrol, extra=()):
        buf = io.StringIO()
        with patch.object(ma, "load", side_effect=lambda p: plans if p == "plans" else enrol), \
             patch.object(sys, "argv", ["ma", "--contract-csv", "plans", "--enrollment-csv", "enrol", "--summarise", *extra]), \
             contextlib.redirect_stdout(buf):
            ma.main()
        return json.loads(buf.getvalue())

    def test_mixed_plans_do_not_overwrite(self):
        plans = [{"Contract ID": "H1", "Plan ID": "001", "Special Needs Plan": "No"},
                 {"Contract ID": "H1", "Plan ID": "002", "Special Needs Plan": "Yes"}]
        enrol = [{"Contract ID": "H1", "Plan ID": "1", "Enrollment": "100"},
                 {"Contract ID": "H1", "Plan ID": "2", "Enrollment": "20"}]
        result = self.run_summary(plans, enrol)
        self.assertEqual(result["snp_enrollment"], 20)
        self.assertEqual(result["snp_share"], 0.1667)

    def test_conflicting_duplicate_metadata_rejected(self):
        plans = [{"Contract ID": "H1", "Plan ID": "1", "Special Needs Plan": value}
                 for value in ("Yes", "No")]
        with self.assertRaises(SystemExit):
            self.run_summary(plans, [])

    def test_unknown_snp_is_not_non_snp(self):
        result = self.run_summary([], [{"Contract ID": "H1", "Plan ID": "1", "Enrollment": "100"}])
        self.assertIsNone(result["snp_share"])
        self.assertEqual(result["unknown_snp_enrollment"], 100)

    def test_unmatched_org_filter_fails(self):
        with self.assertRaises(SystemExit):
            self.run_summary([], [{"Contract ID": "H1", "Plan ID": "1", "Enrollment": "100"}], ["--org", "Example"])

    def test_segment_keys_are_distinct(self):
        self.assertNotEqual(ma.plan_key({"Contract ID": "H1", "Plan ID": "1", "Segment ID": "1"}),
                            ma.plan_key({"Contract ID": "H1", "Plan ID": "1", "Segment ID": "2"}))


if __name__ == "__main__":
    unittest.main()
