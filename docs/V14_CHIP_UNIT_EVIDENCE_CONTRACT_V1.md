# DAVID V14 UNIFIED ENGINE — CHIP UNIT EVIDENCE CONTRACT V1

> Gate 26 — Chip Unit Evidence Contract V1
>
> Parent: Gate 23 — Chip Source Mapping & Unit Contract V1
>
> Protected Input Baseline: 7925d6cd9f25e5d5d2a747ea20d510f61d4a060d
>
> Production Write: NOT AUTHORIZED

---

# 1. Purpose

Gate 26 defines the evidence boundary for Chip raw-field units.

This Gate does not guess or invent source units.

UNKNOWN UNIT != ASSUMED UNIT

NO VERIFIED EVIDENCE = NO UNIT LOCK

---

# 2. Evidence Policy

A unit may become VERIFIED / LOCKED only when sufficient source evidence exists.

Acceptable evidence must identify:

- source
- dataset
- raw field
- field meaning
- unit
- verification status

Existing code usage is not unit evidence.

Existing synthetic Golden Fixture values are not unit evidence.

Field names alone are not unit evidence.

---

# 3. Unit Evidence Matrix

| Domain | Dataset | Field | Evidence Status | Unit Status |
|---|---|---|---|---|
| Institutional | TaiwanStockInstitutionalInvestorsBuySell | buy / sell | INSUFFICIENT | UNIT_PENDING |
| Margin | TaiwanStockMarginPurchaseShortSale | MarginPurchase* | INSUFFICIENT | UNIT_PENDING |
| Short | TaiwanStockMarginPurchaseShortSale | ShortSale* | INSUFFICIENT | UNIT_PENDING |
| Offset | TaiwanStockMarginPurchaseShortSale | OffsetLoanAndShort | INSUFFICIENT | UNIT_PENDING |
| Securities Lending | TaiwanStockSecuritiesLending | volume | INSUFFICIENT | UNIT_PENDING |
| Day Trading | TaiwanStockDayTrading | Volume / BuyAmount / SellAmount | PARTIAL | PARTIAL_UNIT_LOCK |

---

# 4. Fail-Closed Rules

UNKNOWN UNIT != ASSUMED UNIT

UNIT_PENDING != ZERO

UNIT_PENDING != VERIFIED

UNIT_PENDING != LOCKED

No automatic multiply by 1000.

No automatic divide by 1000.

No automatic conversion between shares / lots / thousand-shares.

No automatic amount conversion.

---

# 5. Golden Fixture Boundary

Synthetic fixture values are test evidence only.

Examples such as:

- 1000
- 5000
- 1000000

must not be interpreted as proof of shares, lots, thousand-shares, TWD, or other source units.

Golden Fixture != Source Unit Evidence

---

# 6. Adapter Boundary

Chip Source Adapter V1 must preserve raw values while unit evidence remains pending.

The Adapter must not:

- infer unit from magnitude
- infer unit from field name
- apply undocumented conversion
- emit derived Chip Score
- emit Decision
- emit Risk
- emit Action

---

# 7. Upgrade Rule

UNIT_PENDING may be upgraded only by a future verified evidence Gate.

Required upgrade evidence:

1. source identified
2. dataset identified
3. raw field identified
4. field meaning verified
5. unit explicitly verified
6. compatibility impact reviewed
7. regression fixture added

Without all required evidence:

KEEP UNIT_PENDING

---

# 8. Gate 26 Boundary

No FinMind Live API integration.

No Supabase write.

No Production Write.

No Chip Score.

No Risk V2.

No Action V2.

PRODUCTION_WRITE = NOT_AUTHORIZED

---

# 9. Conclusion

Gate 26 formally locks the Unit Evidence governance boundary.

Current unresolved units remain UNIT_PENDING or PARTIAL_UNIT_LOCK.

This is an intentional fail-closed state, not an implementation failure.
