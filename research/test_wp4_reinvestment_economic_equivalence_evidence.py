import copy
import unittest

from research.wp4_reinvestment_economic_equivalence_evidence import (
    BENCHMARK_DATASET,
    REQUIRED_EQUIVALENCE_EVIDENCE,
    REQUIRED_REINVESTMENT_EVIDENCE,
    STOCK_DATASET,
    assess_c07_c12_evidence,
)


def supported_claim():
    return {
        "state": "SUPPORTED",
        "references": ["PINNED_SOURCE_LOCATOR"],
    }


def pending_claim():
    return {
        "state": "PENDING",
        "references": ["REVIEWED_SCOPE_LOCATOR"],
    }


def packet():
    return {
        "synthetic_only": True,
        "dataset_identity": {
            "stock_dataset": STOCK_DATASET,
            "benchmark_dataset": BENCHMARK_DATASET,
            "benchmark_id": "TAIEX",
        },
        "reinvestment_evidence": {
            name: pending_claim()
            for name in REQUIRED_REINVESTMENT_EVIDENCE
        },
        "equivalence_evidence": {
            name: pending_claim()
            for name in REQUIRED_EQUIVALENCE_EVIDENCE
        },
        "reinvestment_authentication_complete": False,
        "equivalence_authentication_complete": False,
    }


