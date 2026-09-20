from pathlib import Path
import copy
import json
import sys


ROOT = Path(__file__).resolve().parents[2]

CONTRACT_FILE = (
    ROOT
    / "tests"
    / "integration"
    / "golden_integration_payload_cases_v1.json"
)


def build_valid_result():
    return {
        "engine_version": "V14_UNIFIED",
        "baseline_version": "V13.100",
        "six_buy": {
            "score": 5,
        },
        "six_sell": {
            "score": 1,
        },
        "position": {
            "fib_position": "0.618",
        },
        "decision": {
            "core_decision": "BULLISH",
        },
        "risk": {
            "state": "READY",
            "level": "LOW",
            "lock": "CLEAR",
        },
        "action": {
            "state": "READY",
            "signal": "WAIT",
            "reason": "NEUTRAL_DECISION",
            "risk_guard": "CLEAR",
            "confidence": "NORMAL",
        },
    }


def build_valid_consumer():
    return {
        "version": "V14_CONSUMER_BOUNDARY_V1",
        "state": "READY",
        "reason": "CONTRACT_OK",
    }


def build_valid_identity():
    return {
        "trade_date": "2026-09-20",
        "code": "2330",
        "name": "TEST",
        "market": "TW",
        "symbol": "2330.TW",
    }


def build_case_input(mode):
    result = build_valid_result()
    consumer = build_valid_consumer()
    identity = build_valid_identity()

    if mode == "VALID_READY":
        return result, consumer, identity

    if mode == "INVALID_RESULT_TYPE":
        return None, consumer, identity

    if mode == "CONSUMER_BLOCKED":
        consumer["state"] = "BLOCKED"
        consumer["reason"] = "INVALID_RESULT_TYPE"
        return result, consumer, identity

    if mode == "IDENTITY_MISSING":
        identity.pop("code", None)
        return result, consumer, identity

    if mode == "BUY_SCORE_MISSING":
        result["six_buy"] = copy.deepcopy(result["six_buy"])
        result["six_buy"].pop("score", None)
        return result, consumer, identity

    if mode == "SELL_SCORE_MISSING":
        result["six_sell"] = copy.deepcopy(result["six_sell"])
        result["six_sell"].pop("score", None)
        return result, consumer, identity

    if mode == "FIB_POSITION_MISSING":
        result["position"] = copy.deepcopy(result["position"])
        result["position"].pop("fib_position", None)
        return result, consumer, identity

    if mode == "DECISION_MISSING":
        result["decision"] = copy.deepcopy(result["decision"])
        result["decision"].pop("core_decision", None)
        return result, consumer, identity

    if mode == "RISK_MAPPING_MISSING":
        result["risk"] = copy.deepcopy(result["risk"])
        result["risk"].pop("level", None)
        return result, consumer, identity

    if mode == "ACTION_MAPPING_MISSING":
        result["action"] = copy.deepcopy(result["action"])
        result["action"].pop("signal", None)
        return result, consumer, identity

    raise ValueError(f"Unsupported mode: {mode}")


def main():
    print("=" * 72)
    print("DAVID V14 - INTEGRATION PAYLOAD V1 COMPARATOR")
    print("=" * 72)

    if not CONTRACT_FILE.exists():
        print("[FAIL] Integration Golden Contract not found")
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

    if version != "V14_INTEGRATION_PAYLOAD_V1":
        print(f"[FAIL] Unexpected contract version: {version}")
        return 1

    print(f"[PASS] Golden Integration Contract loaded: {version}")

    if spec_status != "FROZEN":
        print(f"[FAIL] Spec status is not FROZEN: {spec_status}")
        return 1

    print("[PASS] Spec Status = FROZEN")

    if not isinstance(cases, list) or len(cases) != 10:
        count = len(cases) if isinstance(cases, list) else "INVALID"
        print(f"[FAIL] Expected 10 Golden Cases, got: {count}")
        return 1

    print("[PASS] 10 Golden Integration Payload Cases loaded")

    try:
        from v14.integration_payload import build_integration_payload
    except (ImportError, ModuleNotFoundError) as exc:
        print("[FAIL] Integration Payload implementation not found")
        print(f"[INFO] {exc}")
        return 1

    if not callable(build_integration_payload):
        print("[FAIL] build_integration_payload() is not callable")
        return 1

    print("[PASS] build_integration_payload() detected")
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
            result, consumer, identity = build_case_input(mode)

            actual = build_integration_payload(
                result,
                consumer,
                identity,
            )
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
    print(f"RESULT: {passed}/10 PASS | {failed}/10 FAIL")
    print("-" * 72)

    if failed == 0:
        print("INTEGRATION PAYLOAD V1 RESULT: PASS")
        print("V14_INTEGRATION_PAYLOAD_V1 CONTRACT VERIFIED")
        return 0

    print("INTEGRATION PAYLOAD V1 RESULT: FAIL")
    return 1


if __name__ == "__main__":
    sys.exit(main())