from importlib import import_module


MODULE_NAME = "v14.runtime_token_safe_configuration_boundary"


def main():
    print("=== GATE 28D.2K-2V - RUNTIME TOKEN SAFE CONFIGURATION BOUNDARY V1 ===")

    m = import_module(MODULE_NAME)

    assert m.READ_ONLY is True
    assert m.CONFIGURATION_BOUNDARY_ONLY is True

    assert m.TOKEN_ENV_NAME == "FINMIND_API_TOKEN"

    assert m.ALLOW_PROCESS_ENVIRONMENT is True
    assert m.ALLOW_ENV_FILE_STORAGE is False
    assert m.ALLOW_SOURCE_CODE_SECRET is False
    assert m.ALLOW_JSON_SECRET_STORAGE is False
    assert m.ALLOW_TEST_SECRET_STORAGE is False
    assert m.ALLOW_SECRET_LOGGING is False
    assert m.ALLOW_SECRET_IN_PUBLIC_RESULT is False

    assert m.REQUIRE_ENV_FILE_GITIGNORE is True
    assert m.REQUIRE_STREAMLIT_SECRET_GITIGNORE is True

    assert m.ALLOW_SESSION_CREATION is False
    assert m.ALLOW_NETWORK_EXECUTION is False

    assert m.ALLOW_CORE_INPUT is False
    assert m.ALLOW_SCORE is False
    assert m.ALLOW_DECISION is False
    assert m.ALLOW_SUPABASE_WRITE is False
    assert m.ALLOW_PRODUCTION_WRITE is False

    evidence = m.build_runtime_token_configuration_evidence()

    assert isinstance(evidence, dict)
    assert evidence["configuration_boundary_ready"] is True
    assert evidence["secret_configured"] is False
    assert evidence["secret_value_read"] is False
    assert evidence["session_created"] is False
    assert evidence["network_executed"] is False
    assert evidence["real_gets_executed"] == 0

    print("[PASS] process-environment configuration path fixed")
    print("[PASS] file/source/test secret storage disabled")
    print("[PASS] secret logging/public exposure disabled")
    print("[PASS] gitignore secret-file protections required")
    print("[PASS] Session/network execution remains disabled")
    print("[PASS] core/score/decision/write paths remain disabled")
    print("=== GATE 28D.2K-2V RUNTIME TOKEN SAFE CONFIGURATION BOUNDARY RESULT: PASS ===")


if __name__ == "__main__":
    main()
