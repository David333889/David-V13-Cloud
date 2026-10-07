"""WP4 C10 historical as-of and revision evidence-gap contract.

Research-only validation of evidence declarations.

This module does not:
- fetch historical market data,
- create or authenticate provider revisions,
- reconstruct historical vintages,
- certify point-in-time availability,
- authorize backtests, live use, or production use.
"""

from datetime import datetime


REQUIRED_HISTORICAL_EVIDENCE = (
    "historical_asof_retrieval",
    "immutable_snapshot",
    "provider_revision_identity",
    "revision_timestamp",
    "correction_history",
    "point_in_time_availability",
    "published_at_evidence",
    "decision_cutoff_alignment",
)


def _parse_aware_timestamp(value):
    if not isinstance(value, str) or not value.strip():
        return None

    try:
        parsed = datetime.fromisoformat(value.replace("Z", "+00:00"))
    except ValueError:
        return None

    if parsed.tzinfo is None or parsed.utcoffset() is None:
        return None

    return parsed


def _supported_claim(claim):
    if not isinstance(claim, dict):
        return False, "MISSING"

    if claim.get("state") != "SUPPORTED":
        return False, "NOT_SUPPORTED"

    references = claim.get("references")

    if (
        not isinstance(references, list)
        or not references
        or any(
            not isinstance(reference, str) or not reference.strip()
            for reference in references
        )
    ):
        return False, "REFERENCE_REQUIRED"

    return True, None


def assess_c10_evidence(packet):
    """Fail closed unless historical-version evidence is complete."""

    result = {
        "contract": "WP4_C10_HISTORICAL_ASOF_REVISION_EVIDENCE_GAP_V1",
        "research_only": True,
        "historical_asof_verified": False,
        "revision_provenance_verified": False,
        "point_in_time_verified": False,
        "lookahead_safe": False,
        "source_verified": False,
        "production_eligible": False,
        "execution_readiness": "BLOCKED",
        "issues": [],
    }

    if not isinstance(packet, dict):
        result["issues"].append("PACKET_INVALID")
        return result

    if packet.get("synthetic_only") is not True:
        result["issues"].append("RESEARCH_DECLARATION_REQUIRED")

    evidence = packet.get("historical_evidence")

    if not isinstance(evidence, dict):
        evidence = {}

    for name in REQUIRED_HISTORICAL_EVIDENCE:
        ok, reason = _supported_claim(evidence.get(name))

        if not ok:
            result["issues"].append(
                "HISTORICAL_EVIDENCE_" + reason + ":" + name
            )

    historical_issue = any(
        issue.startswith("HISTORICAL_EVIDENCE_")
        for issue in result["issues"]
    )

    as_of = _parse_aware_timestamp(packet.get("as_of"))
    published_at = _parse_aware_timestamp(packet.get("published_at"))
    retrieved_at = _parse_aware_timestamp(packet.get("retrieved_at"))
    decision_cutoff = _parse_aware_timestamp(packet.get("decision_cutoff"))
    revision_timestamp = _parse_aware_timestamp(
        packet.get("revision_timestamp")
    )

    if as_of is None:
        result["issues"].append("AS_OF_AWARE_TIMESTAMP_REQUIRED")

    if published_at is None:
        result["issues"].append("PUBLISHED_AT_AWARE_TIMESTAMP_REQUIRED")

    if retrieved_at is None:
        result["issues"].append("RETRIEVED_AT_AWARE_TIMESTAMP_REQUIRED")

    if decision_cutoff is None:
        result["issues"].append("DECISION_CUTOFF_AWARE_TIMESTAMP_REQUIRED")

    if revision_timestamp is None:
        result["issues"].append("REVISION_TIMESTAMP_AWARE_TIMESTAMP_REQUIRED")

    if (
        published_at is not None
        and decision_cutoff is not None
        and published_at > decision_cutoff
    ):
        result["issues"].append("PUBLISHED_AFTER_DECISION_CUTOFF")

    if (
        as_of is not None
        and decision_cutoff is not None
        and as_of > decision_cutoff
    ):
        result["issues"].append("AS_OF_AFTER_DECISION_CUTOFF")

    snapshot_id = packet.get("snapshot_id")
    if not isinstance(snapshot_id, str) or not snapshot_id.strip():
        result["issues"].append("SNAPSHOT_ID_REQUIRED")

    snapshot_sha256 = packet.get("snapshot_sha256")
    if (
        not isinstance(snapshot_sha256, str)
        or len(snapshot_sha256) != 64
        or any(c not in "0123456789abcdefABCDEF" for c in snapshot_sha256)
    ):
        result["issues"].append("SNAPSHOT_SHA256_REQUIRED")

    provider_revision_id = packet.get("provider_revision_id")
    if (
        not isinstance(provider_revision_id, str)
        or not provider_revision_id.strip()
    ):
        result["issues"].append("PROVIDER_REVISION_ID_REQUIRED")

    provenance_issues = {
        "SNAPSHOT_ID_REQUIRED",
        "SNAPSHOT_SHA256_REQUIRED",
        "PROVIDER_REVISION_ID_REQUIRED",
        "REVISION_TIMESTAMP_AWARE_TIMESTAMP_REQUIRED",
    }

    time_issues = {
        "AS_OF_AWARE_TIMESTAMP_REQUIRED",
        "PUBLISHED_AT_AWARE_TIMESTAMP_REQUIRED",
        "RETRIEVED_AT_AWARE_TIMESTAMP_REQUIRED",
        "DECISION_CUTOFF_AWARE_TIMESTAMP_REQUIRED",
        "PUBLISHED_AFTER_DECISION_CUTOFF",
        "AS_OF_AFTER_DECISION_CUTOFF",
    }

    result["historical_asof_verified"] = (
        not historical_issue
        and as_of is not None
        and packet.get("historical_authentication_complete") is True
    )

    result["revision_provenance_verified"] = (
        result["historical_asof_verified"]
        and not any(issue in provenance_issues for issue in result["issues"])
        and packet.get("revision_authentication_complete") is True
    )

    result["point_in_time_verified"] = (
        result["revision_provenance_verified"]
        and not any(issue in time_issues for issue in result["issues"])
        and packet.get("point_in_time_authentication_complete") is True
    )

    result["lookahead_safe"] = result["point_in_time_verified"]

    # Deliberately fail closed:
    # research evidence completion never grants source or production authority.
    return result
