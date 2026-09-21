import sys
from tests.compare_v13_v14 import load_fixture
from pathlib import Path

import pandas as pd


ROOT = Path(__file__).resolve().parents[2]

if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))


def build_test_data():
    fixture_path = (
        ROOT
        / "tests"
        / "fixtures"
        / "golden_real_001.csv"
    )

    return load_fixture(fixture_path)

    return pd.DataFrame(
        {
            "Open": [510.0, 514.0],
            "High": [520.0, 531.0],
            "Low": [505.0, 511.0],
            "Close": [515.0, 519.0],
            "Volume": [10000000.0, 11373100.0],
        },
        index=index,
    )


def build_legacy_result():
    return {
        "昨收": 515.0,
        "開盤": 514.0,
        "現價": 519.0,
    }


def main():
    print("=" * 72)
    print("DAVID V14 - APP DRY-RUN PIPELINE V1 COMPARATOR")
    print("=" * 72)

    try:
        from v14.app_dry_run import run_app_dry_run
    except (ImportError, ModuleNotFoundError) as exc:
        print(
            "[FAIL] "
            "App Dry-Run Pipeline V1 implementation not found"
        )
        print(f"[INFO] {exc}")
        print("APP DRY-RUN PIPELINE V1 RESULT: FAIL")
        return 1

    if not callable(run_app_dry_run):
        print("[FAIL] run_app_dry_run() is not callable")
        return 1

    print("[PASS] run_app_dry_run() detected")

    actual = run_app_dry_run(
        legacy_result=build_legacy_result(),
        data=build_test_data(),
        code="2330",
        name="TEST",
        market="TW",
        symbol="2330.TW",
    )

    if not isinstance(actual, dict):
        print("[FAIL] Dry-Run result is not dict")
        return 1

    if actual.get("state") != "READY":
        print(
            "[FAIL] Expected state READY, "
            f"got: {actual.get('state')}"
        )
        return 1

    print("[PASS] Dry-Run State = READY")

    if actual.get("reason") != "PERSISTENCE_ROW_OK":
        print(
            "[FAIL] Expected reason PERSISTENCE_ROW_OK, "
            f"got: {actual.get('reason')}"
        )
        return 1

    print("[PASS] Dry-Run Reason = PERSISTENCE_ROW_OK")

    row = actual.get("row")

    if not isinstance(row, dict):
        print("[FAIL] Persistence row missing")
        return 1

    print("[PASS] Persistence Row detected")

    expected_identity = {
        "trade_date": "2026-09-15",
        "code": "2330",
        "name": "TEST",
        "market": "TW",
        "symbol": "2330.TW",
    }

    for key, expected in expected_identity.items():
        if row.get(key) != expected:
            print(
                f"[FAIL] Identity mismatch: {key} "
                f"expected={expected!r}, "
                f"actual={row.get(key)!r}"
            )
            return 1

    print("[PASS] Identity derived correctly")

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
        print(
            "[FAIL] Missing Version/Safety fields: "
            f"{missing}"
        )
        return 1

    print("[PASS] Version/Safety fields detected")

    # Negative Case 1: invalid data type
    blocked = run_app_dry_run(
        legacy_result=build_legacy_result(),
        data=None,
        code="2330",
        name="TEST",
        market="TW",
        symbol="2330.TW",
    )

    if (
        blocked.get("state") != "BLOCKED"
        or blocked.get("reason") != "INVALID_DATA_TYPE"
    ):
        print(f"[FAIL] Invalid data type: {blocked}")
        return 1

    print("[PASS] Invalid Data = BLOCKED / INVALID_DATA_TYPE")

    # Negative Case 2: empty DataFrame
    blocked = run_app_dry_run(
        legacy_result=build_legacy_result(),
        data=pd.DataFrame(),
        code="2330",
        name="TEST",
        market="TW",
        symbol="2330.TW",
    )

    if (
        blocked.get("state") != "BLOCKED"
        or blocked.get("reason") != "EMPTY_DATA"
    ):
        print(f"[FAIL] Empty data: {blocked}")
        return 1

    print("[PASS] Empty Data = BLOCKED / EMPTY_DATA")

    # Negative Case 3: invalid trade date
    invalid_date_data = build_test_data().copy()
    invalid_date_data.index = ["INVALID"] * len(invalid_date_data)

    blocked = run_app_dry_run(
        legacy_result=build_legacy_result(),
        data=invalid_date_data,
        code="2330",
        name="TEST",
        market="TW",
        symbol="2330.TW",
    )

    if (
        blocked.get("state") != "BLOCKED"
        or blocked.get("reason") != "INVALID_TRADE_DATE"
    ):
        print(f"[FAIL] Invalid trade date: {blocked}")
        return 1

    print("[PASS] Invalid Trade Date = BLOCKED / INVALID_TRADE_DATE")

    # Negative Case 4: missing identity
    blocked = run_app_dry_run(
        legacy_result=build_legacy_result(),
        data=build_test_data(),
        code="",
        name="TEST",
        market="TW",
        symbol="2330.TW",
    )

    if (
        blocked.get("state") != "BLOCKED"
        or blocked.get("reason") != "IDENTITY_CODE_MISSING"
    ):
        print(f"[FAIL] Missing identity: {blocked}")
        return 1

    print("[PASS] Missing Identity = BLOCKED / IDENTITY_CODE_MISSING")

    print("-" * 72)
    print("APP DRY-RUN PIPELINE V1 RESULT: PASS")
    print(
        "NO APP.PY | NO WRITER | "
        "NO CLIENT | NO NETWORK I/O"
    )
    return 0


if __name__ == "__main__":
    sys.exit(main())