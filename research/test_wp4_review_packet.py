"""End-to-end candidate packet tests exercise cross-layer binding failures."""
import copy
import hashlib
import os
from pathlib import Path
import tempfile
import unittest
from unittest.mock import patch
import uuid

from research.test_wp4_evidence_contract import fixture
from research.test_wp4_observation_quality import observed
from research.wp4_review_packet import review_synthetic_packet


class ReviewPacketTests(unittest.TestCase):
    def setUp(self):
        self.root = Path(os.environ.get("DAVID_TEST_TMP", tempfile.gettempdir())) / uuid.uuid4().hex
        self.root.mkdir()
        self.addCleanup(self._cleanup)
        raw = b'{"fixture":true}'
        (self.root / "proof.json").write_bytes(raw)
        entry = {"artifact_id": "proof", "path": "proof.json", "kind": "REVIEW_RECORD",
                 "source_url": "https://example.test/fixture",
                 "retrieved_at": "2026-09-01T16:00:00+08:00",
                 "sha256": hashlib.sha256(raw).hexdigest(), "bytes": len(raw),
                 "revision_id": "r1", "claim": "Synthetic declarations", "limitations": "Not source evidence",
                 "locator": {"type": "JSON_POINTER", "value": "/fixture"}}
        contract = fixture()
        for claim in contract["evidence"].values():
            claim["references"] = ["proof"]
        stock, benchmark = observed(), observed(100, 105)
        for side, data in (("stock", stock), ("benchmark", benchmark)):
            data["series_metadata"] = copy.deepcopy(contract[side])
        after = {"synthetic_only": True, "snapshot_id": "s1",
                 "artifacts": [{"artifact_id": "proof", "sha256": entry["sha256"], "revision_id": "r1"}]}
        self.packet = {"synthetic_only": True, "contract": contract, "artifacts": [entry],
                       "observations": {"stock": stock, "benchmark": benchmark, "lookback": 1},
                       "revision": {"before": copy.deepcopy(after), "after": after,
                                    "windows": [{"window_id": "RS", "artifact_ids": ["proof"]}]},
                       "review_window_id": "RS"}

    def _cleanup(self):
        (self.root / "proof.json").unlink(missing_ok=True)
        self.root.rmdir()

    def review(self):
        return review_synthetic_packet(self.root, self.packet)

    def test_valid_fixture_yields_metrics_without_source_promotion(self):
        result = self.review()
        self.assertTrue(result["candidate_checks_passed"])
        self.assertAlmostEqual(result["metrics"]["gross_relative_return"], 1.1 / 1.05 - 1)
        self.assertFalse(result["source_verified"])
        self.assertEqual(result["execution_readiness"], "BLOCKED")
        for key in ("signal_emitted", "ranking_emitted", "market_state_emitted", "runtime_results_invalidated"):
            self.assertFalse(result[key])

    def test_contract_gap_prevents_computation(self):
        self.packet["contract"]["evidence"]["corporate_action_factors"]["state"] = "PARTIAL"
        with patch("research.wp4_review_packet.compare_quality_checked_candidates") as calculate:
            result = self.review()
            calculate.assert_not_called()
        self.assertIn("contract", result["blocking_layers"])
        self.assertIsNone(result["metrics"])

    def test_file_tampering_blocks_metrics(self):
        (self.root / "proof.json").write_bytes(b'{"fixture":false}')
        result = self.review()
        self.assertIn("integrity", result["blocking_layers"])
        self.assertIsNone(result["metrics"])

    def test_references_must_bind_to_intake(self):
        self.packet["contract"]["evidence"]["return_basis"]["references"] = ["other"]
        self.assertIn("binding", self.review()["blocking_layers"])

    def test_observation_identity_must_match_contract(self):
        self.packet["observations"]["stock"]["series_metadata"]["series_id"] = "OTHER"
        self.assertIn("binding", self.review()["blocking_layers"])

    def test_revision_hash_must_match_actual_intake_manifest(self):
        self.packet["revision"]["after"]["artifacts"][0]["sha256"] = "c" * 64
        self.assertIn("binding", self.review()["blocking_layers"])

    def test_changed_dependency_blocks_old_window(self):
        self.packet["revision"]["before"]["snapshot_id"] = "s0"
        self.packet["revision"]["before"]["artifacts"][0]["sha256"] = "c" * 64
        result = self.review()
        self.assertIn("revision", result["blocking_layers"])
        self.assertIsNone(result["metrics"])

    def test_carried_price_blocks_last_layer(self):
        self.packet["observations"]["stock"]["records"][0]["observation_status"] = "CARRIED"
        result = self.review()
        self.assertEqual(result["blocking_layers"], ["observations"])
        self.assertIsNone(result["metrics"])

    def test_missing_review_window_and_dependency_set_rejected(self):
        for dependency in (None, [], [{}]):
            self.packet["revision"]["windows"][0]["artifact_ids"] = dependency
            self.assertIn("binding", self.review()["blocking_layers"])

    def test_snapshot_metadata_mismatch_rejected(self):
        self.packet["contract"]["stock"]["snapshot_id"] = "wrong"
        self.assertIn("binding", self.review()["blocking_layers"])

    def test_real_and_malformed_input_rejected_without_promotion(self):
        for packet in (None, [], {"synthetic_only": False}, {"synthetic_only": True}):
            result = review_synthetic_packet(self.root, packet)
            self.assertFalse(result["candidate_checks_passed"])
            self.assertIsNone(result["metrics"])

    def test_input_not_mutated(self):
        saved = copy.deepcopy(self.packet)
        self.review()
        self.assertEqual(self.packet, saved)


if __name__ == "__main__":
    unittest.main()
