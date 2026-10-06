"""Revision planning checks for stale-result and dependency risks."""
import copy
import unittest
from research.wp4_revision_impact import assess_revision_impact


def snapshot(ident="s1"):
    return {"synthetic_only": True, "snapshot_id": ident, "artifacts": [
        {"artifact_id": "stock", "sha256": "a" * 64, "revision_id": "r1"},
        {"artifact_id": "benchmark", "sha256": "b" * 64, "revision_id": "r1"},
    ]}


def windows():
    return [{"window_id": "RS", "artifact_ids": ["stock", "benchmark"]},
            {"window_id": "BENCHMARK", "artifact_ids": ["benchmark"]}]


class RevisionImpactTests(unittest.TestCase):
    def test_stock_content_change_marks_only_declared_dependents(self):
        after = snapshot("s2")
        after["artifacts"][0]["sha256"] = "c" * 64
        result = assess_revision_impact(snapshot(), after, windows())
        self.assertTrue(result["assessment_valid"])
        self.assertEqual(result["windows_needing_review"],
                         [{"window_id": "RS", "changed_dependencies": ["stock"]}])
        self.assertEqual(result["unaffected_by_declared_changes"], ["BENCHMARK"])
        self.assertFalse(result["source_verified"])
        self.assertFalse(result["runtime_results_invalidated"])
        self.assertEqual(result["execution_readiness"], "BLOCKED")

    def test_benchmark_change_marks_both_windows(self):
        after = snapshot("s2")
        after["artifacts"][1]["sha256"] = "c" * 64
        self.assertEqual(len(assess_revision_impact(snapshot(), after, windows())["windows_needing_review"]), 2)

    def test_revision_change_without_content_change_still_requires_review(self):
        after = snapshot("s2")
        after["artifacts"][0]["revision_id"] = "r2"
        self.assertEqual(assess_revision_impact(snapshot(), after, windows())["artifact_changes"][0]["change"],
                         "REVISION_METADATA_CHANGED")

    def test_removed_dependency_marks_window(self):
        after = snapshot("s2")
        after["artifacts"].pop(0)
        self.assertEqual(assess_revision_impact(snapshot(), after, windows())["artifact_changes"][0]["change"], "REMOVED")

    def test_added_artifact_not_previously_reviewed(self):
        after = snapshot("s2")
        after["artifacts"].append({"artifact_id": "calendar", "sha256": "c" * 64, "revision_id": "r1"})
        checks = windows() + [{"window_id": "NEW", "artifact_ids": ["calendar"]}]
        result = assess_revision_impact(snapshot(), after, checks)
        self.assertEqual(result["windows_needing_review"], [{"window_id": "NEW", "changed_dependencies": ["calendar"]}])

    def test_new_snapshot_same_artifacts_is_not_a_content_change(self):
        result = assess_revision_impact(snapshot(), snapshot("s2"), windows())
        self.assertTrue(result["assessment_valid"])
        self.assertEqual(result["windows_needing_review"], [])
        self.assertEqual(len(result["unaffected_by_declared_changes"]), 2)

    def test_reused_snapshot_id_with_changed_content_rejected(self):
        after = snapshot()
        after["artifacts"][0]["sha256"] = "c" * 64
        self.assertEqual(assess_revision_impact(snapshot(), after, windows())["reason"], "IMMUTABLE_SNAPSHOT_ID_REUSED")

    def test_unknown_duplicate_and_empty_dependencies_rejected(self):
        for deps in (["unknown"], ["stock", "stock"], [], [None]):
            self.assertFalse(assess_revision_impact(snapshot(), snapshot("s2"),
                             [{"window_id": "RS", "artifact_ids": deps}])["assessment_valid"])

    def test_duplicate_artifact_or_window_rejected(self):
        after = snapshot("s2")
        after["artifacts"].append(copy.deepcopy(after["artifacts"][0]))
        self.assertEqual(assess_revision_impact(snapshot(), after, windows())["reason"], "DUPLICATE_ARTIFACT_ID")
        self.assertEqual(assess_revision_impact(snapshot(), snapshot("s2"), windows() + [windows()[0]])["reason"],
                         "DUPLICATE_WINDOW_ID")

    def test_invalid_hash_version_and_real_input_rejected(self):
        for key, value in (("sha256", None), ("sha256", "not-a-hash"), ("revision_id", "")):
            after = snapshot("s2")
            after["artifacts"][0][key] = value
            self.assertFalse(assess_revision_impact(snapshot(), after, windows())["assessment_valid"])
        after = snapshot("s2")
        after["synthetic_only"] = False
        self.assertFalse(assess_revision_impact(snapshot(), after, windows())["assessment_valid"])

    def test_input_not_mutated(self):
        before, after, checks = snapshot(), snapshot("s2"), windows()
        saved = copy.deepcopy((before, after, checks))
        assess_revision_impact(before, after, checks)
        self.assertEqual((before, after, checks), saved)

    def test_malformed_empty_inputs_and_hash_case(self):
        for bad in (None, [], {}, {"synthetic_only": True, "snapshot_id": "s2", "artifacts": []}):
            self.assertFalse(assess_revision_impact(snapshot(), bad, windows())["assessment_valid"])
        after = snapshot("s2")
        after["artifacts"][0]["sha256"] = "A" * 64
        self.assertEqual(assess_revision_impact(snapshot(), after, windows())["artifact_changes"], [])


if __name__ == "__main__":
    unittest.main()
