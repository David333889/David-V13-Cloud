# DAVID V13 CORE BASELINE

> V14 Unified Engine 升級施工基準  
> 基準版本：V13.100 Cloud  
> 基準分支來源：main  
> 開發分支：develop-v14-unified  
> 建立目的：保護 V13 Core，作為 V14 升級前後結果比對基準。

---

## 1. 核心原則

V14 Unified Engine 採「保留核心、分層擴充」原則。

V13 已確認之核心公式不得因新增：

- 三大法人
- 融資融券
- 當沖
- 借券
- 大盤
- 產業
- 族群
- Risk Engine
- Action Engine

而直接修改原始六買六賣與 Core Decision。

---

# 2. V13 CORE LOCK

## 2.1 MA20

公式：

MA20 = 最近 20 期收盤價平均

用途：

- 成本判斷
- 六買 b2
- 六賣 s2
- 乖離計算
- DAVID Score 部分計算

狀態：LOCK

---

## 2.2 VM20

公式：

VM20 = 最近 20 期成交量平均

用途：

- 量比
- 動能
- 六買 b3
- 六賣 s3

狀態：LOCK

---

## 2.3 量比

公式：

Volume Ratio = 今日成交量 / VM20

判斷原則：

- 今日量 > VM20：正式「放量」條件
- 量比 > 1.5x：可作 UI 視覺強調
- 1.5x 不取代 1.0x 的核心放量條件

狀態：LOCK

---

## 2.4 MA20 乖離

公式：

Bias20 = (現價 - MA20) / MA20 × 100%

用途：

- 顯示現價與 MA20 距離
- DAVID Score 過熱修正
- 未來 Risk Engine 追價風險參考

注意：

乖離本身不直接取代六買六賣。

狀態：LOCK

---

# 3. 早盤／動能／成本／力道

## 3.1 早盤

判斷順序：

1. 漲跌幅 >= +3.0% → 強攻
2. 否則，現價 > 開盤 → 合格
3. 其他 → 待定

注意：

+3.0% 為第一優先。

狀態：LOCK

---

## 3.2 動能

今日成交量 > VM20：

放量

其他：

量縮

注意：

「放量」描述量能狀態，本身不代表價格一定上漲。

狀態：LOCK

---

## 3.3 成本

現價 > MA20：

站穩

其他：

破位

邊界條件：

現價 = MA20 時，不屬於「站穩」。

狀態：LOCK

---

## 3.4 力道

日內中線：

Mid = (今日最高價 + 今日最低價) / 2

現價 > Mid：

強勢

其他：

弱勢

狀態：LOCK

---

# 4. 六買 V10

六買是六個多方證據開關，不等同六個獨立買進命令。

## b1

現價 > 開盤

## b2

現價 > MA20

## b3

今日成交量 > VM20

## b4

現價 > 日內中線 Mid

## b5

MA5 今日值 > MA5 前值

## b6

MACD Histogram > 0

計算：

BuyScore = b1 + b2 + b3 + b4 + b5 + b6

範圍：

0 ～ 6

狀態：CORE LOCK

---

# 5. 六賣 V10

## s1

現價 < 開盤

## s2

現價 < MA20

## s3

今日成交量 > VM20  
AND  
現價 < 昨收

## s4

現價 < 日內中線 Mid

## s5

MA5 今日沒有向上

亦即：

MA5 今日值 <= MA5 前值

## s6

MACD Histogram <= 0

計算：

SellScore = s1 + s2 + s3 + s4 + s5 + s6

範圍：

0 ～ 6

---

## 5.1 重要非鏡像規則

b3：

今日成交量 > VM20

s3：

今日成交量 > VM20  
AND  
現價 < 昨收

因此：

b3 與 s3 並非互斥鏡像。

不得在 V14 重構時改成：

s3 = NOT b3

狀態：CORE LOCK

---

# 6. V10 CORE DECISION

判斷優先順序：

1. 六買 = 6 → 全導通
2. 六賣 = 6 → 全空破
3. 六買 >= 4 → 看多
4. 六賣 >= 4 → 看空
5. 其他 → 觀望

注意：

判斷順序本身也是規格的一部分。

不得任意調換。

狀態：CORE LOCK

---

# 7. Pivot Swing Fibonacci

V13 Pivot Swing Fibonacci 為正式位置引擎。

基準參數：

- Lookback = 120
- Left = 3
- Right = 3

方向：

最近有效 Swing Low 發生於 Swing High 之前：

多頭 Swing

最近有效 Swing High 發生於 Swing Low 之前：

空頭 Swing

