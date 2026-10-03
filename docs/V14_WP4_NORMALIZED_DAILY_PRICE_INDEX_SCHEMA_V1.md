# DAVID V14 UNIFIED ENGINE — WP4 NORMALIZED DAILY PRICE INDEX SCHEMA V1

> Work Package: WP4 — Market Context
>
> Document Type: Schema Specification
>
> Parent Specification: V14_WP4_MARKET_CONTEXT_SPEC_V1.md
>
> Parent Benchmark Evidence: V14_WP4_BENCHMARK_SOURCE_EVIDENCE_V1.md
>
> Parent Official-EOD Evidence: V14_WP4_OFFICIAL_EOD_EXCEPTION_EVIDENCE_V1.md
>
> Parent Safety Baseline Commit: a7b880a6b57f00702589ab3b96791796d7f43147
>
> Schema Status: CANDIDATE
>
> Normalization Execution: NOT AUTHORIZED
>
> Official EOD Adapter: NOT AUTHORIZED
>
> Runtime Real GET: 0
>
> Production Write: NOT AUTHORIZED

---

# 1. Purpose

本文件定義 WP4 Daily Benchmark
Normalized Daily Price Index 的候選 Schema。

本文件只定義：

- contract structure
- identity vocabulary
- market-data vocabulary
- metadata vocabulary
- semantic-evidence structure
- required / optional / evidence-pending classification
- TWSE / TPEx mapping candidates
- validation principles
- fail-closed principles

本文件不授權：

- raw-data normalization execution
- Official EOD Adapter implementation
- API execution
- Core input
- Benchmark Engine
- Relative Strength Engine
- Market State output
- Risk
- Action
- Supabase write
- production write

SCHEMA SPECIFICATION
!=
NORMALIZATION AUTHORIZATION

---

# 2. Existing V14 Contract Principles

Existing V14 contracts demonstrate:

1. versioned contracts
2. explicit identity section
3. explicit metadata section
4. fail-closed required-field validation
5. structured contract before storage flattening
6. semantic evidence separated from execution authority

WP4 shall reuse these principles.

Do not create a new incompatible
contract style without evidence.

---

# 3. Contract Name

Candidate contract name:

V14_NORMALIZED_DAILY_PRICE_INDEX_V1

Candidate document-level status:

SCHEMA_STATUS
= CANDIDATE

This name describes the target normalized schema.

It does not authorize production of
normalized output.

ALLOW_NORMALIZED_OUTPUT
= False

---

# 4. Top-Level Structure

Candidate structure:

version

identity

market_data

metadata

semantic_evidence

No storage-specific flattening is defined here.

Future storage representation,
if ever authorized,
must be handled by a separate boundary.

---

# 5. Identity Structure

Candidate:

identity
├─ trading_date
├─ market
├─ index_id
└─ index_name

Identity fields describe
what market index observation
the record represents.

---

# 6. trading_date Vocabulary

WP4 candidate field:

trading_date

Reason:

The newer V14 controlled-real,
baseline evidence,
Golden Evidence,
and semantic-evidence chains
use trading_date.

Existing semantic evidence defines:

TRADING_DATE_SEMANTIC
= TRADING_DATE

TRADING_DATE_EVIDENCE_STATUS
= SEMANTIC_LOCKED

WP4 does not modify older contracts
that use trade_date.

Raw provider fields such as:

date

or

資料日期

must be mapped by a future adapter
only after separate authorization.

---

# 7. market Vocabulary

Candidate values:

TWSE

TPEX

market identifies the market domain
of the benchmark observation.

It does not by itself identify
the benchmark index.

market
!=
index_id

---

# 8. index_id Vocabulary

Listed-market candidate:

index_id
= TAIEX

OTC-market candidate:

index_id
= TPEX

Status:

INDEX_ID_MAPPING
= CANDIDATE

Final source mapping requires
a future mapping contract.

---

# 9. index_name Vocabulary

Candidate examples:

TAIEX

TPEx Capitalization-Weighted Index

index_name is human-readable identity metadata.

