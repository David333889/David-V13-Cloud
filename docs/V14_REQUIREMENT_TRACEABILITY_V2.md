# DAVID V14 UNIFIED ENGINE — REQUIREMENT TRACEABILITY V2

> Current Requirement / WP / Gate Reconciliation V2
>
> Previous Requirement Baseline: Gate 21 / V14_REQUIREMENT_TRACEABILITY_V1.md
>
> Current Protected Engineering Baseline: Gate 28D.2K-3L
>
> Protected Commit: 3cbb3bb32fe7ccee89e7121b573fece768aa94ef
>
> Safety Tag: v14-gate-28d2k-3l-protected-runtime-semantic-golden-safe
>
> Full V14 Regression: PASS
>
> E2E - FULL CORE WIRING: PASS
>
> Production Write: NOT AUTHORIZED

---

# 1. Purpose

本文件更新 DAVID V14 Unified Engine 的正式需求追溯狀態。

V1 建立於 Gate 21 時點。
其 Requirement / WP 架構仍保留為 Master Requirement Baseline，
但工程實作已由 Gate 22 持續推進至 Gate 28D.2K-3L。

本 V2 不刪除或覆寫 V1。

V2 的目的為：

Original Requirement
→ WP1~WP7
→ Specification
→ Source / Evidence
→ V14 Module
→ Comparator / Contract
→ Regression
→ Gate / Protected Commit
→ Current Engineering Status
→ Remaining Gap
→ Next Action

重要原則：

存在 Python Module
!= Requirement Complete

Regression PASS
!= Master Specification Complete

Protected Safety Node
!= Downstream Authority Authorization

---

# 2. Engineering Status Definitions

沿用 V1：

- VERIFIED
  Implementation + Comparator / Regression evidence exists.

- PARTIAL VERIFIED
  Formal engineering evidence exists, but Master Specification
  coverage is incomplete.

- SPEC GAP
  Requirement exists, but formula / threshold / formal contract
  is not locked.

- DATA GAP
  Reliable source / evidence / normalized data remains incomplete.

- IMPLEMENTATION GAP
  Specification exists, but implementation is incomplete.

- VALIDATION GAP
  Historical data / backtest / threshold validation is required.

- UI GAP
  Display-layer gap; does not imply Engine gap.

- NOT STARTED
  Insufficient engineering evidence exists.

---

# 3. Architecture Protection Rules

DATA IS EVIDENCE.

ENGINE IS LOGIC.

DECISION IS DIRECTION.

RISK IS CONDITION.

ACTION IS A SEPARATE LAYER.

NO SOURCE DEFINITION
→ NO DATA INTEGRATION.

NO VERIFIED UNIT EVIDENCE
→ NO UNIT LOCK.

NO NORMALIZATION
→ NO ENGINE INPUT.

NO LOCKED FORMULA
→ NO ENGINE IMPLEMENTATION.

NO BASELINE PASS
→ NO CORE REFACTOR.

NO VERIFIED ACTION SPEC
→ NO AUTOMATIC ACTION.

NO PASS
→ NO MERGE.

Market / Chip / Risk enhancement
MUST NOT silently overwrite V13 locked Core behavior.

---

# 4. Gate 21 → Gate 28D.2K-3L Evolution

Gate 21 established the original Requirement Traceability baseline.

Subsequent major engineering evolution includes:

Gate 22
→ Normalized Chip Data Contract

Gate 23
→ Chip Source Mapping

Gate 24
→ Chip Source Adapter

Gate 25
→ Chip Source Compatibility

Gate 26
→ Chip Unit Evidence Governance

Gate 27+
→ Live Source Read-Only / Safety Boundaries

Gate 28D
→ FinMind Live / Evidence / Controlled Runtime chain

Gate 28D.2K
→ Yahoo / FinMind Baseline Evidence Compare family

Gate 28D.2K-3A ~ 3C
→ First Controlled Real GET planning / gate / evidence

Gate 28D.2K-3D
→ Real GET Golden Evidence Integration

Gate 28D.2K-3E ~ 3G
→ One-Shot / Runtime / Entry Composition

Gate 28D.2K-3H ~ 3J
→ Fail-Closed / Runtime Exception / Golden Exception

Gate 28D.2K-3K
→ Golden Evidence Semantic Observer Composition

Gate 28D.2K-3L
→ Protected Runtime Semantic Golden Evidence Composition

Current Protected Commit:

3cbb3bb32fe7ccee89e7121b573fece768aa94ef

---

# 5. Current WP Coverage

