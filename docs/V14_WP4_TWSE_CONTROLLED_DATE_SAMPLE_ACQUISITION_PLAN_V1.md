# DAVID V14 UNIFIED ENGINE — WP4 TWSE CONTROLLED DATE SAMPLE ACQUISITION PLAN V1

> Work Package: WP4 — Market Context
>
> Document Type: Controlled Evidence Acquisition Plan
>
> Provider: TWSE
>
> Evidence Purpose: Raw Date Value Format Only
>
> Parent Evidence:
> V14_WP4_TWSE_OFFICIAL_SCHEMA_EVIDENCE_V1.md
>
> Parent Protected Baseline:
> 2a33f8ce60120da0c3dfbdfed4f673e1818fec3b
>
> Parent Safety Tag:
> v14-wp4-twse-official-schema-evidence-v1-safe
>
> Plan Status: CANDIDATE
>
> Execution Authorization: NOT AUTHORIZED
>
> Current Market Data Real GET: 0
>
> Production Write: NOT AUTHORIZED

---

# 1. Purpose

This document defines
a candidate controlled acquisition plan
for one TWSE official sample.

The sole evidence purpose is:

TWSE_RAW_DATE_VALUE_FORMAT

No broader market-data acquisition
is authorized by this document.

---

# 2. Parent Evidence State

Parent official schema evidence established:

TWSE_MACHINE_KEY_EVIDENCE
= OFFICIAL_SCHEMA_ACQUIRED

TWSE_MACHINE_KEYS
= VERIFIED_CANDIDATE

TWSE_RAW_DATE_SCHEMA_TYPE
= STRING

TWSE_RAW_NUMERIC_TYPE
= STRING

Remaining technical gap:

TWSE_RAW_DATE_VALUE_FORMAT
= EVIDENCE_PENDING

---

# 3. Static Evidence Exhaustion

Official Swagger provides:

Date property
= VERIFIED_CANDIDATE

Date schema type
= STRING

Official Swagger does not provide:

format

pattern

example

Official static web-page review
does not provide a record.Date
machine-value example.

Therefore:

STATIC_DATE_VALUE_EVIDENCE
= INSUFFICIENT

---

# 4. Acquisition Purpose

ACQUISITION_PURPOSE
= RAW_DATE_VALUE_FORMAT_EVIDENCE_ONLY

The future sample,
if separately authorized,
may be used only to observe
the raw Date machine value.

It must not be used
to activate normalization,
benchmark input,
or production execution.

---

# 5. Provider Boundary

PROVIDER
= TWSE

SINGLE_PROVIDER_ONLY
= True

ALLOW_PROVIDER_SWITCH
= False

No FinMind, Yahoo,
or TPEx acquisition
is authorized by this plan.

---

# 6. Endpoint Boundary

The candidate acquisition
must use exactly one
pre-approved TWSE official endpoint.

ONE_ENDPOINT_ONLY
= True

ENDPOINT_IDENTITY
= APPROVAL_REQUIRED

This plan does not yet authorize
a concrete endpoint execution.

ENDPOINT_EXECUTION
= NOT_AUTHORIZED

---

# 7. Request Method Boundary

GET_ONLY
= True

POST_ALLOWED
= False

PUT_ALLOWED
= False

PATCH_ALLOWED
= False

DELETE_ALLOWED
= False

No mutation-capable HTTP method
is authorized.

---

# 8. Request Count Boundary

MAX_REAL_GETS
= 1

ONE_SHOT_ONLY
= True

MULTI_REQUEST_ACQUISITION
= NOT_AUTHORIZED

Current state remains:

REAL_GET
= 0

---

# 9. Retry Boundary

MAX_RETRIES
= 0

AUTOMATIC_RETRY
= False

If the future request fails:

→ STOP

No retry loop
may be introduced.

---

# 10. Redirect Boundary

ALLOW_REDIRECTS
= False

Redirect-following behavior
must remain disabled
for any future controlled request.

---

# 11. Observation Boundary

ALLOWED_OBSERVATION_FIELD
= Date

The acquisition purpose
is limited to observing
the raw Date value.

OpeningIndex

HighestIndex

LowestIndex

ClosingIndex

may exist in the response,
but this plan does not authorize
new semantic conclusions
from those values.

---

# 12. No Conversion

The future sample,
if authorized,
must remain raw evidence.

DATE_CONVERSION
= NOT_AUTHORIZED

NUMERIC_CONVERSION
= NOT_AUTHORIZED

No ROC-to-Gregorian conversion
is authorized.

No string-to-number conversion
is authorized.

---

# 13. No Normalization

NORMALIZATION_EXECUTION
= NOT_AUTHORIZED

ALLOW_NORMALIZED_OUTPUT
= False

The sample must not be transformed
into the normalized
Daily Price Index schema.

---

# 14. No Runtime Integration

OFFICIAL_EOD_ADAPTER
= NOT_AUTHORIZED

ADAPTER_IMPLEMENTATION
= NOT_AUTHORIZED

