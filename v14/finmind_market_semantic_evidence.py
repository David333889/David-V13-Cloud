# Gate 28D.2F - FinMind Market Semantic Evidence Contract V1.
#
# Semantic evidence only.
# No normalization, Core input, scoring, decision, or persistence.

PROVIDER = "FinMind"
DATASET = "TaiwanStockPrice"

READ_ONLY = True

ALLOW_NORMALIZED_OUTPUT = False
ALLOW_CORE_INPUT = False
ALLOW_SCORE = False
ALLOW_DECISION = False
ALLOW_SUPABASE_WRITE = False
ALLOW_PRODUCTION_WRITE = False


TRADING_VOLUME_SEMANTIC = "TRADED_SHARE_COUNT"
TRADING_VOLUME_EVIDENCE_STATUS = "SEMANTIC_LOCKED"

YAHOO_VOLUME_COMPATIBILITY = "COMPATIBILITY_PENDING"


TRADING_DATE_SEMANTIC = "TRADING_DATE"
TRADING_DATE_EVIDENCE_STATUS = "SEMANTIC_LOCKED"

FINMIND_TIMEZONE_STATUS = "TIMEZONE_PENDING"
YAHOO_MARKET_TIMEZONE_STATUS = "COMPATIBILITY_PENDING"


OHLC_SEMANTIC_STATUS = "SEMANTIC_LOCKED"

ZERO_MISSING_POLICY = "ZERO_IS_NOT_MISSING"

NO_PUBLISHED_PRICE_POLICY = (
    "VOLUME_POSITIVE_DOES_NOT_PROVE_VALID_PRICE"
)

OPEN_SEMANTIC_SCOPE = "MARKET_SPECIFIC"


NORMALIZED_VOLUME_STATUS = "BLOCKED"
NORMALIZED_TIMESTAMP_STATUS = "BLOCKED"


def get_market_semantic_evidence():
    """
    Return locked and pending semantic evidence.

    This function does not normalize raw market data.
    """
    return {
        "provider": PROVIDER,
        "dataset": DATASET,
        "trading_volume": {
            "semantic": TRADING_VOLUME_SEMANTIC,
            "evidence_status": (
                TRADING_VOLUME_EVIDENCE_STATUS
            ),
            "yahoo_compatibility": (
                YAHOO_VOLUME_COMPATIBILITY
            ),
        },
        "trading_date": {
            "semantic": TRADING_DATE_SEMANTIC,
            "evidence_status": (
                TRADING_DATE_EVIDENCE_STATUS
            ),
            "finmind_timezone": (
                FINMIND_TIMEZONE_STATUS
            ),
            "yahoo_market_timezone": (
                YAHOO_MARKET_TIMEZONE_STATUS
            ),
        },
        "ohlc": {
            "semantic_status": OHLC_SEMANTIC_STATUS,
            "zero_missing_policy": ZERO_MISSING_POLICY,
            "no_published_price_policy": (
                NO_PUBLISHED_PRICE_POLICY
            ),
            "open_semantic_scope": OPEN_SEMANTIC_SCOPE,
        },
        "normalized_volume_status": (
            NORMALIZED_VOLUME_STATUS
        ),
        "normalized_timestamp_status": (
            NORMALIZED_TIMESTAMP_STATUS
        ),
        "read_only": READ_ONLY,
        "allow_normalized_output": (
            ALLOW_NORMALIZED_OUTPUT
        ),
        "allow_core_input": ALLOW_CORE_INPUT,
        "allow_score": ALLOW_SCORE,
        "allow_decision": ALLOW_DECISION,
        "allow_supabase_write": (
            ALLOW_SUPABASE_WRITE
        ),
        "allow_production_write": (
            ALLOW_PRODUCTION_WRITE
        ),
    }