class ReinvestmentEconomicEquivalenceEvidenceTests(unittest.TestCase):

    def test_current_dataset_identity_supported_but_economic_claims_blocked(self):
        result = assess_c07_c12_evidence(packet())

        self.assertTrue(result["dataset_identity_supported"])
        self.assertFalse(result["reinvestment_verified"])
        self.assertFalse(result["economic_equivalence_verified"])
        self.assertFalse(result["source_verified"])
        self.assertFalse(result["production_eligible"])
        self.assertEqual(result["execution_readiness"], "BLOCKED")

    def test_missing_packet_fails_closed(self):
        result = assess_c07_c12_evidence(None)

        self.assertIn("PACKET_INVALID", result["issues"])
        self.assertFalse(result["reinvestment_verified"])
        self.assertFalse(result["economic_equivalence_verified"])

    def test_real_input_cannot_promote_research_contract(self):
        candidate = packet()
        candidate["synthetic_only"] = False

        result = assess_c07_c12_evidence(candidate)

        self.assertIn("RESEARCH_DECLARATION_REQUIRED", result["issues"])
        self.assertFalse(result["source_verified"])
        self.assertFalse(result["production_eligible"])

    def test_stock_dataset_identity_must_match(self):
        candidate = packet()
        candidate["dataset_identity"]["stock_dataset"] = "TaiwanStockPrice"

        result = assess_c07_c12_evidence(candidate)

        self.assertFalse(result["dataset_identity_supported"])
        self.assertIn(
            "STOCK_DATASET_IDENTITY_MISMATCH",
            result["issues"],
        )

    def test_benchmark_dataset_identity_must_match(self):
        candidate = packet()
        candidate["dataset_identity"]["benchmark_dataset"] = "UNKNOWN"

        result = assess_c07_c12_evidence(candidate)

        self.assertFalse(result["dataset_identity_supported"])
        self.assertIn(
            "BENCHMARK_DATASET_IDENTITY_MISMATCH",
            result["issues"],
        )

    def test_taiex_identity_must_be_explicit(self):
        candidate = packet()
        candidate["dataset_identity"]["benchmark_id"] = "TPEx"

        result = assess_c07_c12_evidence(candidate)

        self.assertFalse(result["dataset_identity_supported"])
        self.assertIn(
            "BENCHMARK_IDENTITY_MISMATCH",
            result["issues"],
        )

    def test_every_reinvestment_item_is_required(self):
        for name in REQUIRED_REINVESTMENT_EVIDENCE:
            candidate = packet()
            del candidate["reinvestment_evidence"][name]

            result = assess_c07_c12_evidence(candidate)

            self.assertIn(
                "REINVESTMENT_EVIDENCE_MISSING:" + name,
                result["issues"],
            )
            self.assertFalse(result["reinvestment_verified"])

    def test_pending_reinvestment_claims_do_not_verify(self):
        result = assess_c07_c12_evidence(packet())

        for name in REQUIRED_REINVESTMENT_EVIDENCE:
            self.assertIn(
                "REINVESTMENT_EVIDENCE_NOT_SUPPORTED:" + name,
                result["issues"],
            )

        self.assertFalse(result["reinvestment_verified"])

    def test_reinvestment_reference_is_required(self):
        candidate = packet()

        candidate["reinvestment_evidence"] = {
            name: supported_claim()
            for name in REQUIRED_REINVESTMENT_EVIDENCE
        }

        candidate["reinvestment_evidence"]["reinvestment_price"][
            "references"
        ] = []

        candidate["reinvestment_authentication_complete"] = True

        result = assess_c07_c12_evidence(candidate)

        self.assertIn(
            "REINVESTMENT_EVIDENCE_REFERENCE_REQUIRED:reinvestment_price",
            result["issues"],
        )
        self.assertFalse(result["reinvestment_verified"])

    def test_complete_reinvestment_declarations_can_verify_reinvestment_only(self):
        candidate = packet()

        candidate["reinvestment_evidence"] = {
            name: supported_claim()
            for name in REQUIRED_REINVESTMENT_EVIDENCE
        }

        candidate["reinvestment_authentication_complete"] = True

        result = assess_c07_c12_evidence(candidate)

        self.assertTrue(result["reinvestment_verified"])
        self.assertFalse(result["economic_equivalence_verified"])
        self.assertFalse(result["production_eligible"])

    def test_every_equivalence_item_is_required(self):
        for name in REQUIRED_EQUIVALENCE_EVIDENCE:
            candidate = packet()

            candidate["reinvestment_evidence"] = {
                item: supported_claim()
                for item in REQUIRED_REINVESTMENT_EVIDENCE
            }
            candidate["reinvestment_authentication_complete"] = True

            del candidate["equivalence_evidence"][name]

            result = assess_c07_c12_evidence(candidate)

            self.assertIn(
                "EQUIVALENCE_EVIDENCE_MISSING:" + name,
                result["issues"],
            )
            self.assertFalse(result["economic_equivalence_verified"])

    def test_pending_equivalence_claims_never_verify_equivalence(self):
        candidate = packet()

        candidate["reinvestment_evidence"] = {
            name: supported_claim()
            for name in REQUIRED_REINVESTMENT_EVIDENCE
        }
        candidate["reinvestment_authentication_complete"] = True

        result = assess_c07_c12_evidence(candidate)

        self.assertTrue(result["reinvestment_verified"])
        self.assertFalse(result["economic_equivalence_verified"])

    def test_equivalence_reference_is_required(self):
        candidate = packet()

        candidate["reinvestment_evidence"] = {
            name: supported_claim()
            for name in REQUIRED_REINVESTMENT_EVIDENCE
        }
        candidate["equivalence_evidence"] = {
            name: supported_claim()
            for name in REQUIRED_EQUIVALENCE_EVIDENCE
        }

        candidate["equivalence_evidence"]["tax_fee_alignment"][
            "references"
        ] = []

        candidate["reinvestment_authentication_complete"] = True
        candidate["equivalence_authentication_complete"] = True

        result = assess_c07_c12_evidence(candidate)

        self.assertIn(
            "EQUIVALENCE_EVIDENCE_REFERENCE_REQUIRED:tax_fee_alignment",
            result["issues"],
        )
        self.assertFalse(result["economic_equivalence_verified"])

    def test_equivalence_requires_reinvestment_verification_first(self):
        candidate = packet()

        candidate["equivalence_evidence"] = {
            name: supported_claim()
            for name in REQUIRED_EQUIVALENCE_EVIDENCE
        }
        candidate["equivalence_authentication_complete"] = True

        result = assess_c07_c12_evidence(candidate)

        self.assertFalse(result["reinvestment_verified"])
        self.assertFalse(result["economic_equivalence_verified"])

    def test_priceadj_name_does_not_imply_total_return_equivalence(self):
        candidate = packet()

        self.assertEqual(
            candidate["dataset_identity"]["stock_dataset"],
            "TaiwanStockPriceAdj",
        )

        result = assess_c07_c12_evidence(candidate)

        self.assertFalse(result["economic_equivalence_verified"])

    def test_all_supported_declarations_still_do_not_authorize_production(self):
        candidate = packet()

        candidate["reinvestment_evidence"] = {
            name: supported_claim()
            for name in REQUIRED_REINVESTMENT_EVIDENCE
        }

        candidate["equivalence_evidence"] = {
            name: supported_claim()
            for name in REQUIRED_EQUIVALENCE_EVIDENCE
        }

        candidate["reinvestment_authentication_complete"] = True
        candidate["equivalence_authentication_complete"] = True

        result = assess_c07_c12_evidence(candidate)

        self.assertTrue(result["reinvestment_verified"])
        self.assertTrue(result["economic_equivalence_verified"])
        self.assertFalse(result["source_verified"])
        self.assertFalse(result["production_eligible"])
        self.assertEqual(result["execution_readiness"], "BLOCKED")

    def test_input_not_mutated(self):
        candidate = packet()
        original = copy.deepcopy(candidate)

        assess_c07_c12_evidence(candidate)

        self.assertEqual(candidate, original)


if __name__ == "__main__":
    unittest.main()