若找不到有效 Pivot：

使用區間 High / Low 作 fallback。

主要 Fib：

- 0.236
- 0.382
- 0.500
- 0.618
- 0.786
- 1.272
- 1.618

狀態：CORE LOCK

---

## 7.1 Fib 統一原則

TradingView、GitHub Web、Mobile 與未來監控水位：

必須使用同一套 Unified Pivot Fib 結果。

不得另外建立第二套不同 Fib 公式。

MA25 不得標示為「Fib 支撐」。

---

# 8. DAVID SCORE V1

DAVID Score 為 V13 現行掃描與排名系統。

主要用途：

100 檔股票掃描與優先排序。

重要原則：

DAVID Score ≠ Core Decision

DAVID Score ≠ Fib Position

DAVID Score ≠ Risk

DAVID Score ≠ Action

現行 V13 DAVID Score 公式列為：

LOCK V1

若未來加入：

- 法人
- 融資融券
- 當沖
- 市場共振
- Risk

應建立新版 Score 並先進行歷史驗證，不直接覆蓋 V1。

---

# 9. V14 六大系統

V14 Unified Engine 採六大系統：

1. 技術面 Technical
2. 籌碼面 Chip
3. 市場面 Market
4. 位置面 Position
5. 風險面 Risk
6. Action

其中：

V13 Core 為技術核心基準。

新增系統不得直接破壞 V13 Core。

---

# 10. V14 新增資料

以下屬 V14 新增／待規格化：

## 籌碼面

- 外資
- 投信
- 自營商
- 融資
- 融券
- 借券
- 當沖

## 市場面

- 加權指數
- 櫃買指數
- 產業
- 族群
- 相對強弱
- 市場共振

## 風險面

- 追價風險
- 多空衝突
- 技術籌碼背離
- 市場逆風
- 當沖過熱
- Risk Lock

## Action

- WAIT
- ENTRY_READY
- ADD_READY
- HOLD
- REDUCE
- EXIT
- RISK_LOCK

上述項目在正式公式與驗證完成以前：

不得偽裝成已驗證的自動買進／賣出命令。

---

# 11. V168 整合原則

V168 定位：

K 線視覺戰術層。

S1～S13 定位：

戰況確認層。

不得取代：

V13 六買六賣 Core Decision。

已知改善：

- 固定數值改為真實計算
- MA25 不再冒充 Fib
- 監控水位改讀 Unified Pivot Fib
- 勝率未經 Backtest 前不得作正式勝率
- 法人／籌碼不得使用固定假數據

---

# 12. V14 Action 原則

Core Decision 回答：

「目前技術證據方向為何？」

Position 回答：

「目前價格位於何處？」

Risk 回答：

「目前風險為何？」

Action 回答：

「下一步狀態為何？」

因此：

看多 ≠ 自動買進

看空 ≠ 自動賣出

Action 必須等待獨立規格與歷史驗證。

---

# 13. V14 升級安全規則

1. main 為 V13.100 正式穩定版。
2. V14 開發只在 develop-v14-unified 進行。
3. Golden Backup 第一階段不得修改。
4. Supabase 現有正式資料不得破壞。
5. Secrets / API Key 不得 Commit 至 Public Repository。
6. app.py 不一次全面重寫。
7. 每次只修改一個可驗證模組。
8. 修改前後必須比對 Core Baseline。
9. Core 結果不同時停止升級並查明原因。
10. 完整測試成功後才允許 Merge 至 main。

---

# 14. V13 → V14 驗證欄位

每次 Core 重構至少比對：

- 股票代碼
- 股票名稱
- 日期／時間
- 昨收
- 開盤
- 現價
- 最高
- 最低
- 成交量
- MA5
- MA20
- VM20
- MACD Histogram
- 量比
- 乖離
- 早盤
- 動能
- 成本
- 力道
- b1～b6
- s1～s6
- 六買
- 六賣
- Swing High
- Swing Low
- Swing Direction
- Fib Position
- Core Decision
- DAVID Score

---

# 15. 最終架構原則

方向 ≠ 位置

位置 ≠ 風險

風險 ≠ 行動

行動 ≠ 排名

Core Decision ≠ DAVID Score

所有結果必須能回溯至：

原始資料 → 計算公式 → 狀態 → Decision / Position / Risk / Action

---

## DAVID V14 UNIFIED ENGINE

### CORE PROTECTION RULE

**同一資料、同一公式、同一 Engine。**

V14 的目的不是推翻 V13，而是在保留 V13 Core 的前提下，增加籌碼、市場、位置、風險與 Action 的完整決策架構。
