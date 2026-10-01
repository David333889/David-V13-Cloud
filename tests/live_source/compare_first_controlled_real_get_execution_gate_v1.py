from importlib import import_module


MODULE_NAME = "v14.first_controlled_real_get_execution_gate"


def main():
    print("=== GATE 28D.2K-3B - FIRST CONTROLLED REAL GET EXECUTION GATE V1 ===")

    m = import_module(MODULE_NAME)

    assert m.READ_ONLY is True
    assert m.EXECUTION_GATE_ONLY is True

    assert m.STOCK_ID == "2330"
    assert m.TRADING_DATE == "2026-09-30"
    assert m.DATASET == "TaiwanStockPrice"

    assert m.UNIQUE_RUNTIME_ENTRY is True
    assert m.PROCESS_ENVIRONMENT_SOURCE is True
    assert m.MINIMAL_TOKEN_MAPPING_ONLY is True

    assert m.ONE_SHOT_ONLY is True
    assert m.MAX_REAL_GETS == 1
    assert m.SECOND_EXECUTION_DENIED is True

    assert m.REQUIRE_TOKEN_AVAILABLE is True
    assert m.ALLOW_SECRET_VALUE_EXPOSURE is False

    assert m.ALLOW_NETWORK_EXECUTION is False
    assert m.ALLOW_REAL_GET_EXECUTION is False

    assert m.ALLOW_CORE_INPUT is False
    assert m.ALLOW_SCORE is False
    assert m.ALLOW_DECISION is False
    assert m.ALLOW_SUPABASE_WRITE is False
    assert m.ALLOW_PRODUCTION_WRITE is False

    evidence = m.build_first_real_get_execution_gate_evidence()

    assert isinstance(evidence, dict)
    assert evidence["execution_gate_ready"] is True
    assert evidence["network_executed"] is False
    assert evidence["real_gets_executed"] == 0
    assert evidence["secret_value_exposed"] is False

    print("[PASS] unique runtime entry fixed")
    print("[PASS] process environment / minimal token mapping fixed")
    print("[PASS] first real sample fixed to one stock/date")
    print("[PASS] exactly-one execution boundary fixed")
    print("[PASS] second execution denial required")
    print("[PASS] real execution remains disabled at gate contract")
    print("[PASS] core/score/decision/write paths remain disabled")
    print("=== GATE 28D.2K-3B FIRST CONTROLLED REAL GET EXECUTION GATE RESULT: PASS ===")


if __name__ == "__main__":
    main()
