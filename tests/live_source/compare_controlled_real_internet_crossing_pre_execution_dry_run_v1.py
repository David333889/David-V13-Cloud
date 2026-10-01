from importlib import import_module


MODULE_NAME = "v14.controlled_real_internet_crossing_pre_execution_dry_run"


def main():
    print("=== GATE 28D.2K-2S - CONTROLLED REAL INTERNET CROSSING PRE-EXECUTION DRY-RUN CONTRACT V1 ===")

    m = import_module(MODULE_NAME)

    assert m.READ_ONLY is True
    assert m.DRY_RUN_ONLY is True
    assert m.NO_ENVIRONMENT_READ is True
    assert m.NO_SECRET_VALUE_READ is True
    assert m.NO_SESSION_CREATION is True
    assert m.NO_NETWORK_EXECUTION is True

    assert m.ONE_SHOT_ONLY is True
    assert m.SINGLE_STOCK_ONLY is True
    assert m.SINGLE_TRADING_DATE_ONLY is True
    assert m.MAX_REAL_GETS == 1

    assert m.GET_ONLY is True
    assert m.ALLOW_REDIRECTS is False
    assert m.MAX_RETRIES == 0
    assert m.DEFAULT_TIMEOUT_SECONDS == 10

    assert m.SECRET_METADATA_ONLY is True
    assert m.ALLOW_SECRET_IN_EVIDENCE is False
    assert m.ALLOW_SECRET_IN_ERROR is False

    assert m.EXECUTION_REAL_GET_AUTHORIZED is True
    assert m.PREFLIGHT_READY is True
    assert m.PREFLIGHT_NETWORK_EXECUTED is False
    assert m.PREFLIGHT_LIVE_GET_DISABLED is True

    assert m.ALLOW_CORE_INPUT is False
    assert m.ALLOW_SCORE is False
    assert m.ALLOW_DECISION is False
    assert m.ALLOW_SUPABASE_WRITE is False
    assert m.ALLOW_PRODUCTION_WRITE is False

    evidence = m.build_pre_execution_dry_run_evidence()

    assert isinstance(evidence, dict)
    assert evidence["ready_for_pre_execution"] is True

    assert evidence["environment_read"] is False
    assert evidence["secret_value_read"] is False
    assert evidence["session_created"] is False
    assert evidence["network_executed"] is False
    assert evidence["real_gets_executed"] == 0

    assert "secret" not in evidence
    assert "token" not in evidence

    print("[PASS] dry-run performs no environment or secret-value read")
    print("[PASS] dry-run performs no Session creation or network execution")
    print("[PASS] single stock/date and one-shot boundaries fixed")
    print("[PASS] GET/redirect/retry/timeout boundaries fixed")
    print("[PASS] execution authorization and preflight evidence fixed")
    print("[PASS] secret/core/score/decision/write paths remain protected")
    print("=== GATE 28D.2K-2S CONTROLLED REAL INTERNET CROSSING PRE-EXECUTION DRY-RUN CONTRACT RESULT: PASS ===")


if __name__ == "__main__":
    main()
