import hashlib
import json
import re


# Gate 28A capability boundary.
# This module defines fetch-safety policy only.
# It does NOT perform a live HTTP request.
GET_ONLY = True

ALLOW_NETWORK_WRITE = False
ALLOW_CORE_INPUT = False
ALLOW_SUPABASE_WRITE = False
ALLOW_PRODUCTION_WRITE = False


def classify_fetch_response(evidence):
    """
    Classify fetch evidence without converting it into core input.
    """

    if not isinstance(evidence, dict):
        return "INVALID_EVIDENCE"

    if evidence.get("timeout") is True:
        return "TIMEOUT"

    if evidence.get("connection_error") is True:
        return "CONNECTION_FAILURE"

    status_code = evidence.get("status_code")

    if status_code in (401, 403):
        return "AUTH_FAILED"

    if status_code == 429:
        return "RATE_LIMITED"

    if status_code != 200:
        return "HTTP_ERROR"

    content_type = evidence.get("content_type", "")

    if not isinstance(content_type, str):
        return "CONTENT_TYPE_INVALID"

    if "application/json" not in content_type.lower():
        return "CONTENT_TYPE_INVALID"

    payload = evidence.get("payload")

    if not isinstance(payload, dict):
        return "SCHEMA_INVALID"

    data = payload.get("data")

    if not isinstance(data, list):
        return "SCHEMA_INVALID"

    if len(data) == 0:
        return "EMPTY_DATASET"

    return "RAW_EVIDENCE"


def sanitize_secret(message):
    """
    Redact common token / API-key / Bearer-secret representations.
    """

    if message is None:
        return ""

    text = str(message)

    patterns = (
        r"(?i)(token\s*=\s*)[^\s,;]+",
        r"(?i)(apikey\s*=\s*)[^\s,;]+",
        r"(?i)(api_key\s*=\s*)[^\s,;]+",
        r"(?i)(authorization\s*:\s*bearer\s+)[^\s,;]+",
    )

    for pattern in patterns:
        text = re.sub(pattern, r"\1[REDACTED]", text)

    return text


def build_raw_provenance(
    provider,
    dataset,
    status_code,
    content_type,
    payload,
):
    """
    Build minimal provenance for raw external evidence.
    No token or secret is accepted or stored here.
    """

    canonical_payload = json.dumps(
        payload,
        sort_keys=True,
        separators=(",", ":"),
        ensure_ascii=False,
    )

    payload_hash = hashlib.sha256(
        canonical_payload.encode("utf-8")
    ).hexdigest()

    return {
        "provider": provider,
        "dataset": dataset,
        "status_code": status_code,
        "content_type": content_type,
        "payload_hash": payload_hash,
    }
