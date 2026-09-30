# Gate 28D.2K-2N - Controlled Real Session Factory
# Integration V1.
#
# Expected RED contract test.
#
# Existing real-session factory capability must enter only
# through the latest protected 2M execution chain.
#
# Fake requests dependencies only.
# No real Session, token, GET, or Internet crossing.

from v14.controlled_real_session_factory_integration import (
    build_session_factory_controlled_real_fetch,
)


def main():
    print(
        "=== GATE 28D.2K-2N - CONTROLLED REAL SESSION "
        "FACTORY INTEGRATION V1 ==="
    )

    calls = {
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

    # Invalid injected dependencies must fail before
    # Session creation / GET.

    try:
        build_session_factory_controlled_real_fetch(
            requests_module=None,
            adapter_class=FakeAdapter,
            env={
                "FINMIND_API_TOKEN": "FAKE_TEST_TOKEN",
            },
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
            "missing requests module must fail closed"
        )

    assert calls["session"] == 0
    assert calls["get"] == 0

    try:
        build_session_factory_controlled_real_fetch(
            requests_module=FakeRequestsModule(),
            adapter_class=None,
            env={
                "FINMIND_API_TOKEN": "FAKE_TEST_TOKEN",
            },
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
            "missing adapter class must fail closed"
        )

    assert calls["session"] == 0
    assert calls["get"] == 0

    execute_once = build_session_factory_controlled_real_fetch(
        requests_module=FakeRequestsModule(),
        adapter_class=FakeAdapter,
        env={
            "FINMIND_API_TOKEN": "FAKE_TEST_TOKEN",
        },
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

    # Building the integration must not create Session / GET.
    assert calls["session"] == 0
    assert calls["get"] == 0

    first = execute_once()

    assert first["allowed"] is True
    assert calls["session"] == 1
    assert calls["get"] == 1

    second = execute_once()

    assert second["allowed"] is False
    assert second["reason"] == "REAL_GET_LIMIT_REACHED"

    assert calls["session"] == 1
    assert calls["get"] == 1

    print("[PASS] missing requests dependency fails closed")
    print("[PASS] missing adapter dependency fails closed")
    print("[PASS] build creates no session / GET")
    print("[PASS] session factory enters protected 2M chain")
    print("[PASS] first execution creates one fake session")
    print("[PASS] first execution reaches fake GET exactly once")
    print("[PASS] second execution denied before session / GET")
    print("[PASS] fake requests dependencies only")

    print(
        "=== GATE 28D.2K-2N CONTROLLED REAL SESSION "
        "FACTORY INTEGRATION RESULT: PASS ==="
    )


if __name__ == "__main__":
    main()
