# Gate 28D.2K-2F - Controlled Real Internet
# Crossing One-Shot Enforcement V1.
#
# Authorization guard only.
#
# This module does not execute a network request.
# It does not create a Session or read a runtime token.
# It only authorizes at most one future real GET.

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


class ControlledRealInternetCrossingOneShot:
    """
    Fail-closed one-shot authorization guard.

    The first authorization is allowed.
    Every later authorization is denied.

    No network request is executed here.
    """

    def __init__(self):
        self.real_get_count = 0

    def authorize(self):
        if self.real_get_count >= MAX_REAL_GETS:
            return {
                "allowed": False,
                "reason": "REAL_GET_LIMIT_REACHED",
            }

        self.real_get_count += 1

        return {
            "allowed": True,
            "real_get_number": self.real_get_count,
        }
