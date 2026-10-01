"""
Gate 28D.2K-2U
Runtime Token Availability Activation V1.

Narrow runtime capability:
- may read exactly one named OS environment variable
- exposes availability metadata only
- never exposes the secret value
- creates no Session
- executes no HTTP request
"""

import os

from v14 import controlled_real_execution_authorization_integration as execution_auth
from v14.secret_runtime import (
    DEFAULT_TOKEN_ENV_NAME,
    build_secret_metadata,
    load_runtime_secret,
)


READ_ONLY = True
TOKEN_AVAILABILITY_ONLY = True

ALLOW_OS_ENV_READ = True
ALLOW_SECRET_VALUE_EXPOSURE = False
ALLOW_SESSION_CREATION = False
ALLOW_NETWORK_EXECUTION = False

TOKEN_ENV_NAME = DEFAULT_TOKEN_ENV_NAME

ONE_SHOT_ONLY = execution_auth.ONE_SHOT_ONLY
SINGLE_STOCK_ONLY = execution_auth.SINGLE_STOCK_ONLY
SINGLE_TRADING_DATE_ONLY = execution_auth.SINGLE_TRADING_DATE_ONLY
MAX_REAL_GETS = execution_auth.MAX_REAL_GETS

ALLOW_CORE_INPUT = execution_auth.ALLOW_CORE_INPUT
ALLOW_SCORE = execution_auth.ALLOW_SCORE
ALLOW_DECISION = execution_auth.ALLOW_DECISION
ALLOW_SUPABASE_WRITE = execution_auth.ALLOW_SUPABASE_WRITE
ALLOW_PRODUCTION_WRITE = execution_auth.ALLOW_PRODUCTION_WRITE


def check_runtime_token_availability():
    """
    Read only FINMIND_API_TOKEN from the OS environment.

    Return public-safe availability metadata only.
    The token value must never leave this function.
    """

    value = os.environ.get(TOKEN_ENV_NAME)

    env = {}

    if value is not None:
        env[TOKEN_ENV_NAME] = value

    loaded = load_runtime_secret(
        env=env,
        name=TOKEN_ENV_NAME,
    )

    return build_secret_metadata(
        loaded,
        name=TOKEN_ENV_NAME,
    )
