# Gate 28D.2K-2B - FinMind Baseline Evidence Observer V1.
#
# Read-only baseline evidence observation only.
# No live fetch, normalization, compatibility establishment,
# provider switching, Core input, scoring, decision,
# or persistence.

from v14.finmind_baseline_evidence_observation import (
    REQUIRED_EVIDENCE_FIELDS,
)
from v14.live_fetch_safety import (
    classify_fetch_response,
)


READ_ONLY = True

ALLOW_LIVE_FETCH = False
ALLOW_NORMALIZATION = False
ALLOW_COMPATIBILITY_ESTABLISHMENT = False
ALLOW_PROVIDER_SWITCH = False
ALLOW_CORE_INPUT = False
ALLOW_SCORE = False
ALLOW_DECISION = False
ALLOW_SUPABASE_WRITE = False
ALLOW_PRODUCTION_WRITE = False


def _deny(reason):
    return {
        "allowed": False,
        "reason": reason,
    }


def observe_finmind_baseline_evidence(
    evidence,
    stock_id,
    trading_date,
):
    """
    Observe one FinMind baseline record from RAW_EVIDENCE.

    The function accepts already-fetched RAW_EVIDENCE only.
    It does not perform a network request.

    Public output contains only the exact baseline evidence
    fields defined by the observation contract.
    """

    classification = classify_fetch_response(
        evidence,
    )

    if classification != "RAW_EVIDENCE":
        return _deny(classification)

    if not isinstance(stock_id, str) or not stock_id:
        return _deny("STOCK_ID_REQUIRED")

    if not isinstance(trading_date, str) or not trading_date:
        return _deny("TRADING_DATE_REQUIRED")

    payload = evidence.get("payload")
    data = payload.get("data")

    matches = [
        record
        for record in data
        if isinstance(record, dict)
        and record.get("stock_id") == stock_id
        and record.get("date") == trading_date
    ]

    if len(matches) == 0:
        return _deny("BASELINE_RECORD_NOT_FOUND")

    if len(matches) != 1:
        return _deny("BASELINE_RECORD_NOT_UNIQUE")

    record = matches[0]

    if not all(
        field in record
        for field in REQUIRED_EVIDENCE_FIELDS
    ):
        return _deny("REQUIRED_EVIDENCE_FIELDS_MISSING")

    observed = {
        field: record[field]
        for field in REQUIRED_EVIDENCE_FIELDS
    }

    return {
        "allowed": True,
        "observed": observed,
    }
