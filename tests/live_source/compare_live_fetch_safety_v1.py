import importlib


def main():
    print("=== GATE 28A - LIVE FETCH SAFETY CONTRACT V1 ===")

    try:
        safety = importlib.import_module("v14.live_fetch_safety")
    except ModuleNotFoundError:
        print("[FAIL] live fetch safety module not found")
        raise SystemExit(1)

    required_flags = {
        "GET_ONLY": True,
        "ALLOW_NETWORK_WRITE": False,
        "ALLOW_CORE_INPUT": False,
        "ALLOW_SUPABASE_WRITE": False,
        "ALLOW_PRODUCTION_WRITE": False,
    }

    for name, expected in required_flags.items():
        actual = getattr(safety, name, None)
        assert actual is expected, (
            f"{name}: expected {expected!r}, got {actual!r}"
        )

    print("[PASS] capability flags fail closed")

    classify = getattr(safety, "classify_fetch_response", None)
    assert callable(classify), "classify_fetch_response missing"

    rate_limited = classify({
        "status_code": 429,
        "content_type": "application/json",
        "payload": {"data": []},
    })
    assert rate_limited == "RATE_LIMITED", rate_limited
    print("[PASS] rate-limit classified")

    invalid_content_type = classify({
        "status_code": 200,
        "content_type": "text/html",
        "payload": {"data": [{"value": 1}]},
    })
    assert invalid_content_type == "CONTENT_TYPE_INVALID", invalid_content_type
    print("[PASS] content-type guarded")

    raw_evidence = classify({
        "status_code": 200,
        "content_type": "application/json; charset=utf-8",
        "payload": {"data": [{"value": 0}]},
    })
    assert raw_evidence == "RAW_EVIDENCE", raw_evidence
    print("[PASS] valid JSON remains raw evidence")

    sanitize = getattr(safety, "sanitize_secret", None)
    assert callable(sanitize), "sanitize_secret missing"

    secret = "TOP_SECRET_123"
    sanitized = sanitize(
        f"token={secret} Authorization: Bearer {secret}"
    )
    assert secret not in sanitized
    print("[PASS] secret redaction contract")

    provenance_fn = getattr(safety, "build_raw_provenance", None)
    assert callable(provenance_fn), "build_raw_provenance missing"

    provenance = provenance_fn(
        provider="TEST_PROVIDER",
        dataset="TEST_DATASET",
        status_code=200,
        content_type="application/json",
        payload={"data": [{"value": 0}]},
    )

    assert isinstance(provenance, dict)
    assert provenance.get("provider") == "TEST_PROVIDER"
    assert provenance.get("dataset") == "TEST_DATASET"
    assert provenance.get("status_code") == 200
    assert provenance.get("content_type") == "application/json"
    assert provenance.get("payload_hash")
    print("[PASS] raw provenance preserved")

    forbidden_names = (
        "core_engine",
        "runtime_writer",
        "supabase_writer",
    )

    module_text = open(
        safety.__file__,
        "r",
        encoding="utf-8",
    ).read().lower()

    for forbidden in forbidden_names:
        assert forbidden not in module_text, (
            f"forbidden wiring detected: {forbidden}"
        )

    print("[PASS] no core/write wiring")
    print("=== GATE 28A LIVE FETCH SAFETY RESULT: PASS ===")


if __name__ == "__main__":
    main()
