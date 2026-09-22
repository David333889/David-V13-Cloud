import sys

from v14.chip_contract import normalize_chip_data


def fail(message: str) -> int:
    print(f"[FAIL] {message}")
    return 1


def main() -> int:
    print("=== GATE 22 - CHIP EVIDENCE CONTRACT V1 ===")

    raw = {
        "code": "2330",
        "market": "TW",
        "trade_date": "2026-09-21",
        "institutional": {
            "foreign": {"buy": 1200, "sell": 700},
            "investment_trust": {"buy": 300, "sell": 100},
            "dealer_self": {"buy": 90, "sell": 40},
            "dealer_hedging": {"buy": 60, "sell": 80},
        },
        "financing": {
            "margin": {
                "today_balance": 1000,
                "yesterday_balance": 900,
                "buy": 120,
                "sell": 80,
                "cash_repayment": 10,
            },
            "short": {
                "today_balance": 200,
                "yesterday_balance": 180,
                "buy": 30,
                "sell": 40,
                "cash_repayment": 5,
            },
            "offset_loan_and_short": 15,
        },
        "securities_lending": {
            "transaction_type": "FIXTURE_TYPE",
            "volume": 500,
            "fee_rate": 1.25,
        },
        "day_trade": {
            "volume": 600,
            "buy_amount": 100000,
            "sell_amount": 101000,
            "buy_after_sale": True,
        },
        "metadata": {
            "source": "GOLDEN_FIXTURE",
            "freshness": "FINAL",
        },
    }

    actual = normalize_chip_data(raw)

    if actual.get("financing") != raw["financing"]:
        return fail("financing evidence missing or changed")
    print("[PASS] financing evidence preserved")

    if actual.get("securities_lending") != raw["securities_lending"]:
        return fail("securities lending evidence missing or changed")
    print("[PASS] securities lending transaction evidence preserved")

    if actual.get("day_trade") != raw["day_trade"]:
        return fail("day-trade evidence missing or changed")
    print("[PASS] day-trade evidence preserved")

    forbidden = {
        "margin_change",
        "short_change",
        "lending_trend",
        "day_trade_ratio",
        "chip_score",
        "institutional_resonance",
    }

    if forbidden.intersection(actual.keys()):
        return fail("derived chip metric emitted by contract layer")

    print("[PASS] derived metrics remain outside contract layer")

    # Missing evidence must remain Missing.
    raw_missing = {
        "code": "2330",
        "market": "TW",
        "trade_date": "2026-09-21",
        "institutional": {
            "foreign": {"buy": 1200, "sell": 700},
            "investment_trust": {"buy": 300, "sell": 100},
            "dealer_self": {"buy": 90, "sell": 40},
            "dealer_hedging": {"buy": 60, "sell": 80},
        },
        "financing": None,
        "securities_lending": None,
        "day_trade": None,
        "metadata": {
            "source": "GOLDEN_FIXTURE",
            "freshness": "FINAL",
        },
    }

    missing = normalize_chip_data(raw_missing)
    metadata = missing.get("metadata", {})
    missing_fields = metadata.get("missing_fields", [])

    if missing.get("financing") is not None:
        return fail("missing financing must remain None")

    if missing.get("securities_lending") is not None:
        return fail("missing securities lending must remain None")

    if missing.get("day_trade") is not None:
        return fail("missing day-trade must remain None")

    if metadata.get("status") != "MISSING":
        return fail("missing evidence must set status=MISSING")

    required_missing = {
        "financing",
        "securities_lending",
        "day_trade",
    }

    if not required_missing.issubset(set(missing_fields)):
        return fail("missing_fields incomplete")

    print("[PASS] financing / lending / day-trade missing != zero")

    print("=== GATE 22 CHIP EVIDENCE RESULT: PASS ===")
    return 0


if __name__ == "__main__":
    sys.exit(main())
