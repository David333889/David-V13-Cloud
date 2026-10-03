# DAVID V14 UNIFIED ENGINE — WP4 OFFICIAL EOD VERIFICATION POLICY V1

> Work Package: WP4 — Market Context
>
> Document Type: Official Verification Policy Specification
>
> Parent Validation:
> V14_WP4_OFFICIAL_EOD_MAPPING_VALIDATION_V1.md
>
> Parent Validation Safety Baseline:
> c7fcc0d64cc4753f9f273167952841e5cf5242d8
>
> Parent Safety Tag:
> v14-wp4-official-eod-mapping-validation-v1-safe
>
> Verification Policy Status: CANDIDATE
>
> Verification Execution: NOT AUTHORIZED
>
> Official EOD Adapter: NOT AUTHORIZED
>
> Market Data Real GET: 0
>
> Production Write: NOT AUTHORIZED

---

# 1. Purpose

本文件定義 WP4 Official-EOD
Official Verification Policy V1 候選規格。

本文件定義：

- provenance requirement
- verification dimensions
- VERIFIED / BLOCKED vocabulary
- stale-data policy
- Price Index protection
- source-channel verification
- license verification
- schema-drift protection
- numeric-comparison pending policy
- cross-source-comparison pending policy
- non-authorization boundary

VERIFICATION POLICY
!=
VERIFICATION EXECUTION

---

# 2. Existing V14 Verification Principles

NO VERIFIED EVIDENCE
=
NO LOCK

PENDING
!=
VERIFIED

STRONG_CANDIDATE
!=
VERIFIED

READY
!=
VERIFIED

HTTP SUCCESS
!=
VERIFIED

No candidate status may be silently
promoted to VERIFIED.

---

# 3. Contract Name

V14_WP4_OFFICIAL_EOD_VERIFICATION_POLICY_V1

VERIFICATION_POLICY_STATUS
= CANDIDATE

VERIFICATION_EXECUTION
= NOT_AUTHORIZED

---

# 4. Verification Architecture

Official verification uses:

Multi-Dimensional Evidence
+
Final Aggregation

Official Source Evidence
→ Provenance Evidence
→ Trading-Date Verification
→ Index Identity Verification
→ Price Index Type Verification
→ Close Semantic Verification
→ Timezone Verification
→ Missing-Data Verification
→ Schema-Version Verification
→ Source-Channel Verification
→ License Verification
→ Freshness / Stale Verification
→ Final Verification Result

---

# 5. Verification Result Vocabulary

Candidate final status:

VERIFIED

or:

BLOCKED

PARTIAL_VERIFIED
= NOT_ADOPTED

---

# 6. VERIFIED Meaning

VERIFIED means all required verification
dimensions have sufficient evidence and pass.

OFFICIAL_VERIFIED
!=
NORMALIZATION_AUTHORIZED

OFFICIAL_VERIFIED
!=
ADAPTER_AUTHORIZED

OFFICIAL_VERIFIED
!=
CORE_INPUT_AUTHORIZED

OFFICIAL_VERIFIED
!=
BENCHMARK_INPUT_AUTHORIZED

---

# 7. BLOCKED Meaning

BLOCKED means at least one required
verification dimension is invalid,
unresolved, stale, ambiguous,
unavailable, or evidence-pending.

BLOCKED
= FAIL_CLOSED

---

# 8. Provenance Requirement

PROVENANCE_REQUIRED
= True

PROVENANCE_REQUIRED_FIELDS
=
provider
dataset
status_code
content_type
payload_hash

---

# 9. Payload Hash

PAYLOAD_HASH
= SHA256

Payload hash supports:

- evidence identity
- reproducibility
- change detection
- Golden Evidence traceability

PAYLOAD_HASH
!=
SEMANTIC_VERIFICATION

---

# 10. Secret Protection

SECRET_IN_PROVENANCE
= PROHIBITED

No token, authorization header,
secret, or credential may be stored
inside verification provenance.

---

# 11. Source Provenance

SOURCE_PROVENANCE_REQUIRED
= True

Source provenance may describe:

- provider
- dataset
- source channel
- documented endpoint identity
- fetch-path identity
- schema identity

EXECUTABLE_FETCH_PATH
= NOT_AUTHORIZED

---

# 12. Verification Dimensions

