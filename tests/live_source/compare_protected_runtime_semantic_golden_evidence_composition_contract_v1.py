from importlib import import_module


MODULE_NAME = (
    "v14.protected_runtime_semantic_golden_evidence_composition"
)


class FakeRuntimeExecutor:
    def __init__(self, evidence):
        self.evidence = evidence
        self.calls = 0

    def __call__(self):
        self.calls += 1
        return {
            "allowed": True,
            "evidence": self.evidence,
        }


def main():
    print(
        "=== GATE 28D.2K-3L - PROTECTED RUNTIME "
        "SEMANTIC GOLDEN EVIDENCE COMPOSITION "
        "CONTRACT V1 ==="
    )

    try:
        m = import_module(MODULE_NAME)
    except ModuleNotFoundError:
        print(
            "[EXPECTED RED] protected runtime semantic "
            "golden evidence composition module not found"
        )
        raise SystemExit(1)

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

    execute = getattr(
        m,
        "execute_protected_runtime_semantic_golden_evidence",
        None,
    )

    assert callable(execute)

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

    # Runtime denial must stop before semantic composition.
    class DeniedRuntimeExecutor:
        def __init__(self):
            self.calls = 0

        def __call__(self):
            self.calls += 1
            return {
                "allowed": False,
                "reason": "RUNTIME_EXECUTION_REJECTED",
            }

    semantic_calls = {"count": 0}

    original_semantic_builder = (
        m.build_semantically_observed_golden_evidence
    )

    def counting_semantic_builder(evidence, params):
        semantic_calls["count"] += 1
        return original_semantic_builder(
            evidence=evidence,
            params=params,
        )

    m.build_semantically_observed_golden_evidence = (
        counting_semantic_builder
    )

    denied_runtime = DeniedRuntimeExecutor()

    denied = execute(
        runtime_executor=denied_runtime,
        params=params,
    )

    assert denied.get("allowed") is False
    assert denied.get("reason") == "RUNTIME_EXECUTION_REJECTED"
    assert denied_runtime.calls == 1
    assert semantic_calls["count"] == 0

    print("[PASS] runtime denial stops before semantic composition")

    m.build_semantically_observed_golden_evidence = (
        original_semantic_builder
    )
    runtime_executor = FakeRuntimeExecutor(evidence)

    result = execute(
        runtime_executor=runtime_executor,
        params=params,
    )

    assert isinstance(result, dict)
    assert result.get("allowed") is True
    assert runtime_executor.calls == 1

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

    print("[PASS] protected runtime executor reused")
    print("[PASS] existing semantic composition reused")
    print("[PASS] sanitized golden evidence returned")
    print("[PASS] raw/secret evidence excluded")
    print("[PASS] network/session/real GET remain disabled")
    print("[PASS] core/score/decision/write remain disabled")

    print(
        "=== GATE 28D.2K-3L PROTECTED RUNTIME "
        "SEMANTIC GOLDEN EVIDENCE COMPOSITION "
        "CONTRACT RESULT: PASS ==="
    )


if __name__ == "__main__":
    main()
