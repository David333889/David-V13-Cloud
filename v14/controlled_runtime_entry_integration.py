# Gate 28D.2K-2P - Controlled Runtime Entry
# Integration V1.
#
# Thin runtime-entry integration only.
#
# Order:
#   1. Accept one stock and one trading date.
#   2. Build the fixed FinMind single-day request.
#   3. Delegate only into the protected 2O chain.
#
# This module does not read os.environ directly,
# create a Session directly, execute HTTP directly,
# normalize data, establish compatibility, enter Core,
# score, decide, or persist data.

from v14.finmind_live_backend import (
    BASE_URL,
)
from v14.controlled_runtime_environment_integration import (
    build_runtime_environment_controlled_real_fetch,
)


DATASET = "TaiwanStockPrice"
DEFAULT_TIMEOUT_SECONDS = 10

READ_ONLY = True
ONE_SHOT_ONLY = True
SINGLE_STOCK_ONLY = True
SINGLE_TRADING_DATE_ONLY = True
MAX_REAL_GETS = 1

ALLOW_DIRECT_ENV_READ = False
ALLOW_NORMALIZATION = False
ALLOW_COMPATIBILITY_ESTABLISHMENT = False
ALLOW_PROVIDER_SWITCH = False
ALLOW_CORE_INPUT = False
ALLOW_SCORE = False
ALLOW_DECISION = False
ALLOW_SUPABASE_WRITE = False
ALLOW_PRODUCTION_WRITE = False


def build_controlled_runtime_entry(
    environment_reader,
    requests_module,
    adapter_class,
    stock_id,
    trading_date,
):
    """
    Build the single controlled runtime-entry callable.

    Runtime environment access and requests dependencies
    remain injected.

    Building performs no Session creation or GET.
    """

    params = {
        "dataset": DATASET,
        "data_id": stock_id,
        "start_date": trading_date,
        "end_date": trading_date,
    }

    return build_runtime_environment_controlled_real_fetch(
        environment_reader=environment_reader,
        requests_module=requests_module,
        adapter_class=adapter_class,
        url=BASE_URL,
        timeout=DEFAULT_TIMEOUT_SECONDS,
        params=params,
        stock_id=stock_id,
        trading_date=trading_date,
    )
