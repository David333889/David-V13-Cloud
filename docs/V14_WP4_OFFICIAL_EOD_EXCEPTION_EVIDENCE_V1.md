# DAVID V14 UNIFIED ENGINE — WP4 OFFICIAL-EOD EXCEPTION EVIDENCE V1

> Work Package: WP4 — Market Context
>
> Document Type: Architecture / Source Evidence Baseline
>
> Parent Specification: V14_WP4_MARKET_CONTEXT_SPEC_V1.md
>
> Parent Benchmark Evidence: V14_WP4_BENCHMARK_SOURCE_EVIDENCE_V1.md
>
> Benchmark Evidence Baseline Commit: 55a65ab7b30dd998a480633f826707309cbaaaf6
>
> Production Implementation: NOT AUTHORIZED
>
> Runtime Real GET Performed By This Evidence Work: 0
>
> Production Write: NOT AUTHORIZED

---

# 1. Purpose

本文件保存 WP4 Daily Benchmark
Official-EOD Exception Architecture Review 的證據與候選結論。

本文件不是：

- provider switch authorization
- global provider-policy replacement
- production implementation
- Official Adapter implementation
- normalization activation
- Benchmark Engine implementation
- Market State activation
- Core input authorization
- production write authorization

本文件的目的為：

FinMind Daily Price Index Gap
→ Exception Trigger
→ TWSE / TPEx Official Open Data Evidence
→ Daily Price Index Semantics
→ License / Usage Evidence
→ Source Channel Separation
→ Scoped Exception Architecture Candidate
→ Normalized Schema Candidate
→ Fail-Closed Boundary
→ Remaining Gap

---

# 2. Existing Global Provider Policy

Existing V14 Master Data Source direction:

FinMind
→ PRIMARY DATA PROVIDER

Yahoo Finance
→ V13 BASELINE / PRICE FALLBACK

TWSE / TPEx
→ OFFICIAL VERIFY SOURCE

Supabase
→ DAVID DATA WAREHOUSE

Important:

This evidence review does not replace
the global provider policy.

GLOBAL_PRIMARY_PROVIDER
= FINMIND

TWSE_GLOBAL_PRIMARY
= NOT_AUTHORIZED

TPEX_GLOBAL_PRIMARY
= NOT_AUTHORIZED

---

# 3. Exception Trigger

Previous Benchmark Source Evidence established:

BENCHMARK_SOURCE
= SOURCE_PENDING

FINMIND_DAILY_PRICE_INDEX
= SOURCE_PENDING

SOURCE_ARCHITECTURE_A1
= CANDIDATE

OFFICIAL_EOD_EXCEPTION
= REVIEW_ONLY

Subsequent public documentation review found:

FinMind can represent
TAIEX / OTC price-index information.

However, the clearest official EOD observation path
through intraday index data is not equivalent to
a dedicated Daily Price Index Dataset.

The strongest FinMind EOD index path also introduces
current-plan compatibility concerns.

Current V14 Master Plan:

FINMIND PLAN
= FREE

Therefore:

A1 Technical Feasibility
= STRONG

A1 Current-Plan Feasibility
= BLOCKED / UNRESOLVED

This triggers:

WP4 Official-EOD Exception Architecture Review.

---

# 4. Exception Scope

The exception candidate is intentionally narrow.

EXCEPTION_SCOPE
= WP4_DAILY_BENCHMARK_ONLY

Allowed evidence scope:

- Listed-market Daily Price Index
- OTC-market Daily Price Index
- Read-only EOD evidence
- Official market-index verification

Not included:

- Chip data
- institutional data
- margin / short
- securities lending
- day trading
- general OHLCV replacement
- V13 Core source replacement
- realtime market context
- Risk V2
- Action V2
- production write

---

# 5. Official Source Channel

The reviewed source channel is:

GOVERNMENT_OPEN_DATA

This is distinct from:

- webpage scraping
- commercial market-data subscription
- Data E-Shop paid products
- realtime feed products

Source channel candidate:

TWSE Government Open Data / OpenAPI

and

TPEx Government Open Data / OpenAPI

Therefore:

OFFICIAL_EOD_SOURCE_CHANNEL
= GOVERNMENT_OPEN_DATA

Status:

STRONG_SOURCE_CANDIDATE

---

# 6. TWSE TAIEX Daily Price Index Evidence

Official open-data evidence identifies:

發行量加權股價指數歷史資料

Data purpose:

TAIEX historical Price Index data.

Documented data content includes:

- date
- opening index
- highest index
- lowest index
- closing index

Update frequency:

DAILY

Cost:

FREE

License:

Government Open Data License
Version 1

Official API / documentation:

TWSE OpenAPI / Swagger

Official OpenAPI separates:

Price Index historical data

from

Total Return Index data.

Therefore:

TWSE_TAIEX_DAILY_PRICE_INDEX
= STRONG_SOURCE_CANDIDATE

TWSE_PRICE_TR_SEPARATION
= STRONG_EVIDENCE

---

# 7. TPEx Daily Price Index Evidence

Official open-data evidence identifies:

櫃買指數歷史資料

Purpose:

