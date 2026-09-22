from pathlib import Path
import sys


def main() -> int:
    print("=== GATE 20 - APP SHADOW WIRING V1 ===")
    text = Path("app.py").read_text(encoding="utf-8", errors="replace")

    checks = {
        "shadow import": "from v14.app_shadow import run_app_shadow_dry_run" in text,
        "shadow default OFF": "V14_APP_SHADOW_ENABLED = False" in text,
        "legacy result variable": "legacy_result = analyze_stock(" in text,
        "legacy append preserved": "results.append(legacy_result)" in text,
        "shadow call": "run_app_shadow_dry_run(" in text,
        "shadow enabled flag": "enabled=V14_APP_SHADOW_ENABLED" in text,
    }

    failed = False
    for name, ok in checks.items():
        print(f"[{'PASS' if ok else 'FAIL'}] {name}")
        if not ok:
            failed = True

    if failed:
        print("=== GATE 20 WIRING RESULT: FAIL ===")
        return 1

    print("=== GATE 20 WIRING RESULT: PASS ===")
    return 0


if __name__ == "__main__":
    sys.exit(main())
