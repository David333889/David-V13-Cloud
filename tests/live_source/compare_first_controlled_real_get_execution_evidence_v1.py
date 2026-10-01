from importlib import import_module


MODULE_NAME = "v14.first_controlled_real_get_execution_evidence"


def main():
    print("=== GATE 28D.2K-3C - FIRST CONTROLLED REAL GET EXECUTION EVIDENCE V1 ===")

    m = import_module(MODULE_NAME)

    assert m.READ_ONLY is True
    assert m.EXECUTION_EVIDENCE_ONLY is True
    assert m.NO_NETWORK_REPLAY is True

    assert m.BASE_COMMIT == "705c2b533a448ab048a23ea86dcd14c74ba4b542"

    assert m.PROVIDER == "FINMIND"
    assert m.DATASET == "TaiwanStockPrice"
    assert m.STOCK_ID == "2330"
    assert m.TRADING_DATE == "2026-09-30"

    assert m.EXECUTION_RETURNED is True
    assert m.RESULT_TYPE == "dict"
    assert m.ALLOWED is True

    assert m.EVIDENCE_KEYS == (
        "content_type",
        "payload",
        "size_bytes",
        "status_code",
    )

    assert m.REAL_GETS_OBSERVED == 1
    assert m.SECOND_EXECUTION_ATTEMPTED is False
    assert m.SECRET_VALUE_EXPOSED is False

    assert m.CORE_INPUT_EXECUTED is False
    assert m.DECISION_EXECUTED is False
    assert m.SUPABASE_WRITE_EXECUTED is False
    assert m.PRODUCTION_WRITE_EXECUTED is False

    assert m.POST_CROSSING_WORKTREE_CLEAN is True
    assert m.POST_CROSSING_LOCAL_REMOTE_MATCH is True

    assert m.HTTP_STATUS_OBSERVED is None
    assert m.PAYLOAD_ROW_COUNT_OBSERVED is None

    assert m.ALLOW_NETWORK_EXECUTION is False
    assert m.ALLOW_REAL_GET_EXECUTION is False

    evidence = m.build_first_controlled_real_get_execution_evidence()

    assert isinstance(evidence, dict)
    assert evidence["evidence_record_ready"] is True
    assert evidence["network_replayed"] is False
    assert evidence["additional_real_gets_executed"] == 0

    print("[PASS] first real GET observed facts recorded")
    print("[PASS] evidence keys recorded without payload replay")
    print("[PASS] second execution not attempted")
    print("[PASS] secret/core/decision/write boundaries preserved")
    print("[PASS] post-crossing repository remained clean")
    print("[PASS] unobserved status/payload details remain unknown")
    print("[PASS] no network replay permitted")
    print("=== GATE 28D.2K-3C FIRST CONTROLLED REAL GET EXECUTION EVIDENCE RESULT: PASS ===")


if __name__ == "__main__":
    main()
