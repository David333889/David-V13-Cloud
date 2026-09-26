from importlib import import_module


def main():
    print(
        "=== GATE 28D.2G - YAHOO / FINMIND MARKET "
        "COMPATIBILITY READINESS CONTRACT V1 ==="
    )

    module = import_module(
        "v14.yahoo_finmind_market_compatibility_readiness"
    )

    assert module.READ_ONLY is True

    assert module.NEW_PROVIDER_DEFINITION == "READY"
    assert module.SOURCE_MAPPING_STATUS == "READY"
    assert module.SEMANTIC_EVIDENCE_STATUS == "READY"

    assert module.NEW_ADAPTER_STATUS == "NOT_READY"
    assert module.NORMALIZED_OUTPUT_STATUS == "BLOCKED"

    assert module.SAME_STOCK_COMPARE_STATUS == (
        "REQUIRED_NOT_EXECUTED"
    )
    assert module.SAME_TRADING_DATE_COMPARE_STATUS == (
        "REQUIRED_NOT_EXECUTED"
    )

    assert module.OHLC_COMPARE_STATUS == (
        "REQUIRED_NOT_EXECUTED"
    )
    assert module.VOLUME_COMPARE_STATUS == (
        "REQUIRED_NOT_EXECUTED"
    )

    pending_items = (
        module.ADJUSTMENT_COMPATIBILITY,
        module.VOLUME_UNIT_COMPATIBILITY,
        module.TRADING_DATE_COMPATIBILITY,
        module.TIMEZONE_COMPATIBILITY,
        module.CORPORATE_ACTION_COMPATIBILITY,
        module.MISSING_DATA_COMPATIBILITY,
        module.SUSPENDED_TRADING_COMPATIBILITY,
        module.PRICE_PRECISION_COMPATIBILITY,
    )

    assert all(
        item == "PENDING"
        for item in pending_items
    )

    assert module.ZERO_MISSING_AUTO_EQUIVALENCE == (
        "BLOCKED"
    )

    assert module.DATA_COMPARE_STATUS == "NOT_EXECUTED"
    assert module.BASELINE_TEST_STATUS == "NOT_EXECUTED"
    assert module.COMPATIBILITY_RESULT == (
        "NOT_ESTABLISHED"
    )

    assert module.PROVIDER_SWITCH_STATUS == "BLOCKED"
    assert module.V13_CORE_SOURCE_SWITCH == "BLOCKED"
    assert module.ENGINE_FORMULA_CHANGE == "BLOCKED"

    assert module.ALLOW_ADAPTER_OUTPUT is False
    assert module.ALLOW_NORMALIZED_OUTPUT is False
    assert module.ALLOW_DATA_SOURCE_SWITCH is False
    assert module.ALLOW_CORE_INPUT is False
    assert module.ALLOW_ENGINE_FORMULA_CHANGE is False
    assert module.ALLOW_SCORE is False
    assert module.ALLOW_DECISION is False
    assert module.ALLOW_SUPABASE_WRITE is False
    assert module.ALLOW_PRODUCTION_WRITE is False

    get_readiness = getattr(
        module,
        "get_market_compatibility_readiness",
        None,
    )

    assert callable(get_readiness)

    readiness = get_readiness()

    assert isinstance(readiness, dict)

    assert readiness["new_provider_definition"] == "READY"
    assert readiness["source_mapping_status"] == "READY"
    assert readiness["semantic_evidence_status"] == "READY"

    assert readiness["new_adapter_status"] == "NOT_READY"
    assert readiness["normalized_output_status"] == "BLOCKED"

    assert readiness["data_compare_status"] == "NOT_EXECUTED"
    assert readiness["baseline_test_status"] == "NOT_EXECUTED"
    assert readiness["compatibility_result"] == (
        "NOT_ESTABLISHED"
    )

    assert readiness["provider_switch_status"] == "BLOCKED"
    assert readiness["v13_core_source_switch"] == "BLOCKED"
    assert readiness["engine_formula_change"] == "BLOCKED"

    assert readiness["read_only"] is True
    assert readiness["allow_adapter_output"] is False
    assert readiness["allow_normalized_output"] is False
    assert readiness["allow_data_source_switch"] is False
    assert readiness["allow_core_input"] is False
    assert readiness["allow_engine_formula_change"] is False
    assert readiness["allow_score"] is False
    assert readiness["allow_decision"] is False
    assert readiness["allow_supabase_write"] is False
    assert readiness["allow_production_write"] is False

    print("[PASS] provider definition / source mapping ready")
    print("[PASS] semantic evidence ready")
    print("[PASS] adapter / normalized output remain blocked")
    print("[PASS] same-stock / same-date compare not executed")
    print("[PASS] OHLCV compare not executed")
    print("[PASS] compatibility dimensions remain pending")
    print("[PASS] zero / missing auto-equivalence blocked")
    print("[PASS] data compare / baseline test not executed")
    print("[PASS] compatibility result not established")
    print("[PASS] provider / V13 Core source switch blocked")
    print("[PASS] Engine Formula change blocked")
    print("[PASS] Core / Score / Decision blocked")
    print("[PASS] Supabase / Production write blocked")

    print(
        "=== GATE 28D.2G YAHOO / FINMIND MARKET "
        "COMPATIBILITY READINESS RESULT: PASS ==="
    )


if __name__ == "__main__":
    main()