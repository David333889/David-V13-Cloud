import importlib


class FakeAcquisition:
    def __init__(self):
        self.calls = []

    def __call__(self, **kwargs):
        self.calls.append(kwargs)

        return {
            "allowed": True,
            "observed": {
                "date": "2026-09-23",
                "stock_id": "2330",
                "open": 1000,
                "max": 1020,
                "min": 990,
                "close": 1010,
                "Trading_Volume": 12345678,
            },
        }


def main():
    print(
        "=== GATE 28D.2K-2H - CONTROLLED REAL "
        "ACQUISITION ADAPTER BOUNDARY V1 ==="
    )

    try:
        module = importlib.import_module(
            "v14.controlled_real_acquisition_adapter"
        )
    except ModuleNotFoundError:
        print(
            "[EXPECTED RED] controlled real acquisition "
            "adapter module not found"
        )
        raise SystemExit(1)

    build_executor = getattr(
        module,
        "build_controlled_real_acquisition_executor",
        None,
    )

    assert callable(build_executor), (
        "controlled real acquisition executor builder missing"
    )

    assert getattr(module, "READ_ONLY", None) is True
    assert getattr(module, "ONE_SHOT_COMPATIBLE", None) is True

    for flag in (
        "ALLOW_NORMALIZATION",
        "ALLOW_COMPATIBILITY_ESTABLISHMENT",
        "ALLOW_PROVIDER_SWITCH",
        "ALLOW_CORE_INPUT",
        "ALLOW_SCORE",
        "ALLOW_DECISION",
        "ALLOW_SUPABASE_WRITE",
        "ALLOW_PRODUCTION_WRITE",
    ):
        assert getattr(module, flag, None) is False

    fake_acquisition = FakeAcquisition()

    executor = build_executor(
        acquisition=fake_acquisition,
        env={"FINMIND_API_TOKEN": "TEST_RUNTIME_SECRET_ONLY"},
        session_factory="FAKE_SESSION_FACTORY",
        url="https://api.finmindtrade.com/api/v4/data",
        timeout=10,
        params={
            "dataset": "TaiwanStockPrice",
            "data_id": "2330",
            "start_date": "2026-09-23",
            "end_date": "2026-09-23",
        },
        stock_id="2330",
        trading_date="2026-09-23",
    )

    assert callable(executor)
    assert len(fake_acquisition.calls) == 0

    result = executor()

    assert len(fake_acquisition.calls) == 1

    assert result.get("allowed") is True
    assert "observed" in result

    call = fake_acquisition.calls[0]

    assert call["stock_id"] == "2330"
    assert call["trading_date"] == "2026-09-23"

    public_text = repr(result)

    assert "TEST_RUNTIME_SECRET_ONLY" not in public_text
    assert "token" not in result
    assert "evidence" not in result
    assert "payload" not in result

    print("[PASS] adapter creation performs no acquisition")
    print("[PASS] executor delegates acquisition exactly once")
    print("[PASS] stock/date boundary preserved")
    print("[PASS] public result excludes secret/raw evidence")
    print("[PASS] compatibility/core/write paths disabled")

    print(
        "=== GATE 28D.2K-2H CONTROLLED REAL "
        "ACQUISITION ADAPTER BOUNDARY RESULT: PASS ==="
    )


if __name__ == "__main__":
    main()
