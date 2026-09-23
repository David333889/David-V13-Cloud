from pathlib import Path
import sys


ROOT = Path(__file__).resolve().parents[2]
ADAPTER = ROOT / "V14" / "chip_source_adapter.py"


def fail(message: str) -> int:
    print(f"[FAIL] {message}")
    return 1


def main() -> int:
    print("=== GATE 24 - CHIP SOURCE ADAPTER V1 ===")

    # Expected RED boundary:
    # Gate 24 implementation must exist before behavioral tests can run.
    if not ADAPTER.exists():
        return fail("chip source adapter implementation missing")

    from v14.chip_source_adapter import adapt_chip_source_data

    fixture = {
        "code": "2330",
        "market": "TWSE",
        "trade_date": "2026-09-22",
        "institutional": {
            "Foreign_Investor": {"buy": 1000, "sell": 800},
            "Investment_Trust": {"buy": 200, "sell": 100},
            "Dealer_self": {"buy": 0, "sell": 50},
            "Dealer_Hedging": {"buy": 30, "sell": 0},
        },
        "financing": {
            "MarginPurchaseTodayBalance": 5000,
            "ShortSaleTodayBalance": 300,
            "OffsetLoanAndShort": 0,
        },
        "securities_lending": {
            "transaction_type": "lend",
            "volume": 100,
            "fee_rate": 0.5,
        },
        "day_trade": {
            "Volume": 2000,
            "BuyAmount": 1000000,
            "SellAmount": 990000,
            "BuyAfterSale": 1,
        },
        "metadata": {
            "source": "GOLDEN_FIXTURE",
            "freshness": "FINAL",
        },
    }

    result = adapt_chip_source_data(fixture)

    required_top_level = [
        "code",
        "market",
        "trade_date",
        "institutional",
        "financing",
        "securities_lending",
        "day_trade",
        "metadata",
    ]

    for key in required_top_level:
        if key not in result:
            return fail(f"canonical raw key missing: {key}")

    print("[PASS] canonical raw top-level structure preserved")

    institutional = result["institutional"]

    expected_institutional = {
        "foreign": {"buy": 1000, "sell": 800},
        "investment_trust": {"buy": 200, "sell": 100},
        "dealer_self": {"buy": 0, "sell": 50},
        "dealer_hedging": {"buy": 30, "sell": 0},
    }

    if institutional != expected_institutional:
        return fail(
            f"institutional mapping mismatch: {institutional!r}"
        )

    print("[PASS] institutional source categories mapped")

    # Real zero must survive mapping.
    if institutional["dealer_self"]["buy"] != 0:
        return fail("real zero was not preserved")

    print("[PASS] real zero preserved")

    # Raw financing evidence must remain raw.
    if result["financing"] != fixture["financing"]:
        return fail("financing raw evidence changed")

    print("[PASS] financing raw evidence preserved")

    # Lending transaction evidence must not become a balance.
    if result["securities_lending"] != fixture["securities_lending"]:
        return fail("securities-lending transaction evidence changed")

    if "balance" in result["securities_lending"]:
        return fail("lending transaction volume incorrectly mapped to balance")

    print("[PASS] lending transaction boundary preserved")

    # Day-trading raw evidence must remain raw.
    if result["day_trade"] != fixture["day_trade"]:
        return fail("day-trading raw evidence changed")

    print("[PASS] day-trading raw evidence preserved")

    # Adapter must not emit derived decision fields.
    forbidden = {
        "chip_score",
        "decision",
        "risk",
        "action",
        "buy_signal",
        "sell_signal",
    }

    if forbidden.intersection(result.keys()):
        return fail("derived signal leaked from source adapter")

    print("[PASS] raw / derived boundary preserved")

    print("=== GATE 24 CHIP SOURCE ADAPTER RESULT: PASS ===")
    return 0


if __name__ == "__main__":
    sys.exit(main())
