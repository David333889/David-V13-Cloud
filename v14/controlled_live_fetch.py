from v14.finmind_live_backend import FinMindReadOnlyBackend
from v14.live_session_boundary import (
    create_live_session,
    validate_live_target,
)
from v14.secret_runtime import (
    DEFAULT_TOKEN_ENV_NAME,
    load_runtime_secret,
)


# Gate 28C.3 controlled-fetch orchestrator.
# This module coordinates already-protected safety boundaries only.
ALLOW_CORE_INPUT = False
ALLOW_SCORE = False
ALLOW_DECISION = False
ALLOW_SUPABASE_WRITE = False
ALLOW_PRODUCTION_WRITE = False


def _deny(reason):
    return {
        "allowed": False,
        "reason": reason,
    }


def execute_controlled_fetch(
    env,
    session_factory,
    url,
    timeout,
    params=None,
    max_bytes=5_000_000,
):
    """
    Execute one controlled read-only fetch through injected boundaries.

    No real session is created here.
    No result is forwarded to Core, score, decision, or persistence.
    """

    # 1. Secret must exist before any session is created.
    secret_result = load_runtime_secret(
        env=env,
        name=DEFAULT_TOKEN_ENV_NAME,
    )

    if secret_result.get("available") is not True:
        return _deny(
            secret_result.get(
                "reason",
                "SECRET_UNAVAILABLE",
            )
        )

    token = secret_result.get("secret")

    # 2. Target must be safe before session creation.
    target_result = validate_live_target(
        url=url,
        timeout=timeout,
    )

    if target_result.get("allowed") is not True:
        return _deny(
            target_result.get(
                "reason",
                "TARGET_REJECTED",
            )
        )

    # 3. Session may only be created through injected factory.
    session_result = create_live_session(
        session_factory=session_factory,
    )

    if session_result.get("allowed") is not True:
        return _deny(
            session_result.get(
                "reason",
                "SESSION_REJECTED",
            )
        )

    session = session_result.get("session")

    # 4. FinMind-specific backend receives the injected session.
    backend = FinMindReadOnlyBackend(
        session=session,
    )

    # 5. Build transport-only query parameters.
    #
    # The runtime secret is appended only at the HTTP transport
    # boundary. It does not enter the validated business params
    # contract or any public evidence.
    transport_params = dict(params or {})
    transport_params["token"] = token

    # 6. Exactly one GET path.
    evidence = backend.get(
        url=url,
        headers={},
        timeout=timeout,
        params=transport_params,
        allow_redirects=False,
        max_bytes=max_bytes,
    )

    # 7. Public result contains evidence only, never token.
    return {
        "allowed": True,
        "evidence": evidence,
    }
