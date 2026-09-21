import sys
from pathlib import Path

import pandas as pd


ROOT = Path(__file__).resolve().parents[2]

if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))


def build_test_data():
    return pd.DataFrame(
        {
            "Open": [510.0, 514.0],
            "High": [520.0, 531.0],
            "Low": [505.0, 511.0],
            "Close": [515.0, 519.0],
            "Volume": [10000000.0, 11373100.0],
        }
    )


def build_legacy_result():
    return {
        "昨收": 515.0,
        "開盤": 514.0,
        "現價": 519.0,
    }


def main():
    print("=" * 72)
    print("DAVID V14 - APP MARKET INPUT ADAPTER V1 COMPARATOR")
    print("=" * 72)

    try:
        from v14.app_market_input_adapter import (
            build_app_market_input,
        )
    except (ImportError, ModuleNotFoundError) as exc:
        print(
            "[FAIL] "
            "App Market Input Adapter V1 implementation not found"
        )
        print(f"[INFO] {exc}")
        print(
            "APP MARKET INPUT ADAPTER V1 RESULT: FAIL"
        )
        return 1

    if not callable(build_app_market_input):
        print("[FAIL] build_app_market_input() is not callable")
        return 1

    if not callable(build_app_market_input):
        print("[FAIL] build_app_market_input() is not callable")
        return 1

    print("[PASS] build_app_market_input() detected")

    data = build_test_data()
    legacy_result = build_legacy_result()

    actual = build_app_market_input(
        legacy_result,
        data,
    )

    if not isinstance(actual, dict):
        print("[FAIL] Adapter result is not dict")
        return 1

    expected = {
        "prev_close": 515.0,
        "open": 514.0,
        "high": 531.0,
        "low": 511.0,
        "close": 519.0,
        "volume": 11373100.0,
    }

    for key, value in expected.items():
        if actual.get(key) != value:
            print(
                f"[FAIL] {key}: "
                f"expected={value!r}, "
                f"actual={actual.get(key)!r}"
            )
            return 1

    print("[PASS] Golden Market Mapping preserved")

    if "_data" not in actual:
        print("[FAIL] _data missing")
        return 1

    if actual["_data"] is not data:
        print("[FAIL] _data DataFrame was copied or replaced")
        return 1

    print("[PASS] _data DataFrame preserved")

    expected_keys = {
        "prev_close",
        "open",
        "high",
        "low",
        "close",
        "volume",
        "_data",
    }

    if set(actual.keys()) != expected_keys:
        print(
            "[FAIL] Unexpected market_input keys: "
            f"{sorted(actual.keys())}"
        )
        return 1

    print("[PASS] Exact market_input contract")

    # Negative Case 1:
    # Invalid legacy result type must be rejected.
    try:
        build_app_market_input(
            None,
            build_test_data(),
        )
        print("[FAIL] Invalid legacy result type was accepted")
        return 1
    except TypeError:
        print("[PASS] Invalid legacy result type rejected")

    # Negative Case 2:
    # Missing required legacy field must be rejected.
    invalid_result = build_legacy_result()
    invalid_result.pop("昨收", None)

    try:
        build_app_market_input(
            invalid_result,
            build_test_data(),
        )
        print("[FAIL] Missing legacy field was accepted")
        return 1
    except ValueError:
        print("[PASS] Missing legacy field rejected")

    # Negative Case 3:
    # Invalid data type must be rejected.
    try:
        build_app_market_input(
            build_legacy_result(),
            None,
        )
        print("[FAIL] Invalid data type was accepted")
        return 1
    except TypeError:
        print("[PASS] Invalid data type rejected")

    # Negative Case 4:
    # Empty DataFrame must be rejected.
    try:
        build_app_market_input(
            build_legacy_result(),
            pd.DataFrame(),
        )
        print("[FAIL] Empty DataFrame was accepted")
        return 1
    except ValueError:
        print("[PASS] Empty DataFrame rejected")

    # Negative Case 5:
    # Missing required market column must be rejected.
    invalid_data = build_test_data().drop(columns=["Volume"])

    try:
        build_app_market_input(
            build_legacy_result(),
            invalid_data,
        )
        print("[FAIL] Missing market column was accepted")
        return 1
    except ValueError:
        print("[PASS] Missing market column rejected")

    print("-" * 72)
    print("APP MARKET INPUT ADAPTER V1 RESULT: PASS")
    print("PURE MAPPING | NO APP.PY | NO WRITER | NO NETWORK I/O")
    return 0


if __name__ == "__main__":
    sys.exit(main())