# DAVID V14 UNIFIED ENGINE — DATA SOURCE SPEC

> V14 Unified Engine 資料來源與六大引擎對照規格書  
> 基準版本：V13.100 Cloud  
> 開發分支：develop-v14-unified  
> Core Baseline：docs/V13_CORE_BASELINE.md  
> Test Plan：docs/V14_TEST_PLAN.md

---

# 1. 文件目的

本文件定義 DAVID V14 Unified Engine 的資料來源、資料責任、
六大引擎使用範圍、資料保存方式及安全規則。

V14 的核心原則：

DATA ≠ SIGNAL ≠ DECISION ≠ ACTION

資料來源只負責提供原始資料。

任何外部資料不得直接產生買進、賣出或其他交易動作。

所有判斷必須經過 DAVID Engine 的正式規則處理。

---

# 2. V14 資料架構

DAVID V14 採多來源資料架構：

FinMind
→ PRIMARY DATA PROVIDER

Yahoo Finance
→ V13 BASELINE / PRICE FALLBACK

TWSE / TPEx
→ OFFICIAL VERIFY SOURCE

Supabase
→ DAVID DATA WAREHOUSE

DAVID V14 Unified Engine
→ CALCULATION / SIGNAL / RISK / ACTION

資料流程：

External Data
↓
Data Adapter
↓
Normalized Schema
↓
Supabase
↓
DAVID Unified Engine
↓
Technical / Chip / Market / Position / Risk
↓
Action Engine
↓
Streamlit Dashboard

---

# 3. V13 Baseline 資料來源

V13.100 現行 Core 使用 Yahoo Finance OHLCV。

在 V14 Core Baseline 驗證完成以前：

禁止直接以 FinMind 取代 Yahoo。

原因：

若同時進行：

資料來源更換
+
Core 模組化
+
新功能加入

發生結果差異時將無法判斷原因。

因此：

Yahoo Finance

目前定位：

V13 BASELINE SOURCE

以及未來：

PRICE FALLBACK SOURCE

---

# 4. FinMind 定位

FinMind 定位為：

V14 PRIMARY TAIWAN MARKET DATA PROVIDER

主要負責：

- OHLCV
- 三大法人
- 外資相關資料
- 融資融券
- 借券
- 當沖
- 股權持股分級
- 市場資料
- 基本面 Context
- 其他經正式確認的台股資料

FinMind 不負責：

- 六買六賣
- Pivot Fibonacci
- Core Decision
- DAVID Score
- Risk Decision
- Action Decision

以上全部由 DAVID Engine 計算。

---

# 5. FinMind 方案策略

V14 開發初期：

FINMIND PLAN = FREE

用途：

- API Schema 驗證
- Dataset 欄位確認
- Data Adapter 開發
- 小量測試
- Golden Data 比對

目前：

不購買付費方案。

---

# 6. Backer 升級條件

只有當 V14 開始需要：

- 大量全市場資料
- 100檔批次籌碼資料
- 進階籌碼 Dataset
- 股權持股分級
- 較高 API Request Limit
- 正式 Daily Collector

才重新評估：

FINMIND BACKER

是否升級必須依：

實際 API 使用量
+
實際 Dataset 權限
+
授權條款
+
V14 實際需求

決定。

不得因「可能以後會用到」提前購買。

---

# 7. Sponsor 升級條件

Sponsor 不屬於 V14 第一階段必要條件。

只有當未來正式需要：

- FinMind 即時市場資料
- 更高 API 額度
- Sponsor 專屬 Dataset
- 盤中市場共振資料

才重新評估。

即使升級 Sponsor：

即時資料仍不得直接產生 Action。

---

# 8. Sponsor Pro

V14 第一階段：

NOT REQUIRED

不得因大量下載或未來可能商業化而提前升級。

若未來：

- SaaS
- Web 對外服務
- App
- 公司正式內部系統
- 商業用途
- 大量資料產品

