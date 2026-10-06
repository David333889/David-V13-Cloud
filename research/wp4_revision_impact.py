"""Synthetic revision-impact planning only; never changes runtime results."""
import re


def _name(value):
    return isinstance(value, str) and bool(value.strip()) and value == value.strip()


def _snapshot(value):
    if not isinstance(value, dict) or value.get("synthetic_only") is not True:
        return None, "SYNTHETIC_SNAPSHOT_ONLY"
    if not _name(value.get("snapshot_id")):
        return None, "SNAPSHOT_ID_REQUIRED"
    artifacts = value.get("artifacts")
    if not isinstance(artifacts, list) or not artifacts:
        return None, "ARTIFACT_LIST_REQUIRED"
    result = {}
    for artifact in artifacts:
        if not isinstance(artifact, dict) or not _name(artifact.get("artifact_id")):
            return None, "ARTIFACT_ID_INVALID"
        ident = artifact["artifact_id"]
        if ident in result:
            return None, "DUPLICATE_ARTIFACT_ID"
        sha = artifact.get("sha256")
        if not isinstance(sha, str) or not re.fullmatch(r"[0-9a-fA-F]{64}", sha):
            return None, "ARTIFACT_HASH_INVALID"
        if not _name(artifact.get("revision_id")):
            return None, "ARTIFACT_REVISION_REQUIRED"
        result[ident] = (sha.lower(), artifact["revision_id"])
    return result, None


def assess_revision_impact(before, after, windows):
    """Identify dependent windows needing review from declared hashes/versions.

    Hashes and dependency completeness are declarations, not verified evidence.
    A change is conservative at artifact level, not a finding about price rows.
    """
    result = {
        "assessment_valid": False, "research_only": True, "source_verified": False,
        "execution_readiness": "BLOCKED", "artifact_changes": [],
        "windows_needing_review": [], "unaffected_by_declared_changes": [],
        "runtime_results_invalidated": False,
    }
    old, reason = _snapshot(before)
    if reason:
        return dict(result, reason=reason)
    new, reason = _snapshot(after)
    if reason:
        return dict(result, reason=reason)
    if before["snapshot_id"] == after["snapshot_id"] and old != new:
        return dict(result, reason="IMMUTABLE_SNAPSHOT_ID_REUSED")
    if not isinstance(windows, list) or not windows:
        return dict(result, reason="WINDOW_LIST_REQUIRED")
    registered = {}
    known = set(old) | set(new)
    for window in windows:
        if not isinstance(window, dict) or not _name(window.get("window_id")):
            return dict(result, reason="WINDOW_ID_INVALID")
        ident = window["window_id"]
        if ident in registered:
            return dict(result, reason="DUPLICATE_WINDOW_ID")
        dependencies = window.get("artifact_ids")
        if not isinstance(dependencies, list) or not dependencies or any(
            not _name(dependency) for dependency in dependencies
        ):
            return dict(result, reason="DEPENDENCIES_REQUIRED")
        if len(dependencies) != len(set(dependencies)):
            return dict(result, reason="DUPLICATE_DEPENDENCY")
        if any(dependency not in known for dependency in dependencies):
            return dict(result, reason="UNKNOWN_DEPENDENCY")
        registered[ident] = set(dependencies)
    changed = set()
    for ident in sorted(known):
        if ident not in old:
            change = "ADDED"
        elif ident not in new:
            change = "REMOVED"
        elif old[ident][0] != new[ident][0]:
            change = "CONTENT_CHANGED"
        elif old[ident][1] != new[ident][1]:
            change = "REVISION_METADATA_CHANGED"
        else:
            continue
        changed.add(ident)
        result["artifact_changes"].append({"artifact_id": ident, "change": change})
    for ident, dependencies in registered.items():
        affected = sorted(dependencies & changed)
        if affected:
            result["windows_needing_review"].append(
                {"window_id": ident, "changed_dependencies": affected})
        else:
            result["unaffected_by_declared_changes"].append(ident)
    result.update(assessment_valid=True, reason="CANDIDATE_IMPACT_PLAN_ONLY")
    return result
