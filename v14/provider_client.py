from v14.live_fetch_safety import (
    classify_fetch_response,
    sanitize_secret,
)


# Gate 28B provider-client skeleton.
# Transport must be injected by the caller.
# This module does NOT create a real network transport.
GET_ONLY = True

ALLOW_LIVE_NETWORK = False
ALLOW_CORE_INPUT = False
ALLOW_SUPABASE_WRITE = False
ALLOW_PRODUCTION_WRITE = False


def fetch_provider_data(
    transport,
    url,
    token,
    timeout,
    params=None,
):
    """
    Fetch provider evidence through an injected transport only.

    Gate 28B does not create or select a real HTTP transport.
    """

    if transport is None:
        return {
            "connection_error": True,
            "error": "transport is required",
        }

    if not isinstance(timeout, (int, float)):
        return {
            "connection_error": True,
            "error": "finite positive timeout is required",
        }

    if timeout <= 0:
        return {
            "connection_error": True,
            "error": "finite positive timeout is required",
        }

    if not isinstance(token, str) or not token:
        return {
            "connection_error": True,
            "error": "token is required",
        }

    headers = {
        "Authorization": f"Bearer {token}",
    }

    try:
        evidence = transport.get(
            url,
            headers=headers,
            timeout=timeout,
            params=params,
        )
    except Exception as exc:
        safe_error = sanitize_secret(str(exc))

        return {
            "connection_error": True,
            "error": safe_error,
        }

    return evidence


def classify_provider_evidence(evidence):
    """
    Reuse Gate 28A classification without deriving core values.
    """

    return classify_fetch_response(evidence)
