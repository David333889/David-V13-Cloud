# Gate 28D.2H - FinMind Market Source Adapter Boundary Contract V1.
#
# Boundary contract only.
# No normalization, Core input, scoring, decision,
# provider switching, or persistence.

from v14.finmind_market_semantic_evidence import (
    FINMIND_TIMEZONE_STATUS,
    NO_PUBLISHED_PRICE_POLICY,
    NORMALIZED_TIMESTAMP_STATUS,
    NORMALIZED_VOLUME_STATUS,
    TRADING_DATE_SEMANTIC,
    TRADING_VOLUME_SEMANTIC,
    YAHOO_VOLUME_COMPATIBILITY,
    ZERO_MISSING_POLICY,
)


CONTRACT_VERSION = (
    "V14_FINMIND_MARKET_SOURCE_ADAPTER_BOUNDARY_V1"
)

PROVIDER = "FinMind"
DATASET = "TaiwanStockPrice"

READ_ONLY = True

ALLOW_RAW_VALIDATION = True
ALLOW_RAW_EVIDENCE_PRESERVATION = True

ALLOW_TIMESTAMP_NORMALIZATION = False
ALLOW_VOLUME_NORMALIZATION = False
ALLOW_NORMALIZED_OUTPUT = False

ALLOW_CORE_INPUT = False
ALLOW_SCORE = False
ALLOW_DECISION = False

ALLOW_PROVIDER_SWITCH = False
ALLOW_V13_CORE_SWITCH = False

ALLOW_SUPABASE_WRITE = False
ALLOW_PRODUCTION_WRITE = False


def get_finmind_market_source_adapter_boundary():
    """
    Return the fail-closed FinMind market source adapter boundary.

    This contract may describe raw validation and evidence
    preservation only.

    It must not normalize timestamps or volume, produce normalized
    OHLCV, enter Core, switch providers, or write persistence.
    """
    return {
        "contract_version": CONTRACT_VERSION,
        "provider": PROVIDER,
        "dataset": DATASET,
        "read_only": READ_ONLY,
        "allow_raw_validation": ALLOW_RAW_VALIDATION,
        "allow_raw_evidence_preservation": (
            ALLOW_RAW_EVIDENCE_PRESERVATION
        ),
        "allow_timestamp_normalization": (
            ALLOW_TIMESTAMP_NORMALIZATION
        ),
        "allow_volume_normalization": (
            ALLOW_VOLUME_NORMALIZATION
        ),
        "allow_normalized_output": ALLOW_NORMALIZED_OUTPUT,
        "allow_core_input": ALLOW_CORE_INPUT,
        "allow_score": ALLOW_SCORE,
        "allow_decision": ALLOW_DECISION,
        "allow_provider_switch": ALLOW_PROVIDER_SWITCH,
        "allow_v13_core_switch": ALLOW_V13_CORE_SWITCH,
        "allow_supabase_write": ALLOW_SUPABASE_WRITE,
        "allow_production_write": ALLOW_PRODUCTION_WRITE,
        "zero_missing_policy": ZERO_MISSING_POLICY,
        "no_published_price_policy": (
            NO_PUBLISHED_PRICE_POLICY
        ),
        "trading_date_semantic": TRADING_DATE_SEMANTIC,
        "finmind_timezone_status": FINMIND_TIMEZONE_STATUS,
        "trading_volume_semantic": TRADING_VOLUME_SEMANTIC,
        "yahoo_volume_compatibility": (
            YAHOO_VOLUME_COMPATIBILITY
        ),
        "normalized_timestamp_status": (
            NORMALIZED_TIMESTAMP_STATUS
        ),
        "normalized_volume_status": NORMALIZED_VOLUME_STATUS,
    }