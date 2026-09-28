# Gate 28D.2K-2D - Controlled Real Sample
# Entry Contract V1.
#
# Boundary contract only.
# Real session factory capability may be used by a future
# execution layer, but real network GET remains disabled here.
#
# No normalization, compatibility establishment,
# provider switching, Core input, scoring, decision,
# or persistence.

READ_ONLY = True
ONE_SHOT_ONLY = True
SINGLE_STOCK_ONLY = True
SINGLE_TRADING_DATE_ONLY = True

ALLOW_REAL_SESSION_FACTORY = True
ALLOW_REAL_GET = False

ALLOW_NORMALIZATION = False
ALLOW_COMPATIBILITY_ESTABLISHMENT = False
ALLOW_PROVIDER_SWITCH = False
ALLOW_CORE_INPUT = False
ALLOW_SCORE = False
ALLOW_DECISION = False
ALLOW_SUPABASE_WRITE = False
ALLOW_PRODUCTION_WRITE = False


def get_controlled_real_sample_entry_contract():
    """
    Return the fail-closed controlled real sample
    entry contract.

    This contract declares that a future execution layer
    may use the already-protected real session factory.

    It does not execute a real GET, use a runtime token,
    normalize market data, establish provider compatibility,
    switch providers, enter Core, score, decide,
    or write persistence.
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