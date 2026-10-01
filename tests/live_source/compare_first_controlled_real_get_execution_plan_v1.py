from importlib import import_module


MODULE_NAME = "v14.first_controlled_real_get_execution_plan"


def main():
    print("=== GATE 28D.2K-3A - FIRST CONTROLLED REAL GET EXECUTION PLAN V1 ===")

    m = import_module(MODULE_NAME)

    assert m.READ_ONLY is True
    assert m.EXECUTION_PLAN_ONLY is True
    assert m.GO_NO_GO_CONTRACT_ONLY is True

    assert m.PROVIDER == "FINMIND"
    assert m.DATASET == "TaiwanStockPrice"
    assert m.STOCK_ID == "2330"
    assert m.TRADING_DATE == "2026-09-30"

    assert m.GET_ONLY is True
    assert m.MAX_REAL_GETS == 1
    assert m.DEFAULT_TIMEOUT_SECONDS == 10
    assert m.MAX_RETRIES == 0
    assert m.ALLOW_REDIRECTS is False

    assert m.REQUIRE_TOKEN_AVAILABLE is True
    assert m.ALLOW_SECRET_VALUE_EXPOSURE is False

    assert m.ALLOW_NETWORK_EXECUTION is False
    assert m.ALLOW_REAL_GET_EXECUTION is False

    assert m.ALLOW_CORE_INPUT is False
    assert m.ALLOW_SCORE is False
    assert m.ALLOW_DECISION is False
    assert m.ALLOW_SUPABASE_WRITE is False
    assert m.ALLOW_PRODUCTION_WRITE is False

    evidence = m.build_first_real_get_execution_plan_evidence()

    assert isinstance(evidence, dict)
    assert evidence["go_no_go_contract_ready"] is True
    assert evidence["network_executed"] is False
    assert evidence["real_gets_executed"] == 0
    assert evidence["secret_value_exposed"] is False

    print("[PASS] first real sample fixed to one stock/date")
    print("[PASS] GET/timeout/retry/redirect boundaries fixed")
    print("[PASS] token availability required without secret exposure")
    print("[PASS] execution remains disabled at planning gate")
    print("[PASS] core/score/decision/write paths remain disabled")
    print("=== GATE 28D.2K-3A FIRST CONTROLLED REAL GET EXECUTION PLAN RESULT: PASS ===")


if __name__ == "__main__":
    main()
