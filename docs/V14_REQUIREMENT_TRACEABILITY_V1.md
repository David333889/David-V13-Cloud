# DAVID V14 UNIFIED ENGINE — REQUIREMENT TRACEABILITY V1

> Gate 21 — Unified Specification Coverage & Shadow Readiness
>
> Baseline: Gate 20 — App Shadow Dry-Run Wiring V1
>
> Protected Baseline: d169f9e197b4d3705372c1673777b17c7d058b48
>
> Regression Baseline: 18-Layer PASS
>
> Shadow Default: OFF
>
> Production Write: NOT AUTHORIZED

---

# 1. 文件目的

本文件建立 DAVID V14 Unified Engine 的正式需求追溯基準。

追溯關係：

Original Requirement
→ Six-System Architecture
→ WP1~WP7
→ V14 Module
→ Comparator
→ Regression Layer
→ Gate / Commit
→ Engineering Status
→ Gap Type
→ Next Action

本文件不以「存在 Python 模組」直接判定需求完成。

Regression PASS 代表已定義 Contract 通過驗證，
不代表 Master Specification 所有需求均已完成。

---

# 2. Engineering Status

- VERIFIED：已有 Implementation + Comparator / Regression 證據。
- PARTIAL VERIFIED：已有正式實作，但未覆蓋 Master Specification 全部需求。
- SPEC GAP：需求存在，但公式或門檻尚未正式鎖定。
- DATA GAP：缺少可靠資料來源或 Normalized Data。
- IMPLEMENTATION GAP：規格已存在，但程式尚未完整實作。
- VALIDATION GAP：需歷史資料、Backtest 或門檻驗證。
- UI GAP：屬顯示層問題，不代表 Engine 缺失。
- NOT STARTED：目前無足夠工程證據證明已開始。

---

# 3. Architecture Protection Rules

DATA IS EVIDENCE.

ENGINE IS LOGIC.

DECISION IS DIRECTION.

RISK IS CONDITION.

ACTION IS A SEPARATE LAYER.

NO SOURCE DEFINITION → NO DATA INTEGRATION.

NO NORMALIZATION → NO ENGINE INPUT.

NO BASELINE PASS → NO CORE REFACTOR.

NO VERIFIED ACTION SPEC → NO AUTOMATIC ACTION.

NO PASS → NO MERGE.

---

# 4. Six-System Coverage

| System | V14 Status | Evidence |
|---|---|---|
| A Technical | VERIFIED | Technical / Status / Six Buy / Six Sell / Core Decision |
| B Chip | DATA GAP / NOT STARTED | Foreign / Trust / Dealer / Margin / Short / Lending / Day Trade not integrated |
| C Market | DATA GAP / NOT STARTED | Benchmark / Industry / Group / Relative Strength not integrated |
| D Position | VERIFIED | Pivot Swing Fibonacci Engine |
| E Risk | PARTIAL VERIFIED | R1 Bias / R2 Position / R3 Conflict / R4 Decision-Position / R5 Volume-Price |
| F Action | PARTIAL VERIFIED | WAIT / ENTER_ALLOWED / REDUCE_BIAS / EXIT_BIAS / BLOCKED |
| DAVID Ranking | VERIFIED | V13.100 DAVID Score V1 migration |

---

# 5. WP Coverage

| WP | Scope | Status |
|---|---|---|
| WP1 | Core Clean | LARGELY VERIFIED / remaining specification gaps |
| WP2 | Data Dictionary / Source Contract | SOURCE SPEC VERIFIED / Integration PARTIAL |
| WP3 | Chip Data | DATA GAP |
| WP4 | Market Context | DATA GAP |
| WP5 | Risk Spec | PARTIAL VERIFIED |
| WP6 | Action Spec | PARTIAL VERIFIED |
| WP7 | Backtest | VALIDATION GAP |

---

# 6. 30-Requirement Traceability

