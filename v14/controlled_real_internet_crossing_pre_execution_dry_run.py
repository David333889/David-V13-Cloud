"""
Gate 28D.2K-2S
Controlled Real Internet Crossing Pre-Execution Dry-Run Contract V1.

Evidence-only dry run.
No environment read, secret-value read, Session creation,
HTTP request, or Internet crossing.
"""

from v14 import controlled_runtime_entry_integration as runtime_entry
from v14 import controlled_real_execution_authorization_integration as execution_auth
from v14 import controlled_real_internet_crossing_execution as execution_contract
from v14 import internet_crossing_preflight as preflight
from v14 import real_session_factory as session_factory
from v14 import read_only_transport as transport
from v14 import secret_runtime


READ_ONLY = True
DRY_RUN_ONLY = True

NO_ENVIRONMENT_READ = True
NO_SECRET_VALUE_READ = True
NO_SESSION_CREATION = True
NO_NETWORK_EXECUTION = True

ONE_SHOT_ONLY = execution_auth.ONE_SHOT_ONLY
SINGLE_STOCK_ONLY = execution_auth.SINGLE_STOCK_ONLY
SINGLE_TRADING_DATE_ONLY = execution_auth.SINGLE_TRADING_DATE_ONLY
MAX_REAL_GETS = execution_auth.MAX_REAL_GETS

GET_ONLY = transport.GET_ONLY
ALLOW_REDIRECTS = transport.ALLOW_REDIRECTS
MAX_RETRIES = session_factory.MAX_RETRIES
DEFAULT_TIMEOUT_SECONDS = runtime_entry.DEFAULT_TIMEOUT_SECONDS

SECRET_METADATA_ONLY = True
ALLOW_SECRET_IN_EVIDENCE = secret_runtime.ALLOW_SECRET_IN_EVIDENCE
ALLOW_SECRET_IN_ERROR = secret_runtime.ALLOW_SECRET_IN_ERROR

EXECUTION_REAL_GET_AUTHORIZED = execution_contract.ALLOW_REAL_GET is True
PREFLIGHT_READY = True
PREFLIGHT_NETWORK_EXECUTED = False
PREFLIGHT_LIVE_GET_DISABLED = preflight.ALLOW_LIVE_GET is False

ALLOW_CORE_INPUT = execution_auth.ALLOW_CORE_INPUT
ALLOW_SCORE = execution_auth.ALLOW_SCORE
ALLOW_DECISION = execution_auth.ALLOW_DECISION
ALLOW_SUPABASE_WRITE = execution_auth.ALLOW_SUPABASE_WRITE
ALLOW_PRODUCTION_WRITE = execution_auth.ALLOW_PRODUCTION_WRITE


def build_pre_execution_dry_run_evidence():
    preflight_result = preflight.run_preflight()
    execution = (
        execution_contract
        .get_controlled_real_internet_crossing_execution_contract()
    )

    checks = {
        "read_only": READ_ONLY is True,
        "dry_run_only": DRY_RUN_ONLY is True,
        "no_environment_read": NO_ENVIRONMENT_READ is True,
        "no_secret_value_read": NO_SECRET_VALUE_READ is True,
        "no_session_creation": NO_SESSION_CREATION is True,
        "no_network_execution": NO_NETWORK_EXECUTION is True,
        "one_shot_only": ONE_SHOT_ONLY is True,
        "single_stock_only": SINGLE_STOCK_ONLY is True,
        "single_trading_date_only": SINGLE_TRADING_DATE_ONLY is True,
        "max_real_gets": MAX_REAL_GETS == 1,
        "get_only": GET_ONLY is True,
        "redirects_disabled": ALLOW_REDIRECTS is False,
        "retries_disabled": MAX_RETRIES == 0,
        "timeout_bounded": DEFAULT_TIMEOUT_SECONDS == 10,
        "secret_metadata_only": SECRET_METADATA_ONLY is True,
        "secret_evidence_disabled": ALLOW_SECRET_IN_EVIDENCE is False,
        "secret_error_disabled": ALLOW_SECRET_IN_ERROR is False,
        "execution_real_get_authorized": (
            execution.get("allow_real_get") is True
        ),
        "execution_real_get_limit": (
            execution.get("max_real_gets") == 1
        ),
        "preflight_ready": (
            preflight_result.get("ready") is True
        ),
        "preflight_no_network": (
            preflight_result.get("network_executed") is False
        ),
        "preflight_live_get_disabled": (
            preflight_result.get("allow_live_get") is False
        ),
        "core_input_disabled": ALLOW_CORE_INPUT is False,
        "score_disabled": ALLOW_SCORE is False,
        "decision_disabled": ALLOW_DECISION is False,
        "supabase_write_disabled": ALLOW_SUPABASE_WRITE is False,
        "production_write_disabled": ALLOW_PRODUCTION_WRITE is False,
    }

    return {
        "ready_for_pre_execution": all(checks.values()),
        "environment_read": False,
        "secret_value_read": False,
        "session_created": False,
        "network_executed": False,
        "real_gets_executed": 0,
        "checks": checks,
    }
