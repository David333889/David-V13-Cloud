# DAVID V14 UNIFIED ENGINE — WP4 TWSE DATE SAMPLE ENDPOINT SELECTION REVIEW V1

> Work Package: WP4 — Market Context
>
> Document Type: Controlled Endpoint Selection Review
>
> Provider: TWSE
>
> Parent Plan:
> V14_WP4_TWSE_CONTROLLED_DATE_SAMPLE_ACQUISITION_PLAN_V1.md
>
> Parent Protected Baseline:
> 3bfff06a189ce662388adddf61fd7c582cb5d2c0
>
> Parent Safety Tag:
> v14-wp4-twse-controlled-date-sample-acquisition-plan-v1-safe
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
the candidate endpoint identity
for a future controlled
TWSE raw Date evidence sample.

This document does not execute
the market-data endpoint.

ENDPOINT_SELECTION_REVIEW
= DOCS_ONLY

---

# 2. Parent Acquisition Purpose

Parent acquisition purpose:

ACQUISITION_PURPOSE
= RAW_DATE_VALUE_FORMAT_EVIDENCE_ONLY

Provider:

PROVIDER
= TWSE

Allowed observation:

ALLOWED_OBSERVATION_FIELD
= Date

Maximum future Real GET:

MAX_REAL_GETS
= 1

Current:

REAL_GET
= 0

---

# 3. Endpoint Selection Requirements

Parent Plan requires:

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

ONE_ENDPOINT_ONLY
= True

---

# 4. Reviewed Route Contexts

Two different official
TWSE route contexts
have been observed.

Official OpenAPI route:

/indicesReport/MI_5MINS_HIST

Official Web Report route:

/TAIEX/MI_5MINS_HIST

These routes must not
be silently treated
as execution aliases.

ENDPOINT_IDENTITY_SEPARATION
= REQUIRED

ENDPOINT_ALIAS_ASSUMPTION
= NOT_AUTHORIZED

---

# 5. Web Report Route Evidence

Official TWSE static page
declares a web-report route:

/TAIEX/MI_5MINS_HIST

The web page also contains
its own date-query UI context.

However:

the web-report route
does not provide the reviewed
Official OpenAPI schema lineage
for the Date machine property.

Therefore:

WEB_REPORT_ROUTE
= OFFICIAL_ROUTE_EVIDENCE

WEB_REPORT_ROUTE_SELECTION
= NOT_SELECTED

---

# 6. OpenAPI Route Evidence

Official TWSE Swagger declares:

Path:

/indicesReport/MI_5MINS_HIST

Method:

GET

Summary:

發行量加權股價指數歷史資料

Produces:

application/json

text/csv

Therefore:

OPENAPI_ROUTE_EVIDENCE
= OFFICIAL_SCHEMA_SUPPORTED

---

# 7. Candidate Endpoint Selection

The OpenAPI route
has direct official schema lineage
to the Date machine property.

Therefore candidate selection:

ENDPOINT_SELECTION_STATUS
= CANDIDATE_SELECTED

ENDPOINT_IDENTITY
= TWSE_OFFICIAL_OPENAPI_MI_5MINS_HIST

ENDPOINT_PATH
= /indicesReport/MI_5MINS_HIST

REQUEST_METHOD
= GET

ENDPOINT_OWNERSHIP
= OFFICIAL_TWSE

ENDPOINT_EXECUTION
= NOT_AUTHORIZED

---

# 8. Date Evidence Capability

Official OpenAPI schema declares:

Date

OpeningIndex

HighestIndex

LowestIndex

ClosingIndex

Date is declared as:

type
= string

Therefore:

DATE_EVIDENCE_CAPABILITY
= OFFICIAL_SCHEMA_SUPPORTED

TWSE_RAW_DATE_SCHEMA_TYPE
= STRING

However:

TWSE_RAW_DATE_VALUE_FORMAT
= EVIDENCE_PENDING

---

# 9. Request Parameter Contract

Official Swagger endpoint declares:

parameters
= null

Therefore:

OPENAPI_REQUEST_PARAMETERS
= NONE_DECLARED

Candidate request parameter set:

REQUEST_PARAMETER_SET
= EMPTY_CANDIDATE

No query parameter
may be invented.

EXTRA_PARAMETERS
= NOT_AUTHORIZED

---

# 10. Date Query Parameter Boundary

Official Swagger does not declare
a Date request parameter.

Therefore:

DATE_QUERY_PARAMETER
= NOT_DECLARED

The web-report page's
date-query UI must not be copied
into the OpenAPI request contract.

WEB_REPORT_PARAMETER_INHERITANCE
= NOT_AUTHORIZED

---

# 11. Trading-Date Request Boundary

Because the selected
OpenAPI candidate declares
no request parameters:

TRADING_DATE_REQUEST_TARGET
= NOT_APPLICABLE_TO_REQUEST

A trading date must not
be invented as a query parameter.

This does not remove
the parent safety requirement
for controlled evidence scope.

---

# 12. Official Response Schema

HTTP 200 official schema:

type
= object

items
= not declared

properties:

Date

OpeningIndex

HighestIndex

LowestIndex

