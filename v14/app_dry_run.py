from typing import Any, Dict

import pandas as pd

from v14.app_market_input_adapter import build_app_market_input
from v14.core_engine import run_core
from v14.runtime_pipeline import build_runtime_persistence


CONTRACT_VERSION = "V14_APP_DRY_RUN_PIPELINE_V1"


def _result(
    state: str,
    reason: str,
) -> Dict[str, Any]:
    return {
        "version": CONTRACT_VERSION,
        "state": state,
        "reason": reason,
        "row": None,
    }


def run_app_dry_run(
    legacy_result: Any,
    data: Any,
    code: Any,
    name: Any,
    market: Any,
    symbol: Any,
) -> Dict[str, Any]:
    """
    V14 App Dry-Run Pipeline V1.

    Flow:
        Legacy Result + DataFrame
            -> App Market Input Adapter V1
            -> run_core()
            -> V14 Core Result
            -> Identity
            -> Runtime Pipeline V1
            -> Persistence Result
            -> STOP

    Safety boundary:
        - no app.py modification
        - no Runtime Writer
        - no Supabase Writer
        - no Supabase client
        - no network I/O
        - no production write
    """

    if not isinstance(data, pd.DataFrame):
        return _result(
            "BLOCKED",
            "INVALID_DATA_TYPE",
        )

    if data.empty:
        return _result(
            "BLOCKED",
            "EMPTY_DATA",
        )

    try:
        trade_date = (
            pd.Timestamp(data.index[-1])
            .date()
            .isoformat()
        )
    except Exception:
        return _result(
            "BLOCKED",
            "INVALID_TRADE_DATE",
        )

    identity_values = {
        "code": code,
        "name": name,
        "market": market,
        "symbol": symbol,
    }

    for key, value in identity_values.items():
        if value is None or str(value).strip() == "":
            return _result(
                "BLOCKED",
                f"IDENTITY_{key.upper()}_MISSING",
            )

    identity = {
        "trade_date": trade_date,
        "code": str(code),
        "name": str(name),
        "market": str(market),
        "symbol": str(symbol),
    }

    try:
        market_input = build_app_market_input(
            legacy_result,
            data,
        )

        core_result = run_core(
            market_input
        )

        return build_runtime_persistence(
            core_result.to_dict(),
            identity,
        )

    except Exception as exc:
        return _result(
            "BLOCKED",
            f"APP_DRY_RUN_EXCEPTION:{type(exc).__name__}",
        )