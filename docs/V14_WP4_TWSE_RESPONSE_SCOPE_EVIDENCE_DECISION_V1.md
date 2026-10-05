# DAVID V14 WP4 TWSE Response Scope Evidence Decision V1

Review date: 2026-10-05 Asia/Taipei

The selected OpenAPI route remains unsuitable for executable single-date
acquisition under the current evidence. A fresh static specification snapshot
confirms a schema declaration but does not close acquisition-scope semantics.
This decision adds evidence and identifies the next evidence requirements.

## Baselines and evidence

- Original project: `a0143836f70d4a981beefbff731c1cd3bc5ccd1f`.
- Isolated timeout fix: `0d09f72c932a5752a1deb349b7980fdb48064ea0`.
- Official static source: <https://openapi.twse.com.tw/v1/swagger.json>.
- Retrieved: `2026-10-05T17:45:02.267158+08:00`.
- Raw source SHA256: `06e1cea82448361e733a0ad1ae16e52f5d5d6b71905acd078472f852c32c0eb0`.
- Selected operation preserved in `evidence/TWSE_RESPONSE_SCOPE_STATIC_EVIDENCE_20261005.json`.
- Full raw snapshot preserved in task outputs as `TWSE_Official_Swagger_20261005.json`.

Only the official documentation URL was retrieved. No market-data route was
called, no response sample obtained, and no runtime date value established.
The operation excerpt can be traced to the raw snapshot hash; the excerpt is
not a substitute for the complete source artifact.

## Fresh specification findings

The selected GET operation is `/indicesReport/MI_5MINS_HIST`. It advertises JSON
and CSV. Its HTTP 200 schema declares an object with five string properties:
Date, OpeningIndex, HighestIndex, LowestIndex, and ClosingIndex.

In this snapshot, `parameters` is absent rather than explicitly null. Earlier
reviews recorded null. Both observations provide no declared date query; preserve
that representational difference instead of overwriting historical evidence.

The response schema does not contain `required` or `additionalProperties`.
It therefore does not explicitly mark Date as mandatory or restrict responses
to exactly five keys. A property declaration is not a runtime presence guarantee.
Date has no declared format, pattern, or example in this operation.

No runtime response, record cardinality, or single-trading-date acquisition
guarantee was established by this documentation retrieval.

## Scope decision

There are two distinct questions: whether an acquired response fits a reviewed
container contract, and whether the acquisition itself stays within one approved
trading-date context. Accepting one matching record after downloading multiple
dates would only address output selection, not the acquisition requirement.

Current evidence does not establish a date selector for this route or an official
guarantee that its complete response covers one approved date. Do not invent Date,
start_date, or end_date parameters. Do not transfer the web-report route's query
parameters or treat its URL as an execution alias.

A runtime object with a string Date would still require verified date format,
index identity, target-date matching, and response-scope semantics before it could
be accepted. A schema mismatch, array, duplicate key, missing Date, or multiple
date context must not be repaired by silently filtering, unwrapping, normalizing,
or coercing the response. These are future acceptance-policy requirements, not
implemented TWSE parser behavior.

## Next evidence route

First seek official static endpoint documentation or an official example that
explicitly establishes response scope, field location, required presence, and
date semantics. An example alone illustrates a value; it does not prove all
responses have the same cardinality or scope.

If static evidence remains insufficient, decide whether a different explicitly
date-scoped official route can be reviewed as a new endpoint candidate. That
requires its own schema lineage, parameter contract, and selection review.
No automatic endpoint or provider switch is made here.

A diagnostic market-data request cannot be used to bootstrap authorization while
single-date acquisition remains blocked. Any proposed relaxation of that scope
requires an explicit plan revision and review; this document does not relax it.

## Readiness matrix

| Requirement | Current evidence | Decision |
| --- | --- | --- |
| Static operation snapshot | Retrieved and hashed | EVIDENCE_CAPTURED |
| Date query declaration | None found in selected operation | NOT_ESTABLISHED |
| Date presence guarantee | No required list | NOT_ESTABLISHED |
| Exact key restriction | No additionalProperties restriction | NOT_ESTABLISHED |
| Date raw format | No format, pattern or example | EVIDENCE_PENDING |
| Actual response container | No runtime sample | NOT_OBSERVED |
| One-date acquisition guarantee | Not established | BLOCKED |
| FinMind classifier compatibility | Not established | BLOCKED |
| Timeout readiness | Candidate specification only | BLOCKED |
| Execution readiness | Preconditions remain open | BLOCKED |

## Preservation and limits

This is a docs-only isolated-branch decision. The parent schema, endpoint,
single-date, and content-type reviews are retained unchanged. The original
project has not adopted the isolated timeout fix. No remote branch or tag
verification is claimed, and no database backup or recovery test was performed.

The next checkpoint should record any new official scope evidence and the exact
decision it supports. Until then, no market-data GET, CSV fallback, parser
activation, date conversion, normalization, classifier promotion, or production
write follows from this document.

## Historical sources

- `V14_WP4_TWSE_OFFICIAL_SCHEMA_EVIDENCE_V1.md`.
- `V14_WP4_TWSE_DATE_SAMPLE_ENDPOINT_SELECTION_REVIEW_V1.md`.
- `V14_WP4_TWSE_SINGLE_TRADING_DATE_ENFORCEMENT_REVIEW_V1.md`.
- `V14_WP4_TWSE_CONTENT_TYPE_SELECTION_REVIEW_V1.md`.
- `V14_WP4_TWSE_TIMEOUT_POLICY_REVIEW_V1.md`.
