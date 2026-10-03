# DAVID V14 UNIFIED ENGINE — WP4 MARKET CONTEXT SPECIFICATION V1

> Work Package: WP4 — Market Context
>
> Document Type: Specification Baseline
>
> Roadmap Baseline: V14_REQUIREMENT_TRACEABILITY_V2.md
>
> Roadmap Commit: 280305d5c23cee78e593b053fb7939c8cbe35f9b
>
> Engineering Baseline: Gate 28D.2K-3L
>
> Engineering Protected Commit: 3cbb3bb32fe7ccee89e7121b573fece768aa94ef
>
> Production Implementation: NOT AUTHORIZED
>
> Production Write: NOT AUTHORIZED

---

# 1. Purpose

本文件建立 DAVID V14 Unified Engine
WP4 Market Context 的正式 Specification Baseline。

WP4 的目的為：

判斷個股所處市場環境。

WP4 不取代：

- Technical Engine
- Chip Engine
- Position Engine
- V13 Core Decision
- DAVID Score
- Risk Engine
- Action Engine

WP4 是獨立 Market Context Layer。

Market Context
!= Core Decision

Market Context
!= Trading Action

---

# 2. Master Requirement Scope

WP4 對應 Requirement Traceability V2：

Requirement 21
→ Market Benchmark

Requirement 22
→ Group Resonance / Breadth

Requirement 23
→ Relative Strength

Master Specification candidate information includes:

- Taiwan market benchmark
- OTC
- industry index
- group / sector
- market advance / decline
- market breadth
- Relative Strength
- market resonance

Future Market State may include:

- MARKET_BULLISH
- MARKET_NEUTRAL
- MARKET_BEARISH

Current formula / threshold definitions are not yet locked.

---

# 3. Specification Status Vocabulary

WP4 V1 uses the following formal states.

SOURCE_PENDING

Meaning:

Source / Dataset / identity / field semantics
have not yet been formally verified and locked.

SOURCE_PENDING
!= MISSING

SOURCE_PENDING
!= INVALID

SOURCE_PENDING
!= VERIFIED SOURCE


SPEC_PENDING

Meaning:

Requirement exists,
but formula / period / threshold / classification rule
has not yet been formally locked.

SPEC_PENDING
!= IMPLEMENTED

SPEC_PENDING
!= VERIFIED


NOT_AUTHORIZED

Meaning:

The operation is explicitly outside the authority
of the current specification.

NOT_AUTHORIZED
!= TODO

NOT_AUTHORIZED
!= IMPLICIT PERMISSION

---

# 4. Current Provider Architecture

Existing Master Data Source direction:

V13 Baseline Price Source
→ Yahoo Finance OHLCV

V14 Primary Taiwan Market Data Provider
→ FinMind

Price Fallback Source
→ Yahoo Finance

FinMind is positioned to provide:

- OHLCV
- institutional data
- margin / short
- securities lending
- day trading
- ownership / holding context
- market data
- fundamental context
- other formally verified Taiwan-market datasets

However:

Provider capability
!= WP4 Source Contract.

A provider must not become a WP4 Market Source
until Dataset / identity / semantics are formally verified.

---

# 5. Data Adapter Protection

External market data must not directly enter
an Engine formula.

Target architecture:

External Provider
→ Data Adapter
→ Normalized Schema
→ Market Context Layer

Existing Master Specification defines
a target Normalized OHLCV schema including:

- timestamp
- open
- high
- low
- close
- volume

Metadata:

- source
- market
- stock_id
- timezone
- adjustment_type
- retrieved_at

Important:

Master Architecture Target
!= Current Runtime Authorization.

Gate 28D.2K / 3L does not authorize
FinMind normalized market output or Core input.

---

# 6. WP4 V1 Scope

WP4 Market Context Specification V1 covers:

1. Market Source Contract
2. Benchmark Identity Policy
3. OTC Identity Policy
4. Industry / Group Identity Policy
5. Market Breadth Definition
6. Market Resonance Definition
7. Relative Strength Definition
8. Market State Contract
9. Missing / Stale / Insufficient Evidence Policy
10. Fail-Closed Boundary
11. Risk Input Boundary
12. V13 Core Non-Overwrite Protection

WP4 V1 is DAILY / READ-ONLY first.

Realtime Market Context is outside V1 scope.

---

# 7. Market Source Contract

Current state:

MARKET_SOURCE_STATUS = SOURCE_PENDING

The following source identities are not yet locked:

Taiwan Market Benchmark
→ SOURCE_PENDING

OTC Benchmark
→ SOURCE_PENDING

Industry Index
→ SOURCE_PENDING

Group / Sector Membership Source
→ SOURCE_PENDING

Market Breadth Source
→ SOURCE_PENDING

Market Resonance Source
→ SOURCE_PENDING

No Dataset name may be invented or assumed.

No Provider field may be mapped into WP4
without source evidence.

---

# 8. Benchmark Identity Policy