ALLOW_BENCHMARK_INPUT
= False

ALLOW_CORE_INPUT
= False

ALLOW_SCORE
= False

ALLOW_DECISION
= False

No runtime path
is opened by this plan.

---

# 15. No Persistence

ALLOW_SUPABASE_WRITE
= False

ALLOW_PRODUCTION_WRITE
= False

DATABASE_WRITE
= NOT_AUTHORIZED

PRODUCTION_WRITE
= NOT_AUTHORIZED

The future evidence sample
must not be persisted
to production storage
by this plan.

---

# 16. Endpoint Selection Rule

A future controlled acquisition
requires a separately reviewed
endpoint identity.

Candidate endpoint selection
must satisfy:

provider
= TWSE

official ownership
= REQUIRED

read-only access
= REQUIRED

GET method
= REQUIRED

Date evidence capability
= REQUIRED

ENDPOINT_SELECTION_STATUS
= REVIEW_REQUIRED

No endpoint is executable
under this plan alone.

---

# 17. Endpoint Identity Separation

Existing evidence identifies
different TWSE route contexts.

Official OpenAPI route evidence
and official web-report route evidence
must not be silently treated
as identical execution targets.

Therefore:

ENDPOINT_IDENTITY_SEPARATION
= REQUIRED

ENDPOINT_ALIAS_ASSUMPTION
= NOT_AUTHORIZED

A future execution target
must be explicitly selected
and separately authorized.

---

# 18. Request Parameter Boundary

Only parameters required
for the approved one-shot
Date evidence request
may be permitted.

REQUEST_PARAMETER_SET
= APPROVAL_REQUIRED

EXTRA_PARAMETERS
= NOT_AUTHORIZED

BULK_RANGE_REQUEST
= NOT_AUTHORIZED

MULTI_DATE_REQUEST
= NOT_AUTHORIZED

A future request must remain
minimal and evidence-specific.

---

# 19. Trading-Date Scope

The future sample acquisition
must target at most
one approved trading-date context.

SINGLE_TRADING_DATE_ONLY
= True

TRADING_DATE_TARGET
= APPROVAL_REQUIRED

No date range
is authorized.

---

# 20. Response Acceptance Boundary

A future response
may be accepted as evidence only if:

HTTP status
= successful

content type
= expected

provider identity
= TWSE

endpoint identity
= approved

response structure
= expected

Date field
= present

Otherwise:

→ STOP

RESPONSE_ACCEPTANCE
= FAIL_CLOSED

---

# 21. Date Observation Rule

The sole observation target is:

Date

The future evidence review
may record:

raw field name

raw field value

raw value type

source identity

request provenance

It must not perform
date conversion.

DATE_OBSERVATION_ONLY
= True

---

# 22. Missing Date Policy

If Date is absent:

→ STOP

If Date is null:

→ STOP

If Date is empty:

→ STOP

If Date appears multiple times
with ambiguous semantics:

→ STOP

MISSING_DATE_POLICY
= FAIL_CLOSED

No inferred date
may be substituted.

---

# 23. Unexpected Response Policy

If the response:

changes schema

returns an error object

returns HTML unexpectedly

redirects

requires authentication
not previously approved

or exposes ambiguous Date semantics:

→ STOP

UNEXPECTED_RESPONSE_POLICY
= FAIL_CLOSED

No fallback provider
is authorized.

---

# 24. Provenance Requirement

A future controlled sample
must preserve minimal provenance.

Required provenance candidate:

provider

endpoint_identity

request_method

request_parameter_identity

status_code

content_type

observed_field

raw_value_type

payload_hash

PROVENANCE_REQUIRED
= True

Secrets must not be stored.

SECRET_IN_PROVENANCE
= PROHIBITED

---

# 25. Payload Hash

If a future sample
is separately authorized,
its raw evidence should be
cryptographically fingerprinted.

Candidate:

PAYLOAD_HASH
= SHA256

Hashing does not authorize
persistence or production use.

---

# 26. Evidence Output Boundary

The only candidate evidence output is:

TWSE_RAW_DATE_VALUE_EVIDENCE

Possible future evidence conclusion:

TWSE_RAW_DATE_VALUE_FORMAT
= EVIDENCE_SUPPORTED

or:

TWSE_RAW_DATE_VALUE_FORMAT
= EVIDENCE_INSUFFICIENT

This plan does not pre-decide
the observed format.

---

# 27. No Automatic Promotion

Even if one future sample
contains a clear Date value:

SAMPLE_OBSERVED
!=
SOURCE_CONTRACT_ACTIVATED

SAMPLE_OBSERVED
!=
OFFICIAL_VERIFICATION_COMPLETE

SAMPLE_OBSERVED
!=
DATE_CONVERSION_AUTHORIZED

Any evidence promotion
requires a separate review.

---

# 28. Separate Authorization Requirement

This Plan is not
an execution authorization.

Before any future
market-data request:

