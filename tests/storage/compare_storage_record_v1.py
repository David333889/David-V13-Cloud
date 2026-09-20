from pathlib import Path
import copy
import json
import sys


ROOT = Path(__file__).resolve().parents[2]

CONTRACT_FILE = (
    ROOT
    / "tests"
    / "storage"
    / "golden_storage_record_cases_v1.json"
)


def build_valid_integration_result():
    return {
        "version": "V14_INTEGRATION_PAYLOAD_V1",
        "state": "READY",
        "reason": "PAYLOAD_OK",
        "payload": {
            "metadata": {
                "payload_version": "V14_INTEGRATION_PAYLOAD_V1",
                "engine_version": "V14_UNIFIED",
                "baseline_version": "V13.100",
            },
            "identity": {
                "trade_date": "2026-09-20",
                "code": "2330",
                "name": "TEST",
                "market": "TW",
                "symbol": "2330.TW",
            },
            "core": {
                "buy_score": 5,
                "sell_score": 1,
                "fib_position": "0.618",
                "decision": "BULLISH",
            },
            "safety": {
                "risk_state": "READY",
                "risk_level": "LOW",
                "risk_lock": "CLEAR",
                "action_state": "READY",
                "action_signal": "WAIT",
                "action_reason": "NEUTRAL_DECISION",
                "action_risk_guard": "CLEAR",
                "action_confidence": "NORMAL",
                "consumer_state": "READY",
            },
        },
    }


def build_case_input(mode):
    integration_result = build_valid_integration_result()

    if mode == "VALID_READY":
        return integration_result

    if mode == "INVALID_RESULT_TYPE":
        return None

    if mode == "INTEGRATION_NOT_READY":
        integration_result["state"] = "BLOCKED"
        integration_result["reason"] = "CONSUMER_NOT_READY"
        return integration_result

    if mode == "PAYLOAD_MISSING":
        integration_result.pop("payload", None)
        return integration_result

    if mode == "METADATA_MISSING":
        integration_result = copy.deepcopy(integration_result)
        integration_result["payload"].pop("metadata", None)
        return integration_result

    if mode == "IDENTITY_MISSING":
        integration_result = copy.deepcopy(integration_result)
        integration_result["payload"].pop("identity", None)
        return integration_result

    if mode == "CORE_MISSING":
        integration_result = copy.deepcopy(integration_result)
        integration_result["payload"].pop("core", None)
        return integration_result

    if mode == "SAFETY_MISSING":
        integration_result = copy.deepcopy(integration_result)
        integration_result["payload"].pop("safety", None)
        return integration_result

    raise ValueError(f"Unsupported mode: {mode}")


def main():
    print("=" * 72)
    print("DAVID V14 - STORAGE RECORD V1 COMPARATOR")
    print("=" * 72)

    if not CONTRACT_FILE.exists():
        print("[FAIL] Storage Golden Contract not found")
        return 1

    try:
        with CONTRACT_FILE.open("r", encoding="utf-8") as f:
            contract = json.load(f)
    except Exception as exc:
        print(f"[FAIL] Golden Contract load failed: {exc}")
        return 1

    version = contract.get("contract_version")
    spec_status = contract.get("spec_status")
    source_contract = contract.get("source_contract")
    cases = contract.get("cases")

    if version != "V14_STORAGE_RECORD_V1":
        print(f"[FAIL] Unexpected contract version: {version}")
        return 1

    print(f"[PASS] Golden Storage Contract loaded: {version}")

    if spec_status != "FROZEN":
        print(f"[FAIL] Spec status is not FROZEN: {spec_status}")
        return 1

    print("[PASS] Spec Status = FROZEN")

    if source_contract != "V14_INTEGRATION_PAYLOAD_V1":
        print(f"[FAIL] Unexpected source contract: {source_contract}")
        return 1

    print("[PASS] Source Contract = V14_INTEGRATION_PAYLOAD_V1")

    if not isinstance(cases, list) or len(cases) != 8:
        count = len(cases) if isinstance(cases, list) else "INVALID"
        print(f"[FAIL] Expected 8 Golden Cases, got: {count}")
        return 1

    print("[PASS] 8 Golden Storage Record Cases loaded")

    try:
        from v14.storage_adapter import build_storage_record
    except (ImportError, ModuleNotFoundError) as exc:
        print("[FAIL] Storage Adapter implementation not found")
        print(f"[INFO] {exc}")
        return 1

    if not callable(build_storage_record):
        print("[FAIL] build_storage_record() is not callable")
        return 1

    print("[PASS] build_storage_record() detected")
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
            integration_result = build_case_input(mode)
            actual = build_storage_record(integration_result)
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
        print("STORAGE RECORD V1 RESULT: PASS")
        print("V14_STORAGE_RECORD_V1 CONTRACT VERIFIED")
        return 0

    print("STORAGE RECORD V1 RESULT: FAIL")
    return 1


if __name__ == "__main__":
    sys.exit(main())