Nine core dimensions are preserved:

1. trading-date match
2. index identity match
3. Price Index type match
4. close-value semantics
5. timezone match
6. missing-data state
7. schema version
8. source-channel identity
9. license metadata

VERIFICATION_DIMENSIONS
= 9

---

# 13. Trading-Date Verification

Wrong trading date:

→ BLOCKED

TRADING_DATE_MISMATCH

No implicit date conversion
is authorized.

---

# 14. Index Identity Verification

Unknown or conflicting identity:

→ BLOCKED

INDEX_IDENTITY_MISMATCH

No identity inference from price values
is authorized.

---

# 15. Price Index Type Verification

INDEX_TYPE
= PRICE_INDEX

Price Index
must not be confused with:

TOTAL_RETURN_INDEX

Wrong or ambiguous index type:

→ BLOCKED

INDEX_TYPE_MISMATCH

TOTAL_RETURN_SUBSTITUTION
= NOT_AUTHORIZED

---

# 16. Close-Value Semantic Verification

Official close must represent
the intended Daily Price Index
closing value.

Missing official close:

→ BLOCKED

Ambiguous close semantics:

→ BLOCKED

CLOSE_SEMANTIC_MISMATCH

No previous-close substitution
is authorized.

---

# 17. Timezone Verification

Timezone semantics must be
formally supported by evidence.

Current unresolved timezone:

→ BLOCKED

TIMEZONE_EVIDENCE_PENDING

No silent timezone assumption
is authorized.

---

# 18. Missing-Data Verification

MISSING
!=
ZERO

MISSING
!=
NEUTRAL

ZERO
!=
MISSING

Required missing data:

→ BLOCKED

Optional missing data may remain
represented as missing only when
the parent contract explicitly permits it.

No missing-value fabrication
is authorized.

---

# 19. Schema-Version Verification

Provider schema must match
the verified / expected schema basis.

Schema mismatch:

→ BLOCKED

SCHEMA_VERSION_MISMATCH

Schema drift:

→ BLOCKED

SCHEMA_DRIFT

Automatic remapping
is not authorized.

---

# 20. Source-Channel Verification

Current Official-EOD exception
is scoped to:

GOVERNMENT_OPEN_DATA

If source channel differs:

→ BLOCKED

SOURCE_CHANNEL_MISMATCH

Government Open Data
must remain distinct from:

- Data E-Shop
- subscribed market data
- commercial data product
- realtime feed

---

# 21. License Verification

For reviewed Open Data sources,
license status must be known
and supported by evidence.

Unknown license:

→ BLOCKED
→ NO ACTIVATION

LICENSE_STATUS_UNKNOWN

Unknown license
must not become authorized use.

---

# 22. Freshness / Stale Verification

Parent WP4 policy:

STALE DATA
→ REJECT

Therefore:

STALE_POLICY
= FAIL_CLOSED

Stale evidence:

→ BLOCKED

STALE_DATA

Exact freshness threshold
has not been formally locked.

FRESHNESS_THRESHOLD
= SPEC_PENDING

No arbitrary threshold
is introduced here.

---

# 23. Official Source Availability

If official source
is unavailable:

→ NO BENCHMARK INPUT

verification_status
= BLOCKED

OFFICIAL_SOURCE_UNAVAILABLE

No automatic replacement source
is authorized by this policy.

---

# 24. Invalid Numeric Evidence

Invalid numeric value:

→ BLOCKED

Current:

RAW_NUMERIC_TYPE
= EVIDENCE_PENDING

NUMERIC_CONVERSION
= NOT_AUTHORIZED

Numeric verification
cannot yet be executable.

---

# 25. Numeric Comparison Tolerance

Verification tolerance
for numeric comparison:

SPEC_PENDING

Therefore:

NUMERIC_COMPARISON_TOLERANCE
= SPEC_PENDING

No numeric tolerance
may be invented here.

---

# 26. Numeric Comparison Verification

Until numeric tolerance
is formally locked:

NUMERIC_COMPARISON_VERIFICATION
= BLOCKED

NUMERIC_TOLERANCE_SPEC_PENDING

This policy does not perform
cross-source numeric comparison.

---

# 27. Cross-Source Comparison Policy

Official cross-source comparison policy:

SPEC_PENDING

Therefore:

CROSS_SOURCE_COMPARISON_POLICY
= SPEC_PENDING

CROSS_SOURCE_POLICY_SPEC_PENDING

No FinMind / TWSE / TPEx
cross-source equality rule
is created here.

---

# 28. Transport Success Is Insufficient

The following are not sufficient
for VERIFIED:

HTTP 200

application/json

non-empty payload

valid JSON

known provider name

known dataset name

HTTP_SUCCESS
!=
OFFICIAL_VERIFIED

---

# 29. Provenance vs Verification

Provenance answers:

Where did this evidence come from?

Verification answers:

Does this evidence satisfy
the official semantic contract?

PROVENANCE_READY
!=
OFFICIAL_VERIFIED

Both are required,
but they are not equivalent.

---

# 30. Validation vs Verification

Mapping Validation asks:

Is the mapping record structurally
acceptable under its contract?

Official Verification asks:

Is the source evidence officially
supported in identity, semantics,
date, provenance, governance,
and integrity?

VALIDATION_READY
!=
OFFICIAL_VERIFIED

---

# 31. Verification vs Implementation

Even when future evidence becomes:

OFFICIAL_VERIFIED

this policy does not automatically allow:

- raw mapping execution
- date conversion
- numeric conversion
- normalization
- Official EOD Adapter
- Core input
- Benchmark input
- production write

Separate authority is required.

---

# 32. Candidate Verification Envelope

Candidate structure:

version

verification_status

reason

provenance

verification

No executable implementation
is created by this document.

---

# 33. Candidate Provenance Structure

provenance
├─ provider
├─ dataset
├─ status_code
├─ content_type
└─ payload_hash

PROVENANCE_SCHEMA
= CANDIDATE

---

# 34. Candidate Verification Structure

verification
├─ trading_date
├─ index_identity
├─ price_index_type
├─ close_value_semantics
├─ timezone
├─ missing_data
├─ schema_version
├─ source_channel
└─ license_metadata

VERIFICATION_SCHEMA
= CANDIDATE

---

# 35. Candidate Successful Result

Future candidate:

verification_status
= VERIFIED

reason
= OK

Only when all required verification
dimensions are formally supported
and pass.

Current providers do not yet
meet this condition.

---

# 36. Candidate Blocked Result

Candidate:

verification_status
= BLOCKED

reason
= specific fail-closed reason

No authorized benchmark payload
is emitted by this policy.

---

# 37. Reason Vocabulary

Candidate reasons:

OK

PROVENANCE_MISSING

TRADING_DATE_MISMATCH

INDEX_IDENTITY_MISMATCH

INDEX_TYPE_MISMATCH

CLOSE_SEMANTIC_MISMATCH

TIMEZONE_EVIDENCE_PENDING

MISSING_DATA_INVALID

SCHEMA_VERSION_MISMATCH

SCHEMA_DRIFT

SOURCE_CHANNEL_MISMATCH

LICENSE_STATUS_UNKNOWN

STALE_DATA

OFFICIAL_SOURCE_UNAVAILABLE

NUMERIC_TOLERANCE_SPEC_PENDING

CROSS_SOURCE_POLICY_SPEC_PENDING

Reason vocabulary remains
specification-level.

---

# 38. TWSE Current Verification Readiness

Current evidence:

TWSE_DISPLAY_SCHEMA
= VERIFIED

TWSE_EXACT_ENDPOINT
= VERIFIED

TWSE_MACHINE_KEYS
= STRONG_CANDIDATE

TWSE_RAW_DATE_VALUE_FORMAT
= EVIDENCE_PENDING

RAW_NUMERIC_TYPE
= EVIDENCE_PENDING

NUMERIC_COMPARISON_TOLERANCE
= SPEC_PENDING

Therefore:

TWSE_OFFICIAL_VERIFICATION
= BLOCKED

No VERIFIED promotion
is authorized.

---

# 39. TPEx Current Verification Readiness

Current evidence:

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

RAW_NUMERIC_TYPE
= EVIDENCE_PENDING

NUMERIC_COMPARISON_TOLERANCE
= SPEC_PENDING

Therefore:

TPEX_OFFICIAL_VERIFICATION
= BLOCKED

No VERIFIED promotion
is authorized.

---

# 40. Current Numeric Readiness

