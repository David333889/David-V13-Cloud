# DAVID V14 UNIFIED ENGINE — WP4 OFFICIAL EOD MAPPING VALIDATION V1

> Work Package: WP4 — Market Context
>
> Document Type: Mapping Validation / Fail-Closed Contract Specification
>
> Parent Field Mapping:
> V14_WP4_OFFICIAL_EOD_FIELD_MAPPING_V1.md
>
> Parent Mapping Safety Baseline:
> 39739d48b60c30c824263441ca7ab24c07768f91
>
> Parent Safety Tag:
> v14-wp4-official-eod-field-mapping-v1-safe
>
> Validation Status: CANDIDATE
>
> Validation Execution: NOT AUTHORIZED
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
Mapping Validation / Fail-Closed
候選 Contract。

本文件整合：

- Required Mapping Validation
- Optional Mapping Validation
- Evidence-Pending blocking
- Missing / Zero protection
- Price Index protection
- Source governance validation
- reason vocabulary
- validation envelope
- payload completeness semantics

本文件不建立：

- executable validator
- raw-field parser
- date converter
- numeric converter
- normalization function
- Official EOD Adapter
- Benchmark Engine
- Core input
- persistence
- production write

CONTRACT SPECIFICATION
!=
VALIDATION EXECUTION

---

# 2. Existing V14 Precedent

Existing V14 contracts demonstrate
three complementary patterns.

Integration Payload:

version
state
reason
payload

Required contract failure:

state
= BLOCKED

payload
= None


Chip Contract:

metadata.status
= READY
or
MISSING

metadata.missing_fields
= [...]

Missing
!=
Zero

Missing
!=
Neutral


Evidence Observer:

allowed
= False

reason
= specific evidence reason

This WP4 validation contract
must not merge all three vocabularies
into a new incompatible envelope.

---

# 3. Contract Name

Candidate:

V14_WP4_OFFICIAL_EOD_MAPPING_VALIDATION_V1

Status:

VALIDATION_STATUS
= CANDIDATE

Execution:

VALIDATION_EXECUTION
= NOT_AUTHORIZED

---

# 4. Validation Envelope

Candidate top-level envelope:

version

state

reason

payload

Candidate states:

READY

BLOCKED

No additional PARTIAL state
is introduced.

PARTIAL_STATE
= NOT_ADOPTED

---

# 5. Why state Instead of allowed

This document defines
a mapping validation contract.

It is not an evidence-observation
execution boundary.

Therefore:

state
is used for the validation envelope.

allowed
is not added to this contract.

ALLOWED_FIELD
= NOT_ADOPTED

This avoids mixing:

Integration Contract vocabulary

with:

Evidence Observer vocabulary.

---

# 6. READY State

Candidate:

state
= READY

Meaning:

All required validation conditions
are satisfied at the contract level.

READY does not mean:

- normalization authorized
- adapter authorized
- production authorized
- Benchmark Engine authorized

READY
!=
IMPLEMENTATION AUTHORIZATION

---

# 7. BLOCKED State

Candidate:

state
= BLOCKED

Meaning:

The candidate record or mapping
must not proceed as a usable
validated mapping payload.

Candidate:

payload
= None

for blocked validation.

BLOCKED
= FAIL_CLOSED

---

# 8. Reason Vocabulary

Candidate reasons:

OK

REQUIRED_MAPPING_MISSING

MACHINE_KEY_EVIDENCE_PENDING

DATE_FORMAT_EVIDENCE_PENDING

NUMERIC_TYPE_EVIDENCE_PENDING

INDEX_TYPE_MISMATCH

SOURCE_CHANNEL_MISMATCH

LICENSE_STATUS_MISSING

Reason vocabulary must remain
small and explicit.

Do not create vague reasons
when a specific blocker exists.

---

# 9. Successful Validation Result

Candidate:

version
= V14_WP4_OFFICIAL_EOD_MAPPING_VALIDATION_V1

state
= READY

reason
= OK

payload
= validated candidate payload

This remains specification-only.

---

# 10. Blocked Validation Result

Candidate:

version
= V14_WP4_OFFICIAL_EOD_MAPPING_VALIDATION_V1

state
= BLOCKED

reason
= specific fail-closed reason

payload
= None

