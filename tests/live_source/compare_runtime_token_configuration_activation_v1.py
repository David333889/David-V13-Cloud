from importlib import import_module


MODULE_NAME = "v14.runtime_token_configuration_activation"


def main():
    print("=== GATE 28D.2K-2W - RUNTIME TOKEN CONFIGURATION ACTIVATION V1 ===")

    m = import_module(MODULE_NAME)

    assert m.READ_ONLY is True
    assert m.CONFIGURATION_ACTIVATION_ONLY is True

    assert m.TOKEN_ENV_NAME == "FINMIND_API_TOKEN"

    assert m.REQUIRE_PROCESS_ENVIRONMENT is True
    assert m.ALLOW_SECRET_VALUE_EXPOSURE is False
    assert m.ALLOW_SECRET_LOGGING is False
    assert m.ALLOW_SECRET_PERSISTENCE is False

    assert m.ALLOW_SESSION_CREATION is False
    assert m.ALLOW_NETWORK_EXECUTION is False

    assert m.ALLOW_CORE_INPUT is False
    assert m.ALLOW_SCORE is False
    assert m.ALLOW_DECISION is False
    assert m.ALLOW_SUPABASE_WRITE is False
    assert m.ALLOW_PRODUCTION_WRITE is False

    evidence = m.build_runtime_token_activation_evidence()

    assert isinstance(evidence, dict)
    assert evidence["activation_contract_ready"] is True

    assert evidence["secret_value_exposed"] is False
    assert evidence["secret_persisted"] is False
    assert evidence["session_created"] is False
    assert evidence["network_executed"] is False
    assert evidence["real_gets_executed"] == 0

    print("[PASS] process-environment token activation path fixed")
    print("[PASS] secret exposure/logging/persistence disabled")
    print("[PASS] Session/network execution remains disabled")
    print("[PASS] core/score/decision/write paths remain disabled")
    print("=== GATE 28D.2K-2W RUNTIME TOKEN CONFIGURATION ACTIVATION RESULT: PASS ===")


if __name__ == "__main__":
    main()
