# DAVID V14 UNIFIED ENGINE — WP4 TWSE CONTENT TYPE SELECTION REVIEW V1

> Work Package: WP4 — Market Context
>
> Document Type: Content-Type Selection Review
>
> Provider: TWSE
>
> Parent Enforcement Review:
> V14_WP4_TWSE_SINGLE_TRADING_DATE_ENFORCEMENT_REVIEW_V1.md
>
> Parent Protected Baseline:
> 7cbd95135c778fc22da17a5969e7407fe7f65c4c
>
> Parent Safety Tag:
> v14-wp4-twse-single-trading-date-enforcement-review-v1-safe
>
> Review Status: CANDIDATE
>
> Execution Authorization: NOT AUTHORIZED
>
> Market Data Real GET: 0
>
> Production Write: NOT AUTHORIZED

---

# 1. Purpose

This document reviews
the content-type boundary
for the future controlled
TWSE Date evidence path.

This review is:

DOCS_ONLY

No market-data request
is executed.

No parser implementation
is authorized.

---

# 2. Parent State

Parent Endpoint Review established:

ENDPOINT_SELECTION_STATUS
= CANDIDATE_SELECTED

ENDPOINT_IDENTITY
= TWSE_OFFICIAL_OPENAPI_MI_5MINS_HIST

Parent Enforcement Review established:

SINGLE_TRADING_DATE_ENFORCEMENT
= BLOCKED

Current content-type state:

CONTENT_TYPE_SELECTION
= REVIEW_REQUIRED

---

# 3. Official TWSE Content Types

Official TWSE Swagger
for the selected endpoint declares:

application/json

text/csv

Therefore:

TWSE_JSON_CONTENT_TYPE
= OFFICIAL_SUPPORTED

TWSE_CSV_CONTENT_TYPE
= OFFICIAL_SUPPORTED

Official support alone
does not determine
V14 safety selection.

---

# 4. Existing V14 Content-Type Gate

Existing V14
live-fetch safety classification
requires content_type
to be a string.

If content_type
is not a string:

→ CONTENT_TYPE_INVALID

Existing V14 safety classification
also requires:

application/json

to appear in
the Content-Type value.

Otherwise:

→ CONTENT_TYPE_INVALID

Therefore:

JSON_CONTENT_TYPE_GATE
= ESTABLISHED

NON_JSON_CONTENT_TYPE
= FAIL_CLOSED

---

# 5. JSON Charset Compatibility

Existing V14 safety tests
support Content-Type values
such as:

application/json; charset=utf-8

Therefore:

JSON_MEDIA_TYPE_MATCH
= CASE_INSENSITIVE_SUBSTRING

JSON_CHARSET_SUFFIX
= ACCEPTABLE_BY_EXISTING_PRECEDENT

This does not authorize
a network request.

---

# 6. Existing JSON Parsing Precedent

Existing controlled backend
uses:

response.json()

to obtain structured payload.

Therefore:

JSON_PARSE_PRECEDENT
= ESTABLISHED

The structured result
is preserved as payload
only when parsing succeeds.

---

# 7. JSON Parse Failure

If response.json()
raises an exception,
the existing backend returns
error evidence including:

status_code

content_type

payload_error

size_bytes

It does not manufacture
a valid payload.

Therefore:

JSON_PARSE_FAILURE_POLICY
= FAIL_CLOSED

JSON_PARSE_FAILURE_VALID_PAYLOAD
= False

---

# 8. Read-Only Transport Boundary

Existing ReadOnlyTransport
preserves:

status_code

content_type

payload

It does not independently
promote response semantics.

Existing transport safety includes:

GET_ONLY
= True

ALLOW_REDIRECTS
= False

MAX_RETRIES
= 0

Transport and semantic
classification remain separate.

---

# 9. JSON Safety Precedent

Existing V14 evidence supports:

JSON_CONTENT_TYPE_SAFETY_PRECEDENT
= ESTABLISHED

JSON_PARSE_FAIL_CLOSED_PRECEDENT
= ESTABLISHED

JSON_STRUCTURED_EVIDENCE
= STRONG_CANDIDATE

This is sufficient
for content-type selection review.

It is not sufficient
for TWSE RAW_EVIDENCE activation.

---

# 10. CSV Safety Review

Official TWSE Swagger
also supports:

text/csv

However current V14
RAW_EVIDENCE safety precedent
does not establish
text/csv classification
for this protected path.

Therefore:

CSV_CONTENT_TYPE_SAFETY_PRECEDENT
= NOT_ESTABLISHED

CSV_SELECTION
= NOT_SELECTED

