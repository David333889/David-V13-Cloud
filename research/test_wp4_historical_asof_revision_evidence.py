import copy
import unittest

from research.wp4_historical_asof_revision_evidence import (
    REQUIRED_HISTORICAL_EVIDENCE,
    assess_c10_evidence,
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
        "historical_evidence": {
            name: pending_claim()
            for name in REQUIRED_HISTORICAL_EVIDENCE
        },
        "as_of": "2026-09-30T17:30:00+08:00",
        "published_at": "2026-09-30T17:30:00+08:00",
        "retrieved_at": "2026-10-06T12:00:00+08:00",
        "decision_cutoff": "2026-09-30T18:00:00+08:00",
        "revision_timestamp": "2026-09-30T17:30:00+08:00",
        "snapshot_id": "SYNTHETIC_SNAPSHOT",
        "snapshot_sha256": "a" * 64,
        "provider_revision_id": "SYNTHETIC_PROVIDER_REVISION",
        "historical_authentication_complete": False,
        "revision_authentication_complete": False,
        "point_in_time_authentication_complete": False,
    }


def fully_supported_packet():
    candidate = packet()

    candidate["historical_evidence"] = {
        name: supported_claim()
        for name in REQUIRED_HISTORICAL_EVIDENCE
    }

    candidate["historical_authentication_complete"] = True
    candidate["revision_authentication_complete"] = True
    candidate["point_in_time_authentication_complete"] = True

    return candidate


