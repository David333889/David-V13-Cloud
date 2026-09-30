# Gate 28D.2K-2K - Controlled Real Request
# Validation Integration V1.
#
# Expected RED contract test.
#
# Invalid FinMind request parameters must fail closed before
# session creation / GET.
#
# Validated parameters may proceed only into the already
# protected 2J composition.
#
# Fake runtime boundaries only.
# No real Session, token, GET, or Internet crossing.

from v14.controlled_real_request_validation_integration import (
    build_validated_controlled_real_fetch,
)


def main():
    print(
        "=== GATE 28D.2K-2K - CONTROLLED REAL REQUEST "
        "VALIDATION INTEGRATION V1 ==="
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

    invalid = build_validated_controlled_real_fetch(
        env={
            "FINMIND_API_TOKEN": "FAKE_TEST_TOKEN",
        },
        session_factory=fake_session_factory,
        url="https://api.finmindtrade.com/api/v4/data",
        timeout=5,
        params={
            "dataset": "OtherDataset",
            "data_id": "2330",
            "start_date": "2026-09-29",
            "end_date": "2026-09-29",
        },
        stock_id="2330",
        trading_date="2026-09-29",
    )

    invalid_result = invalid()

    assert invalid_result["allowed"] is False
    assert invalid_result["reason"] == "DATASET_NOT_ALLOWED"
    assert calls["session_factory"] == 0
    assert calls["get"] == 0

    valid = build_validated_controlled_real_fetch(
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

    # Building must not create a Session or GET.
    assert calls["session_factory"] == 0
    assert calls["get"] == 0

    first = valid()

    assert first["allowed"] is True
    assert calls["session_factory"] == 1
    assert calls["get"] == 1

    second = valid()

    assert second["allowed"] is False
    assert second["reason"] == "REAL_GET_LIMIT_REACHED"
    assert calls["session_factory"] == 1
    assert calls["get"] == 1

    print("[PASS] invalid params denied before session / GET")
    print("[PASS] valid params enter protected 2J composition")
    print("[PASS] first execution reaches fake GET exactly once")
    print("[PASS] second execution denied by one-shot guard")
    print("[PASS] fake runtime boundaries only")

    print(
        "=== GATE 28D.2K-2K CONTROLLED REAL REQUEST "
        "VALIDATION INTEGRATION RESULT: PASS ==="
    )


if __name__ == "__main__":
    main()