No blocked result may expose
a usable normalized payload.

---

# 11. Required Mapping Policy

Required canonical targets:

identity.trading_date

identity.market

identity.index_id

market_data.open

market_data.high

market_data.low

market_data.close

metadata.provider

metadata.source_channel

metadata.source_role

metadata.license_status

Status:

REQUIRED_MAPPING
= CANDIDATE

---

# 12. Required Missing Policy

If any required mapping field
is absent, None, or empty
where empty is invalid:

state
= BLOCKED

reason
= REQUIRED_MAPPING_MISSING

payload
= None

Required missing
must not become:

- zero
- neutral
- previous value
- fabricated value
- optional field

REQUIRED_MISSING_POLICY
= FAIL_CLOSED

---

# 13. Required Record Rejection Semantics

RECORD_REJECTED
is a semantic description.

The formal V14 validation state is:

BLOCKED

Therefore:

RECORD_REJECTED
→ state = BLOCKED

Do not create a separate
RECORD_REJECTED state.

---

# 14. Optional Mapping Policy

Current optional canonical target:

market_data.change

Status:

OPTIONAL_MAPPING
= CANDIDATE

Optional absence alone
must not block the entire record.

---

# 15. Optional Missing Result

If:

market_data.change
is unavailable,

candidate result may remain:

state
= READY

reason
= OK

while:

payload.market_data.change
= None

and:

payload.metadata.status
= MISSING

payload.metadata.missing_fields
contains:

market_data.change

---

# 16. No PARTIAL State

Existing V14 Chip Contract already uses:

READY

MISSING

for payload completeness.

Therefore:

PARTIAL
is not introduced.

PARTIAL_STATE
= NOT_ADOPTED

Optional missing
must not create a new
top-level validation state.

---

# 17. Payload Metadata Completeness

Candidate payload metadata includes:

status

missing_fields

Candidate metadata status:

READY

or

MISSING

If no optional field is missing:

metadata.status
= READY

metadata.missing_fields
= []

If optional field is missing:

metadata.status
= MISSING

metadata.missing_fields
contains the exact canonical field path.

---

# 18. missing_fields Scope

missing_fields records
actual record-data absence.

Example:

market_data.change

Valid:

missing_fields
= ["market_data.change"]

Do not place specification blockers
inside missing_fields.

Invalid examples:

TPEX_MACHINE_KEYS

RAW_NUMERIC_TYPE

DATE_FORMAT_EVIDENCE

Those are evidence / specification states,
not record fields.

---

# 19. Missing / Zero Protection

Candidate policy:

ZERO_IS_NOT_MISSING

Missing
!=
Zero

Missing
!=
Neutral

Zero
!=
Missing

No missing required value
may be silently converted to zero.

No optional missing value
may be silently converted to zero.

---

# 20. Evidence-Pending Policy

Evidence Pending
is not ordinary field missing.

Evidence Pending means:

The specification does not yet
have sufficient evidence
to authorize executable interpretation.

Therefore:

EVIDENCE_PENDING
→ BLOCKED

not:

EVIDENCE_PENDING
→ metadata.status = MISSING

---

# 21. Machine-Key Evidence Pending

If required provider machine-key
evidence is insufficient:

state
= BLOCKED

reason
= MACHINE_KEY_EVIDENCE_PENDING

payload
= None

Current relevant state:

TPEX_MACHINE_KEYS
= EVIDENCE_PENDING

Therefore:

TPEX_EXECUTABLE_MAPPING
= BLOCKED_BY_EVIDENCE

---

# 22. TWSE Machine-Key Maturity

Current parent mapping:

TWSE_MACHINE_KEYS
= STRONG_CANDIDATE

This is not:

VERIFIED

or:

LOCKED

Therefore:

TWSE executable mapping
is not authorized merely because
machine keys are strong candidates.

TWSE_EXECUTABLE_MAPPING
= NOT_AUTHORIZED

---

# 23. Date-Format Evidence Pending

If raw date value format
is not locked:

state
= BLOCKED

reason
= DATE_FORMAT_EVIDENCE_PENDING

payload
= None

No implicit:

ROC → Gregorian

or:

raw date → ISO

conversion is authorized.

DATE_CONVERSION
= NOT_AUTHORIZED

