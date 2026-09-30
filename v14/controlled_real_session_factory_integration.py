# Gate 28D.2K-2N - Controlled Real Session Factory
# Integration V1.
#
# Thin session-factory integration only.
#
# Order:
#   1. Build the existing protected session factory from
#      injected requests dependencies.
#   2. Building performs no Session creation or GET.
#   3. Inject that factory only into the protected 2M chain.
#
# This module does not create a Session directly,
# execute HTTP directly, read os.environ directly,
# normalize data, establish compatibility, enter Core,
# score, decide, or persist data.

from v14.real_session_factory import (
    build_session_factory,
)
from v14.controlled_real_execution_authorization_integration import (
    build_authorized_controlled_real_fetch,
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


def build_session_factory_controlled_real_fetch(
    requests_module,
    adapter_class,
    env,
    url,
    timeout,
    params,
    stock_id,
    trading_date,
    max_bytes=5_000_000,
):
    """
    Build the existing session factory from injected
    dependencies and pass it only into the protected
    2M controlled-real execution chain.

    Building this integration performs no Session
    creation or GET.
    """

    session_factory = build_session_factory(
        requests_module=requests_module,
        adapter_class=adapter_class,
    )

    return build_authorized_controlled_real_fetch(
        env=env,
        session_factory=session_factory,
        url=url,
        timeout=timeout,
        params=params,
        stock_id=stock_id,
        trading_date=trading_date,
        max_bytes=max_bytes,
    )