| WP | Scope | V2 Current Status | Current Interpretation |
|---|---|---|---|
| WP1 | Core Clean | LARGELY VERIFIED | V13 locked Core remains protected; remaining specification gaps are separate |
| WP2 | Data Dictionary / Source Contract | PARTIAL VERIFIED | Source / FinMind / live / Golden safety foundation significantly advanced; all data integration is not complete |
| WP3 | Chip Data | PARTIAL VERIFIED / DATA-EVIDENCE GAP | Schema, mapping, adapter and unit governance exist; verified units and derived Chip Engine remain incomplete |
| WP4 | Market Context | DATA + SPEC + IMPLEMENTATION GAP | Benchmark / Group / Relative Strength production and regression implementation not established |
| WP5 | Risk Spec | PARTIAL VERIFIED | Risk V1 exists; complete Risk Lock depends on additional Chip / Market evidence |
| WP6 | Action Spec | PARTIAL VERIFIED | Action V1 exists; final ENTRY / ADD / HOLD / REDUCE / EXIT specification remains incomplete |
| WP7 | Backtest | VALIDATION GAP | Regression does not replace historical validation / backtest |

---

# 6. Requirement 14–20 — WP3 Reconciliation

| # | Requirement | V2 Status | Evidence / Remaining Gap |
|---|---|---|---|
| 14 | Institutional Data | PARTIAL VERIFIED | Institutional source mapping exists; unit evidence remains pending |
| 15 | Margin / Short | PARTIAL VERIFIED | Raw fields are mapped / field-locked; units remain pending |
| 16 | Day Trading | PARTIAL VERIFIED | Dataset / fields mapped; unit evidence remains PARTIAL |
| 17 | Securities Lending | PARTIAL VERIFIED | Transaction evidence semantics mapped; transaction volume unit remains pending |
| 18 | Institutions Separate | PARTIAL VERIFIED | Foreign / Trust / Dealer categories separated at mapping layer; downstream completion remains incomplete |
| 19 | Dealer Hedge Separation | VERIFIED — MAPPING LAYER | Dealer_self and Dealer_Hedging are explicitly separated |
| 20 | Price × Margin × Short | VALIDATION GAP | Raw foundation exists; derived relationship and historical validation remain incomplete |

---

# 7. WP3 Chip Foundation Status

Current verified / established foundation:

- Normalized Chip Data Contract
- Chip Evidence Contract
- Chip Source Mapping
- Chip Source Adapter
- Chip Source Compatibility
- Chip Unit Evidence Governance

Source domains include:

- Foreign
- Investment Trust
- Dealer Legacy
- Dealer Self
- Dealer Hedging
- Margin
- Short
- Offset
- Securities Lending
- Day Trading

Current unit evidence remains fail-closed:

Institutional
→ UNIT_PENDING

Margin
→ UNIT_PENDING

Short
→ UNIT_PENDING

Offset
→ UNIT_PENDING

Securities Lending
→ UNIT_PENDING

Day Trading
→ PARTIAL_UNIT_LOCK

UNKNOWN UNIT
!= ASSUMED UNIT

UNIT_PENDING
!= VERIFIED

UNIT_PENDING
!= LOCKED

No automatic ×1000 / ÷1000 conversion is authorized.

---

# 8. WP3 Remaining Derived Gaps

Raw Evidence
!= Derived Signal.

The following are not declared complete by the source-mapping layer:

- institutional net buy / sell
- 3-day accumulation
- 5-day accumulation
- 10-day accumulation
- consecutive institutional buy / sell
- institutional acceleration
- foreign / investment-trust resonance
- margin change
- short change
- margin-short relationship
- securities-lending trend
- day-trade ratio
- day-trade moving average
- day-trade overheat
- Chip Score

WP3 current blocker:

EXTERNAL VERIFIED UNIT EVIDENCE

A future unit upgrade requires:

1. source identified
2. dataset identified
3. raw field identified
4. field meaning verified
5. unit explicitly verified
6. compatibility impact reviewed
7. regression fixture added

Without all required evidence:

KEEP UNIT_PENDING.

---

# 9. Requirement 21–23 — WP4 Reconciliation

| # | Requirement | V2 Status | Remaining Gap |
|---|---|---|---|
| 21 | Market Benchmark | DATA + SPEC + IMPLEMENTATION GAP | Benchmark identity, source, formula, threshold and output contract are not locked |
| 22 | Group Resonance / Breadth | DATA + SPEC + IMPLEMENTATION GAP | Industry / group identity, breadth model, resonance formula and threshold are not locked |
| 23 | Relative Strength | SPEC + IMPLEMENTATION GAP | Data foundation may be usable, but benchmark, period, formula, ranking / threshold and output contract are not locked |

Current repository inspection found no dedicated production
implementation or regression contract for:

