# DAVID V14 UNIFIED ENGINE — WP4 OFFICIAL EOD FIELD MAPPING V1

> Work Package: WP4 — Market Context
>
> Document Type: Provider Field Mapping Specification
>
> Parent Schema: V14_WP4_NORMALIZED_DAILY_PRICE_INDEX_SCHEMA_V1.md
>
> Parent Schema Safety Baseline:
> 99716e91e0488bbd52c93671d76c8cf51333385e
>
> Field Mapping Status: CANDIDATE
>
> Raw Field Mapping Execution: NOT AUTHORIZED
>
> Normalized Output: NOT AUTHORIZED
>
> Official EOD Adapter: NOT AUTHORIZED
>
> Market Data Real GET: 0
>
> Production Write: NOT AUTHORIZED

---

# 1. Purpose

本文件定義 WP4 Official-EOD
Provider Field Mapping 候選規格。

本文件建立三層 mapping model：

Official Display Label
→ Raw Machine Key
→ V14 Canonical Field

本文件保存：

- TWSE display-schema evidence
- TWSE machine-key evidence maturity
- TPEx display-schema evidence
- TPEx machine-key evidence gap
- canonical mapping targets
- provider asymmetry
- date-format evidence gap
- missing / zero policy
- Price Index protection
- fail-closed mapping principles

本文件不執行：

- provider API request
- raw-data transformation
- normalization
- Official EOD Adapter
- Core input
- Benchmark Engine
- Relative Strength
- Market State
- persistence
- production write

---

# 2. Parent Schema

Parent contract candidate:

V14_NORMALIZED_DAILY_PRICE_INDEX_V1

Top-level structure:

version

identity

market_data

metadata

semantic_evidence

Parent Schema Status:

CANDIDATE

This mapping specification
does not upgrade the parent schema.

---

# 3. Mapping Evidence Vocabulary

VERIFIED

Direct official evidence supports
the stated identity or display schema.

STRONG_CANDIDATE

Evidence strongly supports the mapping,
but the exact machine-schema property
has not been locked by direct official
schema-property evidence.

CANDIDATE

A mapping target is supported by
current architecture and semantics,
but remains specification-level.

EVIDENCE_PENDING

Evidence is insufficient to lock
the stated property or transformation.

NOT_AUTHORIZED

Execution or authority is explicitly blocked.

---

# 4. Three-Layer Mapping Model

Every provider mapping should distinguish:

Layer 1
Official Display Label

Layer 2
Raw Machine Key

Layer 3
V14 Canonical Field

Therefore:

DISPLAY_LABEL
!=
MACHINE_KEY

MACHINE_KEY
!=
CANONICAL_FIELD

A human-readable field description
must not be silently treated as
an executable JSON property name.

---

# 5. Current Implementation Inventory

Repository review found:

TWSE raw-field mapping implementation
= NOT_ESTABLISHED

TPEx raw-field mapping implementation
= NOT_ESTABLISHED

TWSE mapping regression contract
= NOT_ESTABLISHED

TPEx mapping regression contract
= NOT_ESTABLISHED

Existing Chip Adapter usage of:

market = TWSE

is market metadata only.

It is not Daily Price Index
raw-field mapping evidence.

---

# 6. TWSE Dataset Evidence

Official dataset:

發行量加權股價指數歷史資料

Official semantic purpose:

TAIEX historical Daily Price Index data.

Official display fields:

日期

開盤指數

最高指數

最低指數

收盤指數

Update frequency:

DAILY

Source channel:

GOVERNMENT_OPEN_DATA

Provider:

TWSE

License:

GOVERNMENT_OPEN_DATA_LICENSE_V1

---

# 7. TWSE Endpoint Evidence

Official endpoint evidence supports:

GET /indicesReport/MI_5MINS_HIST

Purpose:

發行量加權股價指數歷史資料

Price Index endpoint
is distinct from
Total Return Index endpoint.

Therefore:

TWSE_EXACT_ENDPOINT
= VERIFIED

TWSE_PRICE_TR_ENDPOINT_SEPARATION
= VERIFIED

---

# 8. TWSE Display Schema Status

TWSE official display schema:

日期

開盤指數

最高指數

最低指數

收盤指數

Status:

TWSE_DISPLAY_SCHEMA
= VERIFIED

---

# 9. TWSE Machine-Key Evidence

Current evidence strongly suggests:

