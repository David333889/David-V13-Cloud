"""
Gate 28D.2K-2V
Runtime Token Safe Configuration Boundary V1.

Configuration-policy/evidence only.
No secret is configured or read here.
No Session creation, HTTP request, or Internet crossing.
"""

from v14.secret_runtime import DEFAULT_TOKEN_ENV_NAME
from v14 import controlled_real_execution_authorization_integration as execution_auth


READ_ONLY = True
CONFIGURATION_BOUNDARY_ONLY = True

TOKEN_ENV_NAME = DEFAULT_TOKEN_ENV_NAME

ALLOW_PROCESS_ENVIRONMENT = True
ALLOW_ENV_FILE_STORAGE = False
ALLOW_SOURCE_CODE_SECRET = False
ALLOW_JSON_SECRET_STORAGE = False
ALLOW_TEST_SECRET_STORAGE = False
ALLOW_SECRET_LOGGING = False
ALLOW_SECRET_IN_PUBLIC_RESULT = False

REQUIRE_ENV_FILE_GITIGNORE = True
REQUIRE_STREAMLIT_SECRET_GITIGNORE = True

ALLOW_SESSION_CREATION = False
ALLOW_NETWORK_EXECUTION = False

ALLOW_CORE_INPUT = execution_auth.ALLOW_CORE_INPUT
ALLOW_SCORE = execution_auth.ALLOW_SCORE
ALLOW_DECISION = execution_auth.ALLOW_DECISION
ALLOW_SUPABASE_WRITE = execution_auth.ALLOW_SUPABASE_WRITE
ALLOW_PRODUCTION_WRITE = execution_auth.ALLOW_PRODUCTION_WRITE


def build_runtime_token_configuration_evidence():
    checks = {
        "read_only": READ_ONLY is True,
        "configuration_boundary_only": (
            CONFIGURATION_BOUNDARY_ONLY is True
        ),
        "token_env_name_fixed": (
            TOKEN_ENV_NAME == "FINMIND_API_TOKEN"
        ),
        "process_environment_allowed": (
            ALLOW_PROCESS_ENVIRONMENT is True
        ),
        "env_file_storage_disabled": (
            ALLOW_ENV_FILE_STORAGE is False
        ),
        "source_code_secret_disabled": (
            ALLOW_SOURCE_CODE_SECRET is False
        ),
        "json_secret_storage_disabled": (
            ALLOW_JSON_SECRET_STORAGE is False
        ),
        "test_secret_storage_disabled": (
            ALLOW_TEST_SECRET_STORAGE is False
        ),
        "secret_logging_disabled": (
            ALLOW_SECRET_LOGGING is False
        ),
        "secret_public_result_disabled": (
            ALLOW_SECRET_IN_PUBLIC_RESULT is False
        ),
        "env_file_gitignore_required": (
            REQUIRE_ENV_FILE_GITIGNORE is True
        ),
        "streamlit_secret_gitignore_required": (
            REQUIRE_STREAMLIT_SECRET_GITIGNORE is True
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
        "configuration_boundary_ready": all(checks.values()),
        "secret_configured": False,
        "secret_value_read": False,
        "session_created": False,
        "network_executed": False,
        "real_gets_executed": 0,
        "checks": checks,
    }
