"""
Gate 28D.2K-2R
Controlled Real Internet Crossing Unique Execution Path Contract V1.

Contract/evidence only.
No environment read, Session creation, HTTP request, or Internet crossing.
"""

from v14 import controlled_runtime_entry_integration as runtime_entry
from v14 import controlled_runtime_environment_integration as runtime_env
from v14 import controlled_real_session_factory_integration as session_integration
from v14 import controlled_real_execution_authorization_integration as execution_auth
from v14 import controlled_real_preflight_integration as preflight
from v14 import controlled_real_request_validation_integration as request_validation
from v14 import controlled_real_internet_crossing_execution as execution_contract


READ_ONLY = True
CONTRACT_ONLY = True
NO_NETWORK_EXECUTION = True

ONE_SHOT_ONLY = execution_auth.ONE_SHOT_ONLY
SINGLE_STOCK_ONLY = execution_auth.SINGLE_STOCK_ONLY
SINGLE_TRADING_DATE_ONLY = execution_auth.SINGLE_TRADING_DATE_ONLY
MAX_REAL_GETS = execution_auth.MAX_REAL_GETS

PREFLIGHT_LIVE_GET_DISABLED = preflight.ALLOW_LIVE_GET is False
EXECUTION_REAL_GET_AUTHORIZED = execution_contract.ALLOW_REAL_GET is True

ALLOW_DIRECT_HTTP_BYPASS = False
ALLOW_DIRECT_SESSION_BYPASS = False
ALLOW_AUTHORIZATION_BYPASS = False
ALLOW_PREFLIGHT_BYPASS = False
ALLOW_REQUEST_VALIDATION_BYPASS = False

ALLOW_CORE_INPUT = execution_auth.ALLOW_CORE_INPUT
ALLOW_SCORE = execution_auth.ALLOW_SCORE
ALLOW_DECISION = execution_auth.ALLOW_DECISION
ALLOW_SUPABASE_WRITE = execution_auth.ALLOW_SUPABASE_WRITE
ALLOW_PRODUCTION_WRITE = execution_auth.ALLOW_PRODUCTION_WRITE


def build_unique_execution_path_evidence():
    checks = {
        "runtime_entry_read_only": runtime_entry.READ_ONLY is True,
        "runtime_environment_read_only": runtime_env.READ_ONLY is True,
        "session_factory_read_only": session_integration.READ_ONLY is True,
        "execution_authorization_read_only": execution_auth.READ_ONLY is True,
        "preflight_read_only": preflight.READ_ONLY is True,
        "request_validation_read_only": request_validation.READ_ONLY is True,
        "one_shot_only": ONE_SHOT_ONLY is True,
        "single_stock_only": SINGLE_STOCK_ONLY is True,
        "single_trading_date_only": SINGLE_TRADING_DATE_ONLY is True,
        "max_real_gets": MAX_REAL_GETS == 1,
        "preflight_live_get_disabled": PREFLIGHT_LIVE_GET_DISABLED is True,
        "execution_real_get_authorized": EXECUTION_REAL_GET_AUTHORIZED is True,
        "direct_http_bypass_disabled": ALLOW_DIRECT_HTTP_BYPASS is False,
        "direct_session_bypass_disabled": ALLOW_DIRECT_SESSION_BYPASS is False,
        "authorization_bypass_disabled": ALLOW_AUTHORIZATION_BYPASS is False,
        "preflight_bypass_disabled": ALLOW_PREFLIGHT_BYPASS is False,
        "request_validation_bypass_disabled": ALLOW_REQUEST_VALIDATION_BYPASS is False,
        "core_input_disabled": ALLOW_CORE_INPUT is False,
        "score_disabled": ALLOW_SCORE is False,
        "decision_disabled": ALLOW_DECISION is False,
        "supabase_write_disabled": ALLOW_SUPABASE_WRITE is False,
        "production_write_disabled": ALLOW_PRODUCTION_WRITE is False,
    }

    return {
        "unique_execution_path_ready": all(checks.values()),
        "network_executed": False,
        "real_gets_executed": 0,
        "path": (
            "runtime_entry",
            "runtime_environment",
            "session_factory_integration",
            "execution_authorization",
            "preflight",
            "request_validation",
            "protected_fetch",
        ),
        "checks": checks,
    }
