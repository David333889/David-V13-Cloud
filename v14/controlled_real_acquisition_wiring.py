# Gate 28D.2K-2I - Controlled Real Acquisition Wiring V1.
#
# Thin composition layer only.
#
# Composes:
#   2F one-shot guard
#   2G one-shot integration
#   2H acquisition adapter
#
# Building the wiring performs no acquisition.
# This module does not create a Session, read a token,
# implement HTTP, normalize data, establish compatibility,
# enter Core, score, decide, or write persistence.

from v14.controlled_real_acquisition_adapter import (
    build_controlled_real_acquisition_executor,
)
from v14.controlled_real_internet_crossing_one_shot import (
    ControlledRealInternetCrossingOneShot,
)
from v14.controlled_real_internet_crossing_one_shot_integration import (
    execute_controlled_real_internet_crossing_once,
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


def build_controlled_real_acquisition_wiring(
    acquisition,
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
    Build a zero-argument one-shot controlled acquisition callable.

    Building this wiring performs no acquisition.
    """

    executor = build_controlled_real_acquisition_executor(
        acquisition=acquisition,
        env=env,
        session_factory=session_factory,
        url=url,
        timeout=timeout,
        params=params,
        stock_id=stock_id,
        trading_date=trading_date,
        max_bytes=max_bytes,
    )

    guard = ControlledRealInternetCrossingOneShot()

    def execute_once():
        return execute_controlled_real_internet_crossing_once(
            guard=guard,
            executor=executor,
        )

    return execute_once
