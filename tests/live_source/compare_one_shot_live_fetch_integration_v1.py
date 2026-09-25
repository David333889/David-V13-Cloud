import importlib


class FakeResponse:
    def __init__(self):
        self.status_code = 200
        self.headers = {
            "Content-Type": "application/json",
        }
        self.content = b'{"data":[{"stock_id":"2330"}]}'

    def json(self):
        return {
            "data": [
                {
                    "date": "2026-09-23",
                    "stock_id": "2330",
                    "close": 1000,
                }
            ]
        }


class FakeSession:
    def __init__(self):
        self.calls = []

    def get(
        self,
        url,
        headers=None,
        timeout=None,
        params=None,
        allow_redirects=False,
    ):
        self.calls.append(
            {
                "url": url,
                "headers": headers,
                "timeout": timeout,
                "params": params,
                "allow_redirects": allow_redirects,
            }
        )
        return FakeResponse()


class FakeSessionFactory:
    def __init__(self):
        self.calls = 0
        self.sessions = []

    def __call__(self):
        self.calls += 1
        session = FakeSession()
        self.sessions.append(session)
        return session


def total_get_calls(factory):
    return sum(
        len(session.calls)
        for session in factory.sessions
    )


def main():
    print(
        "=== GATE 28D.1C - ONE-SHOT LIVE FETCH "
        "INTEGRATION CONTRACT V1 ==="
    )

    try:
        module = importlib.import_module(
            "v14.one_shot_live_fetch"
        )
    except ModuleNotFoundError:
        print(
            "[EXPECTED RED] one-shot live fetch "
            "integration module not found"
        )
        raise SystemExit(1)

    execute = getattr(
        module,
        "execute_one_shot_live_fetch",
        None,
    )
    assert callable(execute), (
        "execute_one_shot_live_fetch missing"
    )

    for flag in (
        "ALLOW_CORE_INPUT",
        "ALLOW_SCORE",
        "ALLOW_DECISION",
        "ALLOW_SUPABASE_WRITE",
        "ALLOW_PRODUCTION_WRITE",
    ):
        assert getattr(module, flag, None) is False

    valid_params = {
        "dataset": "TaiwanStockPrice",
        "data_id": "2330",
        "start_date": "2026-09-23",
        "end_date": "2026-09-23",
    }

    # Invalid params must stop before Session / GET.
    invalid_factory = FakeSessionFactory()

    invalid = execute(
        env={
            "FINMIND_API_TOKEN": "TEST_RUNTIME_SECRET_ONLY",
        },
        session_factory=invalid_factory,
        url="https://api.finmindtrade.com/api/v4/data",
        timeout=10,
        params={
            **valid_params,
            "extra": "not-allowed",
        },
    )

    assert invalid.get("allowed") is False
    assert invalid_factory.calls == 0
    assert total_get_calls(invalid_factory) == 0

    print("[PASS] invalid params stop before session")

    # Missing secret must also stop before Session / GET.
    missing_factory = FakeSessionFactory()

    missing = execute(
        env={},
        session_factory=missing_factory,
        url="https://api.finmindtrade.com/api/v4/data",
        timeout=10,
        params=valid_params,
    )

    assert missing.get("allowed") is False
    assert missing_factory.calls == 0
    assert total_get_calls(missing_factory) == 0

    print("[PASS] missing secret stops before session")

    # Valid path: exactly one Session and one Fake GET.
    success_factory = FakeSessionFactory()

    success = execute(
        env={
            "FINMIND_API_TOKEN": "TEST_RUNTIME_SECRET_ONLY",
        },
        session_factory=success_factory,
        url="https://api.finmindtrade.com/api/v4/data",
        timeout=10,
        params=valid_params,
    )

    assert success.get("allowed") is True
    assert success_factory.calls == 1
    assert total_get_calls(success_factory) == 1

    golden = success.get("golden")

    assert isinstance(golden, dict)
    assert golden.get("provider") == "FinMind"
    assert golden.get("dataset") == "TaiwanStockPrice"
    assert golden.get("data_id") == "2330"
    assert golden.get("trading_date") == "2026-09-23"
    assert golden.get("record_count") == 1

    assert "payload" not in success
    assert "evidence" not in success
    assert "token" not in success

    public_text = repr(success)

    assert "TEST_RUNTIME_SECRET_ONLY" not in public_text
    assert "Authorization" not in public_text
    assert "Bearer" not in public_text

    print("[PASS] exactly one fake GET")
    print("[PASS] golden evidence returned")
    print("[PASS] raw evidence excluded from public result")
    print("[PASS] secret/auth excluded from public result")

    print(
        "=== GATE 28D.1C ONE-SHOT LIVE FETCH "
        "INTEGRATION RESULT: PASS ==="
    )


if __name__ == "__main__":
    main()
