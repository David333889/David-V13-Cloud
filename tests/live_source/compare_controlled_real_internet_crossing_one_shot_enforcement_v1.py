import importlib


def main():
    print(
        "=== GATE 28D.2K-2F - CONTROLLED REAL INTERNET "
        "CROSSING ONE-SHOT ENFORCEMENT V1 ==="
    )

    try:
        module = importlib.import_module(
            "v14.controlled_real_internet_crossing_one_shot"
        )
    except ModuleNotFoundError:
        print(
            "[EXPECTED RED] controlled real Internet crossing "
            "one-shot enforcement module not found"
        )
        raise SystemExit(1)

    guard_class = getattr(
        module,
        "ControlledRealInternetCrossingOneShot",
        None,
    )

    assert guard_class is not None, (
        "one-shot enforcement guard missing"
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

    guard = guard_class()

    first = guard.authorize()

    assert first == {
        "allowed": True,
        "real_get_number": 1,
    }

    second = guard.authorize()

    assert second == {
        "allowed": False,
        "reason": "REAL_GET_LIMIT_REACHED",
    }

    third = guard.authorize()

    assert third == {
        "allowed": False,
        "reason": "REAL_GET_LIMIT_REACHED",
    }

    assert guard.real_get_count == 1

    print("[PASS] first execution authorized")
    print("[PASS] second execution denied")
    print("[PASS] retry remains denied")
    print("[PASS] real GET authorization count fixed at one")
    print("[PASS] compatibility/core/write paths disabled")

    print(
        "=== GATE 28D.2K-2F CONTROLLED REAL INTERNET "
        "CROSSING ONE-SHOT ENFORCEMENT RESULT: PASS ==="
    )


if __name__ == "__main__":
    main()