則必須重新確認：

FinMind 最新授權條款與方案。

---

# 9. 六大引擎

V14 Unified Engine 分為：

1. Technical Engine
2. Chip Engine
3. Market Engine
4. Position Engine
5. Risk Engine
6. Action Engine

各 Engine 職責必須分離。

禁止跨層偷偷修改 Core。

---

# 10. Technical Engine

主要輸入：

OHLCV

資料來源優先順序：

1. V13 Baseline：Yahoo Finance
2. V14 Primary：FinMind
3. Fallback：Yahoo Finance

主要計算：

- Prev Close
- Open
- High
- Low
- Close
- Volume
- MA5
- MA20
- VM20
- MACD Histogram
- Mid
- Volume Ratio
- Bias20
- Early
- Momentum
- Cost
- Strength
- Six Buy
- Six Sell
- Core Decision

V13 六買六賣及 Decision：

LOCK

FinMind 不得直接改寫以上公式。

---

# 11. Chip Engine

主要資料：

三大法人：

- 外資
- 投信
- 自營商

以及：

- 外資持股
- 融資
- 融券
- 借券
- 股權持股分級

可能衍生：

- 今日法人買賣超
- 3日法人累計
- 5日法人累計
- 10日法人累計
- 法人連買
- 法人連賣
- 法人加速
- 外資投信共振
- 融資增減
- 融券增減
- 券資變化
- 借券變化
- 大額持股集中度
- 籌碼趨勢

Chip Engine：

不得增加 b7、b8、b9。

不得修改 V10 六買六賣。

---

# 12. Market Engine

主要目的：

判斷個股所處市場環境。

可能資料：

- 台股大盤
- OTC
- 產業指數
- 類股
- 成交量
- 市場漲跌
- 市場廣度
- Relative Strength
- 市場共振

未來可形成：

MARKET BULLISH

MARKET NEUTRAL

MARKET BEARISH

但 Market 狀態：

不得直接覆蓋 Core Decision。

---

# 13. Position Engine

Position Engine 目前核心：

V13 Pivot Swing Fibonacci

LOCK：

lookback = 120

left = 3

right = 3

主要輸出：

- Swing High
- Swing Low
- Swing Direction
- Fib 0.236
- Fib 0.382
- Fib 0.500
- Fib 0.618
- Fib 0.786
- Fib 1.272
- Fib 1.618
- Fib Position

Position 回答：

現在價格在哪裡？

Position 不回答：

現在是否應該買進？

---

# 14. Risk Engine

Risk Engine 使用：

- Bias
- Volume Ratio
- Fib Position
- 當沖
- 融資融券
- 借券
- 市場狀態
- 波動率
- ATR
- 其他經驗證之 Risk Inputs

可能輸出：

LOW

NORMAL

ELEVATED

HIGH

RISK_LOCK

Risk Engine 不得直接改寫：

六買
六賣
Core Decision

---

# 15. Action Engine

Action Engine 與 Core Decision 分離。

禁止：

看多 = 買進

看空 = 賣出

全導通 = 自動下單

全空破 = 自動出場

Action 必須綜合：

Core Decision
+
DAVID Score
+
Position
+
Chip
+
Market
+
Risk

正式 Action Specification 完成以前：

ACTION STATE = SPEC_PENDING

---

# 16. Action State 預留

未來候選狀態：

WAIT

ENTRY_READY

ADD_READY

HOLD

REDUCE

EXIT

RISK_LOCK

以上目前只是 V14 Architecture State。

尚未正式鎖定交易規則。

不得視為自動交易指令。

---

# 17. DAVID Score

DAVID Score V1：

LOCK

DAVID Score 用途：

Ranking
+
Attention Priority

不得：

DAVID Score 高
→ 強制改變 Core Decision

未來若建立：

DAVID Score V2

必須與 V1 分離。

不得直接覆寫歷史 V1。

