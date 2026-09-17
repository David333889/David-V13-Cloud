"""
DAVID V14 Unified Engine
Gate 2 - Golden Baseline Verifier

Purpose:
- Verify the frozen Golden Fixture exists.
- Verify its SHA-256 has not changed.
- Verify metadata matches the fixture.
- Verify the Expected Oracle belongs to the same fixture.
- Verify required baseline structures and LOCK fields exist.

IMPORTANT:
This verifier does NOT:
- call Yahoo Finance
- call Supabase
- import Streamlit
- modify app.py
- regenerate the fixture
- regenerate the Expected Oracle
- make trading decisions

It only verifies frozen test evidence.
"""

from __future__ import annotations

import hashlib
import json
import sys
from pathlib import Path


# ============================================================
# PATHS
# ============================================================

ROOT = Path(__file__).resolve().parent.parent

FIXTURE_PATH = ROOT / "tests" / "fixtures" / "golden_real_001.csv"
META_PATH = ROOT / "tests" / "fixtures" / "golden_real_001.meta.json"
EXPECTED_PATH = ROOT / "tests" / "expected" / "golden_real_001.expected.json"


# ============================================================
# REQUIRED STRUCTURE
# ============================================================

REQUIRED_TOP_LEVEL = {
    "schema_version",
    "baseline_version",
    "fixture_id",
    "fixture_sha256",
    "symbol",
    "row_count",
    "first_trade_date",
    "last_trade_date",
    "market_input",
    "technical",
    "status",
    "six_buy",
    "six_sell",
    "position",
    "decision",
    "ranking",
    "protection",
}

REQUIRED_MARKET_INPUT = {
    "prev_close",
    "open",
    "high",
    "low",
    "close",
    "volume",
}

REQUIRED_TECHNICAL = {
    "ma5",
    "ma5_previous",
    "ma20",
    "vm20",
    "macd_histogram",
    "mid",
    "volume_ratio_raw",
    "bias20_raw",
    "change_pct_raw",
}

REQUIRED_STATUS = {
    "early",
    "momentum",
    "cost",
    "strength",
}

REQUIRED_SIX_BUY = {
    "b1",
    "b2",
    "b3",
    "b4",
    "b5",
    "b6",
    "score",
}

REQUIRED_SIX_SELL = {
    "s1",
    "s2",
    "s3",
    "s4",
    "s5",
    "s6",
    "score",
}

REQUIRED_POSITION = {
    "swing_high",
    "swing_low",
    "swing_direction",
    "fib_0236",
    "fib_0382",
    "fib_0500",
    "fib_0618",
    "fib_0786",
    "fib_1272",
    "fib_1618",
    "fib_position",
}

REQUIRED_DECISION = {
    "core_decision",
}

REQUIRED_RANKING = {
    "david_score_v1",
}

REQUIRED_PROTECTION = {
    "fixture_read_only",
    "live_api_used",
    "supabase_used",
    "streamlit_used",
    "expected_overwrite_policy",
}


# ============================================================
# HELPERS
# ============================================================

def sha256_file(path: Path) -> str:
    digest = hashlib.sha256()

    with path.open("rb") as f:
        for chunk in iter(lambda: f.read(1024 * 1024), b""):
            digest.update(chunk)

    return digest.hexdigest()


def load_json(path: Path) -> dict:
    with path.open("r", encoding="utf-8") as f:
        return json.load(f)


def check_keys(name: str, data: dict, required: set[str]) -> list[str]:
    missing = sorted(required - set(data.keys()))

    if missing:
        return [
            f"{name}: missing required key -> {key}"
            for key in missing
        ]

    return []


def pass_line(message: str) -> None:
    print(f"[PASS] {message}")


def fail_line(message: str) -> None:
    print(f"[FAIL] {message}")


# ============================================================
# MAIN
# ============================================================

