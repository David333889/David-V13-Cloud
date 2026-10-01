"""
Gate 28D.2K-2X
Controlled Real Session Creation Activation V1.

Narrow activation capability:
- permits exactly one Session creation
- reuses the existing protected real_session_factory
- persists no token or authorization
- performs no HTTP request or Internet crossing
"""

from v14.real_session_factory import (
    MAX_RETRIES,
    ALLOW_TOKEN_PERSISTENCE,
    ALLOW_AUTH_PERSISTENCE,
    build_session_factory,
)
from v14 import controlled_real_execution_authorization_integration as execution_auth


READ_ONLY = True
SESSION_CREATION_ACTIVATION_ONLY = True

ALLOW_SESSION_CREATION = True
MAX_SESSIONS_CREATED = 1

ALLOW_HTTP_REQUEST = False
ALLOW_NETWORK_EXECUTION = False
MAX_REAL_GETS = 0

ALLOW_CORE_INPUT = execution_auth.ALLOW_CORE_INPUT
ALLOW_SCORE = execution_auth.ALLOW_SCORE
ALLOW_DECISION = execution_auth.ALLOW_DECISION
ALLOW_SUPABASE_WRITE = execution_auth.ALLOW_SUPABASE_WRITE
ALLOW_PRODUCTION_WRITE = execution_auth.ALLOW_PRODUCTION_WRITE


def build_controlled_real_session(
    requests_module,
    adapter_class,
):
    """
    Create exactly one configured Session through the existing
    protected session factory.

    No token is accepted here.
    Session creation performs no HTTP request.
    """

    session_factory = build_session_factory(
        requests_module=requests_module,
        adapter_class=adapter_class,
    )

    return session_factory()
