# DAVID V14 UNIFIED ENGINE — WP4 BENCHMARK SOURCE EVIDENCE V1

> Work Package: WP4 — Market Context
>
> Document Type: Source Evidence Baseline
>
> Parent Specification: V14_WP4_MARKET_CONTEXT_SPEC_V1.md
>
> WP4 Specification Baseline Commit: 8b66e51651a8b8ea47d19968de9cb7b3c0a17bbe
>
> Roadmap Baseline: V14_REQUIREMENT_TRACEABILITY_V2.md
>
> Engineering Baseline: Gate 28D.2K-3L
>
> Runtime Real GET Performed By This Evidence Work: 0
>
> Production Implementation: NOT AUTHORIZED
>
> Production Write: NOT AUTHORIZED

---

# 1. Purpose

本文件保存 WP4 Requirement 21
Market Benchmark 的 Source Evidence Review。

本文件不是：

- Market Engine implementation
- Benchmark formula specification lock
- Relative Strength formula lock
- provider switch authorization
- normalization activation
- Core input authorization
- production write authorization

本文件的目的為：

Requirement 21
→ Benchmark Identity Evidence
→ Provider Evidence
→ Daily Source Evidence
→ Official Verification Evidence
→ Index-Type Policy Candidate
→ Source Architecture Candidate
→ Remaining Gap

---

# 2. Evidence Status Vocabulary

SOURCE_PENDING

Source requirement exists,
but the final source contract is not locked.

SOURCE_CANDIDATE

A source has supporting evidence,
but has not yet completed all verification
required for source lock.

STRONG_SOURCE_CANDIDATE

Multiple supporting evidence layers exist,
but final V14 source authorization is not yet locked.

SOURCE_VERIFIED

Reserved for a future state after
all required evidence and specification review pass.

SOURCE_CANDIDATE
!= SOURCE_VERIFIED

STRONG_SOURCE_CANDIDATE
!= SOURCE_VERIFIED

---

# 3. Existing V14 Provider Architecture

Existing Master Data Source direction:

FinMind
→ PRIMARY DATA PROVIDER

Yahoo Finance
→ V13 BASELINE / PRICE FALLBACK

TWSE / TPEx
→ OFFICIAL VERIFY SOURCE

Supabase
→ DAVID DATA WAREHOUSE

Important:

Provider role
!= Dataset verification.

Official verification source
!= automatic primary ingestion source.

Price fallback source
!= official verification source.

---

# 4. Existing WP4 Benchmark Requirement

Requirement 21:

Market Benchmark.

V13 / V14 requirement materials identify:

Listed Market
→ 加權指數

OTC Market
→ 櫃買指數

However, previous local specification review found:

BENCHMARK_SOURCE
= SOURCE_PENDING

BENCHMARK_IDENTITY
= SPEC_PENDING

BENCHMARK_FORMULA
= SPEC_PENDING

BENCHMARK_PERIOD
= SPEC_PENDING

BENCHMARK_THRESHOLD
= SPEC_PENDING

NO BENCHMARK SIGNAL.

---

# 5. Local Repository Evidence Review

Local evidence review covered:

- V13_CORE_BASELINE.md
- V14_DATA_SOURCE_SPEC.md
- V14_REQUIREMENT_TRACEABILITY_V1.md
- V14_REQUIREMENT_TRACEABILITY_V2.md
- V14_WP4_MARKET_CONTEXT_SPEC_V1.md
- v14/*.py
- tests/*.py

Local findings:

V13 requirement direction includes:

- 加權指數
- 櫃買指數
- 產業
- 族群
- 相對強弱
- 市場共振

V14 Data Source architecture defines:

FinMind
→ PRIMARY DATA PROVIDER

TWSE / TPEx
→ OFFICIAL VERIFY SOURCE

Local production search found no dedicated:

- Benchmark Engine
- TAIEX benchmark abstraction
- TPEX benchmark abstraction
- Market Index Engine
- Relative Strength Engine

Local regression search found no dedicated
WP4 Benchmark Contract.

Therefore:

LOCAL_REQUIREMENT_EVIDENCE
= EXISTS

LOCAL_IMPLEMENTATION
= NOT ESTABLISHED

---

# 6. Listed Market Official Identity Evidence

Official evidence identifies the Taiwan listed-market
benchmark as:

TAIEX

TAIEX refers to the Taiwan Stock Exchange
Capitalization Weighted Stock Index.

Official compiler / verification authority:

TWSE

Official methodology distinguishes:

- Price Index
- Total Return Index

Therefore:

LISTED_BENCHMARK_IDENTITY
= STRONG_SOURCE_CANDIDATE

LISTED_OFFICIAL_VERIFY_SOURCE
= TWSE

This does not yet authorize
a V14 Benchmark Source Contract.

---

# 7. OTC Official Identity Evidence

Official TPEx materials provide:

TPEx capitalization-weighted market index

and distinguish:

- Price Index
- Total Return Index

Official compiler / verification authority:

TPEx

Therefore:

OTC_BENCHMARK_IDENTITY
= STRONG_SOURCE_CANDIDATE

OTC_OFFICIAL_VERIFY_SOURCE
= TPEx

This does not yet authorize
a V14 Benchmark Source Contract.

---

# 8. FinMind Index Identity Evidence

FinMind Index Code documentation identifies:

001
→ 加權指數 / TAIEX

101
→ 櫃檯買賣發行量加權股價指數 / OTC

These codes provide useful identity evidence.

However:

Index-code evidence
!= Daily Price Index Dataset evidence.

Snapshot / realtime identity
must not be silently promoted into
a Daily WP4 source.

Therefore:

FINMIND_TAIEX_IDENTITY
= SOURCE_CANDIDATE

FINMIND_OTC_IDENTITY
= SOURCE_CANDIDATE

---

# 9. FinMind Daily Total Return Evidence

FinMind documentation identifies:

Dataset:

TaiwanStockTotalReturnIndex

Purpose:

加權、櫃買報酬指數

Supported identities include:

TAIEX

TPEx

Documented fields include:

- date
- stock_id
- price

Documented history:

2003-01-01
→ current

Documented update pattern:

Daily / weekday update

Therefore:

FINMIND_DAILY_TOTAL_RETURN_SOURCE
= STRONG_SOURCE_CANDIDATE

Important:

Total Return Index
!= Price Index.

TaiwanStockTotalReturnIndex
must not be silently used as
the Daily Price Index source.

---

# 10. FinMind Intraday Price-Index Evidence

FinMind documentation / update history provides
TAIEX intraday index evidence,
including TAIEX KBar / index-related data.

This demonstrates that FinMind can represent
TAIEX price-index values.

However:

Intraday data
!= Daily source contract.

WP4 V1 is:

DAILY / READ-ONLY FIRST.

V14 must not silently create a Daily source
by extracting a close from intraday data
without an explicit aggregation specification.

Therefore:

FINMIND_INTRADAY_PRICE_INDEX
= SECONDARY SOURCE CANDIDATE

FINMIND_DAILY_PRICE_INDEX
= SOURCE_PENDING

---

# 11. TWSE Daily / EOD Verification Evidence

TWSE official data products provide
TAIEX / index information suitable for
official end-of-day verification.

Official TWSE index materials distinguish:

Price Index

and

Total Return Index.

Therefore:

TAIEX_PRICE_INDEX_OFFICIAL_VERIFY
= STRONG_SOURCE_CANDIDATE

TAIEX_TOTAL_RETURN_OFFICIAL_VERIFY
= STRONG_SOURCE_CANDIDATE

Role:

OFFICIAL_VERIFY_SOURCE

This does not automatically change TWSE into
the V14 Primary Data Provider.

---

# 12. TPEx Daily / EOD Verification Evidence

TPEx official data products provide
historical / end-of-day TPEx index information.

Official TPEx materials distinguish:

Price Index

and

Total Return Index.

Therefore:

TPEX_PRICE_INDEX_OFFICIAL_VERIFY
= STRONG_SOURCE_CANDIDATE

TPEX_TOTAL_RETURN_OFFICIAL_VERIFY
= STRONG_SOURCE_CANDIDATE

Role:

OFFICIAL_VERIFY_SOURCE

This does not automatically change TPEx into
the V14 Primary Data Provider.

---

# 13. Price Index vs Total Return Index

Official evidence confirms that:

Price Index
and
Total Return Index

are separate official index series.

Total Return Index incorporates
cash-dividend reinvestment effects.

Therefore:

PRICE_INDEX
!= TOTAL_RETURN_INDEX

V14 must not silently substitute
one for the other.

---

# 14. Benchmark Policy Candidate

Current specification candidate:

Daily Market Trend / Market State
→ Price Index candidate

Long-Term Performance / Backtest Context
→ Total Return Index candidate

Relative Strength
→ BASIS_MATCH_REQUIRED

Meaning:

Stock Price Return
should be compared with
Benchmark Price Index Return.

Stock Total Return
should be compared with
Benchmark Total Return.

Cross-basis comparison is not authorized
without a future explicit specification.

Status:

BENCHMARK_POLICY
= CANDIDATE

BENCHMARK_POLICY
!= LOCKED

---

# 15. Source Architecture Candidate A1

Target architecture candidate:

FinMind
→ Primary Market Provider
→ Adapter
→ Normalized Daily Price Index
→ WP4 Market Context
→ Official Verification by TWSE / TPEx

Status:

SOURCE_ARCHITECTURE_A1
= CANDIDATE

Conditions:

1. FinMind Daily Price Index source must be verified.
2. Dataset semantics must be verified.
3. Trading-date semantics must be verified.
4. Timezone semantics must be verified.
5. Adjustment semantics must be verified.
6. License / usage semantics must be reviewed.

Until all required conditions pass:

SOURCE_ARCHITECTURE_A1
!= LOCKED

---

# 16. Official-EOD Exception Review

If a suitable FinMind Daily Price Index source
cannot be verified:

DO NOT

- invent a Dataset
- silently aggregate intraday data
- silently use Total Return Index
- silently switch provider

Instead:

OPEN

Official-EOD Exception Architecture Review

Candidate architecture:

TWSE / TPEx Official EOD
→ Official Adapter
→ Normalized Daily Price Index
→ WP4 Market Context

Status:

OFFICIAL_EOD_EXCEPTION
= REVIEW_ONLY

It is not currently authorized.

---

# 17. Yahoo Boundary

Existing Master Specification defines:

Yahoo Finance
→ V13 BASELINE / PRICE FALLBACK

This evidence review does not change
Yahoo's existing role.

Yahoo is not automatically promoted to
WP4 Benchmark Primary Source.

YAHOO_WP4_BENCHMARK_PRIMARY
= NOT_AUTHORIZED

---

# 18. License / Usage Evidence Requirement

WP4 Source Contract should include
license / usage governance.

Future evidence fields should include:

- provider
- dataset
- identity
- market
- frequency
- fields
- timezone
- adjustment_semantics
- trading_date_semantics
- license_status
- usage_scope
- redistribution_status
- commercial_review_status
- evidence_status
- official_verify_source

Candidate license states:

PUBLIC_VERIFY

INTERNAL_USE

SUBSCRIPTION_REQUIRED

COMMERCIAL_REVIEW_REQUIRED

UNKNOWN

UNKNOWN LICENSE
!= AUTHORIZED USE

---

# 19. Current Benchmark Evidence Matrix

Listed Market:

Official Identity
→ TAIEX

Official Verify Source
→ TWSE

FinMind Identity Evidence
→ 001 / TAIEX-related index identity

FinMind Daily Total Return
→ TaiwanStockTotalReturnIndex / TAIEX

FinMind Daily Price Index
→ SOURCE_PENDING


OTC Market:

Official Identity
→ TPEx / OTC capitalization-weighted index

Official Verify Source
→ TPEx

FinMind Identity Evidence
→ 101 / OTC index identity

FinMind Daily Total Return
→ TaiwanStockTotalReturnIndex / TPEx

FinMind Daily Price Index
→ SOURCE_PENDING

---

# 20. Evidence Gaps

Remaining evidence gaps:

1. FinMind Daily Price Index Dataset
2. Daily Price Index schema
3. Listed / OTC daily identity mapping
4. Trading-date semantics
5. Timezone semantics
6. Adjustment semantics
7. Missing-data behavior
8. Suspended / non-trading-date behavior
9. License / usage status
10. Normalized Daily Price Index schema
11. Official verification tolerance / comparison policy

Until resolved:

BENCHMARK_SOURCE
= SOURCE_PENDING

---

# 21. Non-Authorization Boundary

This evidence document does not authorize:

- production Python implementation
- Runner integration
- live API execution
- V14 Real GET
- token use
- normalization activation
- provider switch
- Core input
- Market State output
- Risk V2
- Action V2
- Supabase write
- production write

IMPLEMENTATION_GATE
= NOT_AUTHORIZED

REAL_GET
= 0

PRODUCTION_WRITE
= NOT_AUTHORIZED

---

# 22. Relationship to WP4 Specification V1

Parent Specification:

V14_WP4_MARKET_CONTEXT_SPEC_V1.md

This evidence document does not modify
the parent specification.

Parent specification remains:

BENCHMARK_SOURCE
= SOURCE_PENDING

BENCHMARK_IDENTITY
= SPEC_PENDING

BENCHMARK_FORMULA
= SPEC_PENDING

BENCHMARK_PERIOD
= SPEC_PENDING

BENCHMARK_THRESHOLD
= SPEC_PENDING

RS_BENCHMARK
= SPEC_PENDING

---

# 23. Next Evidence Work

Next evidence priority:

1. Resolve FinMind Daily Price Index availability
2. If unresolved, evaluate Official-EOD Exception architecture
3. Verify license / usage semantics
4. Define Normalized Daily Price Index schema candidate
5. Define official verification policy
6. Only then consider Benchmark Source Contract lock

Do not proceed to:

- Benchmark Engine
- Relative Strength Engine
- Market State Engine

before source evidence is sufficiently locked.

---

# 24. Current Status

Requirement 21:

MARKET BENCHMARK

Official Identity Evidence
= STRONG

Official Verification Evidence
= STRONG

Daily Total Return Source Evidence
= STRONG SOURCE CANDIDATE

Daily Price Index Source Evidence
= PARTIAL / SOURCE_PENDING

Source Architecture
= CANDIDATE

Benchmark Policy
= CANDIDATE

Implementation
= NOT AUTHORIZED

Production Write
= NOT AUTHORIZED

---

# 25. Conclusion

WP4 Benchmark Source Evidence has materially advanced.

The market identities are no longer unknown.

Official verification sources are known.

A Daily Total Return source candidate is known.

The remaining critical gap is:

DAILY PRICE INDEX SOURCE CONTRACT.

Therefore:

BENCHMARK_SOURCE
= SOURCE_PENDING

SOURCE_ARCHITECTURE
= CANDIDATE

IMPLEMENTATION_GATE
= NOT_AUTHORIZED

REAL_GET
= 0

PRODUCTION_WRITE
= NOT_AUTHORIZED
