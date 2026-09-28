import importlib


def main():
    print(
        "=== GATE 28D.2K-2D - CONTROLLED REAL SAMPLE "
        "ENTRY CONTRACT V1 ==="
    )

    try:
        module = importlib.import_module(
            "v14.controlled_real_sample_entry"
        )
    except ModuleNotFoundError:
        print(
            "[EXPECTED RED] controlled real sample "
            "entry contract module not found"
        )
        raise SystemExit(1)

    get_contract = getattr(
        module,
        "get_controlled_real_sample_entry_contract",
        None,
    )

    assert callable(get_contract), (
        "get_controlled_real_sample_entry_contract missing"
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

    for flag in (
        "ALLOW_REAL_GET",
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
        "allow_real_get": False,
        "allow_normalization": False,
        "allow_compatibility_establishment": False,
        "allow_provider_switch": False,
        "allow_core_input": False,
        "allow_score": False,
        "allow_decision": False,
        "allow_supabase_write": False,
        "allow_production_write": False,
    }

    print("[PASS] read-only boundary fixed")
    print("[PASS] single stock/date boundary fixed")
    print("[PASS] real session factory capability declared")
    print("[PASS] real GET remains disabled")
    print("[PASS] compatibility/core/write paths remain disabled")

    print(
        "=== GATE 28D.2K-2D CONTROLLED REAL SAMPLE "
        "ENTRY CONTRACT RESULT: PASS ==="
    )


if __name__ == "__main__":
    main()