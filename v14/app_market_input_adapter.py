from typing import Any, Dict

import pandas as pd


CONTRACT_VERSION = "V14_APP_MARKET_INPUT_ADAPTER_V1"


def build_app_market_input(
    legacy_result: Any,
    data: Any,
) -> Dict[str, Any]:
    """
    Build V14 Core market_input from the existing app result
    and its source market DataFrame.

    Mapping is frozen from the verified Golden Builder:

        prev_close <- legacy_result["昨收"]
        open       <- legacy_result["開盤"]
        high       <- data["High"].iloc[-1]
        low        <- data["Low"].iloc[-1]
        close      <- legacy_result["現價"]
        volume     <- data["Volume"].iloc[-1]
        _data      <- original DataFrame

    Safety boundary:
        - pure mapping only
        - no run_core()
        - no Writer
        - no Supabase
        - no network I/O
        - does not modify legacy_result
        - does not modify data
    """

    if not isinstance(legacy_result, dict):
        raise TypeError("legacy_result must be a dictionary")

    if not isinstance(data, pd.DataFrame):
        raise TypeError("data must be a pandas DataFrame")

    if data.empty:
        raise ValueError("data must not be empty")

    required_legacy = (
        "昨收",
        "開盤",
        "現價",
    )

    for key in required_legacy:
        if key not in legacy_result:
            raise ValueError(
                f"legacy_result missing required field: {key}"
            )

    required_columns = (
        "High",
        "Low",
        "Volume",
    )

    for column in required_columns:
        if column not in data.columns:
            raise ValueError(
                f"data missing required column: {column}"
            )

    return {
        "prev_close": float(legacy_result["昨收"]),
        "open": float(legacy_result["開盤"]),
        "high": float(data["High"].iloc[-1]),
        "low": float(data["Low"].iloc[-1]),
        "close": float(legacy_result["現價"]),
        "volume": float(data["Volume"].iloc[-1]),
        "_data": data,
    }