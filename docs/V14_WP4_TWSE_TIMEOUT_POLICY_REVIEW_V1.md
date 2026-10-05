# DAVID V14 WP4 TWSE Timeout Policy Review V1

Review date: 2026-10-05 Asia/Taipei

This review defines a candidate timeout contract for a future TWSE acquisition.
It does not enable that acquisition. Existing FinMind timeout validation has been
hardened in the isolated review branch; TWSE transport readiness remains blocked.

## Baselines and scope

- Original project baseline: `a0143836f70d4a981beefbff731c1cd3bc5ccd1f`.
- Isolated validation fix: `0d09f72c932a5752a1deb349b7980fdb48064ea0`.
- Scope: specification review and offline evidence.
- Market-data GETs in this work: 0. Production and database writes: 0.
- Original project adoption: pending. Remote sealing: not verified.

The original project's HEAD has not been replaced by the isolated commit.
Earlier protected documents remain historical evidence; their status fields are
not silently rewritten by this review.

## Existing implementation findings

`v14/live_session_boundary.py` limits the host to FinMind and accepts positive
scalar timeouts up to 30 seconds. The isolated fix additionally rejects boolean
and non-finite values. Four valid and twelve invalid boundary cases were checked;
invalid values were also rejected before session creation by the orchestrator.

`v14/finmind_live_backend.py` enforces its FinMind URL and passes timeout to an
injected session. `v14/controlled_live_fetch.py` loads and forwards a FinMind
token. Neither is a reviewed TWSE execution path. The transport has no reviewed
whole-operation deadline or provider-independent cancellation contract.

`MAX_RETRIES = 0` is not proof that every injected client adapter has retries
disabled. The actual client configuration must be checked before execution.

## Candidate timeout contract

| Field | Candidate seconds | Meaning | Activation |
| --- | ---: | --- | --- |
| connect_timeout | 5 | Candidate connection wait limit | Not activated |
| read_idle_timeout | 10 | Candidate wait limit without receive progress | Not activated |
| acquisition_deadline | 20 | Candidate elapsed budget including worker startup and body acquisition | Not activated |

These are engineering candidates, not measured TWSE latency or an official
service guarantee. Their purpose is to bound occupation of a one-shot operation.
The selected HTTP client's DNS, TLS, connection, and read semantics must be
verified before values can be approved. Parsing and evidence persistence require
their own bounded budget or explicit inclusion in a full-operation deadline.
Cleanup has a separate bound and must be reported separately.

All values must be finite positive numbers, explicitly excluding booleans.
Reject missing values, strings, unsupported tuples, zero, negative values, NaN,
infinities, and out-of-policy magnitudes before creating a session or worker.
The existing scalar FinMind validator does not accept a connect/read tuple.
Do not insert `(5, 10)` into that interface without a separately reviewed change.

## Cancellation and attempt policy

Validate policy, reserve the one-shot attempt, start the worker, receive under a
monotonic deadline, enter a terminal state, then clean up. Startup failure after
reservation consumes the attempt. None of the terminal failures resets it.

Before accepting a result, recheck the monotonic deadline. A late successful
response remains a failure. Progress does not extend the acquisition deadline.
Timeouts, unexpected responses, redirects, malformed evidence, and transport
errors stop the operation without retry or CSV fallback.

A process-based cancellation design is a candidate supported by offline probes.
It is not a production implementation. Waiting on a future with a timeout or
checking elapsed time after a blocking GET returns does not establish effective
cancellation. Every directly or indirectly created worker must be accounted for.
Cleanup failure must produce a distinct failure and cannot be recorded as CLEAN.

The offline prototype uses mock messages only. It tested normal completion,
transport error, blocked work, sustained progress, late results, abnormal exit,
malformed and excessive IPC, startup failure, and twelve invalid policy values.
All directly created workers exited. It did not test real HTTP cancellation,
descendant processes, startup hard deadlines, or injected cleanup failure.
Its file-size precheck has a growth race; production IPC requires bounded reads,
message-size enforcement, payload validation, and secret sanitization.

## Evidence requirements

Record policy version, original and isolated baselines, provider and endpoint
identity, attempt identity and count, start time with timezone, monotonic elapsed
time, configured limits, terminal reason, cancellation and cleanup outcomes.
Record status, media type, and received bytes only when actually observed.
Do not infer that a timeout means the remote server did not receive the request.
Do not turn partial diagnostic body content into qualified RAW_EVIDENCE.

## Completion criteria

Before `TIMEOUT_READINESS` can become ready, a reviewed TWSE-specific path must
prove policy rejection before resource creation, effective deadline cancellation,
bounded startup and cleanup, process-tree control, secure bounded IPC, no client
retries or redirects, response-size limits, and sanitized failure evidence.
The exact cutoff race requires deterministic clock-injection tests. The chosen
values and budget coverage must be explicitly approved within the execution plan.

This review does not close single-trading-date enforcement, classifier
compatibility, endpoint authorization, or production activation.

## Decision

| State | Decision |
| --- | --- |
| TIMEOUT_POLICY_REVIEW | CANDIDATE_SPEC_RECORDED |
| FINMIND_TIMEOUT_VALIDATION_FIX | VERIFIED_IN_ISOLATED_BRANCH |
| ORIGINAL_PROJECT_FIX_ADOPTION | PENDING |
| TWSE_CANCELLATION_IMPLEMENTATION | NOT_ESTABLISHED |
| TIMEOUT_READINESS | BLOCKED |
| EXECUTION_READINESS | BLOCKED |
| RAW_EVIDENCE_PROMOTION | BLOCKED |
| MARKET_DATA_ENDPOINT_EXECUTION | NOT_PERFORMED |

## Sources

- `V14_WP4_TWSE_CONTENT_TYPE_SELECTION_REVIEW_V1.md`, sections 28 and 33.
- `V14_WP4_TWSE_CONTROLLED_DATE_SAMPLE_ACQUISITION_PLAN_V1.md`, request, retry,
  redirect and execution preconditions.
- `v14/live_session_boundary.py`, `v14/finmind_live_backend.py`,
  `v14/read_only_transport.py`, `v14/controlled_live_fetch.py`.
- Isolated six-gate run, captured in `DAVID_V14_Isolated_Checkpoint_Test_Log.txt`
  and `DAVID_V14_Isolated_Checkpoint_Test_Results.json` in task outputs.
- Offline cancellation probes, captured in
  `DAVID_V14_Deadline_Failure_Probe_Results.json` in task outputs.
