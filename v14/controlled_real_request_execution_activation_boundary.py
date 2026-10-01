"""
Gate 28D.2K-2Y
Controlled Real Request Execution Activation Boundary V1.

Boundary/evidence only.

Defines the final safety conditions required before a future
controlled one-shot real GET may be activated.

This module performs no environment read, secret read,
Session creation, HTTP request, or Internet crossing.
"""

from v14.finmind_live_backend import BASE_URL as FINMIND_BASE_URL
from v14.internet_crossing_preflight import FINMIND_HOST
from v14.real_session_factory import MAX_RETRIES
from v14.read_only_transport import (
    GET_ONLY,
    ALLOW_REDIRECTS,
)
from v14.controlled_runtime_entry_integration import (
    DEFAULT_TIMEOUT_SECONDS,
)
from v14 import controlled_real_execution_authorization_integration as execution_auth


READ_ONLY = True
REQUEST_EXECUTION_ACTIVATION_BOUNDARY_ONLY = True

SINGLE_STOCK_ONLY = True
SINGLE_TRADING_DATE_ONLY = True
MAX_REAL_GETS = 1

REQUIRE_TOKEN_AVAILABLE = True
ALLOW_SECRET_VALUE_EXPOSURE = False

ALLOW_NETWORK_EXECUTION = False

ALLOW_CORE_INPUT = execution_auth.ALLOW_CORE_INPUT
ALLOW_SCORE = execution_auth.ALLOW_SCORE
ALLOW_DECISION = execution_auth.ALLOW_DECISION
ALLOW_SUPABASE_WRITE = execution_auth.ALLOW_SUPABASE_WRITE
ALLOW_PRODUCTION_WRITE = execution_auth.ALLOW_PRODUCTION_WRITE


def build_request_execution_activation_evidence():
    checks = {
        "read_only": READ_ONLY is True,
        "activation_boundary_only": (
            REQUEST_EXECUTION_ACTIVATION_BOUNDARY_ONLY is True
        ),
        "get_only": GET_ONLY is True,
        "single_stock_only": SINGLE_STOCK_ONLY is True,
        "single_trading_date_only": (
            SINGLE_TRADING_DATE_ONLY is True
        ),
        "max_real_gets": MAX_REAL_GETS == 1,
        "timeout_bounded": DEFAULT_TIMEOUT_SECONDS == 10,
        "retries_disabled": MAX_RETRIES == 0,
        "redirects_disabled": ALLOW_REDIRECTS is False,
        "finmind_host_fixed": (
            FINMIND_HOST == "api.finmindtrade.com"
        ),
        "finmind_base_url_fixed": (
            FINMIND_BASE_URL
            == "https://api.finmindtrade.com/api/v4/data"
        ),
        "token_available_required": (
            REQUIRE_TOKEN_AVAILABLE is True
        ),
        "secret_exposure_disabled": (
            ALLOW_SECRET_VALUE_EXPOSURE is False
        ),
        "network_execution_disabled": (
            ALLOW_NETWORK_EXECUTION is False
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
        "activation_boundary_ready": all(checks.values()),
        "network_executed": False,
        "real_gets_executed": 0,
        "session_created": False,
        "secret_value_exposed": False,
        "checks": checks,
    }
