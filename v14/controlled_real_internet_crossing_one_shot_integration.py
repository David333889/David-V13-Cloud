# Gate 28D.2K-2G - Controlled Real Internet
# Crossing One-Shot Integration V1.
#
# Thin authorization integration only.
#
# The injected guard must authorize before the injected
# executor may be called.
#
# This module does not create a Session, read a token,
# or implement an HTTP request itself.

READ_ONLY = True
ONE_SHOT_ONLY = True
MAX_REAL_GETS = 1

ALLOW_NORMALIZATION = False
ALLOW_COMPATIBILITY_ESTABLISHMENT = False
ALLOW_PROVIDER_SWITCH = False
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


def execute_controlled_real_internet_crossing_once(
    guard,
    executor,
):
    """
    Authorize once before calling the injected executor.

    A denied authorization must stop before executor call.
    No network behavior is implemented in this module.
    """

    if guard is None:
        return _deny("GUARD_REQUIRED")

    if not callable(executor):
        return _deny("EXECUTOR_REQUIRED")

    authorize = getattr(
        guard,
        "authorize",
        None,
    )

    if not callable(authorize):
        return _deny("GUARD_INVALID")

    authorization = authorize()

    if authorization.get("allowed") is not True:
        return _deny(
            authorization.get(
                "reason",
                "REAL_GET_NOT_AUTHORIZED",
            )
        )

    return executor()
