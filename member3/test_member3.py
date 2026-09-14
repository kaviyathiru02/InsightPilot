"""
Member 3 - Validation Engine Tests
"""

import json
import os
import unittest

from validation_engine import ValidationEngine


class TestValidationEngine(unittest.TestCase):

    def setUp(self):
        self.engine = ValidationEngine()

    def test_inventory_shortage_validation(self):
        result = self.engine.validate(
            candidate_cause="Inventory shortage",
            supporting_evidence=3,
            sample_size=20000,
            data_quality="GOOD",
        )

        self.assertEqual(
            result["candidate_cause"],
            "Inventory shortage"
        )

        self.assertIn(
            "evidence_reliability_score",
            result
        )

        self.assertIn(
            "validation_status",
            result
        )

        self.assertIn(
            result["validation_status"],
            ["VALIDATED", "REJECTED", "UNCERTAIN"]
        )

    def test_validation_contains_all_evidence_checks(self):
        result = self.engine.validate(
            candidate_cause="Inventory shortage",
            supporting_evidence=3,
            sample_size=20000,
            data_quality="GOOD",
        )

        self.assertTrue(result["alternative_causes"])
        self.assertTrue(result["devils_advocate_challenges"])
        self.assertTrue(result["counterfactual_analysis"])
        self.assertTrue(result["potential_confounders"])
        self.assertTrue(result["contradictory_evidence"])
        self.assertTrue(result["missing_evidence"])

    def test_member3_output_exists(self):
        output_file = "data/member3_output.json"

        self.assertTrue(
            os.path.exists(output_file),
            "Member 3 output file does not exist."
        )

        with open(output_file, "r", encoding="utf-8") as file:
            data = json.load(file)

        self.assertIn(
            "validated_root_causes",
            data
        )

        self.assertGreater(
            len(data["validated_root_causes"]),
            0
        )


if __name__ == "__main__":
    unittest.main()