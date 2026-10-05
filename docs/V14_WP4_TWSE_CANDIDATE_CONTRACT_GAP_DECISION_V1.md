# DAVID V14 WP4 TWSE Candidate Contract Gap Decision V1

Review date: 2026-10-05 Asia/Taipei

The bounded official-source search found identity reference and product-format
evidence, but no sufficient response-scope contract for the proposed daily-close
web API. Keep that route as a research candidate. Do not select it for execution
or continue generating mock tests as a substitute for provider evidence.

## Baselines and search scope

Original project baseline: `a0143836f70d4a981beefbff731c1cd3bc5ccd1f`.
Isolated parent checkpoint: `05b742ab2c0d1e1e21a35c922004037cefe8aaa4`.

Eight official-domain search queries covered exact route fields, MI_INDEX API
dates, A05+ dates, index identity, and non-trading-day behavior. The official
Data E-Shop metadata, index reference table, and linked A05+ format document were
inspected. This is a bounded search outcome, not proof that no specification
exists. No report API, sample-price file, or paid purchase was executed.

## New evidence

The official index reference table contains the row IX0001 with the label
`臺股指數` and ISIN `TW000IX00010`. This establishes a reference identity row.
It does not establish which field or value represents that identity in the
unobserved web-report JSON response, or prove the target's runtime linkage.
The reference snapshot was decoded as cp950; raw bytes and SHA256 were retained.

The official A05+ format is a 120-byte fixed-width Index Summary product for
BFIGUU/BFIGVU/BFIGWU. It specifies an eight-digit Date field at the start and
index identity and closing-value fields. Its recorded revision history includes
2019/04/29 and 2019/12/16. An eight-digit numeric field alone does not establish
the web API's date encoding, or authorize Gregorian/ROC conversion.

That product specification is not a schema for `/rwd/zh/afterTrading/MI_INDEX`.
Do not copy fixed-width offsets, numeric formats, product timing or identity
fields into a JSON parser. No product sample was downloaded and no sample value
was promoted to qualified Date evidence.

Official sources:

- <https://isin.twse.com.tw/isin/C_public.jsp?strMode=11>
- <https://eshop.twse.com.tw/zh/product/detail/cfec9a1470e448ec91bfde006db361e8>
- <https://eshop.twse.com.tw/uploadFile/upload/000000006e0bbe8d016f3aefddf00377.docx>

Capture metadata and the product/reference separation are preserved in
`evidence/TWSE_CANDIDATE_CONTRACT_SEARCH_EVIDENCE_20261005.json`.
The first raw reference-table request failed with a connection reset; a subsequent
capture succeeded. That was a documentation request, not a market-data retry.

## Remaining contract gaps

| Requirement | Finding | State |
| --- | --- | --- |
| Candidate date selector | Day-mode official UI | STATIC_UI_EVIDENCE_ONLY |
| Complete response single-date guarantee | No sufficient contract found | BLOCKED |
| Invalid/holiday/no-data behavior | Not established for exact API | PENDING |
| Exact response containers and field labels | No API schema or runtime sample | PENDING |
| Target index reference | IX0001 reference row captured | REFERENCE_ONLY |
| Target index in candidate JSON | Field/value linkage absent | PENDING |
| Raw Date format and location | Product format differs from API | PENDING |
| Freshness/publication revision semantics | Exact API contract absent | PENDING |

## Precise source-owner clarification

The following questions are ready for review or later authorized outreach:

1. Is `/rwd/zh/afterTrading/MI_INDEX` a supported public machine interface, and
   where is its versioned parameter and response specification?
2. What is the exact `date` input format, and does it guarantee that the complete
   returned payload covers only that requested trading date?
3. What occurs on holidays, invalid dates, or unavailable history: empty result,
   explicit error, or substitution with another date? Is substitution forbidden?
4. Which response containers and fields provide the authoritative raw trading
   date and the TAIEX identity? How does the reference IX0001 map to those fields?
5. Are index identity labels and Date formats stable, and how are schema changes
   announced? What is the policy for duplicate/missing identity records?
6. What are the response finality and revision rules, and which access terms,
   media types, limits and transport requirements apply to this exact interface?

These questions have not been sent. This review does not authorize outreach,
purchase, credentials, or market-data acquisition.

## Execution decision

`PUBLIC_CONTRACT_SEARCH = COMPLETED_WITH_GAPS`.
`RESEARCH_CANDIDATE = WEB_DAILY_CLOSE_UI_ROUTE`.
`NEW_ENDPOINT_EXECUTION_SELECTION = NOT_SELECTED`.
`SINGLE_TRADING_DATE_ENFORCEMENT = BLOCKED`.
`TWSE_CLASSIFIER_COMPATIBILITY = NOT_ESTABLISHED`.
`TIMEOUT_READINESS = BLOCKED`.
`EXECUTION_READINESS = BLOCKED`.

Stop this candidate's public-search phase at the documented gap decision.
The next evidence-changing step is obtaining the exact official contract or
choosing an explicitly revised acquisition plan. Do not imply readiness from
another report, another provider, or a locally filtered subset.

Original-project adoption of the isolated timeout fix remains an independent
action requiring write access. It does not depend on resolving TWSE's public
contract gaps. Remote verification and formal project sealing remain pending.

## Preservation

This step changes documentary evidence only. Existing timeout code tests remain
the six-gate results from the isolated fix checkpoint; no new full regression or
runtime API validation is claimed. Market-data endpoint calls and database writes
in this phase are zero. The new isolated commit and bundle preserve the gap
decision without overwriting original protected reviews.
