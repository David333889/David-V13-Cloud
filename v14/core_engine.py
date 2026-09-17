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

    clean_market_input = {
        key: value
        for key, value in market_input.items()
        if key != "_data"
    }

    return CoreEngineResult(
        market_input=clean_market_input,
        technical=technical,
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