Requirement 21:

Market Benchmark.

Current status:

BENCHMARK_SOURCE = SOURCE_PENDING

BENCHMARK_IDENTITY = SPEC_PENDING

BENCHMARK_FORMULA = SPEC_PENDING

BENCHMARK_PERIOD = SPEC_PENDING

BENCHMARK_THRESHOLD = SPEC_PENDING

The following remain unresolved:

- listed-stock benchmark identity
- OTC benchmark identity
- benchmark selection policy
- benchmark trading-date alignment
- benchmark missing-data policy
- benchmark adjustment policy
- benchmark return / trend definition

Until locked:

NO BENCHMARK SIGNAL.

---

# 9. Industry / Group Identity Policy

Requirement 22 includes:

Group Resonance / Breadth.

Current state:

INDUSTRY_SOURCE = SOURCE_PENDING

GROUP_SOURCE = SOURCE_PENDING

GROUP_MEMBERSHIP = SPEC_PENDING

The following must be formally defined:

- industry identity
- sector / group identity
- constituent membership
- membership effective date
- constituent missing-data policy
- constituent minimum coverage
- group aggregation rule

Until locked:

NO GROUP SIGNAL.

---

# 10. Market Breadth

Market Breadth is part of WP4 candidate information.

Current state:

BREADTH_SOURCE = SOURCE_PENDING

BREADTH_FORMULA = SPEC_PENDING

BREADTH_PERIOD = SPEC_PENDING

BREADTH_THRESHOLD = SPEC_PENDING

Potential concepts must not be treated as formulas.

No assumption is authorized regarding:

- advance / decline ratio
- advancing-stock count
- declining-stock count
- unchanged-stock count
- volume breadth
- percentage-above-MA breadth
- breadth moving average

These remain specification candidates only.

Until formula and source are locked:

NO MARKET BREADTH SIGNAL.

---

# 11. Market Resonance

Requirement 22:

Group Resonance / Market Resonance.

Current state:

RESONANCE_SOURCE = SOURCE_PENDING

RESONANCE_FORMULA = SPEC_PENDING

RESONANCE_PERIOD = SPEC_PENDING

RESONANCE_THRESHOLD = SPEC_PENDING

The following are not yet defined:

- resonance universe
- benchmark relationship
- industry relationship
- breadth relationship
- minimum group coverage
- bullish resonance rule
- bearish resonance rule
- neutral rule

Until formally locked:

NO MARKET RESONANCE SIGNAL.

---

# 12. Relative Strength

Requirement 23:

Relative Strength.

Current state:

RS_DATA_FOUNDATION = PARTIAL

RS_BENCHMARK = SPEC_PENDING

RS_PERIOD = SPEC_PENDING

RS_FORMULA = SPEC_PENDING

RS_NORMALIZATION = SPEC_PENDING

RS_RANKING = SPEC_PENDING

RS_THRESHOLD = SPEC_PENDING

No assumption is authorized regarding whether
Relative Strength means:

- price ratio
- return difference
- excess return
- percentile rank
- cross-sectional rank
- benchmark-relative momentum
- industry-relative momentum

These are candidate concepts only.

Until a formal specification is locked:

NO RELATIVE STRENGTH SIGNAL.

---

# 13. Market State Contract

Future Market State candidates:

MARKET_BULLISH

MARKET_NEUTRAL

MARKET_BEARISH

Current state:

MARKET_STATE_FORMULA = SPEC_PENDING

MARKET_STATE_THRESHOLD = SPEC_PENDING

MARKET_STATE_OUTPUT = NOT_AUTHORIZED

No Market State may be emitted merely because
one candidate input appears bullish or bearish.

Market State requires a future locked contract.

---

# 14. Evidence State

WP4 input evidence must distinguish:

READY

MISSING

STALE

PRELIMINARY

FINAL

INSUFFICIENT_EVIDENCE

SOURCE_PENDING

SPEC_PENDING

Important:

MISSING
!= ZERO

STALE
!= READY

PRELIMINARY
!= FINAL

INSUFFICIENT_EVIDENCE
!= NEUTRAL

SOURCE_PENDING
!= MISSING

SPEC_PENDING
!= NEUTRAL

---

# 15. Fail-Closed Boundary

WP4 must fail closed.

NO VERIFIED SOURCE
→ NO MARKET INPUT.

NO VERIFIED DATA ADAPTER
→ NO MARKET INPUT.

NO LOCKED FORMULA
→ NO MARKET SIGNAL.

NO LOCKED THRESHOLD
→ NO MARKET CLASSIFICATION.

NO VERIFIED MARKET STATE
→ NO RISK ENHANCEMENT.

NO VERIFIED CONTRACT
→ NO IMPLEMENTATION ACTIVATION.

---

# 16. V13 Core Protection

WP4 must not silently modify:

- V13 Six Buy
- V13 Six Sell
- V13 Pivot Fibonacci
- V13 Core Decision
- DAVID Score V1

