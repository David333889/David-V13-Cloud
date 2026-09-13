# David 戰情室 V13.100｜100檔智慧戰情版

## 本版新增
- 100檔股票池、10組設定
- 首頁：從100檔自動選 DAVID 今日 TOP 10
- Page 9：本週熱門候補 TOP 10
- Page 10：異常轉強股 TOP 10
- Page 1~8：六大核心族群 + DAVID自選20檔
- 每日 GitHub Action 改為100檔快照

## 既有 Supabase 專案必做一次
先在 SQL Editor 執行 `supabase_upgrade_v13_100.sql`，把 stock_config.position 的上限由60改為100。此動作不會刪除既有歷史資料。

## 安全
Supabase Secret / service_role key 只放 `.streamlit/secrets.toml`、Streamlit Cloud Secrets、GitHub Actions Secrets，絕對不要提交到 GitHub。

---

# David 戰情室 V13 Cloud｜100檔 × 20交易日智慧戰情版

## 已完成的功能

- 延續 V12 核心並升級為100檔、10組設定、每組10檔、六買/六賣、MACD、MA、量比、乖離、Pivot Swing Fibonacci、決策配色。
- 每頁仍採 10 檔智慧載入與 300 秒 Cache。
- 新增 Supabase 雲端歷史資料庫。
- 同一股票 + 同一交易日採 upsert：重開 App 不會產生重複資料。
- 個股可查看最近 20 個交易日：收盤、漲跌%、量比、乖離、六買、六賣、Fib 位置、決策。
- 左側可一鍵「保存全部100檔今日戰情」。
- GitHub Actions 於台灣時間週一至週五 14:45 自動執行 100 檔快照；遇休市日會再次 upsert 最近交易日，不會重複。
- 股票設定在 Supabase 連線後亦可雲端保存；本機未設定 Supabase 時仍可測試 App。

## 重要原則

V12 正式穩定版不要覆蓋。V13 使用獨立資料夾 / GitHub Repository 測試；V13 確認成功後再把手機改用雲端網址。

## A. 先建立 Supabase

1. 到 Supabase 建立免費 Project。
2. 進入 SQL Editor。
3. 將 `supabase_schema.sql` 全部貼入並執行。
4. 取得 Project URL。
5. 取得後端用 Secret/Service Role Key。此 Key 只能放在 Secrets，絕對不要寫進 GitHub 公開程式碼。

## B. 本機測試（可先不接 Supabase）

將整個 `David_V13_Cloud` 資料夾放到電腦，例如：

```bat
C:\David戰情室\V13Cloud
```

開 CMD：

```bat
cd /d C:\David戰情室\V13Cloud
python -m pip install -r requirements.txt
python -m py_compile app.py
python -m streamlit run app.py --server.address 0.0.0.0 --server.port 8501
```

未設定 Supabase 時，App 仍能看即時戰情，但會顯示「雲端資料庫尚未設定」。

## C. 本機接 Supabase 測試

把 `.streamlit/secrets.toml.example` 複製成 `.streamlit/secrets.toml`，填入：

```toml
[supabase]
url = "https://YOUR_PROJECT.supabase.co"
key = "YOUR_SECRET_OR_SERVICE_ROLE_KEY"
```

重新啟動 Streamlit。左側看到「☁️ 雲端資料庫：已連線」即成功。

第一次建議按：

**📚 保存全部100檔今日戰情**

完成後，到畫面下方選任一股票，即可看到歷史資料。

## D. 上傳 GitHub

建立一個新的 Repository，例如：

`david-stock-warroom-v13`

把這個資料夾內的檔案上傳。請確認 `.streamlit/secrets.toml` 沒有上傳；`.gitignore` 已經排除此檔。

GitHub Repository > Settings > Secrets and variables > Actions > New repository secret，建立：

- `SUPABASE_URL`
- `SUPABASE_KEY`

這兩個 Secret 給每天 14:45 的自動快照使用。

## E. 部署 Streamlit Community Cloud

1. 登入 Streamlit Community Cloud。
2. 連接剛建立的 GitHub Repository。
3. Main file path 選 `app.py`。
4. 在 Streamlit App 的 Settings > Secrets 貼入：

```toml
[supabase]
url = "https://YOUR_PROJECT.supabase.co"
key = "YOUR_SECRET_OR_SERVICE_ROLE_KEY"
```

5. Deploy。

完成後會得到類似：

`https://xxxxx.streamlit.app`

之後手機用 Wi-Fi / 4G / 5G 都可直接開啟，Windows 電腦不必保持開機。

## F. 每日自動保存

`.github/workflows/daily_snapshot.yml` 已設定：

- 週一至週五
- UTC 06:45 = 台灣 14:45
- 執行 `daily_snapshot_v13.py`
- 分 6 頁抓取，共 100 檔
- 寫入 Supabase `stock_history`

同一交易日、同一股票使用唯一鍵 `(trade_date, code)`，所以重跑也只會更新，不會重複新增。

GitHub > Actions > David V13 Daily Stock Snapshot 可手動按 `Run workflow` 做第一次測試。

## G. 20日資料邏輯

App 查詢每支股票最近 20 筆「交易日」資料，而不是 20 個日曆天。資料庫可保留更久，但畫面預設只顯示最新 20 個交易日，因此不會因週末或休市日少掉有效資訊。

## H. 驗收順序

1. `python -m py_compile app.py` 無錯誤。
2. 本機 V13 能正常顯示目前頁 10/10。
3. Supabase 顯示已連線。
4. 按「保存全部100檔今日戰情」後，Supabase `stock_history` 出現資料。
5. App 下方可看到個股歷史表與兩張趨勢圖。
6. GitHub Actions 手動 Run 成功。
7. Streamlit Cloud 部署成功。
8. 手機關閉 Wi-Fi、改 4G/5G，仍能打開 `streamlit.app` 網址。

完成以上 8 點，即代表「電腦不用一直開機 + 100檔20交易日歷史」正式成立。
