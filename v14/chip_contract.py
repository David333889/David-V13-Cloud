from copy import deepcopy
from typing import Any, Dict, List


CONTRACT_VERSION = "V14_NORMALIZED_CHIP_DATA_V1"

_REQUIRED_INSTITUTIONAL = (
    "foreign",
    "investment_trust",
    "dealer_self",
    "dealer_hedging",
)


def normalize_chip_data(raw: Dict[str, Any]) -> Dict[str, Any]:
    """
    Gate 22 - Normalized Chip Data Contract V1.

    Contract only:
    - preserve identity
    - preserve raw institutional evidence
    - keep dealer_self / dealer_hedging separated
    - preserve financing evidence
    - preserve securities-lending transaction evidence
    - preserve day-trade raw evidence
    - missing != zero != neutral
    - attach source / freshness / status / missing_fields
    - emit no derived Chip / Decision / Risk / Action signal
    """

    if not isinstance(raw, dict):
        raise TypeError("raw chip data must be dict")

    identity = {
        "code": raw.get("code"),
        "market": raw.get("market"),
        "trade_date": raw.get("trade_date"),
    }

    raw_institutional = raw.get("institutional")
    if not isinstance(raw_institutional, dict):
        raw_institutional = {}

    institutional: Dict[str, Any] = {}
    missing_fields: List[str] = []

    for key in _REQUIRED_INSTITUTIONAL:
        value = raw_institutional.get(key)

        if value is None:
            institutional[key] = None
            missing_fields.append(f"institutional.{key}")
        else:
            institutional[key] = deepcopy(value)

    financing = deepcopy(raw.get("financing"))
    securities_lending = deepcopy(raw.get("securities_lending"))
    day_trade = deepcopy(raw.get("day_trade"))

    if financing is None:
        missing_fields.append("financing")

    if securities_lending is None:
        missing_fields.append("securities_lending")

    if day_trade is None:
        missing_fields.append("day_trade")

    raw_metadata = raw.get("metadata")
    if not isinstance(raw_metadata, dict):
        raw_metadata = {}

    metadata = {
        "source": raw_metadata.get("source"),
        "freshness": raw_metadata.get("freshness"),
        "status": "MISSING" if missing_fields else "READY",
        "missing_fields": missing_fields,
    }

    return {
        "version": CONTRACT_VERSION,
        "identity": identity,
        "institutional": institutional,
        "financing": financing,
        "securities_lending": securities_lending,
        "day_trade": day_trade,
        "metadata": metadata,
    }