ClosingIndex

Therefore:

OPENAPI_RESPONSE_SCHEMA_TYPE
= OBJECT

OPENAPI_RESPONSE_ITEMS
= NOT_DECLARED

OPENAPI_RESPONSE_PROPERTY_COUNT
= 5

---

# 13. Response Cardinality Boundary

Official Swagger does not explicitly
declare:

single_record

single_trading_date

record_count

pagination

array cardinality

Therefore:

RESPONSE_CARDINALITY_SEMANTICS
= NOT_EXPLICITLY_DECLARED

SCHEMA_TYPE_OBJECT
!=
PROVEN_SINGLE_TRADING_DATE_RESPONSE

No cardinality assumption
is authorized.

---

# 14. Single-Trading-Date Enforcement

Parent Plan requires:

SINGLE_TRADING_DATE_ONLY
= True

However the selected endpoint
does not declare a Date parameter,
and official Swagger does not
explicitly prove single-trading-date
response semantics.

Therefore:

SINGLE_TRADING_DATE_POLICY
= REQUIRED_BY_PLAN

SINGLE_TRADING_DATE_ENFORCEMENT
= BLOCKED

This blocker must be resolved
before execution authorization.

---

# 15. Current Endpoint Decision

Current endpoint review conclusion:

ENDPOINT_SELECTION_STATUS
= CANDIDATE_SELECTED

ENDPOINT_IDENTITY
= TWSE_OFFICIAL_OPENAPI_MI_5MINS_HIST

ENDPOINT_PATH
= /indicesReport/MI_5MINS_HIST

REQUEST_METHOD
= GET

OPENAPI_REQUEST_PARAMETERS
= NONE_DECLARED

REQUEST_PARAMETER_SET
= EMPTY_CANDIDATE

DATE_QUERY_PARAMETER
= NOT_DECLARED

OPENAPI_RESPONSE_SCHEMA_TYPE
= OBJECT

RESPONSE_CARDINALITY_SEMANTICS
= NOT_EXPLICITLY_DECLARED

SINGLE_TRADING_DATE_ENFORCEMENT
= BLOCKED

ENDPOINT_EXECUTION
= NOT_AUTHORIZED

EXECUTION_AUTHORIZATION
= NOT_AUTHORIZED

REAL_GET
= 0

---

# 16. Response Acceptance Requirement

A future controlled response
may be considered evidence only if:

HTTP status
= successful

content type
= expected

provider identity
= TWSE

endpoint identity
= approved

response schema
= expected

Date field
= present

Otherwise:

→ STOP

RESPONSE_ACCEPTANCE
= FAIL_CLOSED

---

# 17. Content-Type Boundary

Official Swagger declares:

application/json

text/csv

For raw Date machine-property
evidence review:

CONTENT_TYPE_SELECTION
= REVIEW_REQUIRED

No content type
is selected for execution
by this document.

CONTENT_TYPE_EXECUTION
= NOT_AUTHORIZED

---

# 18. JSON Evidence Preference

The reviewed official
machine-property schema
is represented through
the OpenAPI JSON schema.

Therefore:

JSON_EVIDENCE_LINEAGE
= DIRECT_SCHEMA_SUPPORTED

CSV_DATE_VALUE_SEMANTICS
= NOT_REVIEWED

This review does not
authorize a JSON request.

---

# 19. Timeout Boundary

Parent Plan requires
timeout to be fixed
before execution authorization.

Current:

TIMEOUT_POLICY
= SPEC_PENDING

TIMEOUT_SECONDS
= NOT_SELECTED

Therefore:

TIMEOUT_READINESS
= BLOCKED

No default timeout
may be silently assumed.

---

# 20. Redirect Boundary

Parent Plan already establishes:

ALLOW_REDIRECTS
= False

Therefore:

REDIRECT_POLICY
= LOCKED_BY_PARENT_PLAN

Any redirect:

→ STOP

No redirect-following behavior
may be introduced.

---

# 21. Retry Boundary

Parent Plan already establishes:

MAX_RETRIES
= 0

AUTOMATIC_RETRY
= False

Therefore:

RETRY_POLICY
= LOCKED_BY_PARENT_PLAN

Any failed request:

→ STOP

No retry loop
is authorized.

---

# 22. Request Parameter Fail-Closed Rule

Official Swagger declares:

parameters
= null

Therefore:

REQUEST_PARAMETER_SET
= EMPTY_CANDIDATE

EXTRA_PARAMETERS
= NOT_AUTHORIZED

DATE_QUERY_PARAMETER
= NOT_DECLARED

Any invented parameter:

→ BLOCKED

REQUEST_PARAMETER_POLICY
= FAIL_CLOSED

---

# 23. Response Cardinality Blocker

Official Swagger declares:

response schema
= object

items
= not declared

Official Swagger does not
explicitly establish
single-trading-date semantics.

Therefore:

RESPONSE_CARDINALITY_SEMANTICS
= NOT_EXPLICITLY_DECLARED

SINGLE_TRADING_DATE_ENFORCEMENT
= BLOCKED

This blocker must not
be bypassed by assuming
object means one trading date.

---

# 24. Date Observation Boundary