- Market Benchmark Engine
- Industry Context Engine
- Group Resonance / Breadth Engine
- Relative Strength Engine

---

# 10. WP4 Market Context Master Direction

Master Specification defines the Market Engine purpose as:

判斷個股所處市場環境。

Candidate information includes:

- Taiwan market benchmark
- OTC
- industry index
- group / sector
- market advance / decline
- market breadth
- Relative Strength
- market resonance

Future Market State may include:

MARKET BULLISH

MARKET NEUTRAL

MARKET BEARISH

Protection rule:

MARKET STATE
MUST NOT directly overwrite
V13 CORE DECISION.

---

# 11. WP4 Specification Gap

Before implementation, WP4 requires a formal specification for:

1. Market Source Contract
2. Benchmark Identity
3. Listed / OTC benchmark policy
4. Industry / Group Identity
5. Market Breadth definition
6. Group Resonance definition
7. Relative Strength benchmark
8. Relative Strength period
9. Relative Strength formula
10. Threshold / classification rules
11. Market State output contract
12. Missing / stale / insufficient evidence behavior
13. Fail-Closed boundary
14. Risk-input boundary
15. V13 Core non-overwrite protection

Therefore:

WP4 IS NOT READY FOR PRODUCTION IMPLEMENTATION.

---

# 12. Live / FinMind Evidence Safety Chain

Current protected chain:

Controlled Runtime
→ RAW_EVIDENCE
→ Semantic Observation
→ Golden Evidence
→ Protected Runtime Semantic Golden Evidence
→ SAFE STOP

Current latest node:

Gate 28D.2K-3L

Protected Commit:

3cbb3bb32fe7ccee89e7121b573fece768aa94ef

Safety Tag:

v14-gate-28d2k-3l-protected-runtime-semantic-golden-safe

Verification:

- Standalone Contract PASS
- Full V14 Regression PASS
- E2E Full Core Wiring PASS
- Local / Remote SHA MATCH
- Remote Safety Tag VERIFIED
- Final Working Tree CLEAN

---

# 13. 28D.2K Explicit Non-Authorization Boundary

Gate 28D.2K / 3L DOES NOT AUTHORIZE:

- normalization
- normalized market output activation
- provider compatibility establishment
- provider switch
- V13 Core source switch
- Core input
- engine formula change
- score
- decision
- Supabase write
- production write

Therefore:

3L PASS
!= FINMIND CORE ACTIVATION

3L PASS
!= NORMALIZATION AUTHORIZATION

3L PASS
!= PROVIDER SWITCH AUTHORIZATION

3L PASS
!= PRODUCTION WRITE AUTHORIZATION

---

# 14. Current Development Priority

Priority A:

Maintain Gate 28D.2K-3L Protected Safety Node.

Priority B:

Lock Requirement Traceability V2.

Priority C:

WP4 Market Context Specification V1.

WP4 specification sequence:

Market Source Contract
→ Benchmark Identity
→ Industry / Group Identity
→ Breadth / Resonance Definition
→ Relative Strength Definition
→ Market State Contract
→ Fail-Closed Boundary
→ Specification Review / Lock

Only after specification lock:

consider a Contract-first implementation Gate.

WP3 Unit Evidence remains an external-evidence workstream.

No unit may be upgraded by assumption.

---

# 15. Next Candidate

Next specification candidate:

WP4 MARKET CONTEXT SPECIFICATION V1

This is a specification candidate.

It is NOT:

- Gate 28D.2K-3M
- Core activation
- normalization activation
- Risk V2 activation
- production implementation
- production write authorization

---

# 16. Current Continuation Point

Current Protected Engineering Baseline:

Gate 28D.2K-3L

Commit:

3cbb3bb32fe7ccee89e7121b573fece768aa94ef

Safety Tag:

v14-gate-28d2k-3l-protected-runtime-semantic-golden-safe

Development continuation rule:

1. verify Working Tree CLEAN
2. verify Local / Remote SHA MATCH
3. preserve 3L Safety Tag
4. use Requirement Traceability V2 as current roadmap baseline
5. begin WP4 Specification before any WP4 production implementation

---

# 17. Conclusion

V14 engineering progress has materially advanced beyond the
Gate 21 Requirement Traceability V1 baseline.

The correct next action is not to continue Gate numbering
mechanically.

Current priorities are:

Requirement Reconciliation
→ WP4 Specification
→ Contract-first review
→ only then implementation.

WP3 remains PARTIAL VERIFIED with external Unit Evidence gaps.

WP4 is the next specification workstream.

Gate 28D.2K-3L remains the latest protected engineering
safety baseline.

PRODUCTION WRITE = NOT AUTHORIZED.
