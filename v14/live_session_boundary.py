from urllib.parse import urlsplit


# Gate 28C.2 live-session boundary.
# Session creation is permitted only through an injected factory.
FINMIND_HOST = "api.finmindtrade.com"

GET_ONLY = True
ALLOW_REDIRECTS = False
MAX_RETRIES = 0
MAX_TIMEOUT_SECONDS = 30

ALLOW_CORE_INPUT = False
ALLOW_SUPABASE_WRITE = False
ALLOW_PRODUCTION_WRITE = False


def _deny(reason):
    return {
        "allowed": False,
        "reason": reason,
    }


def create_live_session(
    session_factory,
):
    """
    Create a session only through an injected factory.

    This module does not import requests or create a network
    session by itself.
    """

    if session_factory is None:
        return _deny("SESSION_FACTORY_REQUIRED")

    if not callable(session_factory):
        return _deny("SESSION_FACTORY_INVALID")

    try:
        session = session_factory()
    except Exception:
        return _deny("SESSION_FACTORY_FAILURE")

    if session is None:
        return _deny("SESSION_CREATION_FAILED")

    get_method = getattr(
        session,
        "get",
        None,
    )

    if not callable(get_method):
        return _deny("SESSION_GET_REQUIRED")

    return {
        "allowed": True,
        "reason": "OK",
        "session": session,
    }


def validate_live_target(
    url,
    timeout,
):
    """
    Validate the only permitted live target before network use.
    """

    if not isinstance(url, str) or not url:
        return _deny("INVALID_URL")

    try:
        parsed = urlsplit(url)
    except (TypeError, ValueError):
        return _deny("INVALID_URL")

    if parsed.scheme.lower() != "https":
        return _deny("HTTPS_REQUIRED")

    host = parsed.hostname

    if not host:
        return _deny("INVALID_URL")

    if host.lower() != FINMIND_HOST:
        return _deny("HOST_NOT_ALLOWED")

    if not isinstance(timeout, (int, float)):
        return _deny("TIMEOUT_OUT_OF_RANGE")

    if timeout <= 0 or timeout > MAX_TIMEOUT_SECONDS:
        return _deny("TIMEOUT_OUT_OF_RANGE")

    return {
        "allowed": True,
        "reason": "OK",
    }
