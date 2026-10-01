from importlib import import_module


MODULE_NAME = "v14.controlled_runtime_dependency_activation_boundary"


def main():
    print("=== GATE 28D.2K-2T - CONTROLLED RUNTIME DEPENDENCY ACTIVATION BOUNDARY V1 ===")

    m = import_module(MODULE_NAME)

    assert m.READ_ONLY is True
    assert m.ACTIVATION_BOUNDARY_ONLY is True

    assert m.ALLOW_DIRECT_OS_ENV_READ is False
    assert m.ALLOW_SECRET_VALUE_EXPOSURE is False
    assert m.ALLOW_SESSION_CREATION is False
    assert m.ALLOW_NETWORK_EXECUTION is False

    assert m.REQUIRE_ENVIRONMENT_READER is True
    assert m.REQUIRE_REQUESTS_MODULE is True
    assert m.REQUIRE_ADAPTER_CLASS is True

    assert m.ONE_SHOT_ONLY is True
    assert m.SINGLE_STOCK_ONLY is True
    assert m.SINGLE_TRADING_DATE_ONLY is True
    assert m.MAX_REAL_GETS == 1

    assert m.ALLOW_CORE_INPUT is False
    assert m.ALLOW_SCORE is False
    assert m.ALLOW_DECISION is False
    assert m.ALLOW_SUPABASE_WRITE is False
    assert m.ALLOW_PRODUCTION_WRITE is False

    evidence = m.build_runtime_dependency_activation_evidence()

    assert isinstance(evidence, dict)
    assert evidence["activation_boundary_ready"] is True

    assert evidence["os_environment_read"] is False
    assert evidence["secret_value_exposed"] is False
    assert evidence["session_created"] is False
    assert evidence["network_executed"] is False
    assert evidence["real_gets_executed"] == 0

    assert evidence["target_entry"] == (
        "controlled_runtime_entry_integration"
    )

    print("[PASS] runtime activation boundary fixed")
    print("[PASS] OS environment direct read remains disabled")
    print("[PASS] Session creation and network execution remain disabled")
    print("[PASS] injected runtime dependencies required")
    print("[PASS] single stock/date and one-shot boundaries preserved")
    print("[PASS] core/score/decision/write paths remain disabled")
    print("=== GATE 28D.2K-2T CONTROLLED RUNTIME DEPENDENCY ACTIVATION BOUNDARY RESULT: PASS ===")


if __name__ == "__main__":
    main()