---

# 18. 當沖資料

FinMind 當沖資料可供：

Risk Engine
+
Chip Context

可能計算：

Day Trading Volume

Day Trading Ratio

Day Trading Trend

但：

當沖比高

不得直接等於：

賣出

只能成為 Risk Input。

---

# 19. 大戶資料

股權持股分級可以用於：

大額持股集中度

可能計算：

- 大額持股比例
- 週變化
- 集中增加
- 集中減少
- Concentration Trend

禁止將股權持股分級直接命名為：

大戶成本

因為：

Holding Concentration ≠ Cost Basis

---

# 20. VWAP 定義

若 V14 使用 VWAP：

正式名稱：

VWAP
或
市場成交均價成本線

不得在沒有證據時直接命名為：

大戶成本價

真正的大戶成本模型：

必須另外建立正式 Specification。

---

# 21. Data Adapter

所有外部資料來源：

不得直接進入 Core Formula。

必須先通過：

Data Adapter

例如：

Yahoo OHLCV
↓
Yahoo Adapter
↓
Normalized OHLCV

FinMind OHLCV
↓
FinMind Adapter
↓
Normalized OHLCV

最後兩者必須輸出：

相同 Schema。

---

# 22. Normalized OHLCV Schema

最低欄位：

timestamp

open

high

low

close

volume

必要 Metadata：

source

market

stock_id

timezone

adjustment_type

retrieved_at

V14 Engine 不應知道資料原本來自 Yahoo 或 FinMind。

Engine 只讀取：

Normalized Schema。

---

# 23. Yahoo vs FinMind 驗證

FinMind 正式取代 V14 Primary OHLCV 前：

必須執行：

Yahoo
VS
FinMind

同一：

股票
交易日
OHLCV

逐欄比較。

必須特別確認：

- Adjusted / Unadjusted
- Volume Unit
- Trading Date
- Timezone
- Corporate Action
- Missing Data
- Suspended Trading
- Price Precision

未確認前：

不得直接切換 V13 Core 資料源。

---

# 24. Supabase 定位

Supabase 是：

DAVID DATA WAREHOUSE

負責保存：

- Raw Data
- Normalized Data
- Daily Snapshot
- Historical Data
- Engine Result
- Golden Fixture
- Expected Result
- Version Metadata

Supabase 不負責：

交易決策。

---

# 25. Collector 原則

禁止設計：

Streamlit 每次 Refresh
→ 100檔
→ 每檔
→ 每個 FinMind Dataset
→ 重複大量 API Request

正確方式：

FinMind
↓
Collector
↓
Normalize
↓
Supabase
↓
Streamlit Read

日資料：

優先批次收集。

即時資料：

未來另設 Realtime Collector。

---

# 26. Cache 原則

V14 必須避免重複抓取：

已完成交易日的歷史資料。

已存在 Supabase 的資料：

若 Source Version 無變更，

優先直接讀取。

不得每次開啟 Dashboard：

重新下載全部歷史資料。

---

# 27. API Failure

如果 FinMind API Failure：

不得產生假資料。

流程：

FinMind Failure
↓
檢查 Supabase Cache
↓
如適用，Price Data 使用 Yahoo Fallback
↓
標記 Data Source
↓
標記 Data Freshness

禁止：

用 0
或
隨機值
或
前一筆資料

假裝今日真實資料。

---

# 28. Missing Data

缺少 Chip Data：

不得將：

Missing

解讀為：

Neutral

例如：

今日沒有取得外資資料

不等於：

外資買賣超 = 0

正確：

DATA_STATUS = MISSING

---

# 29. Data Freshness

每組資料必須可追蹤：

source

data_date

retrieved_at

status

必要時：

is_stale

Dashboard 未來應能區分：

LIVE

TODAY

PREVIOUS_CLOSE

STALE

MISSING

避免使用者誤把舊資料當今日資料。

---

# 30. FinMind Token 安全

