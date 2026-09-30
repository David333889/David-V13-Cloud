# Gate 28D.2K-2O - Controlled Runtime Environment
# Integration V1.
#
# Thin runtime-environment integration only.
#
# Order:
#   1. Read an injected environment mapping.
#   2. Copy only the required FinMind runtime token.
#   3. Do not propagate unrelated environment values.
#   4. Delegate only into the protected 2N chain.
#
# This module does not read os.environ directly,
# create a Session directly, execute HTTP directly,
# normalize data, establish compatibility, enter Core,
# score, decide, or persist data.

from v14.secret_runtime import (
    DEFAULT_TOKEN_ENV_NAME,
)
from v14.controlled_real_session_factory_integration import (
    build_session_factory_controlled_real_fetch,
)


READ_ONLY = True
ONE_SHOT_ONLY = True
SINGLE_STOCK_ONLY = True
SINGLE_TRADING_DATE_ONLY = True
MAX_REAL_GETS = 1

ALLOW_DIRECT_ENV_READ = False
ALLOW_UNRELATED_ENV_PROPAGATION = False
ALLOW_SECRET_IN_PUBLIC_RESULT = False

ALLOW_NORMALIZATION = False
ALLOW_COMPATIBILITY_ESTABLISHMENT = False
ALLOW_PROVIDER_SWITCH = False
ALLOW_CORE_INPUT = False
ALLOW_SCORE = False
ALLOW_DECISION = False
ALLOW_SUPABASE_WRITE = False
ALLOW_PRODUCTION_WRITE = False


def build_runtime_environment_controlled_real_fetch(
    environment_reader,
    requests_module,
    adapter_class,
    url,
    timeout,
    params,
    stock_id,
    trading_date,
    max_bytes=5_000_000,
):
    """
    Read runtime environment through an injected callable,
    retain only the required FinMind token entry, and pass
    that minimal mapping into the protected 2N chain.

    Building performs no Session creation or GET.
    """

    if not callable(environment_reader):
        raise ValueError(
            "environment reader is required"
        )

    environment = environment_reader()

    if not isinstance(environment, dict):
        raise ValueError(
            "environment mapping is required"
        )

    env = {}

    if DEFAULT_TOKEN_ENV_NAME in environment:
        env[DEFAULT_TOKEN_ENV_NAME] = (
            environment[DEFAULT_TOKEN_ENV_NAME]
        )

    return build_session_factory_controlled_real_fetch(
        requests_module=requests_module,
        adapter_class=adapter_class,
        env=env,
        url=url,
        timeout=timeout,
        params=params,
        stock_id=stock_id,
        trading_date=trading_date,
        max_bytes=max_bytes,
    )
