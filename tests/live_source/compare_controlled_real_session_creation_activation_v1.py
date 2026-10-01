from importlib import import_module


MODULE_NAME = "v14.controlled_real_session_creation_activation"


def main():
    print("=== GATE 28D.2K-2X - CONTROLLED REAL SESSION CREATION ACTIVATION V1 ===")

    m = import_module(MODULE_NAME)

    assert m.READ_ONLY is True
    assert m.SESSION_CREATION_ACTIVATION_ONLY is True

    assert m.ALLOW_SESSION_CREATION is True
    assert m.MAX_SESSIONS_CREATED == 1

    assert m.MAX_RETRIES == 0
    assert m.ALLOW_TOKEN_PERSISTENCE is False
    assert m.ALLOW_AUTH_PERSISTENCE is False

    assert m.ALLOW_HTTP_REQUEST is False
    assert m.ALLOW_NETWORK_EXECUTION is False
    assert m.MAX_REAL_GETS == 0

    assert m.ALLOW_CORE_INPUT is False
    assert m.ALLOW_SCORE is False
    assert m.ALLOW_DECISION is False
    assert m.ALLOW_SUPABASE_WRITE is False
    assert m.ALLOW_PRODUCTION_WRITE is False

    assert callable(m.build_controlled_real_session)

    print("[PASS] exactly-one Session creation capability isolated")
    print("[PASS] retry policy remains zero")
    print("[PASS] token/auth persistence disabled")
    print("[PASS] HTTP/GET/network execution disabled")
    print("[PASS] core/score/decision/write paths disabled")
    print("=== GATE 28D.2K-2X CONTROLLED REAL SESSION CREATION ACTIVATION RESULT: PASS ===")


if __name__ == "__main__":
    main()