CSV_EXECUTION
= NOT_AUTHORIZED

No CSV parser
is authorized.

---

# 11. Candidate Content-Type Selection

Based on:

official TWSE support

existing V14 JSON gate

existing fail-closed JSON parsing

structured machine-field lineage

the candidate content type is:

CONTENT_TYPE_SELECTION
= CANDIDATE_SELECTED

SELECTED_CONTENT_TYPE
= application/json

JSON_EXECUTION_SELECTION
= NOT_AUTHORIZED

Candidate selection
does not authorize execution.

---

# 12. Existing RAW_EVIDENCE Classifier

Existing classify_fetch_response()
requires:

payload
= dict

payload["data"]
= list

non-empty data list

Only after these conditions
may classification become:

RAW_EVIDENCE

Therefore:

EXISTING_RAW_EVIDENCE_CLASSIFIER
= FINMIND_SCHEMA_SPECIFIC

---

# 13. TWSE Schema Difference

Current official TWSE
OpenAPI evidence declares:

response schema
= object

properties:

Date

OpeningIndex

HighestIndex

LowestIndex

ClosingIndex

items
= not declared

Current TWSE evidence
does not establish:

payload["data"]
= list

Therefore:

TWSE_EXISTING_CLASSIFIER_COMPATIBILITY
= NOT_ESTABLISHED

---

# 14. No Automatic RAW_EVIDENCE Promotion

Selecting application/json
does not establish
TWSE compatibility with
the existing FinMind-specific
RAW_EVIDENCE classifier.

Therefore:

CONTENT_TYPE_SELECTED
!=
RAW_EVIDENCE_COMPATIBLE

TWSE_RAW_EVIDENCE_CLASSIFICATION
= NOT_AUTHORIZED

TWSE_CLASSIFIER_IMPLEMENTATION
= NOT_AUTHORIZED

---

# 15. Current Content-Type Decision

CONTENT_TYPE_SELECTION
= CANDIDATE_SELECTED

SELECTED_CONTENT_TYPE
= application/json

JSON_CONTENT_TYPE_SAFETY_PRECEDENT
= ESTABLISHED

JSON_PARSE_FAILURE_POLICY
= FAIL_CLOSED

CSV_SELECTION
= NOT_SELECTED

CSV_EXECUTION
= NOT_AUTHORIZED

EXISTING_RAW_EVIDENCE_CLASSIFIER
= FINMIND_SCHEMA_SPECIFIC

TWSE_EXISTING_CLASSIFIER_COMPATIBILITY
= NOT_ESTABLISHED

TWSE_RAW_EVIDENCE_CLASSIFICATION
= NOT_AUTHORIZED

SINGLE_TRADING_DATE_ENFORCEMENT
= BLOCKED

TIMEOUT_READINESS
= BLOCKED

EXECUTION_READINESS
= BLOCKED

EXECUTION_AUTHORIZATION
= NOT_AUTHORIZED

MARKET_DATA_ENDPOINT_EXECUTION
= NOT_AUTHORIZED

REAL_GET
= 0

---

# 16. Content-Type Selection Scope

The selected candidate:

application/json

solves only
the content-type choice.

It does not solve:

TWSE response cardinality

TWSE response structure

single-trading-date enforcement

RAW_EVIDENCE classifier compatibility

execution authorization

Therefore:

CONTENT_TYPE_SELECTION_SCOPE
= CONTENT_TYPE_ONLY

---

# 17. Selection Is Not Execution

Candidate selection:

CONTENT_TYPE_SELECTION
= CANDIDATE_SELECTED

does not imply:

CONTENT_TYPE_EXECUTION
= AUTHORIZED

Current:

CONTENT_TYPE_EXECUTION
= NOT_AUTHORIZED

JSON_EXECUTION_SELECTION
= NOT_AUTHORIZED

---

# 18. JSON Parse Safety Boundary

Existing V14 backend
uses fail-closed JSON parsing.

Successful parse:

→ structured payload candidate

Parse exception:

→ payload_error evidence

No valid payload
is manufactured.

Therefore:

JSON_PARSE_FAILURE_POLICY
= FAIL_CLOSED

PARSE_ERROR_TO_VALID_PAYLOAD
= PROHIBITED

---

# 19. Content-Type Classification Boundary

Existing V14 safety classifier
requires:

HTTP status
= 200

Content-Type
contains application/json

before later schema checks.

Therefore:

JSON_CONTENT_TYPE_GATE
= ESTABLISHED

But:

JSON_CONTENT_TYPE_PASS
!=
RAW_EVIDENCE_PASS

Schema checks remain separate.

