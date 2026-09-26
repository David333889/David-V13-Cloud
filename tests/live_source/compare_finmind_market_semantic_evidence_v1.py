from importlib import import_module


def main():
    print(
        "=== GATE 28D.2F - FINMIND MARKET "
        "SEMANTIC EVIDENCE CONTRACT V1 ==="
    )

    module = import_module(
        "v14.finmind_market_semantic_evidence"
    )

    assert module.PROVIDER == "FinMind"
    assert module.DATASET == "TaiwanStockPrice"

    assert module.READ_ONLY is True

    assert module.ALLOW_NORMALIZED_OUTPUT is False
    assert module.ALLOW_CORE_INPUT is False
    assert module.ALLOW_SCORE is False
    assert module.ALLOW_DECISION is False
    assert module.ALLOW_SUPABASE_WRITE is False
    assert module.ALLOW_PRODUCTION_WRITE is False

    assert module.TRADING_VOLUME_SEMANTIC == (
        "TRADED_SHARE_COUNT"
    )
    assert module.TRADING_VOLUME_EVIDENCE_STATUS == (
        "SEMANTIC_LOCKED"
    )
    assert module.YAHOO_VOLUME_COMPATIBILITY == (
        "COMPATIBILITY_PENDING"
    )

    assert module.TRADING_DATE_SEMANTIC == (
        "TRADING_DATE"
    )
    assert module.TRADING_DATE_EVIDENCE_STATUS == (
        "SEMANTIC_LOCKED"
    )

    assert module.FINMIND_TIMEZONE_STATUS == (
        "TIMEZONE_PENDING"
    )
    assert module.YAHOO_MARKET_TIMEZONE_STATUS == (
        "COMPATIBILITY_PENDING"
    )

    assert module.OHLC_SEMANTIC_STATUS == (
        "SEMANTIC_LOCKED"
    )
    assert module.ZERO_MISSING_POLICY == (
        "ZERO_IS_NOT_MISSING"
    )
    assert module.NO_PUBLISHED_PRICE_POLICY == (
        "VOLUME_POSITIVE_DOES_NOT_PROVE_VALID_PRICE"
    )
    assert module.OPEN_SEMANTIC_SCOPE == (
        "MARKET_SPECIFIC"
    )

    assert module.NORMALIZED_VOLUME_STATUS == "BLOCKED"
    assert module.NORMALIZED_TIMESTAMP_STATUS == "BLOCKED"

    get_evidence = getattr(
        module,
        "get_market_semantic_evidence",
        None,
    )

    assert callable(get_evidence)

    evidence = get_evidence()

    assert isinstance(evidence, dict)

    assert evidence["provider"] == "FinMind"
    assert evidence["dataset"] == "TaiwanStockPrice"

    assert evidence["trading_volume"]["semantic"] == (
        "TRADED_SHARE_COUNT"
    )
    assert evidence["trading_volume"]["evidence_status"] == (
        "SEMANTIC_LOCKED"
    )
    assert evidence["trading_volume"]["yahoo_compatibility"] == (
        "COMPATIBILITY_PENDING"
    )

    assert evidence["trading_date"]["semantic"] == (
        "TRADING_DATE"
    )
    assert evidence["trading_date"]["evidence_status"] == (
        "SEMANTIC_LOCKED"
    )
    assert evidence["trading_date"]["finmind_timezone"] == (
        "TIMEZONE_PENDING"
    )

    assert evidence["ohlc"]["zero_missing_policy"] == (
        "ZERO_IS_NOT_MISSING"
    )
    assert evidence["ohlc"]["no_published_price_policy"] == (
        "VOLUME_POSITIVE_DOES_NOT_PROVE_VALID_PRICE"
    )
    assert evidence["ohlc"]["open_semantic_scope"] == (
        "MARKET_SPECIFIC"
    )

    assert evidence["normalized_volume_status"] == "BLOCKED"
    assert evidence["normalized_timestamp_status"] == "BLOCKED"

    assert evidence["read_only"] is True
    assert evidence["allow_normalized_output"] is False
    assert evidence["allow_core_input"] is False
    assert evidence["allow_score"] is False
    assert evidence["allow_decision"] is False
    assert evidence["allow_supabase_write"] is False
    assert evidence["allow_production_write"] is False

    print("[PASS] FinMind volume semantic locked")
    print("[PASS] Yahoo volume compatibility remains pending")
    print("[PASS] FinMind trading-date semantic locked")
    print("[PASS] FinMind timezone remains pending")
    print("[PASS] zero is not treated as missing")
    print("[PASS] positive volume does not prove valid price")
    print("[PASS] open semantic remains market-specific")
    print("[PASS] normalized volume / timestamp blocked")
    print("[PASS] Core / Score / Decision blocked")
    print("[PASS] Supabase / Production write blocked")

    print(
        "=== GATE 28D.2F FINMIND MARKET "
        "SEMANTIC EVIDENCE RESULT: PASS ==="
    )


if __name__ == "__main__":
    main()