"""
DAVID V14 Unified Engine
Golden Fixture Builder

Purpose:
- Download one frozen Yahoo Finance OHLCV history sample.
- Normalize the data into a reproducible CSV fixture.
- Generate metadata and SHA-256 checksum.
- Never overwrite an existing Golden Fixture by default.

IMPORTANT:
This script does NOT calculate trading decisions.
It does NOT modify app.py, Supabase, or V13 production data.
"""

from __future__ import annotations

import hashlib
import json
from datetime import datetime, timezone
from zoneinfo import ZoneInfo
from pathlib import Path

import pandas as pd
import yfinance as yf


# ============================================================
# Golden Fixture Configuration
# ============================================================

SYMBOL = "6213.TW"
STOCK_CODE = "6213"
STOCK_NAME = "聯茂"
MARKET = "TW"

BASELINE_VERSION = "V13.100"
FIXTURE_VERSION = 1

DOWNLOAD_PERIOD = "2y"
INTERVAL = "1d"

FIXTURE_ROWS = 200
MIN_REQUIRED_ROWS = 160

TESTS_DIR = Path(__file__).resolve().parent
FIXTURE_DIR = TESTS_DIR / "fixtures"

CSV_PATH = FIXTURE_DIR / "golden_real_001.csv"
META_PATH = FIXTURE_DIR / "golden_real_001.meta.json"


# ============================================================
# Helpers
# ============================================================

def sha256_file(path: Path) -> str:
    """Return SHA-256 checksum of a file."""
    digest = hashlib.sha256()

    with path.open("rb") as file_obj:
        for chunk in iter(lambda: file_obj.read(65536), b""):
            digest.update(chunk)

    return digest.hexdigest()


def normalize_yahoo_frame(raw: pd.DataFrame) -> pd.DataFrame:
    """
    Normalize Yahoo Finance data into the Golden OHLCV schema.

    Output columns:
        timestamp, open, high, low, close, volume
    """

    if raw is None or raw.empty:
        raise RuntimeError("Yahoo returned no data.")

    data = raw.copy()

    # yfinance may return MultiIndex columns.
    if isinstance(data.columns, pd.MultiIndex):
        if SYMBOL in data.columns.get_level_values(0):
            data = data[SYMBOL].copy()
        elif SYMBOL in data.columns.get_level_values(-1):
            data = data.xs(SYMBOL, axis=1, level=-1).copy()
        else:
            # Single ticker downloads can still return a MultiIndex.
            data.columns = data.columns.get_level_values(0)

    required = ["Open", "High", "Low", "Close", "Volume"]

    missing = [column for column in required if column not in data.columns]
    if missing:
        raise RuntimeError(
            f"Missing Yahoo columns: {', '.join(missing)}"
        )

    data = data[required].copy()

    for column in required:
        data[column] = pd.to_numeric(data[column], errors="coerce")

    data = data.dropna(
        subset=["Open", "High", "Low", "Close", "Volume"]
    )

    if data.empty:
        raise RuntimeError("No valid OHLCV rows after normalization.")

    # Golden Fixture uses prior completed Taiwan trading days only.
    #
    # Never freeze the execution day's bar.  This keeps the fixture
    # reproducible whether the builder runs before, during, or after
    # Taiwan market hours.
    taipei_today = datetime.now(
        ZoneInfo("Asia/Taipei")
    ).date()

    index_dates = pd.to_datetime(data.index).date
    data = data[index_dates < taipei_today].copy()

    if data.empty:
        raise RuntimeError("No completed trading-day rows available.")

    data = data.tail(FIXTURE_ROWS).copy()

    if len(data) < MIN_REQUIRED_ROWS:
        raise RuntimeError(
            f"Insufficient history: {len(data)} rows; "
            f"minimum required is {MIN_REQUIRED_ROWS}."
        )

    data.index = pd.to_datetime(data.index)

    output = pd.DataFrame(
        {
            "timestamp": data.index.strftime("%Y-%m-%d"),
            "open": data["Open"].astype(float).values,
            "high": data["High"].astype(float).values,
            "low": data["Low"].astype(float).values,
            "close": data["Close"].astype(float).values,
            "volume": data["Volume"].astype(float).values,
        }
    )

    # Basic integrity checks.
    invalid_price = (
        (output["high"] < output["low"])
        | (output["high"] < output["open"])
        | (output["high"] < output["close"])
        | (output["low"] > output["open"])
        | (output["low"] > output["close"])
    )

    if invalid_price.any():
        bad_rows = output.loc[invalid_price, "timestamp"].tolist()
        raise RuntimeError(
            f"Invalid OHLC price relationship on: {bad_rows}"
        )

    if (output["volume"] < 0).any():
        raise RuntimeError("Negative volume detected.")

    if output["timestamp"].duplicated().any():
        raise RuntimeError("Duplicate trading dates detected.")

    return output.reset_index(drop=True)


