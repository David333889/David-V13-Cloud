"""
Gate 28D.2K-3D
Real GET -> Golden Evidence Integration V1.

Offline integration boundary for converting FinMind
RAW_EVIDENCE into sanitized Golden Evidence.

This module performs no environment read, secret read,
Session creation, HTTP request, network execution,
Core/Score/Decision execution, or persistence write.
"""

from v14.finmind_golden_evidence import (
    build_finmind_golden_evidence,
)


READ_ONLY = True
CONTRACT_ONLY = True

ALLOW_NETWORK_EXECUTION = False
ALLOW_REAL_GET_EXECUTION = False
ALLOW_SESSION_CREATION = False

ALLOW_RAW_PAYLOAD_STORAGE = False
ALLOW_SECRET_STORAGE = False

ALLOW_CORE_INPUT = False
ALLOW_SCORE = False
ALLOW_DECISION = False
ALLOW_SUPABASE_WRITE = False
ALLOW_PRODUCTION_WRITE = False


def build_real_get_golden_evidence(
    evidence,
    params,
):
    """
    Convert already-supplied FinMind RAW_EVIDENCE into
    sanitized Golden Evidence.

    This function does not fetch, replay, persist, or expose
    raw payload or secret material.
    """

    return build_finmind_golden_evidence(
        evidence=evidence,
        params=params,
    )
