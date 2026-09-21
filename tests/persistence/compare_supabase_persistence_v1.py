import json
from pathlib import Path

from v14.supabase_persistence_adapter import build_supabase_row


TITLE = "DAVID V14 - SUPABASE PERSISTENCE V1 COMPARATOR"
CONTRACT_PATH = Path(
    "tests/persistence/golden_supabase_persistence_cases_v1.json"
)


def make_record():
    return {
        "state": "READY",
        "reason": "STORAGE_RECORD_OK",
        "record": {
            "trade_date": "2026-09-21",
            "code": "2330",
            "name": "TEST",
            "market": "TW",
            "symbol": "2330.TW",

            "buy_score": 6,
            "sell_score": 1,
            "fib_position": "TEST_FIB",
            "decision": "TEST_DECISION",

            "payload_version": "V14_INTEGRATION_PAYLOAD_V1",
            "engine_version": "V13.100",
            "baseline_version": "9f31b5c",

            "risk_state": "READY",
            "risk_level": "LOW",
            "risk_lock": False,

            "action_state": "READY",
            "action_signal": "WAIT",
            "action_reason": "NEUTRAL_DECISION",
            "action_risk_guard": "PASS",
            "action_confidence": "NORMAL",

            "consumer_state": "READY",
        },
    }


print("=" * 72)
print(TITLE)
print("=" * 72)

with CONTRACT_PATH.open("r", encoding="utf-8") as f:
    contract = json.load(f)

assert contract["contract_version"] == "V14_SUPABASE_PERSISTENCE_V1"
assert contract["spec_status"] == "FROZEN"
assert contract["source_contract"] == "V14_STORAGE_RECORD_V1"
assert contract["target"] == "public.stock_history"

cases = contract["cases"]

print("[PASS] Golden Persistence Contract Loaded:",
      contract["contract_version"])
print("[PASS] Spec Status =", contract["spec_status"])
print("[PASS] Source Contract =", contract["source_contract"])
print("[PASS] Target =", contract["target"])
print(f"[PASS] {len(cases)} Golden Persistence Cases loaded")
print("[PASS] build_supabase_row() detected")
print("-" * 72)

passed = 0
failed = 0


def check(case_id, actual, state, reason):
    global passed, failed

    ok = (
        actual.get("state") == state
        and actual.get("reason") == reason
    )

    if ok:
        print(f"[PASS] {case_id}")
        passed += 1
    else:
        print(f"[FAIL] {case_id}")
        print("       EXPECTED:", state, reason)
        print("       ACTUAL  :", actual)
        failed += 1


# P01 - Complete READY Storage Record
r = make_record()
check(
    "P01",
    build_supabase_row(r),
    "READY",
    "PERSISTENCE_ROW_OK",
)

# P02 - Invalid outer type
check(
    "P02",
    build_supabase_row("INVALID"),
    "BLOCKED",
    "INVALID_STORAGE_RECORD_TYPE",
)

# P03 - Missing trade_date
r = make_record()
del r["record"]["trade_date"]
check(
    "P03",
    build_supabase_row(r),
    "BLOCKED",
    "MISSING_REQUIRED_FIELD",
)

# P04 - Missing code
r = make_record()
del r["record"]["code"]
check(
    "P04",
    build_supabase_row(r),
    "BLOCKED",
    "MISSING_REQUIRED_FIELD",
)

# P05 - Core must pass through unchanged
r = make_record()
out = build_supabase_row(r)
core_ok = (
    out["state"] == "READY"
    and out["row"]["buy_score"] == r["record"]["buy_score"]
    and out["row"]["sell_score"] == r["record"]["sell_score"]
    and out["row"]["fib_position"] == r["record"]["fib_position"]
    and out["row"]["decision"] == r["record"]["decision"]
)

check(
    "P05",
    {
        "state": "READY" if core_ok else "BLOCKED",
        "reason": "PERSISTENCE_ROW_OK" if core_ok else "CORE_CHANGED",
    },
    "READY",
    "PERSISTENCE_ROW_OK",
)

# P06 - Version fields must pass through unchanged
r = make_record()
out = build_supabase_row(r)
version_ok = all(
    out["row"][k] == r["record"][k]
    for k in (
        "payload_version",
        "engine_version",
        "baseline_version",
    )
)

check(
    "P06",
    {
        "state": "READY" if version_ok else "BLOCKED",
        "reason": "PERSISTENCE_ROW_OK" if version_ok else "VERSION_CHANGED",
    },
    "READY",
    "PERSISTENCE_ROW_OK",
)

# P07 - Safety fields must pass through unchanged
r = make_record()
out = build_supabase_row(r)

safety_fields = (
    "risk_state",
    "risk_level",
    "risk_lock",
    "action_state",
    "action_signal",
    "action_reason",
    "action_risk_guard",
    "action_confidence",
    "consumer_state",
)

safety_ok = all(
    out["row"][k] == r["record"][k]
    for k in safety_fields
)

check(
    "P07",
    {
        "state": "READY" if safety_ok else "BLOCKED",
        "reason": "PERSISTENCE_ROW_OK" if safety_ok else "SAFETY_CHANGED",
    },
    "READY",
    "PERSISTENCE_ROW_OK",
)

# P08 - Legacy Market Snapshot remains deferred
r = make_record()

legacy_fields = (
    "prev_close",
    "open_price",
    "close_price",
    "change_value",
    "change_pct",
    "volume_ratio",
    "bias_pct",
    "morning",
    "momentum",
    "cost",
    "strength",
)

out = build_supabase_row(r)
deferred_ok = all(
    field not in out["row"]
    for field in legacy_fields
)

check(
    "P08",
    {
        "state": "READY" if deferred_ok else "BLOCKED",
        "reason": (
            "PERSISTENCE_ROW_OK"
            if deferred_ok
            else "DEFERRED_FIELD_LEAK"
        ),
    },
    "READY",
    "PERSISTENCE_ROW_OK",
)

print("-" * 72)
print(f"RESULT: {passed}/8 PASS | {failed}/8 FAIL")
print("-" * 72)

if failed:
    raise SystemExit(1)

print()
print("SUPABASE PERSISTENCE V1 RESULT: PASS")
print("V14_SUPABASE_PERSISTENCE_V1 CONTRACT VERIFIED")