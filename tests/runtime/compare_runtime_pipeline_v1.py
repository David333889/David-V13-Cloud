from pathlib import Path
import copy
import sys


ROOT = Path(__file__).resolve().parents[2]

if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))


def passed(message):
    print(f"[PASS] {message}")
    return True


def fail(message):
    print(f"[FAIL] {message}")
    return False

def build_runtime_valid_result():
    result = copy.deepcopy(build_valid_result())

    result["six_buy"]["score"] = 5
    result["six_sell"]["score"] = 1
    result["position"]["fib_position"] = "0.618"
    result["decision"]["core_decision"] = "BULLISH"

    return result

def build_valid_identity():
    return {
        "trade_date": "2026-09-20",
        "code": "2330",
        "name": "TEST",
        "market": "TW",
        "symbol": "2330.TW",
    }

from pathlib import Path
import sys

from tests.consumer.compare_consumer_boundary_v1 import (
    build_valid_result,
)


def main():
    print("=" * 72)
    print("DAVID V14 - RUNTIME PIPELINE V1 COMPARATOR")
    print("=" * 72)

    try:
        from v14.runtime_pipeline import build_runtime_persistence
    except (ImportError, ModuleNotFoundError) as exc:
        print("[FAIL] Runtime Pipeline V1 implementation not found")
        print(f"[INFO] {exc}")
        print("RUNTIME PIPELINE V1 RESULT: FAIL")
        return 1

    if not callable(build_runtime_persistence):
        print("[FAIL] build_runtime_persistence() is not callable")
        return 1

    passed("build_runtime_persistence() detected")

    result = build_runtime_valid_result()
    identity = build_valid_identity()

    try:
        actual = build_runtime_persistence(
            result,
            identity,
        )
    except Exception as exc:
        print(
            f"[FAIL] build_runtime_persistence() raised "
            f"{type(exc).__name__}: {exc}"
        )
        return 1

    if not isinstance(actual, dict):
        print("[FAIL] Runtime Pipeline result is not dict")
        return 1

    state = actual.get("state")
    reason = actual.get("reason")
    row = actual.get("row")

    if state != "READY":
        print(f"[FAIL] Expected state READY, got: {state}")
        return 1

    passed("Runtime Pipeline State = READY")

    if reason != "PERSISTENCE_ROW_OK":
        print(
            "[FAIL] Expected reason PERSISTENCE_ROW_OK, "
            f"got: {reason}"
        )
        return 1

    passed("Runtime Pipeline Reason = PERSISTENCE_ROW_OK")

    if not isinstance(row, dict):
        print("[FAIL] Persistence row missing")
        return 1

    passed("Persistence Row detected")

    expected_identity = build_valid_identity()

    for key, expected_value in expected_identity.items():
        actual_value = row.get(key)

        if actual_value != expected_value:
            print(
                f"[FAIL] Identity mismatch: {key} "
                f"expected={expected_value!r} "
                f"actual={actual_value!r}"
            )
            return 1

    passed("Identity preserved")

    required_safety_fields = (
        "payload_version",
        "engine_version",
        "baseline_version",
        "risk_state",
        "risk_level",
        "risk_lock",
        "action_state",
        "action_signal",
        "action_reason",
        "action_risk_guard",
        "action_confidence",
        "consumer_state",
    )

    missing = [
        key
        for key in required_safety_fields
        if key not in row
    ]

    if missing:
        print(f"[FAIL] Missing Version/Safety fields: {missing}")
        return 1

    passed("Version/Safety fields detected")

    print("-" * 72)
    print("RUNTIME PIPELINE V1 RESULT: PASS")
    print("NO WRITER | NO CLIENT | NO NETWORK I/O")
    return 0


if __name__ == "__main__":
    sys.exit(main())
