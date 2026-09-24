from v14.live_fetch_safety import sanitize_secret


# Gate 28B.3 read-only transport contract.
# Backend must be injected. No real network backend is created here.
GET_ONLY = True
ALLOW_REDIRECTS = False
MAX_RETRIES = 0
ALLOW_LIVE_NETWORK = False


class ReadOnlyTransport:
    """
    Read-only transport wrapper around an injected backend.
    """

    def __init__(
        self,
        backend,
        max_response_bytes,
    ):
        self.backend = backend
        self.max_response_bytes = max_response_bytes

    def get(
        self,
        url,
        headers=None,
        timeout=None,
        params=None,
    ):
        if self.backend is None:
            return {
                "connection_error": True,
                "error": "backend is required",
            }

        if not isinstance(
            self.max_response_bytes,
            int,
        ):
            return {
                "connection_error": True,
                "error": "valid max response size is required",
            }

        if self.max_response_bytes <= 0:
            return {
                "connection_error": True,
                "error": "valid max response size is required",
            }

        try:
            response = self.backend.get(
                url,
                headers=headers,
                timeout=timeout,
                params=params,
                allow_redirects=ALLOW_REDIRECTS,
                max_bytes=self.max_response_bytes,
            )
        except Exception as exc:
            return {
                "connection_error": True,
                "error": sanitize_secret(str(exc)),
            }

        if not isinstance(response, dict):
            return {
                "connection_error": True,
                "error": "invalid backend response",
            }

        size_bytes = response.get("size_bytes")

        if not isinstance(size_bytes, int):
            return {
                "connection_error": True,
                "error": "response size evidence required",
            }

        if size_bytes < 0:
            return {
                "connection_error": True,
                "error": "invalid response size evidence",
            }

        if size_bytes > self.max_response_bytes:
            return {
                "response_too_large": True,
                "size_bytes": size_bytes,
            }

        evidence = {
            "status_code": response.get("status_code"),
            "content_type": response.get("content_type"),
            "payload": response.get("payload"),
        }

        return evidence
