from importlib import import_module


MODULE_NAME = "v14.real_internet_crossing_unique_execution_chain_final_audit"


def main():
    print("=== GATE 28D.2K-2Z - REAL INTERNET CROSSING UNIQUE EXECUTION CHAIN FINAL AUDIT V1 ===")

    m = import_module(MODULE_NAME)

    assert m.READ_ONLY is True
    assert m.FINAL_AUDIT_ONLY is True

    assert m.UNIQUE_RUNTIME_ENTRY is True
    assert m.UNIQUE_SESSION_FACTORY_PATH is True
    assert m.UNIQUE_ONE_SHOT_GUARD_PATH is True
    assert m.UNIQUE_CONTROLLED_FETCH_PATH is True
    assert m.UNIQUE_REAL_GET_BACKEND_PATH is True

    assert m.GET_ONLY is True
    assert m.ONE_SHOT_ONLY is True
    assert m.SINGLE_STOCK_ONLY is True
    assert m.SINGLE_TRADING_DATE_ONLY is True
    assert m.MAX_REAL_GETS == 1

    assert m.TOKEN_TRANSPORT_BOUNDARY_ONLY is True
    assert m.ALLOW_SECRET_VALUE_EXPOSURE is False

    assert m.ALLOW_NETWORK_EXECUTION is False
    assert m.ALLOW_CORE_INPUT is False
    assert m.ALLOW_SCORE is False
    assert m.ALLOW_DECISION is False
    assert m.ALLOW_SUPABASE_WRITE is False
    assert m.ALLOW_PRODUCTION_WRITE is False

    evidence = m.build_unique_execution_chain_final_audit_evidence()

    assert isinstance(evidence, dict)
    assert evidence["final_audit_ready"] is True
    assert evidence["network_executed"] is False
    assert evidence["real_gets_executed"] == 0
    assert evidence["secret_value_exposed"] is False

    print("[PASS] unique runtime-to-fetch execution chain fixed")
    print("[PASS] unique Session factory and one-shot guard paths fixed")
    print("[PASS] unique controlled-fetch/backend GET path fixed")
    print("[PASS] token remains transport-boundary only")
    print("[PASS] one-shot stock/date/GET boundaries preserved")
    print("[PASS] network/core/score/decision/write execution remains disabled")
    print("=== GATE 28D.2K-2Z REAL INTERNET CROSSING UNIQUE EXECUTION CHAIN FINAL AUDIT RESULT: PASS ===")


if __name__ == "__main__":
    main()