It must not replace index_id
as the machine identity.

Status:

INDEX_NAME
= REQUIRED_CANDIDATE

Exact canonical display strings
remain subject to mapping review.

---

# 10. Market Data Structure

Candidate:

market_data
├─ open
├─ high
├─ low
├─ close
└─ change

The schema represents:

DAILY PRICE INDEX DATA

It does not represent:

- Total Return Index
- stock OHLCV
- realtime ticks
- intraday KBar
- normalized stock price data

---

# 11. OHLC Required Candidate

Candidate required fields:

open

high

low

close

Official source evidence supports
Daily Price Index OHLC semantics
for the reviewed TWSE / TPEx
Government Open Data sources.

Status:

OHLC_SCHEMA
= REQUIRED_CANDIDATE

This does not yet authorize
raw-to-normalized transformation.

---

# 12. change Optional Candidate

TPEx reviewed evidence includes
a change field.

A symmetric TWSE field must not
be invented merely for schema symmetry.

Therefore:

market_data.change
= OPTIONAL_CANDIDATE

Missing change
!=
zero change

Missing change
!=
neutral market

---

# 13. Metadata Structure

Candidate:

metadata
├─ provider
├─ source_channel
├─ source_role
├─ license_status
└─ retrieved_at

Metadata describes provenance
and governance.

It must not contain
Market State or trading decisions.

---

# 14. provider Vocabulary

Candidate provider values:

TWSE

TPEX

provider identifies the organization
providing the source dataset.

Do not duplicate provider identity
with an additional ambiguous
source field.

Therefore:

ROOT_SOURCE_FIELD
= NOT_REQUIRED_CANDIDATE

---

# 15. source_channel Vocabulary

For the reviewed exception:

source_channel
= GOVERNMENT_OPEN_DATA

This must remain distinct from:

- DATA_ESHOP
- SUBSCRIBED_MARKET_DATA
- REALTIME_FEED
- WEBPAGE_SCRAPING

OPEN_DATA_CHANNEL
!=
COMMERCIAL_DATA_PRODUCT_CHANNEL

---

# 16. source_role Vocabulary

Candidate:

source_role
= OFFICIAL_EOD_EXCEPTION

Meaning:

This source is authorized only as
a candidate for the scoped
WP4 Daily Benchmark exception.

It does not mean:

GLOBAL_PRIMARY_PROVIDER

FinMind remains the global
Primary General Taiwan Data Provider
under the current architecture.

---

# 17. license_status Vocabulary

For reviewed Government Open Data:

license_status
= GOVERNMENT_OPEN_DATA_LICENSE_V1

This value must be source-channel specific.

It must not be copied to
commercial Data E-Shop products.

UNKNOWN LICENSE
!=
AUTHORIZED USE

Future commercial / redistribution use
may require separate review.

---

# 18. retrieved_at Status

retrieved_at is useful provenance metadata.

However:

Current WP4 evidence does not yet
establish a locked retrieved_at contract.

Therefore:

metadata.retrieved_at
= EVIDENCE_PENDING

It must not be fabricated.

---

# 19. Semantic Evidence Structure

Candidate:

semantic_evidence
├─ index_type
├─ trading_date
├─ ohlc
└─ frequency

Semantic evidence is separated
from ordinary metadata.

This follows the existing V14 principle
that semantic evidence may have
different maturity by domain.

---

# 20. index_type Semantic Evidence

Candidate:

index_type.semantic
= PRICE_INDEX

Candidate evidence status:

index_type.evidence_status
= SEMANTIC_LOCKED_CANDIDATE

Important:

PRICE_INDEX
!=
TOTAL_RETURN_INDEX

No Total Return substitution is authorized.

---

# 21. trading_date Semantic Evidence

Candidate:

trading_date.semantic
= TRADING_DATE

Candidate:

trading_date.evidence_status
= SEMANTIC_LOCKED_CANDIDATE

Timezone remains separately governed.

Candidate:

trading_date.timezone_status
= EVIDENCE_PENDING

Do not silently convert
timezone assumptions into
locked evidence.

---

