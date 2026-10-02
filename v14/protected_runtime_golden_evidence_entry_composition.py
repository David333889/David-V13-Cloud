"""
Gate 28D.2K-3G
Protected Runtime Golden Evidence Entry Composition V1.

Thin composition boundary for an already-protected runtime
executor and the existing Gate 28D.2K-3D Golden Evidence
integration.

The runtime executor retains its existing one-shot authority.
This module does not introduce another authorization guard.

This module does not build a runtime entry, create a Session,
perform an HTTP request, read a secret, normalize market data,
enter Core, score, decide, or persist data.
"""

from v14.real_get_golden_evidence_integration import (
    build_real_get_golden_evidence,
)


READ_ONLY = True
COMPOSITION_ONLY = True
ONE_SHOT_ONLY = True
MAX_REAL_GETS = 1

ALLOW_NETWORK_EXECUTION = False
ALLOW_SESSION_CREATION = False

ALLOW_RAW_PAYLOAD_STORAGE = False
ALLOW_SECRET_STORAGE = False

ALLOW_CORE_INPUT = False
ALLOW_SCORE = False
ALLOW_DECISION = False
ALLOW_SUPABASE_WRITE = False
ALLOW_PRODUCTION_WRITE = False


def _deny(reason):
    return {
        "allowed": False,
        "reason": reason,
    }


def execute_runtime_entry_golden_evidence(
    runtime_executor,
    params,
):
    """
    Execute an already-protected runtime executor and convert
    its RAW_EVIDENCE immediately into sanitized Golden Evidence.

    The existing runtime executor remains the one-shot
    authority. No additional guard is introduced here.
    """

    if not callable(runtime_executor):
        return _deny("RUNTIME_EXECUTOR_REQUIRED")

    try:
        execution = runtime_executor()
    except Exception:
        return _deny("RUNTIME_EXECUTION_FAILURE")

    if not isinstance(execution, dict):
        return _deny("RUNTIME_EXECUTION_INVALID")

    if execution.get("allowed") is not True:
        return _deny(
            execution.get(
                "reason",
                "RUNTIME_EXECUTION_REJECTED",
            )
        )

    evidence = execution.get("evidence")

    if not isinstance(evidence, dict):
        return _deny("EVIDENCE_REQUIRED")

    golden_result = build_real_get_golden_evidence(
        evidence=evidence,
        params=params,
    )

    if golden_result.get("allowed") is not True:
        return _deny(
            golden_result.get(
                "reason",
                "GOLDEN_EVIDENCE_REJECTED",
            )
        )

    return {
        "allowed": True,
        "golden": golden_result.get("golden"),
    }
