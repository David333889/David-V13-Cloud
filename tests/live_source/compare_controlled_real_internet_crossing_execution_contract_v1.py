import importlib


def main():
    print(
        "=== GATE 28D.2K-2E - CONTROLLED REAL INTERNET "
        "CROSSING EXECUTION CONTRACT V1 ==="
    )

    try:
        module = importlib.import_module(
            "v14.controlled_real_internet_crossing_execution"
        )
    except ModuleNotFoundError:
        print(
            "[EXPECTED RED] controlled real Internet "
            "crossing execution contract module not found"
        )
        raise SystemExit(1)

    get_contract = getattr(
        module,
        "get_controlled_real_internet_crossing_execution_contract",
        None,
    )

    assert callable(get_contract), (
        "execution contract getter missing"
    )

    assert getattr(module, "READ_ONLY", None) is True
    assert getattr(module, "ONE_SHOT_ONLY", None) is True
    assert getattr(module, "SINGLE_STOCK_ONLY", None) is True
    assert getattr(
        module,
        "SINGLE_TRADING_DATE_ONLY",
        None,
    ) is True

    assert getattr(
        module,
        "ALLOW_REAL_SESSION_FACTORY",
        None,
    ) is True

    assert getattr(
        module,
        "ALLOW_REAL_GET",
        None,
    ) is True

    assert getattr(
        module,
        "MAX_REAL_GETS",
        None,
    ) == 1

    for flag in (
        "ALLOW_NORMALIZATION",
        "ALLOW_COMPATIBILITY_ESTABLISHMENT",
        "ALLOW_PROVIDER_SWITCH",
        "ALLOW_CORE_INPUT",
        "ALLOW_SCORE",
        "ALLOW_DECISION",
        "ALLOW_SUPABASE_WRITE",
        "ALLOW_PRODUCTION_WRITE",
    ):
        assert getattr(module, flag, None) is False

    contract = get_contract()

    assert contract == {
        "read_only": True,
        "one_shot_only": True,
        "single_stock_only": True,
        "single_trading_date_only": True,
        "allow_real_session_factory": True,
        "allow_real_get": True,
        "max_real_gets": 1,
        "allow_normalization": False,
        "allow_compatibility_establishment": False,
        "allow_provider_switch": False,
        "allow_core_input": False,
        "allow_score": False,
        "allow_decision": False,
        "allow_supabase_write": False,
        "allow_production_write": False,
    }

    print("[PASS] read-only execution boundary fixed")
    print("[PASS] single stock/date boundary fixed")
    print("[PASS] real session factory allowed")
    print("[PASS] exactly one real GET authorized")
    print("[PASS] compatibility/core/write paths disabled")

    print(
        "=== GATE 28D.2K-2E CONTROLLED REAL INTERNET "
        "CROSSING EXECUTION CONTRACT RESULT: PASS ==="
    )


if __name__ == "__main__":
    main()
