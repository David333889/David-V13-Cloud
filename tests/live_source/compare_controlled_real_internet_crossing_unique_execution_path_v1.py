from importlib import import_module


MODULE_NAME = "v14.controlled_real_internet_crossing_unique_execution_path"


def main():
    print("=== GATE 28D.2K-2R - CONTROLLED REAL INTERNET CROSSING UNIQUE EXECUTION PATH CONTRACT V1 ===")

    m = import_module(MODULE_NAME)

    assert m.READ_ONLY is True
    assert m.CONTRACT_ONLY is True
    assert m.NO_NETWORK_EXECUTION is True

    assert m.ONE_SHOT_ONLY is True
    assert m.SINGLE_STOCK_ONLY is True
    assert m.SINGLE_TRADING_DATE_ONLY is True
    assert m.MAX_REAL_GETS == 1

    assert m.PREFLIGHT_LIVE_GET_DISABLED is True
    assert m.EXECUTION_REAL_GET_AUTHORIZED is True

    assert m.ALLOW_DIRECT_HTTP_BYPASS is False
    assert m.ALLOW_DIRECT_SESSION_BYPASS is False
    assert m.ALLOW_AUTHORIZATION_BYPASS is False
    assert m.ALLOW_PREFLIGHT_BYPASS is False
    assert m.ALLOW_REQUEST_VALIDATION_BYPASS is False

    assert m.ALLOW_CORE_INPUT is False
    assert m.ALLOW_SCORE is False
    assert m.ALLOW_DECISION is False
    assert m.ALLOW_SUPABASE_WRITE is False
    assert m.ALLOW_PRODUCTION_WRITE is False

    evidence = m.build_unique_execution_path_evidence()

    assert isinstance(evidence, dict)
    assert evidence["unique_execution_path_ready"] is True
    assert evidence["network_executed"] is False
    assert evidence["real_gets_executed"] == 0

    assert evidence["path"] == (
        "runtime_entry",
        "runtime_environment",
        "session_factory_integration",
        "execution_authorization",
        "preflight",
        "request_validation",
        "protected_fetch",
    )

    print("[PASS] unique protected execution path fixed")
    print("[PASS] execution authorization and preflight remain separated")
    print("[PASS] direct HTTP/session/authorization/preflight bypass disabled")
    print("[PASS] single stock/date and one-shot real GET limit fixed")
    print("[PASS] core/score/decision/write paths remain disabled")
    print("[PASS] contract evidence produced without network execution")
    print("=== GATE 28D.2K-2R CONTROLLED REAL INTERNET CROSSING UNIQUE EXECUTION PATH CONTRACT RESULT: PASS ===")


if __name__ == "__main__":
    main()
