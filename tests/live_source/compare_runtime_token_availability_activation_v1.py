from importlib import import_module


MODULE_NAME = "v14.runtime_token_availability_activation"


def main():
    print("=== GATE 28D.2K-2U - RUNTIME TOKEN AVAILABILITY ACTIVATION V1 ===")

    m = import_module(MODULE_NAME)

    assert m.READ_ONLY is True
    assert m.TOKEN_AVAILABILITY_ONLY is True

    assert m.ALLOW_OS_ENV_READ is True
    assert m.ALLOW_SECRET_VALUE_EXPOSURE is False
    assert m.ALLOW_SESSION_CREATION is False
    assert m.ALLOW_NETWORK_EXECUTION is False

    assert m.TOKEN_ENV_NAME == "FINMIND_API_TOKEN"

    assert m.ONE_SHOT_ONLY is True
    assert m.SINGLE_STOCK_ONLY is True
    assert m.SINGLE_TRADING_DATE_ONLY is True
    assert m.MAX_REAL_GETS == 1

    assert m.ALLOW_CORE_INPUT is False
    assert m.ALLOW_SCORE is False
    assert m.ALLOW_DECISION is False
    assert m.ALLOW_SUPABASE_WRITE is False
    assert m.ALLOW_PRODUCTION_WRITE is False

    assert callable(m.check_runtime_token_availability)

    print("[PASS] OS environment read capability isolated")
    print("[PASS] token availability only")
    print("[PASS] secret value exposure disabled")
    print("[PASS] Session/network execution disabled")
    print("[PASS] one-shot safety boundaries preserved")
    print("[PASS] core/score/decision/write paths disabled")
    print("=== GATE 28D.2K-2U RUNTIME TOKEN AVAILABILITY ACTIVATION RESULT: PASS ===")


if __name__ == "__main__":
    main()
