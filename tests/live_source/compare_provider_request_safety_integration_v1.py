import importlib


class MockTransport:
    def __init__(self, response=None):
        self.response = response
        self.calls = []

    def get(self, url, headers=None, timeout=None, params=None):
        self.calls.append({
            "url": url,
            "headers": headers,
            "timeout": timeout,
            "params": params,
        })
        return self.response


def main():
    print("=== GATE 28B.2 - PROVIDER REQUEST SAFETY INTEGRATION V1 ===")

    try:
        pipeline = importlib.import_module(
            "v14.provider_request_pipeline"
        )
    except ModuleNotFoundError:
        print("[FAIL] provider request pipeline module not found")
        raise SystemExit(1)

    execute = getattr(
        pipeline,
        "execute_safe_provider_request",
        None,
    )
    assert callable(execute), (
        "execute_safe_provider_request missing"
    )

    response = {
        "status_code": 200,
        "content_type": "application/json",
        "payload": {
            "data": [{"value": 0}],
        },
    }

    # Valid request: transport must run exactly once.
    transport = MockTransport(response)

    result = execute(
        transport=transport,
        url="https://api.example.invalid/data",
        allowed_hosts={"api.example.invalid"},
        token="TEST_TOKEN_ONLY",
        timeout=5,
        params={"dataset": "TEST_DATASET"},
    )

    assert len(transport.calls) == 1
    assert result.get("classification") == "RAW_EVIDENCE"
    assert result.get("evidence") == response
    assert "TEST_TOKEN_ONLY" not in repr(result)

    print("[PASS] valid request reaches mock transport once")

    # HTTP must fail before transport.
    transport = MockTransport(response)

    result = execute(
        transport=transport,
        url="http://api.example.invalid/data",
        allowed_hosts={"api.example.invalid"},
        token="TEST_TOKEN_ONLY",
        timeout=5,
    )

    assert len(transport.calls) == 0
    assert result.get("allowed") is False
    assert result.get("reason") == "HTTPS_REQUIRED"

    print("[PASS] HTTP blocked before transport")

    # Wrong host must fail before transport.
    transport = MockTransport(response)

    result = execute(
        transport=transport,
        url="https://evil.example.invalid/data",
        allowed_hosts={"api.example.invalid"},
        token="TEST_TOKEN_ONLY",
        timeout=5,
    )

    assert len(transport.calls) == 0
    assert result.get("reason") == "HOST_NOT_ALLOWED"

    print("[PASS] non-allowlisted host blocked before transport")

    # Missing allowlist must fail closed.
    transport = MockTransport(response)

    result = execute(
        transport=transport,
        url="https://api.example.invalid/data",
        allowed_hosts=set(),
        token="TEST_TOKEN_ONLY",
        timeout=5,
    )

    assert len(transport.calls) == 0
    assert result.get("reason") == "HOST_ALLOWLIST_REQUIRED"

    print("[PASS] missing allowlist blocked before transport")

    # Excessive timeout must fail before transport.
    transport = MockTransport(response)

    result = execute(
        transport=transport,
        url="https://api.example.invalid/data",
        allowed_hosts={"api.example.invalid"},
        token="TEST_TOKEN_ONLY",
        timeout=31,
    )

    assert len(transport.calls) == 0
    assert result.get("reason") == "TIMEOUT_OUT_OF_RANGE"

    print("[PASS] excessive timeout blocked before transport")

    # Secret-bearing URL must fail before transport and not leak.
    transport = MockTransport(response)

    result = execute(
        transport=transport,
        url="https://api.example.invalid/data?token=SECRET123",
        allowed_hosts={"api.example.invalid"},
        token="TEST_TOKEN_ONLY",
        timeout=5,
    )

    assert len(transport.calls) == 0
    assert result.get("reason") == "SECRET_IN_URL"
    assert "SECRET123" not in repr(result)
    assert "TEST_TOKEN_ONLY" not in repr(result)

    print("[PASS] secret URL blocked without leakage")

    module_text = open(
        pipeline.__file__,
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

    print("[PASS] no live/core/write wiring")
    print(
        "=== GATE 28B.2 PROVIDER REQUEST SAFETY "
        "INTEGRATION RESULT: PASS ==="
    )


if __name__ == "__main__":
    main()
