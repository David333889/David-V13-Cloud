# Gate 28D.2K-2P - Controlled Runtime Entry
# Integration V1.
#
# Expected RED contract test.
#
# The controlled runtime entry may delegate only into
# the already protected 2O runtime-environment chain.
#
# Fake environment and fake requests dependencies only.
# No real token, Session, GET, or Internet crossing.

from v14.controlled_runtime_entry_integration import (
    build_controlled_runtime_entry,
)


def main():
    print(
        "=== GATE 28D.2K-2P - CONTROLLED RUNTIME "
        "ENTRY INTEGRATION V1 ==="
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
        headers = {
            "Content-Type": "application/json",
        }
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
                {
                    "prefix": prefix,
                    "adapter": adapter,
                }
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
        }

    # Invalid stock/date inputs must fail closed through
    # the existing downstream request-validation boundary,
    # before Session creation / GET.

    invalid_stock = build_controlled_runtime_entry(
        environment_reader=fake_environment_reader,
        requests_module=FakeRequestsModule(),
        adapter_class=FakeAdapter,
        stock_id="2330,2317",
        trading_date="2026-09-29",
    )

    invalid_stock_result = invalid_stock()

    assert invalid_stock_result["allowed"] is False
    assert invalid_stock_result["reason"] == "DATA_ID_INVALID"
    assert calls["session"] == 0
    assert calls["get"] == 0

    invalid_date = build_controlled_runtime_entry(
        environment_reader=fake_environment_reader,
        requests_module=FakeRequestsModule(),
        adapter_class=FakeAdapter,
        stock_id="2330",
        trading_date="2026/09/29",
    )

    invalid_date_result = invalid_date()

    assert invalid_date_result["allowed"] is False
    assert invalid_date_result["reason"] == "DATE_INVALID"
    assert calls["session"] == 0
    assert calls["get"] == 0

    # Reset only the environment-reader counter before
    # the valid-path assertions below.
    calls["environment"] = 0

    execute_once = build_controlled_runtime_entry(
        environment_reader=fake_environment_reader,
        requests_module=FakeRequestsModule(),
        adapter_class=FakeAdapter,
        stock_id="2330",
        trading_date="2026-09-29",
    )

    assert callable(execute_once)

    # Runtime-entry construction may read the injected
    # environment through 2O, but must not create Session / GET.
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

    print("[PASS] invalid stock fails closed before session / GET")
    print("[PASS] invalid date fails closed before session / GET")
    print("[PASS] runtime entry delegates into protected 2O chain")
    print("[PASS] build creates no session / GET")
    print("[PASS] first execution reaches fake GET exactly once")
    print("[PASS] second execution denied before session / GET")
    print("[PASS] runtime secret excluded from public result")
    print("[PASS] fake runtime boundaries only")

    print(
        "=== GATE 28D.2K-2P CONTROLLED RUNTIME "
        "ENTRY INTEGRATION RESULT: PASS ==="
    )


if __name__ == "__main__":
    main()
