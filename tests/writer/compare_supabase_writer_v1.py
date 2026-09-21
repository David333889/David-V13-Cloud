import json
from copy import deepcopy
from pathlib import Path

from v14.supabase_writer import write_supabase_row


TITLE = "DAVID V14 - SUPABASE WRITER V1 COMPARATOR"

CONTRACT_PATH = Path(
    "tests/writer/golden_supabase_writer_cases_v1.json"
)


class MockExecute:
    def __init__(self, client):
        self.client = client

    def execute(self):
        self.client.execute_count += 1
        return {"mock": True, "status": "OK"}


class MockTable:
    def __init__(self, client, table_name):
        self.client = client
        self.table_name = table_name

    def upsert(self, row, on_conflict=None):
        self.client.upsert_count += 1
        self.client.last_row = deepcopy(row)
        self.client.last_conflict = on_conflict
        return MockExecute(self.client)


class MockClient:
    def __init__(self):
        self.table_count = 0
        self.upsert_count = 0
        self.execute_count = 0
        self.last_table = None
        self.last_conflict = None
        self.last_row = None

    def table(self, table_name):
        self.table_count += 1
        self.last_table = table_name
        return MockTable(self, table_name)


def make_persistence_result():
    return {
        "version": "V14_SUPABASE_PERSISTENCE_V1",
        "state": "READY",
        "reason": "PERSISTENCE_ROW_OK",
        "row": {
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
            "baseline_version": "d36ed7c",

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


def check(case_id, ok, detail=""):
    global passed, failed

    if ok:
        print(f"[PASS] {case_id}")
        passed += 1
    else:
        print(f"[FAIL] {case_id}")
        if detail:
            print("       ", detail)
        failed += 1


print("=" * 72)
print(TITLE)
print("=" * 72)

with CONTRACT_PATH.open("r", encoding="utf-8") as f:
    contract = json.load(f)

assert contract["contract_version"] == "V14_SUPABASE_WRITER_V1"
assert contract["spec_status"] == "FROZEN"
assert contract["source_contract"] == "V14_SUPABASE_PERSISTENCE_V1"
assert contract["target_table"] == "stock_history"
assert contract["conflict_key"] == "trade_date,code"

cases = contract["cases"]

print("[PASS] Golden Writer Contract Loaded:",
      contract["contract_version"])
print("[PASS] Spec Status =", contract["spec_status"])
print("[PASS] Source Contract =", contract["source_contract"])
print("[PASS] Target Table =", contract["target_table"])
print("[PASS] Conflict Key =", contract["conflict_key"])
print(f"[PASS] {len(cases)} Golden Writer Cases loaded")
print("[PASS] write_supabase_row() detected")
print("-" * 72)

passed = 0
failed = 0


# W01 - READY row -> exactly one upsert/execute
client = MockClient()
source = make_persistence_result()
out = write_supabase_row(source, client)

check(
    "W01",
    out["state"] == "SAVED"
    and out["reason"] == "UPSERT_OK"
    and client.table_count == 1
    and client.upsert_count == 1
    and client.execute_count == 1,
)


# W02 - Invalid persistence result
client = MockClient()
out = write_supabase_row("INVALID", client)

check(
    "W02",
    out["state"] == "BLOCKED"
    and out["reason"] == "INVALID_PERSISTENCE_RESULT"
    and client.execute_count == 0,
)


# W03 - Non-READY persistence result
client = MockClient()
source = make_persistence_result()
source["state"] = "BLOCKED"

out = write_supabase_row(source, client)

check(
    "W03",
    out["state"] == "BLOCKED"
    and out["reason"] == "PERSISTENCE_NOT_READY"
    and client.execute_count == 0,
)


# W04 - Missing row
client = MockClient()
source = make_persistence_result()
source["row"] = None

out = write_supabase_row(source, client)

check(
    "W04",
    out["state"] == "BLOCKED"
    and out["reason"] == "ROW_MISSING"
    and client.execute_count == 0,
)


# W05 - Missing injected client
source = make_persistence_result()
out = write_supabase_row(source, None)

check(
    "W05",
    out["state"] == "BLOCKED"
    and out["reason"] == "CLIENT_MISSING",
)


# W06 - Exact target table
client = MockClient()
source = make_persistence_result()

out = write_supabase_row(source, client)

check(
    "W06",
    out["state"] == "SAVED"
    and client.last_table == "stock_history",
)


# W07 - Exact conflict key
client = MockClient()
source = make_persistence_result()

out = write_supabase_row(source, client)

check(
    "W07",
    out["state"] == "SAVED"
    and client.last_conflict == "trade_date,code",
)


# W08 - Row must pass through unchanged
client = MockClient()
source = make_persistence_result()
expected_row = deepcopy(source["row"])

out = write_supabase_row(source, client)

check(
    "W08",
    out["state"] == "SAVED"
    and client.last_row == expected_row
    and source["row"] == expected_row,
)


print("-" * 72)
print(f"RESULT: {passed}/8 PASS | {failed}/8 FAIL")
print("-" * 72)

if failed:
    raise SystemExit(1)

print()
print("SUPABASE WRITER V1 RESULT: PASS")
print("V14_SUPABASE_WRITER_V1 CONTRACT VERIFIED")
print("MOCK CLIENT ONLY - NO PRODUCTION NETWORK I/O")