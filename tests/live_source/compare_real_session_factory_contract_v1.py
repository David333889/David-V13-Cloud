import importlib


class FakeAdapter:
    def __init__(self, max_retries=None):
        self.max_retries = max_retries


class FakeSession:
    def __init__(self):
        self.headers = {}
        self.auth = None
        self.mount_calls = []
        self.get_calls = []

    def mount(self, prefix, adapter):
        self.mount_calls.append({
            "prefix": prefix,
            "adapter": adapter,
        })

    def get(self, *args, **kwargs):
        self.get_calls.append({
            "args": args,
            "kwargs": kwargs,
        })
        raise AssertionError(
            "session factory must not perform GET"
        )


class FakeRequestsModule:
    def __init__(self):
        self.session_calls = 0

    def Session(self):
        self.session_calls += 1
        return FakeSession()


def main():
    print(
        "=== GATE 28D.0 - REAL SESSION FACTORY "
        "CONTRACT V1 ==="
    )

    try:
        factory_module = importlib.import_module(
            "v14.real_session_factory"
        )
    except ModuleNotFoundError:
        print("[FAIL] real session factory module not found")
        raise SystemExit(1)

    assert getattr(
        factory_module,
        "MAX_RETRIES",
        None,
    ) == 0

    assert getattr(
        factory_module,
        "ALLOW_AUTH_PERSISTENCE",
        None,
    ) is False

    assert getattr(
        factory_module,
        "ALLOW_TOKEN_PERSISTENCE",
        None,
    ) is False

    assert getattr(
        factory_module,
        "ALLOW_NETWORK_ON_CREATE",
        None,
    ) is False

    assert getattr(
        factory_module,
        "ALLOW_CORE_INPUT",
        None,
    ) is False

    assert getattr(
        factory_module,
        "ALLOW_SUPABASE_WRITE",
        None,
    ) is False

    assert getattr(
        factory_module,
        "ALLOW_PRODUCTION_WRITE",
        None,
    ) is False

    print("[PASS] factory capability flags fail closed")

    create_factory = getattr(
        factory_module,
        "build_session_factory",
        None,
    )

    assert callable(create_factory), (
        "build_session_factory missing"
    )

    fake_requests = FakeRequestsModule()

    session_factory = create_factory(
        requests_module=fake_requests,
        adapter_class=FakeAdapter,
    )

    assert callable(session_factory)

    print("[PASS] session factory created from injected dependencies")

    session = session_factory()

    assert fake_requests.session_calls == 1
    assert isinstance(session, FakeSession)

    print("[PASS] exactly one session created")

    assert len(session.get_calls) == 0

    print("[PASS] session creation performs zero GET calls")

    assert len(session.mount_calls) == 2

    prefixes = {
        item["prefix"]
        for item in session.mount_calls
    }

    assert prefixes == {
        "https://",
        "http://",
    }

    for item in session.mount_calls:
        adapter = item["adapter"]
        assert isinstance(adapter, FakeAdapter)
        assert adapter.max_retries == 0

    print("[PASS] retry policy fixed at zero")

    authorization_keys = {
        str(key).lower()
        for key in session.headers
    }

    assert "authorization" not in authorization_keys
    assert session.auth is None

    print("[PASS] no persisted authorization or auth")

    module_text = open(
        factory_module.__file__,
        "r",
        encoding="utf-8",
    ).read().lower()

    forbidden = (
        "finmind_api_token=",
        "bearer ",
        "core_engine",
        "runtime_writer",
        "supabase_writer",
        "supabase_persistence",
        ".get(",
        ".post(",
        ".put(",
        ".patch(",
        ".delete(",
    )

    for item in forbidden:
        assert item not in module_text, (
            f"forbidden network/secret/write wiring: {item}"
        )

    print("[PASS] no request/secret/core/write execution")

    print(
        "=== GATE 28D.0 REAL SESSION FACTORY "
        "CONTRACT RESULT: PASS ==="
    )


if __name__ == "__main__":
    main()
