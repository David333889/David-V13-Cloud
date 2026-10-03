"""
Gate 28D.2K-3L
Protected Runtime Semantic Golden Evidence Composition V1.

Thin composition boundary joining an already-protected runtime
executor with the existing Gate 28D.2K-3K semantic Golden
Evidence composition.

The runtime executor retains its existing execution authority.
Existing 3K retains semantic-observation and Golden-integration
ordering authority.

This module does not create a Session, perform an HTTP request,
read a secret, normalize market data, enter Core, score, decide,
or persist data.
"""

from v14.golden_evidence_semantic_observer_composition import (
    build_semantically_observed_golden_evidence,
)


READ_ONLY = True
COMPOSITION_ONLY = True

ALLOW_NETWORK_EXECUTION = False
ALLOW_SESSION_CREATION = False
ALLOW_REAL_GET_EXECUTION = False

ALLOW_RAW_PAYLOAD_STORAGE = False
ALLOW_SECRET_STORAGE = False

ALLOW_NORMALIZATION = False
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


def execute_protected_runtime_semantic_golden_evidence(
    runtime_executor,
    params,
):
    """
    Execute an already-protected runtime executor and delegate
    accepted RAW_EVIDENCE to the existing 3K semantic Golden
    Evidence composition.
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

    semantic_result = (
        build_semantically_observed_golden_evidence(
            evidence=evidence,
            params=params,
        )
    )

    if semantic_result.get("allowed") is not True:
        return _deny(
            semantic_result.get(
                "reason",
                "SEMANTIC_GOLDEN_EVIDENCE_REJECTED",
            )
        )

    return {
        "allowed": True,
        "golden": semantic_result.get("golden"),
    }
