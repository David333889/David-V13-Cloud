import importlib


class FakeExecutor:
    def __init__(self):
        self.calls = 0

    def __call__(self):
        self.calls += 1
        return {
            "allowed": True,
            "evidence": "FAKE_EVIDENCE",
        }

class FailingExecutor:
    def __init__(self):
        self.calls = 0

    def __call__(self):
        self.calls += 1
        return {
            "allowed": False,
            "reason": "FAKE_EXECUTOR_FAILURE",
        }

def main():
    print(
        "=== GATE 28D.2K-2G - CONTROLLED REAL INTERNET "
        "CROSSING ONE-SHOT INTEGRATION V1 ==="
    )

    try:
        module = importlib.import_module(
            "v14.controlled_real_internet_crossing_one_shot_integration"
        )
    except ModuleNotFoundError:
        print(
            "[EXPECTED RED] controlled real Internet crossing "
            "one-shot integration module not found"
        )
        raise SystemExit(1)

    execute = getattr(
        module,
        "execute_controlled_real_internet_crossing_once",
        None,
    )

    assert callable(execute), (
        "one-shot integration executor missing"
    )

    assert getattr(module, "READ_ONLY", None) is True
    assert getattr(module, "ONE_SHOT_ONLY", None) is True
    assert getattr(module, "MAX_REAL_GETS", None) == 1

    for flag in (
        "ALLOW_NORMALIZATION",
        "ALLOW_COMPATIBILITY_ESTABLISHMENT",
        "ALLOW_PROVIDER_SWITCH",
        "ALLOW_CORE_INPUT",
        "ALLOW_SCORE",
        "ALLOW_DECISION",
        "ALLOW_SUPABASE_WRITE",
        "ALLOW_PRODUCTION_WRITE",
    ):
        assert getattr(module, flag, None) is False

    guard_module = importlib.import_module(
        "v14.controlled_real_internet_crossing_one_shot"
    )

    guard = (
        guard_module.ControlledRealInternetCrossingOneShot()
    )

    fake_executor = FakeExecutor()

    first = execute(
        guard=guard,
        executor=fake_executor,
    )

    assert first == {
        "allowed": True,
        "evidence": "FAKE_EVIDENCE",
    }

    assert fake_executor.calls == 1
    assert guard.real_get_count == 1

    second = execute(
        guard=guard,
        executor=fake_executor,
    )

    assert second == {
        "allowed": False,
        "reason": "REAL_GET_LIMIT_REACHED",
    }

    assert fake_executor.calls == 1
    assert guard.real_get_count == 1

    third = execute(
        guard=guard,
        executor=fake_executor,
    )

    assert third == {
        "allowed": False,
        "reason": "REAL_GET_LIMIT_REACHED",
    }

    assert fake_executor.calls == 1
    assert guard.real_get_count == 1

    # A failed first execution still consumes the one-shot
    # authorization. Retry must fail before executor call.
    failure_guard = (
        guard_module.ControlledRealInternetCrossingOneShot()
    )

    failing_executor = FailingExecutor()

    failed_first = execute(
        guard=failure_guard,
        executor=failing_executor,
    )

    assert failed_first == {
        "allowed": False,
        "reason": "FAKE_EXECUTOR_FAILURE",
    }

    assert failing_executor.calls == 1
    assert failure_guard.real_get_count == 1

    failed_retry = execute(
        guard=failure_guard,
        executor=failing_executor,
    )

    assert failed_retry == {
        "allowed": False,
        "reason": "REAL_GET_LIMIT_REACHED",
    }

    assert failing_executor.calls == 1
    assert failure_guard.real_get_count == 1
    print("[PASS] failed execution consumes authorization")
    print("[PASS] failed execution retry denied before executor")
    print("[PASS] first authorization reaches executor once")
    print("[PASS] second execution denied before executor")
    print("[PASS] retry denied before executor")
    print("[PASS] executor call count fixed at one")
    print("[PASS] compatibility/core/write paths disabled")

    print(
        "=== GATE 28D.2K-2G CONTROLLED REAL INTERNET "
        "CROSSING ONE-SHOT INTEGRATION RESULT: PASS ==="
    )


if __name__ == "__main__":
    main()
