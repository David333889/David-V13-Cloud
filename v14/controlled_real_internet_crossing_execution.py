# Gate 28D.2K-2E - Controlled Real Internet
# Crossing Execution Contract V1.
#
# Capability authorization contract only.
#
# This contract authorizes a future execution layer to
# perform exactly one controlled read-only real GET.
#
# It does NOT execute a network request itself.
# It does NOT read or persist a runtime token.
# It does NOT normalize data, establish compatibility,
# switch providers, enter Core, score, decide,
# or write persistence.

READ_ONLY = True
ONE_SHOT_ONLY = True
SINGLE_STOCK_ONLY = True
SINGLE_TRADING_DATE_ONLY = True

ALLOW_REAL_SESSION_FACTORY = True
ALLOW_REAL_GET = True
MAX_REAL_GETS = 1

ALLOW_NORMALIZATION = False
ALLOW_COMPATIBILITY_ESTABLISHMENT = False
ALLOW_PROVIDER_SWITCH = False
ALLOW_CORE_INPUT = False
ALLOW_SCORE = False
ALLOW_DECISION = False
ALLOW_SUPABASE_WRITE = False
ALLOW_PRODUCTION_WRITE = False


def get_controlled_real_internet_crossing_execution_contract():
    """
    Return the fail-closed real Internet crossing
    execution authorization contract.

    The contract authorizes exactly one future
    controlled read-only real GET.

    No network request is executed here.
    No runtime token is read or persisted here.
    """

    return {
        "read_only": READ_ONLY,
        "one_shot_only": ONE_SHOT_ONLY,
        "single_stock_only": SINGLE_STOCK_ONLY,
        "single_trading_date_only": (
            SINGLE_TRADING_DATE_ONLY
        ),
        "allow_real_session_factory": (
            ALLOW_REAL_SESSION_FACTORY
        ),
        "allow_real_get": ALLOW_REAL_GET,
        "max_real_gets": MAX_REAL_GETS,
        "allow_normalization": ALLOW_NORMALIZATION,
        "allow_compatibility_establishment": (
            ALLOW_COMPATIBILITY_ESTABLISHMENT
        ),
        "allow_provider_switch": ALLOW_PROVIDER_SWITCH,
        "allow_core_input": ALLOW_CORE_INPUT,
        "allow_score": ALLOW_SCORE,
        "allow_decision": ALLOW_DECISION,
        "allow_supabase_write": ALLOW_SUPABASE_WRITE,
        "allow_production_write": (
            ALLOW_PRODUCTION_WRITE
        ),
    }
