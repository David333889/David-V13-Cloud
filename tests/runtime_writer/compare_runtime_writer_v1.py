from pathlib import Path
import copy
import sys

ROOT = Path(__file__).resolve().parents[2]

if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from tests.consumer.compare_consumer_boundary_v1 import (
    build_valid_result,
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
        self.client.last_row = copy.deepcopy(row)
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


def build_runtime_valid_result():
    result = copy.deepcopy(build_valid_result())

    result["six_buy"]["score"] = 5
    result["six_sell"]["score"] = 1
    result["position"]["fib_position"] = "0.618"
    result["decision"]["core_decision"] = "BULLISH"

    return result


def build_valid_identity():
    return {
        "trade_date": "2026-09-20",
        "code": "2330",
        "name": "TEST",
        "market": "TW",
        "symbol": "2330.TW",
    }


def main():
    print("=" * 72)
    print("DAVID V14 - RUNTIME WRITER WIRING V1 COMPARATOR")
    print("=" * 72)

    try:
        from v14.runtime_writer import write_runtime_result
    except (ImportError, ModuleNotFoundError) as exc:
        print("[FAIL] Runtime Writer V1 implementation not found")
        print(f"[INFO] {exc}")
        print("RUNTIME WRITER V1 RESULT: FAIL")
        return 1

    if not callable(write_runtime_result):
        print("[FAIL] write_runtime_result() is not callable")
        return 1

    print("[PASS] write_runtime_result() detected")

    result = build_runtime_valid_result()
    identity = build_valid_identity()
    client = MockClient()

    try:
        actual = write_runtime_result(
            result,
            identity,
            client,
        )
    except Exception as exc:
        print(
            f"[FAIL] write_runtime_result() raised "
            f"{type(exc).__name__}: {exc}"
        )
        return 1

    if not isinstance(actual, dict):
        print("[FAIL] Runtime Writer result is not dict")
        return 1

    if actual.get("state") != "SAVED":
        print(
            "[FAIL] Expected state SAVED, "
            f"got: {actual.get('state')}"
        )
        return 1

    print("[PASS] Runtime Writer State = SAVED")

    if actual.get("reason") != "UPSERT_OK":
        print(
            "[FAIL] Expected reason UPSERT_OK, "
            f"got: {actual.get('reason')}"
        )
        return 1

    print("[PASS] Runtime Writer Reason = UPSERT_OK")

    if client.table_count != 1:
        print(f"[FAIL] table_count = {client.table_count}")
        return 1

    if client.upsert_count != 1:
        print(f"[FAIL] upsert_count = {client.upsert_count}")
        return 1

    if client.execute_count != 1:
        print(f"[FAIL] execute_count = {client.execute_count}")
        return 1

    print("[PASS] Exactly one table/upsert/execute")

    if client.last_table != "stock_history":
        print(f"[FAIL] Unexpected table: {client.last_table}")
        return 1

    print("[PASS] Target Table = stock_history")

    if client.last_conflict != "trade_date,code":
        print(
            "[FAIL] Unexpected conflict key: "
            f"{client.last_conflict}"
        )
        return 1

    print("[PASS] Conflict Key = trade_date,code")

    if not isinstance(client.last_row, dict):
        print("[FAIL] Persistence row not received by MockClient")
        return 1

    expected_identity = build_valid_identity()

    for key, value in expected_identity.items():
        if client.last_row.get(key) != value:
            print(
                f"[FAIL] Row identity mismatch: {key} "
                f"expected={value!r} "
                f"actual={client.last_row.get(key)!r}"
            )
            return 1

    print("[PASS] Persistence Row reached Writer unchanged")

    # Negative Case 1:
    # Missing injected client must be blocked before any write.
    blocked = write_runtime_result(
        build_runtime_valid_result(),
        build_valid_identity(),
        None,
    )

    if (
        not isinstance(blocked, dict)
        or blocked.get("state") != "BLOCKED"
        or blocked.get("reason") != "CLIENT_MISSING"
    ):
        print(
            "[FAIL] Missing client was not blocked correctly: "
            f"{blocked}"
        )
        return 1

    print("[PASS] Missing Client = BLOCKED / CLIENT_MISSING")

    # Negative Case 2:
    # Invalid upstream result must never reach Writer execute().
    blocked_client = MockClient()

    blocked = write_runtime_result(
        None,
        build_valid_identity(),
        blocked_client,
    )

    if not isinstance(blocked, dict):
        print("[FAIL] Invalid upstream result did not return dict")
        return 1

    if blocked.get("state") != "BLOCKED":
        print(
            "[FAIL] Invalid upstream result was not BLOCKED: "
            f"{blocked}"
        )
        return 1

    if (
        blocked_client.table_count != 0
        or blocked_client.upsert_count != 0
        or blocked_client.execute_count != 0
    ):
        print(
            "[FAIL] BLOCKED pipeline reached Writer: "
            f"table={blocked_client.table_count}, "
            f"upsert={blocked_client.upsert_count}, "
            f"execute={blocked_client.execute_count}"
        )
        return 1

    print("[PASS] Pipeline BLOCKED = zero Writer calls")

    print("-" * 72)
    print("RUNTIME WRITER V1 RESULT: PASS")
    print("MOCK CLIENT ONLY | NO PRODUCTION NETWORK I/O")
    return 0


if __name__ == "__main__":
    sys.exit(main())