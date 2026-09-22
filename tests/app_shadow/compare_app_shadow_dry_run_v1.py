import importlib
import sys


def main() -> int:
    print("=== GATE 20 - APP SHADOW DRY-RUN WIRING V1 ===")

    try:
        module = importlib.import_module("v14.app_shadow")
    except ModuleNotFoundError:
        print("[FAIL] implementation missing: v14.app_shadow")
        return 1

    fn = getattr(module, "run_app_shadow_dry_run", None)
    if not callable(fn):
        print("[FAIL] run_app_shadow_dry_run() missing or not callable")
        return 1

    calls = []

    def fake_dry_run(*args, **kwargs):
        calls.append((args, kwargs))
        return {"state": "READY", "reason": "TEST_READY", "row": {"ok": True}}

    legacy_result = {"昨收": 100, "開盤": 101, "現價": 102, "六買": 4, "六賣": 1, "Fib位置": "TEST", "決策": "看多"}
    data = object()

    # Contract 1: Shadow OFF must produce zero dry-run calls.
    calls.clear()
    off_result = fn(
        enabled=False,
        legacy_result=legacy_result,
        data=data,
        code="2330",
        name="TEST",
        market="TW",
        symbol="2330.TW",
        dry_run_fn=fake_dry_run,
    )
    if calls:
        print("[FAIL] Shadow OFF called dry-run")
        return 1
    if not isinstance(off_result, dict) or off_result.get("state") != "SKIPPED":
        print("[FAIL] Shadow OFF must return state=SKIPPED")
        return 1
    print("[PASS] Shadow OFF - calls / SKIPPED")

    # Contract 2: Shadow ON must call dry-run exactly once.
    calls.clear()
    on_result = fn(
        enabled=True,
        legacy_result=legacy_result,
        data=data,
        code="2330",
        name="TEST",
        market="TW",
        symbol="2330.TW",
        dry_run_fn=fake_dry_run,
    )
    if len(calls) != 1:
        print(f"[FAIL] Shadow ON expected exactly 1 call, got {len(calls)}")
        return 1
    if on_result.get("state") != "READY":
        print("[FAIL] Shadow ON did not preserve dry-run result")
        return 1
    print("[PASS] Shadow ON - one dry-run call")

    # Contract 3: Inputs must pass through unchanged.
    args, kwargs = calls[0]
    expected = {
        "legacy_result": legacy_result,
        "data": data,
        "code": "2330",
        "name": "TEST",
        "market": "TW",
        "symbol": "2330.TW",
    }
    for key, value in expected.items():
        if key not in kwargs or kwargs[key] is not value and kwargs[key] != value:
            print(f"[FAIL] input passthrough mismatch: {key}")
            return 1
    print("[PASS] Shadow input passthrough preserved")

    # Contract 4: Shadow exception must be isolated.
    def raising_dry_run(*args, **kwargs):
        raise RuntimeError("shadow-test-error")

    try:
        isolated = fn(
            enabled=True,
            legacy_result=legacy_result,
            data=data,
            code="2330",
            name="TEST",
            market="TW",
            symbol="2330.TW",
            dry_run_fn=raising_dry_run,
        )
    except Exception as exc:
        print(f"[FAIL] Shadow exception escaped: {exc}")
        return 1

    if not isinstance(isolated, dict) or isolated.get("state") != "BLOCKED" or isolated.get("reason") != "SHADOW_EXCEPTION":
        print("[FAIL] Shadow exception must return BLOCKED / SHADOW_EXCEPTION")
        return 1
    print("[PASS] Shadow exception isolated")

    print("=== GATE 20 RESULT: PASS ===")
    return 0


if __name__ == "__main__":
    sys.exit(main())
