# DAVID V14 UNIFIED ENGINE — YAHOO / FINMIND MARKET COMPATIBILITY READINESS V1

> Gate 28D.2G — Yahoo / FinMind Market Compatibility Readiness Contract V1
>
> Parent Spec: docs/V14_DATA_SOURCE_SPEC.md
>
> Parent Contract: Gate 28D.2F — FinMind Market Semantic Evidence Contract V1
>
> Scope: Compatibility readiness only
>
> Data Compare: NOT YET EXECUTED
>
> Baseline Test: NOT YET EXECUTED
>
> Provider Switch: NOT AUTHORIZED
>
> Core Source Switch: NOT AUTHORIZED

---

# 1. Purpose

本文件定義 Yahoo Finance 與 FinMind
市場 OHLCV 資料正式相容性驗證以前，
必須滿足的 Readiness Contract。

本 Gate 不宣告：

Yahoo = FinMind

也不宣告：

FinMind 已可取代 Yahoo。

本 Gate 僅鎖定：

必須比較什麼

哪些項目仍 Pending

哪些切換仍 Blocked

---

# 2. Parent Rule

依據：

docs/V14_DATA_SOURCE_SPEC.md

FinMind 正式取代
V14 Primary OHLCV 前，

必須執行：

Yahoo
VS
FinMind

同一：

股票
交易日
OHLCV

逐欄比較。

未確認前：

不得直接切換 V13 Core 資料源。

---

# 3. Provider Change Sequence

正式流程：

New Provider
→ New Adapter
→ Normalized Schema
→ Data Compare
→ Baseline Test
→ PASS
→ Provider Switch

不得跳過任何階段。

目前狀態：

New Provider Definition = READY

Source Mapping = READY

Semantic Evidence = READY

New Adapter = NOT_READY

Normalized Output = BLOCKED

Data Compare = NOT_EXECUTED

Baseline Test = NOT_EXECUTED

Provider Switch = BLOCKED

---

# 4. Same-Stock Requirement

Yahoo 與 FinMind 比較必須使用：

SAME_STOCK_REQUIRED

不得以不同股票的 OHLCV
宣告 Provider Compatibility。

目前：

SAME_STOCK_COMPARE_STATUS
= REQUIRED_NOT_EXECUTED

---

# 5. Same-Trading-Date Requirement

Yahoo 與 FinMind 比較必須使用：

SAME_TRADING_DATE_REQUIRED

不得以不同交易日資料
宣告 Provider Compatibility。

目前：

SAME_TRADING_DATE_COMPARE_STATUS
= REQUIRED_NOT_EXECUTED

---

# 6. OHLCV Field Comparison

必須逐欄比較：

open
high
low
close
volume

目前：

OHLC_COMPARE_STATUS
= REQUIRED_NOT_EXECUTED

VOLUME_COMPARE_STATUS
= REQUIRED_NOT_EXECUTED

不得因欄位名稱相似
直接宣告相容。

---

# 7. Adjustment Compatibility

必須確認：

Adjusted / Unadjusted

Yahoo Golden Baseline：

auto_adjust = false

FinMind Adjustment Compatibility：

VALIDATION_PENDING

因此：

ADJUSTMENT_COMPATIBILITY
= PENDING

---

# 8. Volume Unit Compatibility

FinMind Trading_Volume：

Semantic Evidence
= SEMANTIC_LOCKED

Yahoo Volume：

既有 Golden Builder
直接建立 normalized volume。

但是：

Yahoo Volume Unit
尚無正式 Evidence Lock。

因此：

VOLUME_UNIT_COMPATIBILITY
= PENDING

禁止：

Yahoo Volume Unit
= FinMind Trading_Volume Unit

在正式驗證前成立。

---

# 9. Trading Date Compatibility

FinMind date：

TRADING_DATE semantic
= SEMANTIC_LOCKED

但 Provider 間：

Trading Date Compatibility
尚未執行逐日比對。

