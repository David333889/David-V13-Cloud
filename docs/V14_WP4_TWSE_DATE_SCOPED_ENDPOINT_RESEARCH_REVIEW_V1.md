# DAVID V14 WP4 TWSE Date Scoped Endpoint Research Review V1

Review date: 2026-10-05 Asia/Taipei

The daily-close web report is a research candidate for date-scoped evidence.
It is not selected for execution and does not replace the existing OpenAPI route.
The index-history web page is configured for month selection, which reinforces
the need to distinguish a date-looking input from a one-date acquisition contract.

## Baselines

- Original project baseline: `a0143836f70d4a981beefbff731c1cd3bc5ccd1f`.
- Isolated parent checkpoint: `74b5c2d89b26a896800b9823e5d05649c4437528`.
- Mode: static source inspection only; no page scripts executed.
- Direct market-data endpoint calls: 0. Database and production writes: 0.

## Captured official sources

The following static files were retrieved, saved and hashed:

- <https://www.twse.com.tw/zh/indices/taiex/mi-5min-hist.html>
- <https://www.twse.com.tw/zh/trading/historical/mi-index.html>
- <https://www.twse.com.tw/res/js/web-report.js>
- <https://www.twse.com.tw/res/js/web.js>
- <https://www.twse.com.tw/res/js/main.js>
- <https://www.twse.com.tw/res/css/web-report.css>

Raw artifacts are retained in task outputs. Retrieval times and hashes are in
`evidence/TWSE_DATE_SCOPED_CANDIDATE_STATIC_EVIDENCE_20261005.json`.
The static pages contain empty table containers; no runtime JSON was acquired.
Search-engine report excerpts were discovery leads only, not runtime samples or
qualified machine-field evidence. No report API URL from those results was opened.

## Historical report finding

The index-history HTML form names `/TAIEX/MI_5MINS_HIST` and uses date mode `M`.
The official stylesheet hides the day selector in mode M. This establishes a
month-oriented user-interface configuration, not the OpenAPI response scope.
It does not establish an execution alias for `/indicesReport/MI_5MINS_HIST`.

The selected OpenAPI candidate remains unchanged. Its missing date-query and
single-date scope guarantees are not repaired by copying web-report parameters.

## Daily-close research candidate

The daily-close page names `/afterTrading/MI_INDEX` and uses date mode `D`.
Static report code constructs requests from the configured report host, language
and form route. The production configuration uses `/rwd`; combining those facts
gives `/rwd/zh/afterTrading/MI_INDEX` as a derived research route. It was not called.
The date widget builds a year-month-day string. Static UI behavior is evidence of
how the official client prepares a query, not a complete server API contract.

The separately documented OpenAPI operation `/exchangeReport/MI_INDEX` has a
different route and field lineage. Its stored schema lists date, index identity,
closing index, direction and change fields. It does not list the four English
OHLC index properties required by the existing index-history schema. Do not
treat these two MI_INDEX routes as identical or invent missing OHLC fields.

## Candidate comparison

| Route context | Date evidence | Field evidence | Decision |
| --- | --- | --- | --- |
| Selected OpenAPI index history | No declared date parameter | Five English string properties | Existing candidate; scope blocked |
| Web index history | Month-oriented UI | Runtime JSON not observed | Not a single-date replacement |
| Web daily close | Day-oriented UI | Runtime JSON not observed | Research candidate only |
| OpenAPI daily close | No date parameter established in stored operation | Different field names; closing statistics | Not a drop-in OHLC replacement |

The endpoint name alone does not establish index identity, publication finality,
requested-date equality, complete response date scope or schema compatibility.
Multiple securities or indices within one date also differ from multiple dates;
any allowed identity filtering needs its own reviewed rule.

## Evidence required before selecting the new route

Obtain official static API or format documentation specifying parameter meaning,
date format, empty/non-trading-day behavior, exact response containers, field
locations, and whether the complete response is restricted to the target date.
Establish the target TAIEX identity and which fields serve the Date-only evidence
purpose. Separately assess any later OHLC/benchmark requirements; a Date-only
candidate must not automatically satisfy those requirements.

Then review provider-specific media type, parser, classifier, timeout, size,
redirect, retry and authorization boundaries. A documentation gap does not permit
a diagnostic GET while the acquisition scope is still unreviewed. If the plan
must change, record the scope revision explicitly before execution review.

## Decision and next step

`DATE_SCOPED_RESEARCH_CANDIDATE = WEB_DAILY_CLOSE_UI_ROUTE`.
`NEW_ENDPOINT_EXECUTION_SELECTION = NOT_SELECTED`.
`SINGLE_TRADING_DATE_ENFORCEMENT = BLOCKED`.
`TWSE_CLASSIFIER_COMPATIBILITY = NOT_ESTABLISHED`.
`EXECUTION_READINESS = BLOCKED`.

Continue static documentation research for this candidate's response and index
identity contract. If no sufficient public official specification is found,
record that bounded search outcome and prepare the precise clarification needed
from the source owner; do not infer a guarantee from the UI or silently relax the
plan. No outreach is sent by this review.

## Validation and preservation

Both HTML snapshot hashes were checked against the capture manifest. Form routes
and date modes were extracted from the saved bytes. Script and stylesheet assets
were read as source only. No HTTP client integration or market-data test follows
from this document. Original protected reviews remain unchanged.

The isolated code fix retains its previous six-gate validation; this step adds
only documentary review and evidence. Original-project adoption and remote
verification remain pending and are distinct from this local checkpoint.
