from typing import Any, Dict


PAYLOAD_VERSION = "V14_INTEGRATION_PAYLOAD_V1"


def _result(state: str, reason: str, payload=None) -> Dict[str, Any]:
    return {
        "version": PAYLOAD_VERSION,
        "state": state,
        "reason": reason,
        "payload": payload,
    }


def build_integration_payload(
    result: Any,
    consumer_boundary: Any,
    identity: Any,
) -> Dict[str, Any]:
    """
    V14 Integration Payload V1.

    Packages validated V14 Core output for future downstream consumers.

    This function:
    - does not recalculate Gate 3 domains
    - does not recalculate Risk
    - does not recalculate Action
    - does not modify Core Decision
    - does not connect to Streamlit
    - does not connect to Supabase
    - does not call external APIs
    - does not write to a database
    """

    if not isinstance(result, dict):
        return _result("BLOCKED", "INVALID_RESULT_TYPE")

    if not isinstance(consumer_boundary, dict):
        return _result("BLOCKED", "CONSUMER_NOT_READY")

    if consumer_boundary.get("state") != "READY":
        return _result("BLOCKED", "CONSUMER_NOT_READY")

    if not isinstance(identity, dict):
        return _result("BLOCKED", "IDENTITY_MISSING")

    required_identity = (
        "trade_date",
        "code",
        "name",
        "market",
        "symbol",
    )

    if any(
        key not in identity or identity.get(key) in (None, "")
        for key in required_identity
    ):
        return _result("BLOCKED", "IDENTITY_MISSING")

    six_buy = result.get("six_buy")
    six_sell = result.get("six_sell")
    position = result.get("position")
    decision = result.get("decision")

    if not isinstance(six_buy, dict) or "score" not in six_buy:
        return _result("BLOCKED", "CORE_MAPPING_MISSING")

    if not isinstance(six_sell, dict) or "score" not in six_sell:
        return _result("BLOCKED", "CORE_MAPPING_MISSING")

    if not isinstance(position, dict) or "fib_position" not in position:
        return _result("BLOCKED", "CORE_MAPPING_MISSING")

    if not isinstance(decision, dict) or "core_decision" not in decision:
        return _result("BLOCKED", "CORE_MAPPING_MISSING")

    risk = result.get("risk")

    required_risk = (
        "state",
        "level",
        "lock",
    )

    if not isinstance(risk, dict) or any(
        key not in risk for key in required_risk
    ):
        return _result("BLOCKED", "SAFETY_MAPPING_MISSING")

    action = result.get("action")

    required_action = (
        "state",
        "signal",
        "reason",
        "risk_guard",
        "confidence",
    )

    if not isinstance(action, dict) or any(
        key not in action for key in required_action
    ):
        return _result("BLOCKED", "SAFETY_MAPPING_MISSING")

    engine_version = result.get("engine_version")
    baseline_version = result.get("baseline_version")

    if not engine_version or not baseline_version:
        return _result("BLOCKED", "CORE_MAPPING_MISSING")

    payload = {
        "metadata": {
            "payload_version": PAYLOAD_VERSION,
            "engine_version": engine_version,
            "baseline_version": baseline_version,
        },
        "identity": {
            "trade_date": identity["trade_date"],
            "code": identity["code"],
            "name": identity["name"],
            "market": identity["market"],
            "symbol": identity["symbol"],
        },
        "core": {
            "buy_score": six_buy["score"],
            "sell_score": six_sell["score"],
            "fib_position": position["fib_position"],
            "decision": decision["core_decision"],
        },
        "safety": {
            "risk_state": risk["state"],
            "risk_level": risk["level"],
            "risk_lock": risk["lock"],
            "action_state": action["state"],
            "action_signal": action["signal"],
            "action_reason": action["reason"],
            "action_risk_guard": action["risk_guard"],
            "action_confidence": action["confidence"],
            "consumer_state": consumer_boundary["state"],
        },
    }

    return _result("READY", "PAYLOAD_OK", payload)