| # | Requirement | WP | Status | Gap / Note |
|---|---|---|---|---|
| 01 | Data Source Unification | WP2 | PARTIAL VERIFIED | Source Spec exists; multi-source integration incomplete |
| 02 | MA20 / MA25 Conflict | WP1 | VERIFIED / PARTIAL | MA20 Core verified; remaining MA25 uses require cleanup |
| 03 | Volume Ratio Fixed Value | WP1 | VERIFIED | VM20 real calculation |
| 04 | Early Session Star Rating | WP1 | PARTIAL VERIFIED | Strong/Qualified/Pending verified; star rating remains SPEC GAP |
| 05 | V13 Momentum / S13 Naming | WP1 | PARTIAL VERIFIED | V13 volume momentum verified; S13 acceleration separate SPEC GAP |
| 06 | Cost Concept Mixing | WP1 | PARTIAL VERIFIED | MA20 verified; VWAP / institutional cost not integrated |
| 07 | Six Buy / Six Sell Non-Mirror | WP1 | VERIFIED | s3 is not inverse of b3; MACD=0 belongs to s6 |
| 08 | Buy/Sell Conflict | WP5 | VERIFIED V1 | R3 Conflict implemented |
| 09 | MA25 Mislabelled Fib | WP1 | VERIFIED | Pivot Swing Fib Engine |
| 10 | Monitoring Fib Levels | WP1 | VERIFIED | Unified 0.236/0.382/0.500/0.618/0.786 + extensions |
| 11 | S1~S13 Fixed Values | WP1 | GAP | SPEC / IMPLEMENTATION GAP |
| 12 | Step1~3 No Formula | WP6 | PARTIAL VERIFIED | Replaced by Action V1 architecture; final spec incomplete |
| 13 | Win Rate Without Backtest | WP7 | VALIDATION GAP | Backtest required |
| 14 | Institutional Fixed Values | WP3 | DATA GAP | Real data required |
| 15 | Margin / Short Missing | WP3 | DATA GAP | Not integrated |
| 16 | Day Trading Missing | WP3 | DATA GAP | Not integrated |
| 17 | Securities Lending Missing | WP3 | DATA GAP | Not integrated |
| 18 | Institutions Only Aggregated | WP3 | DATA / SPEC GAP | Foreign / Trust / Dealer must remain separate |
| 19 | Dealer Hedge Not Separated | WP3 | DATA GAP | Proprietary / hedge separation required |
| 20 | Price × Margin × Short | WP3/WP7 | DATA + VALIDATION GAP | Historical validation required |
| 21 | Market Benchmark Fixed | WP4 | DATA / IMPLEMENTATION GAP | Benchmark Engine required |
| 22 | Group Resonance Fixed | WP4 | DATA / IMPLEMENTATION GAP | Breadth / group model required |
| 23 | Relative Strength Fixed | WP4 | IMPLEMENTATION GAP | Stock vs benchmark/group required |
| 24 | Six-Level Concepts Mixed | WP1/WP5 | PARTIAL VERIFIED | Pivot Fib verified; trend/cost/volatility/range separation incomplete |
| 25 | Rocket / Warning Role | UI/Risk | SPEC / UI GAP | Must remain context/risk display |
| 26 | Valuation Fixed | Data | DATA / SPEC GAP | Fundamental source and comparison baseline required |
| 27 | Entry Specification | WP6 | PARTIAL VERIFIED | ENTER_ALLOWED V1 exists; final ENTRY spec incomplete |
| 28 | Add/Hold/Reduce/Exit | WP6 | PARTIAL VERIFIED | Reduce/Exit V1; ADD/HOLD incomplete |
| 29 | Risk Lock | WP5 | PARTIAL VERIFIED | CLEAR/CAUTION V1; complete lock requires Chip/Market inputs |
| 30 | Table / Label Accumulation | UI/Pine | UI GAP | Not Unified Core priority |

---

# 7. Verified V14 Core Domains

Technical:
- MA20
- VM20
- MA5
- MACD Histogram
- Volume Ratio
- Bias20
- Mid

Status:
- Early
- Momentum
- Cost
- Strength

Six Buy:
- b1 ~ b6

Six Sell:
- s1 ~ s6
- s3 non-mirror rule preserved
- MACD == 0 → s6

