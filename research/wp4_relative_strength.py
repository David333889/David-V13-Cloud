"""Candidate relative-strength metrics for declared synthetic series only.

This is a research comparison, not a locked WP4 formula or market signal.
No provider, production engine, persistence, or network boundary is imported.
"""
from datetime import date
from math import isfinite


def _deny(reason):
    return {"allowed": False, "reason": reason, "signal_emitted": False}


def _validate_series(series, lookback):
    if not isinstance(series, dict) or series.get("synthetic_only") is not True:
        return None, "SYNTHETIC_RESEARCH_ONLY"
    adjustment = series.get("adjustment_type")
    if not isinstance(adjustment, str) or not adjustment.strip():
        return None, "ADJUSTMENT_METADATA_REQUIRED"
    records = series.get("records")
    if not isinstance(records, list) or len(records) != lookback + 1:
        return None, "EXACT_WINDOW_REQUIRED"
    validated = []
    for record in records:
        if not isinstance(record, dict):
            return None, "RECORD_INVALID"
        trading_date = record.get("trading_date")
        if not isinstance(trading_date, str):
            return None, "DATE_INVALID"
        try:
            parsed = date.fromisoformat(trading_date)
        except ValueError:
            return None, "DATE_INVALID"
        if parsed.isoformat() != trading_date:
            return None, "DATE_INVALID"
        if validated and parsed <= validated[-1][0]:
            return None, "DATES_NOT_STRICTLY_INCREASING"
        close = record.get("close")
        if isinstance(close, bool) or not isinstance(close, (int, float)) or close <= 0:
            return None, "CLOSE_INVALID"
        try:
            if not isfinite(close):
                return None, "CLOSE_INVALID"
        except OverflowError:
            return None, "CLOSE_INVALID"
        validated.append((parsed, close))
    return (adjustment, validated), None


def compare_candidate_metrics(stock, benchmark, lookback):
    """Require an explicit observation-interval count and exact shared date grid.

    No filling, filtering, ranking, classification, or raw-date conversion occurs.
    Declared synthetic input is a research convention, not source verification.
    """
    if type(lookback) is not int or lookback < 1:
        return _deny("LOOKBACK_INVALID")
    stock_data, reason = _validate_series(stock, lookback)
    if reason:
        return _deny(reason)
    benchmark_data, reason = _validate_series(benchmark, lookback)
    if reason:
        return _deny(reason)
    stock_adjustment, stock_records = stock_data
    benchmark_adjustment, benchmark_records = benchmark_data
    if stock_adjustment != benchmark_adjustment:
        return _deny("ADJUSTMENT_MISMATCH")
    if [x[0] for x in stock_records] != [x[0] for x in benchmark_records]:
        return _deny("DATE_GRID_MISMATCH")
    try:
        stock_gross = stock_records[-1][1] / stock_records[0][1]
        benchmark_gross = benchmark_records[-1][1] / benchmark_records[0][1]
        if stock_gross <= 0 or benchmark_gross <= 0:
            return _deny("METRIC_NOT_FINITE")
        difference = stock_gross - benchmark_gross
        gross_relative = stock_gross / benchmark_gross - 1
    except (OverflowError, ZeroDivisionError):
        return _deny("METRIC_NOT_FINITE")
    if not all(isfinite(x) for x in (stock_gross, benchmark_gross, difference, gross_relative)):
        return _deny("METRIC_NOT_FINITE")
    return {
        "allowed": True,
        "research_only": True,
        "synthetic_only": True,
        "spec_status": "CANDIDATE_COMPARISON_ONLY",
        "lookback_intervals": lookback,
        "start_date": stock_records[0][0].isoformat(),
        "end_date": stock_records[-1][0].isoformat(),
        "stock_return": stock_gross - 1,
        "benchmark_return": benchmark_gross - 1,
        "return_difference": difference,
        "gross_relative_return": gross_relative,
        "signal_emitted": False,
        "ranking_emitted": False,
        "market_state_emitted": False,
    }
