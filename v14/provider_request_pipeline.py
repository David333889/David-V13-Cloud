from v14.live_request_safety import validate_request
from v14.provider_client import (
    classify_provider_evidence,
    fetch_provider_data,
)


# Gate 28B.2 integration boundary.
# Unsafe requests must stop before transport execution.
ALLOW_LIVE_NETWORK = False
ALLOW_CORE_INPUT = False
ALLOW_SUPABASE_WRITE = False
ALLOW_PRODUCTION_WRITE = False


def execute_safe_provider_request(
    transport,
    url,
    allowed_hosts,
    token,
    timeout,
    params=None,
):
    """
    Validate request safety before invoking the injected transport.
    """

    request_check = validate_request(
        url=url,
        allowed_hosts=allowed_hosts,
        timeout=timeout,
    )

    if request_check.get("allowed") is not True:
        return {
            "allowed": False,
            "reason": request_check.get(
                "reason",
                "REQUEST_REJECTED",
            ),
        }

    evidence = fetch_provider_data(
        transport=transport,
        url=url,
        token=token,
        timeout=timeout,
        params=params,
    )

    classification = classify_provider_evidence(
        evidence
    )

    return {
        "allowed": True,
        "classification": classification,
        "evidence": evidence,
    }
