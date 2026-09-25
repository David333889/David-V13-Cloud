import importlib


def main():
    print(
        "=== GATE 28D.1A - FINMIND LIVE REQUEST "
        "PARAMETERS CONTRACT V1 ==="
    )

    module_name = "v14.finmind_live_request_parameters"

    try:
        module = importlib.import_module(module_name)
    except ModuleNotFoundError:
        print(
            "[EXPECTED RED] FinMind live request "
            "parameters module not found"
        )
        raise SystemExit(1)

    validate = getattr(
        module,
        "validate_finmind_live_params",
        None,
    )
    assert callable(validate), (
        "validate_finmind_live_params missing"
    )

    assert getattr(
        module,
        "ALLOWED_DATASET",
        None,
    ) == "TaiwanStockPrice"

    assert getattr(
        module,
        "ALLOW_TOKEN_IN_PARAMS",
        None,
    ) is False

    assert getattr(
        module,
        "ALLOW_UNKNOWN_PARAMS",
        None,
    ) is False

    valid = {
        "dataset": "TaiwanStockPrice",
        "data_id": "2330",
        "start_date": "2026-09-23",
        "end_date": "2026-09-23",
    }

    result = validate(valid)

    assert result.get("allowed") is True
    assert result.get("params") == valid

    print("[PASS] valid single-day request accepted")

    invalid_cases = [
        (
            {
                "dataset": "OtherDataset",
                "data_id": "2330",
                "start_date": "2026-09-23",
                "end_date": "2026-09-23",
            },
            "DATASET_NOT_ALLOWED",
        ),
        (
            {
                "dataset": "TaiwanStockPrice",
                "start_date": "2026-09-23",
                "end_date": "2026-09-23",
            },
            "DATA_ID_REQUIRED",
        ),
        (
            {
                "dataset": "TaiwanStockPrice",
                "data_id": "2330,2317",
                "start_date": "2026-09-23",
                "end_date": "2026-09-23",
            },
            "DATA_ID_INVALID",
        ),
        (
            {
                "dataset": "TaiwanStockPrice",
                "data_id": "2330",
                "start_date": "2026/09/23",
                "end_date": "2026/09/23",
            },
            "DATE_INVALID",
        ),
        (
            {
                "dataset": "TaiwanStockPrice",
                "data_id": "2330",
                "start_date": "2026-09-22",
                "end_date": "2026-09-23",
            },
            "SINGLE_DAY_REQUIRED",
        ),
        (
            {
                "dataset": "TaiwanStockPrice",
                "data_id": "2330",
                "start_date": "2026-09-23",
                "end_date": "2026-09-23",
                "token": "TEST_SECRET_ONLY",
            },
            "UNKNOWN_PARAM",
        ),
        (
            {
                "dataset": "TaiwanStockPrice",
                "data_id": "2330",
                "start_date": "2026-09-23",
                "end_date": "2026-09-23",
                "extra": "unexpected",
            },
            "UNKNOWN_PARAM",
        ),
    ]

    for params, reason in invalid_cases:
        rejected = validate(params)

        assert rejected.get("allowed") is False
        assert rejected.get("reason") == reason
        assert "params" not in rejected

    print("[PASS] unsafe request parameters fail closed")
    print("[PASS] multi-symbol request rejected")
    print("[PASS] single trading-day scope enforced")
    print("[PASS] token/unknown parameters rejected")

    print(
        "=== GATE 28D.1A FINMIND LIVE REQUEST "
        "PARAMETERS RESULT: PASS ==="
    )


if __name__ == "__main__":
    main()
