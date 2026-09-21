from typing import Any, Dict


PERSISTENCE_VERSION = "V14_SUPABASE_PERSISTENCE_V1"

REQUIRED_FIELDS = (
    "trade_date",
    "code",
    "name",
    "market",
    "symbol",
    "buy_score",
    "sell_score",
    "fib_position",
    "decision",
    "payload_version",
    "engine_version",
    "baseline_version",
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


def _result(state: str, reason: str, row=None) -> Dict[str, Any]:
    return {
        "version": PERSISTENCE_VERSION,
        "state": state,
        "reason": reason,
        "row": row,
    }


def build_supabase_row(storage_record: Any) -> Dict[str, Any]:
    """
    V14 Supabase Persistence Adapter V1.

    Pure mapping / validation boundary.

    This function:
    - accepts Storage Record V1 output only
    - does not recalculate Core
    - does not recalculate Risk
    - does not recalculate Action
    - does not import core_engine
    - does not connect to Supabase
    - does not execute SQL
    - does not perform network I/O
    - does not modify database schema

    Legacy Market Snapshot fields remain DEFERRED.
    """

    if not isinstance(storage_record, dict):
        return _result(
            "BLOCKED",
            "INVALID_STORAGE_RECORD_TYPE",
        )

    # Storage Adapter returns an outer result envelope.
    if storage_record.get("state") != "READY":
        return _result(
            "BLOCKED",
            "STORAGE_RECORD_NOT_READY",
        )

    record = storage_record.get("record")

    if not isinstance(record, dict):
        return _result(
            "BLOCKED",
            "INVALID_STORAGE_RECORD",
        )

    missing = [
        field
        for field in REQUIRED_FIELDS
        if field not in record
    ]

    if missing:
        return _result(
            "BLOCKED",
            "MISSING_REQUIRED_FIELD",
        )

    row = {
        field: record[field]
        for field in REQUIRED_FIELDS
    }

    return _result(
        "READY",
        "PERSISTENCE_ROW_OK",
        row,
    )