---

# 24. Numeric-Type Evidence Pending

Current parent mapping:

RAW_NUMERIC_TYPE
= EVIDENCE_PENDING

Therefore:

state
= BLOCKED

reason
= NUMERIC_TYPE_EVIDENCE_PENDING

payload
= None

No implicit:

string → float

comma removal

rounding

precision conversion

is authorized.

NUMERIC_CONVERSION
= NOT_AUTHORIZED

---

# 25. Current TWSE Validation Readiness

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

Therefore:

TWSE_VALIDATION_READINESS
= BLOCKED

Current blockers include:

DATE_FORMAT_EVIDENCE_PENDING

NUMERIC_TYPE_EVIDENCE_PENDING

and machine-key lock remains incomplete.

---

# 26. Current TPEx Validation Readiness

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

Therefore:

TPEX_VALIDATION_READINESS
= BLOCKED

Primary blocker:

MACHINE_KEY_EVIDENCE_PENDING

Additional blockers:

DATE_FORMAT_EVIDENCE_PENDING

NUMERIC_TYPE_EVIDENCE_PENDING

---

# 27. Price Index Validation

Target contract:

INDEX_TYPE
= PRICE_INDEX

If source evidence indicates:

TOTAL_RETURN_INDEX

or Price / Total Return identity
is ambiguous:

state
= BLOCKED

reason
= INDEX_TYPE_MISMATCH

payload
= None

TOTAL_RETURN_SUBSTITUTION
= NOT_AUTHORIZED

---

# 28. Source Channel Validation

Required:

metadata.source_channel
= GOVERNMENT_OPEN_DATA

If source channel differs:

state
= BLOCKED

reason
= SOURCE_CHANNEL_MISMATCH

payload
= None

This protects the separation between:

Government Open Data

and:

Data E-Shop

Subscribed Market Data

Commercial Data Product

Realtime Feed

---

# 29. License Validation

Required candidate:

metadata.license_status

For reviewed open-data sources:

GOVERNMENT_OPEN_DATA_LICENSE_V1

If license status is missing:

state
= BLOCKED

reason
= LICENSE_STATUS_MISSING

payload
= None

Unknown license
must not become
authorized use.

---

# 30. Provider Identity Validation

Candidate provider constants:

TWSE

TPEX

Candidate market constants:

TWSE

TPEX

Candidate index identities:

TAIEX

TPEX

Unknown or conflicting identity:

must fail closed.

Provider identity validation
remains specification-level.

---

# 31. Schema Drift Protection

If provider schema changes
such that expected mapping evidence
no longer matches:

validation must fail closed.

SCHEMA_DRIFT
→ BLOCKED

Exact future reason vocabulary
for schema drift remains:

SPEC_PENDING

No automatic remapping
is authorized.

---

# 32. Unknown Field Policy

Unknown provider fields
must not automatically become
canonical fields.

Unknown field:

→ ignore only if explicitly safe
or
→ block when it affects required semantics

Exact executable behavior remains:

NOT_AUTHORIZED

---

# 33. Payload Structure Candidate

Candidate READY payload follows
the parent schema structure:

identity

market_data

metadata

semantic_evidence

Candidate metadata adds:

status

missing_fields

This document does not define
a flattened storage row.

---

# 34. Storage Boundary

Validation payload
!=
Storage Record

No Supabase-compatible row
is created by this contract.

ALLOW_SUPABASE_WRITE
= False

STORAGE_MAPPING
= NOT_AUTHORIZED

---

# 35. Evidence Gap vs Data Missing

Data Missing:

A record field expected under
an already-known contract is absent.

Handling:

required
→ BLOCKED

optional
→ metadata.status = MISSING


Evidence Gap:

The contract itself lacks enough evidence
to interpret a provider field safely.

Handling:

→ BLOCKED
→ specific EVIDENCE_PENDING reason

Therefore:

DATA_MISSING
!=
EVIDENCE_GAP

---

# 36. Validation Order Candidate

Candidate validation order:

1. contract/version structure
2. evidence readiness
3. provider identity
4. source channel
5. license status
6. index type
7. required field presence
8. date-format readiness
9. numeric-type readiness
10. optional field completeness

Status:

VALIDATION_ORDER
= CANDIDATE