RAW_NUMERIC_TYPE
= EVIDENCE_PENDING

NUMERIC_CONVERSION
= NOT_AUTHORIZED

NUMERIC_COMPARISON_TOLERANCE
= SPEC_PENDING

NUMERIC_COMPARISON_VERIFICATION
= BLOCKED

NUMERIC_VERIFICATION_READY
= False

---

# 41. Current Freshness Readiness

STALE_POLICY
= FAIL_CLOSED

FRESHNESS_THRESHOLD
= SPEC_PENDING

FRESHNESS_VERIFICATION_READY
= False

No stale threshold
is invented by this policy.

---

# 42. Current Cross-Source Readiness

CROSS_SOURCE_COMPARISON_POLICY
= SPEC_PENDING

CROSS_SOURCE_VERIFICATION_READY
= False

No provider equality rule
is authorized.

---

# 43. Verification Aggregation Candidate

Future aggregation may produce VERIFIED
only when every required verification
dimension is verified.

ANY_REQUIRED_BLOCKER
→ BLOCKED

ALL_REQUIRED_VERIFIED
→ VERIFIED

VERIFICATION_AGGREGATION
= CANDIDATE

VERIFICATION_AGGREGATION_EXECUTION
= NOT_AUTHORIZED

---

# 44. No Executable Verifier

This document does not create:

verify_official_eod()

or equivalent executable code.

VERIFIER_IMPLEMENTATION
= NOT_AUTHORIZED

VERIFICATION_EXECUTION
= NOT_AUTHORIZED

---

# 45. Parent Validation Status

Parent:

V14_WP4_OFFICIAL_EOD_MAPPING_VALIDATION_V1

remains:

VALIDATION_STATUS
= CANDIDATE

TWSE_VALIDATION_READINESS
= BLOCKED

TPEX_VALIDATION_READINESS
= BLOCKED

This Verification Policy
does not upgrade validation authority.

---

# 46. Parent Field Mapping Status

Parent:

V14_WP4_OFFICIAL_EOD_FIELD_MAPPING_V1

remains:

FIELD_MAPPING_STATUS
= CANDIDATE

TWSE_MACHINE_KEYS
= STRONG_CANDIDATE

TPEX_MACHINE_KEYS
= EVIDENCE_PENDING

This Verification Policy
does not upgrade machine-key evidence.

---

# 47. Parent Schema Status

Parent:

V14_NORMALIZED_DAILY_PRICE_INDEX_V1

remains:

SCHEMA_STATUS
= CANDIDATE

ALLOW_NORMALIZED_OUTPUT
= False

This policy does not authorize
normalized output.

---

# 48. Official-EOD Architecture Status

Parent architecture remains:

WP4_OFFICIAL_EOD_BENCHMARK_EXCEPTION
= STRONG_ARCHITECTURE_CANDIDATE

EXCEPTION_SCOPE
= WP4_DAILY_BENCHMARK_ONLY

GLOBAL_PRIMARY_PROVIDER
= FINMIND

This Verification Policy
does not activate the exception.

---

# 49. Non-Authorization Boundary

READ_ONLY
= True

VERIFICATION_POLICY_STATUS
= CANDIDATE

VERIFICATION_EXECUTION
= NOT_AUTHORIZED

VERIFIER_IMPLEMENTATION
= NOT_AUTHORIZED

VERIFICATION_AGGREGATION_EXECUTION
= NOT_AUTHORIZED

RAW_FIELD_MAPPING_EXECUTION
= NOT_AUTHORIZED

DATE_CONVERSION
= NOT_AUTHORIZED

NUMERIC_CONVERSION
= NOT_AUTHORIZED

ALLOW_NORMALIZED_OUTPUT
= False

NORMALIZATION_EXECUTION
= NOT_AUTHORIZED

OFFICIAL_EOD_ADAPTER
= NOT_AUTHORIZED

ALLOW_CORE_INPUT
= False

ALLOW_BENCHMARK_INPUT
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

# 50. Current Policy Matrix

Provenance Missing:

verification_status
= BLOCKED

reason
= PROVENANCE_MISSING


Wrong Trading Date:

verification_status
= BLOCKED

reason
= TRADING_DATE_MISMATCH


Index Identity Mismatch:

verification_status
= BLOCKED

