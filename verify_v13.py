import json, pathlib, py_compile
root = pathlib.Path(__file__).resolve().parent
for name in ["app.py", "daily_snapshot_v13.py", "backfill_20days_v13.py"]:
    py_compile.compile(str(root / name), doraise=True)
with open(root / "stock_config_v13.json", encoding="utf-8") as f:
    cfg = json.load(f)
rows = cfg if isinstance(cfg, list) else cfg.get("stocks", cfg)
assert len(rows) == 100, f"Expected 100 stocks, got {len(rows)}"
row8271 = next((x for x in rows if str(x.get("code")) == "8271"), None)
assert row8271 and str(row8271.get("market")).upper() == "TW", f"8271 config incorrect: {row8271}"
print("V13.100 VERIFY: OK")
print("Stocks: 100/100")
print("8271: 8271.TW")
print("Python compile: OK")
print("secrets.toml included:", (root / ".streamlit" / "secrets.toml").exists())
