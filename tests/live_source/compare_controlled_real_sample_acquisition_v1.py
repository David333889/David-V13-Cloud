# Gate 28D.2K-2C - Controlled Real Sample
# Acquisition Contract V1.
#
# Contract only.
# No network execution in this test.

import importlib


def main():
    print(
        "=== GATE 28D.2K-2C - CONTROLLED REAL SAMPLE "
        "ACQUISITION CONTRACT V1 ==="
    )

    try:
        module = importlib.import_module(
            "v14.controlled_real_sample_acquisition"
        )
    except ModuleNotFoundError:
        print(
            "[EXPECTED RED] controlled real sample "
            "acquisition module not found"
        )
        raise SystemExit(1)

    assert module.READ_ONLY is True
    assert module.ONE_SHOT_ONLY is True
    assert module.SINGLE_STOCK_ONLY is True
    assert module.SINGLE_TRADING_DATE_ONLY is True

    assert module.ALLOW_NORMALIZATION is False
    assert (
        module.ALLOW_COMPATIBILITY_ESTABLISHMENT
        is False
    )
    assert module.ALLOW_PROVIDER_SWITCH is False
    assert module.ALLOW_CORE_INPUT is False
    assert module.ALLOW_SCORE is False
    assert module.ALLOW_DECISION is False
    assert module.ALLOW_SUPABASE_WRITE is False
    assert module.ALLOW_PRODUCTION_WRITE is False

    assert module.DATASET == "TaiwanStockPrice"

    contract = (
        module.get_controlled_real_sample_acquisition_contract()
    )

    assert contract["read_only"] is True
    assert contract["one_shot_only"] is True
    assert contract["single_stock_only"] is True
    assert contract["single_trading_date_only"] is True

    assert contract["allow_normalization"] is False
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

    assert contract["dataset"] == "TaiwanStockPrice"

    print(
        "CONTROLLED REAL SAMPLE ACQUISITION "
        "CONTRACT V1: PASS"
    )


if __name__ == "__main__":
    main()