FinMind Token：

SECRET

禁止：

寫入 app.py

寫入 Python Source

寫入 JSON

寫入 Markdown

寫入 Golden Fixture

Commit GitHub

公開於 Public Repository

Token 未來只能存放：

Environment Variable

Streamlit Secrets

GitHub Actions Secrets

或其他正式 Secret Manager。

---

# 31. Supabase Secret 安全

同樣禁止提交：

Supabase Service Role Key

Database Password

Private Token

任何 Secret

Public Repository 只允許：

公開 Schema
+
程式碼
+
不含秘密的測試資料

---

# 32. Golden Fixture 與外部 API

Golden Fixture 建立後：

測試執行時不得依賴：

Yahoo Live API

FinMind Live API

TWSE Live API

TPEx Live API

Golden Fixture 必須：

固定
可重現
可離線測試

---

# 33. Source of Truth

不同資料類型的 Source of Truth：

V13 Core Baseline
→ Yahoo Frozen Fixture

V14 Taiwan Market Primary
→ FinMind Normalized Data

Official Verification
→ TWSE / TPEx

Historical Storage
→ Supabase

Core Formula
→ V13_CORE_BASELINE.md

Test Rule
→ V14_TEST_PLAN.md

---

# 34. V14 第一階段資料範圍

Phase 1：

只處理：

OHLCV
+
V13 Core Baseline

目的：

證明 V14 Engine 不改變 V13 Core。

---

# 35. V14 第二階段資料範圍

Phase 2：

加入：

三大法人
外資
投信
自營商
融資融券
借券
當沖

建立：

Chip Engine
+
Risk Inputs

但仍不得修改：

V13 Core。

---

# 36. V14 第三階段資料範圍

Phase 3：

加入：

市場共振
產業強弱
Relative Strength
股權集中度
其他進階資料

建立：

Market Engine
+
Chip Enhancement
+
Risk Enhancement

---

# 37. V14 即時資料階段

Realtime 屬於獨立階段。

只有當：

Daily Engine
+
Chip Engine
+
Market Engine
+
Risk Engine

全部穩定後，

才評估：

FinMind Sponsor
或
其他正式即時行情來源。

---

# 38. 資料來源更換規則

任何 Data Provider 更換：

不得直接修改 Engine Formula。

流程：

New Provider
↓
New Adapter
↓
Normalized Schema
↓
Data Compare
↓
Baseline Test
↓
PASS
↓
才允許切換

---

# 39. V14 Data Safety Gate

任何新資料來源加入：

必須回答：

1. 資料來源是什麼？
2. Dataset 是什麼？
3. 更新頻率？
4. 單位？
5. 日期定義？
6. 缺值定義？
7. 是否 Adjusted？
8. 是否有 API Limit？
9. 是否有授權限制？
10. 保存在哪裡？
11. 進入哪個 Engine？
12. 是否影響 V13 LOCK？

如果第 12 題答案是：

YES

則：

STOP

必須先建立正式 Version Change Specification。

---

# 40. 最終原則

DAVID V14 的資料架構必須做到：

資料來源可以換

Core Formula 不亂變

資料缺失可以看見

歷史結果可以重現

每個判斷可以追溯

每個 Engine 職責清楚

Risk 與 Direction 分開

Action 與 Decision 分開

---

## DAVID V14 UNIFIED ENGINE

### DATA ARCHITECTURE RULE

DATA IS EVIDENCE

ENGINE IS LOGIC

DECISION IS DIRECTION

RISK IS CONDITION

ACTION IS A SEPARATE LAYER

---

### FINAL PROTECTION RULE

NO SOURCE DEFINITION
→ NO DATA INTEGRATION

NO NORMALIZATION
→ NO ENGINE INPUT

NO BASELINE PASS
→ NO CORE REFACTOR

NO VERIFIED ACTION SPEC
→ NO AUTOMATIC ACTION
