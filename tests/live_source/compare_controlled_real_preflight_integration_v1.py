# Gate 28D.2K-2L - Controlled Real Preflight
# Integration V1.
#
# Expected RED contract test.
#
# Preflight readiness must be checked before the protected
# 2K request-validation / 2J composition path is built.
#
# Fake runtime boundaries only.
# No real Session, token, GET, or Internet crossing.

from v14.controlled_real_preflight_integration import (
    build_preflight_validated_controlled_real_fetch,
)


def main():
    print(
        "=== GATE 28D.2K-2L - CONTROLLED REAL "
        "PREFLIGHT INTEGRATION V1 ==="
    )

    calls = {
        "session_factory": 0,
        "get": 0,
    }

    class FakeResponse:
        status_code = 200
        headers = {
            "Content-Type": "application/json",
        }
        content = b'{"data": []}'

        def json(self):
            return {
                "data": [],
            }

    class FakeSession:
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

    def fake_session_factory():
        calls["session_factory"] += 1
        return FakeSession()

    valid_params = {
        "dataset": "TaiwanStockPrice",
        "data_id": "2330",
        "start_date": "2026-09-29",
        "end_date": "2026-09-29",
    }

    denied_calls = {
        "preflight": 0,
        "session_factory": 0,
        "get": 0,
    }

    def denied_preflight():
        denied_calls["preflight"] += 1
        return {
            "ready": False,
            "network_executed": False,
            "allow_live_get": False,
        }

    def denied_session_factory():
        denied_calls["session_factory"] += 1
        return FakeSession()

    denied = build_preflight_validated_controlled_real_fetch(
        env={
            "FINMIND_API_TOKEN": "FAKE_TEST_TOKEN",
        },
        session_factory=denied_session_factory,
        url="https://api.finmindtrade.com/api/v4/data",
        timeout=5,
        params=valid_params,
        stock_id="2330",
        trading_date="2026-09-29",
        preflight=denied_preflight,
    )

    denied_result = denied()

    assert denied_result["allowed"] is False
    assert denied_result["reason"] == "PREFLIGHT_NOT_READY"
    assert denied_calls["preflight"] == 1
    assert denied_calls["session_factory"] == 0
    assert denied_calls["get"] == 0

    def network_executed_preflight():
        return {
            "ready": True,
            "network_executed": True,
            "allow_live_get": False,
        }

    network_executed = (
        build_preflight_validated_controlled_real_fetch(
            env={
                "FINMIND_API_TOKEN": "FAKE_TEST_TOKEN",
            },
            session_factory=denied_session_factory,
            url="https://api.finmindtrade.com/api/v4/data",
            timeout=5,
            params=valid_params,
            stock_id="2330",
            trading_date="2026-09-29",
            preflight=network_executed_preflight,
        )
    )

    network_result = network_executed()

    assert network_result["allowed"] is False
    assert (
        network_result["reason"]
        == "PREFLIGHT_NETWORK_EXECUTED"
    )
    assert denied_calls["session_factory"] == 0
    assert denied_calls["get"] == 0

    def live_get_enabled_preflight():
        return {
            "ready": True,
            "network_executed": False,
            "allow_live_get": True,
        }

    live_get_enabled = (
        build_preflight_validated_controlled_real_fetch(
            env={
                "FINMIND_API_TOKEN": "FAKE_TEST_TOKEN",
            },
            session_factory=denied_session_factory,
            url="https://api.finmindtrade.com/api/v4/data",
            timeout=5,
            params=valid_params,
            stock_id="2330",
            trading_date="2026-09-29",
            preflight=live_get_enabled_preflight,
        )
    )

    live_get_result = live_get_enabled()

    assert live_get_result["allowed"] is False
    assert (
        live_get_result["reason"]
        == "PREFLIGHT_LIVE_GET_NOT_DISABLED"
    )
    assert denied_calls["session_factory"] == 0
    assert denied_calls["get"] == 0

    execute_once = (
        build_preflight_validated_controlled_real_fetch(
            preflight=lambda: {
                "ready": True,
                "network_executed": False,
                "allow_live_get": False,
            },
            env={
                "FINMIND_API_TOKEN": "FAKE_TEST_TOKEN",
            },
            session_factory=fake_session_factory,
            url="https://api.finmindtrade.com/api/v4/data",
            timeout=5,
            params=valid_params,
            stock_id="2330",
            trading_date="2026-09-29",
        )
    )

    # Building must not create Session / GET.
    assert callable(execute_once)
    assert calls["session_factory"] == 0
    assert calls["get"] == 0

    first = execute_once()

    assert first["allowed"] is True
    assert calls["session_factory"] == 1
    assert calls["get"] == 1

    second = execute_once()

    assert second["allowed"] is False
    assert second["reason"] == "REAL_GET_LIMIT_REACHED"
    assert calls["session_factory"] == 1
    assert calls["get"] == 1

    print("[PASS] preflight network-executed state denied")
    print("[PASS] preflight live-GET-enabled state denied")
    print("[PASS] preflight not-ready fails closed")
    print("[PASS] denied preflight stops before session / GET")
    print("[PASS] preflight integrated before protected fetch path")
    print("[PASS] build performs no session / GET")
    print("[PASS] first execution reaches fake GET exactly once")
    print("[PASS] second execution denied by one-shot guard")
    print("[PASS] fake runtime boundaries only")

    print(
        "=== GATE 28D.2K-2L CONTROLLED REAL "
        "PREFLIGHT INTEGRATION RESULT: PASS ==="
    )


if __name__ == "__main__":
    main()