reason
= INDEX_IDENTITY_MISMATCH


Price Index Type Mismatch:

verification_status
= BLOCKED

reason
= INDEX_TYPE_MISMATCH


Close Semantic Mismatch:

verification_status
= BLOCKED

reason
= CLOSE_SEMANTIC_MISMATCH


Timezone Evidence Pending:

verification_status
= BLOCKED

reason
= TIMEZONE_EVIDENCE_PENDING


Invalid Missing-Data State:

verification_status
= BLOCKED

reason
= MISSING_DATA_INVALID


Schema Version Mismatch:

verification_status
= BLOCKED

reason
= SCHEMA_VERSION_MISMATCH


Schema Drift:

verification_status
= BLOCKED

reason
= SCHEMA_DRIFT


Source Channel Mismatch:

verification_status
= BLOCKED

reason
= SOURCE_CHANNEL_MISMATCH


Unknown License:

verification_status
= BLOCKED

reason
= LICENSE_STATUS_UNKNOWN


Stale Data:

verification_status
= BLOCKED

reason
= STALE_DATA


Official Source Unavailable:

verification_status
= BLOCKED

reason
= OFFICIAL_SOURCE_UNAVAILABLE


Numeric Tolerance Pending:

verification_status
= BLOCKED

reason
= NUMERIC_TOLERANCE_SPEC_PENDING


Cross-Source Policy Pending:

verification_status
= BLOCKED

reason
= CROSS_SOURCE_POLICY_SPEC_PENDING

---

# 51. Current Provider Status

TWSE_OFFICIAL_VERIFICATION
= BLOCKED

TPEX_OFFICIAL_VERIFICATION
= BLOCKED

No provider currently receives
Official-EOD VERIFIED status.

---

# 52. Current Specification Gaps

Current unresolved evidence / specification:

TWSE machine-key final lock

TWSE raw date value format

TPEx exact endpoint

TPEx machine keys

TPEx raw date value format

raw numeric type

timezone evidence

freshness threshold

numeric comparison tolerance

cross-source comparison policy

These gaps remain explicit.

PENDING
!=
VERIFIED

---

# 53. Relationship to Source Contract

Official Verification Policy
defines how official evidence
would be evaluated.

It does not yet define
the complete executable
Official-EOD Source Contract.

Therefore:

SOURCE_CONTRACT
= NOT_YET_LOCKED

SOURCE_CONTRACT_EXECUTION
= NOT_AUTHORIZED

Next work may review
the Source Contract boundary.

---

# 54. Next Work

After this Verification Policy
is reviewed and safely sealed:

1. Source Contract Review
2. Evidence-gap resolution planning
3. Provider-specific evidence review
4. Re-evaluate implementation authority

Do not proceed directly to:

- executable verifier
- raw mapping implementation
- Official EOD Adapter
- normalization runtime
- Benchmark Engine

---

# 55. Current Continuation Point

Parent Validation Safety Baseline:

c7fcc0d64cc4753f9f273167952841e5cf5242d8

Parent Safety Tag:

v14-wp4-official-eod-mapping-validation-v1-safe

Production Code Change:

0

Runner Change:

0

Market Data Real GET:

0

---

# 56. Conclusion

WP4 Official-EOD Verification Policy
now has a candidate specification
based on multi-dimensional evidence
and fail-closed aggregation.

Official verification requires:

- provenance evidence
- trading-date match
- index identity match
- Price Index type match
- close-value semantics
- timezone evidence
- valid missing-data state
- schema-version compatibility
- source-channel identity
- license metadata
- freshness acceptance

Current providers remain:

TWSE_OFFICIAL_VERIFICATION
= BLOCKED

TPEX_OFFICIAL_VERIFICATION
= BLOCKED

Numeric comparison remains:

NUMERIC_COMPARISON_TOLERANCE
= SPEC_PENDING

Cross-source comparison remains:

CROSS_SOURCE_COMPARISON_POLICY
= SPEC_PENDING

Freshness threshold remains:

FRESHNESS_THRESHOLD
= SPEC_PENDING

Therefore:

VERIFICATION_POLICY_STATUS
= CANDIDATE

VERIFICATION_EXECUTION
= NOT_AUTHORIZED

VERIFIER_IMPLEMENTATION
= NOT_AUTHORIZED

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
