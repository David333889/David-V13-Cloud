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


def main():
    print(
        "=== GATE 28D.2K-3I - PROTECTED RUNTIME "
        "GOLDEN EVIDENCE EXCEPTION BOUNDARY "
        "CONTRACT V1 ==="
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

    def failing_runtime_executor():
        raise RuntimeError(
            "token=TEST_TOKEN_ONLY runtime failure"
        )

    try:
        result = execute(
            runtime_executor=failing_runtime_executor,
            params=VALID_PARAMS,
        )
    except RuntimeError:
        print(
            "[EXPECTED RED] runtime executor exception "
            "escaped composition boundary"
        )
        raise SystemExit(1)

    assert isinstance(result, dict)
    assert result.get("allowed") is False
    assert result.get("reason") == (
        "RUNTIME_EXECUTION_FAILURE"
    )

    assert "golden" not in result
    assert "payload" not in result
    assert "evidence" not in result
    assert "token" not in result
    assert "exception" not in result
    assert "error" not in result

    public_text = repr(result)

    assert "TEST_TOKEN_ONLY" not in public_text
    assert "runtime failure" not in public_text
    assert "RuntimeError" not in public_text
    assert "Authorization" not in public_text
    assert "Bearer" not in public_text

    print("[PASS] runtime exception fails closed")
    print("[PASS] stable public failure reason returned")
    print("[PASS] raw exception text excluded")
    print("[PASS] secret/token excluded")
    print("[PASS] raw evidence/golden output excluded")
    print("[PASS] network/session/write remain disabled")

    print(
        "=== GATE 28D.2K-3I PROTECTED RUNTIME "
        "GOLDEN EVIDENCE EXCEPTION BOUNDARY "
        "CONTRACT RESULT: PASS ==="
    )


if __name__ == "__main__":
    main()
