from v14.finmind_live_backend import BASE_URL
from v14.live_fetch_safety import (
    build_raw_provenance,
    classify_fetch_response,
)


# Gate 28D.1B - FinMind golden evidence contract.
# Metadata/fingerprint only. No raw-payload persistence.

PROVIDER = "FinMind"

ALLOW_RAW_PAYLOAD_STORAGE = False
ALLOW_SECRET_STORAGE = False

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


def build_finmind_golden_evidence(
    evidence,
    params,
):
    """
    Build sanitized FinMind golden metadata from RAW_EVIDENCE.

    Reuses Gate 28A raw provenance and payload SHA-256.
    Does not store the raw payload, token, or authorization data.
    """

    classification = classify_fetch_response(
        evidence,
    )

    if classification != "RAW_EVIDENCE":
        return _deny(classification)

    if not isinstance(params, dict):
        return _deny("PARAMS_REQUIRED")

    dataset = params.get("dataset")
    data_id = params.get("data_id")
    start_date = params.get("start_date")
    end_date = params.get("end_date")

    if not all(
        isinstance(value, str) and value
        for value in (
            dataset,
            data_id,
            start_date,
            end_date,
        )
    ):
        return _deny("PARAMS_INVALID")

    if start_date != end_date:
        return _deny("SINGLE_DAY_REQUIRED")

    payload = evidence.get("payload")
    data = payload.get("data")

    provenance = build_raw_provenance(
        provider=PROVIDER,
        dataset=dataset,
        status_code=evidence.get("status_code"),
        content_type=evidence.get("content_type"),
        payload=payload,
    )

    golden = {
        "provider": provenance["provider"],
        "endpoint": BASE_URL,
        "dataset": provenance["dataset"],
        "data_id": data_id,
        "trading_date": start_date,
        "status_code": provenance["status_code"],
        "content_type": provenance["content_type"],
        "size_bytes": evidence.get("size_bytes"),
        "record_count": len(data),
        "payload_hash": provenance["payload_hash"],
    }

    return {
        "allowed": True,
        "golden": golden,
    }
