# Gate 28D.2I - Market Data Evidence Compare Contract V1.
#
# Contract comparator only.
# No live fetch, normalization, provider switching,
# Core input, scoring, decision, or persistence.

import v14.market_data_evidence_compare as module


def main():
    assert module.READ_ONLY is True

    assert module.ALLOW_EVIDENCE_VALIDATION is True
    assert module.ALLOW_FIELD_COMPARE is True

    assert module.ALLOW_LIVE_FETCH is False
    assert module.ALLOW_NORMALIZATION is False
    assert module.ALLOW_COMPATIBILITY_ESTABLISHMENT is False
    assert module.ALLOW_ADAPTER_OUTPUT is False
    assert module.ALLOW_PROVIDER_SWITCH is False
    assert module.ALLOW_CORE_INPUT is False
    assert module.ALLOW_ENGINE_FORMULA_CHANGE is False
    assert module.ALLOW_SCORE is False
    assert module.ALLOW_DECISION is False
    assert module.ALLOW_SUPABASE_WRITE is False
    assert module.ALLOW_PRODUCTION_WRITE is False

    assert module.REQUIRED_COMPARE_DIMENSIONS == (
        "SAME_STOCK",
        "SAME_TRADING_DATE",
        "OHLC",
        "VOLUME",
    )

    assert module.ALLOWED_COMPARE_RESULTS == (
        "MATCH",
        "MISMATCH",
        "NOT_COMPARED",
        "INSUFFICIENT_EVIDENCE",
    )

    contract = module.get_market_data_evidence_compare_contract()

    assert contract["read_only"] is True

    assert contract["allow_evidence_validation"] is True
    assert contract["allow_field_compare"] is True

    assert contract["allow_live_fetch"] is False
    assert contract["allow_normalization"] is False
    assert (
        contract["allow_compatibility_establishment"]
        is False
    )
    assert contract["allow_adapter_output"] is False
    assert contract["allow_provider_switch"] is False
    assert contract["allow_core_input"] is False
    assert contract["allow_engine_formula_change"] is False
    assert contract["allow_score"] is False
    assert contract["allow_decision"] is False
    assert contract["allow_supabase_write"] is False
    assert contract["allow_production_write"] is False

    assert contract["required_compare_dimensions"] == (
        "SAME_STOCK",
        "SAME_TRADING_DATE",
        "OHLC",
        "VOLUME",
    )

    assert contract["allowed_compare_results"] == (
        "MATCH",
        "MISMATCH",
        "NOT_COMPARED",
        "INSUFFICIENT_EVIDENCE",
    )

    print(
        "MARKET DATA EVIDENCE COMPARE CONTRACT V1: PASS"
    )


if __name__ == "__main__":
    main()