# DAVID V14 UNIFIED ENGINE — WP4 TWSE OFFICIAL SCHEMA EVIDENCE V1

> Work Package: WP4 — Market Context
>
> Document Type: Provider-Specific Official Schema Evidence
>
> Provider: TWSE
>
> Parent Source Contract:
> V14_WP4_OFFICIAL_EOD_SOURCE_CONTRACT_V1.md
>
> Parent Protected Baseline:
> 624b2040d43f75e5aa06c6668182804ca9f68a61
>
> Parent Safety Tag:
> v14-wp4-official-eod-source-contract-v1-safe
>
> Evidence Status: CANDIDATE
>
> Market Data Real GET: 0
>
> Production Write: NOT AUTHORIZED

---

# 1. Purpose

This document records
provider-specific official schema evidence
for the TWSE Official-EOD source candidate.

The evidence source is:

TWSE Official OpenAPI Swagger

This document records only
what the official Swagger schema
directly supports.

It does not infer
unsupported value formats.

---

# 2. Evidence Acquisition Boundary

Evidence acquisition used:

TWSE official Swagger document

https://openapi.twse.com.tw/v1/swagger.json

Evidence acquisition did not execute:

/indicesReport/MI_5MINS_HIST

Therefore:

DOCUMENTATION_EVIDENCE_ACQUISITION
= PERFORMED

MARKET_DATA_ENDPOINT_EXECUTION
= NOT_PERFORMED

REAL_GET
= 0

---

# 3. Official Endpoint Schema

Official Swagger path:

/indicesReport/MI_5MINS_HIST

Method:

GET

Summary:

發行量加權股價指數歷史資料

Produces:

application/json

text/csv

TWSE_SWAGGER_ENDPOINT_SCHEMA
= EVIDENCE_ACQUIRED

---

# 4. Response Schema Shape

Official Swagger response:

HTTP 200

schema.type
= object

The response schema is defined
inline in the endpoint declaration.

No external definition reference
is required for this schema.

INLINE_RESPONSE_SCHEMA
= VERIFIED_EVIDENCE

---

# 5. Official Machine Properties

Official Swagger properties:

Date

OpeningIndex

HighestIndex

LowestIndex

ClosingIndex

Therefore:

TWSE_MACHINE_KEY_EVIDENCE
= OFFICIAL_SCHEMA_ACQUIRED

Candidate evidence conclusion:

TWSE_MACHINE_KEYS
= VERIFIED_CANDIDATE

This document does not modify
the previously protected
Field Mapping document.

---

# 6. Date Property Evidence

Official Swagger declares:

Property
= Date

Type
= string

Description
= 日期

Therefore:

TWSE_RAW_DATE_SCHEMA_TYPE
= STRING

Schema type evidence
is directly supported.

---

# 7. Date Value Format Boundary

Official Swagger does not provide:

format

pattern

example

for the Date property.

Therefore:

TWSE_RAW_DATE_VALUE_FORMAT
= EVIDENCE_PENDING

The following are not inferred:

ROC date value format

Gregorian date value format

YYYYMMDD

YYYY-MM-DD

or any other machine-value format.

SCHEMA_TYPE
!=
VALUE_FORMAT

---

# 8. OpeningIndex Evidence

Official Swagger declares:

Property
= OpeningIndex

Type
= string

Description
= 開盤指數

Therefore:

TWSE_OPENING_INDEX_SCHEMA_TYPE
= STRING

---

# 9. HighestIndex Evidence

Official Swagger declares:

Property
= HighestIndex

Type
= string

Description
= 最高指數

Therefore:

TWSE_HIGHEST_INDEX_SCHEMA_TYPE
= STRING

---

# 10. LowestIndex Evidence

Official Swagger declares:

Property
= LowestIndex

Type
= string

Description
= 最低指數

Therefore:

TWSE_LOWEST_INDEX_SCHEMA_TYPE
= STRING

---

