# Gate 28D.2K-2I - Controlled Real Acquisition Wiring V1.
#
# Expected RED contract test.
#
# This test requires a future thin wiring layer that composes:
#   2F one-shot guard
#   2G one-shot integration
#   2H acquisition adapter
#
# No real Session, token, HTTP request, or Internet crossing
# is permitted by this test.

from v14.controlled_real_acquisition_wiring import (
    build_controlled_real_acquisition_wiring,
)


def main():
    print(
        "=== GATE 28D.2K-2I - CONTROLLED REAL "
        "ACQUISITION WIRING V1 ==="
    )

    calls = {
        "acquisition": 0,
    }

    def fake_acquisition(**kwargs):
        calls["acquisition"] += 1
        return {
            "ok": True,
            "source": "FAKE_ACQUISITION",
        }

    execute_once = build_controlled_real_acquisition_wiring(
        acquisition=fake_acquisition,
        env={},
        session_factory=lambda: None,
        url="https://example.invalid",
        timeout=1,
        params={},
        stock_id="2330",
        trading_date="2026-09-29",
    )

    assert callable(execute_once)
    assert calls["acquisition"] == 0

    first = execute_once()

    assert first["ok"] is True
    assert calls["acquisition"] == 1

    second = execute_once()

    assert second["allowed"] is False
    assert second["reason"] == "REAL_GET_LIMIT_REACHED"
    assert calls["acquisition"] == 1

    print("[PASS] wiring build performs no acquisition")
    print("[PASS] first execution reaches injected acquisition once")
    print("[PASS] second execution denied before acquisition")
    print("[PASS] fake acquisition only; no real Internet crossing")

    print(
        "=== GATE 28D.2K-2I CONTROLLED REAL "
        "ACQUISITION WIRING RESULT: PASS ==="
    )


if __name__ == "__main__":
    main()
