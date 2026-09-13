# David V13.100 PATCH1

本修正版完成兩件事：

1. 修正 `8271 宇瞻`：上市，Yahoo Symbol 應為 `8271.TW`。
2. 新增 `backfill_20days_v13.py`：將100檔最近20交易日戰情回補至 Supabase。

## 建議執行順序
1. Supabase SQL Editor 執行 `supabase_fix_8271.sql`。
2. 備份本機 `app.py`、`daily_snapshot_v13.py`、`stock_config_v13.json`。
3. 用本包同名檔覆蓋三個檔案；保留 `.streamlit/secrets.toml`，不要覆蓋。
4. CMD 執行 `python backfill_20days_v13.py`。
5. 再執行 `python -m streamlit run app.py`。

注意：回補會 upsert，不會刪除既有歷史。
