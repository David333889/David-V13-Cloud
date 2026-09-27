# Gate 28D.2H - FinMind Market Source Adapter Boundary Contract V1.
#
# Contract comparator only.
# The adapter boundary may validate/preserve raw evidence,
# but must not normalize market data or cross into Core/production.

from v14.finmind_market_source_adapter_boundary import (
    get_finmind_market_source_adapter_boundary,
)


EXPECTED_CONTRACT_VERSION = (
    "V14_FINMIND_MARKET_SOURCE_ADAPTER_BOUNDARY_V1"
)


def main():
    contract = get_finmind_market_source_adapter_boundary()

    assert contract["contract_version"] == EXPECTED_CONTRACT_VERSION

    assert contract["provider"] == "FinMind"
    assert contract["dataset"] == "TaiwanStockPrice"

    assert contract["read_only"] is True

    assert contract["allow_raw_validation"] is True
    assert contract["allow_raw_evidence_preservation"] is True

    assert contract["allow_timestamp_normalization"] is False
    assert contract["allow_volume_normalization"] is False
    assert contract["allow_normalized_output"] is False

    assert contract["allow_core_input"] is False
    assert contract["allow_score"] is False
    assert contract["allow_decision"] is False

    assert contract["allow_provider_switch"] is False
    assert contract["allow_v13_core_switch"] is False

    assert contract["allow_supabase_write"] is False
    assert contract["allow_production_write"] is False

    assert contract["zero_missing_policy"] == (
        "ZERO_IS_NOT_MISSING"
    )

    assert contract["no_published_price_policy"] == (
        "VOLUME_POSITIVE_DOES_NOT_PROVE_VALID_PRICE"
    )

    assert contract["trading_date_semantic"] == "TRADING_DATE"
    assert contract["finmind_timezone_status"] == (
        "TIMEZONE_PENDING"
    )

    assert contract["trading_volume_semantic"] == (
        "TRADED_SHARE_COUNT"
    )
    assert contract["yahoo_volume_compatibility"] == (
        "COMPATIBILITY_PENDING"
    )

    assert contract["normalized_timestamp_status"] == "BLOCKED"
    assert contract["normalized_volume_status"] == "BLOCKED"

    print(
        "FINMIND MARKET SOURCE ADAPTER BOUNDARY V1: PASS"
    )


if __name__ == "__main__":
    main()