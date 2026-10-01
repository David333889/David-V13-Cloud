"""
Gate 28D.2K-3C
First Controlled Real GET Execution Evidence V1.

Immutable evidence record for the first observed controlled
FinMind real GET.

This module records only facts actually observed during the
first execution. It performs no environment read, secret read,
Session creation, HTTP request, network replay, Core execution,
decision execution, or persistence write.
"""

READ_ONLY = True
EXECUTION_EVIDENCE_ONLY = True
NO_NETWORK_REPLAY = True

BASE_COMMIT = "705c2b533a448ab048a23ea86dcd14c74ba4b542"

PROVIDER = "FINMIND"
DATASET = "TaiwanStockPrice"
STOCK_ID = "2330"
TRADING_DATE = "2026-09-30"

EXECUTION_RETURNED = True
RESULT_TYPE = "dict"
ALLOWED = True

EVIDENCE_KEYS = (
    "content_type",
    "payload",
    "size_bytes",
    "status_code",
)

REAL_GETS_OBSERVED = 1
SECOND_EXECUTION_ATTEMPTED = False
SECRET_VALUE_EXPOSED = False

CORE_INPUT_EXECUTED = False
DECISION_EXECUTED = False
SUPABASE_WRITE_EXECUTED = False
PRODUCTION_WRITE_EXECUTED = False

POST_CROSSING_WORKTREE_CLEAN = True
POST_CROSSING_LOCAL_REMOTE_MATCH = True

# These values were not printed/observed during the first
# controlled real execution. Preserve them as unknown rather
# than inferring or replaying the request.
HTTP_STATUS_OBSERVED = None
PAYLOAD_ROW_COUNT_OBSERVED = None

ALLOW_NETWORK_EXECUTION = False
ALLOW_REAL_GET_EXECUTION = False


def build_first_controlled_real_get_execution_evidence():
    checks = {
        "read_only": READ_ONLY is True,
        "execution_evidence_only": (
            EXECUTION_EVIDENCE_ONLY is True
        ),
        "no_network_replay": NO_NETWORK_REPLAY is True,

        "base_commit_fixed": (
            BASE_COMMIT
            == "705c2b533a448ab048a23ea86dcd14c74ba4b542"
        ),

        "provider_fixed": PROVIDER == "FINMIND",
        "dataset_fixed": DATASET == "TaiwanStockPrice",
        "stock_fixed": STOCK_ID == "2330",
        "trading_date_fixed": (
            TRADING_DATE == "2026-09-30"
        ),

        "execution_returned": EXECUTION_RETURNED is True,
        "result_type_fixed": RESULT_TYPE == "dict",
        "allowed_observed": ALLOWED is True,

        "evidence_keys_fixed": EVIDENCE_KEYS == (
            "content_type",
            "payload",
            "size_bytes",
            "status_code",
        ),

        "one_real_get_observed": (
            REAL_GETS_OBSERVED == 1
        ),
        "second_execution_not_attempted": (
            SECOND_EXECUTION_ATTEMPTED is False
        ),
        "secret_not_exposed": (
            SECRET_VALUE_EXPOSED is False
        ),

        "core_not_executed": CORE_INPUT_EXECUTED is False,
        "decision_not_executed": DECISION_EXECUTED is False,
        "supabase_not_written": (
            SUPABASE_WRITE_EXECUTED is False
        ),
        "production_not_written": (
            PRODUCTION_WRITE_EXECUTED is False
        ),

        "post_crossing_tree_clean": (
            POST_CROSSING_WORKTREE_CLEAN is True
        ),
        "post_crossing_sha_match": (
            POST_CROSSING_LOCAL_REMOTE_MATCH is True
        ),

        "http_status_unknown": (
            HTTP_STATUS_OBSERVED is None
        ),
        "payload_row_count_unknown": (
            PAYLOAD_ROW_COUNT_OBSERVED is None
        ),

        "network_execution_disabled": (
            ALLOW_NETWORK_EXECUTION is False
        ),
        "real_get_execution_disabled": (
            ALLOW_REAL_GET_EXECUTION is False
        ),
    }

    return {
        "evidence_record_ready": all(checks.values()),
        "network_replayed": False,
        "additional_real_gets_executed": 0,
        "checks": checks,
    }
