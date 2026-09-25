from v14.controlled_live_fetch import (
    execute_controlled_fetch,
)
from v14.finmind_golden_evidence import (
    build_finmind_golden_evidence,
)
from v14.finmind_live_request_parameters import (
    validate_finmind_live_params,
)


# Gate 28D.1C - One-shot live fetch integration contract.
# Integration only. Real network execution is not enabled here.

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


def execute_one_shot_live_fetch(
    env,
    session_factory,
    url,
    timeout,
    params,
    max_bytes=5_000_000,
):
    """
    Execute the protected one-shot fetch integration path.

    Order:
    1. Validate FinMind request parameters.
    2. Execute through the existing controlled-fetch boundary.
    3. Convert RAW evidence into sanitized golden metadata.
    4. Return golden metadata only.

    No result is forwarded to Core, score, decision, or persistence.
    """

    # 1. Parameters must fail closed before Session / GET.
    params_result = validate_finmind_live_params(
        params,
    )

    if params_result.get("allowed") is not True:
        return _deny(
            params_result.get(
                "reason",
                "PARAMS_REJECTED",
            )
        )

    safe_params = params_result.get("params")

    # 2. Reuse the already-protected controlled-fetch path.
    fetch_result = execute_controlled_fetch(
        env=env,
        session_factory=session_factory,
        url=url,
        timeout=timeout,
        params=safe_params,
        max_bytes=max_bytes,
    )

    if fetch_result.get("allowed") is not True:
        return _deny(
            fetch_result.get(
                "reason",
                "FETCH_REJECTED",
            )
        )

    evidence = fetch_result.get("evidence")

    # 3. Build sanitized golden metadata only.
    golden_result = build_finmind_golden_evidence(
        evidence=evidence,
        params=safe_params,
    )

    if golden_result.get("allowed") is not True:
        return _deny(
            golden_result.get(
                "reason",
                "GOLDEN_EVIDENCE_REJECTED",
            )
        )

    # 4. Public result contains golden metadata only.
    return {
        "allowed": True,
        "golden": golden_result.get("golden"),
    }
