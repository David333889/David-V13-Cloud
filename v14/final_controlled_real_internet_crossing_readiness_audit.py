"""
Gate 28D.2K-2Q
Final Controlled Real Internet Crossing Readiness Audit V1.

Audit only:
- no environment read
- no session creation
- no HTTP request
- no Internet crossing
- no write path
"""

from v14 import controlled_runtime_entry_integration as runtime_entry
from v14 import controlled_runtime_environment_integration as runtime_env
from v14 import controlled_real_execution_authorization_integration as execution_auth
from v14 import real_session_factory as session_factory
from v14 import read_only_transport as transport


READ_ONLY = runtime_entry.READ_ONLY
AUDIT_ONLY = True
NO_NETWORK_EXECUTION = True

ONE_SHOT_ONLY = runtime_entry.ONE_SHOT_ONLY
SINGLE_STOCK_ONLY = runtime_entry.SINGLE_STOCK_ONLY
SINGLE_TRADING_DATE_ONLY = runtime_entry.SINGLE_TRADING_DATE_ONLY
MAX_REAL_GETS = execution_auth.MAX_REAL_GETS

GET_ONLY = transport.GET_ONLY
ALLOW_REDIRECTS = transport.ALLOW_REDIRECTS
MAX_RETRIES = session_factory.MAX_RETRIES
DEFAULT_TIMEOUT_SECONDS = runtime_entry.DEFAULT_TIMEOUT_SECONDS

ALLOW_DIRECT_ENV_READ = runtime_env.ALLOW_DIRECT_ENV_READ
ALLOW_SECRET_IN_PUBLIC_RESULT = runtime_env.ALLOW_SECRET_IN_PUBLIC_RESULT

ALLOW_NORMALIZATION = runtime_entry.ALLOW_NORMALIZATION
ALLOW_COMPATIBILITY_ESTABLISHMENT = runtime_entry.ALLOW_COMPATIBILITY_ESTABLISHMENT
ALLOW_PROVIDER_SWITCH = runtime_entry.ALLOW_PROVIDER_SWITCH
ALLOW_CORE_INPUT = runtime_entry.ALLOW_CORE_INPUT
ALLOW_SCORE = runtime_entry.ALLOW_SCORE
ALLOW_DECISION = runtime_entry.ALLOW_DECISION
ALLOW_SUPABASE_WRITE = runtime_entry.ALLOW_SUPABASE_WRITE
ALLOW_PRODUCTION_WRITE = runtime_entry.ALLOW_PRODUCTION_WRITE


def build_readiness_evidence():
    checks = {
        "read_only": READ_ONLY is True,
        "audit_only": AUDIT_ONLY is True,
        "no_network_execution": NO_NETWORK_EXECUTION is True,
        "one_shot_only": ONE_SHOT_ONLY is True,
        "single_stock_only": SINGLE_STOCK_ONLY is True,
        "single_trading_date_only": SINGLE_TRADING_DATE_ONLY is True,
        "max_real_gets": MAX_REAL_GETS == 1,
        "get_only": GET_ONLY is True,
        "redirects_disabled": ALLOW_REDIRECTS is False,
        "retries_disabled": MAX_RETRIES == 0,
        "timeout_bounded": DEFAULT_TIMEOUT_SECONDS == 10,
        "direct_env_read_disabled": ALLOW_DIRECT_ENV_READ is False,
        "secret_public_result_disabled": ALLOW_SECRET_IN_PUBLIC_RESULT is False,
        "normalization_disabled": ALLOW_NORMALIZATION is False,
        "compatibility_disabled": ALLOW_COMPATIBILITY_ESTABLISHMENT is False,
        "provider_switch_disabled": ALLOW_PROVIDER_SWITCH is False,
        "core_input_disabled": ALLOW_CORE_INPUT is False,
        "score_disabled": ALLOW_SCORE is False,
        "decision_disabled": ALLOW_DECISION is False,
        "supabase_write_disabled": ALLOW_SUPABASE_WRITE is False,
        "production_write_disabled": ALLOW_PRODUCTION_WRITE is False,
    }

    return {
        "ready_for_controlled_real_crossing": all(checks.values()),
        "network_executed": False,
        "real_gets_executed": 0,
        "secret_exposed": False,
        "checks": checks,
    }
