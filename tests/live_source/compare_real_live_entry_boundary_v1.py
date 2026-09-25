import importlib


class FakeResponse:
    status_code = 200
    headers = {
        "Content-Type": "application/json",
    }
    content = b'{"data":[{"stock_id":"2330"}]}'

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
        self.calls = 0

    def get(self, *args, **kwargs):
        self.calls += 1
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
        session.calls
        for session in factory.sessions
    )


def main():
    print(
        "=== GATE 28D.2A - REAL LIVE ENTRY "
        "BOUNDARY CONTRACT V1 ==="
    )

    try:
        module = importlib.import_module(
            "v14.real_live_entry"
        )
    except ModuleNotFoundError:
        print(
            "[EXPECTED RED] real live entry "
            "module not found"
        )
        raise SystemExit(1)

    execute = getattr(
        module,
        "execute_real_live_entry",
        None,
    )

    assert callable(execute), (
        "execute_real_live_entry missing"
    )

    for flag in (
        "ALLOW_CORE_INPUT",
        "ALLOW_SCORE",
        "ALLOW_DECISION",
        "ALLOW_SUPABASE_WRITE",
        "ALLOW_PRODUCTION_WRITE",
    ):
        assert getattr(module, flag, None) is False

    factory = FakeSessionFactory()

    result = execute(
        env={
            "FINMIND_API_TOKEN":
                "TEST_RUNTIME_SECRET_ONLY",
        },
        session_factory=factory,
        data_id="2330",
        trading_date="2026-09-23",
    )

    assert result.get("allowed") is True

    assert factory.calls == 1
    assert total_get_calls(factory) == 1

    golden = result.get("golden")

    assert isinstance(golden, dict)
    assert golden.get("provider") == "FinMind"
    assert golden.get("dataset") == "TaiwanStockPrice"
    assert golden.get("data_id") == "2330"
    assert golden.get("trading_date") == "2026-09-23"

    assert "payload" not in result
    assert "evidence" not in result
    assert "token" not in result

    public_text = repr(result)

    assert "TEST_RUNTIME_SECRET_ONLY" not in public_text
    assert "Authorization" not in public_text
    assert "Bearer" not in public_text

    print("[PASS] injected runtime entry accepted")
    print("[PASS] exactly one fake GET")
    print("[PASS] golden metadata only")
    print("[PASS] secret/auth excluded")

    print(
        "=== GATE 28D.2A REAL LIVE ENTRY "
        "BOUNDARY RESULT: PASS ==="
    )


if __name__ == "__main__":
    main()
