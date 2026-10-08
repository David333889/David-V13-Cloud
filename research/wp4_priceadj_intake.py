"""Bounded offline content intake, not provider/formula/PIT authentication."""
from datetime import date
import json
import math

from research.wp4_local_snapshot_store import save_snapshot, _safe_query

DATASET = 'TaiwanStockPriceAdj'
ENDPOINT = 'https://api.finmindtrade.com/api/v4/data'
FIELDS = ('open', 'max', 'min', 'close', 'Trading_Volume', 'Trading_money', 'Trading_turnover', 'spread')


def _date(value):
    if not isinstance(value, str):
        raise ValueError('ISO_DATE_REQUIRED')
    parsed = date.fromisoformat(value)
    if parsed.isoformat() != value:
        raise ValueError('ISO_DATE_REQUIRED')
    return parsed


def _pairs(pairs):
    result = {}
    for key, value in pairs:
        if key in result:
            raise ValueError('DUPLICATE_JSON_KEY')
        result[key] = value
    return result


def validate_priceadj_response(raw, query, *, status_code, max_rows=1000, max_bytes=2_000_000):
    """Validate exact single-security scope. Empty data and unknown shapes fail.

    Numeric/schema checks do not establish calendar completeness or economics.
    Zero prices require independent review; open is not forced into the daily
    high/low interval because emerging-market open may mean prior-day average.
    """
    query = _safe_query(query)
    if set(query) != {'dataset', 'data_id', 'start_date', 'end_date'} or query['dataset'] != DATASET:
        raise ValueError('BOUNDED_PRICEADJ_QUERY_REQUIRED')
    stock = query['data_id']
    if not isinstance(stock, str) or not stock.strip():
        raise ValueError('SECURITY_ID_REQUIRED')
    start, end = _date(query['start_date']), _date(query['end_date'])
    if start > end:
        raise ValueError('DATE_RANGE_INVALID')
    if type(max_rows) is not int or max_rows <= 0 or type(max_bytes) is not int or max_bytes <= 0:
        raise ValueError('POSITIVE_LIMIT_REQUIRED')
    if type(status_code) is not int or status_code != 200:
        raise ValueError('HTTP_SUCCESS_REQUIRED')
    if not isinstance(raw, bytes) or not raw or len(raw) > max_bytes:
        raise ValueError('RESPONSE_SIZE_INVALID')
    def reject_constant(value):
        raise ValueError('NONFINITE_JSON_NUMBER')
    try:
        payload = json.loads(raw.decode('utf-8-sig'), object_pairs_hook=_pairs, parse_constant=reject_constant)
    except (UnicodeError, ValueError, RecursionError) as exc:
        raise ValueError('INVALID_JSON_RESPONSE') from exc
    if not isinstance(payload, dict) or type(payload.get('status')) is not int or payload['status'] != 200:
        raise ValueError('PROVIDER_SUCCESS_REQUIRED')
    rows = payload.get('data')
    if not isinstance(rows, list) or not rows or len(rows) > max_rows:
        raise ValueError('BOUNDED_NONEMPTY_ROWS_REQUIRED')
    seen, warnings = set(), []
    for index, row in enumerate(rows):
        if not isinstance(row, dict) or row.get('stock_id') != stock:
            raise ValueError('SECURITY_SCOPE_MISMATCH')
        day = _date(row.get('date'))
        if not start <= day <= end:
            raise ValueError('DATE_SCOPE_MISMATCH')
        key = (stock, day)
        if key in seen:
            raise ValueError('DUPLICATE_OBSERVATION')
        seen.add(key)
        for field in FIELDS:
            value = row.get(field)
            try:
                finite = type(value) in (int, float) and math.isfinite(value)
            except OverflowError:
                finite = False
            if not finite:
                raise ValueError('FINITE_NUMERIC_FIELD_REQUIRED:' + field)
            if field != 'spread' and value < 0:
                raise ValueError('NEGATIVE_FIELD:' + field)
        for field in ('Trading_Volume', 'Trading_turnover'):
            if row[field] != int(row[field]):
                raise ValueError('INTEGER_COUNT_REQUIRED:' + field)
        if row['min'] > row['max']:
            raise ValueError('HIGH_LOW_ORDER_INVALID')
        if any(row[field] == 0 for field in ('open', 'max', 'min', 'close')):
            warnings.append({'row': index, 'code': 'ZERO_PRICE_REQUIRES_REVIEW'})
    return {'schema_and_scope_valid': True, 'row_count': len(rows), 'warnings': warnings,
            'calendar_completeness_verified': False, 'formula_verified': False,
            'source_verified': False, 'production_eligible': False, 'execution_readiness': 'BLOCKED'}


def save_validated_priceadj(root, raw, query, *, request_started_at, response_completed_at,
                           status_code, capture_mode):
    """Validate before writing; preserve raw bytes without normalizing values."""
    assessment = validate_priceadj_response(raw, query, status_code=status_code)
    snapshot = save_snapshot(
        root, raw, dataset=DATASET, query=query, source_url=ENDPOINT,
        request_started_at=request_started_at, response_completed_at=response_completed_at,
        status_code=status_code, capture_mode=capture_mode,
    )
    return {'snapshot': snapshot, 'assessment': assessment}
