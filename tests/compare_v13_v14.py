"""
DAVID V14 Unified Engine
Gate 3 - V13 Golden Oracle vs V14 Core Engine Comparator

Baseline:
    V13.100 Cloud

Purpose:
    Compare the frozen V13.100 Golden Expected Oracle
    against the V14 Unified Core Engine.

IMPORTANT:
    V14 is currently only a skeleton.
    Therefore Gate 3 MUST NOT report PASS until the
    V14 Core Engine produces real Core calculation results.
"""

from __future__ import annotations

import json
import math
import sys

import pandas as pd
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[1]
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))


ROOT = Path(__file__).resolve().parents[1]

EXPECTED_PATH = (
    ROOT
    / "tests"
    / "expected"
    / "golden_real_001.expected.json"
)
FIXTURE_PATH = (
    ROOT
    / "tests"
    / "fixtures"
    / "golden_real_001.csv"
)
ABS_TOL = 1e-8


def load_json(path: Path):
    if not path.exists():
        raise FileNotFoundError(f"Required file not found: {path}")

    with path.open("r", encoding="utf-8") as f:
        return json.load(f)

def load_fixture(path: Path):
    if not path.exists():
        raise FileNotFoundError(f"Required fixture not found: {path}")

    df = pd.read_csv(path)

    required = {"timestamp", "open", "high", "low", "close", "volume"}
    missing = required - set(df.columns)

    if missing:
        raise RuntimeError(
            f"Fixture missing columns: {sorted(missing)}"
        )

    df["timestamp"] = pd.to_datetime(df["timestamp"])

    df = df.rename(
        columns={
            "open": "Open",
            "high": "High",
            "low": "Low",
            "close": "Close",
            "volume": "Volume",
        }
    )

    df = df.set_index("timestamp")

    for col in ["Open", "High", "Low", "Close", "Volume"]:
        df[col] = pd.to_numeric(df[col], errors="raise")

    if len(df) < 60:
        raise RuntimeError("Fixture has fewer than 60 rows.")

    return df
def is_number(value):
    return (
        isinstance(value, (int, float))
        and not isinstance(value, bool)
    )


def values_equal(expected, actual):
    if is_number(expected) and is_number(actual):
        return math.isclose(
            float(expected),
            float(actual),
            rel_tol=0.0,
            abs_tol=ABS_TOL,
        )

    return expected == actual


def compare_value(path, expected, actual, differences):
    if isinstance(expected, dict):
        if not isinstance(actual, dict):
            differences.append(
                f"{path}: expected dict, actual={type(actual).__name__}"
            )
            return

        for key, expected_value in expected.items():
            child_path = f"{path}.{key}" if path else key

            if key not in actual:
                differences.append(
                    f"{child_path}: missing in V14"
                )
                continue

            compare_value(
                child_path,
                expected_value,
                actual[key],
                differences,
            )

        return

    if isinstance(expected, list):
        if not isinstance(actual, list):
            differences.append(
                f"{path}: expected list, actual={type(actual).__name__}"
            )
            return

        if len(expected) != len(actual):
            differences.append(
                f"{path}: list length "
                f"V13={len(expected)} V14={len(actual)}"
            )
            return

        for i, expected_value in enumerate(expected):
            compare_value(
                f"{path}[{i}]",
                expected_value,
                actual[i],
                differences,
            )

        return

    if not values_equal(expected, actual):
        differences.append(
            f"{path}: V13={expected!r} V14={actual!r}"
        )


