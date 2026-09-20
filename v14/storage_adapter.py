from typing import Any, Dict


STORAGE_VERSION = "V14_STORAGE_RECORD_V1"
SOURCE_CONTRACT = "V14_INTEGRATION_PAYLOAD_V1"


def _result(
    state: str,
    reason: str,
    record=None,
) -> Dict[str, Any]:
    return {
        "version": STORAGE_VERSION,
        "state": state,
        "reason": reason,
        "record": record,
    }


def build_storage_record(
    integration_result: Any,
) -> Dict[str, Any]:
    """
    V14 Storage Record V1.

    Converts a validated V14 Integration Payload V1 result into
    a local, database-compatible storage record.

    This function:
    - does not call run_core()
    - does not recalculate trading logic
    - does not recalculate Risk
    - does not recalculate Action
    - does not call Consumer Boundary
    - does not modify Integration Payload
    - does not connect to Streamlit
    - does not connect to Supabase
    - does not execute SQL
    - does not perform network I/O
    """

    if not isinstance(integration_result, dict):
        return _result(
            "BLOCKED",
            "INVALID_INTEGRATION_RESULT",
        )

    if integration_result.get("state") != "READY":
        return _result(
            "BLOCKED",
            "INTEGRATION_NOT_READY",
        )

    payload = integration_result.get("payload")

    if not isinstance(payload, dict):
        return _result(
            "BLOCKED",
            "PAYLOAD_MISSING",
        )

    metadata = payload.get("metadata")
    identity = payload.get("identity")
    core = payload.get("core")
    safety = payload.get("safety")

    required_metadata = (
        "payload_version",
        "engine_version",
        "baseline_version",
    )

    if not isinstance(metadata, dict) or any(
        key not in metadata
        or metadata.get(key) in (None, "")
        for key in required_metadata
    ):
        return _result(
            "BLOCKED",
            "STORAGE_MAPPING_MISSING",
        )

    if metadata.get("payload_version") != SOURCE_CONTRACT:
        return _result(
            "BLOCKED",
            "STORAGE_MAPPING_MISSING",
        )

    required_identity = (
        "trade_date",
        "code",
        "name",
        "market",
        "symbol",
    )

    if not isinstance(identity, dict) or any(
        key not in identity
        or identity.get(key) in (None, "")
        for key in required_identity
    ):
        return _result(
            "BLOCKED",
            "STORAGE_MAPPING_MISSING",
        )

    required_core = (
        "buy_score",
        "sell_score",
        "fib_position",
        "decision",
    )

    if not isinstance(core, dict) or any(
        key not in core
        or core.get(key) is None
        for key in required_core
    ):
        return _result(
            "BLOCKED",
            "STORAGE_MAPPING_MISSING",
        )

    required_safety = (
        "risk_state",
        "risk_level",
        "risk_lock",
        "action_state",
        "action_signal",
        "action_reason",
        "action_risk_guard",
        "action_confidence",
        "consumer_state",
    )

    if not isinstance(safety, dict) or any(
        key not in safety
        or safety.get(key) in (None, "")
        for key in required_safety
    ):
        return _result(
            "BLOCKED",
            "STORAGE_MAPPING_MISSING",
        )

    record = {
        "trade_date": identity["trade_date"],
        "code": identity["code"],
        "name": identity["name"],
        "market": identity["market"],
        "symbol": identity["symbol"],

        "buy_score": core["buy_score"],
        "sell_score": core["sell_score"],
        "fib_position": core["fib_position"],
        "decision": core["decision"],

        "payload_version": metadata["payload_version"],
        "engine_version": metadata["engine_version"],
        "baseline_version": metadata["baseline_version"],

        "risk_state": safety["risk_state"],
        "risk_level": safety["risk_level"],
        "risk_lock": safety["risk_lock"],

        "action_state": safety["action_state"],
        "action_signal": safety["action_signal"],
        "action_reason": safety["action_reason"],
        "action_risk_guard": safety["action_risk_guard"],
        "action_confidence": safety["action_confidence"],

        "consumer_state": safety["consumer_state"],
    }

    return _result(
        "READY",
        "STORAGE_RECORD_OK",
        record,
    )