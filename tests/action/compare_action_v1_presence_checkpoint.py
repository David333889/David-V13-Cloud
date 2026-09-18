from v14 import core_engine


print("=" * 72)
print("DAVID V14 - GATE 5 ACTION PRESENCE CHECKPOINT")
print("=" * 72)

if hasattr(core_engine, "calculate_action"):
    print("[PASS] calculate_action() detected")
    raise SystemExit(0)

print("[EXPECTED RED] calculate_action() NOT detected")
print("Gate 5 implementation has NOT started.")
print("Golden Contract exists before implementation.")
raise SystemExit(1)