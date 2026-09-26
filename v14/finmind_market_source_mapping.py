# Gate 28D.2E - FinMind Market Source Mapping Contract V1.
#
# Raw source semantics only.
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


RAW_FIELDS = (
    "date",
    "stock_id",
    "open",
    "max",
    "min",
    "close",
    "Trading_Volume",
)


RAW_FIELD_STATUS = {
    "date": "MAPPING_PENDING",
    "stock_id": "IDENTITY_LOCKED",
    "open": "MAPPING_PENDING",
    "max": "MAPPING_PENDING",
    "min": "MAPPING_PENDING",
    "close": "MAPPING_PENDING",
    "Trading_Volume": "UNIT_PENDING",
}


def get_market_source_mapping():
    """
    Return the locked FinMind TaiwanStockPrice
    raw-source mapping contract.

    This function does not normalize raw values.
    """
    return {
        "provider": PROVIDER,
        "dataset": DATASET,
        "raw_fields": RAW_FIELDS,
        "field_status": dict(RAW_FIELD_STATUS),
        "read_only": READ_ONLY,
        "allow_normalized_output": ALLOW_NORMALIZED_OUTPUT,
        "allow_core_input": ALLOW_CORE_INPUT,
        "allow_score": ALLOW_SCORE,
        "allow_decision": ALLOW_DECISION,
        "allow_supabase_write": ALLOW_SUPABASE_WRITE,
        "allow_production_write": ALLOW_PRODUCTION_WRITE,
    }