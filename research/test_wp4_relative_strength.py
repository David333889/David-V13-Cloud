"""Offline checks of candidate semantics and rejection behavior."""
import copy
import math
import unittest

from research.wp4_relative_strength import compare_candidate_metrics


def series(start, finish):
    return {
        "synthetic_only": True,
        "adjustment_type": "SYNTHETIC_MATCHED_PRICE_BASIS",
        "records": [
            {"trading_date": "2026-09-01", "close": start},
            {"trading_date": "2026-09-02", "close": finish},
        ],
    }


class CandidateMetricsTests(unittest.TestCase):
    def test_equal_performance_at_different_price_scales(self):
        result = compare_candidate_metrics(series(10, 11), series(100, 110), 1)
        self.assertTrue(result["allowed"])
        self.assertAlmostEqual(result["return_difference"], 0)
        self.assertAlmostEqual(result["gross_relative_return"], 0)

    def test_formula_candidates_have_different_magnitudes(self):
        result = compare_candidate_metrics(series(100, 110), series(100, 105), 1)
        self.assertAlmostEqual(result["return_difference"], .05)
        self.assertAlmostEqual(result["gross_relative_return"], 1.1 / 1.05 - 1)
        self.assertNotAlmostEqual(result["return_difference"], result["gross_relative_return"])
        self.assertFalse(result["signal_emitted"])
        self.assertFalse(result["ranking_emitted"])
        self.assertFalse(result["market_state_emitted"])

    def test_absolute_loss_can_have_positive_relative_performance(self):
        result = compare_candidate_metrics(series(100, 90), series(100, 80), 1)
        self.assertAlmostEqual(result["stock_return"], -.1)
        self.assertAlmostEqual(result["gross_relative_return"], .125)
        self.assertFalse(result["signal_emitted"])

    def test_underperformance_and_flat_benchmark(self):
        result = compare_candidate_metrics(series(100, 95), series(100, 100), 1)
        self.assertAlmostEqual(result["return_difference"], -.05)
        self.assertAlmostEqual(result["gross_relative_return"], -.05)

    def test_scale_invariance(self):
        a = compare_candidate_metrics(series(10, 12), series(50, 55), 1)
        b = compare_candidate_metrics(series(1000, 1200), series(5, 5.5), 1)
        self.assertAlmostEqual(a["gross_relative_return"], b["gross_relative_return"])

    def test_every_observation_date_must_align(self):
        a = series(100, 110)
        b = series(100, 105)
        b["records"][0]["trading_date"] = "2026-08-31"
        self.assertEqual(compare_candidate_metrics(a, b, 1)["reason"], "DATE_GRID_MISMATCH")

    def test_duplicates_and_reverse_dates_rejected(self):
        for bad_date in ("2026-09-01", "2026-08-31"):
            with self.subTest(date=bad_date):
                a = series(100, 110)
                a["records"][1]["trading_date"] = bad_date
                self.assertEqual(compare_candidate_metrics(a, series(100, 105), 1)["reason"],
                                 "DATES_NOT_STRICTLY_INCREASING")

    def test_invalid_date_formats_rejected(self):
        for bad_date in ("20260901", "2026-02-30", None, "115/09/01"):
            with self.subTest(date=bad_date):
                a = series(100, 110)
                a["records"][0]["trading_date"] = bad_date
                self.assertEqual(compare_candidate_metrics(a, series(100, 105), 1)["reason"], "DATE_INVALID")

    def test_invalid_close_values_rejected_in_both_series(self):
        for bad in (True, False, 0, -1, None, "100", math.nan, math.inf, -math.inf, 10 ** 400):
            for target in ("stock", "benchmark"):
                with self.subTest(value=repr(bad), target=target):
                    a, b = series(100, 110), series(100, 105)
                    (a if target == "stock" else b)["records"][1]["close"] = bad
                    self.assertEqual(compare_candidate_metrics(a, b, 1)["reason"], "CLOSE_INVALID")

    def test_missing_window_is_not_padded(self):
        self.assertEqual(compare_candidate_metrics(series(100, 110), series(100, 105), 2)["reason"],
                         "EXACT_WINDOW_REQUIRED")

    def test_explicit_lookback_required(self):
        for bad in (None, True, 0, -1, 1.0, "1"):
            with self.subTest(value=bad):
                self.assertEqual(compare_candidate_metrics(series(100, 110), series(100, 105), bad)["reason"],
                                 "LOOKBACK_INVALID")

    def test_real_input_and_adjustment_mismatch_rejected(self):
        a, b = series(100, 110), series(100, 105)
        a["synthetic_only"] = False
        self.assertEqual(compare_candidate_metrics(a, b, 1)["reason"], "SYNTHETIC_RESEARCH_ONLY")
        a["synthetic_only"] = True
        a["adjustment_type"] = "UNMATCHED"
        self.assertEqual(compare_candidate_metrics(a, b, 1)["reason"], "ADJUSTMENT_MISMATCH")

    def test_derived_overflow_is_not_a_valid_metric(self):
        self.assertEqual(compare_candidate_metrics(series(1e-308, 1e308), series(100, 105), 1)["reason"],
                         "METRIC_NOT_FINITE")

    def test_input_not_mutated(self):
        a, b = series(100, 110), series(100, 105)
        snapshot = copy.deepcopy((a, b))
        compare_candidate_metrics(a, b, 1)
        self.assertEqual((a, b), snapshot)

    def test_underflow_does_not_manufacture_complete_loss(self):
        extreme = series(1e308, 1e-308)
        normal = series(100, 105)
        for a, b in ((extreme, normal), (normal, extreme)):
            self.assertEqual(compare_candidate_metrics(a, b, 1)["reason"], "METRIC_NOT_FINITE")

    def test_middle_observation_is_validated_even_when_endpoints_match(self):
        a, b = series(100, 110), series(100, 105)
        a["records"].insert(1, {"trading_date": "2026-09-01", "close": 101})
        b["records"].insert(1, {"trading_date": "2026-09-01", "close": 102})
        self.assertEqual(compare_candidate_metrics(a, b, 2)["reason"], "DATES_NOT_STRICTLY_INCREASING")


if __name__ == "__main__":
    unittest.main()
