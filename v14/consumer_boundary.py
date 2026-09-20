from typing import Any, Dict


CONTRACT_VERSION = "V14_CONSUMER_BOUNDARY_V1"

REQUIRED_V13_DOMAINS = (
    "market_input",
    "technical",
    "status",
    "six_buy",
    "six_sell",
    "position",
    "decision",
    "ranking",
)

REQUIRED_RISK_FIELDS = (
    "version",
    "state",
    "level",
    "lock",
    "factors",
)

REQUIRED_ACTION_FIELDS = (
    "version",
    "state",
    "signal",
    "reason",
    "risk_guard",
    "confidence",
)


def _result(state: str, reason: str) -> Dict[str, str]:
    return {
        "version": CONTRACT_VERSION,
        "state": state,
        "reason": reason,
    }


def evaluate_consumer_boundary(result: Any) -> Dict[str, str]:
    """
    Gate 6 Consumer Boundary V1.

    Validates whether a completed V14 CoreEngineResult-style payload
    is structurally safe for downstream consumers.

    This function:
    - does not recalculate Gate 3 domains
    - does not recalculate Risk
    - does not recalculate Action
    - does not modify Core Decision
    - performs no external integration
    """

    if not isinstance(result, dict):
        return _result("BLOCKED", "INVALID_RESULT_TYPE")

    engine_version = result.get("engine_version")
    baseline_version = result.get("baseline_version")

    if not engine_version or not baseline_version:
        return _result("BLOCKED", "VERSION_MISSING")

    for domain in REQUIRED_V13_DOMAINS:
        if domain not in result:
            return _result("BLOCKED", "REQUIRED_DOMAIN_MISSING")

    if "risk" not in result or result.get("risk") is None:
        return _result("BLOCKED", "RISK_CONTRACT_MISSING")

    risk = result.get("risk")

    if not isinstance(risk, dict):
        return _result("BLOCKED", "INVALID_RISK_CONTRACT")

    if any(field not in risk for field in REQUIRED_RISK_FIELDS):
        return _result("BLOCKED", "INVALID_RISK_CONTRACT")

    if risk.get("version") != "V14_RISK_V1":
        return _result("BLOCKED", "INVALID_RISK_CONTRACT")

    if "action" not in result or result.get("action") is None:
        return _result("BLOCKED", "ACTION_CONTRACT_MISSING")

    action = result.get("action")

    if not isinstance(action, dict):
        return _result("BLOCKED", "INVALID_ACTION_CONTRACT")

    if any(field not in action for field in REQUIRED_ACTION_FIELDS):
        return _result("BLOCKED", "INVALID_ACTION_CONTRACT")

    if action.get("version") != "V14_ACTION_V1":
        return _result("BLOCKED", "INVALID_ACTION_CONTRACT")

    return _result("READY", "CONTRACT_OK")