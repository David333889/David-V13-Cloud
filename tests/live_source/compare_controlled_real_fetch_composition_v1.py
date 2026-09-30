# Gate 28D.2K-2J - Controlled Real Fetch Composition V1.
#
# Expected RED contract test.
#
# Compose the protected 2I one-shot wiring with the
# existing controlled live-fetch path using fake runtime
# boundaries only.
#
# No real requests Session, real token, real GET,
# or Internet crossing is permitted by this test.

from v14.controlled_real_fetch_composition import (
    build_controlled_real_fetch_composition,
)


def main():
    print(
        "=== GATE 28D.2K-2J - CONTROLLED REAL "
        "FETCH COMPOSITION V1 ==="
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

            assert url == (
                "https://api.finmindtrade.com/api/v4/data"
            )
            assert allow_redirects is False
            assert params.get("token") == "FAKE_TEST_TOKEN"

            return FakeResponse()

    def fake_session_factory():
        calls["session_factory"] += 1
        return FakeSession()

    execute_once = build_controlled_real_fetch_composition(
        env={
            "FINMIND_API_TOKEN": "FAKE_TEST_TOKEN",
        },
        session_factory=fake_session_factory,
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

    # Building composition must do nothing.
    assert calls["session_factory"] == 0
    assert calls["get"] == 0

    first = execute_once()

    assert first["allowed"] is True
    assert calls["session_factory"] == 1
    assert calls["get"] == 1

    # Second opportunity must stop at the one-shot guard.
    second = execute_once()

    assert second["allowed"] is False
    assert second["reason"] == "REAL_GET_LIMIT_REACHED"

    assert calls["session_factory"] == 1
    assert calls["get"] == 1

    # Semantic identity mismatch must fail closed
    # before Session creation / GET.

    mismatch_calls = {
        "session_factory": 0,
        "get": 0,
    }

    class MismatchFakeSession:
        def get(
            self,
            url,
            headers=None,
            timeout=None,
            params=None,
            allow_redirects=False,
        ):
            mismatch_calls["get"] += 1
            return FakeResponse()

    def mismatch_session_factory():
        mismatch_calls["session_factory"] += 1
        return MismatchFakeSession()

    stock_mismatch = build_controlled_real_fetch_composition(
        env={
            "FINMIND_API_TOKEN": "FAKE_TEST_TOKEN",
        },
        session_factory=mismatch_session_factory,
        url="https://api.finmindtrade.com/api/v4/data",
        timeout=5,
        params={
            "dataset": "TaiwanStockPrice",
            "data_id": "2317",
            "start_date": "2026-09-29",
            "end_date": "2026-09-29",
        },
        stock_id="2330",
        trading_date="2026-09-29",
    )

    stock_result = stock_mismatch()

    assert stock_result["allowed"] is False
    assert stock_result["reason"] == "STOCK_ID_MISMATCH"
    assert mismatch_calls["session_factory"] == 0
    assert mismatch_calls["get"] == 0

    date_mismatch = build_controlled_real_fetch_composition(
        env={
            "FINMIND_API_TOKEN": "FAKE_TEST_TOKEN",
        },
        session_factory=mismatch_session_factory,
        url="https://api.finmindtrade.com/api/v4/data",
        timeout=5,
        params={
            "dataset": "TaiwanStockPrice",
            "data_id": "2330",
            "start_date": "2026-09-28",
            "end_date": "2026-09-29",
        },
        stock_id="2330",
        trading_date="2026-09-29",
    )

    date_result = date_mismatch()

    assert date_result["allowed"] is False
    assert date_result["reason"] == "TRADING_DATE_MISMATCH"
    assert mismatch_calls["session_factory"] == 0
    assert mismatch_calls["get"] == 0

    print("[PASS] stock identity mismatch fails closed")
    print("[PASS] trading-date mismatch fails closed")
    print("[PASS] build performs no session creation")
    print("[PASS] first execution reaches fake GET exactly once")
    print("[PASS] second execution denied before session / GET")
    print("[PASS] fake token only; no real runtime secret")
    print("[PASS] fake session only; no real Internet crossing")

    print(
        "=== GATE 28D.2K-2J CONTROLLED REAL "
        "FETCH COMPOSITION RESULT: PASS ==="
    )


if __name__ == "__main__":
    main()
