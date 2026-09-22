import importlib
import sys


FORBIDDEN_OUTPUT_KEYS = {
    "decision",
    "risk",
    "action",
    "buy6",
    "sell6",
    "chip_score",
    "institutional_resonance",
}


def fail(message: str) -> int:
    print(f"[FAIL] {message}")
    return 1


def main() -> int:
    print("=== GATE 22 - NORMALIZED CHIP DATA CONTRACT V1 ===")

    try:
        module = importlib.import_module("v14.chip_contract")
    except ModuleNotFoundError:
        return fail("implementation missing: v14.chip_contract")

    fn = getattr(module, "normalize_chip_data", None)
    if not callable(fn):
        return fail("normalize_chip_data() missing or not callable")

    # Golden Fixture A:
    # Raw evidence only. Values are synthetic contract fixtures,
    # not real market data and not source-unit assertions.
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
        "metadata": {
            "source": "GOLDEN_FIXTURE",
            "freshness": "FINAL",
        },
    }

    actual = fn(raw)

    if not isinstance(actual, dict):
        return fail("normalized result must be dict")

    # Contract 1: Identity must be preserved.
    identity = actual.get("identity")
    if not isinstance(identity, dict):
        return fail("identity missing")

    expected_identity = {
        "code": "2330",
        "market": "TW",
        "trade_date": "2026-09-21",
    }
    for key, value in expected_identity.items():
        if identity.get(key) != value:
            return fail(f"identity mismatch: {key}")

    print("[PASS] identity preserved")

    # Contract 2: Institutional categories must remain separated.
    institutional = actual.get("institutional")
    if not isinstance(institutional, dict):
        return fail("institutional block missing")

    required_institutional = {
        "foreign",
        "investment_trust",
        "dealer_self",
        "dealer_hedging",
    }
    if not required_institutional.issubset(institutional.keys()):
        return fail("institutional categories lost or merged")

    if institutional["dealer_self"] == institutional["dealer_hedging"]:
        return fail("dealer_self and dealer_hedging must remain distinct")

    print("[PASS] institutional categories preserved")

    # Contract 3: Metadata is mandatory.
    metadata = actual.get("metadata")
    if not isinstance(metadata, dict):
        return fail("metadata missing")

    for key in ("source", "freshness", "status", "missing_fields"):
        if key not in metadata:
            return fail(f"metadata field missing: {key}")

    print("[PASS] metadata contract preserved")

    # Contract 4: Missing must never become zero or neutral.
    raw_missing = {
        "code": "2330",
        "market": "TW",
        "trade_date": "2026-09-21",
        "institutional": {
            "foreign": None,
            "investment_trust": {"buy": 300, "sell": 100},
            "dealer_self": {"buy": 90, "sell": 40},
            "dealer_hedging": {"buy": 60, "sell": 80},
        },
        "metadata": {
            "source": "GOLDEN_FIXTURE",
            "freshness": "FINAL",
        },
    }

    missing_result = fn(raw_missing)
    missing_inst = missing_result.get("institutional", {})
    missing_meta = missing_result.get("metadata", {})

    if missing_inst.get("foreign") in (0, {"buy": 0, "sell": 0}):
        return fail("missing foreign data was converted to zero")

    if missing_meta.get("status") != "MISSING":
        return fail("missing chip data must set status=MISSING")

    if "institutional.foreign" not in missing_meta.get("missing_fields", []):
        return fail("missing_fields must include institutional.foreign")

    print("[PASS] missing != zero != neutral")

    # Contract 5: Contract layer must not emit derived signals.
    forbidden_found = FORBIDDEN_OUTPUT_KEYS.intersection(actual.keys())
    if forbidden_found:
        return fail(
            "contract emitted forbidden derived outputs: "
            + ",".join(sorted(forbidden_found))
        )

    print("[PASS] raw evidence / derived-signal boundary preserved")

    # Contract 6: No Core / Risk / Action mutation contract.
    forbidden_nested = {"decision", "risk", "action", "buy6", "sell6"}
    for block_name, block in actual.items():
        if isinstance(block, dict):
            found = forbidden_nested.intersection(block.keys())
            if found:
                return fail(
                    f"forbidden keys in {block_name}: "
                    + ",".join(sorted(found))
                )

    print("[PASS] Core / Risk / Action boundary preserved")

    print("=== GATE 22 RESULT: PASS ===")
    return 0


if __name__ == "__main__":
    sys.exit(main())
