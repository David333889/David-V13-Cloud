# Gate 28D.2J - Legacy Yahoo Market Source Provenance Contract V1.
#
# Provenance contract only.
# Describes the existing legacy Yahoo/yfinance source path.
# No live fetch, new fetch path, normalization,
# compatibility establishment, provider switching,
# Core input, scoring, decision, or persistence.

PROVIDER = "Yahoo"
CLIENT = "yfinance"

READ_ONLY = True

PRIMARY_FETCH = "yf.download"

FALLBACK_FETCH = (
    "yf.download",
    "yf.Ticker.history",
)

PERIOD = "1y"
INTERVAL = "1d"
AUTO_ADJUST = False

CLEANING_BOUNDARY = "_clean_history_frame"

REQUIRED_COLUMNS = (
    "Open",
    "High",
    "Low",
    "Close",
    "Volume",
)

FETCH_PATH_PROVENANCE_REQUIRED = True
CLEANED_DATA_IS_RAW_PAYLOAD = False

ALLOW_PROVENANCE_DESCRIPTION = True

ALLOW_LIVE_FETCH = False
ALLOW_NEW_FETCH_PATH = False
ALLOW_NORMALIZATION = False
ALLOW_COMPATIBILITY_ESTABLISHMENT = False
ALLOW_PROVIDER_SWITCH = False
ALLOW_CORE_INPUT = False
ALLOW_ENGINE_FORMULA_CHANGE = False
ALLOW_SCORE = False
ALLOW_DECISION = False
ALLOW_SUPABASE_WRITE = False
ALLOW_PRODUCTION_WRITE = False


def get_legacy_yahoo_market_source_provenance():
    """
    Return the locked legacy Yahoo/yfinance source provenance.

    This function describes the existing source path only.
    It does not fetch live data, create a new fetch path,
    normalize market data, establish compatibility,
    switch providers, enter Core, score, decide,
    or write persistence.
    """
    return {
        "provider": PROVIDER,
        "client": CLIENT,
        "primary_fetch": PRIMARY_FETCH,
        "fallback_fetch": FALLBACK_FETCH,
        "period": PERIOD,
        "interval": INTERVAL,
        "auto_adjust": AUTO_ADJUST,
        "cleaning_boundary": CLEANING_BOUNDARY,
        "required_columns": REQUIRED_COLUMNS,
        "fetch_path_provenance_required": (
            FETCH_PATH_PROVENANCE_REQUIRED
        ),
        "cleaned_data_is_raw_payload": (
            CLEANED_DATA_IS_RAW_PAYLOAD
        ),
        "read_only": READ_ONLY,
        "allow_provenance_description": (
            ALLOW_PROVENANCE_DESCRIPTION
        ),
        "allow_live_fetch": ALLOW_LIVE_FETCH,
        "allow_new_fetch_path": ALLOW_NEW_FETCH_PATH,
        "allow_normalization": ALLOW_NORMALIZATION,
        "allow_compatibility_establishment": (
            ALLOW_COMPATIBILITY_ESTABLISHMENT
        ),
        "allow_provider_switch": ALLOW_PROVIDER_SWITCH,
        "allow_core_input": ALLOW_CORE_INPUT,
        "allow_engine_formula_change": (
            ALLOW_ENGINE_FORMULA_CHANGE
        ),
        "allow_score": ALLOW_SCORE,
        "allow_decision": ALLOW_DECISION,
        "allow_supabase_write": ALLOW_SUPABASE_WRITE,
        "allow_production_write": ALLOW_PRODUCTION_WRITE,
    }