---

# 20. FinMind-Specific Schema Gate

Existing RAW_EVIDENCE classifier
requires:

payload
= dict

payload["data"]
= list

len(payload["data"])
> 0

Therefore:

FINMIND_RAW_EVIDENCE_SCHEMA_GATE
= ESTABLISHED

This is provider-specific evidence.

---

# 21. TWSE Schema Compatibility Gap

Current TWSE Swagger
does not establish:

payload["data"]

data list

non-empty data list

Therefore:

TWSE_FINMIND_SCHEMA_EQUIVALENCE
= NOT_ESTABLISHED

TWSE_EXISTING_CLASSIFIER_COMPATIBILITY
= NOT_ESTABLISHED

---

# 22. No Classifier Reuse Assumption

Existing classifier
must not be reused for TWSE
merely because both providers
may return JSON.

Therefore:

JSON_MEDIA_TYPE_MATCH
!=
SCHEMA_COMPATIBILITY

CLASSIFIER_REUSE_ASSUMPTION
= NOT_AUTHORIZED

---

# 23. No TWSE Classifier Implementation

This review does not authorize:

TWSE-specific classifier

TWSE response parser

TWSE response observer

TWSE schema adapter

Therefore:

TWSE_CLASSIFIER_IMPLEMENTATION
= NOT_AUTHORIZED

TWSE_PARSER_IMPLEMENTATION
= NOT_AUTHORIZED

TWSE_OBSERVER_IMPLEMENTATION
= NOT_AUTHORIZED

---

# 24. RAW_EVIDENCE Boundary

Current TWSE state:

TWSE_RAW_EVIDENCE_CLASSIFICATION
= NOT_AUTHORIZED

No response may be promoted
to RAW_EVIDENCE
solely because:

HTTP status is 200

or

Content-Type is application/json

or

JSON parsing succeeds.

RAW_EVIDENCE_PROMOTION
= BLOCKED

---

# 25. CSV Boundary

Official TWSE supports:

text/csv

But current protected V14 path
has no reviewed CSV
RAW_EVIDENCE safety precedent
for this use.

Therefore:

CSV_SELECTION
= NOT_SELECTED

CSV_EXECUTION
= NOT_AUTHORIZED

CSV_PARSER_IMPLEMENTATION
= NOT_AUTHORIZED

CSV_FALLBACK
= NOT_AUTHORIZED

---

# 26. No Content-Type Fallback

If a future separately-authorized
request does not return
the selected expected media type:

→ STOP

No automatic fallback
from JSON to CSV
is authorized.

CONTENT_TYPE_FALLBACK
= NOT_AUTHORIZED

UNEXPECTED_CONTENT_TYPE_POLICY
= FAIL_CLOSED

---

# 27. Single-Date Relationship

Content-Type selection
does not resolve:

TWSE response structure

TWSE Date multiplicity

TWSE Date uniqueness

Therefore:

CONTENT_TYPE_SELECTION
!=
SINGLE_TRADING_DATE_ENFORCEMENT

Current:

SINGLE_TRADING_DATE_ENFORCEMENT
= BLOCKED

---

# 28. Timeout Relationship

Content-Type selection
does not resolve timeout policy.

Existing V14 precedent
contains bounded timeout behavior.

However TWSE WP4
timeout selection remains:

TIMEOUT_POLICY
= SPEC_PENDING

TIMEOUT_READINESS
= BLOCKED

No timeout value
is activated by this review.

---

# 29. Parent Protection

Parent Enforcement Review:

V14_WP4_TWSE_SINGLE_TRADING_DATE_ENFORCEMENT_REVIEW_V1

Parent Protected Baseline:

7cbd95135c778fc22da17a5969e7407fe7f65c4c

Parent Safety Tag:

v14-wp4-twse-single-trading-date-enforcement-review-v1-safe

Parent document
is not modified.

PARENT_DOCUMENT_MODIFICATION
= 0

---

# 30. Content-Type Decision Matrix

Official TWSE JSON:

TWSE_JSON_CONTENT_TYPE
= OFFICIAL_SUPPORTED

Official TWSE CSV:

TWSE_CSV_CONTENT_TYPE
= OFFICIAL_SUPPORTED

Selected candidate:

SELECTED_CONTENT_TYPE
= application/json

Selection status:

CONTENT_TYPE_SELECTION
= CANDIDATE_SELECTED

JSON safety precedent:

JSON_CONTENT_TYPE_SAFETY_PRECEDENT
= ESTABLISHED

JSON parse policy:

JSON_PARSE_FAILURE_POLICY
= FAIL_CLOSED

