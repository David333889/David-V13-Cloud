"""
Gate 28D.2K-3K
Golden Evidence Semantic Observer Composition V1.

Thin composition boundary joining the existing FinMind
baseline evidence observer with the existing 3D Golden
Evidence integration.

Order:
1. Validate the request identity carried by params.
2. Reuse the existing baseline semantic observer.
3. Stop immediately when semantic observation is denied.
4. Delegate accepted RAW_EVIDENCE into the existing
   Golden Evidence integration.
5. Return sanitized Golden Evidence only.

This module does not perform a network request, create a
Session, normalize market data, enter Core, score, decide,
or persist data.
"""

from v14.finmind_baseline_evidence_observer import (
    observe_finmind_baseline_evidence,
)
from v14.real_get_golden_evidence_integration import (
    build_real_get_golden_evidence,
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


def build_semantically_observed_golden_evidence(
    evidence,
    params,
):
    """
    Require semantic observation before Golden Evidence
    conversion.

    Existing 2B owns baseline semantic validation.
    Existing 3D owns Golden Evidence conversion.
    """

    if not isinstance(params, dict):
        return _deny("PARAMS_REQUIRED")

    stock_id = params.get("data_id")
    start_date = params.get("start_date")
    end_date = params.get("end_date")

    if not isinstance(stock_id, str) or not stock_id:
        return _deny("PARAMS_INVALID")

    if (
        not isinstance(start_date, str)
        or not start_date
        or not isinstance(end_date, str)
        or not end_date
    ):
        return _deny("PARAMS_INVALID")

    if start_date != end_date:
        return _deny("SINGLE_DAY_REQUIRED")

    observation_result = observe_finmind_baseline_evidence(
        evidence=evidence,
        stock_id=stock_id,
        trading_date=start_date,
    )

    if observation_result.get("allowed") is not True:
        return _deny(
            observation_result.get(
                "reason",
                "OBSERVATION_REJECTED",
            )
        )

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
