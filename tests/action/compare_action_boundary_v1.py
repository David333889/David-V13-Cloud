import json
from pathlib import Path

from v14.core_engine import calculate_action


CONTRACT_PATH = (
    Path(__file__).resolve().parent
    / "golden_action_boundary_cases_v1.json"
)


def build_input(mode):
    if mode == "UNKNOWN_DECISION":
        return {
            "decision": "UNSUPPORTED_TEST_VALUE",
            "risk": {
                "version": "V14_RISK_V1",
                "state": "READY",
                "level": "LOW",
                "lock": "CLEAR",
                "factors": {},
            },
            "position_context": "SUPPORT",
        }

    if mode == "RISK_NONE":
        return {
            "decision": "BULLISH",
            "risk": None,
            "position_context": "SUPPORT",
        }

    if mode == "RISK_EMPTY":
        return {
            "decision": "BULLISH",
            "risk": {},
            "position_context": "SUPPORT",
        }

    raise ValueError(f"Unsupported boundary mode: {mode}")


def main():
    print("=" * 72)
    print("DAVID V14 - ACTION BOUNDARY V1 COMPARATOR")
    print("=" * 72)

    with CONTRACT_PATH.open("r", encoding="utf-8") as f:
        contract = json.load(f)

    version = contract.get("contract_version")

    if version != "V14_ACTION_BOUNDARY_V1":
        print(f"[FAIL] Unexpected contract version: {version}")
        return 1

    print("[PASS] Boundary Contract loaded: V14_ACTION_BOUNDARY_V1")

    cases = contract.get("cases", [])

    if len(cases) != 3:
        print(f"[FAIL] Expected 3 Boundary Cases, got {len(cases)}")
        return 1

    print("[PASS] 3 Boundary Cases loaded")
    print("[PASS] calculate_action() detected")
    print()

    passed_count = 0
    failed_count = 0

    for case in cases:
        case_id = case["id"]

        try:
            inputs = build_input(case.get("mode"))

            result = calculate_action(
                decision=inputs["decision"],
                risk=inputs["risk"],
                position_context=inputs["position_context"],
            )

            expected = {
                "state": case.get("expected_state"),
                "signal": case.get("expected_signal"),
                "reason": case.get("expected_reason"),
            }

            actual = {
                "state": result.get("state"),
                "signal": result.get("signal"),
                "reason": result.get("reason"),
            }

            if actual == expected:
                print(f"[PASS] {case_id}")
                passed_count += 1
            else:
                print(
                    f"[FAIL] {case_id}: "
                    f"expected={expected!r}, actual={actual!r}"
                )
                failed_count += 1

        except Exception as exc:
            print(
                f"[FAIL] {case_id}: "
                f"{type(exc).__name__}: {exc}"
            )
            failed_count += 1

    print()
    print("-" * 72)
    print(
        f"RESULT: {passed_count}/3 PASS | "
        f"{failed_count}/3 FAIL"
    )
    print("-" * 72)

    if failed_count:
        print("ACTION BOUNDARY V1 RESULT: FAIL")
        return 1

    print("ACTION BOUNDARY V1 RESULT: PASS")
    print("V14_ACTION_BOUNDARY_V1 CONTRACT VERIFIED")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())