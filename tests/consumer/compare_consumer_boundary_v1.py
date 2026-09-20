from pathlib import Path
import copy
import json
import sys


ROOT = Path(__file__).resolve().parents[2]

CONTRACT_FILE = (
    ROOT
    / "tests"
    / "consumer"
    / "golden_consumer_boundary_cases_v1.json"
)


def build_valid_result():
    return {
        "engine_version": "V14_UNIFIED",
        "baseline_version": "V13.100",
        "market_input": {},
        "technical": {},
        "status": {},
        "six_buy": {},
        "six_sell": {},
        "position": {},
        "decision": {},
        "ranking": {},
        "risk": {
            "version": "V14_RISK_V1",
            "state": "READY",
            "level": "LOW",
            "lock": "CLEAR",
            "factors": {},
        },
        "action": {
            "version": "V14_ACTION_V1",
            "state": "READY",
            "signal": "WAIT",
            "reason": "NEUTRAL_DECISION",
            "risk_guard": "CLEAR",
            "confidence": "NORMAL",
        },
    }


def build_case_input(mode):
    result = build_valid_result()

    if mode == "VALID_RESULT":
        return result

    if mode == "INVALID_RESULT_TYPE":
        return None

    if mode == "VERSION_MISSING":
        result.pop("engine_version", None)
        return result

    if mode == "REQUIRED_DOMAIN_MISSING":
        result.pop("decision", None)
        return result

    if mode == "RISK_MISSING":
        result.pop("risk", None)
        return result

    if mode == "RISK_INVALID":
        result["risk"] = copy.deepcopy(result["risk"])
        result["risk"].pop("level", None)
        return result

    if mode == "ACTION_MISSING":
        result.pop("action", None)
        return result

    if mode == "ACTION_INVALID":
        result["action"] = copy.deepcopy(result["action"])
        result["action"].pop("signal", None)
        return result

    raise ValueError(f"Unsupported mode: {mode}")


def main():
    print("=" * 72)
    print("DAVID V14 - GATE 6 CONSUMER BOUNDARY V1 COMPARATOR")
    print("=" * 72)

    if not CONTRACT_FILE.exists():
        print("[FAIL] Gate 6 Golden Contract not found")
        return 1

    try:
        with CONTRACT_FILE.open("r", encoding="utf-8") as f:
            contract = json.load(f)
    except Exception as exc:
        print(f"[FAIL] Golden Contract load failed: {exc}")
        return 1

    version = contract.get("contract_version")
    spec_status = contract.get("spec_status")
    cases = contract.get("cases")

    if version != "V14_CONSUMER_BOUNDARY_V1":
        print(f"[FAIL] Unexpected contract version: {version}")
        return 1

    print(f"[PASS] Golden Consumer Contract loaded: {version}")

    if spec_status != "FROZEN":
        print(f"[FAIL] Spec status is not FROZEN: {spec_status}")
        return 1

    print("[PASS] Spec Status = FROZEN")

    if not isinstance(cases, list) or len(cases) != 8:
        count = len(cases) if isinstance(cases, list) else "INVALID"
        print(f"[FAIL] Expected 8 Golden Cases, got: {count}")
        return 1

    print("[PASS] 8 Golden Consumer Boundary Cases loaded")

    try:
        from v14.consumer_boundary import evaluate_consumer_boundary
    except (ImportError, ModuleNotFoundError) as exc:
        print("[FAIL] Consumer Boundary implementation not found")
        print(f"[INFO] {exc}")
        return 1

    if not callable(evaluate_consumer_boundary):
        print("[FAIL] evaluate_consumer_boundary() is not callable")
        return 1

    print("[PASS] evaluate_consumer_boundary() detected")
    print("-" * 72)

    passed = 0
    failed = 0

    for case in cases:
        case_id = case["id"]
        mode = case["mode"]
        expected = {
            "state": case["expected_state"],
            "reason": case["expected_reason"],
        }

        try:
            case_input = build_case_input(mode)
            actual = evaluate_consumer_boundary(case_input)
        except Exception as exc:
            print(f"[FAIL] {case_id}: exception = {exc}")
            failed += 1
            continue

        actual_core = {
            "state": actual.get("state"),
            "reason": actual.get("reason"),
        }

        if actual_core == expected:
            print(f"[PASS] {case_id}")
            passed += 1
        else:
            print(
                f"[FAIL] {case_id}: "
                f"expected={expected}, actual={actual_core}"
            )
            failed += 1

    print("-" * 72)
    print(f"RESULT: {passed}/8 PASS | {failed}/8 FAIL")
    print("-" * 72)

    if failed == 0:
        print("GATE 6 RESULT: PASS")
        print("V14_CONSUMER_BOUNDARY_V1 CONTRACT VERIFIED")
        return 0

    print("GATE 6 RESULT: FAIL")
    return 1


if __name__ == "__main__":
    sys.exit(main())