# Gate 28D.2I - Market Data Evidence Compare Contract V1.
#
# Contract only.
# No live fetch, normalization, compatibility establishment,
# adapter output, provider switching, Core input,
# engine formula change, scoring, decision, or persistence.

READ_ONLY = True

ALLOW_EVIDENCE_VALIDATION = True
ALLOW_FIELD_COMPARE = True

ALLOW_LIVE_FETCH = False
ALLOW_NORMALIZATION = False
ALLOW_COMPATIBILITY_ESTABLISHMENT = False
ALLOW_ADAPTER_OUTPUT = False
ALLOW_PROVIDER_SWITCH = False
ALLOW_CORE_INPUT = False
ALLOW_ENGINE_FORMULA_CHANGE = False
ALLOW_SCORE = False
ALLOW_DECISION = False
ALLOW_SUPABASE_WRITE = False
ALLOW_PRODUCTION_WRITE = False


REQUIRED_COMPARE_DIMENSIONS = (
    "SAME_STOCK",
    "SAME_TRADING_DATE",
    "OHLC",
    "VOLUME",
)

ALLOWED_COMPARE_RESULTS = (
    "MATCH",
    "MISMATCH",
    "NOT_COMPARED",
    "INSUFFICIENT_EVIDENCE",
)


def get_market_data_evidence_compare_contract():
    """
    Return the read-only market data evidence compare contract.

    This function does not fetch live data, normalize market data,
    establish provider compatibility, switch providers, enter Core,
    score, decide, or write persistence.
    """
    return {
        "read_only": READ_ONLY,
        "allow_evidence_validation": (
            ALLOW_EVIDENCE_VALIDATION
        ),
        "allow_field_compare": ALLOW_FIELD_COMPARE,
        "allow_live_fetch": ALLOW_LIVE_FETCH,
        "allow_normalization": ALLOW_NORMALIZATION,
        "allow_compatibility_establishment": (
            ALLOW_COMPATIBILITY_ESTABLISHMENT
        ),
        "allow_adapter_output": ALLOW_ADAPTER_OUTPUT,
        "allow_provider_switch": ALLOW_PROVIDER_SWITCH,
        "allow_core_input": ALLOW_CORE_INPUT,
        "allow_engine_formula_change": (
            ALLOW_ENGINE_FORMULA_CHANGE
        ),
        "allow_score": ALLOW_SCORE,
        "allow_decision": ALLOW_DECISION,
        "allow_supabase_write": ALLOW_SUPABASE_WRITE,
        "allow_production_write": ALLOW_PRODUCTION_WRITE,
        "required_compare_dimensions": (
            REQUIRED_COMPARE_DIMENSIONS
        ),
        "allowed_compare_results": (
            ALLOWED_COMPARE_RESULTS
        ),
    }