日期
→ Date

開盤指數
→ OpeningIndex

最高指數
→ HighestIndex

最低指數
→ LowestIndex

收盤指數
→ ClosingIndex

However:

The current evidence does not justify
promoting these machine properties
to direct official-schema LOCK.

Therefore:

TWSE_MACHINE_KEYS
= STRONG_CANDIDATE

Not:

VERIFIED

Not:

LOCKED

---

# 10. TWSE Canonical Mapping Candidate

Candidate mapping:

Official Display:
日期

Machine Key:
Date

Machine-Key Status:
STRONG_CANDIDATE

Canonical Target:
identity.trading_date

Canonical Status:
CANDIDATE


Official Display:
開盤指數

Machine Key:
OpeningIndex

Machine-Key Status:
STRONG_CANDIDATE

Canonical Target:
market_data.open

Canonical Status:
CANDIDATE


Official Display:
最高指數

Machine Key:
HighestIndex

Machine-Key Status:
STRONG_CANDIDATE

Canonical Target:
market_data.high

Canonical Status:
CANDIDATE


Official Display:
最低指數

Machine Key:
LowestIndex

Machine-Key Status:
STRONG_CANDIDATE

Canonical Target:
market_data.low

Canonical Status:
CANDIDATE


Official Display:
收盤指數

Machine Key:
ClosingIndex

Machine-Key Status:
STRONG_CANDIDATE

Canonical Target:
market_data.close

Canonical Status:
CANDIDATE

---

# 11. TWSE change Policy

Current parent schema defines:

market_data.change
= OPTIONAL_CANDIDATE

No symmetric TWSE change field
shall be invented merely to match TPEx.

Therefore:

TWSE_CHANGE_MAPPING
= NOT_ESTABLISHED

Missing TWSE change
!=
zero change

Missing TWSE change
!=
neutral market

---

# 12. TWSE Date Evidence

Official display evidence demonstrates
ROC-calendar date presentation.

Example semantic form:

ROC year / month / day

However:

Display-format evidence
does not automatically prove
the exact JSON machine-value format.

Therefore:

TWSE_DISPLAY_DATE_FORMAT
= ROC_DATE_EVIDENCE

TWSE_RAW_DATE_VALUE_FORMAT
= EVIDENCE_PENDING

No date conversion is authorized
by this specification.

---

# 13. TPEx Dataset Evidence

Official dataset:

櫃買指數歷史資料

Official semantic purpose:

Daily / EOD OTC Price Index information.

Official display fields:

資料日期

開市

最高價

最低價

收市

漲跌

Update frequency:

DAILY

Source channel:

GOVERNMENT_OPEN_DATA

Provider:

TPEX

License:

GOVERNMENT_OPEN_DATA_LICENSE_V1

---

# 14. TPEx OAS Evidence

Official documentation identifies
TPEx OpenAPI / Swagger availability.

Therefore:

TPEX_OAS_EXISTENCE
= VERIFIED

However:

Static retrieval of the official Swagger
from the current research environment
was blocked.

The exact machine properties
were not directly established.

Therefore:

TPEX_EXACT_ENDPOINT
= EVIDENCE_PENDING

TPEX_MACHINE_KEYS
= EVIDENCE_PENDING

---

# 15. TPEx Display Schema Status

Official display schema:

資料日期

開市

最高價

最低價

收市

漲跌

Status:

TPEX_DISPLAY_SCHEMA
= VERIFIED

---

# 16. TPEx Canonical Mapping Candidate

Official Display:
資料日期

Machine Key:
EVIDENCE_PENDING

Canonical Target:
identity.trading_date

Canonical Status:
CANDIDATE


Official Display:
開市

Machine Key:
EVIDENCE_PENDING

Canonical Target:
market_data.open

Canonical Status:
CANDIDATE


Official Display:
最高價

Machine Key:
EVIDENCE_PENDING

Canonical Target:
market_data.high

Canonical Status:
CANDIDATE


Official Display:
最低價

Machine Key:
EVIDENCE_PENDING

Canonical Target:
market_data.low

Canonical Status:
CANDIDATE


Official Display:
收市

Machine Key:
EVIDENCE_PENDING

Canonical Target:
market_data.close

Canonical Status:
CANDIDATE


Official Display:
漲跌

Machine Key:
EVIDENCE_PENDING

Canonical Target:
market_data.change

