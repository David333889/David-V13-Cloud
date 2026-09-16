# DAVID V14 UNIFIED ENGINE — TEST PLAN

> V14 Unified Engine 升級驗證計畫  
> 基準版本：V13.100 Cloud  
> 開發分支：develop-v14-unified  
> Core Baseline：docs/V13_CORE_BASELINE.md

---

# 1. 測試目的

V14 Unified Engine 的升級原則不是重新發明 V13 Core，
而是在保留 V13.100 核心計算結果的前提下進行模組化與功能擴充。

因此所有 Core 重構必須回答：

> 同一份輸入資料，V13 與 V14 是否得到相同的核心結果？

只要 LOCK 欄位出現非預期差異：

FAIL → STOP

不得繼續 Merge 至 main。

---

# 2. 三道測試安全門

## Gate 1 — V13 System Verify

現有：

verify_v13.py

用途：

- app.py Python compile
- daily_snapshot_v13.py Python compile
- backfill_20days_v13.py Python compile
- stock_config_v13.json 可正常讀取
- 股票數量 = 100
- 8271 market 設定檢查
- 基本環境檢查

Gate 1 不負責：

- 六買六賣結果比較
- Fib 比較
- DAVID Score 比較
- V13 vs V14 Engine 比較

結果：

PASS / FAIL

---

## Gate 2 — Golden Fixture Test

目的：

建立固定、不會隨盤中行情改變的測試資料。

固定輸入：

tests/fixtures/

固定標準答案：

tests/expected/

測試時禁止使用兩個不同時間點的即時行情作為 Core 一致性依據。

原因：

行情本身可能變化，造成假 FAIL。

---

## Gate 3 — V13 vs V14 Engine Compare

使用完全相同的 Golden Fixture：

V13 Core
VS
V14 Unified Engine

逐欄比較。

LOCK 欄位必須一致。

若不一致：

輸出差異
→ 標記 FAIL
→ 停止該次 Core 重構
→ 查明原因
→ 不得 Merge main

---

# 3. Golden Fixture 原則

Golden Fixture 必須保存固定 OHLCV 歷史資料。

最低資料欄位：

- date / timestamp
- open
- high
- low
- close
- volume

如計算需要其他欄位：

必須明確加入 Fixture Schema。

不得在測試執行時偷偷重新抓取即時行情。

---

# 4. Expected Result 原則

Expected Result 是：

V13.100 現行 Core 使用 Golden Fixture 所產生的標準答案。

一旦建立並確認：

不得因 V14 重構而直接覆寫 Expected Result。

如果真的需要修改標準答案：

必須先說明：

1. 原 V13 行為
2. 新行為
3. 修改原因
4. 影響欄位
5. 是否屬於 Bug Fix
6. 是否影響歷史可比性

確認後才允許更新 Expected Result。

---

# 5. Core 必測欄位

## Market Input

- prev_close
- open
- high
- low
- close
- volume

## Technical

- MA5
- MA20
- VM20
- MACD Histogram
- Mid
- Volume Ratio
- Bias20

## Status

- Early
- Momentum
- Cost
- Strength

## Six Buy

- b1
- b2
- b3
- b4
- b5
- b6
- BuyScore

## Six Sell

- s1
- s2
- s3
- s4
- s5
- s6
- SellScore

## Position

- Swing High
- Swing Low
- Swing Direction
- Fib 0.236
- Fib 0.382
- Fib 0.500
- Fib 0.618
- Fib 0.786
- Fib Position

## Decision

- Core Decision

## Ranking

- DAVID Score V1

---

# 6. LOCK 欄位 PASS 標準

布林值：

必須完全相同。

例如：

b1 V13 = True
b1 V14 = True

PASS

若：

b1 V13 = True
b1 V14 = False

FAIL

---

# 7. 文字狀態 PASS 標準

以下文字狀態必須完全一致：

- 強攻
- 合格
- 待定
- 放量
- 量縮
- 站穩
- 破位
- 強勢
- 弱勢
- 全導通
- 全空破
- 看多
- 看空
- 觀望

除非另有正式版本變更規格。

---

# 8. 浮點數比較原則

MA、VM、MACD、Fib、Bias 等浮點數：

不得直接依畫面四捨五入值判定。

測試應比較原始計算值。

允許極小浮點運算誤差。

Tolerance 必須集中定義，
不得不同模組各自使用不同標準。

初期建議：

ABS_TOL = 1e-8

正式值仍需依實際 V13 計算結果驗證後鎖定。

---

# 9. 邊界值測試

V14 必須特別測試以下情況。

## Boundary A

close = MA20

預期：

b2 = False

成本不得判定為站穩。

---

## Boundary B

volume = VM20

預期：

b3 = False

不得判定為正式放量。

---

## Boundary C

close = Mid

