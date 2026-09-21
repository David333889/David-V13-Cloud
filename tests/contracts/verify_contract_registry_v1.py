from pathlib import Path
import json
import sys


ROOT = Path(__file__).resolve().parents[2]

REGISTRY = ROOT / "tests" / "contracts" / "contract_registry_v1.json"

EXPECTED_REGISTRY_VERSION = "V14_CONTRACT_REGISTRY_V1"
EXPECTED_SPEC_STATUS = "FROZEN"
EXPECTED_CONTRACT_COUNT = 7


def fail(message):
    print(f"[FAIL] {message}")
    return False


def main():
    print("=" * 72)
    print("DAVID V14 - CONTRACT REGISTRY V1 VERIFIER")
    print("=" * 72)

    ok = True

    print(f"[INFO] Registry path: {REGISTRY}")

    if not REGISTRY.exists():
        print("[FAIL] Contract Registry V1 does not exist")
        return 1

    print("[PASS] Contract Registry V1 detected")

    try:
        with REGISTRY.open("r", encoding="utf-8") as f:
            registry = json.load(f)
    except Exception as exc:
        print(f"[FAIL] Registry JSON load failed: {exc}")
        return 1

    print("[PASS] Registry JSON loaded")

    if registry.get("registry_version") == EXPECTED_REGISTRY_VERSION:
        print(f"[PASS] Registry Version = {EXPECTED_REGISTRY_VERSION}")
    else:
        ok = fail(
            f"Registry Version mismatch: {registry.get('registry_version')}"
        ) and ok

    if registry.get("spec_status") == EXPECTED_SPEC_STATUS:
        print(f"[PASS] Spec Status = {EXPECTED_SPEC_STATUS}")
    else:
        ok = fail(
            f"Spec Status mismatch: {registry.get('spec_status')}"
        ) and ok

    contracts = registry.get("contracts")

    if not isinstance(contracts, list):
        print("[FAIL] contracts must be a list")
        return 1

    if len(contracts) == EXPECTED_CONTRACT_COUNT:
        print(f"[PASS] Contract Count = {EXPECTED_CONTRACT_COUNT}")
    else:
        ok = fail(
            f"Contract Count mismatch: {len(contracts)}"
        ) and ok

    for entry in contracts:
        name = entry.get("name", "<UNKNOWN>")
        version = entry.get("contract_version")
        contract_path = entry.get("contract_path")
        comparator_path = entry.get("comparator_path")

        print("-" * 72)
        print(f"[CHECK] {name}")

        if not contract_path:
            ok = fail(f"{name}: contract_path missing") and ok
            continue

        if not comparator_path:
            ok = fail(f"{name}: comparator_path missing") and ok
            continue

        contract_file = ROOT / contract_path
        comparator_file = ROOT / comparator_path

        if contract_file.exists():
            print(f"[PASS] {name}: contract file exists")
        else:
            ok = fail(f"{name}: contract file missing") and ok
            continue

        if comparator_file.exists():
            print(f"[PASS] {name}: comparator file exists")
        else:
            ok = fail(f"{name}: comparator file missing") and ok

        try:
            with contract_file.open("r", encoding="utf-8") as f:
                source_contract = json.load(f)
        except Exception as exc:
            ok = fail(f"{name}: contract JSON load failed: {exc}") and ok
            continue

        source_version = source_contract.get("contract_version")

        if source_version == version:
            print(f"[PASS] {name}: version match = {version}")
        else:
            ok = fail(
                f"{name}: version mismatch "
                f"(registry={version}, source={source_version})"
            ) and ok

    print("=" * 72)

    if ok:
        print("CONTRACT REGISTRY V1 RESULT: PASS")
        print("[PASS] CONTRACT REGISTRY V1 VERIFIED")
        return 0

    print("CONTRACT REGISTRY V1 RESULT: FAIL")
    return 1


if __name__ == "__main__":
    sys.exit(main())