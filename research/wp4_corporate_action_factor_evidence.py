"""WP4 C06 corporate-action factor evidence-gap contract.

Research-only validation of evidence declarations.
This module does not calculate adjustment factors, authenticate providers,
fetch market data, or authorize production use.
"""

SUPPORTED_EVENT_TYPES = (
    "EX_RIGHT_DIVIDEND",
    "CAPITAL_REDUCTION",
    "STOCK_SPLIT",
    "PAR_VALUE_CHANGE",
)

REQUIRED_FORMULA_EVIDENCE = (
    "exact_formula",
    "numerator_denominator",
    "same_day_event_order",
    "precision",
    "rounding",
    "exception_rules",
)


def assess_c06_evidence(packet):
    """Fail closed unless every exact-formula evidence item is supported."""

    result = {
        "contract": "WP4_C06_CORPORATE_ACTION_FACTOR_EVIDENCE_GAP_V1",
        "research_only": True,
        "framework_supported": False,
        "formula_verified": False,
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

    framework = packet.get("framework")

    if not isinstance(framework, dict):
        result["issues"].append("FRAMEWORK_REQUIRED")
        framework = {}

    if framework.get("adjustment_direction") != "BACKWARD":
        result["issues"].append("BACKWARD_ADJUSTMENT_EVIDENCE_REQUIRED")

    if framework.get("event_day_adjusted_equals_raw") is not True:
        result["issues"].append("EVENT_DAY_IDENTITY_EVIDENCE_REQUIRED")

    if framework.get("event_day_after_close_inclusion") is not True:
        result["issues"].append("EVENT_TIMING_EVIDENCE_REQUIRED")

    if framework.get("holiday_shift_to_actual_trading_date") is not True:
        result["issues"].append("HOLIDAY_SHIFT_EVIDENCE_REQUIRED")

    events = framework.get("event_types")

    if (
        not isinstance(events, list)
        or any(not isinstance(event, str) for event in events)
        or len(events) != len(set(events))
        or set(events) != set(SUPPORTED_EVENT_TYPES)
    ):
        result["issues"].append("EVENT_TAXONOMY_EVIDENCE_REQUIRED")

    framework_issue_codes = {
        "FRAMEWORK_REQUIRED",
        "BACKWARD_ADJUSTMENT_EVIDENCE_REQUIRED",
        "EVENT_DAY_IDENTITY_EVIDENCE_REQUIRED",
        "EVENT_TIMING_EVIDENCE_REQUIRED",
        "HOLIDAY_SHIFT_EVIDENCE_REQUIRED",
        "EVENT_TAXONOMY_EVIDENCE_REQUIRED",
    }

    result["framework_supported"] = not any(
        issue in framework_issue_codes for issue in result["issues"]
    )

    formula = packet.get("formula_evidence")

    if not isinstance(formula, dict):
        formula = {}

    for name in REQUIRED_FORMULA_EVIDENCE:
        claim = formula.get(name)

        if not isinstance(claim, dict):
            result["issues"].append("FORMULA_EVIDENCE_MISSING:" + name)
            continue

        if claim.get("state") != "SUPPORTED":
            result["issues"].append("FORMULA_EVIDENCE_NOT_SUPPORTED:" + name)
            continue

        refs = claim.get("references")

        if (
            not isinstance(refs, list)
            or not refs
            or any(not isinstance(ref, str) or not ref.strip() for ref in refs)
        ):
            result["issues"].append("FORMULA_REFERENCE_REQUIRED:" + name)

    formula_issue = any(
        issue.startswith("FORMULA_") for issue in result["issues"]
    )

    result["formula_verified"] = (
        packet.get("synthetic_only") is True
        and result["framework_supported"]
        and not formula_issue
        and packet.get("formula_authentication_complete") is True
    )

    # C06 remains non-production even when a synthetic evidence declaration
    # is complete. Promotion requires a separate authenticated source gate.
    return result
