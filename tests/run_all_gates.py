import subprocess
import sys


def run_gate(name, command):
    print()
    print("=" * 70)
    print(f"RUNNING: {name}")
    print("=" * 70)

    result = subprocess.run(command)

    if result.returncode == 0:
        print(f"[PASS] {name}")
        return True

    print(f"[FAIL] {name} | return code = {result.returncode}")
    return False


def main():
    print("=" * 70)
    print("DAVID V14 - UNIFIED REGRESSION RUNNER")
    print("=" * 70)

    results = []

    results.append(
        run_gate(
            "GATE 3 - CORE BASELINE",
            [sys.executable, r"tests\compare_v13_v14.py"],
        )
    )

    results.append(
        run_gate(
            "GATE 4 - RISK ENGINE",
            [sys.executable, r"tests\risk\compare_risk_v1.py"],
        )
    )

    results.append(
        run_gate(
            "GATE 5 - ACTION ENGINE",
            [sys.executable, "-m", "tests.action.compare_action_v1"],
        )
    )
    results.append(
        run_gate(
            "ACTION BOUNDARY V1",
            [sys.executable, "-m", "tests.action.compare_action_boundary_v1"],
        )
    )

    results.append(
        run_gate(
            "CONTRACT REGISTRY V1",
            [sys.executable, "-m", "tests.contracts.verify_contract_registry_v1"],
        )
    )

    results.append(
        run_gate(
            "E2E - FULL CORE WIRING",
            [sys.executable, "-m", "tests.e2e.compare_e2e_v1"],
        )
    )
    print()
    print("=" * 70)
    print("V14 REGRESSION SUMMARY")
    print("=" * 70)

    gate_names = [
        "GATE 3 - CORE BASELINE",
        "GATE 4 - RISK ENGINE",
        "GATE 5 - ACTION ENGINE",
        "ACTION BOUNDARY V1",
        "CONTRACT REGISTRY V1",
        "E2E - FULL CORE WIRING",
    ]

    for name, passed in zip(gate_names, results):
        status = "PASS" if passed else "FAIL"
        print(f"{name}: {status}")

    print("=" * 70)

    if all(results):
        print("V14 REGRESSION RESULT: PASS")
        return 0

    print("V14 REGRESSION RESULT: FAIL")
    return 1


if __name__ == "__main__":
    sys.exit(main())