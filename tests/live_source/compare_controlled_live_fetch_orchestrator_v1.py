import importlib


class FakeResponse:
    def __init__(
        self,
        status_code=200,
        content_type="application/json",
        payload=None,
        content=b"{}",
    ):
        self.status_code = status_code
        self.headers = {
            "Content-Type": content_type,
            "Content-Length": str(len(content)),
        }
        self._payload = payload
        self.content = content

    def json(self):
        return self._payload


class FakeSession:
    def __init__(self, response):
        self.response = response
        self.calls = []

    def get(
        self,
        url,
        headers=None,
        timeout=None,
        params=None,
        allow_redirects=None,
    ):
        self.calls.append({
            "url": url,
            "headers": headers,
            "timeout": timeout,
            "params": params,
            "allow_redirects": allow_redirects,
        })

        return self.response


class FakeSessionFactory:
    def __init__(self, response):
        self.response = response
        self.calls = 0
        self.sessions = []

    def __call__(self):
        self.calls += 1

        session = FakeSession(
            response=self.response,
        )

        self.sessions.append(session)

        return session


def total_get_calls(factory):
    return sum(
        len(session.calls)
        for session in factory.sessions
    )


def main():
    print(
        "=== GATE 28C.3 - CONTROLLED LIVE FETCH "
        "ORCHESTRATOR V1 ==="
    )

    try:
        orchestrator = importlib.import_module(
            "v14.controlled_live_fetch"
        )
    except ModuleNotFoundError:
        print(
            "[FAIL] controlled live fetch module not found"
        )
        raise SystemExit(1)

    assert getattr(
        orchestrator,
        "ALLOW_CORE_INPUT",
        None,
    ) is False

    assert getattr(
        orchestrator,
        "ALLOW_SCORE",
        None,
    ) is False

    assert getattr(
        orchestrator,
        "ALLOW_DECISION",
        None,
    ) is False

    assert getattr(
        orchestrator,
        "ALLOW_SUPABASE_WRITE",
        None,
    ) is False

    assert getattr(
        orchestrator,
        "ALLOW_PRODUCTION_WRITE",
        None,
    ) is False

    print("[PASS] orchestrator flags fail closed")

    execute = getattr(
        orchestrator,
        "execute_controlled_fetch",
        None,
    )

    assert callable(execute), (
        "execute_controlled_fetch missing"
    )

    payload = {
        "msg": "success",
        "status": 200,
        "data": [
            {
                "date": "2026-09-23",
                "stock_id": "2330",
                "open": 0,
                "max": 1,
                "min": 0,
                "close": 1,
                "Trading_Volume": 0,
            }
        ],
    }

    response = FakeResponse(
        status_code=200,
        content_type="application/json",
        payload=payload,
        content=b'{"offline":true}',
    )

    # Missing secret:
    # no session and no GET may occur.
    missing_factory = FakeSessionFactory(response)

    missing = execute(
        env={},
        session_factory=missing_factory,
        url="https://api.finmindtrade.com/api/v4/data",
        timeout=5,
        params={
            "dataset": "TaiwanStockPrice",
            "data_id": "2330",
            "start_date": "2026-09-23",
            "end_date": "2026-09-23",
        },
        max_bytes=5_000_000,
    )

    assert missing.get("allowed") is False
    assert missing.get("reason") == "SECRET_MISSING"
    assert missing_factory.calls == 0
    assert total_get_calls(missing_factory) == 0

    print("[PASS] missing secret blocks before session")

    # Invalid target:
    # secret exists, but session still must not be created.
    target_factory = FakeSessionFactory(response)

    invalid_target = execute(
        env={
            "FINMIND_API_TOKEN": "TEST_RUNTIME_SECRET_ONLY",
        },
        session_factory=target_factory,
        url="https://example.com/api/v4/data",
        timeout=5,
        params={
            "dataset": "TaiwanStockPrice",
        },
        max_bytes=5_000_000,
    )

    assert invalid_target.get("allowed") is False
    assert invalid_target.get("reason") == "HOST_NOT_ALLOWED"
    assert target_factory.calls == 0
    assert total_get_calls(target_factory) == 0

    print("[PASS] invalid target blocks before session")

    # Missing session factory:
    # must fail before any GET.
    no_factory = execute(
        env={
            "FINMIND_API_TOKEN": "TEST_RUNTIME_SECRET_ONLY",
        },
        session_factory=None,
        url="https://api.finmindtrade.com/api/v4/data",
        timeout=5,
        params={
            "dataset": "TaiwanStockPrice",
        },
        max_bytes=5_000_000,
    )

    assert no_factory.get("allowed") is False
    assert no_factory.get("reason") == (
        "SESSION_FACTORY_REQUIRED"
    )

    print("[PASS] missing session factory fails closed")

    # All gates pass:
    # exactly one fake GET is permitted.
    success_factory = FakeSessionFactory(response)

    success = execute(
        env={
            "FINMIND_API_TOKEN": "TEST_RUNTIME_SECRET_ONLY",
        },
        session_factory=success_factory,
        url="https://api.finmindtrade.com/api/v4/data",
        timeout=5,
        params={
            "dataset": "TaiwanStockPrice",
            "data_id": "2330",
            "start_date": "2026-09-23",
            "end_date": "2026-09-23",
        },
        max_bytes=5_000_000,
    )

    assert success.get("allowed") is True
    assert success_factory.calls == 1
    assert total_get_calls(success_factory) == 1

    evidence = success.get("evidence")

    assert isinstance(evidence, dict)
    assert evidence.get("status_code") == 200
    assert evidence.get("payload") == payload

    assert "TEST_RUNTIME_SECRET_ONLY" not in repr(success)

    print("[PASS] safe path permits exactly one fake GET")
    print("[PASS] secret excluded from public result")

    module_text = open(
        orchestrator.__file__,
        "r",
        encoding="utf-8",
    ).read().lower()

    forbidden = (
        "import requests",
        "from requests",
        "requests.session(",
        "import httpx",
        "from httpx",
        "httpx.client(",
        "urlopen(",
        "core_engine",
        "runtime_writer",
        "supabase_writer",
        "supabase_persistence",
        "post(",
        "put(",
        "patch(",
        "delete(",
    )

    for item in forbidden:
        assert item not in module_text, (
            f"forbidden dependency/wiring detected: {item}"
        )

    print("[PASS] no direct network/core/write wiring")

    print(
        "=== GATE 28C.3 CONTROLLED LIVE FETCH "
        "ORCHESTRATOR RESULT: PASS ==="
    )


if __name__ == "__main__":
    main()
