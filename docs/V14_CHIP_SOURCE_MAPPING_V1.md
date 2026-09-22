# DAVID V14 UNIFIED ENGINE — CHIP SOURCE MAPPING V1

> Gate 23 — Chip Source Mapping & Unit Contract V1
>
> Parent Contract: Gate 22 — Normalized Chip Data Contract V1
>
> Protected Input Baseline: 71d61eac4ae72b4344e5c945e9458a4a7d37b97a
>
> Scope: Source semantics and mapping only
>
> Production Write: NOT AUTHORIZED

---

# 1. Purpose

本文件定義 DAVID V14 Unified Engine 籌碼資料的來源映射與資料語意。

資料流程：

Official Source
→ Raw Dataset
→ Source Mapping
→ Normalized Chip Data Contract
→ STOP

本文件不建立 Chip Score，
不修改 Core Decision，
不修改 Risk，
不修改 Action，
不授權 Production Write。

---

# 2. Protection Rules

UNKNOWN UNIT != ASSUMED UNIT

MISSING != ZERO

RAW EVIDENCE != DERIVED SIGNAL

Legacy Dealer != Missing

Lending transaction volume != Lending balance

Raw source field 必須先確認 Dataset、欄位意義與資料分類，
才可映射至 Gate 22 Normalized Chip Contract。

尚未由來源規格確認的單位一律標記 UNIT_PENDING，
不得依經驗自行假設為股、張、千股或其他單位。

---

# 3. Source Mapping Matrix

| Domain | Dataset | Raw Field / Category | Meaning | Unit Status | Normalized Target | Status |
|---|---|---|---|---|---|---|
| Foreign | TaiwanStockInstitutionalInvestorsBuySell | Foreign_Investor + buy/sell | 外資買進/賣出 Raw Evidence | UNIT_PENDING | institutional.foreign | LOCKED |
| Investment Trust | TaiwanStockInstitutionalInvestorsBuySell | Investment_Trust + buy/sell | 投信買進/賣出 Raw Evidence | UNIT_PENDING | institutional.investment_trust | LOCKED |
| Dealer Legacy | TaiwanStockInstitutionalInvestorsBuySell | Dealer + buy/sell | 舊制自營商 Raw Evidence | UNIT_PENDING | Historical Compatibility | LOCKED |
| Dealer Self | TaiwanStockInstitutionalInvestorsBuySell | Dealer_self + buy/sell | 自營商自行買賣 Raw Evidence | UNIT_PENDING | institutional.dealer_self | LOCKED |
| Dealer Hedging | TaiwanStockInstitutionalInvestorsBuySell | Dealer_Hedging + buy/sell | 自營商避險 Raw Evidence | UNIT_PENDING | institutional.dealer_hedging | LOCKED |
| Foreign Dealer Self | TaiwanStockInstitutionalInvestorsBuySell | Foreign_Dealer_Self + buy/sell | 外資自營商 Raw Evidence | UNIT_PENDING | Historical Compatibility | LOCKED |
| Margin | TaiwanStockMarginPurchaseShortSale | MarginPurchase* | 融資 Raw Evidence | UNIT_PENDING | financing.margin | FIELD_LOCKED |
| Short | TaiwanStockMarginPurchaseShortSale | ShortSale* | 融券 Raw Evidence | UNIT_PENDING | financing.short | FIELD_LOCKED |
| Offset | TaiwanStockMarginPurchaseShortSale | OffsetLoanAndShort | 資券互抵 Raw Evidence | UNIT_PENDING | financing.offset_loan_and_short | FIELD_LOCKED |
| Lending | TaiwanStockSecuritiesLending | transaction_type / volume / fee_rate | 借券成交明細 | UNIT_PENDING | securities_lending | LOCKED |
| Day Trading | TaiwanStockDayTrading | Volume / BuyAmount / SellAmount / BuyAfterSale | 當沖 Raw Evidence | PARTIAL_UNIT_LOCK | day_trade | LOCKED |

---

# 4. Institutional Investors

Official Dataset:

TaiwanStockInstitutionalInvestorsBuySell

Core Raw Fields:

- date
- stock_id
- buy
- sell
- name

Institutional categories:

- Foreign_Investor
- Investment_Trust
- Dealer
- Dealer_self
- Dealer_Hedging
- Foreign_Dealer_Self

Gate 23 保留 buy / sell Raw Evidence。

法人淨買賣超屬 Derived Metric，
不得由 Source Mapping Layer 取代原始 buy / sell。

---

# 5. Historical Compatibility

法人分類具有歷史相容性問題。

Legacy Dealer != Missing

舊資料中的 Dealer 不得因新制已有 Dealer_self / Dealer_Hedging，
就被判定為缺值。

Dealer_self 與 Dealer_Hedging 必須保持可區分。

Foreign_Dealer_Self 亦不得因特定日期不存在，
直接被偽造為其他法人分類。

Historical Compatibility 的處理責任屬後續 Source Adapter，
不得在 Source Mapping 階段任意合併或補值。

---

# 6. Margin / Short

Official Dataset:

TaiwanStockMarginPurchaseShortSale

Margin Raw Fields:

- MarginPurchaseBuy
- MarginPurchaseCashRepayment
- MarginPurchaseLimit
- MarginPurchaseSell
- MarginPurchaseTodayBalance
- MarginPurchaseYesterdayBalance

Short Raw Fields:

- ShortSaleBuy
- ShortSaleCashRepayment
- ShortSaleLimit
- ShortSaleSell
- ShortSaleTodayBalance
- ShortSaleYesterdayBalance

Additional Raw Field:

- OffsetLoanAndShort

Gate 23 狀態：

FIELD_LOCKED

Unit 狀態：

UNIT_PENDING

在 Unit Contract 正式驗證前，
不得自行將數值宣告為股、張、千股或其他單位。

---

# 7. Securities Lending

Official Dataset:

TaiwanStockSecuritiesLending

Raw Fields:

- date
- stock_id
- transaction_type
- volume
- fee_rate
- close
- original_return_date
- original_lending_period

資料語意：

Securities Lending 在此 Dataset 中為借券成交明細 Evidence。

Lending transaction volume != Lending balance

因此 Source Adapter 不得將 transaction volume 重新命名為 lending balance。

借券增加、借券減少、借券趨勢均屬 Derived Metric。

---

# 8. Day Trading

Official Dataset:

TaiwanStockDayTrading

Raw Fields:

- stock_id
- date
- BuyAfterSale
- Volume
- BuyAmount
- SellAmount

資料語意：

Volume 為 Raw Volume Evidence。

BuyAmount / SellAmount 為 Raw Amount Evidence。

BuyAfterSale 為資料來源提供之資格/狀態 Evidence，
不得直接解讀為交易強弱訊號。

當沖比率、5日當沖均值、當沖過熱均屬 Derived Metric。

---

# 9. Unit Policy

Unit Contract 採 Fail-Closed 原則。

UNKNOWN UNIT != ASSUMED UNIT

目前未取得足夠來源證據之欄位：

UNIT_STATUS = PARTIAL

其 Raw Value 可以保存，
但不得在需要單位語意的 Derived Engine 中直接使用。

任何 Unit 升級為 LOCKED，
必須留下來源與驗證證據。

---

# 10. Freshness

所有 Chip Evidence 必須可追蹤：

- trade_date
- source
- freshness
- status
- missing_fields

Source 已回傳資料，不代表資料必然 Final。

Freshness 必須與 Missing 分離。

可能狀態概念：

- READY
- MISSING
- STALE
- PRELIMINARY
- FINAL

實際 Adapter Contract 應由後續 Gate 正式鎖定。

---

# 11. Raw / Derived Boundary

以下屬 Raw Evidence：

- institutional buy / sell
- margin raw fields
- short raw fields
- OffsetLoanAndShort
- securities-lending transaction evidence
- day-trading Volume / BuyAmount / SellAmount / BuyAfterSale

以下屬 Derived，Gate 23 不計算：

- institutional net buy/sell
- 3-day institutional accumulation
- 5-day institutional accumulation
- 10-day institutional accumulation
- institutional consecutive buy/sell
- institutional acceleration
- foreign / investment-trust resonance
- margin change
- short change
- margin-short relationship
- securities-lending trend
- day-trade ratio
- day-trade moving average
- day-trade overheat
- chip score

RAW EVIDENCE != DERIVED SIGNAL

---

# 12. Missing Policy

MISSING != ZERO

資料來源未回傳某欄位時：

不得補 0。

不得使用隨機值。

不得使用前一筆資料假裝今日資料。

不得將 Missing 解讀為 Neutral。

應保留：

status = MISSING

並將欄位加入 missing_fields。

真實來源明確回傳 0 時，
0 才是有效 Raw Evidence。

---

# 13. Gate 22 Mapping Target

Gate 23 Source Mapping 的下游目標為：

Normalized Chip Data Contract V1

Target blocks:

- identity
- institutional
- financing
- securities_lending
- day_trade
- metadata

Gate 23 不修改 Gate 22 Contract。

Gate 23 不修改六買六賣。

Gate 23 不修改 Core Decision。

Gate 23 不修改 Risk。

Gate 23 不修改 Action。

---

# 14. Gate 23 Boundary

Gate 23 is Source Mapping only.

No FinMind live API integration.

No Supabase write.

No Production Write.

No Chip Score.

No Risk V2.

No Action V2.

No automatic trading action.

PRODUCTION_WRITE = NOT_AUTHORIZED

---

# 15. Gate 23 Conclusion

Gate 23 建立 Chip Source Mapping 與 Unit Contract 的資料治理基準。

已確認之 Dataset / Raw Field / Meaning 可標記 LOCKED 或 FIELD_LOCKED。

未有充分來源證據之 Unit 維持 UNIT_PENDING。

後續 Source Adapter 必須遵守：

UNKNOWN UNIT != ASSUMED UNIT

MISSING != ZERO

RAW EVIDENCE != DERIVED SIGNAL

Legacy Dealer != Missing

Lending transaction volume != Lending balance