Execution remains unauthorized.

---

# 37. No Executable Validator

This document does not create:

validate_official_eod_mapping()

or any equivalent executable validator.

VALIDATOR_IMPLEMENTATION
= NOT_AUTHORIZED

VALIDATION_EXECUTION
= NOT_AUTHORIZED

---

# 38. Parent Mapping Status

Parent:

V14_WP4_OFFICIAL_EOD_FIELD_MAPPING_V1

remains:

FIELD_MAPPING_STATUS
= CANDIDATE

TWSE_MACHINE_KEYS
= STRONG_CANDIDATE

TPEX_MACHINE_KEYS
= EVIDENCE_PENDING

RAW_NUMERIC_TYPE
= EVIDENCE_PENDING

This validation specification
does not upgrade those states.

---

# 39. Parent Schema Status

Parent:

V14_NORMALIZED_DAILY_PRICE_INDEX_V1

remains:

SCHEMA_STATUS
= CANDIDATE

ALLOW_NORMALIZED_OUTPUT
= False

This validation specification
does not authorize normalization.

---

# 40. Official-EOD Architecture Status

Parent architecture remains:

WP4_OFFICIAL_EOD_BENCHMARK_EXCEPTION
= STRONG_ARCHITECTURE_CANDIDATE

EXCEPTION_SCOPE
= WP4_DAILY_BENCHMARK_ONLY

GLOBAL_PRIMARY_PROVIDER
= FINMIND

This validation specification
does not activate the exception.

---

# 41. Non-Authorization Boundary

READ_ONLY
= True

VALIDATION_STATUS
= CANDIDATE

VALIDATION_EXECUTION
= NOT_AUTHORIZED

VALIDATOR_IMPLEMENTATION
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

# 42. Current Validation Matrix

Required Missing:

state
= BLOCKED

reason
= REQUIRED_MAPPING_MISSING

payload
= None


Optional Missing:

state
= READY

reason
= OK

payload metadata status
= MISSING

missing_fields
= exact optional canonical field


Machine-Key Evidence Pending:

state
= BLOCKED

reason
= MACHINE_KEY_EVIDENCE_PENDING

payload
= None


Date-Format Evidence Pending:

state
= BLOCKED

reason
= DATE_FORMAT_EVIDENCE_PENDING

payload
= None


Numeric-Type Evidence Pending:

state
= BLOCKED

reason
= NUMERIC_TYPE_EVIDENCE_PENDING

payload
= None


Index-Type Mismatch:

state
= BLOCKED

reason
= INDEX_TYPE_MISMATCH

payload
= None


Source-Channel Mismatch:

state
= BLOCKED

reason
= SOURCE_CHANNEL_MISMATCH

payload
= None


License Status Missing:

state
= BLOCKED

reason
= LICENSE_STATUS_MISSING

payload
= None

---

# 43. Current Readiness

TWSE_VALIDATION_READINESS
= BLOCKED

TPEX_VALIDATION_READINESS
= BLOCKED

VALIDATION_STATUS
= CANDIDATE

VALIDATION_EXECUTION
= NOT_AUTHORIZED

No provider currently receives
executable READY authorization.

---

# 44. Next Work

After this validation contract
is reviewed and safely sealed:

1. Official Verification Policy Review
2. Source Contract Review
3. Evidence-gap resolution planning
4. Re-evaluate implementation authority

Do not proceed directly to:

- executable validator
- raw mapping implementation
- Official EOD Adapter
- normalized output
- Benchmark Engine

---

# 45. Current Continuation Point

Parent Mapping Safety Baseline:

39739d48b60c30c824263441ca7ab24c07768f91

Parent Safety Tag:

v14-wp4-official-eod-field-mapping-v1-safe

Production Code Change:

0

Runner Change:

0

Market Data Real GET:

0

---

# 46. Conclusion

WP4 Official-EOD Mapping Validation
now has a candidate fail-closed
contract specification.

The contract preserves:

Required missing
→ BLOCKED

Optional missing
→ READY + metadata MISSING

Evidence pending
→ BLOCKED

Missing
!=
Zero
!=
Neutral

No PARTIAL state is introduced.

Therefore:

VALIDATION_STATUS
= CANDIDATE

VALIDATION_EXECUTION
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