# 22. OHLC Semantic Evidence

Candidate:

ohlc.semantic_status
= SEMANTIC_LOCKED_CANDIDATE

Candidate policy:

ohlc.zero_missing_policy
= ZERO_IS_NOT_MISSING

Candidate close semantic:

ohlc.close_semantic
= OFFICIAL_EOD_CLOSING_PRICE_INDEX

Missing official close
must not become zero.

Missing official close
must not become previous close.

---

# 23. Frequency Semantic Evidence

Candidate:

frequency.semantic
= DAILY

Candidate:

frequency.evidence_status
= SEMANTIC_LOCKED_CANDIDATE

This schema must not silently accept:

- intraday
- realtime
- 5-second
- minute KBar

as equivalent Daily records.

---

# 24. Required Candidate Fields

Candidate required fields:

version

identity.trading_date

identity.market

identity.index_id

identity.index_name

market_data.open

market_data.high

market_data.low

market_data.close

metadata.provider

metadata.source_channel

metadata.source_role

metadata.license_status

semantic_evidence.index_type

semantic_evidence.trading_date

semantic_evidence.ohlc

semantic_evidence.frequency

Status:

REQUIRED_FIELDS
= CANDIDATE

---

# 25. Optional Candidate Fields

Candidate optional fields:

market_data.change

Reason:

Provider asymmetry must be preserved.

Optional
!=
irrelevant.

Missing
!=
zero.

---

# 26. Evidence-Pending Fields

Evidence-pending candidates:

metadata.retrieved_at

semantic_evidence.trading_date.timezone_status

These fields must not be silently
promoted into locked values.

EVIDENCE_PENDING
!=
SEMANTIC_LOCKED

---

# 27. Missing Data Policy

Candidate fail-closed principles:

Missing trading_date
→ REJECT

Missing market
→ REJECT

Missing index_id
→ REJECT

Missing open
→ REJECT

Missing high
→ REJECT

Missing low
→ REJECT

Missing close
→ REJECT

Missing provider
→ REJECT

Missing source_channel
→ REJECT

Missing license_status
→ REJECT

Missing change
→ ALLOWED

---

# 28. Zero / Missing Policy

Candidate:

ZERO_IS_NOT_MISSING

A numeric zero must not automatically
be converted to missing.

A missing value must not automatically
be converted to zero.

No imputation is authorized
by this schema specification.

---

# 29. Price / Total Return Protection

The schema is for:

PRICE_INDEX

It must reject or isolate:

TOTAL_RETURN_INDEX

unless a future separate contract
explicitly authorizes that index type.

PRICE_INDEX
!=
TOTAL_RETURN_INDEX

TOTAL_RETURN_SUBSTITUTION
= NOT_AUTHORIZED

---

# 30. Provider Mapping Candidate

TWSE candidate:

provider
= TWSE

market
= TWSE

index_id
= TAIEX

source_channel
= GOVERNMENT_OPEN_DATA

source_role
= OFFICIAL_EOD_EXCEPTION


TPEx candidate:

provider
= TPEX

market
= TPEX

index_id
= TPEX

source_channel
= GOVERNMENT_OPEN_DATA

source_role
= OFFICIAL_EOD_EXCEPTION

Status:

PROVIDER_MAPPING
= CANDIDATE

---

# 31. Raw Field Mapping Boundary

This schema does not define
executable raw-field mapping.

Examples such as:

日期
→ trading_date

收盤指數
→ close

資料日期
→ trading_date

收市
→ close

remain:

MAPPING_CANDIDATE

A future Field Mapping Review
must lock provider-specific mapping.

RAW_FIELD_MAPPING_EXECUTION
= NOT_AUTHORIZED

---

# 32. Validation Candidate

Future contract validation should consider:

- top-level type
- version
- required sections
- required identity
- required OHLC
- provider identity
- market identity
- index identity
- Price Index type
- Daily frequency
- source channel
- license status
- numeric validity
- trading-date validity
- missing / zero distinction

Status:

VALIDATION_CONTRACT
= NOT_AUTHORIZED

