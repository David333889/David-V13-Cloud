# Gate 28D.2K-2C - Controlled Real Sample
# Acquisition Implementation V1.
#
# Thin read-only orchestration only.
# Reuses existing protected validation, controlled fetch,
# and baseline evidence observer boundaries.

from v14.controlled_live_fetch import (
    execute_controlled_fetch,
)
from v14.finmind_baseline_evidence_observer import (
    observe_finmind_baseline_evidence,
)
from v14.finmind_live_request_parameters import (
    validate_finmind_live_params,
)


READ_ONLY = True
ONE_SHOT_ONLY = True
SINGLE_STOCK_ONLY = True
SINGLE_TRADING_DATE_ONLY = True

ALLOW_NORMALIZATION = False
ALLOW_COMPATIBILITY_ESTABLISHMENT = False
ALLOW_PROVIDER_SWITCH = False
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


def execute_controlled_real_sample_acquisition(
    env,
    session_factory,
    url,
    timeout,
    params,
    stock_id,
    trading_date,
    max_bytes=5_000_000,
):
    """
    Execute one controlled read-only sample acquisition.

    Order:
    1. Validate FinMind request parameters.
    2. Execute exactly through the protected controlled-fetch path.
    3. Observe one stock / one trading-date baseline record.
    4. Return the seven-field observation only.

    No normalization, compatibility establishment,
    provider switching, Core input, scoring, decision,
    or persistence is performed here.
    """

    # 1. Fail closed before Session / GET when params are invalid.
    params_result = validate_finmind_live_params(
        params,
    )

    if params_result.get("allowed") is not True:
        return _deny(
            params_result.get(
                "reason",
                "PARAMS_REJECTED",
            )
        )

    safe_params = params_result.get("params")

    # 2. Reuse the existing protected controlled-fetch boundary.
    fetch_result = execute_controlled_fetch(
        env=env,
        session_factory=session_factory,
        url=url,
        timeout=timeout,
        params=safe_params,
        max_bytes=max_bytes,
    )

    if fetch_result.get("allowed") is not True:
        return _deny(
            fetch_result.get(
                "reason",
                "FETCH_REJECTED",
            )
        )

    evidence = fetch_result.get("evidence")

    # 3. Reuse the existing read-only baseline observer.
    observation_result = observe_finmind_baseline_evidence(
        evidence=evidence,
        stock_id=stock_id,
        trading_date=trading_date,
    )

    if observation_result.get("allowed") is not True:
        return _deny(
            observation_result.get(
                "reason",
                "OBSERVATION_REJECTED",
            )
        )

    # 4. Public result exposes the sanitized observation only.
    return {
        "allowed": True,
        "observed": observation_result.get("observed"),
    }