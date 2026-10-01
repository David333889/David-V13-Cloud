from importlib import import_module


MODULE_NAME = "v14.final_controlled_real_internet_crossing_readiness_audit"


def main():
    print("=== GATE 28D.2K-2Q - FINAL CONTROLLED REAL INTERNET CROSSING READINESS AUDIT V1 ===")

    m = import_module(MODULE_NAME)

    assert m.READ_ONLY is True
    assert m.AUDIT_ONLY is True
    assert m.NO_NETWORK_EXECUTION is True

    assert m.ONE_SHOT_ONLY is True
    assert m.SINGLE_STOCK_ONLY is True
    assert m.SINGLE_TRADING_DATE_ONLY is True
    assert m.MAX_REAL_GETS == 1

    assert m.GET_ONLY is True
    assert m.ALLOW_REDIRECTS is False
    assert m.MAX_RETRIES == 0
    assert m.DEFAULT_TIMEOUT_SECONDS == 10

    assert m.ALLOW_DIRECT_ENV_READ is False
    assert m.ALLOW_SECRET_IN_PUBLIC_RESULT is False
    assert m.ALLOW_NORMALIZATION is False
    assert m.ALLOW_COMPATIBILITY_ESTABLISHMENT is False
    assert m.ALLOW_PROVIDER_SWITCH is False
    assert m.ALLOW_CORE_INPUT is False
    assert m.ALLOW_SCORE is False
    assert m.ALLOW_DECISION is False
    assert m.ALLOW_SUPABASE_WRITE is False
    assert m.ALLOW_PRODUCTION_WRITE is False

    evidence = m.build_readiness_evidence()

    assert isinstance(evidence, dict)
    assert evidence["ready_for_controlled_real_crossing"] is True
    assert evidence["network_executed"] is False
    assert evidence["real_gets_executed"] == 0
    assert evidence["secret_exposed"] is False

    print("[PASS] readiness audit is read-only and audit-only")
    print("[PASS] single stock/date and one-shot boundary fixed")
    print("[PASS] GET/redirect/retry/timeout boundary fixed")
    print("[PASS] secret/core/score/decision/write paths disabled")
    print("[PASS] readiness evidence produced without network execution")
    print("=== GATE 28D.2K-2Q FINAL CONTROLLED REAL INTERNET CROSSING READINESS AUDIT RESULT: PASS ===")


if __name__ == "__main__":
    main()
