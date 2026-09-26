# DAVID V14 UNIFIED ENGINE — FINMIND MARKET SEMANTIC EVIDENCE V1

> Gate 28D.2F — FinMind Market Semantic Evidence Contract V1
>
> Parent Contract: Gate 28D.2E — FinMind Market Source Mapping Contract V1
>
> Parent Spec: docs/V14_DATA_SOURCE_SPEC.md
>
> Dataset: TaiwanStockPrice
>
> Scope: Market semantic evidence only
>
> Normalized Output: NOT AUTHORIZED
>
> Core Input: NOT AUTHORIZED
>
> Production Write: NOT AUTHORIZED

---

# 1. Purpose

本文件定義 FinMind TaiwanStockPrice
Raw Market Evidence 的語意證據狀態。

本 Gate 的責任是區分：

LOCKED EVIDENCE

與

PENDING EVIDENCE

不得將推論、經驗或既有 Yahoo 行為
直接宣告為 FinMind 正式 Mapping。

資料流程：

FinMind TaiwanStockPrice
→ Raw Market Evidence
→ Source Mapping
→ Semantic Evidence
→ STOP

---

# 2. Evidence Principles

SOURCE DOCUMENTATION != ASSUMPTION

RAW SEMANTIC != NORMALIZED MAPPING

FINMIND SEMANTIC != YAHOO COMPATIBILITY

ZERO != MISSING

TRADING DATE != NORMALIZED TIMESTAMP

GENERATED_AT_UTC != MARKET TIMEZONE

只有具有來源證據的語意才可 LOCK。

---

# 3. Trading Volume Evidence

Raw Field:

Trading_Volume

FinMind Semantic:

TRADED_SHARE_COUNT

Evidence Status:

SEMANTIC_LOCKED

說明：

FinMind TaiwanStockPrice 官方資料規格
將 Trading_Volume 定義為成交量，
官方特殊案例亦以成交股數描述該數值。

因此：

Trading_Volume 的 FinMind Raw Semantic
可鎖定為成交股數語意。

但是：

Yahoo Volume Unit Compatibility

仍為：

COMPATIBILITY_PENDING

不得僅因兩者皆稱為 Volume，
就宣告可以 1:1 直接替換。

---

# 4. Trading Date Evidence

Raw Field:

date

FinMind Semantic:

TRADING_DATE

Evidence Status:

SEMANTIC_LOCKED

date 為交易日期語意。

但是：

date != normalized timestamp

Timezone:

TIMEZONE_PENDING

目前不得直接宣告：

date
→ Asia/Taipei timestamp

也不得從其他 Fixture 的 timezone 使用方式
反推 FinMind Dataset Timezone Contract。

---

# 5. OHLC Raw Semantic Evidence

Raw Fields:

open
max
min
close

Raw Semantic:

open = raw open-price evidence

max = raw high-price evidence

min = raw low-price evidence

close = raw close-price evidence

Evidence Status:

SEMANTIC_LOCKED

但：

Normalized Mapping

仍不得在本 Gate 輸出。

---

# 6. Zero / Missing Evidence

FinMind TaiwanStockPrice
存在特殊資料語意：

OHLC value = 0

不必然等於：

Missing Data

因此：

ZERO != MISSING

Raw Zero 必須保留。

不得自動：

0 → None

0 → NaN

0 → Missing

0 → Previous Price

0 → Synthetic Price

---

# 7. No Published Price Evidence

FinMind 官方資料說明存在：

Trading_Volume > 0

但：

open = 0
max = 0
min = 0
close = 0

的可能情況。

因此：

Trading_Volume > 0

不得單獨作為：

VALID_PRICE_AVAILABLE

的判定條件。

此特殊語意必須由後續
Compatibility / Adapter Contract
明確處理。

---

# 8. Market-Specific Open Semantic

open 欄位可能具有 Market-Specific Semantic。

一般上市 / 上櫃行情
與特定市場類型的 open 語意
不得未經驗證即視為完全相同。

因此：

OPEN_SEMANTIC_SCOPE

狀態：

MARKET_SPECIFIC

後續 Adapter 不得僅依欄位名稱
假設所有市場類型具有相同 open 語意。

---

# 9. Yahoo Frozen Baseline Evidence

V13.100 Golden Fixture：

source = Yahoo Finance

source_type = frozen_historical_ohlcv

market = TW

interval = 1d

auto_adjust = false

Normalized Fixture Columns：

timestamp
open
high
low
close
volume

Yahoo raw Volume
在既有 Golden Builder 中
直接轉換為 normalized volume，
未執行倍率轉換。

但是現有 Fixture Metadata
未宣告 Yahoo Volume Unit。

因此：

YAHOO_VOLUME_UNIT

狀態：

COMPATIBILITY_PENDING

不得以數值大小
推定單位。

---

# 10. Yahoo Time Evidence

Golden Fixture Metadata：

generated_at_utc

只代表 Fixture 產生時間。

不得解讀為：

Yahoo Market Data Timezone

因此：

YAHOO_MARKET_TIMEZONE

狀態：

COMPATIBILITY_PENDING

---

# 11. Compatibility Status

FinMind Trading_Volume Semantic:

SEMANTIC_LOCKED

Yahoo Volume Unit:

COMPATIBILITY_PENDING

FinMind Trading Date Semantic:

SEMANTIC_LOCKED

FinMind Timezone:

TIMEZONE_PENDING

Yahoo Market Timezone:

COMPATIBILITY_PENDING

Normalized Volume Mapping:

BLOCKED

Normalized Timestamp Mapping:

BLOCKED

---

# 12. Safety Boundary

READ_ONLY = True

ALLOW_NORMALIZED_OUTPUT = False

ALLOW_CORE_INPUT = False

ALLOW_SCORE = False

ALLOW_DECISION = False

ALLOW_SUPABASE_WRITE = False

ALLOW_PRODUCTION_WRITE = False

---

# 13. Prohibited Assumptions

禁止：

Trading_Volume = normalized Volume

date = normalized timestamp

date timezone = Asia/Taipei

Yahoo Volume Unit = FinMind Volume Unit

generated_at_utc = Market Timezone

Trading_Volume > 0 = Valid Price Available

OHLC zero = Missing

所有上述關係必須由後續
Compatibility / Adapter Contract
正式驗證。

---

# 14. Next Boundary

下一候選 Gate：

FINMIND / YAHOO MARKET COMPATIBILITY CONTRACT V1

或：

FINMIND MARKET SOURCE ADAPTER CONTRACT V1

但只有在必要 Semantic / Unit / Date
Compatibility 足夠後，
才可開放 Normalized Output。

---

# 15. Final Rule

EVIDENCE BEFORE MAPPING

SEMANTIC BEFORE NORMALIZATION

UNKNOWN != ASSUMED

PENDING != LOCKED

NO VERIFIED COMPATIBILITY
→ NO NORMALIZED OUTPUT

NO NORMALIZED OUTPUT
→ NO CORE INPUT