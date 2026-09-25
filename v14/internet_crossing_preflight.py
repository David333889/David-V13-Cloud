# Gate 28D.0P - Internet Crossing Preflight V1.
#
# This module performs configuration/readiness checks only.
# It must not execute network requests or require a live token.

FINMIND_HOST = "api.finmindtrade.com"
FINMIND_BASE_URL = "https://api.finmindtrade.com/api/v4/data"
DATASET = "TaiwanStockPrice"

ALLOW_LIVE_GET = False

ALLOW_CORE_INPUT = False
ALLOW_SCORE = False
ALLOW_DECISION = False
ALLOW_SUPABASE_WRITE = False
ALLOW_PRODUCTION_WRITE = False


def run_preflight():
    """
    Return the fixed safety/readiness contract for the first
    controlled Internet crossing.

    This function performs no network request and requires no token.
    """

    return {
        "ready": True,
        "network_executed": False,
        "token_required": False,
        "method": "GET",
        "host": FINMIND_HOST,
        "base_url": FINMIND_BASE_URL,
        "dataset": DATASET,
        "allow_live_get": ALLOW_LIVE_GET,
        "allow_core_input": ALLOW_CORE_INPUT,
        "allow_score": ALLOW_SCORE,
        "allow_decision": ALLOW_DECISION,
        "allow_supabase_write": ALLOW_SUPABASE_WRITE,
        "allow_production_write": ALLOW_PRODUCTION_WRITE,
    }
