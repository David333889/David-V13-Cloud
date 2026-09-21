from typing import Any, Dict

from v14.runtime_pipeline import build_runtime_persistence
from v14.supabase_writer import write_supabase_row


CONTRACT_VERSION = "V14_RUNTIME_WRITER_V1"


def _result(
    state: str,
    reason: str,
) -> Dict[str, Any]:
    return {
        "version": CONTRACT_VERSION,
        "state": state,
        "reason": reason,
    }


def write_runtime_result(
    result: Any,
    identity: Any,
    client: Any,
) -> Dict[str, Any]:
    """
    V14 Runtime Writer Wiring V1.

    Orchestration only:

        Core Result + Identity
            -> Runtime Pipeline
            -> READY Persistence Result
            -> Supabase Writer V1
            -> Injected Client

    Safety boundary:
        - client must be externally injected
        - does not create Supabase client
        - does not modify schema
        - does not recalculate Core/Risk/Action
        - does not modify Persistence Row
    """

    if client is None:
        return _result(
            "BLOCKED",
            "CLIENT_MISSING",
        )

    try:
        persistence_result = build_runtime_persistence(
            result,
            identity,
        )

        if not isinstance(persistence_result, dict):
            return _result(
                "BLOCKED",
                "PERSISTENCE_RESULT_INVALID",
            )

        if persistence_result.get("state") != "READY":
            return persistence_result

        return write_supabase_row(
            persistence_result,
            client,
        )

    except Exception as exc:
        return _result(
            "BLOCKED",
            f"RUNTIME_WRITER_EXCEPTION:{type(exc).__name__}",
        )