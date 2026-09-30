# Gate 28D.2K-2K - Controlled Real Request
# Validation Integration V1.
#
# Thin validation integration only.
#
# Order:
#   1. Validate FinMind request parameters.
#   2. Deny invalid parameters before Session / GET.
#   3. Pass validated parameters only into the already
#      protected 2J controlled-real fetch composition.
#
# Building this integration performs no Session creation,
# GET, or Internet crossing.
#
# This module does not read os.environ directly, create a
# requests Session directly, normalize data, establish
# compatibility, enter Core, score, decide, or persist data.

from v14.finmind_live_request_parameters import (
    validate_finmind_live_params,
)
from v14.controlled_real_fetch_composition import (
    build_controlled_real_fetch_composition,
)


READ_ONLY = True
ONE_SHOT_ONLY = True
SINGLE_STOCK_ONLY = True
SINGLE_TRADING_DATE_ONLY = True
MAX_REAL_GETS = 1

ALLOW_NORMALIZATION = False
ALLOW_COMPATIBILITY_ESTABLISHMENT = False
ALLOW_PROVIDER_SWITCH = False
ALLOW_CORE_INPUT = False
ALLOW_SCORE = False
ALLOW_DECISION = False
ALLOW_SUPABASE_WRITE = False
ALLOW_PRODUCTION_WRITE = False


def _deny_executor(reason):
    """
    Return a zero-argument fail-closed callable.

    Building or calling this denied executor performs
    no Session creation or GET.
    """

    def denied():
        return {
            "allowed": False,
            "reason": reason,
        }

    return denied


def build_validated_controlled_real_fetch(
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
    Validate request parameters before building the protected
    2J controlled-real fetch composition.
    """

    validation = validate_finmind_live_params(
        params,
    )

    if validation.get("allowed") is not True:
        return _deny_executor(
            validation.get(
                "reason",
                "PARAMS_REJECTED",
            )
        )

    safe_params = validation.get("params")

    return build_controlled_real_fetch_composition(
        env=env,
        session_factory=session_factory,
        url=url,
        timeout=timeout,
        params=safe_params,
        stock_id=stock_id,
        trading_date=trading_date,
        max_bytes=max_bytes,
    )
