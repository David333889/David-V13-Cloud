"""Check evidence gaps, historical cutoff and series-version mixing."""
import copy
import unittest
from research.wp4_evidence_contract import assess_candidate_contract, REQUIREMENTS


def fixture():
    series = {
        "provider": "SYNTHETIC", "dataset": "fixture", "series_id": "TEST",
        "revision_id": "r1", "snapshot_id": "s1", "return_basis": "TOTAL_RETURN",
        "as_of": "2026-09-01T16:00:00+08:00",
        "published_at": "2026-09-01T16:00:00+08:00",
    }
    stock = copy.deepcopy(series)
    stock["raw_adjusted_pair"] = {
        key: stock[key] for key in ("series_id", "revision_id", "snapshot_id")
    }
    return {
        "synthetic_only": True, "contract_version": "WP4_EVIDENCE_CANDIDATE_V1",
        "decision_cutoff": "2026-09-01T17:00:00+08:00",
        "stock": stock, "benchmark": copy.deepcopy(series),
        "evidence": {name: {"state": "SUPPORTED", "references": ["synthetic-fixture-only"]}
                     for name in REQUIREMENTS},
    }


class EvidenceContractTests(unittest.TestCase):
    def test_valid_declarations_never_authorize_live_use(self):
        result = assess_candidate_contract(fixture())
        self.assertTrue(result["metadata_valid"])
        self.assertFalse(result["source_verified"])
        self.assertFalse(result["live_eligible"])
        self.assertEqual(result["execution_readiness"], "BLOCKED")

    def test_all_evidence_categories_required(self):
        for name in REQUIREMENTS:
            data = fixture()
            del data["evidence"][name]
            self.assertIn("EVIDENCE_INCOMPLETE:" + name,
                          assess_candidate_contract(data)["issues"])

    def test_partial_unknown_or_contradicted_not_promoted(self):
        for state in ("PARTIAL", "PENDING", "CONTRADICTED", True, None):
            data = fixture()
            data["evidence"]["dividend_reinvestment"]["state"] = state
            self.assertFalse(assess_candidate_contract(data)["metadata_valid"])

    def test_supported_without_reference_rejected(self):
        for refs in (None, [], [""], ["   "], [True], "a-reference"):
            data = fixture()
            data["evidence"]["revision_history"]["references"] = refs
            self.assertIn("EVIDENCE_REFERENCE_REQUIRED:revision_history",
                          assess_candidate_contract(data)["issues"])

    def test_price_and_total_return_cannot_mix(self):
        data = fixture()
        data["benchmark"]["return_basis"] = "PRICE"
        self.assertIn("RETURN_BASIS_MISMATCH", assess_candidate_contract(data)["issues"])

    def test_unknown_adjusted_basis_not_assumed_total_return(self):
        data = fixture()
        data["stock"]["return_basis"] = "ADJUSTED"
        self.assertIn("RETURN_BASIS_INVALID:stock", assess_candidate_contract(data)["issues"])

    def test_future_asof_or_publication_rejected_on_both_sides(self):
        for side in ("stock", "benchmark"):
            for key in ("as_of", "published_at"):
                data = fixture()
                data[side][key] = "2026-09-01T18:00:00+08:00"
                self.assertIn("FUTURE_INFORMATION:" + side + ":" + key,
                              assess_candidate_contract(data)["issues"])

    def test_timezone_equivalent_cutoff_accepted(self):
        data = fixture()
        data["decision_cutoff"] = "2026-09-01T08:00:00+00:00"
        self.assertTrue(assess_candidate_contract(data)["metadata_valid"])

    def test_naive_malformed_or_missing_times_rejected(self):
        for value in ("2026-09-01T16:00:00", "yesterday", None, True):
            for side in ("stock", "benchmark"):
                data = fixture()
                data[side]["as_of"] = value
                self.assertIn("TIME_INVALID:" + side + ":as_of",
                              assess_candidate_contract(data)["issues"])

    def test_raw_adjusted_identity_revision_and_snapshot_must_match(self):
        for key in ("series_id", "revision_id", "snapshot_id"):
            data = fixture()
            data["stock"]["raw_adjusted_pair"][key] = "other"
            self.assertIn("RAW_ADJUSTED_MISMATCH:" + key,
                          assess_candidate_contract(data)["issues"])

    def test_real_or_malformed_packet_rejected_without_exception(self):
        for value in (None, [], 1, {"synthetic_only": False}):
            self.assertFalse(assess_candidate_contract(value)["metadata_valid"])

    def test_missing_identity_and_version_are_reported(self):
        data = fixture()
        data["contract_version"] = "unknown"
        data["benchmark"]["series_id"] = ""
        issues = assess_candidate_contract(data)["issues"]
        self.assertIn("CONTRACT_VERSION_INVALID", issues)
        self.assertIn("IDENTITY_FIELD_REQUIRED:benchmark:series_id", issues)

    def test_input_not_mutated(self):
        data = fixture()
        before = copy.deepcopy(data)
        assess_candidate_contract(data)
        self.assertEqual(data, before)


if __name__ == "__main__":
    unittest.main()
