import re


# Gate 27 capability boundary.
# External live-source evidence is read-only and untrusted.
READ_ONLY = True

ALLOW_PRODUCTION_WRITE = False
ALLOW_SUPABASE_WRITE = False
ALLOW_CORE_INPUT = False
ALLOW_SCORE = False
ALLOW_DECISION = False
ALLOW_UNIT_GUESS = False


def classify_live_response(evidence):
    """
    Classify external live-source evidence without transforming it
    into core input, score, decision, or derived unit values.
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

    if status_code != 200:
        return "HTTP_ERROR"

    payload = evidence.get("payload")

    if not isinstance(payload, dict):
        return "SCHEMA_INVALID"

    data = payload.get("data")

    if not isinstance(data, list):
        return "SCHEMA_INVALID"

    if len(data) == 0:
        return "EMPTY_DATASET"

    return "RAW_EVIDENCE"


def sanitize_error(message):
    """
    Redact common token / API-key / Bearer-secret representations
    before an external-source error is exposed to logs or tests.
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