---

# 33. Storage Boundary

This schema is a structured contract.

It does not define
a database-compatible flattened row.

Future storage flattening,
if ever required,
must be performed by
a separate Storage Adapter boundary.

SCHEMA CONTRACT
!=
STORAGE RECORD

SUPABASE_WRITE
= NOT_AUTHORIZED

---

# 34. Semantic Evidence Maturity

Evidence maturity may differ by domain.

Candidate examples:

index_type
→ SEMANTIC_LOCKED_CANDIDATE

trading_date
→ SEMANTIC_LOCKED_CANDIDATE

ohlc
→ SEMANTIC_LOCKED_CANDIDATE

frequency
→ SEMANTIC_LOCKED_CANDIDATE

timezone
→ EVIDENCE_PENDING

retrieved_at
→ EVIDENCE_PENDING

Therefore:

A single root-level
evidence_status = READY

is not adopted.

---

# 35. Existing Normalization Boundary

Existing V14 market-source safety work
keeps normalized output blocked.

This schema specification does not
override that boundary.

ALLOW_NORMALIZED_OUTPUT
= False

NORMALIZATION_EXECUTION
= NOT_AUTHORIZED

---

# 36. Non-Authorization Boundary

READ_ONLY
= True

ALLOW_NORMALIZED_OUTPUT
= False

ALLOW_CORE_INPUT
= False

ALLOW_SCORE
= False

ALLOW_DECISION
= False

ALLOW_SUPABASE_WRITE
= False

ALLOW_PRODUCTION_WRITE
= False

OFFICIAL_EOD_ADAPTER
= NOT_AUTHORIZED

IMPLEMENTATION_GATE
= NOT_AUTHORIZED

REAL_GET
= 0

---

# 37. Relationship to Parent Evidence

Parent Official-EOD Evidence remains:

WP4_OFFICIAL_EOD_BENCHMARK_EXCEPTION
= STRONG_ARCHITECTURE_CANDIDATE

SOURCE_CHANNEL
= GOVERNMENT_OPEN_DATA

GLOBAL_PRIMARY_PROVIDER
= FINMIND

EXCEPTION_SCOPE
= WP4_DAILY_BENCHMARK_ONLY

This schema document does not
upgrade the architecture candidate
into an activated exception.

---

# 38. Relationship to WP4 Specification

Parent WP4 Specification remains:

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

No Benchmark signal is authorized.

---

# 39. Next Work

After this schema candidate is reviewed:

1. Provider Field Mapping Review
2. Required / Optional validation review
3. Fail-Closed Contract Review
4. Official Verification Policy Review
5. Source Contract Review

Do not proceed directly to
Official EOD Adapter implementation.

---

# 40. Current Status

SCHEMA_NAME
= V14_NORMALIZED_DAILY_PRICE_INDEX_V1

SCHEMA_STATUS
= CANDIDATE

REQUIRED_FIELDS
= CANDIDATE

PROVIDER_MAPPING
= CANDIDATE

RAW_FIELD_MAPPING
= CANDIDATE

TIMEZONE
= EVIDENCE_PENDING

RETRIEVED_AT
= EVIDENCE_PENDING

ALLOW_NORMALIZED_OUTPUT
= False

OFFICIAL_EOD_ADAPTER
= NOT_AUTHORIZED

IMPLEMENTATION_GATE
= NOT_AUTHORIZED

REAL_GET
= 0

PRODUCTION_WRITE
= NOT_AUTHORIZED

---

# 41. Conclusion

WP4 Normalized Daily Price Index
now has a candidate schema structure
aligned with existing V14 contract
and semantic-evidence principles.

The schema remains specification-only.

Therefore:

SCHEMA_STATUS
= CANDIDATE

NORMALIZATION_EXECUTION
= NOT_AUTHORIZED

OFFICIAL_EOD_ADAPTER
= NOT_AUTHORIZED

IMPLEMENTATION_GATE
= NOT_AUTHORIZED

REAL_GET
= 0

PRODUCTION_WRITE
= NOT_AUTHORIZED
