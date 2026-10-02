from importlib import import_module


MODULE_NAME = (
    "v14.protected_runtime_golden_evidence_entry_composition"
)


VALID_PARAMS = {
    "dataset": "TaiwanStockPrice",
    "data_id": "2330",
    "start_date": "2026-09-30",
    "end_date": "2026-09-30",
}


def assert_private_failure(result, reason):
    assert isinstance(result, dict)
    assert result.get("allowed") is False
    assert result.get("reason") == reason

    assert "golden" not in result
    assert "payload" not in result
    assert "evidence" not in result
    assert "token" not in result

    public_text = repr(result).lower()

    assert "authorization" not in public_text
    assert "bearer" not in public_text


def main():
    print(
        "=== GATE 28D.2K-3H - PROTECTED RUNTIME "
        "GOLDEN EVIDENCE FAIL-CLOSED CONTRACT V1 ==="
    )

    m = import_module(MODULE_NAME)

    execute = getattr(
        m,
        "execute_runtime_entry_golden_evidence",
        None,
    )

    assert callable(execute)

    assert m.READ_ONLY is True
    assert m.COMPOSITION_ONLY is True
    assert m.ONE_SHOT_ONLY is True
    assert m.MAX_REAL_GETS == 1

    assert m.ALLOW_NETWORK_EXECUTION is False
    assert m.ALLOW_SESSION_CREATION is False
    assert m.ALLOW_RAW_PAYLOAD_STORAGE is False
    assert m.ALLOW_SECRET_STORAGE is False
    assert m.ALLOW_CORE_INPUT is False
    assert m.ALLOW_SCORE is False
    assert m.ALLOW_DECISION is False
    assert m.ALLOW_SUPABASE_WRITE is False
    assert m.ALLOW_PRODUCTION_WRITE is False

    # 1. Runtime executor must be callable.
    result = execute(
        runtime_executor=None,
        params=VALID_PARAMS,
    )

    assert_private_failure(
        result,
        "RUNTIME_EXECUTOR_REQUIRED",
    )

    print("[PASS] non-callable runtime executor fails closed")

    # 2. Runtime execution result must be a dict.
    def invalid_result_executor():
        return "INVALID_RESULT"

    result = execute(
        runtime_executor=invalid_result_executor,
        params=VALID_PARAMS,
    )

    assert_private_failure(
        result,
        "RUNTIME_EXECUTION_INVALID",
    )

    print("[PASS] invalid runtime result fails closed")

    # 3. Existing runtime denial reason must be preserved.
    def denied_executor():
        return {
            "allowed": False,
            "reason": "REAL_GET_LIMIT_REACHED",
        }

    result = execute(
        runtime_executor=denied_executor,
        params=VALID_PARAMS,
    )

    assert_private_failure(
        result,
        "REAL_GET_LIMIT_REACHED",
    )

    print("[PASS] runtime denial reason preserved")

    # 4. Allowed execution must contain evidence.
    def missing_evidence_executor():
        return {
            "allowed": True,
        }

    result = execute(
        runtime_executor=missing_evidence_executor,
        params=VALID_PARAMS,
    )

    assert_private_failure(
        result,
        "EVIDENCE_REQUIRED",
    )

    print("[PASS] missing evidence fails closed")

    # 5. Empty dataset must fail closed through the
    # existing Golden Evidence classification path.
    def empty_dataset_executor():
        return {
            "allowed": True,
            "evidence": {
                "status_code": 200,
                "content_type": "application/json",
                "payload": {
                    "data": [],
                },
                "size_bytes": 20,
            },
        }

    result = execute(
        runtime_executor=empty_dataset_executor,
        params=VALID_PARAMS,
    )

    assert_private_failure(
        result,
        "EMPTY_DATASET",
    )

    print("[PASS] empty dataset fails closed")

    # 6. Params must be a dict.
    def valid_evidence_executor():
        return {
            "allowed": True,
            "evidence": {
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
            },
        }

    result = execute(
        runtime_executor=valid_evidence_executor,
        params=None,
    )

    assert_private_failure(
        result,
        "PARAMS_REQUIRED",
    )

    print("[PASS] missing params fail closed")

    # 7. Required params fields must be valid.
    invalid_params = {
        "dataset": "TaiwanStockPrice",
        "data_id": "",
        "start_date": "2026-09-30",
        "end_date": "2026-09-30",
    }

    result = execute(
        runtime_executor=valid_evidence_executor,
        params=invalid_params,
    )

    assert_private_failure(
        result,
        "PARAMS_INVALID",
    )

    print("[PASS] invalid params fail closed")

    # 8. Golden Evidence remains single-day only.
    multi_day_params = {
        "dataset": "TaiwanStockPrice",
        "data_id": "2330",
        "start_date": "2026-09-30",
        "end_date": "2026-10-01",
    }

    result = execute(
        runtime_executor=valid_evidence_executor,
        params=multi_day_params,
    )

    assert_private_failure(
        result,
        "SINGLE_DAY_REQUIRED",
    )

    print("[PASS] multi-day params fail closed")

    print("[PASS] no failure result exposes raw evidence")
    print("[PASS] no failure result exposes secret/auth data")
    print("[PASS] network/session/write remain disabled")

    print(
        "=== GATE 28D.2K-3H PROTECTED RUNTIME "
        "GOLDEN EVIDENCE FAIL-CLOSED "
        "CONTRACT RESULT: PASS ==="
    )


if __name__ == "__main__":
    main()
