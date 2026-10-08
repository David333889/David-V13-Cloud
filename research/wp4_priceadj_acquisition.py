"""Isolated candidate. All real-acquisition prerequisites default closed."""
from datetime import datetime, timezone
from research.wp4_plan_request_budget import RequestBudget
from research.wp4_priceadj_intake import validate_priceadj_response, save_validated_priceadj, ENDPOINT

LIMIT = 2_000_000

def build_no_retry_session():
    """Session construction only; no network. Runtime entry still defaults blocked."""
    import requests
    from requests.adapters import HTTPAdapter
    session = requests.Session()
    session.trust_env = False
    session.mount('https://', HTTPAdapter(max_retries=0))
    session.mount('http://', HTTPAdapter(max_retries=0))
    return session

def acquire_once(*, budget_root, snapshot_root, plan_id, query, token=None,
                 session_factory=None, membership_confirmed=False,
                 calendar_confirmed=False, execution_authorized=False,
                 capture_mode='SYNTHETIC'):
    blocked = {'source_verified': False, 'production_eligible': False,
               'execution_readiness': 'BLOCKED'}
    # This candidate is fixed to the reviewed first sample; version labels cannot reset the budget.
    scope = dict(dataset='TaiwanStockPriceAdj', data_id='2330',
                 start_date='2026-10-07', end_date='2026-10-07')
    if query != scope or plan_id != 'PRICEADJ_2330_20261007_FIRST_OBSERVATION':
        return dict(blocked, allowed=False, reason='FIXED_PLAN_SCOPE_REQUIRED')
    if not all(x is True for x in (membership_confirmed,calendar_confirmed,execution_authorized)):
        return dict(blocked, allowed=False, reason='PREREQUISITES_NOT_CONFIRMED')
    if not isinstance(token,str) or not token.strip() or not callable(session_factory):
        return dict(blocked, allowed=False, reason='RUNTIME_DEPENDENCIES_REQUIRED')
    if capture_mode not in ('SYNTHETIC','LOCAL_OBSERVATION'):
        return dict(blocked, allowed=False, reason='CAPTURE_MODE_INVALID')
    try:
        budget = RequestBudget(budget_root,plan_id,scope)
    except (ValueError,OSError):
        return dict(blocked, allowed=False, reason='BUDGET_STORE_INVALID')
    saved = {}
    cleanup_warnings = []
    def action():
        session = session_factory()
        response = None
        try:
            started = datetime.now(timezone.utc).isoformat()
            response = session.get(ENDPOINT, params=dict(scope),
                                   headers={"Authorization": "Bearer " + token},
                                   timeout=(5,20),allow_redirects=False,stream=True)
            if type(response.status_code) is not int or response.status_code != 200:
                raise ValueError('HTTP_SUCCESS_REQUIRED')
            raw = bytearray()
            for chunk in response.iter_content(chunk_size=65536):
                if not isinstance(chunk,bytes):
                    raise ValueError('INVALID_RESPONSE_CHUNK')
                if len(raw)+len(chunk)>LIMIT:
                    raise ValueError('RESPONSE_SIZE_INVALID')
                raw.extend(chunk)
            completed = datetime.now(timezone.utc).isoformat()
            content = bytes(raw)
            validate_priceadj_response(content,scope,status_code=200,max_rows=1,max_bytes=LIMIT)
            saved.update(save_validated_priceadj(snapshot_root,content,scope,
                request_started_at=started,response_completed_at=completed,
                status_code=200,capture_mode=capture_mode))
        finally:
            try:
                if response is not None: response.close()
            except Exception:
                cleanup_warnings.append('RESPONSE_CLOSE_FAILED')
            try:
                session.close()
            except Exception:
                cleanup_warnings.append('SESSION_CLOSE_FAILED')
    result = budget.execute(action)
    # Missing returned snapshot receipt does not prove that no snapshot exists.
    outcome = ('SNAPSHOT_RECEIPT_RETURNED' if saved else
               'FAILED_OR_UNKNOWN' if result.get('reason') == 'ACTION_FAILED_BUDGET_CONSUMED'
               else 'NOT_STARTED')
    return dict(blocked, **result, observation=saved or None,
                acquisition_outcome=outcome,cleanup_warnings=cleanup_warnings)
