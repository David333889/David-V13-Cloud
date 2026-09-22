from pathlib import Path
import sys


DOC = Path("docs/V14_CHIP_SOURCE_MAPPING_V1.md")


def fail(message: str) -> int:
    print(f"[FAIL] {message}")
    return 1


def main() -> int:
    print("=== GATE 23 - CHIP SOURCE MAPPING V1 ===")

    if not DOC.exists():
        return fail("source mapping document missing")

    text = DOC.read_text(encoding="utf-8-sig")

    required_sections = [
        "Source Mapping Matrix",
        "Institutional Investors",
        "Margin / Short",
        "Securities Lending",
        "Day Trading",
        "Historical Compatibility",
        "Unit Policy",
        "Freshness",
        "Raw / Derived Boundary",
    ]

    for section in required_sections:
        if section not in text:
            return fail(f"required section missing: {section}")

    print("[PASS] required mapping sections present")

    required_datasets = [
        "TaiwanStockInstitutionalInvestorsBuySell",
        "TaiwanStockMarginPurchaseShortSale",
        "TaiwanStockSecuritiesLending",
        "TaiwanStockDayTrading",
    ]

    for dataset in required_datasets:
        if dataset not in text:
            return fail(f"dataset missing: {dataset}")

    print("[PASS] official dataset mappings present")

    protection_rules = [
        "UNKNOWN UNIT != ASSUMED UNIT",
        "MISSING != ZERO",
        "RAW EVIDENCE != DERIVED SIGNAL",
        "Legacy Dealer != Missing",
        "Lending transaction volume != Lending balance",
    ]

    for rule in protection_rules:
        if rule not in text:
            return fail(f"protection rule missing: {rule}")

    print("[PASS] source protection rules preserved")

    required_categories = [
        "Foreign_Investor",
        "Investment_Trust",
        "Dealer",
        "Dealer_self",
        "Dealer_Hedging",
        "Foreign_Dealer_Self",
    ]

    for category in required_categories:
        if category not in text:
            return fail(f"institutional category missing: {category}")

    print("[PASS] institutional compatibility categories preserved")

    forbidden_claims = [
        "UNIT_STATUS = VERIFIED_ALL",
        "PRODUCTION_WRITE = AUTHORIZED",
        "CHIP_SCORE = READY",
    ]

    for claim in forbidden_claims:
        if claim in text:
            return fail(f"unsupported claim detected: {claim}")

    print("[PASS] unsupported completion claims blocked")

    print("=== GATE 23 SOURCE MAPPING RESULT: PASS ===")
    return 0


if __name__ == "__main__":
    sys.exit(main())
