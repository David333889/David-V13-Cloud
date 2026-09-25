from v14.finmind_live_backend import BASE_URL
from v14.one_shot_live_fetch import (
    execute_one_shot_live_fetch,
)


# Gate 28D.2A - Real live entry boundary contract.
#
# This module defines the single controlled entry into the
# one-shot live-fetch path.
#
# Runtime environment and session factory must be injected.
# This module does not read os.environ, create a Session,
# persist a token, or implement an HTTP request itself.

DATASET = "TaiwanStockPrice"
DEFAULT_TIMEOUT_SECONDS = 10

ALLOW_CORE_INPUT = False
ALLOW_SCORE = False
ALLOW_DECISION = False
ALLOW_SUPABASE_WRITE = False
ALLOW_PRODUCTION_WRITE = False

ALLOW_DIRECT_ENV_READ = False
ALLOW_TOKEN_PERSISTENCE = False
ALLOW_SESSION_CREATION = False


def execute_real_live_entry(
    env,
    session_factory,
    data_id,
    trading_date,
):
    """
    Execute the single protected live-entry path.

    Dependencies are injected by the caller.
    Public output is delegated to the protected one-shot
    integration and contains golden metadata only.
    """

    params = {
        "dataset": DATASET,
        "data_id": data_id,
        "start_date": trading_date,
        "end_date": trading_date,
    }

    return execute_one_shot_live_fetch(
        env=env,
        session_factory=session_factory,
        url=BASE_URL,
        timeout=DEFAULT_TIMEOUT_SECONDS,
        params=params,
    )