def build_metadata(
    fixture: pd.DataFrame,
    checksum: str,
) -> dict:
    """Build provenance metadata for the frozen fixture."""

    return {
        "fixture_id": "golden_real_001",
        "fixture_version": FIXTURE_VERSION,
        "baseline_version": BASELINE_VERSION,
        "purpose": "V13.100 Core Golden Baseline regression fixture",
        "source": "Yahoo Finance",
        "source_type": "frozen_historical_ohlcv",
        "symbol": SYMBOL,
        "stock_code": STOCK_CODE,
        "stock_name": STOCK_NAME,
        "market": MARKET,
        "interval": INTERVAL,
        "auto_adjust": False,
        "row_count": int(len(fixture)),
        "first_trade_date": str(fixture.iloc[0]["timestamp"]),
        "last_trade_date": str(fixture.iloc[-1]["timestamp"]),
        "generated_at_utc": datetime.now(timezone.utc).isoformat(),
        "csv_file": CSV_PATH.name,
        "csv_sha256": checksum,
        "overwrite_policy": "DENY_BY_DEFAULT",
        "notes": [
            "Fixture contains frozen OHLCV only.",
            "Fixture must not depend on live APIs during baseline tests.",
            "This file is test evidence, not a trading recommendation.",
        ],
    }


# ============================================================
# Builder
# ============================================================

def main() -> None:
    FIXTURE_DIR.mkdir(parents=True, exist_ok=True)

    if CSV_PATH.exists() or META_PATH.exists():
        raise FileExistsError(
            "Golden Fixture already exists. "
            "Refusing to overwrite frozen baseline data."
        )

    print("=" * 60)
    print("DAVID V14 GOLDEN FIXTURE BUILDER")
    print("=" * 60)
    print(f"Symbol: {SYMBOL}")
    print("Downloading historical OHLCV...")

    raw = yf.download(
        tickers=SYMBOL,
        period=DOWNLOAD_PERIOD,
        interval=INTERVAL,
        auto_adjust=False,
        actions=False,
        progress=False,
        threads=False,
    )

    fixture = normalize_yahoo_frame(raw)

    fixture.to_csv(
        CSV_PATH,
        index=False,
        encoding="utf-8",
        float_format="%.10f",
        lineterminator="\n",
    )

    checksum = sha256_file(CSV_PATH)

    metadata = build_metadata(
        fixture=fixture,
        checksum=checksum,
    )

    META_PATH.write_text(
        json.dumps(
            metadata,
            ensure_ascii=False,
            indent=2,
        )
        + "\n",
        encoding="utf-8",
    )

    print()
    print("Golden Fixture created successfully.")
    print(f"Rows:       {len(fixture)}")
    print(
        f"Date range: {fixture.iloc[0]['timestamp']} "
        f"→ {fixture.iloc[-1]['timestamp']}"
    )
    print(f"CSV:        {CSV_PATH}")
    print(f"Metadata:   {META_PATH}")
    print(f"SHA-256:    {checksum}")
    print()
    print("IMPORTANT:")
    print("The fixture is now frozen.")
    print("Do not regenerate it during normal baseline tests.")


if __name__ == "__main__":
    main()
