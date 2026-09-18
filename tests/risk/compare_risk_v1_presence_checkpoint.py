import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from v14 import core_engine


CONTRACT_FILE = Path(__file__).with_name("golden_risk_cases_v1.json")


def main():
    print("=" * 64)
    print("DAVID V14 - GATE 4 RISK CONTRACT TEST")
    print("=" * 64)

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
        print()
        print("GATE 4 RESULT: EXPECTED FAIL")
        print("RED TEST CONFIRMED")
        return 1

    print("[PASS] calculate_risk() exists")
    print()
    print("GATE 4 RESULT: IMPLEMENTATION DETECTED")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())