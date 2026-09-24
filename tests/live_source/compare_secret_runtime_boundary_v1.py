import importlib


def main():
    print("=== GATE 28B.4 - SECRET RUNTIME BOUNDARY V1 ===")

    try:
        secret_runtime = importlib.import_module(
            "v14.secret_runtime"
        )
    except ModuleNotFoundError:
        print("[FAIL] secret runtime module not found")
        raise SystemExit(1)

    assert getattr(
        secret_runtime,
        "DEFAULT_TOKEN_ENV_NAME",
        None,
    ) == "FINMIND_API_TOKEN"

    assert getattr(
        secret_runtime,
        "ALLOW_SOURCE_SECRET",
        None,
    ) is False

    assert getattr(
        secret_runtime,
        "ALLOW_SECRET_IN_EVIDENCE",
        None,
    ) is False

    assert getattr(
        secret_runtime,
        "ALLOW_SECRET_IN_ERROR",
        None,
    ) is False

    print("[PASS] secret capability flags fail closed")

    load_secret = getattr(
        secret_runtime,
        "load_runtime_secret",
        None,
    )
    assert callable(load_secret), "load_runtime_secret missing"

    # Missing secret must fail closed.
    missing = load_secret(
        env={},
        name="FINMIND_API_TOKEN",
    )

    assert missing.get("available") is False
    assert missing.get("reason") == "SECRET_MISSING"
    assert "secret" not in missing

    print("[PASS] missing secret fails closed")

    # Blank secret must fail closed.
    blank = load_secret(
        env={
            "FINMIND_API_TOKEN": "   ",
        },
        name="FINMIND_API_TOKEN",
    )

    assert blank.get("available") is False
    assert blank.get("reason") == "SECRET_BLANK"
    assert "secret" not in blank

    print("[PASS] blank secret fails closed")

    # Fake runtime secret only.
    fake_secret = "TEST_RUNTIME_SECRET_ONLY"

    loaded = load_secret(
        env={
            "FINMIND_API_TOKEN": fake_secret,
        },
        name="FINMIND_API_TOKEN",
    )

    assert loaded.get("available") is True
    assert loaded.get("secret") == fake_secret

    print("[PASS] runtime secret loaded from injected environment")

    # Public metadata must never expose the secret.
    public_view = getattr(
        secret_runtime,
        "build_secret_metadata",
        None,
    )
    assert callable(public_view), "build_secret_metadata missing"

    metadata = public_view(
        loaded,
        name="FINMIND_API_TOKEN",
    )

    assert metadata.get("available") is True
    assert metadata.get("name") == "FINMIND_API_TOKEN"
    assert fake_secret not in repr(metadata)
    assert "secret" not in metadata

    print("[PASS] secret excluded from public metadata")

    # Safe error must redact a secret if an exception contains it.
    safe_error = getattr(
        secret_runtime,
        "sanitize_runtime_error",
        None,
    )
    assert callable(safe_error), "sanitize_runtime_error missing"

    sanitized = safe_error(
        f"token={fake_secret} runtime failure"
    )

    assert fake_secret not in sanitized

    print("[PASS] runtime error redacts secret")

    module_text = open(
        secret_runtime.__file__,
        "r",
        encoding="utf-8",
    ).read()

    assert "TEST_RUNTIME_SECRET_ONLY" not in module_text
    assert "FINMIND_API_TOKEN=" not in module_text

    forbidden = (
        "core_engine",
        "runtime_writer",
        "supabase_writer",
        "requests",
        "httpx",
        "urlopen(",
    )

    lowered = module_text.lower()

    for item in forbidden:
        assert item not in lowered, (
            f"forbidden dependency/wiring detected: {item}"
        )

    print("[PASS] no hardcoded/live/core/write wiring")

    print(
        "=== GATE 28B.4 SECRET RUNTIME "
        "BOUNDARY RESULT: PASS ==="
    )


if __name__ == "__main__":
    main()
