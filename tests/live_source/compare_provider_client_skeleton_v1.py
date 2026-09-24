import importlib


class MockTransport:
    def __init__(self, response=None, error=None):
        self.response = response
        self.error = error
        self.calls = []

    def get(self, url, headers=None, timeout=None, params=None):
        self.calls.append({
            "url": url,
            "headers": headers,
            "timeout": timeout,
            "params": params,
        })

        if self.error is not None:
            raise self.error

        return self.response


def main():
    print("=== GATE 28B - PROVIDER CLIENT SKELETON V1 ===")

    try:
        client = importlib.import_module("v14.provider_client")
    except ModuleNotFoundError:
        print("[FAIL] provider client module not found")
        raise SystemExit(1)

    assert getattr(client, "GET_ONLY", None) is True
    assert getattr(client, "ALLOW_LIVE_NETWORK", None) is False
    assert getattr(client, "ALLOW_CORE_INPUT", None) is False
    assert getattr(client, "ALLOW_SUPABASE_WRITE", None) is False
    assert getattr(client, "ALLOW_PRODUCTION_WRITE", None) is False
    print("[PASS] provider capability flags fail closed")

    fetch = getattr(client, "fetch_provider_data", None)
    assert callable(fetch), "fetch_provider_data missing"

    response = {
        "status_code": 200,
        "content_type": "application/json",
        "payload": {
            "data": [
                {"value": 0},
            ],
        },
    }

    transport = MockTransport(response=response)

    evidence = fetch(
        transport=transport,
        url="https://example.invalid/mock",
        token="TEST_TOKEN_ONLY",
        timeout=5,
        params={"dataset": "TEST_DATASET"},
    )

    assert len(transport.calls) == 1
    call = transport.calls[0]

    assert call["url"] == "https://example.invalid/mock"
    assert call["timeout"] == 5
    assert call["params"] == {"dataset": "TEST_DATASET"}

    headers = call["headers"]
    assert isinstance(headers, dict)
    assert headers.get("Authorization") == "Bearer TEST_TOKEN_ONLY"

    print("[PASS] mock transport dependency injection")

    assert evidence == response
    assert "TEST_TOKEN_ONLY" not in repr(evidence)
    print("[PASS] raw fetch evidence preserved without token")

    classify = getattr(client, "classify_provider_evidence", None)
    assert callable(classify), "classify_provider_evidence missing"

    result = classify(evidence)
    assert result == "RAW_EVIDENCE", result
    print("[PASS] Gate 28A safety classification reused")

    zero = evidence["payload"]["data"][0]["value"]
    assert zero == 0
    print("[PASS] explicit zero preserved")

    failing_transport = MockTransport(
        error=RuntimeError("token=TEST_TOKEN_ONLY transport failure")
    )

    failed = fetch(
        transport=failing_transport,
        url="https://example.invalid/mock",
        token="TEST_TOKEN_ONLY",
        timeout=5,
        params=None,
    )

    assert isinstance(failed, dict)
    assert failed.get("connection_error") is True
    assert "TEST_TOKEN_ONLY" not in repr(failed)
    print("[PASS] transport failure fails closed and redacts secret")

    module_text = open(
        client.__file__,
        "r",
        encoding="utf-8",
    ).read().lower()

    forbidden = (
        "import requests",
        "import httpx",
        "import urllib",
        "urlopen",
        "core_engine",
        "runtime_writer",
        "supabase_writer",
        "os.environ",
    )

    for item in forbidden:
        assert item not in module_text, (
            f"forbidden dependency/wiring detected: {item}"
        )

    print("[PASS] no live/core/write wiring")
    print("=== GATE 28B PROVIDER CLIENT SKELETON RESULT: PASS ===")


if __name__ == "__main__":
    main()
