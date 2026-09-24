from v14.live_fetch_safety import sanitize_secret


# Gate 28B.4 secret-runtime boundary.
# Secrets are runtime-only and must not enter public evidence.
DEFAULT_TOKEN_ENV_NAME = "FINMIND_API_TOKEN"

ALLOW_SOURCE_SECRET = False
ALLOW_SECRET_IN_EVIDENCE = False
ALLOW_SECRET_IN_ERROR = False


def load_runtime_secret(
    env,
    name=DEFAULT_TOKEN_ENV_NAME,
):
    """
    Load a secret from an injected environment mapping.

    This function does not read os.environ directly.
    """

    if env is None:
        return {
            "available": False,
            "reason": "SECRET_MISSING",
        }

    try:
        value = env.get(name)
    except AttributeError:
        return {
            "available": False,
            "reason": "INVALID_ENVIRONMENT",
        }

    if value is None:
        return {
            "available": False,
            "reason": "SECRET_MISSING",
        }

    if not isinstance(value, str):
        return {
            "available": False,
            "reason": "SECRET_INVALID",
        }

    if not value.strip():
        return {
            "available": False,
            "reason": "SECRET_BLANK",
        }

    return {
        "available": True,
        "secret": value,
    }


def build_secret_metadata(
    loaded,
    name=DEFAULT_TOKEN_ENV_NAME,
):
    """
    Build a public-safe view without exposing secret material.
    """

    available = (
        isinstance(loaded, dict)
        and loaded.get("available") is True
    )

    return {
        "available": available,
        "name": name,
    }


def sanitize_runtime_error(message):
    """
    Redact common token representations from runtime errors.
    """

    return sanitize_secret(message)