# 11. ClosingIndex Evidence

Official Swagger declares:

Property
= ClosingIndex

Type
= string

Description
= 收盤指數

Therefore:

TWSE_CLOSING_INDEX_SCHEMA_TYPE
= STRING

---

# 12. TWSE Raw Index Schema Type

The four official index properties:

OpeningIndex

HighestIndex

LowestIndex

ClosingIndex

are declared by
the official Swagger schema
as:

string

Therefore:

TWSE_RAW_NUMERIC_TYPE
= STRING

This is provider-specific
schema representation evidence.

---

# 13. Provider-Specific Boundary

TWSE evidence does not establish
TPEx schema representation.

Therefore:

TWSE_RAW_NUMERIC_TYPE
= STRING

does not imply:

TPEX_RAW_NUMERIC_TYPE
= STRING

PROVIDER_ASYMMETRY
= REQUIRED

---

# 14. Numeric Conversion Boundary

Raw schema type:

STRING

does not authorize
numeric conversion.

Therefore:

NUMERIC_CONVERSION
= NOT_AUTHORIZED

No parsing rule is created.

No decimal rule is created.

No thousands-separator rule
is created.

No rounding rule is created.

---

# 15. Evidence Maturity

Current TWSE technical evidence:

TWSE_DISPLAY_SCHEMA
= VERIFIED

TWSE_EXACT_ENDPOINT
= VERIFIED

TWSE_MACHINE_KEY_EVIDENCE
= OFFICIAL_SCHEMA_ACQUIRED

TWSE_MACHINE_KEYS
= VERIFIED_CANDIDATE

TWSE_RAW_DATE_SCHEMA_TYPE
= STRING

TWSE_RAW_DATE_VALUE_FORMAT
= EVIDENCE_PENDING

TWSE_RAW_NUMERIC_TYPE
= STRING

This evidence does not
activate the Source Contract.

---

# 16. Official Schema Evidence Matrix

Date:

machine_property
= Date

schema_type
= string

description
= 日期

machine_key_evidence
= OFFICIAL_SCHEMA_ACQUIRED

value_format
= EVIDENCE_PENDING


Opening Index:

machine_property
= OpeningIndex

schema_type
= string

description
= 開盤指數

machine_key_evidence
= OFFICIAL_SCHEMA_ACQUIRED


Highest Index:

machine_property
= HighestIndex

schema_type
= string

description
= 最高指數

machine_key_evidence
= OFFICIAL_SCHEMA_ACQUIRED


Lowest Index:

machine_property
= LowestIndex

schema_type
= string

description
= 最低指數

machine_key_evidence
= OFFICIAL_SCHEMA_ACQUIRED


Closing Index:

machine_property
= ClosingIndex

schema_type
= string

description
= 收盤指數

machine_key_evidence
= OFFICIAL_SCHEMA_ACQUIRED

---

# 17. Swagger Metadata Boundary

For the reviewed properties,
official Swagger provides:

type

description

Official Swagger does not provide:

format

pattern

example

Therefore:

SWAGGER_PROPERTY_TYPE_EVIDENCE
= ACQUIRED

SWAGGER_PROPERTY_DESCRIPTION_EVIDENCE
= ACQUIRED

SWAGGER_PROPERTY_FORMAT_EVIDENCE
= NOT_PROVIDED

SWAGGER_PROPERTY_PATTERN_EVIDENCE
= NOT_PROVIDED

SWAGGER_PROPERTY_EXAMPLE_EVIDENCE
= NOT_PROVIDED

---

# 18. Machine-Key Evidence Conclusion

Official Swagger directly declares:

Date

OpeningIndex

HighestIndex

LowestIndex

ClosingIndex

Therefore:

TWSE_MACHINE_KEY_EVIDENCE
= OFFICIAL_SCHEMA_ACQUIRED

TWSE_MACHINE_KEYS
= VERIFIED_CANDIDATE

Final promotion of protected
parent documents is not performed
by this evidence record.

