import subprocess
import sys


def run_gate(name, command):
    print()
    print("=" * 70)
    print(f"RUNNING: {name}")
    print("=" * 70)

    result = subprocess.run(command)

    if result.returncode == 0:
        print(f"[PASS] {name}")
        return True

    print(f"[FAIL] {name} | return code = {result.returncode}")
    return False


def main():
    print("=" * 70)
    print("DAVID V14 - UNIFIED REGRESSION RUNNER")
    print("=" * 70)

    results = []

    results.append(
        run_gate(
            "GATE 3 - CORE BASELINE",
            [sys.executable, r"tests\compare_v13_v14.py"],
        )
    )

    results.append(
        run_gate(
            "GATE 4 - RISK ENGINE",
            [sys.executable, r"tests\risk\compare_risk_v1.py"],
        )
    )

    results.append(
        run_gate(
            "GATE 5 - ACTION ENGINE",
            [sys.executable, "-m", "tests.action.compare_action_v1"],
        )
    )
    results.append(
        run_gate(
            "ACTION BOUNDARY V1",
            [sys.executable, "-m", "tests.action.compare_action_boundary_v1"],
        )
    )

    results.append(
        run_gate(
            "CONTRACT REGISTRY V1",
            [sys.executable, "-m", "tests.contracts.verify_contract_registry_v1"],
        )
    )

    results.append(
        run_gate(
            "GATE 6 - CONSUMER BOUNDARY",
            [sys.executable, "-m", "tests.consumer.compare_consumer_boundary_v1"],
        )
    )

    results.append(
        run_gate(
            "INTEGRATION PAYLOAD V1",
            [
                sys.executable,
                "-m",
                "tests.integration.compare_integration_payload_v1",
            ],
        )
    )

    results.append(
        run_gate(
            "STORAGE RECORD V1",
            [
                sys.executable,
                "-m",
                "tests.storage.compare_storage_record_v1",
            ],
        )
    )

    results.append(
        run_gate(
            "SUPABASE PERSISTENCE V1",
            [
                sys.executable,
                "-m",
                "tests.persistence.compare_supabase_persistence_v1",
            ],
        )
    )

    results.append(
        run_gate(
            "RUNTIME PIPELINE V1",
            [
                sys.executable,
                "-m",
                "tests.runtime.compare_runtime_pipeline_v1",
            ],
        )
    )

    results.append(
        run_gate(
            "RUNTIME WRITER V1",
            [
                sys.executable,
                "-m",
                "tests.runtime_writer.compare_runtime_writer_v1",
            ],
        )
    )

    results.append(
        run_gate(
            "APP MARKET INPUT ADAPTER V1",
            [
                sys.executable,
                "-m",
                "tests.app_adapter.compare_app_market_input_adapter_v1",
            ],
        )
    )

    results.append(
        run_gate(
            "APP DRY-RUN PIPELINE V1",
            [
                sys.executable,
                "-m",
                "tests.app_dry_run.compare_app_dry_run_v1",
            ],
        )
    )

    results.append(
        run_gate(
            "SUPABASE SCHEMA MIGRATION V1",
            [
                sys.executable,
                "-m",
                "tests.schema.verify_supabase_schema_migration_v1",
            ],
        )
    )

    results.append(
        run_gate(
            "SUPABASE WRITER V1",
            [
                sys.executable,
                "-m",
                "tests.writer.compare_supabase_writer_v1",
            ],
        )
    )

    results.append(
        run_gate(
            "APP SHADOW DRY-RUN WIRING V1",
            [
                sys.executable,
                "-m",
                "tests.app_shadow.compare_app_shadow_dry_run_v1",
            ],
        )
    )
    results.append(
        run_gate(
            "APP SHADOW WIRING V1",
            [
                sys.executable,
                "-m",
                "tests.app_shadow.compare_app_shadow_wiring_v1",
            ],
        )
    )

    results.append(
        run_gate(
            "NORMALIZED CHIP DATA CONTRACT V1",
            [sys.executable, "-m", "tests.chip.compare_chip_contract_v1"],
        )
    )
    results.append(
        run_gate(
            "CHIP EVIDENCE CONTRACT V1",
            [sys.executable, "-m", "tests.chip.compare_chip_evidence_v1"],
        )
    )
    results.append(
        run_gate(
            "CHIP SOURCE MAPPING V1",
            [sys.executable, "-m", "tests.source_mapping.compare_chip_source_mapping_v1"],
        )
    )

    results.append(
        run_gate(
            "E2E - FULL CORE WIRING",
            [sys.executable, "-m", "tests.e2e.compare_e2e_v1"],
        )
    )
    print()
    print("=" * 70)
    print("V14 REGRESSION SUMMARY")
    print("=" * 70)

    gate_names = [
        "GATE 3 - CORE BASELINE",
        "GATE 4 - RISK ENGINE",
        "GATE 5 - ACTION ENGINE",
        "ACTION BOUNDARY V1",
        "CONTRACT REGISTRY V1",
        "GATE 6 - CONSUMER BOUNDARY",
        "INTEGRATION PAYLOAD V1",
        "STORAGE RECORD V1",
        "SUPABASE PERSISTENCE V1",
        "RUNTIME PIPELINE V1",
        "RUNTIME WRITER V1",
        "APP MARKET INPUT ADAPTER V1",
        "APP DRY-RUN PIPELINE V1",
        "SUPABASE SCHEMA MIGRATION V1",
        "SUPABASE WRITER V1",
        "APP SHADOW DRY-RUN WIRING V1",
        "APP SHADOW WIRING V1",
        "NORMALIZED CHIP DATA CONTRACT V1",
        "CHIP EVIDENCE CONTRACT V1",
        "CHIP SOURCE MAPPING V1",
        "E2E - FULL CORE WIRING",
    ]

    for name, passed in zip(gate_names, results):
        status = "PASS" if passed else "FAIL"
        print(f"{name}: {status}")

    print("=" * 70)

    if all(results):
        print("V14 REGRESSION RESULT: PASS")
        return 0

    print("V14 REGRESSION RESULT: FAIL")
    return 1


if __name__ == "__main__":
    sys.exit(main())