CSV selection:

CSV_SELECTION
= NOT_SELECTED

Classifier compatibility:

TWSE_EXISTING_CLASSIFIER_COMPATIBILITY
= NOT_ESTABLISHED

TWSE RAW_EVIDENCE:

TWSE_RAW_EVIDENCE_CLASSIFICATION
= NOT_AUTHORIZED

---

# 31. Non-Authorization Matrix

REVIEW_STATUS
= CANDIDATE

CONTENT_TYPE_SELECTION
= CANDIDATE_SELECTED

CONTENT_TYPE_EXECUTION
= NOT_AUTHORIZED

JSON_EXECUTION_SELECTION
= NOT_AUTHORIZED

TWSE_RAW_EVIDENCE_CLASSIFICATION
= NOT_AUTHORIZED

TWSE_CLASSIFIER_IMPLEMENTATION
= NOT_AUTHORIZED

SINGLE_TRADING_DATE_ENFORCEMENT
= BLOCKED

TIMEOUT_READINESS
= BLOCKED

EXECUTION_READINESS
= BLOCKED

EXECUTION_AUTHORIZATION
= NOT_AUTHORIZED

MARKET_DATA_ENDPOINT_EXECUTION
= NOT_AUTHORIZED

MAX_REAL_GETS
= 1

REAL_GET
= 0

DATE_CONVERSION
= NOT_AUTHORIZED

NUMERIC_CONVERSION
= NOT_AUTHORIZED

NORMALIZATION_EXECUTION
= NOT_AUTHORIZED

ALLOW_PROVIDER_SWITCH
= False

ALLOW_NORMALIZED_OUTPUT
= False

ALLOW_BENCHMARK_INPUT
= False

ALLOW_CORE_INPUT
= False

ALLOW_SUPABASE_WRITE
= False

ALLOW_PRODUCTION_WRITE
= False

OFFICIAL_EOD_ADAPTER
= NOT_AUTHORIZED

PRODUCTION_WRITE
= NOT_AUTHORIZED

---

# 32. Evidence-Gap Decision

Current evidence is sufficient
to select:

application/json

as the candidate
TWSE content type.

Current evidence is insufficient
to establish:

TWSE compatibility
with existing RAW_EVIDENCE classifier

TWSE response cardinality

TWSE single-Date enforcement

TWSE executable classifier

Therefore:

CONTENT_TYPE_EVIDENCE_GAP
= SELECTION_RESOLVED

CLASSIFIER_COMPATIBILITY_GAP
= REMAINS_OPEN

---

# 33. Next Work

After this review
is safely sealed:

1. Timeout Policy Review
2. Response-Scope Evidence Decision
3. Re-evaluate Single-Trading-Date Enforcement
4. Re-evaluate TWSE RAW_EVIDENCE boundary
5. Execution Authorization Review
   only if blockers are resolved

Do not proceed directly to:

- TWSE market-data GET
- TWSE classifier implementation
- TWSE parser implementation
- CSV fallback
- date conversion
- normalization
- Official EOD Adapter
- Benchmark Engine

---

# 34. Conclusion

Official TWSE Swagger supports:

application/json

and

text/csv

Existing V14 safety precedent
strongly supports JSON
as the protected candidate.

Existing JSON parsing
fails closed.

CSV has no reviewed
protected RAW_EVIDENCE precedent
for this path.

Therefore:

CONTENT_TYPE_SELECTION
= CANDIDATE_SELECTED

SELECTED_CONTENT_TYPE
= application/json

JSON_CONTENT_TYPE_SAFETY_PRECEDENT
= ESTABLISHED

JSON_PARSE_FAILURE_POLICY
= FAIL_CLOSED

CSV_SELECTION
= NOT_SELECTED

CSV_EXECUTION
= NOT_AUTHORIZED

However:

EXISTING_RAW_EVIDENCE_CLASSIFIER
= FINMIND_SCHEMA_SPECIFIC

TWSE_EXISTING_CLASSIFIER_COMPATIBILITY
= NOT_ESTABLISHED

TWSE_RAW_EVIDENCE_CLASSIFICATION
= NOT_AUTHORIZED

SINGLE_TRADING_DATE_ENFORCEMENT
= BLOCKED

TIMEOUT_READINESS
= BLOCKED

EXECUTION_READINESS
= BLOCKED

EXECUTION_AUTHORIZATION
= NOT_AUTHORIZED

MARKET_DATA_ENDPOINT_EXECUTION
= NOT_AUTHORIZED

REAL_GET
= 0

PRODUCTION_WRITE
= NOT_AUTHORIZED