---

# 19. Raw Date Type Conclusion

Official Swagger directly declares:

Date
type
= string

Therefore:

TWSE_RAW_DATE_SCHEMA_TYPE
= STRING

This evidence supports
schema type only.

It does not establish
the machine value format.

---

# 20. Raw Date Value Format Conclusion

Official Swagger provides no:

format

pattern

example

for Date.

Therefore:

TWSE_RAW_DATE_VALUE_FORMAT
= EVIDENCE_PENDING

No date format
is inferred or invented.

DATE_CONVERSION
= NOT_AUTHORIZED

---

# 21. Raw Index Type Conclusion

Official Swagger directly declares:

OpeningIndex
= string

HighestIndex
= string

LowestIndex
= string

ClosingIndex
= string

Therefore:

TWSE_RAW_NUMERIC_TYPE
= STRING

This is provider-specific
schema representation evidence.

---

# 22. Numeric Semantic Boundary

STRING schema representation
does not establish:

decimal parsing policy

thousands-separator policy

missing-value parsing policy

rounding policy

numeric comparison tolerance

Therefore:

NUMERIC_CONVERSION
= NOT_AUTHORIZED

NUMERIC_COMPARISON_TOLERANCE
= SPEC_PENDING

---

# 23. Unsupported Claims

This evidence does not prove:

TWSE raw Date value format

TWSE date conversion rule

TWSE numeric conversion rule

TWSE numeric comparison tolerance

TWSE freshness threshold

cross-source equivalence

TPEx machine schema

TPEx raw numeric type

TPEx raw date type

Therefore unsupported claims
remain blocked or pending.

---

# 24. Provider Asymmetry Protection

TWSE official schema evidence
applies only to TWSE.

It must not be copied
to TPEx.

Therefore:

PROVIDER_ASYMMETRY
= REQUIRED

TWSE_SCHEMA_EVIDENCE
!=
TPEX_SCHEMA_EVIDENCE

TPEX_MACHINE_KEYS
= EVIDENCE_PENDING

TPEX_RAW_DATE_VALUE_FORMAT
= EVIDENCE_PENDING

---

# 25. Parent Document Protection

The following protected documents
are not modified by this evidence record:

V14_WP4_OFFICIAL_EOD_FIELD_MAPPING_V1

V14_WP4_OFFICIAL_EOD_MAPPING_VALIDATION_V1

V14_WP4_OFFICIAL_EOD_VERIFICATION_POLICY_V1

V14_WP4_OFFICIAL_EOD_SOURCE_CONTRACT_V1

PARENT_DOCUMENT_MODIFICATION
= 0

Evidence acquisition
does not silently rewrite
protected parent contracts.

---

# 26. Source Contract Boundary

Current Source Contract remains:

SOURCE_CONTRACT_STATUS
= CANDIDATE

SOURCE_CONTRACT_ACTIVATION
= BLOCKED

SOURCE_CONTRACT_EXECUTION
= NOT_AUTHORIZED

TWSE_SOURCE_CONTRACT_READINESS
= BLOCKED

This evidence alone
does not activate TWSE.

---

# 27. Verification Boundary

Current official verification remains:

TWSE_OFFICIAL_VERIFICATION
= BLOCKED

VERIFICATION_EXECUTION
= NOT_AUTHORIZED

VERIFIER_IMPLEMENTATION
= NOT_AUTHORIZED

Official schema evidence
does not automatically equal
complete Official Verification.

---

# 28. Acquisition Safety Boundary

This evidence review performed:

official documentation acquisition

official Swagger schema inspection

This evidence review did not perform:

TWSE market-data endpoint execution

provider adapter execution

normalization execution

Benchmark input

Core input

database write

production write

Therefore:

MARKET_DATA_ENDPOINT_EXECUTION
= NOT_PERFORMED

REAL_GET
= 0

---

# 29. Non-Authorization Boundary

READ_ONLY
= True

