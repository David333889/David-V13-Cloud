from importlib import import_module


MODULE_NAME = (
    "v14.real_get_golden_evidence_integration"
)


def main():
    print(
        "=== GATE 28D.2K-3D - REAL GET -> "
        "GOLDEN EVIDENCE INTEGRATION CONTRACT V1 ==="
    )

    try:
        m = import_module(MODULE_NAME)
    except ModuleNotFoundError:
        print(
            "[EXPECTED RED] real GET -> golden evidence "
            "integration module not found"
        )
        raise SystemExit(1)

    # Integration boundary must remain offline during
    # contract/build verification.
    assert m.READ_ONLY is True
    assert m.CONTRACT_ONLY is True

    assert m.ALLOW_NETWORK_EXECUTION is False
    assert m.ALLOW_REAL_GET_EXECUTION is False
    assert m.ALLOW_SESSION_CREATION is False

    assert m.ALLOW_RAW_PAYLOAD_STORAGE is False
    assert m.ALLOW_SECRET_STORAGE is False

    assert m.ALLOW_CORE_INPUT is False
    assert m.ALLOW_SCORE is False
    assert m.ALLOW_DECISION is False
    assert m.ALLOW_SUPABASE_WRITE is False
    assert m.ALLOW_PRODUCTION_WRITE is False

    build = getattr(
        m,
        "build_real_get_golden_evidence",
        None,
    )
    assert callable(build)

    # Fake RAW_EVIDENCE only.
    # No Session, HTTP request, token, or network crossing.
    payload = {
        "data": [
            {
                "date": "2026-09-30",
                "stock_id": "2330",
                "open": 1000,
                "max": 1010,
                "min": 995,
                "close": 1005,
                "Trading_Volume": 123456,
            }
        ]
    }

    evidence = {
        "status_code": 200,
        "content_type": "application/json",
        "payload": payload,
        "size_bytes": 321,
    }

    params = {
        "dataset": "TaiwanStockPrice",
        "data_id": "2330",
        "start_date": "2026-09-30",
        "end_date": "2026-09-30",
    }

    result = build(
        evidence=evidence,
        params=params,
    )

    assert isinstance(result, dict)
    assert result.get("allowed") is True

    golden = result.get("golden")
    assert isinstance(golden, dict)

    assert golden.get("provider") == "FinMind"
    assert golden.get("dataset") == "TaiwanStockPrice"
    assert golden.get("data_id") == "2330"
    assert golden.get("trading_date") == "2026-09-30"

    assert golden.get("status_code") == 200
    assert golden.get("content_type") == "application/json"
    assert golden.get("size_bytes") == 321
    assert golden.get("record_count") == 1

    payload_hash = golden.get("payload_hash")
    assert isinstance(payload_hash, str)
    assert len(payload_hash) == 64

    # Sanitized Golden Evidence only.
    assert "payload" not in golden
    assert "token" not in golden

    golden_keys = {
        str(key).lower()
        for key in golden
    }

    assert "authorization" not in golden_keys
    assert "finmind_api_token" not in golden_keys

    print("[PASS] fake RAW_EVIDENCE accepted")
    print("[PASS] existing FinMind golden builder reused")
    print("[PASS] record count preserved as metadata")
    print("[PASS] payload SHA-256 preserved as metadata")
    print("[PASS] raw payload excluded from golden output")
    print("[PASS] secret/auth fields excluded")
    print("[PASS] network/session/real GET remain disabled")
    print("[PASS] core/score/decision/write remain disabled")

    # Empty dataset must continue to fail closed.
    invalid = build(
        evidence={
            "status_code": 200,
            "content_type": "application/json",
            "payload": {
                "data": [],
            },
            "size_bytes": 20,
        },
        params=params,
    )

    assert isinstance(invalid, dict)
    assert invalid.get("allowed") is False
    assert invalid.get("reason") == "EMPTY_DATASET"
    assert "golden" not in invalid

    print("[PASS] invalid evidence fails closed")

    print(
        "=== GATE 28D.2K-3D REAL GET -> "
        "GOLDEN EVIDENCE INTEGRATION "
        "CONTRACT RESULT: PASS ==="
    )


if __name__ == "__main__":
    main()