# Gate 28D.2K-2A - FinMind Baseline Evidence
# Observation Contract V1.
#
# Boundary contract only.
# No live fetch, normalization, compatibility establishment,
# provider switching, Core input, scoring, decision,
# or persistence.

READ_ONLY = True

ALLOW_RAW_EVIDENCE_INPUT = True
ALLOW_BASELINE_FIELD_OBSERVATION = True

ALLOW_RAW_PAYLOAD_STORAGE = False
ALLOW_NORMALIZATION = False
ALLOW_ADAPTER_OUTPUT = False
ALLOW_COMPATIBILITY_ESTABLISHMENT = False
ALLOW_PROVIDER_SWITCH = False
ALLOW_CORE_INPUT = False
ALLOW_SCORE = False
ALLOW_DECISION = False
ALLOW_SUPABASE_WRITE = False
ALLOW_PRODUCTION_WRITE = False

SINGLE_STOCK_REQUIRED = True
SINGLE_TRADING_DATE_REQUIRED = True
EXACT_REQUIRED_FIELDS = True

REQUIRED_EVIDENCE_FIELDS = (
    "date",
    "stock_id",
    "open",
    "max",
    "min",
    "close",
    "Trading_Volume",
)


def get_finmind_baseline_evidence_observation_contract():
    """
    Return the fail-closed FinMind baseline evidence
    observation contract.

    This contract describes the boundary only.

    It does not fetch live data, expose a raw payload,
    normalize market data, establish compatibility,
    switch providers, enter Core, score, decide,
    or write persistence.
    """
    return {
        "read_only": READ_ONLY,
        "allow_raw_evidence_input": (
            ALLOW_RAW_EVIDENCE_INPUT
        ),
        "allow_baseline_field_observation": (
            ALLOW_BASELINE_FIELD_OBSERVATION
        ),
        "allow_raw_payload_storage": (
            ALLOW_RAW_PAYLOAD_STORAGE
        ),
        "allow_normalization": ALLOW_NORMALIZATION,
        "allow_adapter_output": ALLOW_ADAPTER_OUTPUT,
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
        "single_stock_required": (
            SINGLE_STOCK_REQUIRED
        ),
        "single_trading_date_required": (
            SINGLE_TRADING_DATE_REQUIRED
        ),
        "exact_required_fields": EXACT_REQUIRED_FIELDS,
        "required_evidence_fields": (
            REQUIRED_EVIDENCE_FIELDS
        ),
    }
