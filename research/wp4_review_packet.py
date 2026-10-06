"""Offline synthetic review composition; no provider or production integration."""
from research.wp4_evidence_contract import assess_candidate_contract, REQUIREMENTS
from research.wp4_evidence_intake import audit_intake
from research.wp4_observation_quality import compare_quality_checked_candidates
from research.wp4_revision_impact import assess_revision_impact

SERIES_FIELDS = ("provider", "dataset", "series_id", "revision_id", "snapshot_id", "return_basis")


def review_synthetic_packet(root, packet):
    result = {"candidate_checks_passed": False, "research_only": True,
              "source_verified": False, "execution_readiness": "BLOCKED",
              "signal_emitted": False, "ranking_emitted": False,
              "market_state_emitted": False, "runtime_results_invalidated": False,
              "layers": {}, "blocking_layers": [], "metrics": None}
    if not isinstance(packet, dict) or packet.get("synthetic_only") is not True:
        result["blocking_layers"] = ["SYNTHETIC_PACKET_ONLY"]
        return result
    contract = packet.get("contract")
    entries = packet.get("artifacts")
    observations = packet.get("observations")
    revision = packet.get("revision")
    if not isinstance(contract, dict):
        contract = {}
    if not isinstance(observations, dict):
        observations = {}
    if not isinstance(revision, dict):
        revision = {}
    layers = result["layers"]
    layers["contract"] = assess_candidate_contract(contract)
    layers["integrity"] = audit_intake(root, entries)
    layers["revision"] = assess_revision_impact(
        revision.get("before"), revision.get("after"), revision.get("windows"))
    binding_issues = []
    artifact_map = {entry["artifact_id"]: entry for entry in entries
                    if isinstance(entry, dict) and isinstance(entry.get("artifact_id"), str)} if isinstance(entries, list) else {}
    for name in REQUIREMENTS:
        claim = contract.get("evidence", {}).get(name) if isinstance(contract.get("evidence"), dict) else None
        references = claim.get("references") if isinstance(claim, dict) else None
        if not isinstance(references, list) or any(
            not isinstance(ref, str) or ref not in artifact_map for ref in references
        ):
            binding_issues.append("UNBOUND_EVIDENCE:" + name)
    for side in ("stock", "benchmark"):
        expected = contract.get(side)
        actual = observations.get(side)
        metadata = actual.get("series_metadata") if isinstance(actual, dict) else None
        if not isinstance(expected, dict) or not isinstance(metadata, dict) or any(
            metadata.get(key) != expected.get(key) for key in SERIES_FIELDS
        ):
            binding_issues.append("OBSERVATION_IDENTITY_MISMATCH:" + side)
    after = revision.get("after")
    revised_artifacts = after.get("artifacts") if isinstance(after, dict) else None
    if isinstance(revised_artifacts, list):
        revised_map = {}
        for item in revised_artifacts:
            if not isinstance(item, dict) or not isinstance(item.get("artifact_id"), str):
                continue
            ident = item["artifact_id"]
            revised_map[ident] = item
            entry = artifact_map.get(ident)
            if entry is None or str(item.get("sha256", "")).lower() != str(entry.get("sha256", "")).lower() or item.get("revision_id") != entry.get("revision_id"):
                binding_issues.append("REVISION_ARTIFACT_MISMATCH:" + ident)
        if set(revised_map) != set(artifact_map):
            binding_issues.append("REVISION_INTAKE_SET_MISMATCH")
        for side in ("stock", "benchmark"):
            expected = contract.get(side)
            if isinstance(expected, dict) and expected.get("snapshot_id") != after.get("snapshot_id"):
                binding_issues.append("SERIES_SNAPSHOT_MISMATCH:" + side)
    else:
        binding_issues.append("REVISION_ARTIFACT_BINDING_REQUIRED")
    required = packet.get("review_window_id")
    windows = revision.get("windows")
    registered = [window for window in windows if isinstance(window, dict) and window.get("window_id") == required] if isinstance(windows, list) else []
    if not isinstance(required, str) or not required.strip() or len(registered) != 1:
        binding_issues.append("REVIEW_WINDOW_REQUIRED")
    else:
        dependencies = registered[0].get("artifact_ids")
        if not isinstance(dependencies, list) or any(not isinstance(item, str) for item in dependencies):
            binding_issues.append("REVIEW_DEPENDENCY_SET_MISMATCH")
        elif set(dependencies) != set(artifact_map):
            binding_issues.append("REVIEW_DEPENDENCY_SET_MISMATCH")
    layers["binding"] = {"valid": not binding_issues, "issues": binding_issues}
    if not layers["contract"]["metadata_valid"]:
        result["blocking_layers"].append("contract")
    if not layers["integrity"]["intake_valid"]:
        result["blocking_layers"].append("integrity")
    if not layers["binding"]["valid"]:
        result["blocking_layers"].append("binding")
    if not layers["revision"]["assessment_valid"] or layers["revision"]["windows_needing_review"]:
        result["blocking_layers"].append("revision")
    if result["blocking_layers"]:
        layers["observations"] = {"status": "NOT_RUN_PREREQUISITES_BLOCKED"}
        return result
    quality = compare_quality_checked_candidates(observations.get("stock"), observations.get("benchmark"),
                                                 observations.get("lookback"))
    layers["observations"] = quality
    if not quality["allowed"]:
        result["blocking_layers"].append("observations")
        return result
    result["candidate_checks_passed"] = True
    result["metrics"] = {key: quality[key] for key in
                        ("stock_return", "benchmark_return", "return_difference", "gross_relative_return")}
    return result
