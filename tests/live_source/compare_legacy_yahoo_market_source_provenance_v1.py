# Gate 28D.2J - Legacy Yahoo Market Source Provenance Contract V1.
#
# Provenance contract only.
# Describes the existing legacy Yahoo/yfinance source path.
# No live fetch, new fetch path, normalization,
# compatibility establishment, provider switching,
# Core input, scoring, decision, or persistence.

import v14.legacy_yahoo_market_source_provenance as module


def main():
    assert module.READ_ONLY is True

    assert module.PROVIDER == "Yahoo"
    assert module.CLIENT == "yfinance"

    assert module.PRIMARY_FETCH == "yf.download"

    assert module.FALLBACK_FETCH == (
        "yf.download",
        "yf.Ticker.history",
    )

    assert module.PERIOD == "1y"
    assert module.INTERVAL == "1d"
    assert module.AUTO_ADJUST is False

    assert (
        module.CLEANING_BOUNDARY
        == "_clean_history_frame"
    )

    assert module.REQUIRED_COLUMNS == (
        "Open",
        "High",
        "Low",
        "Close",
        "Volume",
    )

    assert (
        module.FETCH_PATH_PROVENANCE_REQUIRED
        is True
    )

    assert (
        module.CLEANED_DATA_IS_RAW_PAYLOAD
        is False
    )

    assert module.ALLOW_PROVENANCE_DESCRIPTION is True

    assert module.ALLOW_LIVE_FETCH is False
    assert module.ALLOW_NEW_FETCH_PATH is False
    assert module.ALLOW_NORMALIZATION is False
    assert (
        module.ALLOW_COMPATIBILITY_ESTABLISHMENT
        is False
    )
    assert module.ALLOW_PROVIDER_SWITCH is False
    assert module.ALLOW_CORE_INPUT is False
    assert module.ALLOW_ENGINE_FORMULA_CHANGE is False
    assert module.ALLOW_SCORE is False
    assert module.ALLOW_DECISION is False
    assert module.ALLOW_SUPABASE_WRITE is False
    assert module.ALLOW_PRODUCTION_WRITE is False

    contract = (
        module.get_legacy_yahoo_market_source_provenance()
    )

    assert contract["provider"] == "Yahoo"
    assert contract["client"] == "yfinance"

    assert contract["primary_fetch"] == "yf.download"

    assert contract["fallback_fetch"] == (
        "yf.download",
        "yf.Ticker.history",
    )

    assert contract["period"] == "1y"
    assert contract["interval"] == "1d"
    assert contract["auto_adjust"] is False

    assert (
        contract["cleaning_boundary"]
        == "_clean_history_frame"
    )

    assert contract["required_columns"] == (
        "Open",
        "High",
        "Low",
        "Close",
        "Volume",
    )

    assert (
        contract["fetch_path_provenance_required"]
        is True
    )

    assert (
        contract["cleaned_data_is_raw_payload"]
        is False
    )

    assert contract["read_only"] is True
    assert (
        contract["allow_provenance_description"]
        is True
    )

    assert contract["allow_live_fetch"] is False
    assert contract["allow_new_fetch_path"] is False
    assert contract["allow_normalization"] is False

    assert (
        contract["allow_compatibility_establishment"]
        is False
    )

    assert contract["allow_provider_switch"] is False
    assert contract["allow_core_input"] is False

    assert (
        contract["allow_engine_formula_change"]
        is False
    )

    assert contract["allow_score"] is False
    assert contract["allow_decision"] is False
    assert contract["allow_supabase_write"] is False
    assert contract["allow_production_write"] is False

    print(
        "LEGACY YAHOO MARKET SOURCE "
        "PROVENANCE CONTRACT V1: PASS"
    )


if __name__ == "__main__":
    main()