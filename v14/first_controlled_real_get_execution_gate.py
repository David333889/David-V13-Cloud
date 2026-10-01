"""
Gate 28D.2K-3B
First Controlled Real GET Execution Gate V1.

Execution-gate contract/evidence only.

Defines the final protected conditions required before the
first controlled real GET may actually be executed.

This module performs no environment read, secret read,
Session creation, HTTP request, or Internet crossing.
"""

from v14.controlled_runtime_entry_integration import (
    DATASET,
    ONE_SHOT_ONLY,
    MAX_REAL_GETS,
)
from v14.first_controlled_real_get_execution_plan import (
    STOCK_ID,
    TRADING_DATE,
    REQUIRE_TOKEN_AVAILABLE,
)
from v14 import controlled_real_execution_authorization_integration as execution_auth


READ_ONLY = True
EXECUTION_GATE_ONLY = True

UNIQUE_RUNTIME_ENTRY = True
PROCESS_ENVIRONMENT_SOURCE = True
MINIMAL_TOKEN_MAPPING_ONLY = True

SECOND_EXECUTION_DENIED = True

ALLOW_SECRET_VALUE_EXPOSURE = False

ALLOW_NETWORK_EXECUTION = False
ALLOW_REAL_GET_EXECUTION = False

ALLOW_CORE_INPUT = execution_auth.ALLOW_CORE_INPUT
ALLOW_SCORE = execution_auth.ALLOW_SCORE
ALLOW_DECISION = execution_auth.ALLOW_DECISION
ALLOW_SUPABASE_WRITE = execution_auth.ALLOW_SUPABASE_WRITE
ALLOW_PRODUCTION_WRITE = execution_auth.ALLOW_PRODUCTION_WRITE


def build_first_real_get_execution_gate_evidence():
    checks = {
        "read_only": READ_ONLY is True,
        "execution_gate_only": EXECUTION_GATE_ONLY is True,

        "stock_fixed": STOCK_ID == "2330",
        "trading_date_fixed": (
            TRADING_DATE == "2026-09-30"
        ),
        "dataset_fixed": DATASET == "TaiwanStockPrice",

        "unique_runtime_entry": (
            UNIQUE_RUNTIME_ENTRY is True
        ),
        "process_environment_source": (
            PROCESS_ENVIRONMENT_SOURCE is True
        ),
        "minimal_token_mapping_only": (
            MINIMAL_TOKEN_MAPPING_ONLY is True
        ),

        "one_shot_only": ONE_SHOT_ONLY is True,
        "max_real_gets": MAX_REAL_GETS == 1,
        "second_execution_denied": (
            SECOND_EXECUTION_DENIED is True
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
        "execution_gate_ready": all(checks.values()),
        "network_executed": False,
        "real_gets_executed": 0,
        "secret_value_exposed": False,
        "checks": checks,
    }
