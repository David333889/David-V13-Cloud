import requests
from requests.adapters import HTTPAdapter


# Gate 28D.0 real-session factory contract.
# Session creation is allowed; network execution is not.
MAX_RETRIES = 0

ALLOW_AUTH_PERSISTENCE = False
ALLOW_TOKEN_PERSISTENCE = False
ALLOW_NETWORK_ON_CREATE = False

ALLOW_CORE_INPUT = False
ALLOW_SUPABASE_WRITE = False
ALLOW_PRODUCTION_WRITE = False


def build_session_factory(
    requests_module=requests,
    adapter_class=HTTPAdapter,
):
    """
    Build a callable that creates a configured requests Session.

    Creating the Session performs no network request.
    No token or authorization data is persisted here.
    """

    if requests_module is None:
        raise ValueError("requests module is required")

    if adapter_class is None:
        raise ValueError("adapter class is required")

    def session_factory():
        session = requests_module.Session()

        adapter = adapter_class(
            max_retries=MAX_RETRIES,
        )

        session.mount(
            "https://",
            adapter,
        )

        session.mount(
            "http://",
            adapter,
        )

        return session

    return session_factory
