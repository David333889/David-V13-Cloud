# Gate 28D.2K-2M - Controlled Real Execution
# Authorization Integration V1.
#
# Thin execution-authorization integration only.
#
# Order:
#   1. Read the injected 2E execution authorization contract.
#   2. Require exactly one authorized future real GET.
#   3. Fail closed before Session / GET when unauthorized.
#   4. Delegate only into the already protected 2L chain.
#
# This module does not create a requests Session directly,
# read os.environ directly, execute HTTP, normalize data,
# establish compatibility, enter Core, score, decide,
# or persist data.

from v14.controlled_real_internet_crossing_execution import (
    get_controlled_real_internet_crossing_execution_contract,
)
from v14.controlled_real_preflight_integration import (
    build_preflight_validated_controlled_real_fetch,
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

    Calling it performs no Session creation or GET.
    """

    def denied():
        return {
            "allowed": False,
            "reason": reason,
        }

    return denied


def build_authorized_controlled_real_fetch(
    env,
    session_factory,
    url,
    timeout,
    params,
    stock_id,
    trading_date,
    max_bytes=5_000_000,
    authorization=(
        get_controlled_real_internet_crossing_execution_contract
    ),
):
    """
    Require the protected 2E execution authorization contract
    before entering the already protected 2L chain.
    """

    if not callable(authorization):
        return _deny_executor(
            "EXECUTION_AUTHORIZATION_REQUIRED"
        )

    try:
        contract = authorization()
    except Exception:
        return _deny_executor(
            "EXECUTION_AUTHORIZATION_FAILURE"
        )

    if not isinstance(contract, dict):
        return _deny_executor(
            "EXECUTION_AUTHORIZATION_INVALID"
        )

    if contract.get("allow_real_get") is not True:
        return _deny_executor(
            "REAL_GET_NOT_AUTHORIZED"
        )

    if contract.get("max_real_gets") != MAX_REAL_GETS:
        return _deny_executor(
            "REAL_GET_LIMIT_INVALID"
        )

    return build_preflight_validated_controlled_real_fetch(
        env=env,
        session_factory=session_factory,
        url=url,
        timeout=timeout,
        params=params,
        stock_id=stock_id,
        trading_date=trading_date,
        max_bytes=max_bytes,
    )
