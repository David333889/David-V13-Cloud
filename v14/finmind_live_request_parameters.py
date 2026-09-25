from datetime import date


# Gate 28D.1A - FinMind live request parameters contract.
# Validation only. No network, session, token, or persistence.

ALLOWED_DATASET = "TaiwanStockPrice"

ALLOW_TOKEN_IN_PARAMS = False
ALLOW_UNKNOWN_PARAMS = False

ALLOWED_PARAM_KEYS = frozenset(
    {
        "dataset",
        "data_id",
        "start_date",
        "end_date",
    }
)


def _deny(reason):
    return {
        "allowed": False,
        "reason": reason,
    }


def _valid_iso_date(value):
    if not isinstance(value, str):
        return False

    try:
        parsed = date.fromisoformat(value)
    except ValueError:
        return False

    return parsed.isoformat() == value


def validate_finmind_live_params(params):
    """
    Validate the fixed parameter scope for the first controlled
    FinMind live request.

    This function performs validation only.
    It executes no network request and handles no token.
    """

    if not isinstance(params, dict):
        return _deny("PARAMS_REQUIRED")

    unknown_keys = set(params) - ALLOWED_PARAM_KEYS

    if unknown_keys:
        return _deny("UNKNOWN_PARAM")

    if params.get("dataset") != ALLOWED_DATASET:
        return _deny("DATASET_NOT_ALLOWED")

    data_id = params.get("data_id")

    if data_id is None or data_id == "":
        return _deny("DATA_ID_REQUIRED")

    if not isinstance(data_id, str):
        return _deny("DATA_ID_INVALID")

    if not data_id.isdigit():
        return _deny("DATA_ID_INVALID")

    start_date = params.get("start_date")
    end_date = params.get("end_date")

    if not _valid_iso_date(start_date):
        return _deny("DATE_INVALID")

    if not _valid_iso_date(end_date):
        return _deny("DATE_INVALID")

    if start_date != end_date:
        return _deny("SINGLE_DAY_REQUIRED")

    normalized = {
        "dataset": ALLOWED_DATASET,
        "data_id": data_id,
        "start_date": start_date,
        "end_date": end_date,
    }

    return {
        "allowed": True,
        "params": normalized,
    }
