# Gate 28D.2K-2L - Controlled Real Preflight
# Integration V1.
#
# Thin preflight integration only.
#
# Order:
#   1. Execute injected preflight readiness check.
#   2. Fail closed before Session / GET when not ready.
#   3. Require preflight itself to have executed no network.
#   4. Require live GET to remain disabled at preflight.
#   5. Delegate only into the already protected 2K chain.
#
# This module does not create a requests Session directly,
# read os.environ directly, execute HTTP, normalize data,
# establish compatibility, enter Core, score, decide,
# or persist data.

from v14.internet_crossing_preflight import (
    run_preflight,
)
from v14.controlled_real_request_validation_integration import (
    build_validated_controlled_real_fetch,
)


READ_ONLY = True
ONE_SHOT_ONLY = True
SINGLE_STOCK_ONLY = True
SINGLE_TRADING_DATE_ONLY = True
MAX_REAL_GETS = 1

ALLOW_LIVE_GET = False
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

    Calling it performs no Session creation or GET.
    """

    def denied():
        return {
            "allowed": False,
            "reason": reason,
        }

    return denied


def build_preflight_validated_controlled_real_fetch(
    env,
    session_factory,
    url,
    timeout,
    params,
    stock_id,
    trading_date,
    max_bytes=5_000_000,
    preflight=run_preflight,
):
    """
    Require safe preflight state before building the already
    protected 2K controlled-real fetch chain.
    """

    if not callable(preflight):
        return _deny_executor("PREFLIGHT_REQUIRED")

    try:
        result = preflight()
    except Exception:
        return _deny_executor("PREFLIGHT_FAILURE")

    if not isinstance(result, dict):
        return _deny_executor("PREFLIGHT_INVALID")

    if result.get("ready") is not True:
        return _deny_executor("PREFLIGHT_NOT_READY")

    if result.get("network_executed") is not False:
        return _deny_executor(
            "PREFLIGHT_NETWORK_EXECUTED"
        )

    if result.get("allow_live_get") is not False:
        return _deny_executor(
            "PREFLIGHT_LIVE_GET_NOT_DISABLED"
        )

    return build_validated_controlled_real_fetch(
        env=env,
        session_factory=session_factory,
        url=url,
        timeout=timeout,
        params=params,
        stock_id=stock_id,
        trading_date=trading_date,
        max_bytes=max_bytes,
    )