End-of-day OTC market index information.

Documented data content includes:

- trading date
- open
- high
- low
- close
- change

Update frequency:

DAILY

Cost:

FREE

License:

Government Open Data License
Version 1

Official API / documentation:

TPEx OpenAPI / Swagger

Therefore:

TPEX_DAILY_PRICE_INDEX
= STRONG_SOURCE_CANDIDATE

TPEX_OFFICIAL_CLOSE_SEMANTICS
= STRONG_EVIDENCE

---

# 8. TPEx Price / Total Return Verification Evidence

Additional official open data provides:

櫃買指數與報酬指數之收市指數

Documented values include:

- trading date
- TPEx Price Index
- TPEx Total Return Index

This provides direct official evidence that:

PRICE_INDEX
!=
TOTAL_RETURN_INDEX

Therefore:

TPEX_PRICE_TR_SEPARATION
= STRONG_EVIDENCE

This evidence is useful for future
benchmark-basis verification.

---

# 9. Source Channel Separation

Official exchange data must distinguish
different distribution channels.

Channel A:

Government Open Data / OpenAPI

Candidate characteristics:

- public open-data dataset
- machine-readable API
- daily data
- free
- Government Open Data License V1

Channel B:

Exchange Data E-Shop /
Subscribed Market Data Products

Candidate characteristics may include:

- subscription
- contract
- fee
- separate usage restrictions
- redistribution restrictions

Therefore:

OPEN_DATA_CHANNEL
!=
COMMERCIAL_DATA_PRODUCT_CHANNEL

V14 must not transfer license assumptions
from one channel to the other.

---

# 10. License / Usage Evidence

For the reviewed Government Open Data datasets:

LICENSE_STATUS
= GOVERNMENT_OPEN_DATA_LICENSE_V1

COST_STATUS
= FREE

PUBLIC_OPEN_DATA
= SUPPORTED

However:

This evidence document does not independently
interpret every future commercial,
redistribution, SaaS, or derivative-data use case.

Future production use must preserve
source-specific license metadata.

COMMERCIAL_REVIEW
= REQUIRED_WHEN_APPLICABLE

REDISTRIBUTION_REVIEW
= REQUIRED_WHEN_APPLICABLE

UNKNOWN FUTURE USE
!=
AUTOMATIC AUTHORIZATION

---

# 11. Scoped Architecture Candidate

Candidate architecture:

TWSE / TPEx Government Open Data
→ Official EOD Adapter
→ Normalized Daily Price Index
→ WP4 Market Context

Scope:

WP4 DAILY BENCHMARK ONLY

This architecture does not replace:

FinMind
→ PRIMARY GENERAL TAIWAN DATA PROVIDER

Therefore:

WP4_OFFICIAL_EOD_BENCHMARK_EXCEPTION
= STRONG_ARCHITECTURE_CANDIDATE

GLOBAL_PRIMARY_PROVIDER
= FINMIND

EXCEPTION_SCOPE
= WP4_DAILY_BENCHMARK_ONLY

---

# 12. Why This Is an Exception

The exception exists because:

1. WP4 requires Daily Price Index evidence.
2. FinMind remains the V14 general Primary Provider.
3. A dedicated FinMind Daily Price Index source
   is not yet locked for the current V14 plan.
4. Official Government Open Data provides
   direct Daily Price Index evidence.
5. Official open-data licensing is explicitly identified.
6. The exception can remain narrow and read-only.

Therefore:

This is a scoped source exception.

It is not a global provider-policy change.

---

# 13. Normalized Schema Candidate

Candidate name:

NormalizedDailyPriceIndexV1

Candidate fields:

trading_date

market

index_id

index_name

open

high

low

close

change

index_type

frequency

timezone

source

source_channel

source_role

license_status

retrieved_at

evidence_status

Candidate constants:

index_type
= PRICE_INDEX

frequency
= DAILY

timezone
= Asia/Taipei

source_channel
= GOVERNMENT_OPEN_DATA

source_role
= OFFICIAL_EOD_EXCEPTION

Status:

NORMALIZED_DAILY_PRICE_INDEX_SCHEMA
= CANDIDATE

SCHEMA_LOCK
= NOT_AUTHORIZED

---

# 14. Listed Market Mapping Candidate

Listed-market candidate:

market
= TWSE

index_id
= TAIEX

index_type
= PRICE_INDEX

frequency
= DAILY

source
= TWSE

source_channel
= GOVERNMENT_OPEN_DATA

Status:

TWSE_DAILY_MAPPING
= CANDIDATE

---

# 15. OTC Market Mapping Candidate

OTC-market candidate:

market
= TPEX

index_id
= TPEX

index_type
= PRICE_INDEX

frequency
= DAILY

source
= TPEX

source_channel
= GOVERNMENT_OPEN_DATA

Status:

TPEX_DAILY_MAPPING
= CANDIDATE

---

# 16. Close Semantics

A future Official EOD Adapter must not infer
the closing index from arbitrary webpage position.

Required semantics:

trading_date
→ official trading date

index_id
→ formally mapped index identity

index_type
→ PRICE_INDEX

close
→ official end-of-day closing index value

