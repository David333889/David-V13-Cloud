# V14 Yahoo / FinMind Baseline Evidence Compare V1

## 1. Purpose

Define the read-only baseline evidence comparison boundary between the
legacy Yahoo/yfinance market-data path and FinMind TaiwanStockPrice.

This specification does not establish provider compatibility.

## 2. Gate

Gate 28D.2K - Yahoo / FinMind Baseline Evidence Compare V1

## 3. Comparison Layers

### Yahoo / yfinance

Comparison layer:

- legacy cleaned market_data
- fetch-path provenance is required
- cleaned market_data is NOT the Yahoo raw payload

### FinMind

Comparison layer:

- TaiwanStockPrice RAW_EVIDENCE records
- raw validation is allowed
- raw evidence preservation is allowed
- normalization is not allowed

This comparison MUST NOT be described as raw-to-raw comparison.

## 4. Required Compare Dimensions

The comparison reuses the Gate 28D.2I contract dimensions:

- SAME_STOCK
- SAME_TRADING_DATE
- OHLC
- VOLUME

Allowed comparison results remain:

- MATCH
- MISMATCH
- NOT_COMPARED
- INSUFFICIENT_EVIDENCE

## 5. Evidence Matrix

| Dimension | Yahoo Evidence | FinMind Evidence |
| --- | --- | --- |
| Stock | symbol + fetch provenance | stock_id |
| Trading Date | cleaned market_data date/index | date |
| Open | Open | open |
| High | High | max |
| Low | Low | min |
| Close | Close | close |
| Volume | Volume | Trading_Volume |

## 6. Sample Selection Policy

The first baseline sample MUST:

- use the same Taiwan stock identity on both providers
- use the same normal trading date
- use daily market data
- use unadjusted Yahoo data
- preserve Yahoo fetch-path provenance
- use FinMind TaiwanStockPrice evidence
- exclude known corporate-action comparison cases
- exclude suspended-trading cases
- exclude missing-data special cases

Sample selection itself does not establish compatibility.

## 7. Precision and Unit Policy

Price precision compatibility is still PENDING.

Yahoo / FinMind volume compatibility is still PENDING.

FinMind Trading_Volume semantic evidence is locked as
TRADED_SHARE_COUNT, but cross-provider volume compatibility has not
been established.

No timestamp, price, or volume normalization is allowed by this
specification.

## 8. Fail-Closed Boundary

The following remain prohibited:

- live fetch capability added by this Gate
- normalization
- adapter output
- compatibility establishment
- provider switch
- V13 Core source switch
- Core input
- engine formula change
- scoring
- decision
- Supabase write
- production write

## 9. Compatibility Status

Even if a baseline sample produces matching OHLCV values:

COMPATIBILITY_RESULT remains NOT_ESTABLISHED.

The following compatibility evidence remains independently pending:

- adjustment compatibility
- volume-unit compatibility
- trading-date compatibility
- timezone compatibility
- corporate-action compatibility
- missing-data compatibility
- suspended-trading compatibility
- price-precision compatibility

## 10. Next Step

After this specification is reviewed and locked:

1. select the first baseline sample;
2. record the Evidence Matrix for that sample;
3. define comparison precision/tolerance behavior;
4. verify volume-unit evidence;
5. only then consider a minimal read-only baseline comparator.

No production or Core path may be enabled by this Gate.
