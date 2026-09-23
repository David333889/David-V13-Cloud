import sys

from v14.chip_source_adapter import adapt_chip_source_data
from v14.chip_contract import normalize_chip_data


def fail(message: str) -> int:
    print(f"[FAIL] {message}")
    return 1


def main() -> int:
    print("=== GATE 25 - CHIP SOURCE COMPATIBILITY CONTRACT V1 ===")

    # Case A: Missing source blocks must remain Missing, never fabricated as zero.
    missing_fixture = {
        "code": "2330",
        "market": "TW",
        "trade_date": "2026-09-23",
        "institutional": {},
        "financing": None,
        "securities_lending": None,
        "day_trade": None,
        "metadata": {
            "source": "GOLDEN_FIXTURE",
            "freshness": "FINAL",
        },
    }

    canonical = adapt_chip_source_data(missing_fixture)
    normalized = normalize_chip_data(canonical)

    if canonical["financing"] is not None:
        return fail("missing financing was fabricated")

    if canonical["securities_lending"] is not None:
        return fail("missing securities lending was fabricated")

    if canonical["day_trade"] is not None:
        return fail("missing day-trade was fabricated")

    if normalized["metadata"]["status"] != "MISSING":
        return fail("missing evidence did not propagate to status=MISSING")

    print("[PASS] missing dataset != zero")

    # Case B: Explicit zero is valid evidence and must survive.
    zero_fixture = {
        "code": "2330",
        "market": "TW",
        "trade_date": "2026-09-23",
        "institutional": {
            "Foreign_Investor": {"buy": 0, "sell": 0},
            "Investment_Trust": {"buy": 0, "sell": 0},
            "Dealer_self": {"buy": 0, "sell": 0},
            "Dealer_Hedging": {"buy": 0, "sell": 0},
        },
        "financing": {},
        "securities_lending": {},
        "day_trade": {},
        "metadata": {
            "source": "GOLDEN_FIXTURE",
            "freshness": "FINAL",
        },
    }

    zero = adapt_chip_source_data(zero_fixture)

    if zero["institutional"]["foreign"] != {"buy": 0, "sell": 0}:
        return fail("explicit institutional zero was not preserved")

    print("[PASS] explicit zero preserved")

    # Case C: Unknown units must not trigger conversion.
    unit_fixture = {
        "code": "2330",
        "market": "TW",
        "trade_date": "2026-09-23",
        "institutional": {
            "Foreign_Investor": {"buy": 123, "sell": 45},
        },
        "financing": {"MarginPurchaseTodayBalance": 456},
        "securities_lending": {"volume": 789},
        "day_trade": {"Volume": 321},
        "metadata": {
            "source": "GOLDEN_FIXTURE",
            "freshness": "FINAL",
        },
    }

    unit = adapt_chip_source_data(unit_fixture)

    if unit["institutional"]["foreign"]["buy"] != 123:
        return fail("unknown institutional unit was converted")

    if unit["financing"]["MarginPurchaseTodayBalance"] != 456:
        return fail("unknown financing unit was converted")

    if unit["securities_lending"]["volume"] != 789:
        return fail("unknown lending unit was converted")

    if unit["day_trade"]["Volume"] != 321:
        return fail("unknown day-trade unit was converted")

    print("[PASS] unknown unit remains unconverted")

    # Case D: Legacy Dealer exists, but target semantics are not yet authorized.
    legacy_fixture = {
        "code": "2330",
        "market": "TW",
        "trade_date": "LEGACY_DATE",
        "institutional": {
            "Dealer": {"buy": 70, "sell": 20},
        },
        "metadata": {
            "source": "GOLDEN_FIXTURE",
            "freshness": "FINAL",
        },
    }

    legacy = adapt_chip_source_data(legacy_fixture)

    if legacy["institutional"]["dealer_self"] is not None:
        return fail("legacy Dealer was guessed as dealer_self")

    if legacy["institutional"]["dealer_hedging"] is not None:
        return fail("legacy Dealer was guessed as dealer_hedging")

    print("[PASS] legacy Dealer not falsely classified")

    print("=== GATE 25 CHIP SOURCE COMPATIBILITY RESULT: PASS ===")
    return 0


if __name__ == "__main__":
    sys.exit(main())
