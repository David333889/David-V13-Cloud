"""Synthetic evidence-contract metadata checks, without evidence promotion."""
from datetime import datetime

REQUIREMENTS = (
    "series_identity", "return_basis", "corporate_action_factors",
    "dividend_reinvestment", "observation_provenance", "trading_calendar",
    "revision_history", "publication_time",
)


def _instant(value):
    if not isinstance(value, str):
        return None
    try:
        parsed = datetime.fromisoformat(value)
    except ValueError:
        return None
    if parsed.tzinfo is None or parsed.utcoffset() is None:
        return None
    return parsed


def assess_candidate_contract(packet):
    """Check declarations only; refs and SUPPORTED claims are not authenticated.

    The decision cutoff constrains declared as-of and publication times, not the
    acquisition time. A later download does not prove past availability.
    """
    issues = []
    def issue(code):
        if code not in issues:
            issues.append(code)
    if not isinstance(packet, dict) or packet.get("synthetic_only") is not True:
        issue("SYNTHETIC_CONTRACT_ONLY")
        packet = {}
    if packet.get("contract_version") != "WP4_EVIDENCE_CANDIDATE_V1":
        issue("CONTRACT_VERSION_INVALID")
    cutoff = _instant(packet.get("decision_cutoff"))
    if cutoff is None:
        issue("DECISION_CUTOFF_INVALID")
    evidence = packet.get("evidence")
    if not isinstance(evidence, dict):
        evidence = {}
    for name in REQUIREMENTS:
        claim = evidence.get(name)
        if not isinstance(claim, dict) or claim.get("state") != "SUPPORTED":
            issue("EVIDENCE_INCOMPLETE:" + name)
            continue
        refs = claim.get("references")
        if not isinstance(refs, list) or not refs or any(
            not isinstance(ref, str) or not ref.strip() for ref in refs
        ):
            issue("EVIDENCE_REFERENCE_REQUIRED:" + name)
    bases = []
    for side in ("stock", "benchmark"):
        series = packet.get(side)
        if not isinstance(series, dict):
            issue("SERIES_REQUIRED:" + side)
            continue
        for key in ("provider", "dataset", "series_id", "revision_id", "snapshot_id"):
            value = series.get(key)
            if not isinstance(value, str) or not value.strip():
                issue("IDENTITY_FIELD_REQUIRED:" + side + ":" + key)
        basis = series.get("return_basis")
        if basis not in ("PRICE", "TOTAL_RETURN"):
            issue("RETURN_BASIS_INVALID:" + side)
        bases.append(basis)
        for key in ("as_of", "published_at"):
            instant = _instant(series.get(key))
            if instant is None:
                issue("TIME_INVALID:" + side + ":" + key)
            elif cutoff is not None and instant > cutoff:
                issue("FUTURE_INFORMATION:" + side + ":" + key)
        if side == "stock":
            pairs = series.get("raw_adjusted_pair")
            if not isinstance(pairs, dict):
                issue("RAW_ADJUSTED_PAIR_REQUIRED")
            else:
                for key in ("series_id", "revision_id", "snapshot_id"):
                    if pairs.get(key) != series.get(key):
                        issue("RAW_ADJUSTED_MISMATCH:" + key)
    if len(bases) == 2 and bases[0] != bases[1]:
        issue("RETURN_BASIS_MISMATCH")
    return {
        "metadata_valid": not issues, "issues": issues, "research_only": True,
        "source_verified": False, "live_eligible": False,
        "execution_readiness": "BLOCKED",
    }