def main() -> int:
    print("=" * 64)
    print("DAVID V14 - GATE 2 GOLDEN BASELINE VERIFIER")
    print("=" * 64)
    print()

    errors: list[str] = []

    # --------------------------------------------------------
    # 1. File existence
    # --------------------------------------------------------

    required_files = [
        FIXTURE_PATH,
        META_PATH,
        EXPECTED_PATH,
    ]

    for path in required_files:
        if not path.is_file():
            errors.append(f"Missing file: {path}")

    if errors:
        for error in errors:
            fail_line(error)

        print()
        print("GATE 2 RESULT: FAIL")
        return 1

    pass_line("Frozen Fixture exists")
    pass_line("Fixture metadata exists")
    pass_line("Golden Expected Oracle exists")

    # --------------------------------------------------------
    # 2. Load evidence
    # --------------------------------------------------------

    try:
        metadata = load_json(META_PATH)
        expected = load_json(EXPECTED_PATH)
    except Exception as exc:
        fail_line(f"JSON load error: {exc}")
        print()
        print("GATE 2 RESULT: FAIL")
        return 1

    pass_line("JSON files loaded successfully")

    # --------------------------------------------------------
    # 3. Fixture SHA-256
    # --------------------------------------------------------

    actual_sha256 = sha256_file(FIXTURE_PATH)

    metadata_sha256 = str(
        metadata.get("csv_sha256", "")
    ).lower()

    expected_sha256 = str(
        expected.get("fixture_sha256", "")
    ).lower()

    if actual_sha256.lower() != metadata_sha256:
        errors.append(
            "Fixture SHA-256 does not match metadata"
        )
    else:
        pass_line("Fixture SHA-256 matches metadata")

    if actual_sha256.lower() != expected_sha256:
        errors.append(
            "Fixture SHA-256 does not match Expected Oracle"
        )
    else:
        pass_line("Fixture SHA-256 matches Expected Oracle")

    # --------------------------------------------------------
    # 4. Identity checks
    # --------------------------------------------------------

    identity_checks = [
        (
            "fixture_id",
            metadata.get("fixture_id"),
            expected.get("fixture_id"),
        ),
        (
            "baseline_version",
            metadata.get("baseline_version"),
            expected.get("baseline_version"),
        ),
        (
            "symbol",
            metadata.get("symbol"),
            expected.get("symbol"),
        ),
        (
            "row_count",
            metadata.get("row_count"),
            expected.get("row_count"),
        ),
        (
            "first_trade_date",
            metadata.get("first_trade_date"),
            expected.get("first_trade_date"),
        ),
        (
            "last_trade_date",
            metadata.get("last_trade_date"),
            expected.get("last_trade_date"),
        ),
    ]

    for field, meta_value, expected_value in identity_checks:
        if meta_value != expected_value:
            errors.append(
                f"Identity mismatch: {field} "
                f"(metadata={meta_value!r}, expected={expected_value!r})"
            )
        else:
            pass_line(f"Identity matches: {field}")

    # --------------------------------------------------------
    # 5. Expected structure
    # --------------------------------------------------------

    errors.extend(
        check_keys(
            "expected",
            expected,
            REQUIRED_TOP_LEVEL,
        )
    )

    section_checks = [
        (
            "market_input",
            expected.get("market_input", {}),
            REQUIRED_MARKET_INPUT,
        ),
        (
            "technical",
            expected.get("technical", {}),
            REQUIRED_TECHNICAL,
        ),
        (
            "status",
            expected.get("status", {}),
            REQUIRED_STATUS,
        ),
        (
            "six_buy",
            expected.get("six_buy", {}),
            REQUIRED_SIX_BUY,
        ),
        (
            "six_sell",
            expected.get("six_sell", {}),
            REQUIRED_SIX_SELL,
        ),
        (
            "position",
            expected.get("position", {}),
            REQUIRED_POSITION,
        ),
        (
            "decision",
            expected.get("decision", {}),
            REQUIRED_DECISION,
        ),
        (
            "ranking",
            expected.get("ranking", {}),
            REQUIRED_RANKING,
        ),
        (
            "protection",
            expected.get("protection", {}),
            REQUIRED_PROTECTION,
        ),
    ]

    for section_name, section_data, required_keys in section_checks:
        if not isinstance(section_data, dict):
            errors.append(
                f"{section_name}: section is not a JSON object"
            )
            continue

        section_errors = check_keys(
            section_name,
            section_data,
            required_keys,
        )

        errors.extend(section_errors)

        if not section_errors:
            pass_line(f"Required fields complete: {section_name}")

    # --------------------------------------------------------
    # 6. Protection rules
    # --------------------------------------------------------

    protection = expected.get("protection", {})

    if protection.get("fixture_read_only") is not True:
        errors.append(
            "Protection failure: fixture_read_only must be true"
        )
    else:
        pass_line("Protection: fixture_read_only = true")

    for field in (
        "live_api_used",
        "supabase_used",
        "streamlit_used",
    ):
        if protection.get(field) is not False:
            errors.append(
                f"Protection failure: {field} must be false"
            )
        else:
            pass_line(f"Protection: {field} = false")

    if protection.get("expected_overwrite_policy") != "DENY_BY_DEFAULT":
        errors.append(
            "Protection failure: "
            "expected_overwrite_policy must be DENY_BY_DEFAULT"
        )
    else:
        pass_line(
            "Protection: expected_overwrite_policy = DENY_BY_DEFAULT"
        )

    # --------------------------------------------------------
    # 7. Baseline sanity checks
    # --------------------------------------------------------

    six_buy = expected.get("six_buy", {})
    six_sell = expected.get("six_sell", {})

    buy_count = sum(
        1
        for key in ("b1", "b2", "b3", "b4", "b5", "b6")
        if six_buy.get(key) is True
    )

    sell_count = sum(
        1
        for key in ("s1", "s2", "s3", "s4", "s5", "s6")
        if six_sell.get(key) is True
    )

    if six_buy.get("score") != buy_count:
        errors.append(
            f"Six Buy score mismatch: "
            f"stored={six_buy.get('score')}, calculated={buy_count}"
        )
    else:
        pass_line(f"Six Buy score integrity = {buy_count}")

    if six_sell.get("score") != sell_count:
        errors.append(
            f"Six Sell score mismatch: "
            f"stored={six_sell.get('score')}, calculated={sell_count}"
        )
    else:
        pass_line(f"Six Sell score integrity = {sell_count}")

    # --------------------------------------------------------
    # FINAL RESULT
    # --------------------------------------------------------

    print()
    print("-" * 64)

    if errors:
        print("GATE 2 RESULT: FAIL")
        print("-" * 64)

        for error in errors:
            fail_line(error)

        print()
        print("STOP:")
        print("Do NOT modify the Golden Oracle.")
        print("Do NOT continue to Core Refactor.")
        return 1

    print("GATE 2 RESULT: PASS")
    print("-" * 64)
    print()
    print(f"Fixture ID:       {expected['fixture_id']}")
    print(f"Baseline Version: {expected['baseline_version']}")
    print(f"Symbol:           {expected['symbol']}")
    print(f"Rows:             {expected['row_count']}")
    print(f"Fixture SHA-256:  {actual_sha256}")
    print()
    print(
        f"Core Decision:    "
        f"{expected['decision']['core_decision']}"
    )
    print(
        f"Six Buy / Sell:   "
        f"{expected['six_buy']['score']} / "
        f"{expected['six_sell']['score']}"
    )
    print(
        f"Fib Position:     "
        f"{expected['position']['fib_position']}"
    )
    print(
        f"DAVID Score V1:   "
        f"{expected['ranking']['david_score_v1']}"
    )
    print()
    print("GOLDEN BASELINE INTEGRITY: VERIFIED")
    print("SAFE TO CONTINUE TO NEXT TEST STAGE")

    return 0


if __name__ == "__main__":
    sys.exit(main())