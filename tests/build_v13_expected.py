"""
DAVID V14 Unified Engine
V13.100 Golden Expected Builder

Purpose:
- Read the frozen Golden Fixture only.
- Reproduce the locked V13.100 Core calculations.
- Produce a Golden Expected JSON for regression testing.
- Never call Yahoo, Supabase, Streamlit, or any live API.
"""

from __future__ import annotations

import hashlib
import json
from pathlib import Path

import numpy as np
import pandas as pd


BASE_DIR = Path(__file__).resolve().parent
FIXTURE_PATH = BASE_DIR / "fixtures" / "golden_real_001.csv"
META_PATH = BASE_DIR / "fixtures" / "golden_real_001.meta.json"
EXPECTED_DIR = BASE_DIR / "expected"
EXPECTED_PATH = EXPECTED_DIR / "golden_real_001.expected.json"

EXPECTED_FIXTURE_SHA256 = (
    "82c7d4eb4c868bf2707b9315f00ec741b0bf60f40a3c1b3ed2de0686dfa36c70"
)

CODE = "6213"
NAME = "聯茂"
SYMBOL = "6213.TW"


def sha256_file(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as f:
        for block in iter(lambda: f.read(1024 * 1024), b""):
            h.update(block)
    return h.hexdigest()


def load_fixture() -> pd.DataFrame:
    if not FIXTURE_PATH.exists():
        raise FileNotFoundError(f"Fixture not found: {FIXTURE_PATH}")

    actual_sha = sha256_file(FIXTURE_PATH)

    if actual_sha != EXPECTED_FIXTURE_SHA256:
        raise RuntimeError(
            "GOLDEN FIXTURE SHA-256 MISMATCH.\n"
            f"Expected: {EXPECTED_FIXTURE_SHA256}\n"
            f"Actual:   {actual_sha}\n"
            "STOP: Expected Result will NOT be generated."
        )

    df = pd.read_csv(FIXTURE_PATH)

    required = {"timestamp", "open", "high", "low", "close", "volume"}
    missing = required - set(df.columns)

    if missing:
        raise RuntimeError(f"Fixture missing columns: {sorted(missing)}")

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


# ============================================================
# V13.100 MACD Histogram
# ============================================================

def calculate_macd(close):
    ema12 = close.ewm(span=12, adjust=False).mean()
    ema26 = close.ewm(span=26, adjust=False).mean()

    macd_line = ema12 - ema26
    signal_line = macd_line.ewm(span=9, adjust=False).mean()

    histogram = macd_line - signal_line

    return histogram


# ============================================================
# V13.100 Pivot Swing + Fibonacci
# ============================================================

def calculate_pivot_fib(data, lookback=120, left=3, right=3):

    empty_result = {
        "方向": "資料不足",
        "波段高": np.nan,
        "波段低": np.nan,
        "0.236": np.nan,
        "0.382": np.nan,
        "0.500": np.nan,
        "0.618": np.nan,
        "0.786": np.nan,
        "1.272": np.nan,
        "1.618": np.nan,
        "Fib位置": "資料不足",
    }

    if (
        data is None
        or data.empty
        or len(data) < left + right + 20
    ):
        return empty_result

    d = (
        data
        .tail(lookback)
        .copy()
        .reset_index(drop=True)
    )

    highs = d["High"].astype(float).to_numpy()
    lows = d["Low"].astype(float).to_numpy()

    close_now = float(d["Close"].iloc[-1])

    pivot_highs = []
    pivot_lows = []

    for i in range(left, len(d) - right):

        hi_window = highs[i-left:i+right+1]
        lo_window = lows[i-left:i+right+1]

        if highs[i] == np.max(hi_window):
            pivot_highs.append(i)

        if lows[i] == np.min(lo_window):
            pivot_lows.append(i)

    if not pivot_highs or not pivot_lows:
        high_idx = int(d["High"].idxmax())
        low_idx = int(d["Low"].idxmin())
    else:
        high_idx = pivot_highs[-1]
        low_idx = pivot_lows[-1]

    swing_high = float(d.loc[high_idx, "High"])
    swing_low = float(d.loc[low_idx, "Low"])

    wave = swing_high - swing_low

    if wave <= 0:
        result = empty_result.copy()

        result.update(
            {
                "方向": "無有效波段",
                "波段高": swing_high,
                "波段低": swing_low,
                "Fib位置": "無有效波段",
            }
        )

        return result

    if low_idx < high_idx:

        direction = "多頭波段"

        levels = {
            "0.236": swing_high - wave * 0.236,
            "0.382": swing_high - wave * 0.382,
            "0.500": swing_high - wave * 0.500,
            "0.618": swing_high - wave * 0.618,
            "0.786": swing_high - wave * 0.786,
            "1.272": swing_high + wave * 0.272,
            "1.618": swing_high + wave * 0.618,
        }

        if close_now > swing_high:
            fib_status = "突破前高"
        elif close_now >= levels["0.236"]:
            fib_status = "近前高"
        elif close_now >= levels["0.382"]:
            fib_status = "0.382支撐"
        elif close_now >= levels["0.500"]:
            fib_status = "0.500支撐"
        elif close_now >= levels["0.618"]:
            fib_status = "0.618關鍵"
        elif close_now >= levels["0.786"]:
            fib_status = "0.786深回"
        else:
            fib_status = "跌破0.786"

    else:

        direction = "空頭波段"

        levels = {
            "0.236": swing_low + wave * 0.236,
            "0.382": swing_low + wave * 0.382,
            "0.500": swing_low + wave * 0.500,
            "0.618": swing_low + wave * 0.618,
            "0.786": swing_low + wave * 0.786,
            "1.272": swing_low - wave * 0.272,
            "1.618": swing_low - wave * 0.618,
        }

        if close_now < swing_low:
            fib_status = "跌破前低"
        elif close_now <= levels["0.236"]:
            fib_status = "近前低"
        elif close_now <= levels["0.382"]:
            fib_status = "0.382壓力"
        elif close_now <= levels["0.500"]:
            fib_status = "0.500壓力"
        elif close_now <= levels["0.618"]:
            fib_status = "0.618壓力"
        elif close_now <= levels["0.786"]:
            fib_status = "0.786壓力"
        else:
            fib_status = "逼近前高"

    return {
        "方向": direction,
        "波段高": swing_high,
        "波段低": swing_low,
        **levels,
        "Fib位置": fib_status,
    }


# ============================================================
# V13.100 Core Analysis
# ============================================================

def analyze_stock(code, name, data, symbol):

    if data.empty or len(data) < 60:
        raise RuntimeError("Golden Fixture does not contain enough rows.")

    close = data["Close"].astype(float)
    volume_series = data["Volume"].astype(float)

    latest = data.iloc[-1]
    previous = data.iloc[-2]

    p = float(latest["Close"])
    op = float(latest["Open"])
    hi = float(latest["High"])
    lo = float(latest["Low"])
    vo = float(latest["Volume"])
    pc = float(previous["Close"])

    ma20_series = close.rolling(20).mean()
    vm20_series = volume_series.rolling(20).mean()
    ma5_series = close.rolling(5).mean()

    ma20 = float(ma20_series.iloc[-1])
    vm20 = float(vm20_series.iloc[-1])
    ma5_now = float(ma5_series.iloc[-1])
    ma5_prev = float(ma5_series.iloc[-2])

    ma5_up = (
        not np.isnan(ma5_now)
        and not np.isnan(ma5_prev)
        and ma5_now > ma5_prev
    )

    macd_hist = calculate_macd(close)
    mh = float(macd_hist.iloc[-1])

    if np.isnan(mh):
        mh = 0.0

    diff = p - pc

    ch = (
        ((p - pc) / pc) * 100
        if pc > 0
        else 0.0
    )

    vr = (
        vo / vm20
        if vm20 > 0
        else 1.0
    )

    bias = (
        ((p - ma20) / ma20) * 100
        if ma20 > 0
        else 0.0
    )

    mid = (hi + lo) / 2

    # Six Buy V10
    b1 = p > op
    b2 = p > ma20
    b3 = vo > vm20
    b4 = p > mid
    b5 = ma5_up
    b6 = mh > 0

    b_score = sum([b1, b2, b3, b4, b5, b6])

    # Six Sell V10
    s1 = p < op
    s2 = p < ma20
    s3 = vo > vm20 and p < pc
    s4 = p < mid
    s5 = not ma5_up
    s6 = mh <= 0

    s_score = sum([s1, s2, s3, s4, s5, s6])

    is_strong = ch >= 3.0

    if is_strong:
        morning = "強攻"
    elif b1:
        morning = "合格"
    else:
        morning = "待定"

    momentum = "放量" if vo > vm20 else "量縮"
    cost = "站穩" if p > ma20 else "破位"
    strength = "強勢" if p > mid else "弱勢"

    if b_score == 6:
        decision = "全導通"
    elif s_score == 6:
        decision = "全空破"
    elif b_score >= 4:
        decision = "看多"
    elif s_score >= 4:
        decision = "看空"
    else:
        decision = "觀望"

    fib = calculate_pivot_fib(data)

    return {
        "AI 精選族群": f"{code} {name}",
        "昨收": pc,
        "開盤": op,
        "現價": p,
        "漲跌": diff,
        "幅%": f"{ch:+.1f}%",
        "量比": f"{vr:.1f}x",
        "乖離": f"{bias:+.1f}%",
        "早盤": morning,
        "動能": momentum,
        "成本": cost,
        "力道": strength,
        "六買": int(b_score),
        "六賣": int(s_score),
        "Fib位置": fib["Fib位置"],
        "決策": decision,
        "_fib": fib,

        # Golden-only raw evidence.
        "_raw": {
            "ma5": ma5_now,
            "ma5_previous": ma5_prev,
            "ma20": ma20,
            "vm20": vm20,
            "macd_histogram": mh,
            "mid": mid,
            "volume_ratio": vr,
            "bias20": bias,
            "change_pct": ch,
            "b1": bool(b1),
            "b2": bool(b2),
            "b3": bool(b3),
            "b4": bool(b4),
            "b5": bool(b5),
            "b6": bool(b6),
            "s1": bool(s1),
            "s2": bool(s2),
            "s3": bool(s3),
            "s4": bool(s4),
            "s5": bool(s5),
            "s6": bool(s6),
        },
    }


# ============================================================
# V13.100 DAVID Score V1
# ============================================================

def _safe_float(value, suffix=""):
    try:
        text = str(value).replace(suffix, "").strip()

        if text in ("", "--", "nan", "None"):
            return 0.0

        return float(text)

    except Exception:
        return 0.0


def _technical_metrics(data):

    m = {
        "ret1": 0.0,
        "ret5": 0.0,
        "ret20": 0.0,
        "vol_ratio": 1.0,
        "new20": False,
        "macd_flip": False,
        "ma_cross": False,
    }

    if data is None or data.empty or len(data) < 25:
        return m

    try:
        close = data["Close"].astype(float)
        vol = data["Volume"].astype(float)

        m["ret1"] = (
            (close.iloc[-1] / close.iloc[-2] - 1) * 100
            if close.iloc[-2]
            else 0.0
        )

        m["ret5"] = (
            (close.iloc[-1] / close.iloc[-6] - 1) * 100
            if close.iloc[-6]
            else 0.0
        )

        m["ret20"] = (
            (close.iloc[-1] / close.iloc[-21] - 1) * 100
            if close.iloc[-21]
            else 0.0
        )

        vm20 = float(vol.rolling(20).mean().iloc[-1])

        m["vol_ratio"] = (
            float(vol.iloc[-1] / vm20)
            if vm20 > 0
            else 1.0
        )

        prior20_high = float(close.iloc[-21:-1].max())

        m["new20"] = float(close.iloc[-1]) >= prior20_high

        macd = calculate_macd(close)

        m["macd_flip"] = bool(
            macd.iloc[-1] > 0
            and macd.iloc[-2] <= 0
        )

        ma5 = close.rolling(5).mean()
        ma20 = close.rolling(20).mean()

        m["ma_cross"] = bool(
            ma5.iloc[-1] > ma20.iloc[-1]
            and ma5.iloc[-2] <= ma20.iloc[-2]
        )

    except Exception:
        pass

    return m


def _score_bundle(result, data):

    buy = _safe_float(result.get("六買"))
    sell = _safe_float(result.get("六賣"))
    vr = _safe_float(result.get("量比"), "x")
    bias = abs(_safe_float(result.get("乖離"), "%"))
    fib = str(result.get("Fib位置", ""))
    decision = str(result.get("決策", ""))

    tech = _technical_metrics(data)

    score = (
        buy / 6 * 30
        + max(0.0, 6 - sell) / 6 * 15
    )

    score += (
        15
        if (
            str(result.get("動能")) == "放量"
            or tech["ret5"] > 3
        )
        else 6
    )

    score += min(max(vr, 0), 2.0) / 2.0 * 10

    score += (
        10
        if str(result.get("成本")) == "站穩"
        else 0
    )

    score += max(
        0.0,
        5 - max(0.0, bias - 5) * 0.5
    )

    if any(
        k in fib
        for k in ["突破前高", "近前高", "0.382支撐"]
    ):
        score += 10

    elif any(
        k in fib
        for k in ["0.500", "0.618"]
    ):
        score += 6

    else:
        score += 2

    score += (
        5
        if tech["ret5"] > 0 and tech["ret20"] > 0
        else 0
    )

    if decision in ("全導通", "看多"):
        score += 3

    if bias > 15:
        score -= min(8, (bias - 15) * 0.6)

    david = max(0.0, min(100.0, score))

    return david, tech


def json_safe(value):
    if isinstance(value, (np.bool_, bool)):
        return bool(value)

    if isinstance(value, (np.integer,)):
        return int(value)

    if isinstance(value, (np.floating, float)):
        if np.isnan(value) or np.isinf(value):
            return None
        return float(value)

    if isinstance(value, dict):
        return {str(k): json_safe(v) for k, v in value.items()}

    if isinstance(value, list):
        return [json_safe(v) for v in value]

    return value


def main():

    print("=" * 60)
    print("DAVID V13.100 GOLDEN EXPECTED BUILDER")
    print("=" * 60)

    data = load_fixture()

    fixture_sha = sha256_file(FIXTURE_PATH)

    result = analyze_stock(
        CODE,
        NAME,
        data,
        SYMBOL,
    )

    david_score, tech = _score_bundle(
        result,
        data,
    )

    fib = result["_fib"]
    raw = result["_raw"]

    expected = {
        "schema_version": 1,
        "baseline_version": "V13.100",
        "fixture_id": "golden_real_001",
        "fixture_sha256": fixture_sha,
        "symbol": SYMBOL,
        "row_count": int(len(data)),
        "first_trade_date": data.index[0].date().isoformat(),
        "last_trade_date": data.index[-1].date().isoformat(),

        "market_input": {
            "prev_close": result["昨收"],
            "open": result["開盤"],
            "high": float(data["High"].iloc[-1]),
            "low": float(data["Low"].iloc[-1]),
            "close": result["現價"],
            "volume": float(data["Volume"].iloc[-1]),
        },

        "technical": {
            "ma5": raw["ma5"],
            "ma5_previous": raw["ma5_previous"],
            "ma20": raw["ma20"],
            "vm20": raw["vm20"],
            "macd_histogram": raw["macd_histogram"],
            "mid": raw["mid"],
            "volume_ratio_raw": raw["volume_ratio"],
            "bias20_raw": raw["bias20"],
            "change_pct_raw": raw["change_pct"],
        },

        "status": {
            "early": result["早盤"],
            "momentum": result["動能"],
            "cost": result["成本"],
            "strength": result["力道"],
        },

        "six_buy": {
            "b1": raw["b1"],
            "b2": raw["b2"],
            "b3": raw["b3"],
            "b4": raw["b4"],
            "b5": raw["b5"],
            "b6": raw["b6"],
            "score": result["六買"],
        },

        "six_sell": {
            "s1": raw["s1"],
            "s2": raw["s2"],
            "s3": raw["s3"],
            "s4": raw["s4"],
            "s5": raw["s5"],
            "s6": raw["s6"],
            "score": result["六賣"],
        },

        "position": {
            "swing_high": fib["波段高"],
            "swing_low": fib["波段低"],
            "swing_direction": fib["方向"],
            "fib_0236": fib["0.236"],
            "fib_0382": fib["0.382"],
            "fib_0500": fib["0.500"],
            "fib_0618": fib["0.618"],
            "fib_0786": fib["0.786"],
            "fib_1272": fib["1.272"],
            "fib_1618": fib["1.618"],
            "fib_position": fib["Fib位置"],
        },

        "decision": {
            "core_decision": result["決策"],
        },

        "ranking": {
            "david_score_v1": david_score,
            "ret1": tech["ret1"],
            "ret5": tech["ret5"],
            "ret20": tech["ret20"],
            "technical_volume_ratio": tech["vol_ratio"],
            "new20": tech["new20"],
            "macd_flip": tech["macd_flip"],
            "ma_cross": tech["ma_cross"],
        },

        "display_reference": {
            "change": result["漲跌"],
            "change_pct": result["幅%"],
            "volume_ratio": result["量比"],
            "bias": result["乖離"],
        },

        "protection": {
            "fixture_read_only": True,
            "live_api_used": False,
            "supabase_used": False,
            "streamlit_used": False,
            "expected_overwrite_policy": "DENY_BY_DEFAULT",
        },
    }

    expected = json_safe(expected)

    EXPECTED_DIR.mkdir(parents=True, exist_ok=True)

    if EXPECTED_PATH.exists():
        raise RuntimeError(
            f"Expected file already exists: {EXPECTED_PATH}\n"
            "STOP: Golden Expected will not be overwritten."
        )

    EXPECTED_PATH.write_text(
        json.dumps(
            expected,
            ensure_ascii=False,
            indent=2,
        ) + "\n",
        encoding="utf-8",
    )

    expected_sha = sha256_file(EXPECTED_PATH)

    print()
    print("Golden Expected created successfully.")
    print(f"Fixture SHA-256:  {fixture_sha}")
    print(f"Expected:           {EXPECTED_PATH}")
    print(f"Expected SHA-256:   {expected_sha}")
    print()
    print(f"Core Decision:      {result['決策']}")
    print(f"Six Buy:            {result['六買']}")
    print(f"Six Sell:           {result['六賣']}")
    print(f"Fib Position:       {result['Fib位置']}")
    print(f"DAVID Score V1:     {david_score:.8f}")
    print()
    print("IMPORTANT:")
    print("This Expected Result is now a candidate Golden Oracle.")
    print("Do NOT commit it until manual verification is complete.")


if __name__ == "__main__":
    main()