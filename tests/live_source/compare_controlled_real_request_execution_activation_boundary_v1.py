from importlib import import_module


MODULE_NAME = "v14.controlled_real_request_execution_activation_boundary"


def main():
    print("=== GATE 28D.2K-2Y - CONTROLLED REAL REQUEST EXECUTION ACTIVATION BOUNDARY V1 ===")

    m = import_module(MODULE_NAME)

    assert m.READ_ONLY is True
    assert m.REQUEST_EXECUTION_ACTIVATION_BOUNDARY_ONLY is True

    assert m.GET_ONLY is True
    assert m.SINGLE_STOCK_ONLY is True
    assert m.SINGLE_TRADING_DATE_ONLY is True
    assert m.MAX_REAL_GETS == 1

    assert m.DEFAULT_TIMEOUT_SECONDS == 10
    assert m.MAX_RETRIES == 0
    assert m.ALLOW_REDIRECTS is False

    assert m.FINMIND_HOST == "api.finmindtrade.com"
    assert m.FINMIND_BASE_URL == "https://api.finmindtrade.com/api/v4/data"

    assert m.REQUIRE_TOKEN_AVAILABLE is True
    assert m.ALLOW_SECRET_VALUE_EXPOSURE is False

    assert m.ALLOW_NETWORK_EXECUTION is False
    assert m.ALLOW_CORE_INPUT is False
    assert m.ALLOW_SCORE is False
    assert m.ALLOW_DECISION is False
    assert m.ALLOW_SUPABASE_WRITE is False
    assert m.ALLOW_PRODUCTION_WRITE is False

    evidence = m.build_request_execution_activation_evidence()

    assert isinstance(evidence, dict)
    assert evidence["activation_boundary_ready"] is True
    assert evidence["network_executed"] is False
    assert evidence["real_gets_executed"] == 0
    assert evidence["session_created"] is False
    assert evidence["secret_value_exposed"] is False

    print("[PASS] GET-only one-shot request boundary fixed")
    print("[PASS] single stock/date boundary fixed")
    print("[PASS] timeout/retry/redirect boundaries fixed")
    print("[PASS] FinMind host/base URL fixed")
    print("[PASS] token availability required without secret exposure")
    print("[PASS] network/core/score/decision/write execution remains disabled")
    print("=== GATE 28D.2K-2Y CONTROLLED REAL REQUEST EXECUTION ACTIVATION BOUNDARY RESULT: PASS ===")


if __name__ == "__main__":
    main()