Canonical Status:
OPTIONAL_CANDIDATE

---

# 17. TPEx Machine-Key Protection

Third-party naming patterns
must not be promoted into
official index machine-key evidence.

For example:

Open

High

Low

Close

Change

may appear in other contexts.

But:

OTHER ENDPOINT NAMING
!=
OFFICIAL INDEX ENDPOINT CONTRACT

Therefore:

TPEX_MACHINE_KEYS
remain:

EVIDENCE_PENDING

---

# 18. TPEx Date Format

Current evidence does not lock
the exact raw machine date format
for the target index endpoint.

Therefore:

TPEX_RAW_DATE_VALUE_FORMAT
= EVIDENCE_PENDING

No ROC-to-Gregorian conversion
is authorized by this document.

No ISO-date conversion
is authorized by this document.

---

# 19. Provider Asymmetry

Provider differences must be preserved.

TWSE:

change
= NOT_ESTABLISHED

TPEx:

change
= OPTIONAL_CANDIDATE

Therefore:

PROVIDER_ASYMMETRY
= PRESERVED

Schema symmetry must not override
source evidence.

---

# 20. Canonical Identity Constants

TWSE candidate identity:

market
= TWSE

index_id
= TAIEX

provider
= TWSE


TPEx candidate identity:

market
= TPEX

index_id
= TPEX

provider
= TPEX

Status:

IDENTITY_CONSTANTS
= CANDIDATE

---

# 21. Source Governance Constants

For reviewed datasets:

source_channel
= GOVERNMENT_OPEN_DATA

source_role
= OFFICIAL_EOD_EXCEPTION

license_status
= GOVERNMENT_OPEN_DATA_LICENSE_V1

Status:

SOURCE_GOVERNANCE
= CANDIDATE

These constants apply only
to the reviewed Open Data channel.

They must not be copied to:

Data E-Shop

Subscribed Market Data

Realtime Feed

Commercial Data Product

---

# 22. Price Index Protection

Target mapping is for:

PRICE_INDEX

Not:

TOTAL_RETURN_INDEX

Therefore:

INDEX_TYPE
= PRICE_INDEX

TOTAL_RETURN_SUBSTITUTION
= NOT_AUTHORIZED

TWSE Price Index and
Total Return endpoints
must remain separated.

TPEx Price Index and
Total Return evidence
must remain separated.

---

# 23. Numeric Representation

Current mapping evidence
does not yet lock:

- raw numeric JSON type
- string-to-decimal conversion
- comma removal
- decimal precision
- rounding policy

Therefore:

RAW_NUMERIC_TYPE
= EVIDENCE_PENDING

NUMERIC_CONVERSION
= NOT_AUTHORIZED

ROUNDING_POLICY
= SPEC_PENDING

---

# 24. Missing / Zero Policy

Existing V14 semantic principle:

ZERO_IS_NOT_MISSING

This mapping specification preserves:

missing
!=
zero

zero
!=
missing

Missing required raw value
must not silently become zero.

No imputation is authorized.

---

# 25. Required Mapping Candidate

Required canonical targets:

identity.trading_date

market_data.open

market_data.high

market_data.low

market_data.close

Provider constants:

identity.market

identity.index_id

metadata.provider

metadata.source_channel

metadata.source_role

metadata.license_status

Status:

REQUIRED_MAPPING
= CANDIDATE

---

# 26. Optional Mapping Candidate

Optional canonical target:

market_data.change

Current provider support:

TWSE
→ NOT_ESTABLISHED

TPEx
→ OPTIONAL_CANDIDATE

Status:

OPTIONAL_MAPPING
= CANDIDATE

---

# 27. Evidence-Pending Mapping Items

Evidence-pending:

TWSE raw date value format

TPEx exact endpoint

TPEx machine keys

TPEx raw date value format

raw numeric type

numeric conversion

rounding policy

These gaps must remain explicit.

EVIDENCE_PENDING
!=
VERIFIED

---

# 28. Fail-Closed Mapping Principles

Unknown machine key
→ NO EXECUTION

Unknown date format
→ NO DATE CONVERSION

Unknown numeric representation
→ NO NUMERIC CONVERSION

Missing required field
→ REJECT

Unknown index identity
→ REJECT

Price / Total Return ambiguity
→ REJECT

Unknown source channel
→ REJECT

Unknown license state
→ NO ACTIVATION

