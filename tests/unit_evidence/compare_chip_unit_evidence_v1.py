from pathlib import Path
import sys


DOC = Path("docs/V14_CHIP_UNIT_EVIDENCE_CONTRACT_V1.md")


def fail(message: str) -> int:
    print(f"[FAIL] {message}")
    return 1


def main() -> int:
    print("=== GATE 26 - CHIP UNIT EVIDENCE CONTRACT V1 ===")

    if not DOC.exists():
        return fail("unit evidence contract missing")

    text = DOC.read_text(encoding="utf-8-sig")

    required_rules = [
        "UNKNOWN UNIT != ASSUMED UNIT",
        "NO VERIFIED EVIDENCE = NO UNIT LOCK",
        "UNIT_PENDING != VERIFIED",
        "UNIT_PENDING != LOCKED",
        "Golden Fixture != Source Unit Evidence",
        "KEEP UNIT_PENDING",
        "PRODUCTION_WRITE = NOT_AUTHORIZED",
    ]

    for rule in required_rules:
        if rule not in text:
            return fail(f"required unit evidence rule missing: {rule}")

    print("[PASS] unit evidence governance rules present")

    required_datasets = [
        "TaiwanStockInstitutionalInvestorsBuySell",
        "TaiwanStockMarginPurchaseShortSale",
        "TaiwanStockSecuritiesLending",
        "TaiwanStockDayTrading",
    ]

    for dataset in required_datasets:
        if dataset not in text:
            return fail(f"dataset evidence row missing: {dataset}")

    print("[PASS] unit evidence datasets covered")

    required_states = [
        "INSUFFICIENT",
        "UNIT_PENDING",
        "PARTIAL",
        "PARTIAL_UNIT_LOCK",
    ]

    for state in required_states:
        if state not in text:
            return fail(f"unit evidence state missing: {state}")

    print("[PASS] fail-closed unit states preserved")

    forbidden_claims = [
        "UNIT_STATUS = VERIFIED_ALL",
        "ALL_UNITS_LOCKED",
        "PRODUCTION_WRITE = AUTHORIZED",
    ]

    for claim in forbidden_claims:
        if claim in text:
            return fail(f"unsupported unit completion claim: {claim}")

    print("[PASS] unsupported unit claims blocked")

    print("=== GATE 26 CHIP UNIT EVIDENCE RESULT: PASS ===")
    return 0


if __name__ == "__main__":
    sys.exit(main())
