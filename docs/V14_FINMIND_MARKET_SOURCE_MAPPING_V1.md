# DAVID V14 UNIFIED ENGINE — FINMIND MARKET SOURCE MAPPING V1

> Gate 28D.2E — FinMind Market Source Mapping Contract V1
>
> Parent Spec: docs/V14_DATA_SOURCE_SPEC.md
>
> Dataset: TaiwanStockPrice
>
> Scope: Raw source semantics and mapping only
>
> Core Input: NOT AUTHORIZED
>
> Production Write: NOT AUTHORIZED

---

# 1. Purpose

本文件定義 FinMind TaiwanStockPrice Raw Evidence
在 DAVID V14 Unified Engine 中的市場行情來源映射邊界。

資料流程：

FinMind TaiwanStockPrice
→ Raw Market Evidence
→ Market Source Mapping
→ STOP

本 Gate 不建立 Market Score，
不修改 Core Decision，
不修改 Risk，
不修改 Action，
不執行 Supabase Write，
不授權 Production Write。

---

# 2. Parent Architecture

本 Contract 繼承：

docs/V14_DATA_SOURCE_SPEC.md

既有架構：

External Source
→ Data Adapter
→ Normalized OHLCV
→ V14 Engine

本 Gate 僅處理：

FinMind Raw Source
→ Raw Field Semantics
→ STOP

不得在本 Gate 直接建立 Normalized OHLCV。

---

# 3. Dataset Boundary

Provider:

FinMind

Dataset:

TaiwanStockPrice

目前允許：

單一股票
單一交易日
Read Only

不得：

多股票批次擴張
直接進 Core
直接產生 Score
直接產生 Decision
直接寫入 Supabase
直接寫入 Production

---

# 4. Raw Source Mapping Matrix

| Raw Field | Raw Meaning | Normalized Status |
|---|---|---|
| date | Trading date raw evidence | MAPPING_PENDING |
| stock_id | Stock identity raw evidence | IDENTITY_LOCKED |
| open | Raw open price | MAPPING_PENDING |
| max | Raw high price | MAPPING_PENDING |
| min | Raw low price | MAPPING_PENDING |
| close | Raw close price | MAPPING_PENDING |
| Trading_Volume | Raw trading volume evidence | UNIT_PENDING |

---

# 5. Raw / Normalized Boundary

RAW EVIDENCE != NORMALIZED DATA

本 Gate 不得直接宣告：

date = timestamp

open = Open

max = High

min = Low

close = Close

Trading_Volume = Volume

上述 Mapping 必須由後續
FinMind Market Source Adapter Contract
正式驗證後才可成立。

---

# 6. Volume Unit Policy

Trading_Volume：

UNIT_PENDING

禁止自行假設為：

股
張
千股
其他單位

Volume Unit 未驗證以前，
不得直接映射至 Normalized OHLCV volume。

UNKNOWN UNIT != ASSUMED UNIT

---

# 7. Trading Date / Timezone Policy

date 為 Raw Trading Date Evidence。

目前不得直接宣告：

date = normalized timestamp

原因：

Trading Date 尚需驗證。

Timezone 尚需驗證。

Normalized OHLCV 所需：

timestamp
timezone

必須由後續 Adapter Contract 處理。

---

# 8. Missing / Zero Policy

MISSING != ZERO

欄位不存在不得補 0。

Raw value = 0 必須保留為真實 Raw Evidence。

不得將 Missing Data 偽造成：

0
空字串
False
其他預設值

---

# 9. Raw / Derived Boundary

本 Gate 只允許 Raw Evidence。

不得在 Source Mapping Layer 計算：

漲跌幅
振幅
均價
量比
均線
技術指標
Score
Decision
Risk
Action

RAW EVIDENCE != DERIVED SIGNAL

---

# 10. Safety Boundary

READ_ONLY = True

ALLOW_CORE_INPUT = False

ALLOW_SCORE = False

ALLOW_DECISION = False

ALLOW_SUPABASE_WRITE = False

ALLOW_PRODUCTION_WRITE = False

ALLOW_NORMALIZED_OUTPUT = False

---

# 11. Compatibility Rule

目前 Raw Field Baseline：

date
stock_id
open
max
min
close
Trading_Volume

此 Baseline 來自既有 V14
FinMind Backend Contract
與 Controlled Live Fetch Contract
所使用的 TaiwanStockPrice Fake Evidence。

新增 Raw Field 不得自動成為必要欄位。

未知欄位不得自行推定語意或單位。

---

# 12. Fail-Closed Policy

若未來 Raw Record：

不是 Mapping

必要 Identity 缺失

Raw Field Semantic 尚未確認

Volume Unit 尚未確認

Trading Date / Timezone 尚未確認

則不得直接進入 Normalized OHLCV。

---

# 13. Next Boundary

下一候選 Gate：

FINMIND MARKET SOURCE ADAPTER V1

其責任才是：

FinMind Raw Market Evidence
→ Verified Mapping
→ Normalized OHLCV

在 Adapter Contract 完成以前：

NO CORE INPUT

NO SCORE

NO DECISION

NO SUPABASE WRITE

NO PRODUCTION WRITE

---

# 14. Final Rule

NO SOURCE DEFINITION
→ NO DATA INTEGRATION

NO VERIFIED MAPPING
→ NO NORMALIZATION

NO NORMALIZATION
→ NO CORE INPUT