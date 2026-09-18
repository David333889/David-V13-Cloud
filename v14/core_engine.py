"""
DAVID V14 Unified Engine
Core Engine Skeleton

Baseline:
    V13.100 Cloud

Purpose:
    Establish the V14 Core Engine contract before migrating
    any V13 production calculation logic.

IMPORTANT:
    - Do NOT change V13 six-buy / six-sell rules here yet.
    - Do NOT change V13 Pivot Fibonacci rules here yet.
    - Do NOT change V13 Core Decision rules here yet.
    - Do NOT change DAVID Score V1 rules here yet.
    - Risk and Action are NOT Core Decision.
    - This module must not use Streamlit, Supabase, or live APIs.
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Dict
import numpy as np
import pandas as pd

V14_ENGINE_VERSION = "V14_UNIFIED"
V13_BASELINE_VERSION = "V13.100"

ACTION_SPEC_PENDING = "SPEC_PENDING"


@dataclass(frozen=True)
class CoreEngineResult:
    """
    Unified output contract for the V14 Core Engine.

    Locked V13 domains:
        market_input
        technical
        status
        six_buy
        six_sell
        position
        decision
        ranking

    V14 extension domains:
        risk
        action
    """

    market_input: Dict[str, Any]
    technical: Dict[str, Any]
    status: Dict[str, Any]
    six_buy: Dict[str, Any]
    six_sell: Dict[str, Any]
    position: Dict[str, Any]
    decision: Dict[str, Any]
    ranking: Dict[str, Any]

    risk: Dict[str, Any]
    action: Dict[str, Any]

    engine_version: str = V14_ENGINE_VERSION
    baseline_version: str = V13_BASELINE_VERSION

    def to_dict(self) -> Dict[str, Any]:
        return {
            "engine_version": self.engine_version,
            "baseline_version": self.baseline_version,
            "market_input": self.market_input,
            "technical": self.technical,
            "status": self.status,
            "six_buy": self.six_buy,
            "six_sell": self.six_sell,
            "position": self.position,
            "decision": self.decision,
            "ranking": self.ranking,
            "risk": self.risk,
            "action": self.action,
        }


def build_pending_result() -> CoreEngineResult:
    """
    Temporary V14 skeleton result.

    No V13 trading calculation is performed here.

    This exists only to verify:
        1. module import
        2. output schema
        3. Core / Risk / Action separation

    Action remains SPEC_PENDING until the Action Engine
    specification is formally defined and validated.
    """

    return CoreEngineResult(
        market_input={},
        technical={},
        status={},
        six_buy={},
        six_sell={},
        position={},
        decision={},
        ranking={},
        risk={
            "state": "SPEC_PENDING",
            "reason": "V14 Risk Engine not implemented",
        },
        action={
            "state": ACTION_SPEC_PENDING,
            "reason": "V14 Action Engine not implemented",
        },
    )
def calculate_macd(close):
    """
    V13.100 MACD Histogram.
    Frozen migration from the Golden Builder.
    """
    ema12 = close.ewm(span=12, adjust=False).mean()
    ema26 = close.ewm(span=26, adjust=False).mean()

    macd_line = ema12 - ema26
    signal_line = macd_line.ewm(span=9, adjust=False).mean()

    histogram = macd_line - signal_line

    return histogram
def calculate_technical(data: pd.DataFrame) -> Dict[str, Any]:
    """
    V13.100 Technical domain migration.

    Frozen from V13.100 Core Analysis.
    Technical calculations only.

    Excludes:
    - Status
    - Six Buy / Six Sell
    - Pivot Fibonacci
    - Decision
    - DAVID Score
    """

    if data is None or data.empty or len(data) < 60:
        return {}

    close = data["Close"].astype(float)
    volume_series = data["Volume"].astype(float)

    latest = data.iloc[-1]
    previous = data.iloc[-2]

    p = float(latest["Close"])
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

    macd_hist = calculate_macd(close)
    mh = float(macd_hist.iloc[-1])

    if np.isnan(mh):
        mh = 0.0

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

    return {
        "ma5": ma5_now,
        "ma5_previous": ma5_prev,
        "ma20": ma20,
        "vm20": vm20,
        "macd_histogram": mh,
        "mid": mid,
        "volume_ratio_raw": vr,
        "bias20_raw": bias,
        "change_pct_raw": ch,
    }
def calculate_status(
    market_input: Dict[str, Any],
    technical: Dict[str, Any],
) -> Dict[str, Any]:
    """
    V13.100 Status domain migration only.

    Early / Momentum / Cost / Strength.
    No Six Buy / Six Sell.
    No Decision.
    """

    if not technical:
        return {}

    close = float(market_input["close"])
    open_price = float(market_input["open"])
    volume = float(market_input["volume"])

    change_pct = float(technical["change_pct_raw"])
    vm20 = float(technical["vm20"])
    ma20 = float(technical["ma20"])
    mid = float(technical["mid"])

    is_strong = change_pct >= 3.0

    if is_strong:
        early = "\u5f37\u653b"
    elif close > open_price:
        early = "\u5408\u683c"
    else:
        early = "\u5f85\u5b9a"

    momentum = (
        "\u653e\u91cf"
        if volume > vm20
        else "\u91cf\u7e2e"
    )

    cost = (
        "\u7ad9\u7a69"
        if close > ma20
        else "\u7834\u4f4d"
    )

    strength = (
        "\u5f37\u52e2"
        if close > mid
        else "\u5f31\u52e2"
    )

    return {
        "early": early,
        "momentum": momentum,
        "cost": cost,
        "strength": strength,
    }
def calculate_six_buy(
    market_input: Dict[str, Any],
    technical: Dict[str, Any],
) -> Dict[str, Any]:
    """
    V13.100 Six Buy V10 migration only.
    """

    if not technical:
        return {}

    p = float(market_input["close"])
    op = float(market_input["open"])
    vo = float(market_input["volume"])

    ma20 = float(technical["ma20"])
    vm20 = float(technical["vm20"])
    mid = float(technical["mid"])
    mh = float(technical["macd_histogram"])

    ma5_now = float(technical["ma5"])
    ma5_prev = float(technical["ma5_previous"])

    ma5_up = (
        not np.isnan(ma5_now)
        and not np.isnan(ma5_prev)
        and ma5_now > ma5_prev
    )

    b1 = p > op
    b2 = p > ma20
    b3 = vo > vm20
    b4 = p > mid
    b5 = ma5_up
    b6 = mh > 0

    score = sum([b1, b2, b3, b4, b5, b6])

    return {
        "b1": bool(b1),
        "b2": bool(b2),
        "b3": bool(b3),
        "b4": bool(b4),
        "b5": bool(b5),
        "b6": bool(b6),
        "score": int(score),
    }


def calculate_six_sell(
    market_input: Dict[str, Any],
    technical: Dict[str, Any],
) -> Dict[str, Any]:
    """
    V13.100 Six Sell V10 migration only.

    Important:
    s3 is NOT the inverse of b3.
    MACD == 0 belongs to s6.
    """

    if not technical:
        return {}

    p = float(market_input["close"])
    op = float(market_input["open"])
    vo = float(market_input["volume"])
    pc = float(market_input["prev_close"])

    ma20 = float(technical["ma20"])
    vm20 = float(technical["vm20"])
    mid = float(technical["mid"])
    mh = float(technical["macd_histogram"])

    ma5_now = float(technical["ma5"])
    ma5_prev = float(technical["ma5_previous"])

    ma5_up = (
        not np.isnan(ma5_now)
        and not np.isnan(ma5_prev)
        and ma5_now > ma5_prev
    )

    s1 = p < op
    s2 = p < ma20
    s3 = vo > vm20 and p < pc
    s4 = p < mid
    s5 = not ma5_up
    s6 = mh <= 0

    score = sum([s1, s2, s3, s4, s5, s6])

    return {
        "s1": bool(s1),
        "s2": bool(s2),
        "s3": bool(s3),
        "s4": bool(s4),
        "s5": bool(s5),
        "s6": bool(s6),
        "score": int(score),
    }
def calculate_position(
    data: pd.DataFrame,
    lookback: int = 120,
    left: int = 3,
    right: int = 3,
) -> Dict[str, Any]:
    """
    V13.100 Pivot Swing + Fibonacci migration.

    Position domain only.
    No Decision.
    No Ranking.
    """

    if (
        data is None
        or data.empty
        or len(data) < left + right + 20
    ):
        return {}

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
        return {}

    if low_idx < high_idx:
        swing_direction = "\u591a\u982d\u6ce2\u6bb5"

        levels = {
            "fib_0236": swing_high - wave * 0.236,
            "fib_0382": swing_high - wave * 0.382,
            "fib_0500": swing_high - wave * 0.500,
            "fib_0618": swing_high - wave * 0.618,
            "fib_0786": swing_high - wave * 0.786,
            "fib_1272": swing_high + wave * 0.272,
            "fib_1618": swing_high + wave * 0.618,
        }

        if close_now > swing_high:
            fib_position = "\u7a81\u7834\u524d\u9ad8"
        elif close_now >= levels["fib_0236"]:
            fib_position = "0.236\u58d3\u529b"
        elif close_now >= levels["fib_0382"]:
            fib_position = "0.382\u58d3\u529b"
        elif close_now >= levels["fib_0500"]:
            fib_position = "0.500\u58d3\u529b"
        elif close_now >= levels["fib_0618"]:
            fib_position = "0.618\u58d3\u529b"
        elif close_now >= levels["fib_0786"]:
            fib_position = "0.786\u58d3\u529b"
        else:
            fib_position = "\u8dcc\u7834 0.786"

    else:
        swing_direction = "\u7a7a\u982d\u6ce2\u6bb5"

        levels = {
            "fib_0236": swing_low + wave * 0.236,
            "fib_0382": swing_low + wave * 0.382,
            "fib_0500": swing_low + wave * 0.500,
            "fib_0618": swing_low + wave * 0.618,
            "fib_0786": swing_low + wave * 0.786,
            "fib_1272": swing_low - wave * 0.272,
            "fib_1618": swing_low - wave * 0.618,
        }

        if close_now < swing_low:
            fib_position = "\u8dcc\u7834\u524d\u4f4e"
        elif close_now <= levels["fib_0236"]:
            fib_position = "0.236\u652f\u6490"
        elif close_now <= levels["fib_0382"]:
            fib_position = "0.382\u58d3\u529b"
        elif close_now <= levels["fib_0500"]:
            fib_position = "0.500\u58d3\u529b"
        elif close_now <= levels["fib_0618"]:
            fib_position = "0.618\u58d3\u529b"
        elif close_now <= levels["fib_0786"]:
            fib_position = "0.786\u58d3\u529b"
        else:
            fib_position = "\u7a81\u7834 0.786"

    return {
        "swing_high": swing_high,
        "swing_low": swing_low,
        "swing_direction": swing_direction,
        **levels,
        "fib_position": fib_position,
    }
def calculate_decision(
    six_buy: Dict[str, Any],
    six_sell: Dict[str, Any],
) -> Dict[str, Any]:
    """
    V13.100 Core Decision migration only.

    Priority is frozen:
    1. Buy score == 6
    2. Sell score == 6
    3. Buy score >= 4
    4. Sell score >= 4
    5. Otherwise observe
    """

    if not six_buy or not six_sell:
        return {}

    b_score = int(six_buy["score"])
    s_score = int(six_sell["score"])

    if b_score == 6:
        core_decision = "\u5f37\u529b\u8cb7\u9032"
    elif s_score == 6:
        core_decision = "\u5f37\u529b\u8ce3\u51fa"
    elif b_score >= 4:
        core_decision = "\u504f\u591a"
    elif s_score >= 4:
        core_decision = "\u504f\u7a7a"
    else:
        core_decision = "\u89c0\u671b"

    return {
        "core_decision": core_decision,
    }

def calculate_ranking_metrics(
    data: pd.DataFrame,
) -> Dict[str, Any]:
    """
    V13.100 DAVID Score V1 technical metrics.

    Metrics only.
    No DAVID Score calculation here.
    """

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

        prior20_high = float(
            close.iloc[-21:-1].max()
        )

        m["new20"] = (
            float(close.iloc[-1]) >= prior20_high
        )

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
def calculate_ranking(
    data: pd.DataFrame,
    technical: Dict[str, Any],
    status: Dict[str, Any],
    six_buy: Dict[str, Any],
    six_sell: Dict[str, Any],
    position: Dict[str, Any],
    decision: Dict[str, Any],
) -> Dict[str, Any]:
    """
    V13.100 DAVID Score V1 migration.
    Ranking domain only.
    """

    if (
        data is None
        or data.empty
        or not technical
        or not status
        or not six_buy
        or not six_sell
        or not position
        or not decision
    ):
        return {}

    tech = calculate_ranking_metrics(data)

    buy = float(six_buy["score"])
    sell = float(six_sell["score"])

    vr = round(float(technical["volume_ratio_raw"]), 1)
    bias = abs(round(float(technical["bias20_raw"]), 1))

    fib = str(position["fib_position"])
    core_decision = str(decision["core_decision"])

    score = (
        buy / 6 * 30
        + max(0.0, 6 - sell) / 6 * 15
    )

    score += (
        15
        if (
            str(status["momentum"]) == "\u653e\u91cf"
            or tech["ret5"] > 3
        )
        else 6
    )

    score += min(max(vr, 0), 2.0) / 2.0 * 10

    score += (
        10
        if str(status["cost"]) == "\u7ad9\u7a69"
        else 0
    )

    score += max(
        0.0,
        5 - max(0.0, bias - 5) * 0.5
    )

    if any(
        k in fib
        for k in [
            "\u7a81\u7834\u524d\u9ad8",
            "\u8fd1\u524d\u9ad8",
            "0.382\u652f\u6490",
        ]
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

    if core_decision in (
        "\u5f37\u529b\u8cb7\u9032",
        "\u504f\u591a",
    ):
        score += 3

    if bias > 15:
        score -= min(
            8,
            (bias - 15) * 0.6
        )

    david = max(
        0.0,
        min(100.0, score)
    )

    return {
        "david_score_v1": david,
        "ret1": tech["ret1"],
        "ret5": tech["ret5"],
        "ret20": tech["ret20"],
        "technical_volume_ratio": tech["vol_ratio"],
        "new20": tech["new20"],
        "macd_flip": tech["macd_flip"],
        "ma_cross": tech["ma_cross"],
    }
def run_core(market_input: Dict[str, Any]) -> CoreEngineResult:
    """
    V14 Unified Core Engine entry point.

    Phase 1:
    Accept Market Input from the caller only.

    IMPORTANT:
    - No live API.
    - No Supabase.
    - No Streamlit.
    - No V13 formula is changed here.
    - Remaining V13 locked domains stay pending
      until migrated and verified by Gate 3.
    """

    if not isinstance(market_input, dict):
        raise TypeError("market_input must be a dictionary")

    data = market_input.get("_data")

    technical = (
        calculate_technical(data)
        if isinstance(data, pd.DataFrame)
        else {}
    )
    status = calculate_status(
        market_input,
        technical,
    )
    six_buy = calculate_six_buy(
        market_input,
        technical,
    )

    six_sell = calculate_six_sell(
        market_input,
        technical,
    )
    position = (
        calculate_position(data)
        if isinstance(data, pd.DataFrame)
        else {}
    )
    decision = calculate_decision(
        six_buy,
        six_sell,
    )
    ranking = (
        calculate_ranking(
            data,
            technical,
            status,
            six_buy,
            six_sell,
            position,
            decision,
        )
        if isinstance(data, pd.DataFrame)
        else {}
    )
    clean_market_input = {
        key: value
        for key, value in market_input.items()
        if key != "_data"
    }

    return CoreEngineResult(
        market_input=clean_market_input,
        technical=technical,
        status=status,
        six_buy=six_buy,
        six_sell=six_sell,
        position=position,
        decision=decision,
        ranking=ranking,
        risk={
            "state": "SPEC_PENDING",
            "reason": "V14 Risk Engine not implemented",
        },
        action={
            "state": ACTION_SPEC_PENDING,
            "reason": "V14 Action Engine not implemented",
        },
    )


def engine_contract() -> Dict[str, Any]:
    """
    Return the V14 Core Engine contract.

    This function intentionally contains no trading logic.
    """

    return {
        "engine_version": V14_ENGINE_VERSION,
        "baseline_version": V13_BASELINE_VERSION,

        "locked_v13_domains": [
            "market_input",
            "technical",
            "status",
            "six_buy",
            "six_sell",
            "position",
            "decision",
            "ranking",
        ],

        "v14_extension_domains": [
            "risk",
            "action",
        ],

        "rules": {
            "six_buy_sell_locked": True,
            "pivot_fib_locked": True,
            "core_decision_locked": True,
            "david_score_v1_locked": True,
            "risk_is_not_decision": True,
            "action_is_not_decision": True,
            "live_api_allowed": False,
            "supabase_allowed": False,
            "streamlit_allowed": False,
        },
    }


if __name__ == "__main__":
    contract = engine_contract()
    pending = build_pending_result()

    print("=" * 64)
    print("DAVID V14 UNIFIED ENGINE - CORE SKELETON")
    print("=" * 64)
    print()
    print(f"Engine Version:   {contract['engine_version']}")
    print(f"Baseline Version: {contract['baseline_version']}")
    print()
    print("Locked V13 Domains:")
    for domain in contract["locked_v13_domains"]:
        print(f"  - {domain}")

    print()
    print("V14 Extension Domains:")
    for domain in contract["v14_extension_domains"]:
        print(f"  - {domain}")

    print()
    print(f"Risk State:   {pending.risk['state']}")
    print(f"Action State: {pending.action['state']}")
    print()
    print("NO V13 CORE FORMULA HAS BEEN MODIFIED.")
    print("CORE ENGINE SKELETON: READY")