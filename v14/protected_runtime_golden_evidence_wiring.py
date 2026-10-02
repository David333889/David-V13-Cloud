"""
Gate 28D.2K-3F
Protected Runtime Golden Evidence Wiring V1.

Thin wiring boundary joining an injected protected runtime
executor with the existing Gate 28D.2K-3E protected one-shot
Golden Evidence composition.

This module does not build a runtime entry, create a Session,
perform an HTTP request, read a secret, normalize market data,
enter Core, score, decide, or persist data.
"""

from v14.protected_one_shot_golden_evidence_composition import (
    execute_protected_one_shot_golden_evidence,
)



READ_ONLY = True
WIRING_ONLY = True
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


def execute_protected_runtime_golden_evidence(
    guard,
    runtime_executor,
    params,
):
    """
    Wire an already-built protected runtime executor into
    the existing protected one-shot Golden Evidence path.

    No runtime entry, Session, HTTP request, or secret access
    is created by this wiring boundary itself.
    """

    if not callable(runtime_executor):
        return {
            "allowed": False,
            "reason": "RUNTIME_EXECUTOR_REQUIRED",
        }

    return execute_protected_one_shot_golden_evidence(
        guard=guard,
        executor=runtime_executor,
        params=params,
    )