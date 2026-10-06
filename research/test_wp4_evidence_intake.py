"""Local artifacts exercise tampering, missing provenance and path boundaries."""
import copy
import hashlib
import json
import os
from pathlib import Path
import tempfile
import uuid
import unittest
from unittest.mock import patch
from research.wp4_evidence_intake import audit_artifact, audit_intake


class EvidenceIntakeTests(unittest.TestCase):
    def setUp(self):
        self.root = Path(os.environ.get("DAVID_TEST_TMP", tempfile.gettempdir())) / uuid.uuid4().hex
        self.root.mkdir()
        self.addCleanup(self._cleanup_fixture)
        self.raw = b'{"facts":{"a/b":42,"rows":[1,2]}}'
        (self.root / "source.json").write_bytes(self.raw)
        self.entry = {"artifact_id": "fixture", "path": "source.json",
                      "kind": "ORIGINAL_SNAPSHOT", "source_url": "https://example.test/doc",
                      "retrieved_at": "2026-10-06T10:00:00+08:00",
                      "claim": "Fixture only", "limitations": "Not official evidence",
                      "sha256": hashlib.sha256(self.raw).hexdigest(), "bytes": len(self.raw),
                      "locator": {"type": "JSON_POINTER", "value": "/facts/a~1b"}}

    def _cleanup_fixture(self):
        (self.root / "source.json").unlink(missing_ok=True)
        self.root.rmdir()

    def test_valid_local_hash_and_pointer_does_not_verify_source(self):
        result = audit_intake(self.root, [self.entry])
        self.assertTrue(result["intake_valid"])
        self.assertFalse(result["source_verified"])
        self.assertEqual(result["execution_readiness"], "BLOCKED")

    def test_changed_contents_rejected(self):
        (self.root / "source.json").write_bytes(b'{"facts":{"a/b":43}}')
        self.assertIn("HASH_MISMATCH", audit_artifact(self.root, self.entry)["integrity_issues"])

    def test_missing_artifact_rejected(self):
        self.entry["path"] = "absent.json"
        self.assertIn("ARTIFACT_MISSING", audit_artifact(self.root, self.entry)["integrity_issues"])

    def test_traversal_and_absolute_paths_rejected(self):
        for path in ("../outside.txt", str(self.root / "source.json")):
            self.entry["path"] = path
            self.assertIn("PATH_OUTSIDE_ROOT", audit_artifact(self.root, self.entry)["integrity_issues"])

    def test_missing_hash_and_wrong_size_rejected(self):
        self.entry["sha256"] = None
        self.entry["bytes"] = True
        issues = audit_artifact(self.root, self.entry)["integrity_issues"]
        self.assertIn("HASH_REQUIRED", issues)
        self.assertIn("EXPECTED_SIZE_REQUIRED", issues)

    def test_pointer_missing_or_invalid_escape_rejected(self):
        for pointer in ("/facts/nope", "/facts/a~2b", "/facts/rows/99", "/facts/rows/-1"):
            self.entry["locator"]["value"] = pointer
            self.assertFalse(audit_artifact(self.root, self.entry)["integrity_valid"])

    def test_exact_text_locator_and_missing_text(self):
        self.entry["locator"] = {"type": "TEXT", "value": '"a/b"'}
        self.assertTrue(audit_artifact(self.root, self.entry)["integrity_valid"])
        self.entry["locator"]["value"] = "absent claim"
        self.assertFalse(audit_artifact(self.root, self.entry)["integrity_valid"])

    def test_unknown_retrieval_time_not_fabricated(self):
        self.entry["retrieved_at"] = None
        result = audit_artifact(self.root, self.entry)
        self.assertTrue(result["integrity_valid"])
        self.assertFalse(result["metadata_complete"])
        self.assertIn("RETRIEVAL_TIME_UNKNOWN", result["metadata_issues"])

    def test_review_record_not_promoted_to_original_snapshot(self):
        self.entry["kind"] = "REVIEW_RECORD"
        result = audit_artifact(self.root, self.entry)
        self.assertTrue(result["integrity_valid"])
        self.assertEqual(result["artifact_kind"], "REVIEW_RECORD")
        self.assertFalse(result["source_verified"])

    def test_duplicate_id_and_empty_intake_rejected(self):
        self.assertIn("DUPLICATE_ARTIFACT_ID", audit_intake(self.root, [self.entry, self.entry])["issues"])
        self.assertFalse(audit_intake(self.root, [])["intake_valid"])

    def test_invalid_entries_and_non_utf8_do_not_raise(self):
        self.assertFalse(audit_intake(self.root, [None])["intake_valid"])
        (self.root / "source.json").write_bytes(b'\xff')
        self.assertFalse(audit_artifact(self.root, self.entry)["integrity_valid"])

    def test_input_not_mutated(self):
        before = copy.deepcopy(self.entry)
        audit_intake(self.root, [self.entry])
        self.assertEqual(self.entry, before)

    def test_declared_legacy_encoding_and_unknown_encoding(self):
        raw = "臺股 IX0001".encode("cp950")
        (self.root / "source.json").write_bytes(raw)
        self.entry.update(sha256=hashlib.sha256(raw).hexdigest(), bytes=len(raw),
                          locator={"type": "TEXT", "value": "臺股", "encoding": "cp950"})
        self.assertTrue(audit_artifact(self.root, self.entry)["integrity_valid"])
        self.entry["locator"]["encoding"] = "unknown-encoding"
        self.assertFalse(audit_artifact(self.root, self.entry)["integrity_valid"])

    def test_size_limit_refuses_artifact_before_processing(self):
        with patch("research.wp4_evidence_intake.MAX_ARTIFACT_BYTES", 5):
            self.assertIn("ARTIFACT_TOO_LARGE",
                          audit_artifact(self.root, self.entry)["integrity_issues"])


if __name__ == "__main__":
    unittest.main()