因此：

TRADING_DATE_COMPATIBILITY
= PENDING

---

# 10. Timezone Compatibility

FinMind Timezone：

TIMEZONE_PENDING

Yahoo Market Timezone：

COMPATIBILITY_PENDING

因此：

TIMEZONE_COMPATIBILITY
= PENDING

禁止使用：

generated_at_utc

推定 Market Timezone。

---

# 11. Corporate Action Compatibility

必須確認：

Corporate Action

以及：

Adjusted / Unadjusted

對 OHLCV 的影響。

目前：

CORPORATE_ACTION_COMPATIBILITY
= PENDING

---

# 12. Missing Data Compatibility

必須確認：

Yahoo Missing Data

與：

FinMind Missing / Zero Semantic

是否可安全 Normalization。

已知：

FinMind OHLC zero
不必然代表 Missing。

因此：

MISSING_DATA_COMPATIBILITY
= PENDING

ZERO_MISSING_AUTO_EQUIVALENCE
= BLOCKED

---

# 13. Suspended Trading Compatibility

必須確認：

Suspended Trading

在 Yahoo 與 FinMind
兩個 Provider 中的資料表示方式。

目前：

SUSPENDED_TRADING_COMPATIBILITY
= PENDING

---

# 14. Price Precision Compatibility

必須確認：

open
high
low
close

兩 Provider 的：

precision
rounding
representation

目前：

PRICE_PRECISION_COMPATIBILITY
= PENDING

---

# 15. Baseline Test Status

DATA_COMPARE_STATUS
= NOT_EXECUTED

BASELINE_TEST_STATUS
= NOT_EXECUTED

COMPATIBILITY_RESULT
= NOT_ESTABLISHED

不得將：

Readiness Contract PASS

解讀為：

Provider Compatibility PASS

---

# 16. V13 Lock Protection

目前：

V13_CORE_SOURCE_SWITCH
= BLOCKED

ENGINE_FORMULA_CHANGE
= BLOCKED

任何 Provider 更換：

不得直接修改 Engine Formula。

若未來變更會影響 V13 LOCK：

STOP

必須先建立正式
Version Change Specification。

---

# 17. Safety Boundary

READ_ONLY = True

ALLOW_ADAPTER_OUTPUT = False

ALLOW_NORMALIZED_OUTPUT = False

ALLOW_DATA_SOURCE_SWITCH = False

ALLOW_CORE_INPUT = False

ALLOW_ENGINE_FORMULA_CHANGE = False

ALLOW_SCORE = False

ALLOW_DECISION = False

ALLOW_SUPABASE_WRITE = False

ALLOW_PRODUCTION_WRITE = False

---

# 18. Exit Criteria

只有以下條件完成後：

Adapter Contract PASS

Normalized Schema PASS

Same Stock Compare PASS

Same Trading Date Compare PASS

OHLCV Compare PASS

Adjustment Compatibility PASS

Volume Unit Compatibility PASS

Trading Date Compatibility PASS

Timezone Compatibility PASS

Corporate Action Compatibility PASS

Missing Data Compatibility PASS

Suspended Trading Compatibility PASS

Price Precision Compatibility PASS

Baseline Test PASS

才可重新評估：

Provider Switch Authorization

在此以前：

PROVIDER SWITCH = BLOCKED

---

# 19. Next Boundary

下一階段不得直接宣告
FinMind 已可取代 Yahoo。

下一候選工作：

FINMIND MARKET SOURCE ADAPTER CONTRACT

以及後續：

YAHOO / FINMIND DATA COMPARE

BASELINE COMPATIBILITY TEST

---

# 20. Final Rule

READINESS != COMPATIBILITY

PENDING != PASS

SAME FIELD NAME != SAME SEMANTIC

NO VERIFIED ADAPTER
→ NO DATA COMPARE

NO DATA COMPARE
→ NO BASELINE PASS

NO BASELINE PASS
→ NO PROVIDER SWITCH