If a future request
is separately authorized,
the sole semantic observation
remains:

Date

DATE_OBSERVATION_ONLY
= True

OpeningIndex

HighestIndex

LowestIndex

ClosingIndex

must not be used
to authorize new conversion,
normalization,
or benchmark behavior.

---

# 25. Evidence Promotion Boundary

Even if a future response
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

Evidence promotion requires
a separate review.

---

# 26. Parent Plan Protection

Parent Plan:

V14_WP4_TWSE_CONTROLLED_DATE_SAMPLE_ACQUISITION_PLAN_V1

Parent Protected Baseline:

3bfff06a189ce662388adddf61fd7c582cb5d2c0

Parent Safety Tag:

v14-wp4-twse-controlled-date-sample-acquisition-plan-v1-safe

The parent Plan
is not modified
by this review.

PARENT_DOCUMENT_MODIFICATION
= 0

---

# 27. Existing Evidence Protection

Existing TWSE evidence remains:

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

This review does not
promote the pending Date format.

---

# 28. Execution Blockers

Current blockers before
Execution Authorization include:

SINGLE_TRADING_DATE_ENFORCEMENT
= BLOCKED

TIMEOUT_READINESS
= BLOCKED

CONTENT_TYPE_SELECTION
= REVIEW_REQUIRED

Execution authorization itself:

EXECUTION_AUTHORIZATION
= NOT_AUTHORIZED

Therefore:

EXECUTION_READINESS
= BLOCKED

---

# 29. Non-Authorization Matrix

REVIEW_STATUS
= CANDIDATE

ENDPOINT_SELECTION_STATUS
= CANDIDATE_SELECTED

ENDPOINT_EXECUTION
= NOT_AUTHORIZED

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

# 30. Endpoint Review Matrix

Provider:

PROVIDER
= TWSE

Selected Candidate:

ENDPOINT_IDENTITY
= TWSE_OFFICIAL_OPENAPI_MI_5MINS_HIST

ENDPOINT_PATH
= /indicesReport/MI_5MINS_HIST

REQUEST_METHOD
= GET

Endpoint Ownership:

ENDPOINT_OWNERSHIP
= OFFICIAL_TWSE

Request Parameters:

OPENAPI_REQUEST_PARAMETERS
= NONE_DECLARED

REQUEST_PARAMETER_SET
= EMPTY_CANDIDATE

DATE_QUERY_PARAMETER
= NOT_DECLARED

Response:

OPENAPI_RESPONSE_SCHEMA_TYPE
= OBJECT

OPENAPI_RESPONSE_ITEMS
= NOT_DECLARED

OPENAPI_RESPONSE_PROPERTY_COUNT
= 5

Response Cardinality:

RESPONSE_CARDINALITY_SEMANTICS
= NOT_EXPLICITLY_DECLARED

Single Trading Date:

SINGLE_TRADING_DATE_ENFORCEMENT
= BLOCKED

---

# 31. Next Work

After this Endpoint Selection Review
is reviewed and safely sealed:

1. Single-Trading-Date Enforcement Review
2. Content-Type Selection Review
3. Timeout Policy Review
4. Execution Authorization Review

Only after a separate
Protected Authorization Node
may one controlled Real GET
be reconsidered.

Do not proceed directly to:

- Invoke-RestMethod market endpoint
- Invoke-WebRequest market endpoint
- date conversion
- numeric conversion
- normalization
- Official EOD Adapter
- Benchmark Engine

---

# 32. Current Continuation Point

Parent Protected Safety Node:

3bfff06a189ce662388adddf61fd7c582cb5d2c0

Parent Safety Tag:

v14-wp4-twse-controlled-date-sample-acquisition-plan-v1-safe

Production Code Change:

0

Runner Change:

0

Market Data Real GET:

0

---

# 33. Conclusion

TWSE Official OpenAPI endpoint:

/indicesReport/MI_5MINS_HIST

is selected as the candidate
controlled Date-evidence endpoint
because it has direct
official schema lineage
to the Date machine property.

Official Swagger declares:

request parameters
= none

response schema
= object

response properties
= 5

However official Swagger
does not explicitly establish
single-trading-date response semantics.

Therefore:

ENDPOINT_SELECTION_STATUS
= CANDIDATE_SELECTED

REQUEST_PARAMETER_SET
= EMPTY_CANDIDATE

DATE_QUERY_PARAMETER
= NOT_DECLARED

RESPONSE_CARDINALITY_SEMANTICS
= NOT_EXPLICITLY_DECLARED

SINGLE_TRADING_DATE_ENFORCEMENT
= BLOCKED

TIMEOUT_READINESS
= BLOCKED

CONTENT_TYPE_SELECTION
= REVIEW_REQUIRED

EXECUTION_READINESS
= BLOCKED

EXECUTION_AUTHORIZATION
= NOT_AUTHORIZED

MARKET_DATA_ENDPOINT_EXECUTION
= NOT_AUTHORIZED

TWSE_RAW_DATE_VALUE_FORMAT
= EVIDENCE_PENDING

REAL_GET
= 0

PRODUCTION_WRITE
= NOT_AUTHORIZED
