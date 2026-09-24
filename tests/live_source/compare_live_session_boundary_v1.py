import importlib


class FakeSession:
    def __init__(self):
        self.calls = []
        self.closed = False

    def get(
        self,
        url,
        headers=None,
        timeout=None,
        params=None,
        allow_redirects=None,
    ):
        self.calls.append({
            "method": "GET",
            "url": url,
            "headers": headers,
            "timeout": timeout,
            "params": params,
            "allow_redirects": allow_redirects,
        })

        return {
            "fake": True,
        }

    def close(self):
        self.closed = True


class FakeSessionFactory:
    def __init__(self):
        self.calls = 0
        self.sessions = []

    def __call__(self):
        self.calls += 1

        session = FakeSession()
        self.sessions.append(session)

        return session


def main():
    print("=== GATE 28C.2 - LIVE SESSION BOUNDARY V1 ===")

    try:
        boundary = importlib.import_module(
            "v14.live_session_boundary"
        )
    except ModuleNotFoundError:
        print("[FAIL] live session boundary module not found")
        raise SystemExit(1)

    assert getattr(
        boundary,
        "FINMIND_HOST",
        None,
    ) == "api.finmindtrade.com"

    assert getattr(
        boundary,
        "GET_ONLY",
        None,
    ) is True

    assert getattr(
        boundary,
        "ALLOW_REDIRECTS",
        None,
    ) is False

    assert getattr(
        boundary,
        "MAX_RETRIES",
        None,
    ) == 0

    assert getattr(
        boundary,
        "MAX_TIMEOUT_SECONDS",
        None,
    ) == 30

    assert getattr(
        boundary,
        "ALLOW_CORE_INPUT",
        None,
    ) is False

    assert getattr(
        boundary,
        "ALLOW_SUPABASE_WRITE",
        None,
    ) is False

    assert getattr(
        boundary,
        "ALLOW_PRODUCTION_WRITE",
        None,
    ) is False

    print("[PASS] session capability flags fail closed")

    create_session = getattr(
        boundary,
        "create_live_session",
        None,
    )

    assert callable(create_session), (
        "create_live_session missing"
    )

    factory = FakeSessionFactory()

    result = create_session(
        session_factory=factory,
    )

    assert isinstance(result, dict)
    assert result.get("allowed") is True

    session = result.get("session")
    assert session is not None

    assert factory.calls == 1
    assert len(factory.sessions) == 1

    print("[PASS] session created only through injected factory")

    validate_target = getattr(
        boundary,
        "validate_live_target",
        None,
    )

    assert callable(validate_target), (
        "validate_live_target missing"
    )

    valid = validate_target(
        url="https://api.finmindtrade.com/api/v4/data",
        timeout=5,
    )

    assert valid.get("allowed") is True

    print("[PASS] FinMind HTTPS target accepted")

    wrong_scheme = validate_target(
        url="http://api.finmindtrade.com/api/v4/data",
        timeout=5,
    )

    assert wrong_scheme.get("allowed") is False
    assert wrong_scheme.get("reason") == "HTTPS_REQUIRED"

    print("[PASS] HTTP target rejected")

    wrong_host = validate_target(
        url="https://example.com/api/v4/data",
        timeout=5,
    )

    assert wrong_host.get("allowed") is False
    assert wrong_host.get("reason") == "HOST_NOT_ALLOWED"

    print("[PASS] non-FinMind host rejected")

    excessive_timeout = validate_target(
        url="https://api.finmindtrade.com/api/v4/data",
        timeout=31,
    )

    assert excessive_timeout.get("allowed") is False
    assert excessive_timeout.get("reason") == (
        "TIMEOUT_OUT_OF_RANGE"
    )

    print("[PASS] timeout upper bound enforced")

    missing_factory = create_session(
        session_factory=None,
    )

    assert missing_factory.get("allowed") is False
    assert missing_factory.get("reason") == (
        "SESSION_FACTORY_REQUIRED"
    )

    print("[PASS] missing session factory fails closed")

    module_text = open(
        boundary.__file__,
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
        "finmind_api_token=",
        "bearer ",
    )

    for item in forbidden:
        assert item not in module_text, (
            f"forbidden wiring/method/secret detected: {item}"
        )

    print("[PASS] no write/core/secret wiring")

    print(
        "=== GATE 28C.2 LIVE SESSION "
        "BOUNDARY RESULT: PASS ==="
    )


if __name__ == "__main__":
    main()
