import importlib


def main():
    print("=== GATE 28B.1 - LIVE REQUEST SAFETY CONTRACT V1 ===")

    try:
        safety = importlib.import_module("v14.live_request_safety")
    except ModuleNotFoundError:
        print("[FAIL] live request safety module not found")
        raise SystemExit(1)

    assert getattr(safety, "HTTPS_ONLY", None) is True
    assert getattr(safety, "ALLOW_REDIRECTS", None) is False
    assert getattr(safety, "MAX_TIMEOUT_SECONDS", None) == 30
    assert getattr(safety, "MAX_RESPONSE_BYTES", None) == 5_000_000
    assert getattr(safety, "MAX_RETRIES", None) == 0
    print("[PASS] request safety defaults fail closed")

    validate = getattr(safety, "validate_request", None)
    assert callable(validate), "validate_request missing"

    valid = validate(
        url="https://api.example.invalid/data",
        allowed_hosts={"api.example.invalid"},
        timeout=5,
    )
    assert valid["allowed"] is True, valid
    print("[PASS] allowed HTTPS request accepted")

    http = validate(
        url="http://api.example.invalid/data",
        allowed_hosts={"api.example.invalid"},
        timeout=5,
    )
    assert http["allowed"] is False
    assert http["reason"] == "HTTPS_REQUIRED"
    print("[PASS] HTTP rejected")

    wrong_host = validate(
        url="https://evil.example.invalid/data",
        allowed_hosts={"api.example.invalid"},
        timeout=5,
    )
    assert wrong_host["allowed"] is False
    assert wrong_host["reason"] == "HOST_NOT_ALLOWED"
    print("[PASS] non-allowlisted host rejected")

    no_allowlist = validate(
        url="https://api.example.invalid/data",
        allowed_hosts=set(),
        timeout=5,
    )
    assert no_allowlist["allowed"] is False
    assert no_allowlist["reason"] == "HOST_ALLOWLIST_REQUIRED"
    print("[PASS] missing allowlist fails closed")

    timeout = validate(
        url="https://api.example.invalid/data",
        allowed_hosts={"api.example.invalid"},
        timeout=31,
    )
    assert timeout["allowed"] is False
    assert timeout["reason"] == "TIMEOUT_OUT_OF_RANGE"
    print("[PASS] timeout upper bound enforced")

    secret_url = validate(
        url="https://api.example.invalid/data?token=SECRET123",
        allowed_hosts={"api.example.invalid"},
        timeout=5,
    )
    assert secret_url["allowed"] is False
    assert secret_url["reason"] == "SECRET_IN_URL"
    assert "SECRET123" not in repr(secret_url)
    print("[PASS] secret-bearing URL rejected without leakage")

    response_check = getattr(safety, "validate_response_size", None)
    assert callable(response_check), "validate_response_size missing"

    assert response_check(1024)["allowed"] is True

    oversized = response_check(5_000_001)
    assert oversized["allowed"] is False
    assert oversized["reason"] == "RESPONSE_TOO_LARGE"
    print("[PASS] response-size limit enforced")

    module_text = open(
        safety.__file__,
        "r",
        encoding="utf-8",
    ).read().lower()

    forbidden = (
        "requests",
        "httpx",
        "urlopen",
        "core_engine",
        "runtime_writer",
        "supabase_writer",
    )

    for item in forbidden:
        assert item not in module_text, (
            f"forbidden dependency/wiring detected: {item}"
        )

    print("[PASS] no live/core/write wiring")
    print("=== GATE 28B.1 LIVE REQUEST SAFETY RESULT: PASS ===")


if __name__ == "__main__":
    main()
