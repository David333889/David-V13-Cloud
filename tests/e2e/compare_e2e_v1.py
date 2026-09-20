import json
import sys
from pathlib import Path

from tests.compare_v13_v14 import load_fixture
from v14.core_engine import run_core


ROOT = Path(__file__).resolve().parents[2]
FIXTURE_FILE = ROOT / "tests" / "fixtures" / "golden_real_001.csv"
EXPECTED_FILE = ROOT / "tests" / "expected" / "golden_real_001.expected.json"


def fail(message):
    print(f"[FAIL] {message}")
    return False


def passed(message):
    print(f"[PASS] {message}")
    return True


def main():
    print("=" * 70)
    print("DAVID V14 - E2E REGRESSION V1")
    print("=" * 70)

    ok = True

    with EXPECTED_FILE.open("r", encoding="utf-8") as f:
        expected = json.load(f)

    df = load_fixture(FIXTURE_FILE)

    if len(df) == expected.get("row_count"):
        passed(f"Golden Fixture loaded: {len(df)} rows")
    else:
        ok = fail(
            f"Fixture row count mismatch: "
            f"expected={expected.get('row_count')} actual={len(df)}"
        ) and ok

    market_input = expected.get("market_input")

    if not isinstance(market_input, dict):
        ok = fail("market_input missing from Golden Expected") and ok
    else:
        market_input = dict(market_input)
        market_input["_data"] = df
        passed("Golden market_input + fixture loaded")

    try:
        result = run_core(market_input)
        passed("run_core() executed")
    except Exception as exc:
        fail(f"run_core() raised {type(exc).__name__}: {exc}")
        return 1

    risk = getattr(result, "risk", None)
    action = getattr(result, "action", None)
    decision = getattr(result, "decision", None)

    if isinstance(risk, dict):
        passed("Risk Wired = True")
    else:
        ok = fail("Risk Wired = False") and ok

    if isinstance(action, dict):
        passed("Action Wired = True")
    else:
        ok = fail("Action Wired = False") and ok

    if isinstance(risk, dict):
        if risk.get("version") == "V14_RISK_V1":
            passed("Risk Version = V14_RISK_V1")
        else:
            ok = fail(
                f"Unexpected Risk Version: {risk.get('version')}"
            ) and ok

        if risk.get("state") == "READY":
            passed("Risk State = READY")
        else:
            ok = fail(
                f"Unexpected Risk State: {risk.get('state')}"
            ) and ok

        if risk.get("level") == "LOW":
            passed("Risk Level = LOW")
        else:
            ok = fail(
                f"Unexpected Risk Level: {risk.get('level')}"
            ) and ok

    if isinstance(action, dict):
        if action.get("version") == "V14_ACTION_V1":
            passed("Action Version = V14_ACTION_V1")
        else:
            ok = fail(
                f"Unexpected Action Version: {action.get('version')}"
            ) and ok

        if action.get("state") == "READY":
            passed("Action State = READY")
        else:
            ok = fail(
                f"Unexpected Action State: {action.get('state')}"
            ) and ok

        signal = action.get("signal")

        if signal == "WAIT":
            passed("Action Signal = WAIT")
        else:
            ok = fail(
                f"Unexpected Action Signal: {signal}"
            ) and ok

        reason = action.get("reason")

        if reason == "NEUTRAL_DECISION":
            passed("Action Reason = NEUTRAL_DECISION")
        else:
            ok = fail(
                f"Unexpected Action Reason: {reason}"
            ) and ok

    if isinstance(decision, dict):
        core_decision = decision.get(
            "core_decision",
            decision.get("decision"),
        )

        if core_decision == "觀望":
            passed("Core Decision = 觀望")
        else:
            ok = fail(
                f"Unexpected Core Decision: {core_decision}"
            ) and ok
    else:
        ok = fail("Decision wiring missing") and ok

    print("=" * 70)

    if ok:
        print("E2E RESULT: PASS")
        return 0

    print("E2E RESULT: FAIL")
    return 1


if __name__ == "__main__":
    sys.exit(main())