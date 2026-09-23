from pathlib import Path
import importlib


MODULE_NAME = "v14.live_source_boundary"


def fail(message):
    print(f"[FAIL] {message}")
    raise SystemExit(1)


def passed(message):
    print(f"[PASS] {message}")


print("=== GATE 27 - LIVE SOURCE READ-ONLY BOUNDARY V1 ===")


# 1. Boundary module must exist
module_path = Path("v14/live_source_boundary.py")

if not module_path.exists():
    fail("live source boundary module not found")

passed("live source boundary module exists")


# 2. Boundary module must be importable
try:
    boundary = importlib.import_module(MODULE_NAME)
except Exception as exc:
    fail(f"boundary import failed: {type(exc).__name__}")

passed("live source boundary importable")


# 3. Required public contract
required_names = (
    "READ_ONLY",
    "ALLOW_PRODUCTION_WRITE",
    "ALLOW_SUPABASE_WRITE",
    "ALLOW_CORE_INPUT",
    "ALLOW_SCORE",
    "ALLOW_DECISION",
    "ALLOW_UNIT_GUESS",
    "classify_live_response",
    "sanitize_error",
)

for name in required_names:
    if not hasattr(boundary, name):
        fail(f"required contract missing: {name}")

passed("required public contract present")


# 4. Fail-closed capability flags
if boundary.READ_ONLY is not True:
    fail("READ_ONLY must be True")

for name in (
    "ALLOW_PRODUCTION_WRITE",
    "ALLOW_SUPABASE_WRITE",
    "ALLOW_CORE_INPUT",
    "ALLOW_SCORE",
    "ALLOW_DECISION",
    "ALLOW_UNIT_GUESS",
):
    if getattr(boundary, name) is not False:
        fail(f"{name} must be False")

passed("fail-closed capability flags preserved")


# 5. Failure taxonomy
cases = (
    (
        {"status_code": 200, "payload": {"data": []}},
        "EMPTY_DATASET",
    ),
    (
        {"status_code": 401, "payload": None},
        "AUTH_FAILED",
    ),
    (
        {"status_code": 500, "payload": None},
        "HTTP_ERROR",
    ),
    (
        {"timeout": True},
        "TIMEOUT",
    ),
    (
        {"connection_error": True},
        "CONNECTION_FAILURE",
    ),
)

for evidence, expected in cases:
    actual = boundary.classify_live_response(evidence)
    if actual != expected:
        fail(
            f"failure taxonomy mismatch: expected={expected}, actual={actual}"
        )

passed("failure taxonomy fail-closed")


# 6. Valid raw evidence must remain raw
valid = {
    "status_code": 200,
    "payload": {
        "data": [
            {
                "date": "2026-09-23",
                "value": 0,
            }
        ]
    },
}

if boundary.classify_live_response(valid) != "RAW_EVIDENCE":
    fail("valid response not classified as RAW_EVIDENCE")

passed("valid response remains raw evidence")


# 7. Explicit zero must not become missing
zero_case = {
    "status_code": 200,
    "payload": {
        "data": [
            {
                "value": 0,
            }
        ]
    },
}

if boundary.classify_live_response(zero_case) != "RAW_EVIDENCE":
    fail("explicit zero was not preserved as raw evidence")

passed("explicit zero preserved")


# 8. Token / secret redaction
secret = "DAVID_TEST_SECRET_123456"

unsafe_messages = (
    f"token={secret}",
    f"apikey={secret}",
    f"Authorization: Bearer {secret}",
)

for message in unsafe_messages:
    sanitized = boundary.sanitize_error(message)

    if secret in sanitized:
        fail("secret leaked through sanitize_error")

passed("token and secret redaction enforced")


# 9. Boundary source must not wire into forbidden systems
source = module_path.read_text(encoding="utf-8").lower()

for forbidden in (
    "supabase_writer",
    "runtime_writer",
    "core_engine",
):
    if forbidden in source:
        fail(f"forbidden wiring detected: {forbidden}")

passed("no core/write wiring detected")


print("=== GATE 27 LIVE SOURCE READ-ONLY BOUNDARY RESULT: PASS ===")
