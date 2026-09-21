from typing import Any, Dict

from v14.consumer_boundary import evaluate_consumer_boundary
from v14.integration_payload import build_integration_payload
from v14.storage_adapter import build_storage_record
from v14.supabase_persistence_adapter import build_supabase_row


CONTRACT_VERSION = "V14_RUNTIME_PIPELINE_V1"


def _result(state: str, reason: str, row=None) -> Dict[str, Any]:
    return {
        "state": state,
        "reason": reason,
        "row": row,
    }


def build_runtime_persistence(
    result: Any,
    identity: Any,
) -> Dict[str, Any]:
    """
    V14 Runtime Pipeline V1.

    Pure orchestration only:

        Core Result
            -> Consumer Boundary
            -> Integration Payload
            -> Storage Record
            -> Persistence Row

    Safety boundary:
        - no Supabase client
        - no Writer
        - no network I/O
        - no schema mutation
        - no Core/Risk/Action recomputation
    """

    try:
        consumer_result = evaluate_consumer_boundary(result)

        if not isinstance(consumer_result, dict):
            return _result(
                "BLOCKED",
                "CONSUMER_RESULT_INVALID",
            )

        if consumer_result.get("state") != "READY":
            return _result(
                "BLOCKED",
                consumer_result.get(
                    "reason",
                    "CONSUMER_NOT_READY",
                ),
            )

        integration_result = build_integration_payload(
            result,
            consumer_result,
            identity,
        )

        if not isinstance(integration_result, dict):
            return _result(
                "BLOCKED",
                "INTEGRATION_RESULT_INVALID",
            )

        if integration_result.get("state") != "READY":
            return _result(
                "BLOCKED",
                integration_result.get(
                    "reason",
                    "INTEGRATION_NOT_READY",
                ),
            )

        storage_result = build_storage_record(
            integration_result
        )

        if not isinstance(storage_result, dict):
            return _result(
                "BLOCKED",
                "STORAGE_RESULT_INVALID",
            )

        if storage_result.get("state") != "READY":
            return _result(
                "BLOCKED",
                storage_result.get(
                    "reason",
                    "STORAGE_NOT_READY",
                ),
            )

        persistence_result = build_supabase_row(
            storage_result
        )

        if not isinstance(persistence_result, dict):
            return _result(
                "BLOCKED",
                "PERSISTENCE_RESULT_INVALID",
            )

        return persistence_result

    except Exception as exc:
        return _result(
            "BLOCKED",
            f"RUNTIME_PIPELINE_EXCEPTION:{type(exc).__name__}",
        )