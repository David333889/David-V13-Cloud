# David 戰情室 V13.100 — 正式雲端部署版

## 已確認成功基準
- 100/100 股票行情可取得
- 8271 宇瞻已修正為 8271.TW
- Supabase 已連線且可寫入
- 20/20 交易日歷史已回補
- 首頁 DAVID TOP 10 正常
- Page 1~10 正常
- Page 9 本週熱門候補：100檔自動排名
- Page 10 異常轉強股：100檔自動排名

## 安全規則
- 不要把 `.streamlit/secrets.toml` 上傳 GitHub。
- Streamlit Cloud Secrets 使用 Supabase Secret key。
- GitHub Actions Secrets 建立 `SUPABASE_URL`、`SUPABASE_KEY`。

## 本機驗證
```
python verify_v13.py
python -m streamlit run app.py
```

## GitHub Actions
`.github/workflows/daily_snapshot.yml` 每週一至週五 14:45（台灣時間）執行每日100檔快照；也可在 GitHub Actions 手動執行 workflow_dispatch。

## Streamlit Cloud
主程式檔案：`app.py`

Secrets：
```
[supabase]
url = "https://YOUR_PROJECT.supabase.co"
key = "YOUR_SUPABASE_SECRET_KEY"
```

## 20日回補
如需重建最近20交易日：
```
python backfill_20days_v13.py
```
此動作採 upsert，不會因重跑而重複建立同一交易日/股票資料。
