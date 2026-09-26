from v14.live_fetch_safety import sanitize_secret


# Gate 28C.1 FinMind live-backend contract.
# A session must be injected by the caller.
# This module does not create a network session by itself.
BASE_URL = "https://api.finmindtrade.com/api/v4/data"

GET_ONLY = True
ALLOW_REDIRECTS = False
MAX_RETRIES = 0

ALLOW_CORE_INPUT = False
ALLOW_SUPABASE_WRITE = False
ALLOW_PRODUCTION_WRITE = False


class FinMindReadOnlyBackend:
    """
    FinMind read-only backend around an injected session.
    """

    def __init__(
        self,
        session,
    ):
        self.session = session

    def get(
        self,
        url,
        headers=None,
        timeout=None,
        params=None,
        allow_redirects=False,
        max_bytes=5_000_000,
    ):
        if self.session is None:
            return {
                "connection_error": True,
                "error": "session is required",
            }

        if url != BASE_URL:
            return {
                "connection_error": True,
                "error": "FinMind endpoint not allowed",
            }

        if allow_redirects is not False:
            return {
                "connection_error": True,
                "error": "redirects are not allowed",
            }

        if not isinstance(max_bytes, int):
            return {
                "connection_error": True,
                "error": "valid max response size is required",
            }

        if max_bytes <= 0:
            return {
                "connection_error": True,
                "error": "valid max response size is required",
            }

        try:
            response = self.session.get(
                url,
                headers=headers,
                timeout=timeout,
                params=params,
                allow_redirects=False,
            )
        except Exception as exc:
            return {
                "connection_error": True,
                "error": sanitize_secret(str(exc)),
            }

        content = getattr(
            response,
            "content",
            b"",
        )

        if not isinstance(
            content,
            (bytes, bytearray),
        ):
            return {
                "connection_error": True,
                "error": "invalid response content",
            }

        size_bytes = len(content)

        if size_bytes > max_bytes:
            return {
                "response_too_large": True,
                "size_bytes": size_bytes,
            }

        headers_map = getattr(
            response,
            "headers",
            {},
        )


        content_type = headers_map.get(
            "Content-Type",
            "",
        )

        try:
            payload = response.json()
        except Exception as exc:
            return {
                "status_code": getattr(
                    response,
                    "status_code",
                    None,
                ),
                "content_type": content_type,
                "payload_error": sanitize_secret(
                    str(exc)
                ),
                "size_bytes": size_bytes,
            }

        return {
            "status_code": getattr(
                response,
                "status_code",
                None,
            ),
            "content_type": content_type,
            "payload": payload,
            "size_bytes": size_bytes,
        }
