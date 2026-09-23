from copy import deepcopy
from typing import Any, Dict


def adapt_chip_source_data(source: Dict[str, Any]) -> Dict[str, Any]:
    """
    Gate 24 - Chip Source Adapter V1.

    Source mapping only:
    - map official-shaped institutional categories to Gate 22 canonical raw keys
    - preserve financing raw evidence
    - preserve securities-lending transaction evidence
    - preserve day-trading raw evidence
    - preserve real zero
    - do not assume unknown units
    - emit no derived Chip / Decision / Risk / Action signal
    """

    if not isinstance(source, dict):
        raise TypeError("chip source data must be dict")

    raw_institutional = source.get("institutional")
    if not isinstance(raw_institutional, dict):
        raw_institutional = {}

    institutional = {
        "foreign": deepcopy(raw_institutional.get("Foreign_Investor")),
        "investment_trust": deepcopy(
            raw_institutional.get("Investment_Trust")
        ),
        "dealer_self": deepcopy(raw_institutional.get("Dealer_self")),
        "dealer_hedging": deepcopy(
            raw_institutional.get("Dealer_Hedging")
        ),
    }

    raw_metadata = source.get("metadata")
    if not isinstance(raw_metadata, dict):
        raw_metadata = {}

    return {
        "code": source.get("code"),
        "market": source.get("market"),
        "trade_date": source.get("trade_date"),
        "institutional": institutional,
        "financing": deepcopy(source.get("financing")),
        "securities_lending": deepcopy(
            source.get("securities_lending")
        ),
        "day_trade": deepcopy(source.get("day_trade")),
        "metadata": {
            "source": raw_metadata.get("source"),
            "freshness": raw_metadata.get("freshness"),
        },
    }
