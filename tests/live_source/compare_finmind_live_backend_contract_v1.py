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
    def __init__(self, response=None, error=None):
        self.response = response
        self.error = error
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

        if self.error is not None:
            raise self.error

        return self.response


def main():
    print("=== GATE 28C.1 - FINMIND LIVE BACKEND CONTRACT V1 ===")

    try:
        backend_module = importlib.import_module(
            "v14.finmind_live_backend"
        )
    except ModuleNotFoundError:
        print("[FAIL] FinMind live backend module not found")
        raise SystemExit(1)

    assert getattr(
        backend_module,
        "BASE_URL",
        None,
    ) == "https://api.finmindtrade.com/api/v4/data"

    assert getattr(
        backend_module,
        "GET_ONLY",
        None,
    ) is True

    assert getattr(
        backend_module,
        "ALLOW_REDIRECTS",
        None,
    ) is False

    assert getattr(
        backend_module,
        "MAX_RETRIES",
        None,
    ) == 0

    assert getattr(
        backend_module,
        "ALLOW_CORE_INPUT",
        None,
    ) is False

    assert getattr(
        backend_module,
        "ALLOW_SUPABASE_WRITE",
        None,
    ) is False

    assert getattr(
        backend_module,
        "ALLOW_PRODUCTION_WRITE",
        None,
    ) is False

    print("[PASS] backend capability flags fail closed")

    backend_class = getattr(
        backend_module,
        "FinMindReadOnlyBackend",
        None,
    )
    assert backend_class is not None, (
        "FinMindReadOnlyBackend missing"
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
        content=b'{"test":"offline"}',
    )

    session = FakeSession(response=response)

    backend = backend_class(
        session=session,
    )

    evidence = backend.get(
        url="https://api.finmindtrade.com/api/v4/data",
        headers={
            "Authorization": "Bearer TEST_TOKEN_ONLY",
        },
        timeout=5,
        params={
            "dataset": "TaiwanStockPrice",
            "data_id": "2330",
            "start_date": "2026-09-23",
            "end_date": "2026-09-23",
        },
        allow_redirects=False,
        max_bytes=5_000_000,
    )

    assert len(session.calls) == 1
    call = session.calls[0]

    assert call["url"] == (
        "https://api.finmindtrade.com/api/v4/data"
    )

    assert call["timeout"] == 5
    assert call["allow_redirects"] is False

    assert call["params"]["dataset"] == (
        "TaiwanStockPrice"
    )

    assert call["params"]["data_id"] == "2330"

    print("[PASS] fake session GET contract enforced")

    assert evidence.get("status_code") == 200
    assert evidence.get("content_type") == (
        "application/json"
    )
    assert evidence.get("payload") == payload
    assert evidence.get("size_bytes") == len(
        b'{"test":"offline"}'
    )

    assert "TEST_TOKEN_ONLY" not in repr(evidence)

    print("[PASS] HTTP evidence preserved without token")

    # Oversized response must fail before payload exposure.
    oversized_response = FakeResponse(
        status_code=200,
        content_type="application/json",
        payload={"data": [{"value": 1}]},
        content=b"x" * 101,
    )

    oversized_session = FakeSession(
        response=oversized_response
    )

    oversized_backend = backend_class(
        session=oversized_session,
    )

    oversized = oversized_backend.get(
        url="https://api.finmindtrade.com/api/v4/data",
        headers=None,
        timeout=5,
        params=None,
        allow_redirects=False,
        max_bytes=100,
    )

    assert oversized.get("size_bytes") == 101
    assert "payload" not in oversized

    print("[PASS] oversized HTTP response blocks payload")

    # Backend exception must be secret-safe.
    failing_session = FakeSession(
        error=RuntimeError(
            "token=TEST_TOKEN_ONLY network failure"
        )
    )

    failing_backend = backend_class(
        session=failing_session,
    )

    failed = failing_backend.get(
        url="https://api.finmindtrade.com/api/v4/data",
        headers={
            "Authorization": "Bearer TEST_TOKEN_ONLY",
        },
        timeout=5,
        params=None,
        allow_redirects=False,
        max_bytes=5_000_000,
    )

    assert failed.get("connection_error") is True
    assert "TEST_TOKEN_ONLY" not in repr(failed)

    print("[PASS] backend exception redacts secret")

    module_text = open(
        backend_module.__file__,
        "r",
        encoding="utf-8",
    ).read().lower()

    forbidden = (
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
            f"forbidden wiring/method detected: {item}"
        )

    print("[PASS] no write/core wiring")

    print(
        "=== GATE 28C.1 FINMIND LIVE BACKEND "
        "CONTRACT RESULT: PASS ==="
    )


if __name__ == "__main__":
    main()