Schema drift
→ REJECT

---

# 29. No Executable Mapping

This specification does not create:

- Python mapping dictionary
- adapter function
- provider parser
- date converter
- numeric converter
- normalization function
- runtime path

Therefore:

RAW_FIELD_MAPPING_EXECUTION
= NOT_AUTHORIZED

---

# 30. Relationship to Parent Schema

Parent:

V14_NORMALIZED_DAILY_PRICE_INDEX_V1

remains:

SCHEMA_STATUS
= CANDIDATE

ALLOW_NORMALIZED_OUTPUT
= False

This mapping document
does not change that authority.

---

# 31. Relationship to Official-EOD Exception

Parent architecture remains:

WP4_OFFICIAL_EOD_BENCHMARK_EXCEPTION
= STRONG_ARCHITECTURE_CANDIDATE

EXCEPTION_SCOPE
= WP4_DAILY_BENCHMARK_ONLY

GLOBAL_PRIMARY_PROVIDER
= FINMIND

This field mapping specification
does not activate the exception.

---

# 32. Documentation Acquisition Boundary

This review used external
documentation research only.

DAVID local documentation fetch:

0

Market Data Real GET:

0

No new local Internet Crossing path
was created.

LOCAL_DOCUMENTATION_FETCH
= 0

MARKET_DATA_REAL_GET
= 0

---

# 33. Non-Authorization Boundary

READ_ONLY
= True

FIELD_MAPPING_STATUS
= CANDIDATE

RAW_FIELD_MAPPING_EXECUTION
= NOT_AUTHORIZED

ALLOW_NORMALIZED_OUTPUT
= False

NORMALIZATION_EXECUTION
= NOT_AUTHORIZED

OFFICIAL_EOD_ADAPTER
= NOT_AUTHORIZED

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

IMPLEMENTATION_GATE
= NOT_AUTHORIZED

REAL_GET
= 0

PRODUCTION_WRITE
= NOT_AUTHORIZED

---

# 34. Current Evidence Status

TWSE_DISPLAY_SCHEMA
= VERIFIED

TWSE_EXACT_ENDPOINT
= VERIFIED

TWSE_MACHINE_KEYS
= STRONG_CANDIDATE

TWSE_RAW_DATE_VALUE_FORMAT
= EVIDENCE_PENDING

TPEX_DISPLAY_SCHEMA
= VERIFIED

TPEX_OAS_EXISTENCE
= VERIFIED

TPEX_EXACT_ENDPOINT
= EVIDENCE_PENDING

TPEX_MACHINE_KEYS
= EVIDENCE_PENDING

TPEX_RAW_DATE_VALUE_FORMAT
= EVIDENCE_PENDING

CANONICAL_MAPPING_TARGETS
= CANDIDATE

RAW_NUMERIC_TYPE
= EVIDENCE_PENDING

---

# 35. Next Work

After this mapping candidate is reviewed:

1. Mapping Safety Review
2. Required / Optional Mapping Validation Review
3. Fail-Closed Contract Review
4. Official Verification Policy Review
5. Source Contract Review

Do not proceed directly to:

- executable mapping
- Official EOD Adapter
- normalization runtime
- Benchmark Engine

---

# 36. Current Continuation Point

Parent Schema Safety Baseline:

99716e91e0488bbd52c93671d76c8cf51333385e

Parent Safety Tag:

v14-wp4-normalized-daily-price-index-schema-v1-safe

Production Code Change:

0

Runner Change:

0

Market Data Real GET:

0

---

# 37. Conclusion

WP4 Official-EOD Provider Field Mapping
now has a candidate specification
that preserves asymmetric evidence maturity.

TWSE:

Display Schema
= VERIFIED

Exact Endpoint
= VERIFIED

Machine Keys
= STRONG_CANDIDATE

TPEx:

Display Schema
= VERIFIED

OAS Existence
= VERIFIED

Machine Keys
= EVIDENCE_PENDING

Therefore:

FIELD_MAPPING_STATUS
= CANDIDATE

RAW_FIELD_MAPPING_EXECUTION
= NOT_AUTHORIZED

ALLOW_NORMALIZED_OUTPUT
= False

OFFICIAL_EOD_ADAPTER
= NOT_AUTHORIZED

REAL_GET
= 0

PRODUCTION_WRITE
= NOT_AUTHORIZED
