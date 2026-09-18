import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from v14 import core_engine


CONTRACT_FILE = Path(__file__).with_name("golden_risk_cases_v1.json")


def build_inputs(case_input):
    decision = {
        "decision": case_input.get("decision")
    }

    six_buy = {
        "score": case_input.get("buy_score")
    }

    six_sell = {
        "score": case_input.get("sell_score")
    }

    technical = {
        "bias_pct": case_input.get("bias_pct")
    }

    position = {
        "position_context": case_input.get("position_context")
    }

    return decision, six_buy, six_sell, technical, position


def compare_case(case, actual):
    expected = case["expected"]

    keys = ("state", "level", "lock")
    mismatches = []

    for key in keys:
        expected_value = expected.get(key)
        actual_value = actual.get(key)

        if actual_value != expected_value:
            mismatches.append(
                f"{key}: expected={expected_value!r}, actual={actual_value!r}"
            )

    return mismatches


def main():
    print("=" * 72)
    print("DAVID V14 - GATE 4 RISK GOLDEN COMPARATOR")
    print("=" * 72)

    with CONTRACT_FILE.open("r", encoding="utf-8") as f:
        contract = json.load(f)

    version = contract.get("contract_version")
    cases = contract.get("cases", [])

    if version != "V14_RISK_V1":
        print(f"[FAIL] Unexpected contract version: {version}")
        return 1

    print(f"[PASS] Golden Risk Contract loaded: {version}")

    ids = [case.get("id") for case in cases]
    expected_ids = [f"G{i:02d}" for i in range(1, 13)]

    if len(cases) != 12 or ids != expected_ids:
        print(f"[FAIL] Golden Risk Cases invalid: {ids}")
        return 1

    print("[PASS] 12 Golden Risk Cases loaded")

    calculate_risk = getattr(core_engine, "calculate_risk", None)

    if not callable(calculate_risk):
        print("[FAIL] calculate_risk() not implemented")
        return 1

    print("[PASS] calculate_risk() detected")
    print()

    passed = 0
    failed = 0

    for case in cases:
        case_id = case["id"]
        case_input = case["input"]

        decision, six_buy, six_sell, technical, position = build_inputs(
            case_input
        )

        actual = calculate_risk(
            decision=decision,
            six_buy=six_buy,
            six_sell=six_sell,
            technical=technical,
            position=position,
        )

        mismatches = compare_case(case, actual)

        if mismatches:
            failed += 1
            print(f"[FAIL] {case_id}")
            for mismatch in mismatches:
                print(f"       {mismatch}")
        else:
            passed += 1
            print(f"[PASS] {case_id}")

    print()
    print("-" * 72)
    print(f"RESULT: {passed}/12 PASS | {failed}/12 FAIL")
    print("-" * 72)

    if failed:
        print("GATE 4 RESULT: FAIL")
        print("RISK IMPLEMENTATION NOT YET GOLDEN VERIFIED")
        return 1

    print("GATE 4 RESULT: PASS")
    print("V14_RISK_V1 GOLDEN CONTRACT VERIFIED")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())