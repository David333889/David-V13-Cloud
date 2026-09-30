# Gate 28D.2K-2M - Controlled Real Execution
# Authorization Integration V1.
#
# Expected RED contract test.
#
# Existing 2E execution authorization must be validated
# before entering the protected 2L chain.
#
# Fake runtime boundaries only.
# No real Session, token, GET, or Internet crossing.

from v14.controlled_real_execution_authorization_integration import (
    build_authorized_controlled_real_fetch,
)


def main():
    print(
        "=== GATE 28D.2K-2M - CONTROLLED REAL EXECUTION "
        "AUTHORIZATION INTEGRATION V1 ==="
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
            return {"data": []}

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

    def denied_authorization():
        return {
            "allow_real_get": False,
            "max_real_gets": 1,
        }

    denied = build_authorized_controlled_real_fetch(
        env={"FINMIND_API_TOKEN": "FAKE_TEST_TOKEN"},
        session_factory=fake_session_factory,
        url="https://api.finmindtrade.com/api/v4/data",
        timeout=5,
        params=valid_params,
        stock_id="2330",
        trading_date="2026-09-29",
        authorization=denied_authorization,
    )

    denied_result = denied()

    assert denied_result["allowed"] is False
    assert denied_result["reason"] == "REAL_GET_NOT_AUTHORIZED"
    assert calls["session_factory"] == 0
    assert calls["get"] == 0

    def invalid_limit_authorization():
        return {
            "allow_real_get": True,
            "max_real_gets": 2,
        }

    invalid_limit = build_authorized_controlled_real_fetch(
        env={
            "FINMIND_API_TOKEN": "FAKE_TEST_TOKEN",
        },
        session_factory=fake_session_factory,
        url="https://api.finmindtrade.com/api/v4/data",
        timeout=5,
        params=valid_params,
        stock_id="2330",
        trading_date="2026-09-29",
        authorization=invalid_limit_authorization,
    )

    invalid_limit_result = invalid_limit()

    assert invalid_limit_result["allowed"] is False
    assert (
        invalid_limit_result["reason"]
        == "REAL_GET_LIMIT_INVALID"
    )
    assert calls["session_factory"] == 0
    assert calls["get"] == 0

    def valid_authorization():
        return {
            "allow_real_get": True,
            "max_real_gets": 1,
        }

    execute_once = build_authorized_controlled_real_fetch(
        env={"FINMIND_API_TOKEN": "FAKE_TEST_TOKEN"},
        session_factory=fake_session_factory,
        url="https://api.finmindtrade.com/api/v4/data",
        timeout=5,
        params=valid_params,
        stock_id="2330",
        trading_date="2026-09-29",
        authorization=valid_authorization,
    )

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

    print("[PASS] invalid real-GET limit fails closed")
    print("[PASS] invalid limit stops before session / GET")
    print("[PASS] denied execution authorization fails closed")
    print("[PASS] denied authorization stops before session / GET")
    print("[PASS] valid authorization enters protected 2L chain")
    print("[PASS] first execution reaches fake GET exactly once")
    print("[PASS] second execution denied by existing one-shot guard")
    print("[PASS] fake runtime boundaries only")

    print(
        "=== GATE 28D.2K-2M CONTROLLED REAL EXECUTION "
        "AUTHORIZATION INTEGRATION RESULT: PASS ==="
    )


if __name__ == "__main__":
    main()
