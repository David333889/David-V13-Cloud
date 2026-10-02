from importlib import import_module


MODULE_NAME = (
    "v14.real_get_golden_evidence_integration"
)


def main():
    print(
        "=== GATE 28D.2K-3J - GOLDEN EVIDENCE "
        "INTEGRATION EXCEPTION BOUNDARY "
        "CONTRACT V1 ==="
    )

    m = import_module(MODULE_NAME)

    build = getattr(
        m,
        "build_real_get_golden_evidence",
        None,
    )

    assert callable(build)

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

    evidence = {
        "status_code": 200,
        "content_type": "application/json",
        "payload": {
            "data": [
                {
                    "date": "2026-09-30",
                    "stock_id": "2330",
                    "close": 1005,
                }
            ]
        },
        "size_bytes": 321,
    }

    params = {
        "dataset": "TaiwanStockPrice",
        "data_id": "2330",
        "start_date": "2026-09-30",
        "end_date": "2026-09-30",
    }

    original_builder = m.build_finmind_golden_evidence

    def failing_builder(
        evidence,
        params,
    ):
        raise RuntimeError(
            "token=TEST_TOKEN_ONLY golden builder failure"
        )

    m.build_finmind_golden_evidence = failing_builder

    try:
        try:
            result = build(
                evidence=evidence,
                params=params,
            )
        except RuntimeError:
            print(
                "[EXPECTED RED] golden builder exception "
                "escaped integration boundary"
            )
            raise SystemExit(1)
    finally:
        m.build_finmind_golden_evidence = original_builder

    assert isinstance(result, dict)
    assert result.get("allowed") is False
    assert result.get("reason") == (
        "GOLDEN_EVIDENCE_FAILURE"
    )

    assert "golden" not in result
    assert "payload" not in result
    assert "evidence" not in result
    assert "token" not in result
    assert "exception" not in result
    assert "error" not in result

    public_text = repr(result)

    assert "TEST_TOKEN_ONLY" not in public_text
    assert "golden builder failure" not in public_text
    assert "RuntimeError" not in public_text
    assert "Authorization" not in public_text
    assert "Bearer" not in public_text

    print("[PASS] golden builder exception fails closed")
    print("[PASS] stable public failure reason returned")
    print("[PASS] raw exception text excluded")
    print("[PASS] secret/token excluded")
    print("[PASS] raw evidence/golden output excluded")
    print("[PASS] network/session/real GET remain disabled")
    print("[PASS] core/score/decision/write remain disabled")

    print(
        "=== GATE 28D.2K-3J GOLDEN EVIDENCE "
        "INTEGRATION EXCEPTION BOUNDARY "
        "CONTRACT RESULT: PASS ==="
    )


if __name__ == "__main__":
    main()