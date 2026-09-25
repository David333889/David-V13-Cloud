from pathlib import Path
import importlib


def main():
    print(
        "=== GATE 28D.0P - "
        "INTERNET CROSSING PREFLIGHT V1 ==="
    )

    module_name = "v14.internet_crossing_preflight"

    try:
        preflight = importlib.import_module(module_name)
    except ModuleNotFoundError:
        print("[EXPECTED RED] internet crossing preflight module not found")
        raise SystemExit(1)

    required_flags = {
        "ALLOW_LIVE_GET": False,
        "ALLOW_CORE_INPUT": False,
        "ALLOW_SCORE": False,
        "ALLOW_DECISION": False,
        "ALLOW_SUPABASE_WRITE": False,
        "ALLOW_PRODUCTION_WRITE": False,
    }

    for name, expected in required_flags.items():
        actual = getattr(preflight, name, None)
        assert actual is expected, (
            f"{name} expected {expected!r}, got {actual!r}"
        )

    assert getattr(
        preflight,
        "FINMIND_HOST",
        None,
    ) == "api.finmindtrade.com"

    assert getattr(
        preflight,
        "FINMIND_BASE_URL",
        None,
    ) == "https://api.finmindtrade.com/api/v4/data"

    assert getattr(
        preflight,
        "DATASET",
        None,
    ) == "TaiwanStockPrice"

    run_preflight = getattr(
        preflight,
        "run_preflight",
        None,
    )
    assert callable(run_preflight), "run_preflight missing"

    result = run_preflight()

    assert isinstance(result, dict)
    assert result.get("ready") is True
    assert result.get("network_executed") is False
    assert result.get("token_required") is False
    assert result.get("method") == "GET"
    assert result.get("host") == "api.finmindtrade.com"
    assert result.get("dataset") == "TaiwanStockPrice"

    module_text = Path(preflight.__file__).read_text(
        encoding="utf-8"
    ).lower()

    forbidden_patterns = (
        ".get(",
        ".post(",
        ".put(",
        ".patch(",
        ".delete(",
        "requests.get(",
        "requests.post(",
        "finmind_api_token=",
    )

    for pattern in forbidden_patterns:
        assert pattern not in module_text, (
            f"preflight must not execute network or embed secret: {pattern}"
        )

    print("[PASS] preflight capability flags fail closed")
    print("[PASS] FinMind target contract fixed")
    print("[PASS] TaiwanStockPrice scope fixed")
    print("[PASS] zero network execution")
    print("[PASS] no token required")
    print(
        "=== GATE 28D.0P INTERNET CROSSING "
        "PREFLIGHT RESULT: PASS ==="
    )


if __name__ == "__main__":
    main()