timezone
→ Asia/Taipei

frequency
→ DAILY

Price Index
must not be confused with
Total Return Index.

---

# 17. Missing / Stale / Invalid Evidence Policy

Candidate fail-closed policy:

Wrong trading date
→ REJECT

Unknown index identity
→ REJECT

Missing official close
→ REJECT

Invalid numeric value
→ REJECT

Price / Total-Return ambiguity
→ REJECT

Stale data
→ REJECT

Schema drift
→ REJECT

Unknown source channel
→ REJECT

Unknown license state
→ NO ACTIVATION

Official source unavailable
→ NO BENCHMARK INPUT

---

# 18. No Automatic Fallback

This review does not authorize:

TWSE unavailable
→ Yahoo

TPEx unavailable
→ Yahoo

Official source unavailable
→ FinMind intraday aggregation

Official source unavailable
→ Total Return substitution

No fallback path may be created
without a separate explicit contract.

OFFICIAL_EOD_FALLBACK
= NOT_AUTHORIZED

---

# 19. Adapter Boundary

Future Official EOD Adapter responsibilities
may include:

- source-specific field mapping
- date normalization
- numeric validation
- index identity validation
- Price Index validation
- source metadata
- license metadata
- evidence-state mapping

Future Official EOD Adapter must not:

- calculate Market State
- calculate Relative Strength
- modify V13 Core
- score
- decide
- emit Action
- write production data without separate authority

OFFICIAL_EOD_ADAPTER
= NOT_AUTHORIZED

---

# 20. Verification Policy Candidate

Future source verification should consider:

- trading-date match
- index identity match
- Price Index type match
- close-value semantics
- timezone match
- missing-data state
- schema version
- source-channel identity
- license metadata

Verification tolerance for numeric comparison:

SPEC_PENDING

Official cross-source comparison policy:

SPEC_PENDING

---

# 21. Relationship to FinMind

FinMind remains:

PRIMARY GENERAL TAIWAN DATA PROVIDER

This exception does not declare:

FINMIND FAILED

or

FINMIND INVALID

The exception exists only because:

WP4 Daily Benchmark
has a specific Daily Price Index requirement

and

Official Government Open Data
provides a strong fit for that narrow requirement.

---

# 22. Relationship to Yahoo

Yahoo remains:

V13 BASELINE / PRICE FALLBACK

This review does not authorize:

YAHOO_WP4_BENCHMARK_PRIMARY

or

YAHOO_OFFICIAL_EOD_FALLBACK

Both remain:

NOT_AUTHORIZED

---

# 23. Relationship to WP4 Specification V1

Parent specification remains unchanged.

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

This Evidence V1 does not silently modify
the parent specification.

---

# 24. Architecture Status

Evidence review supports:

WP4_OFFICIAL_EOD_BENCHMARK_EXCEPTION
= STRONG_ARCHITECTURE_CANDIDATE

Official source identity
= STRONG

Daily frequency
= STRONG

Price Index semantics
= STRONG

Official close semantics
= STRONG

Machine-readable API
= STRONG

Government Open Data license
= STRONG

Listed coverage
= STRONG

OTC coverage
= STRONG

Normalized schema
= CANDIDATE

Adapter contract
= NOT_AUTHORIZED

Implementation
= NOT_AUTHORIZED

---

# 25. Non-Authorization Boundary

This document does not authorize:

- production Python implementation
- Official Adapter implementation
- Runner integration
- live API execution
- V14 Real GET
- normalization activation
- provider switch
- Core input
- Benchmark Engine
- Relative Strength Engine
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

# 26. Next Work

Next specification work should be:

1. Normalized Daily Price Index Schema Review
2. Official EOD Adapter Boundary Review
3. Field Mapping Review
4. Fail-Closed Contract Review
5. Official Verification Policy Review
6. Only then consider Source Contract Lock

Do not proceed directly to:

- Benchmark Engine
- Relative Strength Engine
- Market State Engine

---

# 27. Current Continuation Point

Parent Benchmark Evidence Baseline:

55a65ab7b30dd998a480633f826707309cbaaaf6

Parent Safety Tag:

v14-wp4-benchmark-source-evidence-v1-safe

Current Evidence Work:

Official-EOD Exception Architecture Review

Production Code Change:

0

Runner Change:

0

V14 Real GET:

0

---

# 28. Conclusion

WP4 Official-EOD Exception Review has
materially advanced.

Official Government Open Data provides
strong Daily Price Index evidence for:

TAIEX

and

TPEx / OTC.

The exception remains narrow:

WP4 DAILY BENCHMARK ONLY.

Therefore:

WP4_OFFICIAL_EOD_BENCHMARK_EXCEPTION
= STRONG_ARCHITECTURE_CANDIDATE

SOURCE_CHANNEL
= GOVERNMENT_OPEN_DATA

NORMALIZED_SCHEMA
= CANDIDATE

OFFICIAL_EOD_ADAPTER
= NOT_AUTHORIZED

IMPLEMENTATION_GATE
= NOT_AUTHORIZED

REAL_GET
= 0

PRODUCTION_WRITE
= NOT_AUTHORIZED