EXECUTION_AUTHORIZATION
must be separately reviewed.

Current:

EXECUTION_AUTHORIZATION
= NOT_AUTHORIZED

MARKET_DATA_ENDPOINT_EXECUTION
= NOT_AUTHORIZED

REAL_GET
= 0

No command in this document
performs the future GET.

---

# 29. Execution Preconditions

A future controlled request
may be considered only after:

1. endpoint identity is selected
2. endpoint ownership is confirmed
3. request parameters are fixed
4. trading-date scope is fixed
5. timeout is fixed
6. redirect policy is fixed
7. retry policy is fixed
8. allowed observation field is fixed
9. provenance fields are fixed
10. separate execution authorization passes

Until then:

EXECUTION_READINESS
= BLOCKED

---

# 30. Candidate Safety Matrix

PROVIDER
= TWSE

ACQUISITION_PURPOSE
= RAW_DATE_VALUE_FORMAT_EVIDENCE_ONLY

SINGLE_PROVIDER_ONLY
= True

ONE_ENDPOINT_ONLY
= True

GET_ONLY
= True

MAX_REAL_GETS
= 1

ONE_SHOT_ONLY
= True

SINGLE_TRADING_DATE_ONLY
= True

MAX_RETRIES
= 0

ALLOW_REDIRECTS
= False

ALLOWED_OBSERVATION_FIELD
= Date

PROVENANCE_REQUIRED
= True

PAYLOAD_HASH
= SHA256

DATE_CONVERSION
= NOT_AUTHORIZED

NUMERIC_CONVERSION
= NOT_AUTHORIZED

NORMALIZATION_EXECUTION
= NOT_AUTHORIZED

OFFICIAL_EOD_ADAPTER
= NOT_AUTHORIZED

ALLOW_BENCHMARK_INPUT
= False

ALLOW_CORE_INPUT
= False

ALLOW_SUPABASE_WRITE
= False

ALLOW_PRODUCTION_WRITE
= False

EXECUTION_AUTHORIZATION
= NOT_AUTHORIZED

MARKET_DATA_ENDPOINT_EXECUTION
= NOT_AUTHORIZED

REAL_GET
= 0

PRODUCTION_WRITE
= NOT_AUTHORIZED

---

# 31. Current Evidence State

Current protected evidence remains:

TWSE_MACHINE_KEY_EVIDENCE
= OFFICIAL_SCHEMA_ACQUIRED

TWSE_MACHINE_KEYS
= VERIFIED_CANDIDATE

TWSE_RAW_DATE_SCHEMA_TYPE
= STRING

TWSE_RAW_NUMERIC_TYPE
= STRING

TWSE_RAW_DATE_VALUE_FORMAT
= EVIDENCE_PENDING

This Plan does not alter
those evidence states.

---

# 32. Parent Protection

Parent Protected Baseline:

2a33f8ce60120da0c3dfbdfed4f673e1818fec3b

Parent Safety Tag:

v14-wp4-twse-official-schema-evidence-v1-safe

Parent evidence document
is not modified.

PARENT_DOCUMENT_MODIFICATION
= 0

---

# 33. Next Work

After this Plan
is reviewed and safely sealed:

1. Endpoint Selection Review
2. Request Parameter Review
3. Trading-Date Selection Review
4. Execution Authorization Review

Only after a separate
authorization safety node
may one controlled request
be considered.

Do not proceed directly to:

- Invoke-RestMethod market endpoint
- Invoke-WebRequest market endpoint
- adapter implementation
- date conversion
- numeric conversion
- normalization
- Benchmark Engine

---

# 34. Conclusion

A candidate controlled
TWSE Date sample acquisition plan
is now defined.

Its sole purpose is:

TWSE_RAW_DATE_VALUE_FORMAT evidence.

The plan is bounded by:

one provider

one endpoint

GET only

one trading-date context

maximum one Real GET

zero retries

no redirects

Date-only observation

required provenance

SHA256 payload fingerprint

fail-closed response handling

No execution is authorized.

Current state remains:

PLAN_STATUS
= CANDIDATE

EXECUTION_READINESS
= BLOCKED

EXECUTION_AUTHORIZATION
= NOT_AUTHORIZED

MARKET_DATA_ENDPOINT_EXECUTION
= NOT_AUTHORIZED

TWSE_RAW_DATE_VALUE_FORMAT
= EVIDENCE_PENDING

DATE_CONVERSION
= NOT_AUTHORIZED

NUMERIC_CONVERSION
= NOT_AUTHORIZED

NORMALIZATION_EXECUTION
= NOT_AUTHORIZED

OFFICIAL_EOD_ADAPTER
= NOT_AUTHORIZED

ALLOW_BENCHMARK_INPUT
= False

ALLOW_CORE_INPUT
= False

ALLOW_SUPABASE_WRITE
= False

ALLOW_PRODUCTION_WRITE
= False

REAL_GET
= 0

PRODUCTION_WRITE
= NOT_AUTHORIZED
