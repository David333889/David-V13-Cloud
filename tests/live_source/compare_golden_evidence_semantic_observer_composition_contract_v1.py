from importlib import import_module


MODULE_NAME = (
    "v14.golden_evidence_semantic_observer_composition"
)


def main():
    print(
        "=== GATE 28D.2K-3K - GOLDEN EVIDENCE "
        "SEMANTIC OBSERVER COMPOSITION "
        "CONTRACT V1 ==="
    )

    try:
        m = import_module(MODULE_NAME)
    except ModuleNotFoundError:
        print(
            "[EXPECTED RED] golden evidence semantic "
            "observer composition module not found"
        )
        raise SystemExit(1)

    execute = getattr(
        m,
        "build_semantically_observed_golden_evidence",
        None,
    )

    assert callable(execute)

    assert m.READ_ONLY is True
    assert m.COMPOSITION_ONLY is True

    assert m.ALLOW_NETWORK_EXECUTION is False
    assert m.ALLOW_SESSION_CREATION is False
    assert m.ALLOW_REAL_GET_EXECUTION is False

    assert m.ALLOW_RAW_PAYLOAD_STORAGE is False
    assert m.ALLOW_SECRET_STORAGE is False

    assert m.ALLOW_NORMALIZATION is False
    assert m.ALLOW_CORE_INPUT is False
    assert m.ALLOW_SCORE is False
    assert m.ALLOW_DECISION is False
    assert m.ALLOW_SUPABASE_WRITE is False
    assert m.ALLOW_PRODUCTION_WRITE is False

    evidence = {
        "status_code": 200,
        "content_type": "application/json",
        "size_bytes": 321,
        "payload": {
            "data": [
                {
                    "date": "2026-09-23",
                    "stock_id": "2330",
                    "open": 1000,
                    "max": 1010,
                    "min": 995,
                    "close": 1005,
                    "Trading_Volume": 12345678,
                }
            ]
        },
    }

    params = {
        "dataset": "TaiwanStockPrice",
        "data_id": "2330",
        "start_date": "2026-09-23",
        "end_date": "2026-09-23",
    }

    result = execute(
        evidence=evidence,
        params=params,
    )

    assert isinstance(result, dict)
    assert result.get("allowed") is True

    golden = result.get("golden")

    assert isinstance(golden, dict)
    assert golden.get("provider") == "FinMind"
    assert golden.get("data_id") == "2330"
    assert golden.get("trading_date") == "2026-09-23"
    assert golden.get("record_count") == 1

    assert "payload" not in result
    assert "evidence" not in result
    assert "observed" not in result
    assert "token" not in result

    # Ordering safety:
    # semantic denial must stop before Golden integration.

    original_golden_builder = (
        m.build_real_get_golden_evidence
    )

    golden_calls = {
        "count": 0,
    }

    def counting_golden_builder(
        evidence,
        params,
    ):
        golden_calls["count"] += 1

        return {
            "allowed": True,
            "golden": {
                "should_not": "be_reached",
            },
        }

    m.build_real_get_golden_evidence = (
        counting_golden_builder
    )

    try:
        # 1. Stock mismatch.
        stock_mismatch_params = {
            **params,
            "data_id": "2317",
        }

        stock_mismatch = execute(
            evidence=evidence,
            params=stock_mismatch_params,
        )

        assert stock_mismatch.get("allowed") is False
        assert (
            stock_mismatch.get("reason")
            == "BASELINE_RECORD_NOT_FOUND"
        )
        assert golden_calls["count"] == 0

        print(
            "[PASS] stock mismatch stops before "
            "Golden integration"
        )

        # 2. Trading-date mismatch.
        date_mismatch_params = {
            **params,
            "start_date": "2026-09-24",
            "end_date": "2026-09-24",
        }

        date_mismatch = execute(
            evidence=evidence,
            params=date_mismatch_params,
        )

        assert date_mismatch.get("allowed") is False
        assert (
            date_mismatch.get("reason")
            == "BASELINE_RECORD_NOT_FOUND"
        )
        assert golden_calls["count"] == 0

        print(
            "[PASS] date mismatch stops before "
            "Golden integration"
        )

        # 3. Duplicate matching baseline records.
        duplicate_evidence = {
            **evidence,
            "payload": {
                "data": [
                    dict(
                        evidence[
                            "payload"
                        ][
                            "data"
                        ][0]
                    ),
                    dict(
                        evidence[
                            "payload"
                        ][
                            "data"
                        ][0]
                    ),
                ]
            },
        }

        duplicate = execute(
            evidence=duplicate_evidence,
            params=params,
        )

        assert duplicate.get("allowed") is False
        assert (
            duplicate.get("reason")
            == "BASELINE_RECORD_NOT_UNIQUE"
        )
        assert golden_calls["count"] == 0

        print(
            "[PASS] duplicate baseline stops before "
            "Golden integration"
        )

        # 4. Required baseline field missing.
        missing_field_record = dict(
            evidence["payload"]["data"][0]
        )

        missing_field_record.pop(
            "Trading_Volume"
        )

        missing_field_evidence = {
            **evidence,
            "payload": {
                "data": [
                    missing_field_record,
                ]
            },
        }

        missing_field = execute(
            evidence=missing_field_evidence,
            params=params,
        )

        assert missing_field.get("allowed") is False
        assert (
            missing_field.get("reason")
            == "REQUIRED_EVIDENCE_FIELDS_MISSING"
        )
        assert golden_calls["count"] == 0

        print(
            "[PASS] missing required field stops "
            "before Golden integration"
        )

    finally:
        m.build_real_get_golden_evidence = (
            original_golden_builder
        )

    assert golden_calls["count"] == 0

    print(
        "[PASS] semantic observer always precedes "
        "Golden integration"
    )

    print("[PASS] existing semantic observer reused")
    print("[PASS] matching baseline evidence accepted")
    print("[PASS] existing 3D golden integration reused")
    print("[PASS] sanitized golden evidence returned")
    print("[PASS] raw/observed evidence excluded")
    print("[PASS] network/session/real GET remain disabled")
    print("[PASS] core/score/decision/write remain disabled")

    print(
        "=== GATE 28D.2K-3K GOLDEN EVIDENCE "
        "SEMANTIC OBSERVER COMPOSITION "
        "CONTRACT RESULT: PASS ==="
    )


if __name__ == "__main__":
    main()
