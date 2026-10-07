import copy
import unittest

from research.wp4_corporate_action_factor_evidence import (
    REQUIRED_FORMULA_EVIDENCE,
    SUPPORTED_EVENT_TYPES,
    assess_c06_evidence,
)


def framework():
    return {
        "adjustment_direction": "BACKWARD",
        "event_day_adjusted_equals_raw": True,
        "event_day_after_close_inclusion": True,
        "holiday_shift_to_actual_trading_date": True,
        "event_types": list(SUPPORTED_EVENT_TYPES),
    }


def formula(state="PENDING"):
    return {
        name: {
            "state": state,
            "references": ["PINNED_SOURCE_LOCATOR"],
        }
        for name in REQUIRED_FORMULA_EVIDENCE
    }


def packet():
    return {
        "synthetic_only": True,
        "framework": framework(),
        "formula_evidence": formula(),
        "formula_authentication_complete": False,
    }


class C06EvidenceGapContractTests(unittest.TestCase):

    def test_current_known_framework_is_supported_but_formula_remains_unverified(self):
        result = assess_c06_evidence(packet())
        self.assertTrue(result["framework_supported"])
        self.assertFalse(result["formula_verified"])
        self.assertFalse(result["source_verified"])
        self.assertFalse(result["production_eligible"])
        self.assertEqual(result["execution_readiness"], "BLOCKED")

    def test_missing_packet_fails_closed(self):
        result = assess_c06_evidence(None)
        self.assertIn("PACKET_INVALID", result["issues"])
        self.assertFalse(result["formula_verified"])

    def test_real_input_cannot_be_promoted(self):
        candidate = packet()
        candidate["synthetic_only"] = False
        result = assess_c06_evidence(candidate)
        self.assertIn("RESEARCH_DECLARATION_REQUIRED", result["issues"])
        self.assertFalse(result["source_verified"])
        self.assertFalse(result["production_eligible"])

    def test_wrong_adjustment_direction_rejected(self):
        candidate = packet()
        candidate["framework"]["adjustment_direction"] = "FORWARD"
        result = assess_c06_evidence(candidate)
        self.assertFalse(result["framework_supported"])
        self.assertIn(
            "BACKWARD_ADJUSTMENT_EVIDENCE_REQUIRED",
            result["issues"],
        )

    def test_event_day_identity_required(self):
        candidate = packet()
        candidate["framework"]["event_day_adjusted_equals_raw"] = False
        result = assess_c06_evidence(candidate)
        self.assertFalse(result["framework_supported"])

    def test_after_close_timing_required(self):
        candidate = packet()
        candidate["framework"]["event_day_after_close_inclusion"] = False
        result = assess_c06_evidence(candidate)
        self.assertFalse(result["framework_supported"])

    def test_holiday_shift_rule_required(self):
        candidate = packet()
        candidate["framework"]["holiday_shift_to_actual_trading_date"] = False
        result = assess_c06_evidence(candidate)
        self.assertFalse(result["framework_supported"])

    def test_exact_event_taxonomy_required(self):
        candidate = packet()
        candidate["framework"]["event_types"].remove("PAR_VALUE_CHANGE")
        result = assess_c06_evidence(candidate)
        self.assertFalse(result["framework_supported"])
        self.assertIn(
            "EVENT_TAXONOMY_EVIDENCE_REQUIRED",
            result["issues"],
        )

    def test_duplicate_event_taxonomy_rejected(self):
        candidate = packet()
        candidate["framework"]["event_types"].append("STOCK_SPLIT")
        result = assess_c06_evidence(candidate)
        self.assertFalse(result["framework_supported"])

    def test_each_formula_evidence_item_is_required(self):
        for name in REQUIRED_FORMULA_EVIDENCE:
            candidate = packet()
            del candidate["formula_evidence"][name]
            result = assess_c06_evidence(candidate)
            self.assertIn(
                "FORMULA_EVIDENCE_MISSING:" + name,
                result["issues"],
            )
            self.assertFalse(result["formula_verified"])

    def test_pending_formula_claims_never_verify_formula(self):
        result = assess_c06_evidence(packet())
        for name in REQUIRED_FORMULA_EVIDENCE:
            self.assertIn(
                "FORMULA_EVIDENCE_NOT_SUPPORTED:" + name,
                result["issues"],
            )
        self.assertFalse(result["formula_verified"])

    def test_supported_without_reference_is_rejected(self):
        candidate = packet()
        candidate["formula_evidence"] = formula("SUPPORTED")
        candidate["formula_evidence"]["precision"]["references"] = []
        candidate["formula_authentication_complete"] = True

        result = assess_c06_evidence(candidate)

        self.assertIn(
            "FORMULA_REFERENCE_REQUIRED:precision",
            result["issues"],
        )
        self.assertFalse(result["formula_verified"])

    def test_supported_declarations_still_do_not_authorize_production(self):
        candidate = packet()
        candidate["formula_evidence"] = formula("SUPPORTED")
        candidate["formula_authentication_complete"] = True

        result = assess_c06_evidence(candidate)

        self.assertTrue(result["formula_verified"])
        self.assertFalse(result["source_verified"])
        self.assertFalse(result["production_eligible"])
        self.assertEqual(result["execution_readiness"], "BLOCKED")

    def test_input_not_mutated(self):
        candidate = packet()
        original = copy.deepcopy(candidate)

        assess_c06_evidence(candidate)

        self.assertEqual(candidate, original)


if __name__ == "__main__":
    unittest.main()
