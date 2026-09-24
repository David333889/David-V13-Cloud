import importlib


class MockBackend:
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
        max_bytes=None,
    ):
        self.calls.append({
            "url": url,
            "headers": headers,
            "timeout": timeout,
            "params": params,
            "allow_redirects": allow_redirects,
            "max_bytes": max_bytes,
        })

        if self.error is not None:
            raise self.error

        return self.response


def main():
    print("=== GATE 28B.3 - READ-ONLY TRANSPORT CONTRACT V1 ===")

    try:
        transport_module = importlib.import_module(
            "v14.read_only_transport"
        )
    except ModuleNotFoundError:
        print("[FAIL] read-only transport module not found")
        raise SystemExit(1)

    assert getattr(
        transport_module,
        "GET_ONLY",
        None,
    ) is True

    assert getattr(
        transport_module,
        "ALLOW_REDIRECTS",
        None,
    ) is False

    assert getattr(
        transport_module,
        "MAX_RETRIES",
        None,
    ) == 0

    assert getattr(
        transport_module,
        "ALLOW_LIVE_NETWORK",
        None,
    ) is False

    print("[PASS] transport capability flags fail closed")

    transport_class = getattr(
        transport_module,
        "ReadOnlyTransport",
        None,
    )
    assert transport_class is not None, (
        "ReadOnlyTransport missing"
    )

    response = {
        "status_code": 200,
        "content_type": "application/json",
        "payload": {
            "data": [{"value": 0}],
        },
        "size_bytes": 128,
    }

    backend = MockBackend(response=response)

    transport = transport_class(
        backend=backend,
        max_response_bytes=5_000_000,
    )

    evidence = transport.get(
        "https://api.example.invalid/data",
        headers={
            "Authorization": "Bearer TEST_TOKEN_ONLY",
        },
        timeout=5,
        params={
            "dataset": "TEST_DATASET",
        },
    )

    assert len(backend.calls) == 1
    call = backend.calls[0]

    assert call["url"] == (
        "https://api.example.invalid/data"
    )
    assert call["timeout"] == 5
    assert call["params"] == {
        "dataset": "TEST_DATASET",
    }
    assert call["allow_redirects"] is False
    assert call["max_bytes"] == 5_000_000

    print("[PASS] GET-only backend contract enforced")

    assert evidence.get("status_code") == 200
    assert evidence.get("content_type") == (
        "application/json"
    )
    assert evidence.get("payload") == {
        "data": [{"value": 0}],
    }

    assert "TEST_TOKEN_ONLY" not in repr(evidence)

    print("[PASS] response evidence preserved without token")

    # Oversized response must fail closed.
    oversized_backend = MockBackend(
        response={
            "status_code": 200,
            "content_type": "application/json",
            "payload": {
                "data": [{"value": 1}],
            },
            "size_bytes": 5_000_001,
        }
    )

    oversized_transport = transport_class(
        backend=oversized_backend,
        max_response_bytes=5_000_000,
    )

    oversized = oversized_transport.get(
        "https://api.example.invalid/data",
        headers=None,
        timeout=5,
        params=None,
    )

    assert oversized.get("response_too_large") is True
    assert "payload" not in oversized

    print("[PASS] oversized response fails closed")

    # Backend exception must be converted to safe evidence.
    failing_backend = MockBackend(
        error=RuntimeError(
            "token=TEST_TOKEN_ONLY backend failure"
        )
    )

    failing_transport = transport_class(
        backend=failing_backend,
        max_response_bytes=5_000_000,
    )

    failed = failing_transport.get(
        "https://api.example.invalid/data",
        headers={
            "Authorization": "Bearer TEST_TOKEN_ONLY",
        },
        timeout=5,
        params=None,
    )

    assert failed.get("connection_error") is True
    assert "TEST_TOKEN_ONLY" not in repr(failed)

    print("[PASS] backend exception fails closed without secret")

    module_text = open(
        transport_module.__file__,
        "r",
        encoding="utf-8",
    ).read().lower()

    forbidden = (
        "import requests",
        "from requests",
        "import httpx",
        "from httpx",
        "urlopen(",
        "core_engine",
        "runtime_writer",
        "supabase_writer",
    )

    for item in forbidden:
        assert item not in module_text, (
            f"forbidden dependency/wiring detected: {item}"
        )

    print("[PASS] no real-network/core/write wiring")

    print(
        "=== GATE 28B.3 READ-ONLY TRANSPORT "
        "CONTRACT RESULT: PASS ==="
    )


if __name__ == "__main__":
    main()
