"""
Gate 28D.2K-2W
Runtime Token Configuration Activation V1.

Activation contract/evidence only.
The real token is supplied through the process environment
outside this module.

No secret value read, exposure, logging, or persistence.
No Session creation, HTTP request, or Internet crossing.
"""

from v14.secret_runtime import DEFAULT_TOKEN_ENV_NAME
from v14 import controlled_real_execution_authorization_integration as execution_auth


READ_ONLY = True
CONFIGURATION_ACTIVATION_ONLY = True

TOKEN_ENV_NAME = DEFAULT_TOKEN_ENV_NAME

REQUIRE_PROCESS_ENVIRONMENT = True

ALLOW_SECRET_VALUE_EXPOSURE = False
ALLOW_SECRET_LOGGING = False
ALLOW_SECRET_PERSISTENCE = False

ALLOW_SESSION_CREATION = False
ALLOW_NETWORK_EXECUTION = False

ALLOW_CORE_INPUT = execution_auth.ALLOW_CORE_INPUT
ALLOW_SCORE = execution_auth.ALLOW_SCORE
ALLOW_DECISION = execution_auth.ALLOW_DECISION
ALLOW_SUPABASE_WRITE = execution_auth.ALLOW_SUPABASE_WRITE
ALLOW_PRODUCTION_WRITE = execution_auth.ALLOW_PRODUCTION_WRITE


def build_runtime_token_activation_evidence():
    checks = {
        "read_only": READ_ONLY is True,
        "configuration_activation_only": (
            CONFIGURATION_ACTIVATION_ONLY is True
        ),
        "token_env_name_fixed": (
            TOKEN_ENV_NAME == "FINMIND_API_TOKEN"
        ),
        "process_environment_required": (
            REQUIRE_PROCESS_ENVIRONMENT is True
        ),
        "secret_value_exposure_disabled": (
            ALLOW_SECRET_VALUE_EXPOSURE is False
        ),
        "secret_logging_disabled": (
            ALLOW_SECRET_LOGGING is False
        ),
        "secret_persistence_disabled": (
            ALLOW_SECRET_PERSISTENCE is False
        ),
        "session_creation_disabled": (
            ALLOW_SESSION_CREATION is False
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
        "activation_contract_ready": all(checks.values()),
        "secret_value_exposed": False,
        "secret_persisted": False,
        "session_created": False,
        "network_executed": False,
        "real_gets_executed": 0,
        "checks": checks,
    }