class HistoricalAsOfRevisionEvidenceTests(unittest.TestCase):

    def test_current_pending_evidence_stays_blocked(self):
        result = assess_c10_evidence(packet())

        self.assertFalse(result["historical_asof_verified"])
        self.assertFalse(result["revision_provenance_verified"])
        self.assertFalse(result["point_in_time_verified"])
        self.assertFalse(result["lookahead_safe"])
        self.assertFalse(result["source_verified"])
        self.assertFalse(result["production_eligible"])
        self.assertEqual(result["execution_readiness"], "BLOCKED")

    def test_missing_packet_fails_closed(self):
        result = assess_c10_evidence(None)

        self.assertIn("PACKET_INVALID", result["issues"])
        self.assertFalse(result["lookahead_safe"])

    def test_real_input_cannot_promote_research_contract(self):
        candidate = fully_supported_packet()
        candidate["synthetic_only"] = False

        result = assess_c10_evidence(candidate)

        self.assertIn("RESEARCH_DECLARATION_REQUIRED", result["issues"])
        self.assertFalse(result["source_verified"])
        self.assertFalse(result["production_eligible"])

    def test_every_historical_evidence_item_is_required(self):
        for name in REQUIRED_HISTORICAL_EVIDENCE:
            candidate = packet()
            del candidate["historical_evidence"][name]

            result = assess_c10_evidence(candidate)

            self.assertIn(
                "HISTORICAL_EVIDENCE_MISSING:" + name,
                result["issues"],
            )
            self.assertFalse(result["historical_asof_verified"])

    def test_pending_claims_do_not_verify_historical_asof(self):
        result = assess_c10_evidence(packet())

        for name in REQUIRED_HISTORICAL_EVIDENCE:
            self.assertIn(
                "HISTORICAL_EVIDENCE_NOT_SUPPORTED:" + name,
                result["issues"],
            )

        self.assertFalse(result["historical_asof_verified"])

    def test_supported_claim_requires_reference(self):
        candidate = fully_supported_packet()
        candidate["historical_evidence"]["immutable_snapshot"][
            "references"
        ] = []

        result = assess_c10_evidence(candidate)

        self.assertIn(
            "HISTORICAL_EVIDENCE_REFERENCE_REQUIRED:immutable_snapshot",
            result["issues"],
        )
        self.assertFalse(result["historical_asof_verified"])

    def test_snapshot_identity_is_required(self):
        candidate = fully_supported_packet()
        candidate["snapshot_id"] = ""

        result = assess_c10_evidence(candidate)

        self.assertIn("SNAPSHOT_ID_REQUIRED", result["issues"])
        self.assertFalse(result["revision_provenance_verified"])
        self.assertFalse(result["lookahead_safe"])

    def test_snapshot_hash_is_required(self):
        for bad in (None, "", "abc", "g" * 64):
            candidate = fully_supported_packet()
            candidate["snapshot_sha256"] = bad

            result = assess_c10_evidence(candidate)

            self.assertIn("SNAPSHOT_SHA256_REQUIRED", result["issues"])
            self.assertFalse(result["revision_provenance_verified"])

    def test_provider_revision_identity_is_required(self):
        candidate = fully_supported_packet()
        candidate["provider_revision_id"] = ""

        result = assess_c10_evidence(candidate)

        self.assertIn("PROVIDER_REVISION_ID_REQUIRED", result["issues"])
        self.assertFalse(result["revision_provenance_verified"])

    def test_revision_timestamp_requires_timezone(self):
        candidate = fully_supported_packet()
        candidate["revision_timestamp"] = "2026-09-30T17:30:00"

        result = assess_c10_evidence(candidate)

        self.assertIn(
            "REVISION_TIMESTAMP_AWARE_TIMESTAMP_REQUIRED",
            result["issues"],
        )
        self.assertFalse(result["revision_provenance_verified"])

    def test_published_after_decision_cutoff_rejected(self):
        candidate = fully_supported_packet()
        candidate["published_at"] = "2026-09-30T18:30:00+08:00"

        result = assess_c10_evidence(candidate)

        self.assertIn(
            "PUBLISHED_AFTER_DECISION_CUTOFF",
            result["issues"],
        )
        self.assertFalse(result["point_in_time_verified"])
        self.assertFalse(result["lookahead_safe"])

    def test_asof_after_decision_cutoff_rejected(self):
        candidate = fully_supported_packet()
        candidate["as_of"] = "2026-09-30T19:00:00+08:00"

        result = assess_c10_evidence(candidate)

        self.assertIn(
            "AS_OF_AFTER_DECISION_CUTOFF",
            result["issues"],
        )
        self.assertFalse(result["point_in_time_verified"])

    def test_retrieved_at_does_not_replace_published_at(self):
        candidate = fully_supported_packet()
        candidate["published_at"] = None
        candidate["retrieved_at"] = "2026-09-30T17:00:00+08:00"

        result = assess_c10_evidence(candidate)

        self.assertIn(
            "PUBLISHED_AT_AWARE_TIMESTAMP_REQUIRED",
            result["issues"],
        )
        self.assertFalse(result["point_in_time_verified"])

    def test_naive_timestamps_are_rejected(self):
        fields = (
            "as_of",
            "published_at",
            "retrieved_at",
            "decision_cutoff",
        )

        for field in fields:
            candidate = fully_supported_packet()
            candidate[field] = "2026-09-30T17:30:00"

            result = assess_c10_evidence(candidate)

            self.assertFalse(result["point_in_time_verified"])
            self.assertFalse(result["lookahead_safe"])

    def test_revision_authentication_is_separate_from_asof(self):
        candidate = fully_supported_packet()
        candidate["revision_authentication_complete"] = False

        result = assess_c10_evidence(candidate)

        self.assertTrue(result["historical_asof_verified"])
        self.assertFalse(result["revision_provenance_verified"])
        self.assertFalse(result["point_in_time_verified"])

    def test_point_in_time_authentication_is_separate(self):
        candidate = fully_supported_packet()
        candidate["point_in_time_authentication_complete"] = False

        result = assess_c10_evidence(candidate)

        self.assertTrue(result["historical_asof_verified"])
        self.assertTrue(result["revision_provenance_verified"])
        self.assertFalse(result["point_in_time_verified"])
        self.assertFalse(result["lookahead_safe"])

    def test_all_supported_research_evidence_still_blocks_production(self):
        result = assess_c10_evidence(fully_supported_packet())

        self.assertTrue(result["historical_asof_verified"])
        self.assertTrue(result["revision_provenance_verified"])
        self.assertTrue(result["point_in_time_verified"])
        self.assertTrue(result["lookahead_safe"])

        self.assertFalse(result["source_verified"])
        self.assertFalse(result["production_eligible"])
        self.assertEqual(result["execution_readiness"], "BLOCKED")

    def test_input_not_mutated(self):
        candidate = fully_supported_packet()
        original = copy.deepcopy(candidate)

        assess_c10_evidence(candidate)

        self.assertEqual(candidate, original)


if __name__ == "__main__":
    unittest.main()
