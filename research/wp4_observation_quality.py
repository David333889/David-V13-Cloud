"""Offline synthetic observation-quality experiment; no source authorization."""
from math import isfinite

from research.wp4_relative_strength import compare_candidate_metrics


def _deny(reason):
    return {
        "allowed": False, "reason": reason, "research_only": True,
        "signal_emitted": False, "ranking_emitted": False,
        "market_state_emitted": False, "source_verified": False,
    }


def compare_quality_checked_candidates(stock, benchmark, lookback):
    """Require synthetic, explicitly observed prices paired to raw dates.

    raw_close is synthetic fixture metadata, not authenticated provider evidence.
    Equal successive closes are not evidence that a price was carried forward.
    This experiment neither validates corporate-action factors nor authorizes use.
    """
    result = compare_candidate_metrics(stock, benchmark, lookback)
    if not result["allowed"]:
        return _deny(result["reason"])
    for series in (stock, benchmark):
        raw_records = series.get("raw_records")
        records = series["records"]
        if not isinstance(raw_records, list) or len(raw_records) != len(records):
            return _deny("RAW_WINDOW_REQUIRED")
        for record, raw in zip(records, raw_records):
            if not isinstance(raw, dict):
                return _deny("RAW_RECORD_INVALID")
            if raw.get("trading_date") != record["trading_date"]:
                return _deny("RAW_DATE_MISMATCH")
            status = record.get("observation_status")
            if status == "CARRIED":
                return _deny("CARRIED_PRICE_REJECTED")
            if status == "MISSING":
                return _deny("MISSING_PRICE_REJECTED")
            if status != "OBSERVED":
                return _deny("OBSERVATION_STATUS_REQUIRED")
            raw_close = raw.get("close")
            if isinstance(raw_close, bool) or not isinstance(raw_close, (int, float)):
                return _deny("RAW_CLOSE_INVALID")
            try:
                if not isfinite(raw_close) or raw_close < 0:
                    return _deny("RAW_CLOSE_INVALID")
            except OverflowError:
                return _deny("RAW_CLOSE_INVALID")
            if raw_close == 0:
                return _deny("NO_ANNOUNCED_PRICE")
    result.update(quality_contract="SYNTHETIC_OBSERVATION_PREFLIGHT_V1",
                  source_verified=False)
    return result