Position:
- Pivot High / Low
- Lookback 120
- left=3 / right=3
- Swing Direction
- Fib 0.236 / 0.382 / 0.500 / 0.618 / 0.786
- Extension 1.272 / 1.618

Ranking:
- DAVID Score V1
- Risk / Action do not overwrite DAVID Score

---

# 8. Risk V1 Coverage

Implemented:

R1_BIAS

R2_POSITION

R3_CONFLICT

R4_DECISION_POSITION

R5_VOLUME_PRICE

Risk outputs currently include:

- state
- level
- lock
- CLEAR / CAUTION

Remaining Master-Spec gaps:

- Chip Divergence
- Market Headwind
- Day-Trade Overheat
- Full Risk Lock validation

Therefore:

RISK V1 = PARTIAL VERIFIED.

---

# 9. Action V1 Coverage

Current Action outputs include:

- WAIT
- ENTER_ALLOWED
- REDUCE_BIAS
- EXIT_BIAS
- BLOCKED

Protection order includes:

P0 Contract Validity

P1 Risk Readiness

P2 High Risk Guard

P3 Neutral → WAIT

P4 Bullish Path

P5 Bearish Path

P6 Unsupported Decision → BLOCKED

Remaining Master-Spec targets:

- ENTRY final specification
- ADD
- HOLD
- REDUCE final specification
- EXIT final specification

Therefore:

ACTION V1 = PARTIAL VERIFIED.

---

# 10. Gate / Commit Traceability

Key evolution:

- Gate 3 — Core Baseline
- Gate 4 — Risk Engine V1
- Gate 5 — Action Engine V1
- Gate 6 — Consumer Boundary
- Integration Payload V1
- Storage Record V1
- Supabase Persistence Adapter V1
- Supabase Schema Migration V1
- Supabase Writer V1
- Gate 16 — Runtime Pipeline V1
- Gate 17 — Runtime Writer Wiring V1
- Gate 18 — App Market Input Adapter V1
- Gate 19 — App Dry-Run Pipeline V1
- Gate 20 — App Shadow Dry-Run Wiring V1

Current Protected Baseline:

d169f9e197b4d3705372c1673777b17c7d058b48

Current Regression Baseline:

18-Layer PASS

---

# 11. Shadow Readiness

VERIFIED:

- Shadow OFF → zero dry-run calls
- Shadow ON → exactly one dry-run call
- Input passthrough preserved
- Exception isolation
- App wiring comparator PASS
- 18-Layer Regression PASS
- Local SHA = Remote SHA
- Post-Push Regression PASS
- Working Tree Clean

NOT YET VERIFIED:

- Controlled-ON real App observation
- Long-running READY / BLOCKED behavior
- Production Writer activation

Current policy:

SHADOW DEFAULT = OFF

PRODUCTION WRITE = NOT AUTHORIZED

---

# 12. Development Priority

Priority 0:
Protect Gate 20 baseline.

Priority 1:
Complete Data Contract / Dictionary.

Priority 2:
WP3 Chip Data Foundation.

Priority 3:
WP4 Market Context.

Priority 4:
Risk V2.

Priority 5:
Action V2.

Priority 6:
Backtest / Validation.

Production Write evaluation occurs only after required safety and data gates are satisfied.

---

# 13. Gate 22 Candidate Entry Direction

Candidate:

Gate 22 — Unified Data Contract & Chip Schema V1

Initial scope:

Raw Chip Fixture
→ Validation
→ Normalization
→ ChipDataResult
→ STOP

No trading decision.

No Action modification.

No Production Write.

Real external data integration should follow only after the schema and Golden Fixture are verified.

---

# 14. Gate 21 Conclusion

Gate 21 establishes specification coverage and development priority.

It does not authorize Production Write.

It does not modify V13 locked Core behavior.

It does not declare incomplete Chip / Market / Risk / Action / Backtest requirements complete.

The next development gate must preserve:

DATA → ENGINE → DECISION → RISK → ACTION

as separate responsibilities.
