"""Business-risk checks for the synthetic observation-quality experiment."""
import copy
import math
import unittest
from research.wp4_observation_quality import compare_quality_checked_candidates
from research.test_wp4_relative_strength import series


def observed(start=100, finish=110):
    data = series(start, finish)
    data["raw_records"] = copy.deepcopy(data["records"])
    for row in data["records"]:
        row["observation_status"] = "OBSERVED"
    return data


class ObservationQualityTests(unittest.TestCase):
    def test_valid_comparison_is_still_not_source_verified_or_signal(self):
        result = compare_quality_checked_candidates(observed(), observed(100, 105), 1)
        self.assertTrue(result["allowed"])
        self.assertAlmostEqual(result["gross_relative_return"], 1.1 / 1.05 - 1)
        for key in ("source_verified", "signal_emitted", "ranking_emitted", "market_state_emitted"):
            self.assertFalse(result[key])

    def test_positive_adjusted_price_cannot_mask_zero_raw_price(self):
        for side in (0, 1):
            inputs = [observed(), observed()]
            inputs[side]["raw_records"][1]["close"] = 0
            result = compare_quality_checked_candidates(*inputs, 1)
            self.assertEqual(result["reason"], "NO_ANNOUNCED_PRICE")

    def test_carried_missing_unknown_or_absent_status_rejected(self):
        for status, reason in (("CARRIED", "CARRIED_PRICE_REJECTED"),
                               ("MISSING", "MISSING_PRICE_REJECTED"),
                               ("UNKNOWN", "OBSERVATION_STATUS_REQUIRED"),
                               (None, "OBSERVATION_STATUS_REQUIRED")):
            for side in (0, 1):
                with self.subTest(status=status, side=side):
                    inputs = [observed(), observed()]
                    inputs[side]["records"][0]["observation_status"] = status
                    self.assertEqual(compare_quality_checked_candidates(*inputs, 1)["reason"], reason)

    def test_unchanged_observed_price_is_not_inferred_to_be_carried(self):
        self.assertTrue(compare_quality_checked_candidates(observed(100, 100), observed(), 1)["allowed"])

    def test_raw_date_mismatch_cannot_be_silently_rejoined(self):
        a = observed()
        a["raw_records"][1]["trading_date"] = "2026-09-03"
        self.assertEqual(compare_quality_checked_candidates(a, observed(), 1)["reason"], "RAW_DATE_MISMATCH")

    def test_missing_extra_or_reordered_raw_rows_rejected(self):
        for raw in (None, [], observed()["raw_records"] + [{}],
                    list(reversed(observed()["raw_records"]))):
            a = observed()
            a["raw_records"] = raw
            self.assertFalse(compare_quality_checked_candidates(a, observed(), 1)["allowed"])

    def test_malformed_raw_row_rejected_without_exception(self):
        a = observed()
        a["raw_records"][1] = None
        self.assertEqual(compare_quality_checked_candidates(a, observed(), 1)["reason"], "RAW_RECORD_INVALID")

    def test_non_numeric_non_finite_and_negative_raw_close_rejected(self):
        for value in (True, False, None, "100", math.nan, math.inf, -math.inf, -1, 10 ** 400):
            a = observed()
            a["raw_records"][0]["close"] = value
            self.assertEqual(compare_quality_checked_candidates(a, observed(), 1)["reason"], "RAW_CLOSE_INVALID")

    def test_middle_observation_must_pass_quality_check(self):
        a, b = observed(), observed()
        for data in (a, b):
            data["records"].insert(1, {"trading_date": "2026-09-01", "close": 100,
                                       "observation_status": "OBSERVED"})
            data["records"][0]["trading_date"] = "2026-08-31"
            data["raw_records"] = copy.deepcopy(data["records"])
        a["raw_records"][1]["close"] = 0
        self.assertEqual(compare_quality_checked_candidates(a, b, 2)["reason"], "NO_ANNOUNCED_PRICE")

    def test_input_is_not_mutated_on_success_or_rejection(self):
        for raw_close in (100, 0):
            a, b = observed(), observed()
            a["raw_records"][0]["close"] = raw_close
            before = copy.deepcopy((a, b))
            compare_quality_checked_candidates(a, b, 1)
            self.assertEqual((a, b), before)

    def test_real_input_and_mixed_basis_still_rejected(self):
        a = observed()
        a["synthetic_only"] = False
        self.assertEqual(compare_quality_checked_candidates(a, observed(), 1)["reason"], "SYNTHETIC_RESEARCH_ONLY")
        a = observed()
        a["adjustment_type"] = "OTHER"
        self.assertEqual(compare_quality_checked_candidates(a, observed(), 1)["reason"], "ADJUSTMENT_MISMATCH")


if __name__ == "__main__":
    unittest.main()