預期：

b4 = False

不得判定為強勢。

---

## Boundary D

MACD Histogram = 0

預期：

b6 = False
s6 = True

---

## Boundary E

MA5_today = MA5_previous

預期：

b5 = False
s5 = True

---

## Boundary F

BuyScore = 4

預期：

Core Decision = 看多

前提：

未先符合六賣 = 6。

---

## Boundary G

SellScore = 4

預期：

Core Decision = 看空

前提：

未先符合更高優先序條件。

---

# 10. 六買六賣非鏡像測試

必須建立專門案例驗證：

volume > VM20
AND
close < prev_close

此時：

b3 = True
s3 = True

這不是 Bug。

不得因 V14 重構將兩者改成互斥。

---

# 11. Decision Priority Test

必須驗證以下優先序：

1. BuyScore == 6 → 全導通
2. SellScore == 6 → 全空破
3. BuyScore >= 4 → 看多
4. SellScore >= 4 → 看空
5. 其他 → 觀望

測試目的：

防止未來將 Decision 改成單純比較：

BuyScore > SellScore

這不是 V13 Core 規則。

---

# 12. Pivot Fibonacci Test

至少建立：

- Bullish Swing Fixture
- Bearish Swing Fixture
- Pivot Fallback Fixture

測試：

- Swing High
- Swing Low
- Swing Direction
- 0.236
- 0.382
- 0.500
- 0.618
- 0.786
- Fib Position

不得使用 MA25 代替 Fib。

---

# 13. DAVID Score Test

DAVID Score V1 必須獨立測試。

確認：

Core Decision 與 DAVID Score 為不同輸出。

不得建立：

DAVID Score 高
→ 自動改變 Core Decision

若未來新增：

DAVID Score V2

必須與 V1 並存驗證，
不得直接覆蓋歷史 V1。

---

# 14. 測試情境

至少建立以下 Golden Test Cases：

A. 強勢多方  
B. 一般多方  
C. 多空衝突  
D. 一般空方  
E. 強勢空方  
F. Bullish Pivot Fib  
G. Bearish Pivot Fib  
H. Boundary Conditions  
I. Pivot Fallback  
J. 六買六賣非鏡像案例

---

# 15. V14 新增模組測試原則

以下屬 V14 新增：

- 三大法人
- 融資融券
- 當沖
- 借券
- 市場共振
- Relative Strength
- Risk Engine
- Action Engine

新增模組可以有自己的測試。

但不得因新增模組造成：

- V13 六買改變
- V13 六賣改變
- V13 Pivot Fib 改變
- V13 Core Decision 改變
- DAVID Score V1 被靜默改寫

---

# 16. Action Engine 測試原則

Action 與 Core Decision 分開測試。

禁止假設：

看多 = ENTRY

看空 = EXIT

Action 必須有獨立輸入、規則、Reason 與 Risk Gate。

正式 Action 規格完成前：

Action State = SPEC_PENDING

不得產生未驗證的自動買賣命令。

---

# 17. FAIL 處理流程

若 Core Compare 發生 FAIL：

1. 停止該次重構
2. 記錄欄位
3. 記錄 V13 值
4. 記錄 V14 值
5. 計算差異
6. 查明原因
7. 判斷是 Bug 或預期版本變更
8. 未確認前不得修改 Expected Result
9. 未通過前不得 Merge main

---

# 18. PASS 條件

一個 Core 模組只有在：

Gate 1 = PASS

Gate 2 = PASS

Gate 3 = PASS

才視為完成。

即：

SYSTEM OK
+
GOLDEN DATA OK
+
CORE COMPARE OK

= SAFE TO CONTINUE

注意：

PASS 不代表可以立即 Merge main。

仍需完成整體 V14 整合測試。

---

# 19. 測試資料安全

Golden Fixture：

不得包含：

- API Key
- Supabase Service Role Key
- Password
- Token
- secrets.toml
- 個人敏感資料

Public Repository 只允許提交：

可公開的固定測試資料。

---

# 20. V14 TEST GATE

流程：

V13.100
↓
verify_v13.py
↓
Gate 1 PASS
↓
Golden Fixture
↓
Gate 2 PASS
↓
V13 Core vs V14 Unified Engine
↓
Gate 3 PASS
↓
允許繼續下一個 WP

任何 Core FAIL：

STOP

---

# 21. 最終測試原則

同一資料

↓

同一公式

↓

同一結果

↓

才允許重構

V14 的新增能力應增加：

Context、Risk、Action

而不是偷偷改寫：

V13 Core。

---

## DAVID V14 UNIFIED ENGINE

### TEST PROTECTION RULE

**NO BASELINE — NO REFACTOR**

**NO PASS — NO MERGE**

先建立可重現的標準答案，
再進行 Unified Engine 重構。
