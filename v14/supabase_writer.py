from typing import Any, Dict


WRITER_VERSION = "V14_SUPABASE_WRITER_V1"
TARGET_TABLE = "stock_history"
CONFLICT_KEY = "trade_date,code"


def _result(
    state: str,
    reason: str,
    response=None,
) -> Dict[str, Any]:
    return {
        "version": WRITER_VERSION,
        "state": state,
        "reason": reason,
        "response": response,
    }


def write_supabase_row(
    persistence_result: Any,
    client: Any,
) -> Dict[str, Any]:
    """
    V14 Supabase Writer V1.

    Safety boundary:
    - accepts READY Persistence V1 result only
    - requires an injected client
    - does not create a Supabase client
    - does not recalculate Core / Risk / Action
    - does not modify database schema
    - writes only to stock_history
    - uses trade_date,code as conflict key

    Network I/O occurs only through the injected client.
    Tests must use a mock client.
    """

    if not isinstance(persistence_result, dict):
        return _result(
            "BLOCKED",
            "INVALID_PERSISTENCE_RESULT",
        )

    if persistence_result.get("state") != "READY":
        return _result(
            "BLOCKED",
            "PERSISTENCE_NOT_READY",
        )

    row = persistence_result.get("row")

    if not isinstance(row, dict) or not row:
        return _result(
            "BLOCKED",
            "ROW_MISSING",
        )

    if client is None:
        return _result(
            "BLOCKED",
            "CLIENT_MISSING",
        )

    try:
        response = (
            client
            .table(TARGET_TABLE)
            .upsert(
                row,
                on_conflict=CONFLICT_KEY,
            )
            .execute()
        )
    except Exception as exc:
        return _result(
            "ERROR",
            "UPSERT_FAILED",
            str(exc),
        )

    return _result(
        "SAVED",
        "UPSERT_OK",
        response,
    )