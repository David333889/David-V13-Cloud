# Gate 28D.2G - Yahoo / FinMind Market
# Compatibility Readiness Contract V1.
#
# Readiness state only.
# No adapter, normalization, data compare, Core input,
# provider switch, or persistence.

READ_ONLY = True

ALLOW_ADAPTER_OUTPUT = False
ALLOW_NORMALIZED_OUTPUT = False
ALLOW_DATA_SOURCE_SWITCH = False
ALLOW_CORE_INPUT = False
ALLOW_ENGINE_FORMULA_CHANGE = False
ALLOW_SCORE = False
ALLOW_DECISION = False
ALLOW_SUPABASE_WRITE = False
ALLOW_PRODUCTION_WRITE = False


NEW_PROVIDER_DEFINITION = "READY"
SOURCE_MAPPING_STATUS = "READY"
SEMANTIC_EVIDENCE_STATUS = "READY"

NEW_ADAPTER_STATUS = "NOT_READY"
NORMALIZED_OUTPUT_STATUS = "BLOCKED"

SAME_STOCK_COMPARE_STATUS = "REQUIRED_NOT_EXECUTED"
SAME_TRADING_DATE_COMPARE_STATUS = (
    "REQUIRED_NOT_EXECUTED"
)

OHLC_COMPARE_STATUS = "REQUIRED_NOT_EXECUTED"
VOLUME_COMPARE_STATUS = "REQUIRED_NOT_EXECUTED"

ADJUSTMENT_COMPATIBILITY = "PENDING"
VOLUME_UNIT_COMPATIBILITY = "PENDING"
TRADING_DATE_COMPATIBILITY = "PENDING"
TIMEZONE_COMPATIBILITY = "PENDING"
CORPORATE_ACTION_COMPATIBILITY = "PENDING"
MISSING_DATA_COMPATIBILITY = "PENDING"
SUSPENDED_TRADING_COMPATIBILITY = "PENDING"
PRICE_PRECISION_COMPATIBILITY = "PENDING"

ZERO_MISSING_AUTO_EQUIVALENCE = "BLOCKED"

DATA_COMPARE_STATUS = "NOT_EXECUTED"
BASELINE_TEST_STATUS = "NOT_EXECUTED"
COMPATIBILITY_RESULT = "NOT_ESTABLISHED"

PROVIDER_SWITCH_STATUS = "BLOCKED"
V13_CORE_SOURCE_SWITCH = "BLOCKED"
ENGINE_FORMULA_CHANGE = "BLOCKED"


def get_market_compatibility_readiness():
    """
    Return Yahoo / FinMind compatibility readiness state.

    This function does not perform provider comparison,
    normalization, baseline testing, or source switching.
    """
    return {
        "new_provider_definition": NEW_PROVIDER_DEFINITION,
        "source_mapping_status": SOURCE_MAPPING_STATUS,
        "semantic_evidence_status": SEMANTIC_EVIDENCE_STATUS,
        "new_adapter_status": NEW_ADAPTER_STATUS,
        "normalized_output_status": NORMALIZED_OUTPUT_STATUS,
        "same_stock_compare_status": (
            SAME_STOCK_COMPARE_STATUS
        ),
        "same_trading_date_compare_status": (
            SAME_TRADING_DATE_COMPARE_STATUS
        ),
        "ohlc_compare_status": OHLC_COMPARE_STATUS,
        "volume_compare_status": VOLUME_COMPARE_STATUS,
        "adjustment_compatibility": (
            ADJUSTMENT_COMPATIBILITY
        ),
        "volume_unit_compatibility": (
            VOLUME_UNIT_COMPATIBILITY
        ),
        "trading_date_compatibility": (
            TRADING_DATE_COMPATIBILITY
        ),
        "timezone_compatibility": (
            TIMEZONE_COMPATIBILITY
        ),
        "corporate_action_compatibility": (
            CORPORATE_ACTION_COMPATIBILITY
        ),
        "missing_data_compatibility": (
            MISSING_DATA_COMPATIBILITY
        ),
        "suspended_trading_compatibility": (
            SUSPENDED_TRADING_COMPATIBILITY
        ),
        "price_precision_compatibility": (
            PRICE_PRECISION_COMPATIBILITY
        ),
        "zero_missing_auto_equivalence": (
            ZERO_MISSING_AUTO_EQUIVALENCE
        ),
        "data_compare_status": DATA_COMPARE_STATUS,
        "baseline_test_status": BASELINE_TEST_STATUS,
        "compatibility_result": COMPATIBILITY_RESULT,
        "provider_switch_status": PROVIDER_SWITCH_STATUS,
        "v13_core_source_switch": V13_CORE_SOURCE_SWITCH,
        "engine_formula_change": ENGINE_FORMULA_CHANGE,
        "read_only": READ_ONLY,
        "allow_adapter_output": ALLOW_ADAPTER_OUTPUT,
        "allow_normalized_output": (
            ALLOW_NORMALIZED_OUTPUT
        ),
        "allow_data_source_switch": (
            ALLOW_DATA_SOURCE_SWITCH
        ),
        "allow_core_input": ALLOW_CORE_INPUT,
        "allow_engine_formula_change": (
            ALLOW_ENGINE_FORMULA_CHANGE
        ),
        "allow_score": ALLOW_SCORE,
        "allow_decision": ALLOW_DECISION,
        "allow_supabase_write": ALLOW_SUPABASE_WRITE,
        "allow_production_write": (
            ALLOW_PRODUCTION_WRITE
        ),
    }