def main():
    print("=" * 72)
    print("DAVID V14 - GATE 3 CORE BASELINE COMPARATOR")
    print("=" * 72)
    print()

    try:
        expected = load_json(EXPECTED_PATH)
        print("[PASS] V13.100 Golden Expected Oracle loaded")
    except Exception as exc:
        print(f"[FAIL] Cannot load Golden Expected Oracle: {exc}")
        return 1
    try:
        fixture = load_fixture(FIXTURE_PATH)
        print(
            f"[PASS] Golden Fixture loaded: "
            f"{len(fixture)} rows"
        )
    except Exception as exc:
        print(f"[FAIL] Cannot load Golden Fixture: {exc}")
        return 1
    try:
        from v14.core_engine import (
        build_pending_result,
        engine_contract,
        run_core,
        )

        print("[PASS] V14 Core Engine imported")
    except Exception as exc:
        print(f"[FAIL] Cannot import V14 Core Engine: {exc}")
        return 1

    contract = engine_contract()
    market_input = dict(expected["market_input"])
    market_input["_data"] = fixture

    result = run_core(market_input)
    actual = result.to_dict()

    print(
        f"[INFO] V14 Engine Version: "
        f"{contract['engine_version']}"
    )
    print(
        f"[INFO] V13 Baseline Version: "
        f"{contract['baseline_version']}"
    )
    print()

    locked_domains = contract["locked_v13_domains"]

    empty_domains = []

    for domain in locked_domains:
        value = actual.get(domain)

        if value is None or value == {}:
            empty_domains.append(domain)

    # ------------------------------------------------------------
    # Incremental Gate 3 - Technical Domain Verification
    # ------------------------------------------------------------
    if actual.get("technical"):
        technical_differences = []

        if "technical" not in expected:
            technical_differences.append(
                "technical: missing in V13 Golden Oracle"
            )
        else:
            compare_value(
                "technical",
                expected["technical"],
                actual["technical"],
                technical_differences,
            )

        print()
        print("=" * 72)
        print("GATE 3 - TECHNICAL DOMAIN CHECK")
        print("=" * 72)

        if technical_differences:
            print("[FAIL] Technical domain mismatch")
            print(
                f"Differences found: "
                f"{len(technical_differences)}"
            )
            print()

            for item in technical_differences:
                print(f"[DIFF] {item}")

        else:
            print("[PASS] Technical domain")
            print("V13.100 Golden Oracle == V14 Technical")

        print("=" * 72)
        print()

    # ------------------------------------------------------------
    # Incremental Gate 3 - Status Domain Verification
    # ------------------------------------------------------------
    if actual.get("status"):
        status_differences = []

        if "status" not in expected:
            status_differences.append(
                "status: missing in V13 Golden Oracle"
            )
        else:
            compare_value(
                "status",
                expected["status"],
                actual["status"],
                status_differences,
            )

        print()
        print("=" * 72)
        print("GATE 3 - STATUS DOMAIN CHECK")
        print("=" * 72)

        if status_differences:
            print("[FAIL] Status domain mismatch")
            print(
                f"Differences found: "
                f"{len(status_differences)}"
            )
            print()

            for item in status_differences:
                print(f"[DIFF] {item}")

        else:
            print("[PASS] Status domain")
            print("V13.100 Golden Oracle == V14 Status")

        print("=" * 72)
        print()

    # ------------------------------------------------------------
    # Incremental Gate 3 - Six Buy Domain Verification
    # ------------------------------------------------------------
    if actual.get("six_buy"):
        six_buy_differences = []

        if "six_buy" not in expected:
            six_buy_differences.append(
                "six_buy: missing in V13 Golden Oracle"
            )
        else:
            compare_value(
                "six_buy",
                expected["six_buy"],
                actual["six_buy"],
                six_buy_differences,
            )

        print()
        print("=" * 72)
        print("GATE 3 - SIX BUY DOMAIN CHECK")
        print("=" * 72)

        if six_buy_differences:
            print("[FAIL] Six Buy domain mismatch")
            print(
                f"Differences found: "
                f"{len(six_buy_differences)}"
            )
            print()

            for item in six_buy_differences:
                print(f"[DIFF] {item}")

        else:
            print("[PASS] Six Buy domain")
            print("V13.100 Golden Oracle == V14 Six Buy")

        print("=" * 72)
        print()

    # ------------------------------------------------------------
    # Incremental Gate 3 - Six Sell Domain Verification
    # ------------------------------------------------------------
    if actual.get("six_sell"):
        six_sell_differences = []

        if "six_sell" not in expected:
            six_sell_differences.append(
                "six_sell: missing in V13 Golden Oracle"
            )
        else:
            compare_value(
                "six_sell",
                expected["six_sell"],
                actual["six_sell"],
                six_sell_differences,
            )

        print()
        print("=" * 72)
        print("GATE 3 - SIX SELL DOMAIN CHECK")
        print("=" * 72)

        if six_sell_differences:
            print("[FAIL] Six Sell domain mismatch")
            print(
                f"Differences found: "
                f"{len(six_sell_differences)}"
            )
            print()

            for item in six_sell_differences:
                print(f"[DIFF] {item}")

        else:
            print("[PASS] Six Sell domain")
            print("V13.100 Golden Oracle == V14 Six Sell")

        print("=" * 72)
        print()
    # ------------------------------------------------------------
    # Incremental Gate 3 - Position Domain Verification
    # ------------------------------------------------------------
    if actual.get("position"):
        position_differences = []

        if "position" not in expected:
            position_differences.append(
                "position: missing in V13 Golden Oracle"
            )
        else:
            compare_value(
                "position",
                expected["position"],
                actual["position"],
                position_differences,
            )

        print()
        print("=" * 72)
        print("GATE 3 - POSITION DOMAIN CHECK")
        print("=" * 72)

        if position_differences:
            print("[FAIL] Position domain mismatch")
            print(
                f"Differences found: "
                f"{len(position_differences)}"
            )
            print()

            for item in position_differences:
                print(f"[DIFF] {item}")

        else:
            print("[PASS] Position domain")
            print("V13.100 Golden Oracle == V14 Position")

        print("=" * 72)
        print()
    # ------------------------------------------------------------
    # Incremental Gate 3 - Decision Domain Verification
    # ------------------------------------------------------------
    if actual.get("decision"):
        decision_differences = []

        if "decision" not in expected:
            decision_differences.append(
                "decision: missing in V13 Golden Oracle"
            )
        else:
            compare_value(
                "decision",
                expected["decision"],
                actual["decision"],
                decision_differences,
            )

        print()
        print("=" * 72)
        print("GATE 3 - DECISION DOMAIN CHECK")
        print("=" * 72)

        if decision_differences:
            print("[FAIL] Decision domain mismatch")
            print(
                f"Differences found: "
                f"{len(decision_differences)}"
            )
            print()

            for item in decision_differences:
                print(f"[DIFF] {item}")

        else:
            print("[PASS] Decision domain")
            print("V13.100 Golden Oracle == V14 Decision")

        print("=" * 72)
        print()
    if empty_domains:
        print("[NOT READY] V14 Core Engine is still a skeleton.")
        print()
        print("Locked domains not implemented:")

        for domain in empty_domains:
            print(f"  - {domain}")

        print()
        print("GATE 3 RESULT: NOT READY")
        print()
        print(
            "This is the EXPECTED result at the current "
            "V14 development stage."
        )
        print(
            "NO PASS is allowed until real V13 Core logic "
            "has been migrated and compared."
        )

        return 2

    differences = []

    for domain in locked_domains:
        if domain not in expected:
            differences.append(
                f"{domain}: missing in V13 Golden Oracle"
            )
            continue

        if domain not in actual:
            differences.append(
                f"{domain}: missing in V14 result"
            )
            continue

        compare_value(
            domain,
            expected[domain],
            actual[domain],
            differences,
        )

    print()

    if differences:
        print("=" * 72)
        print("GATE 3 RESULT: FAIL")
        print("=" * 72)
        print()
        print(f"Differences found: {len(differences)}")
        print()

        for item in differences:
            print(f"[DIFF] {item}")

        print()
        print("STOP - DO NOT MERGE MAIN")

        return 1

    print("=" * 72)
    print("GATE 3 RESULT: PASS")
    print("=" * 72)
    print()
    print("V13.100 Golden Oracle == V14 Core Engine")
    print(f"ABS_TOL = {ABS_TOL}")
    print()
    print("CORE BASELINE COMPATIBILITY: VERIFIED")
    print("SAFE TO CONTINUE TO NEXT MIGRATION STAGE")

    return 0


if __name__ == "__main__":
    sys.exit(main())