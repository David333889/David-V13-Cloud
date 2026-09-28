# Gate 28D.2K-2A - FinMind Baseline Evidence
# Observation Contract V1.
#
# Contract comparator only.
# No live fetch, normalization, compatibility establishment,
# provider switching, Core input, scoring, decision,
# or persistence.

import importlib


def main():
    print(
        "=== GATE 28D.2K-2A - FINMIND BASELINE "
        "EVIDENCE OBSERVATION CONTRACT V1 ==="
    )

    try:
        module = importlib.import_module(
            "v14.finmind_baseline_evidence_observation"
        )
    except ModuleNotFoundError:
        print(
            "[EXPECTED RED] FinMind baseline evidence "
            "observation module not found"
        )
        raise SystemExit(1)

    assert module.READ_ONLY is True

    assert module.ALLOW_RAW_EVIDENCE_INPUT is True
    assert module.ALLOW_BASELINE_FIELD_OBSERVATION is True

    assert module.ALLOW_RAW_PAYLOAD_STORAGE is False
    assert module.ALLOW_NORMALIZATION is False
    assert module.ALLOW_ADAPTER_OUTPUT is False
    assert module.ALLOW_COMPATIBILITY_ESTABLISHMENT is False
    assert module.ALLOW_PROVIDER_SWITCH is False
    assert module.ALLOW_CORE_INPUT is False
    assert module.ALLOW_SCORE is False
    assert module.ALLOW_DECISION is False
    assert module.ALLOW_SUPABASE_WRITE is False
    assert module.ALLOW_PRODUCTION_WRITE is False

    assert module.SINGLE_STOCK_REQUIRED is True
    assert module.SINGLE_TRADING_DATE_REQUIRED is True
    assert module.EXACT_REQUIRED_FIELDS is True

    assert module.REQUIRED_EVIDENCE_FIELDS == (
        "date",
        "stock_id",
        "open",
        "max",
        "min",
        "close",
        "Trading_Volume",
    )

    contract = (
        module.get_finmind_baseline_evidence_observation_contract()
    )

    assert contract["read_only"] is True
    assert contract["allow_raw_evidence_input"] is True
    assert (
        contract["allow_baseline_field_observation"]
        is True
    )

    assert contract["allow_raw_payload_storage"] is False
    assert contract["allow_normalization"] is False
    assert contract["allow_adapter_output"] is False
    assert (
        contract["allow_compatibility_establishment"]
        is False
    )
    assert contract["allow_provider_switch"] is False
    assert contract["allow_core_input"] is False
    assert contract["allow_score"] is False
    assert contract["allow_decision"] is False
    assert contract["allow_supabase_write"] is False
    assert contract["allow_production_write"] is False

    assert contract["single_stock_required"] is True
    assert contract["single_trading_date_required"] is True
    assert contract["exact_required_fields"] is True

    assert contract["required_evidence_fields"] == (
        "date",
        "stock_id",
        "open",
        "max",
        "min",
        "close",
        "Trading_Volume",
    )

    print(
        "FINMIND BASELINE EVIDENCE OBSERVATION "
        "CONTRACT V1: PASS"
    )


if __name__ == "__main__":
    main()
