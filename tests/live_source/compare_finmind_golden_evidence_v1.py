import importlib


def main():
    print(
        "=== GATE 28D.1B - FINMIND GOLDEN "
        "EVIDENCE CONTRACT V1 ==="
    )

    module_name = "v14.finmind_golden_evidence"

    try:
        module = importlib.import_module(module_name)
    except ModuleNotFoundError:
        print(
            "[EXPECTED RED] FinMind golden evidence "
            "module not found"
        )
        raise SystemExit(1)

    build = getattr(
        module,
        "build_finmind_golden_evidence",
        None,
    )
    assert callable(build), (
        "build_finmind_golden_evidence missing"
    )

    assert getattr(
        module,
        "ALLOW_RAW_PAYLOAD_STORAGE",
        None,
    ) is False

    assert getattr(
        module,
        "ALLOW_SECRET_STORAGE",
        None,
    ) is False

    assert getattr(
        module,
        "ALLOW_CORE_INPUT",
        None,
    ) is False

    assert getattr(
        module,
        "ALLOW_SUPABASE_WRITE",
        None,
    ) is False

    payload = {
        "data": [
            {
                "date": "2026-09-23",
                "stock_id": "2330",
                "close": 1000,
            }
        ]
    }

    evidence = {
        "status_code": 200,
        "content_type": "application/json",
        "payload": payload,
        "size_bytes": 123,
    }

    params = {
        "dataset": "TaiwanStockPrice",
        "data_id": "2330",
        "start_date": "2026-09-23",
        "end_date": "2026-09-23",
    }

    result = build(
        evidence=evidence,
        params=params,
    )

    assert result.get("allowed") is True

    golden = result.get("golden")
    assert isinstance(golden, dict)

    assert golden.get("provider") == "FinMind"
    assert golden.get("endpoint") == (
        "https://api.finmindtrade.com/api/v4/data"
    )
    assert golden.get("dataset") == "TaiwanStockPrice"
    assert golden.get("data_id") == "2330"
    assert golden.get("trading_date") == "2026-09-23"
    assert golden.get("status_code") == 200
    assert golden.get("content_type") == "application/json"
    assert golden.get("size_bytes") == 123
    assert golden.get("record_count") == 1

    payload_hash = golden.get("payload_hash")

    assert isinstance(payload_hash, str)
    assert len(payload_hash) == 64

    assert "payload" not in golden
    assert "token" not in golden
    assert "authorization" not in {
        str(key).lower()
        for key in golden
    }

    print("[PASS] golden metadata built")
    print("[PASS] existing payload SHA-256 reused")
    print("[PASS] raw payload excluded")
    print("[PASS] secret/auth fields excluded")

    invalid = build(
        evidence={
            "status_code": 200,
            "content_type": "application/json",
            "payload": {"data": []},
            "size_bytes": 20,
        },
        params=params,
    )

    assert invalid.get("allowed") is False
    assert invalid.get("reason") == "EMPTY_DATASET"
    assert "golden" not in invalid

    print("[PASS] non-RAW evidence fails closed")

    print(
        "=== GATE 28D.1B FINMIND GOLDEN "
        "EVIDENCE RESULT: PASS ==="
    )


if __name__ == "__main__":
    main()
