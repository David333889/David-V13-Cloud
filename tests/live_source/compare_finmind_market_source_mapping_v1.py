from importlib import import_module


EXPECTED_RAW_FIELDS = (
    "date",
    "stock_id",
    "open",
    "max",
    "min",
    "close",
    "Trading_Volume",
)


def main():
    print(
        "=== GATE 28D.2E - FINMIND MARKET "
        "SOURCE MAPPING CONTRACT V1 ==="
    )

    module = import_module(
        "v14.finmind_market_source_mapping"
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

    assert module.RAW_FIELDS == EXPECTED_RAW_FIELDS

    status = module.RAW_FIELD_STATUS

    assert isinstance(status, dict)

    assert set(status) == set(
        EXPECTED_RAW_FIELDS
    )

    assert status["date"] == "MAPPING_PENDING"
    assert status["stock_id"] == "IDENTITY_LOCKED"

    assert status["open"] == "MAPPING_PENDING"
    assert status["max"] == "MAPPING_PENDING"
    assert status["min"] == "MAPPING_PENDING"
    assert status["close"] == "MAPPING_PENDING"

    assert status["Trading_Volume"] == "UNIT_PENDING"

    get_mapping = getattr(
        module,
        "get_market_source_mapping",
        None,
    )

    assert callable(get_mapping)

    mapping = get_mapping()

    assert isinstance(mapping, dict)

    assert mapping["provider"] == "FinMind"
    assert mapping["dataset"] == "TaiwanStockPrice"

    assert mapping["raw_fields"] == EXPECTED_RAW_FIELDS

    assert mapping["field_status"] == status

    assert mapping["read_only"] is True
    assert mapping["allow_normalized_output"] is False
    assert mapping["allow_core_input"] is False
    assert mapping["allow_score"] is False
    assert mapping["allow_decision"] is False
    assert mapping["allow_supabase_write"] is False
    assert mapping["allow_production_write"] is False

    print("[PASS] FinMind provider locked")
    print("[PASS] TaiwanStockPrice dataset locked")
    print("[PASS] exactly seven raw fields locked")
    print("[PASS] stock identity locked")
    print("[PASS] price mappings remain pending")
    print("[PASS] Trading_Volume unit remains pending")
    print("[PASS] normalized output blocked")
    print("[PASS] Core / Score / Decision blocked")
    print("[PASS] Supabase / Production write blocked")

    print(
        "=== GATE 28D.2E FINMIND MARKET "
        "SOURCE MAPPING RESULT: PASS ==="
    )


if __name__ == "__main__":
    main()