Market State
MUST NOT directly overwrite
V13 Core Decision.

Market Context is supplemental evidence.

It is not Core authority.

---

# 17. Risk Boundary

Future verified Market Context may become
a Risk input only through a separate,
explicitly verified Risk contract.

WP4 V1 does not modify Risk V1.

WP4 V1 does not authorize Risk V2.

MARKET STATE
!= RISK STATE

MARKET STATE
!= ACTION

---

# 18. Action Boundary

WP4 does not authorize:

- ENTRY
- ADD
- HOLD
- REDUCE
- EXIT
- automatic trading action

Market Context
must not directly emit Action.

NO VERIFIED ACTION SPEC
→ NO AUTOMATIC ACTION.

---

# 19. 28D.2K / 3L Boundary

Current Engineering Protected Baseline:

Gate 28D.2K-3L

Protected Commit:

3cbb3bb32fe7ccee89e7121b573fece768aa94ef

Safety Tag:

v14-gate-28d2k-3l-protected-runtime-semantic-golden-safe

Current chain:

Controlled Runtime
→ RAW_EVIDENCE
→ Semantic Observation
→ Golden Evidence
→ Protected Runtime Semantic Golden Evidence
→ SAFE STOP

This baseline does not authorize:

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

---

# 20. Realtime Boundary

WP4 V1 is Daily / Read-Only first.

Realtime Market Context is a separate future phase.

Sponsor / realtime capability
must not be treated as a prerequisite
for WP4 V1 specification.

Intraday Market Resonance
is outside WP4 V1 scope.

---

# 21. Production Boundary

WP4 V1 is specification-only.

It does not authorize:

- production Python implementation
- Runner integration
- live market fetch
- Real GET
- normalization activation
- Core input
- Risk V2
- Action V2
- Supabase write
- production write

PRODUCTION_IMPLEMENTATION = NOT_AUTHORIZED

PRODUCTION_WRITE = NOT_AUTHORIZED

---

# 22. Verification Requirements Before Implementation

Before any WP4 implementation Gate is considered,
the following must be reviewed and locked:

1. Benchmark source
2. Benchmark identity
3. OTC source / identity
4. Industry / group source
5. Group membership policy
6. Market breadth source
7. Market breadth formula
8. Market resonance formula
9. Relative Strength benchmark
10. Relative Strength period
11. Relative Strength formula
12. Market State formula
13. Market State thresholds
14. Missing / stale / insufficient evidence policy
15. Normalized schema requirements
16. V13 Core non-overwrite contract
17. Risk-input boundary

Without these:

IMPLEMENTATION_GATE = NOT_AUTHORIZED

---

# 23. Next Evidence Work

The next work is evidence / specification work,
not production implementation.

Candidate evidence tasks:

- identify benchmark source candidates
- identify OTC source candidates
- identify industry / group source candidates
- verify Dataset semantics
- verify trading-date alignment
- verify timezone semantics
- verify adjustment semantics
- define benchmark policy
- define group membership policy
- define Relative Strength specification candidates
- define Breadth / Resonance specification candidates

Candidate
!= Approved Specification.

---

# 24. Current Status Summary

WP4 Market Context:

DATA GAP
+
SPEC GAP
+
IMPLEMENTATION GAP

Requirement 21 — Market Benchmark:

DATA + SPEC + IMPLEMENTATION GAP

Requirement 22 — Group Resonance / Breadth:

DATA + SPEC + IMPLEMENTATION GAP

Requirement 23 — Relative Strength:

SPEC + IMPLEMENTATION GAP

Production Implementation:

NOT AUTHORIZED

Production Write:

NOT AUTHORIZED

Realtime:

OUT OF V1 SCOPE

---

# 25. Continuation Rule

Current Roadmap Baseline:

V14 Requirement Traceability V2

Commit:

280305d5c23cee78e593b053fb7939c8cbe35f9b

Roadmap Safety Tag:

v14-requirement-traceability-v2-safe

Current Engineering Baseline:

Gate 28D.2K-3L

Commit:

3cbb3bb32fe7ccee89e7121b573fece768aa94ef

Before continuing:

1. preserve both safety baselines
2. verify Working Tree CLEAN
3. perform evidence / specification review
4. do not invent Dataset names
5. do not invent formulas
6. do not invent thresholds
7. do not create implementation Gate before specification lock

---

# 26. Conclusion

WP4 Market Context is the next specification workstream.

The requirement exists.

The architecture direction exists.

The provider architecture exists.

The Market-specific source contract is not yet locked.

The Benchmark / Group / Relative Strength formulas
are not yet locked.

Therefore:

WP4 MARKET CONTEXT SPECIFICATION V1
= SPECIFICATION BASELINE

WP4 PRODUCTION IMPLEMENTATION
= NOT AUTHORIZED

NEXT ACTION
= EVIDENCE / SPECIFICATION REVIEW

PRODUCTION WRITE
= NOT AUTHORIZED
