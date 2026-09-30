# Gate 28D.2K-2O - Controlled Runtime Environment
# Integration V1.
#
# Expected RED contract test.
#
# Runtime environment access must be injected.
# Only the required FinMind token may enter the env mapping
# passed into the already protected 2N chain.
#
# Fake environment and fake requests dependencies only.
# No real token, Session, GET, or Internet crossing.

from v14.controlled_runtime_environment_integration import (
    build_runtime_environment_controlled_real_fetch,
)


def main():
    print(
        "=== GATE 28D.2K-2O - CONTROLLED RUNTIME "
        "ENVIRONMENT INTEGRATION V1 ==="
    )

    calls = {
        "environment": 0,
        "session": 0,
        "get": 0,
    }

    class FakeAdapter:
        def __init__(self, max_retries=None):
            self.max_retries = max_retries

    class FakeResponse:
        status_code = 200
        headers = {"Content-Type": "application/json"}
        content = b'{"data": []}'

        def json(self):
            return {"data": []}

    class FakeSession:
        def __init__(self):
            self.headers = {}
            self.auth = None
            self.mount_calls = []

        def mount(self, prefix, adapter):
            self.mount_calls.append(
                {"prefix": prefix, "adapter": adapter}
            )

        def get(
            self,
            url,
            headers=None,
            timeout=None,
            params=None,
            allow_redirects=False,
        ):
            calls["get"] += 1
            return FakeResponse()

    class FakeRequestsModule:
        def Session(self):
            calls["session"] += 1
            return FakeSession()

    def fake_environment_reader():
        calls["environment"] += 1
        return {
            "FINMIND_API_TOKEN": "FAKE_TEST_TOKEN",
            "UNRELATED_SECRET": "MUST_NOT_PROPAGATE",
        }

    # Invalid runtime-environment dependencies must fail
    # before Session creation / GET.

    try:
        build_runtime_environment_controlled_real_fetch(
            environment_reader=None,
            requests_module=FakeRequestsModule(),
            adapter_class=FakeAdapter,
            url="https://api.finmindtrade.com/api/v4/data",
            timeout=5,
            params={
                "dataset": "TaiwanStockPrice",
                "data_id": "2330",
                "start_date": "2026-09-29",
                "end_date": "2026-09-29",
            },
            stock_id="2330",
            trading_date="2026-09-29",
        )
    except ValueError:
        pass
    else:
        raise AssertionError(
            "missing environment reader must fail closed"
        )

    assert calls["environment"] == 0
    assert calls["session"] == 0
    assert calls["get"] == 0

    def invalid_environment_reader():
        calls["environment"] += 1
        return "INVALID_ENVIRONMENT"

    try:
        build_runtime_environment_controlled_real_fetch(
            environment_reader=invalid_environment_reader,
            requests_module=FakeRequestsModule(),
            adapter_class=FakeAdapter,
            url="https://api.finmindtrade.com/api/v4/data",
            timeout=5,
            params={
                "dataset": "TaiwanStockPrice",
                "data_id": "2330",
                "start_date": "2026-09-29",
                "end_date": "2026-09-29",
            },
            stock_id="2330",
            trading_date="2026-09-29",
        )
    except ValueError:
        pass
    else:
        raise AssertionError(
            "invalid environment mapping must fail closed"
        )

    assert calls["environment"] == 1
    assert calls["session"] == 0
    assert calls["get"] == 0

    # Reset only the environment-reader counter before
    # the valid-path assertions below.
    calls["environment"] = 0

    execute_once = build_runtime_environment_controlled_real_fetch(
        environment_reader=fake_environment_reader,
        requests_module=FakeRequestsModule(),
        adapter_class=FakeAdapter,
        url="https://api.finmindtrade.com/api/v4/data",
        timeout=5,
        params={
            "dataset": "TaiwanStockPrice",
            "data_id": "2330",
            "start_date": "2026-09-29",
            "end_date": "2026-09-29",
        },
        stock_id="2330",
        trading_date="2026-09-29",
    )

    assert callable(execute_once)

    # Environment may be read during build, but Session / GET
    # must not occur during build.
    assert calls["environment"] == 1
    assert calls["session"] == 0
    assert calls["get"] == 0

    first = execute_once()

    assert first["allowed"] is True
    assert calls["session"] == 1
    assert calls["get"] == 1

    second = execute_once()

    assert second["allowed"] is False
    assert second["reason"] == "REAL_GET_LIMIT_REACHED"
    assert calls["environment"] == 1
    assert calls["session"] == 1
    assert calls["get"] == 1

    public_text = repr(first)

    assert "FAKE_TEST_TOKEN" not in public_text
    assert "MUST_NOT_PROPAGATE" not in public_text

    print("[PASS] missing environment reader fails closed")
    print("[PASS] invalid environment mapping fails closed")
    print("[PASS] runtime environment access injected")
    print("[PASS] build creates no session / GET")
    print("[PASS] first execution reaches fake GET once")
    print("[PASS] second execution denied before session / GET")
    print("[PASS] runtime secrets excluded from public result")
    print("[PASS] fake runtime boundaries only")

    print(
        "=== GATE 28D.2K-2O CONTROLLED RUNTIME "
        "ENVIRONMENT INTEGRATION RESULT: PASS ==="
    )


if __name__ == "__main__":
    main()
