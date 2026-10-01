"""
Gate 28D.2K-3A
First Controlled Real GET Execution Plan V1.

Planning / final go-no-go contract only.

Fixes the first controlled real sample target and safety
conditions before any real network execution is permitted.

This module performs no environment read, secret read,
Session creation, HTTP request, or Internet crossing.
"""

from v14.read_only_transport import (
    GET_ONLY,
    ALLOW_REDIRECTS,
)
from v14.real_session_factory import MAX_RETRIES
from v14.controlled_runtime_entry_integration import (
    DATASET,
    DEFAULT_TIMEOUT_SECONDS,
)
from v14 import controlled_real_execution_authorization_integration as execution_auth


READ_ONLY = True
EXECUTION_PLAN_ONLY = True
GO_NO_GO_CONTRACT_ONLY = True

PROVIDER = "FINMIND"
STOCK_ID = "2330"
TRADING_DATE = "2026-09-30"

MAX_REAL_GETS = 1

REQUIRE_TOKEN_AVAILABLE = True
ALLOW_SECRET_VALUE_EXPOSURE = False

ALLOW_NETWORK_EXECUTION = False
ALLOW_REAL_GET_EXECUTION = False

ALLOW_CORE_INPUT = execution_auth.ALLOW_CORE_INPUT
ALLOW_SCORE = execution_auth.ALLOW_SCORE
ALLOW_DECISION = execution_auth.ALLOW_DECISION
ALLOW_SUPABASE_WRITE = execution_auth.ALLOW_SUPABASE_WRITE
ALLOW_PRODUCTION_WRITE = execution_auth.ALLOW_PRODUCTION_WRITE


def build_first_real_get_execution_plan_evidence():
    checks = {
        "read_only": READ_ONLY is True,
        "execution_plan_only": EXECUTION_PLAN_ONLY is True,
        "go_no_go_contract_only": (
            GO_NO_GO_CONTRACT_ONLY is True
        ),

        "provider_fixed": PROVIDER == "FINMIND",
        "dataset_fixed": DATASET == "TaiwanStockPrice",
        "stock_fixed": STOCK_ID == "2330",
        "trading_date_fixed": (
            TRADING_DATE == "2026-09-30"
        ),

        "get_only": GET_ONLY is True,
        "max_real_gets": MAX_REAL_GETS == 1,
        "timeout_fixed": DEFAULT_TIMEOUT_SECONDS == 10,
        "retries_disabled": MAX_RETRIES == 0,
        "redirects_disabled": ALLOW_REDIRECTS is False,

        "token_available_required": (
            REQUIRE_TOKEN_AVAILABLE is True
        ),
        "secret_exposure_disabled": (
            ALLOW_SECRET_VALUE_EXPOSURE is False
        ),

        "network_execution_disabled": (
            ALLOW_NETWORK_EXECUTION is False
        ),
        "real_get_execution_disabled": (
            ALLOW_REAL_GET_EXECUTION is False
        ),

        "core_input_disabled": ALLOW_CORE_INPUT is False,
        "score_disabled": ALLOW_SCORE is False,
        "decision_disabled": ALLOW_DECISION is False,
        "supabase_write_disabled": (
            ALLOW_SUPABASE_WRITE is False
        ),
        "production_write_disabled": (
            ALLOW_PRODUCTION_WRITE is False
        ),
    }

    return {
        "go_no_go_contract_ready": all(checks.values()),
        "network_executed": False,
        "real_gets_executed": 0,
        "secret_value_exposed": False,
        "checks": checks,
    }
