import json
from pathlib import Path

from v14.core_engine import calculate_action


CONTRACT_PATH = (
    Path(__file__).resolve().parent
    / "golden_action_cases_v1.json"
)


print("=" * 72)
print("DAVID V14 - GATE 5 ACTION GOLDEN COMPARATOR")
print("=" * 72)

with CONTRACT_PATH.open("r", encoding="utf-8") as f:
    contract = json.load(f)

if contract.get("contract_version") != "V14_ACTION_V1":
    print(
        "[FAIL] Golden Action Contract version:",
        contract.get("contract_version"),
    )
    raise SystemExit(1)

print("[PASS] Golden Action Contract loaded: V14_ACTION_V1")

cases = contract.get("cases", [])

if len(cases) != 18:
    print(f"[FAIL] Expected 18 Golden Action Cases, got {len(cases)}")
    raise SystemExit(1)

print("[PASS] 18 Golden Action Cases loaded")
print("[PASS] calculate_action() detected")
print()

passed = 0
failed = 0

for case in cases:
    case_id = case["id"]

    risk = {
        "version": "V14_RISK_V1",
        "state": case.get("risk_state"),
        "level": case.get("risk_level"),
        "lock": case.get("risk_lock"),
        "factors": {
            "R3_CONFLICT": {
                "level": case.get("r3_conflict")
            },
            "R4_DECISION_POSITION": {
                "state": case.get("r4_decision_position")
            },
            "R5_VOLUME_PRICE": {
                "state": case.get("r5_volume_price")
            },
        },
    }

    result = calculate_action(
        decision=case.get("decision"),
        risk=risk,
        position_context=case.get("position_context"),
    )

    expected = case.get("expected_signal")
    actual = result.get("signal")

    if actual == expected:
        print(f"[PASS] {case_id}")
        passed += 1
    else:
        print(
            f"[FAIL] {case_id}: "
            f"expected={expected!r}, actual={actual!r}"
        )
        failed += 1


print()
print("-" * 72)
print(f"RESULT: {passed}/18 PASS | {failed}/18 FAIL")
print("-" * 72)

if failed:
    print("GATE 5 RESULT: EXPECTED RED")
    print("V14_ACTION_V1 IMPLEMENTATION NOT COMPLETE")
    raise SystemExit(1)

print("GATE 5 RESULT: PASS")
print("V14_ACTION_V1 GOLDEN CONTRACT VERIFIED")