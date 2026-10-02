from importlib import import_module


MODULE_NAME = (
    "v14.protected_one_shot_golden_evidence_composition"
)


class FakeGuard:
    def __init__(self):
        self.calls = 0

    def authorize(self):
        self.calls += 1

        if self.calls == 1:
            return {
                "allowed": True,
            }

        return {
            "allowed": False,
            "reason": "REAL_GET_LIMIT_REACHED",
        }


class FakeEvidenceExecutor:
    def __init__(self):
        self.calls = 0

    def __call__(self):
        self.calls += 1

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


def main():
    print(
        "=== GATE 28D.2K-3E - PROTECTED ONE-SHOT "
        "GOLDEN EVIDENCE COMPOSITION CONTRACT V1 ==="
    )

    try:
        m = import_module(MODULE_NAME)
    except ModuleNotFoundError:
        print(
            "[EXPECTED RED] protected one-shot golden "
            "evidence composition module not found"
        )
        raise SystemExit(1)

    assert m.READ_ONLY is True
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

    execute = getattr(
        m,
        "execute_protected_one_shot_golden_evidence",
        None,
    )
    assert callable(execute)

    params = {
        "dataset": "TaiwanStockPrice",
        "data_id": "2330",
        "start_date": "2026-09-30",
        "end_date": "2026-09-30",
    }

    guard = FakeGuard()
    executor = FakeEvidenceExecutor()

    first = execute(
        guard=guard,
        executor=executor,
        params=params,
    )

    assert isinstance(first, dict)
    assert first.get("allowed") is True

    golden = first.get("golden")
    assert isinstance(golden, dict)

    assert golden.get("provider") == "FinMind"
    assert golden.get("dataset") == "TaiwanStockPrice"
    assert golden.get("data_id") == "2330"
    assert golden.get("trading_date") == "2026-09-30"
    assert golden.get("status_code") == 200
    assert golden.get("record_count") == 1

    payload_hash = golden.get("payload_hash")
    assert isinstance(payload_hash, str)
    assert len(payload_hash) == 64

    assert guard.calls == 1
    assert executor.calls == 1

    assert "payload" not in first
    assert "evidence" not in first
    assert "token" not in first

    print("[PASS] first authorization accepted")
    print("[PASS] injected evidence executor called once")
    print("[PASS] sanitized golden evidence returned")
    print("[PASS] raw evidence excluded from public result")
    print("[PASS] secret/token excluded from public result")

    second = execute(
        guard=guard,
        executor=executor,
        params=params,
    )

    assert isinstance(second, dict)
    assert second.get("allowed") is False
    assert second.get("reason") == "REAL_GET_LIMIT_REACHED"

    assert guard.calls == 2
    assert executor.calls == 1

    print("[PASS] second authorization denied")
    print("[PASS] executor not called a second time")
    print("[PASS] one-shot boundary preserved")
    print("[PASS] network/session/write remain disabled")

    print(
        "=== GATE 28D.2K-3E PROTECTED ONE-SHOT "
        "GOLDEN EVIDENCE COMPOSITION "
        "CONTRACT RESULT: PASS ==="
    )


if __name__ == "__main__":
    main()