from urllib.parse import parse_qsl, urlsplit


# Gate 28B.1 request-safety contract.
# Policy only: this module performs no network request.
HTTPS_ONLY = True
ALLOW_REDIRECTS = False
MAX_TIMEOUT_SECONDS = 30
MAX_RESPONSE_BYTES = 5_000_000
MAX_RETRIES = 0


_SECRET_QUERY_KEYS = {
    "token",
    "apikey",
    "api_key",
    "access_token",
    "authorization",
}


def _deny(reason):
    return {
        "allowed": False,
        "reason": reason,
    }


def validate_request(
    url,
    allowed_hosts,
    timeout,
):
    """
    Validate a prospective external request before any transport runs.
    """

    if not isinstance(url, str) or not url:
        return _deny("INVALID_URL")

    try:
        parsed = urlsplit(url)
    except (TypeError, ValueError):
        return _deny("INVALID_URL")

    if HTTPS_ONLY and parsed.scheme.lower() != "https":
        return _deny("HTTPS_REQUIRED")

    host = parsed.hostname

    if not host:
        return _deny("INVALID_URL")

    if not allowed_hosts:
        return _deny("HOST_ALLOWLIST_REQUIRED")

    normalized_hosts = {
        str(item).lower()
        for item in allowed_hosts
        if item
    }

    if host.lower() not in normalized_hosts:
        return _deny("HOST_NOT_ALLOWED")

    if not isinstance(timeout, (int, float)):
        return _deny("TIMEOUT_OUT_OF_RANGE")

    if timeout <= 0 or timeout > MAX_TIMEOUT_SECONDS:
        return _deny("TIMEOUT_OUT_OF_RANGE")

    try:
        query_items = parse_qsl(
            parsed.query,
            keep_blank_values=True,
        )
    except ValueError:
        return _deny("INVALID_URL")

    for key, _value in query_items:
        if key.lower() in _SECRET_QUERY_KEYS:
            return _deny("SECRET_IN_URL")

    return {
        "allowed": True,
        "reason": "OK",
    }


def validate_response_size(size_bytes):
    """
    Validate response size before downstream processing.
    """

    if not isinstance(size_bytes, int):
        return _deny("INVALID_RESPONSE_SIZE")

    if size_bytes < 0:
        return _deny("INVALID_RESPONSE_SIZE")

    if size_bytes > MAX_RESPONSE_BYTES:
        return _deny("RESPONSE_TOO_LARGE")

    return {
        "allowed": True,
        "reason": "OK",
    }
