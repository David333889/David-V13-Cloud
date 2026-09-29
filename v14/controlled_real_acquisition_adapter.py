# Gate 28D.2K-2H - Controlled Real
# Acquisition Adapter Boundary V1.
#
# Thin callable adapter only.
#
# Building the executor performs no acquisition.
# The injected acquisition callable is invoked only
# when the returned executor is explicitly called.
#
# This module does not create a Session, read os.environ,
# implement an HTTP request, normalize data,
# establish compatibility, or write persistence.

READ_ONLY = True
ONE_SHOT_COMPATIBLE = True

ALLOW_NORMALIZATION = False
ALLOW_COMPATIBILITY_ESTABLISHMENT = False
ALLOW_PROVIDER_SWITCH = False
ALLOW_CORE_INPUT = False
ALLOW_SCORE = False
ALLOW_DECISION = False
ALLOW_SUPABASE_WRITE = False
ALLOW_PRODUCTION_WRITE = False


def build_controlled_real_acquisition_executor(
    acquisition,
    env,
    session_factory,
    url,
    timeout,
    params,
    stock_id,
    trading_date,
    max_bytes=5_000_000,
):
    """
    Build a zero-argument callable around an injected
    controlled real acquisition function.

    Building the callable performs no acquisition.
    """

    if not callable(acquisition):
        raise ValueError("acquisition callable is required")

    def executor():
        return acquisition(
            env=env,
            session_factory=session_factory,
            url=url,
            timeout=timeout,
            params=params,
            stock_id=stock_id,
            trading_date=trading_date,
            max_bytes=max_bytes,
        )

    return executor
