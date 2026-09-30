# Gate 28D.2K-2J - Controlled Real Fetch Composition V1.
#
# Thin composition / signature bridge only.
#
# Composes:
#   existing execute_controlled_fetch acquisition path
#   protected 2I one-shot acquisition wiring
#
# The acquisition bridge accepts the protected 2H acquisition
# signature, but stock_id and trading_date remain boundary
# identity inputs and are not forwarded to the legacy
# execute_controlled_fetch API.
#
# Building the composition performs no session creation,
# GET, or Internet crossing.
#
# This module does not create a requests Session directly,
# read os.environ directly, normalize data, establish
# compatibility, enter Core, score, decide, or persist data.

from v14.controlled_live_fetch import (
    execute_controlled_fetch,
)
from v14.controlled_real_acquisition_wiring import (
    build_controlled_real_acquisition_wiring,
)


READ_ONLY = True
ONE_SHOT_ONLY = True
MAX_REAL_GETS = 1

ALLOW_NORMALIZATION = False
ALLOW_COMPATIBILITY_ESTABLISHMENT = False
ALLOW_PROVIDER_SWITCH = False
ALLOW_CORE_INPUT = False
ALLOW_SCORE = False
ALLOW_DECISION = False
ALLOW_SUPABASE_WRITE = False
ALLOW_PRODUCTION_WRITE = False


def _execute_controlled_fetch_bridge(
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
    Adapt the protected acquisition signature to the existing
    controlled-fetch signature.

    stock_id and trading_date are intentionally accepted here
    as protected boundary identity inputs but are not forwarded
    as unsupported keyword arguments.
    """

    if not isinstance(stock_id, str) or not stock_id.strip():
        return {
            "allowed": False,
            "reason": "STOCK_ID_REQUIRED",
        }

    if not isinstance(trading_date, str) or not trading_date.strip():
        return {
            "allowed": False,
            "reason": "TRADING_DATE_REQUIRED",
        }

    if not isinstance(params, dict):
        return {
            "allowed": False,
            "reason": "PARAMS_REQUIRED",
        }

    data_id = params.get("data_id")

    if data_id != stock_id:
        return {
            "allowed": False,
            "reason": "STOCK_ID_MISMATCH",
        }

    start_date = params.get("start_date")
    end_date = params.get("end_date")

    if (
        start_date != trading_date
        or end_date != trading_date
    ):
        return {
            "allowed": False,
            "reason": "TRADING_DATE_MISMATCH",
        }

    return execute_controlled_fetch(
        env=env,
        session_factory=session_factory,
        url=url,
        timeout=timeout,
        params=params,
        max_bytes=max_bytes,
    )


def build_controlled_real_fetch_composition(
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
    Build a protected one-shot controlled-fetch callable.

    Building this composition performs no session creation,
    GET, or Internet crossing.
    """

    return build_controlled_real_acquisition_wiring(
        acquisition=_execute_controlled_fetch_bridge,
        env=env,
        session_factory=session_factory,
        url=url,
        timeout=timeout,
        params=params,
        stock_id=stock_id,
        trading_date=trading_date,
        max_bytes=max_bytes,
    )
