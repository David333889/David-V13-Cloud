"""
Gate 28D.2K-2T
Controlled Runtime Dependency Activation Boundary V1.

Boundary/evidence only.
No direct OS environment read, secret-value exposure,
Session creation, HTTP request, or Internet crossing.
"""

from v14 import controlled_runtime_entry_integration as runtime_entry
from v14 import controlled_real_execution_authorization_integration as execution_auth


READ_ONLY = True
ACTIVATION_BOUNDARY_ONLY = True

ALLOW_DIRECT_OS_ENV_READ = False
ALLOW_SECRET_VALUE_EXPOSURE = False
ALLOW_SESSION_CREATION = False
ALLOW_NETWORK_EXECUTION = False

REQUIRE_ENVIRONMENT_READER = True
REQUIRE_REQUESTS_MODULE = True
REQUIRE_ADAPTER_CLASS = True

ONE_SHOT_ONLY = execution_auth.ONE_SHOT_ONLY
SINGLE_STOCK_ONLY = execution_auth.SINGLE_STOCK_ONLY
SINGLE_TRADING_DATE_ONLY = execution_auth.SINGLE_TRADING_DATE_ONLY
MAX_REAL_GETS = execution_auth.MAX_REAL_GETS

ALLOW_CORE_INPUT = execution_auth.ALLOW_CORE_INPUT
ALLOW_SCORE = execution_auth.ALLOW_SCORE
ALLOW_DECISION = execution_auth.ALLOW_DECISION
ALLOW_SUPABASE_WRITE = execution_auth.ALLOW_SUPABASE_WRITE
ALLOW_PRODUCTION_WRITE = execution_auth.ALLOW_PRODUCTION_WRITE


def build_runtime_dependency_activation_evidence():
    checks = {
        "read_only": READ_ONLY is True,
        "activation_boundary_only": (
            ACTIVATION_BOUNDARY_ONLY is True
        ),
        "direct_os_env_read_disabled": (
            ALLOW_DIRECT_OS_ENV_READ is False
        ),
        "secret_value_exposure_disabled": (
            ALLOW_SECRET_VALUE_EXPOSURE is False
        ),
        "session_creation_disabled": (
            ALLOW_SESSION_CREATION is False
        ),
        "network_execution_disabled": (
            ALLOW_NETWORK_EXECUTION is False
        ),
        "environment_reader_required": (
            REQUIRE_ENVIRONMENT_READER is True
        ),
        "requests_module_required": (
            REQUIRE_REQUESTS_MODULE is True
        ),
        "adapter_class_required": (
            REQUIRE_ADAPTER_CLASS is True
        ),
        "one_shot_only": ONE_SHOT_ONLY is True,
        "single_stock_only": SINGLE_STOCK_ONLY is True,
        "single_trading_date_only": (
            SINGLE_TRADING_DATE_ONLY is True
        ),
        "max_real_gets": MAX_REAL_GETS == 1,
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
        "os_environment_read": False,
        "secret_value_exposed": False,
        "session_created": False,
        "network_executed": False,
        "real_gets_executed": 0,
        "target_entry": (
            "controlled_runtime_entry_integration"
        ),
        "checks": checks,
    }