EVIDENCE_STATUS
= CANDIDATE

SOURCE_CONTRACT_ACTIVATION
= BLOCKED

SOURCE_CONTRACT_EXECUTION
= NOT_AUTHORIZED

RAW_FIELD_MAPPING_EXECUTION
= NOT_AUTHORIZED

DATE_CONVERSION
= NOT_AUTHORIZED

NUMERIC_CONVERSION
= NOT_AUTHORIZED

NORMALIZATION_EXECUTION
= NOT_AUTHORIZED

VERIFICATION_EXECUTION
= NOT_AUTHORIZED

VERIFIER_IMPLEMENTATION
= NOT_AUTHORIZED

ALLOW_PROVIDER_SWITCH
= False

ALLOW_NORMALIZED_OUTPUT
= False

ALLOW_BENCHMARK_INPUT
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

PRODUCTION_WRITE
= NOT_AUTHORIZED

---

# 30. Remaining TWSE Technical Gap

After official Swagger review:

TWSE_DISPLAY_SCHEMA
= VERIFIED

TWSE_EXACT_ENDPOINT
= VERIFIED

TWSE_MACHINE_KEY_EVIDENCE
= OFFICIAL_SCHEMA_ACQUIRED

TWSE_MACHINE_KEYS
= VERIFIED_CANDIDATE

TWSE_RAW_DATE_SCHEMA_TYPE
= STRING

TWSE_RAW_NUMERIC_TYPE
= STRING

Remaining primary technical gap:

TWSE_RAW_DATE_VALUE_FORMAT
= EVIDENCE_PENDING

---

# 31. Next Work

After this evidence record
is reviewed and safely sealed:

1. Search official static documentation
   for TWSE raw Date value example.

2. Preserve:
   TWSE_RAW_DATE_VALUE_FORMAT
   = EVIDENCE_PENDING
   if no official evidence exists.

3. Only if necessary,
   separately evaluate a controlled
   official sample acquisition.

Do not proceed directly to:

- market-data Real GET
- date conversion
- numeric conversion
- Official EOD Adapter
- normalization runtime
- Benchmark Engine

---

# 32. Current Continuation Point

Parent Protected Safety Node:

624b2040d43f75e5aa06c6668182804ca9f68a61

Parent Safety Tag:

v14-wp4-official-eod-source-contract-v1-safe

Production Code Change:

0

Runner Change:

0

Market Data Real GET:

0

---

# 33. Conclusion

TWSE Official Swagger
provides direct official schema evidence
for the machine properties:

Date

OpeningIndex

HighestIndex

LowestIndex

ClosingIndex

All five properties
are declared as:

string

Therefore:

TWSE_MACHINE_KEY_EVIDENCE
= OFFICIAL_SCHEMA_ACQUIRED

TWSE_MACHINE_KEYS
= VERIFIED_CANDIDATE

TWSE_RAW_DATE_SCHEMA_TYPE
= STRING

TWSE_RAW_NUMERIC_TYPE
= STRING

However:

TWSE_RAW_DATE_VALUE_FORMAT
= EVIDENCE_PENDING

because official Swagger
does not provide:

format

pattern

example

No unsupported value format
is inferred.

Current authority remains:

SOURCE_CONTRACT_ACTIVATION
= BLOCKED

TWSE_SOURCE_CONTRACT_READINESS
= BLOCKED

TWSE_OFFICIAL_VERIFICATION
= BLOCKED

NUMERIC_CONVERSION
= NOT_AUTHORIZED

DATE_CONVERSION
= NOT_AUTHORIZED

ALLOW_NORMALIZED_OUTPUT
= False

ALLOW_BENCHMARK_INPUT
= False

OFFICIAL_EOD_ADAPTER
= NOT_AUTHORIZED

IMPLEMENTATION_GATE
= NOT_AUTHORIZED

REAL_GET
= 0

PRODUCTION_WRITE
= NOT_AUTHORIZED
