from pathlib import Path


TITLE = "DAVID V14 - SUPABASE SCHEMA MIGRATION V1 VERIFIER"

MIGRATION_VERSION = "V14_SUPABASE_SCHEMA_MIGRATION_V1"
MIGRATION_PATH = Path("supabase_migration_v14_persistence_v1.sql")

REQUIRED_COLUMNS = {
    "payload_version": "text",
    "engine_version": "text",
    "baseline_version": "text",
    "risk_state": "text",
    "risk_level": "text",
    "risk_lock": "boolean",
    "action_state": "text",
    "action_signal": "text",
    "action_reason": "text",
    "action_risk_guard": "text",
    "action_confidence": "text",
    "consumer_state": "text",
}

FORBIDDEN_TOKENS = (
    "drop table",
    "truncate",
    "delete from",
    "drop column",
    "drop constraint",
)


print("=" * 72)
print(TITLE)
print("=" * 72)

print("[PASS] Migration Version =", MIGRATION_VERSION)
print("[PASS] Target = public.stock_history")
print(f"[PASS] Required V14 Columns = {len(REQUIRED_COLUMNS)}")

# ------------------------------------------------------------
# Expected RED #2
# Migration SQL must not exist before the specification/verifier.
# ------------------------------------------------------------
if not MIGRATION_PATH.exists():
    print()
    print("[EXPECTED RED #2]")
    print("Schema Migration SQL not found.")
    print("Expected file:", MIGRATION_PATH)
    raise SystemExit(1)

sql = MIGRATION_PATH.read_text(encoding="utf-8")

# Static verification must inspect executable SQL only.
# Ignore full-line SQL comments to avoid false positives such as:
# "-- no DROP / DELETE / TRUNCATE".
executable_lines = [
    line
    for line in sql.splitlines()
    if not line.lstrip().startswith("--")
]

normalized = " ".join(
    "\n".join(executable_lines).lower().split()
)

# ------------------------------------------------------------
# Static contract verification only.
# NO database connection / NO SQL execution.
# ------------------------------------------------------------
if "alter table public.stock_history" not in normalized:
    raise AssertionError(
        "Migration must target public.stock_history"
    )

for column, sql_type in REQUIRED_COLUMNS.items():
    if column.lower() not in normalized:
        raise AssertionError(
            f"Missing required column: {column}"
        )

    expected = f"{column.lower()} {sql_type.lower()}"
    if expected not in normalized:
        raise AssertionError(
            f"Type mismatch: expected '{expected}'"
        )

for token in FORBIDDEN_TOKENS:
    if token in normalized:
        raise AssertionError(
            f"Forbidden destructive SQL detected: {token}"
        )

print("[PASS] Target table verified")
print("[PASS] 12 V14 Persistence columns verified")
print("[PASS] Required SQL types verified")
print("[PASS] No destructive SQL detected")
print()
print("SUPABASE SCHEMA MIGRATION V1 RESULT: PASS")
print("V14_SUPABASE_SCHEMA_MIGRATION_V1 CONTRACT VERIFIED")