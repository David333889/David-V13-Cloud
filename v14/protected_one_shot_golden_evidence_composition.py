"""
Gate 28D.2K-3E
Protected One-Shot Golden Evidence Composition V1.

Thin composition boundary joining the existing protected
one-shot authorization path with the existing sanitized
Golden Evidence integration.

This module does not create a Session, perform an HTTP
request, read a secret, normalize market data, enter Core,
score, decide, or persist data.
"""

from v14.controlled_real_internet_crossing_one_shot_integration import (
    execute_controlled_real_internet_crossing_once,
)
from v14.real_get_golden_evidence_integration import (
    build_real_get_golden_evidence,
)


READ_ONLY = True
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


def execute_protected_one_shot_golden_evidence(
    guard,
    executor,
    params,
):
    """
    Authorize exactly once, obtain injected RAW_EVIDENCE,
    and convert it immediately into sanitized Golden Evidence.

    The public result contains Golden Evidence only.
    """

    execution = (
        execute_controlled_real_internet_crossing_once(
            guard=guard,
            executor=executor,
        )
    )

    if execution.get("allowed") is not True:
        return _deny(
            execution.get(
                "reason",
                "EXECUTION_REJECTED",
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
