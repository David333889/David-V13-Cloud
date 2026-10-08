"""WP4 C07/C12 reinvestment and economic-equivalence evidence-gap contract.

Research-only validation of evidence declarations.

This module does not:
- calculate total return,
- calculate reinvestment,
- fetch market data,
- authenticate providers,
- authorize live or production use.
"""

STOCK_DATASET = "TaiwanStockPriceAdj"
BENCHMARK_DATASET = "TaiwanStockTotalReturnIndex"

REQUIRED_REINVESTMENT_EVIDENCE = (
    "cash_dividend_treatment",
    "reinvestment_date",
    "reinvestment_price",
    "tax_treatment",
    "fee_treatment",
    "fractional_share_treatment",
    "cash_capital_reduction_treatment",
    "rights_treatment",
)

REQUIRED_EQUIVALENCE_EVIDENCE = (
    "stock_return_basis",
    "benchmark_return_basis",
    "cash_flow_alignment",
    "event_timing_alignment",
    "tax_fee_alignment",
    "fractional_share_alignment",
    "capital_reduction_alignment",
    "rights_alignment",
)


def _supported_claim(claim):
    if not isinstance(claim, dict):
        return False, "MISSING"

    if claim.get("state") != "SUPPORTED":
        return False, "NOT_SUPPORTED"

    refs = claim.get("references")

    if (
        not isinstance(refs, list)
        or not refs
        or any(not isinstance(ref, str) or not ref.strip() for ref in refs)
    ):
        return False, "REFERENCE_REQUIRED"

    return True, None


def assess_c07_c12_evidence(packet):
    """Fail closed unless reinvestment and equivalence evidence are complete."""

    result = {
        "contract": "WP4_C07_C12_REINVESTMENT_ECONOMIC_EQUIVALENCE_EVIDENCE_GAP_V1",
        "research_only": True,
        "dataset_identity_supported": False,
        "reinvestment_verified": False,
        "economic_equivalence_verified": False,
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

    identities = packet.get("dataset_identity")

    if not isinstance(identities, dict):
        result["issues"].append("DATASET_IDENTITY_REQUIRED")
        identities = {}

    if identities.get("stock_dataset") != STOCK_DATASET:
        result["issues"].append("STOCK_DATASET_IDENTITY_MISMATCH")

    if identities.get("benchmark_dataset") != BENCHMARK_DATASET:
        result["issues"].append("BENCHMARK_DATASET_IDENTITY_MISMATCH")

    if identities.get("benchmark_id") != "TAIEX":
        result["issues"].append("BENCHMARK_IDENTITY_MISMATCH")

    identity_issues = {
        "DATASET_IDENTITY_REQUIRED",
        "STOCK_DATASET_IDENTITY_MISMATCH",
        "BENCHMARK_DATASET_IDENTITY_MISMATCH",
        "BENCHMARK_IDENTITY_MISMATCH",
    }

    result["dataset_identity_supported"] = not any(
        issue in identity_issues for issue in result["issues"]
    )

    reinvestment = packet.get("reinvestment_evidence")
    if not isinstance(reinvestment, dict):
        reinvestment = {}

    for name in REQUIRED_REINVESTMENT_EVIDENCE:
        ok, reason = _supported_claim(reinvestment.get(name))

        if not ok:
            result["issues"].append(
                "REINVESTMENT_EVIDENCE_" + reason + ":" + name
            )

    reinvestment_issue = any(
        issue.startswith("REINVESTMENT_EVIDENCE_")
        for issue in result["issues"]
    )

    result["reinvestment_verified"] = (
        packet.get("synthetic_only") is True
        and result["dataset_identity_supported"]
        and not reinvestment_issue
        and packet.get("reinvestment_authentication_complete") is True
    )

    equivalence = packet.get("equivalence_evidence")
    if not isinstance(equivalence, dict):
        equivalence = {}

    for name in REQUIRED_EQUIVALENCE_EVIDENCE:
        ok, reason = _supported_claim(equivalence.get(name))

        if not ok:
            result["issues"].append(
                "EQUIVALENCE_EVIDENCE_" + reason + ":" + name
            )

    equivalence_issue = any(
        issue.startswith("EQUIVALENCE_EVIDENCE_")
        for issue in result["issues"]
    )

    result["economic_equivalence_verified"] = (
        result["dataset_identity_supported"]
        and result["reinvestment_verified"]
        and not equivalence_issue
        and packet.get("equivalence_authentication_complete") is True
    )

    # Deliberately fail closed:
    # research evidence completion never grants source or production authority.
    return result
