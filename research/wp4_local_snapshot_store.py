"""Offline local observation storage; no network or provider authentication.

Caller-supplied request times describe local observation only. Hashes detect
corruption, not malicious rewriting or trusted historical publication times.
"""
from datetime import datetime, timezone
import hashlib
import json
from pathlib import Path
import re
from urllib.parse import urlsplit
from uuid import uuid4

SCHEMA = 'WP4_LOCAL_OBSERVATION_V1'
MODES = ('SYNTHETIC', 'LOCAL_OBSERVATION')
FORBIDDEN = re.compile(r'token|secret|password|credential|authorization|api.?key|cookie', re.I)


def _utc_now():
    return datetime.now(timezone.utc)


def _time(value):
    if not isinstance(value, str):
        raise ValueError('AWARE_TIMESTAMP_REQUIRED')
    try:
        parsed = datetime.fromisoformat(value.replace('Z', '+00:00'))
    except ValueError as exc:
        raise ValueError('AWARE_TIMESTAMP_REQUIRED') from exc
    if parsed.tzinfo is None or parsed.utcoffset() is None:
        raise ValueError('AWARE_TIMESTAMP_REQUIRED')
    return parsed.astimezone(timezone.utc)


def _safe_query(value):
    if not isinstance(value, dict):
        raise ValueError('QUERY_OBJECT_REQUIRED')
    def check(item):
        if isinstance(item, dict):
            for key, child in item.items():
                if not isinstance(key, str) or FORBIDDEN.search(key):
                    raise ValueError('SECRET_OR_INVALID_QUERY_KEY')
                check(child)
        elif isinstance(item, list):
            for child in item:
                check(child)
        elif item is not None and type(item) not in (str, int, float, bool):
            raise ValueError('QUERY_JSON_REQUIRED')
    check(value)
    return json.loads(json.dumps(value, allow_nan=False))


def _source(value):
    if not isinstance(value, str):
        raise ValueError('SAFE_SOURCE_URL_REQUIRED')
    url = urlsplit(value)
    if (url.scheme != 'https' or not url.hostname or url.username or
            url.password or url.query or url.fragment):
        raise ValueError('SAFE_SOURCE_URL_REQUIRED')
    return value


def save_snapshot(root, raw, *, dataset, query, source_url,
                  request_started_at, response_completed_at, status_code,
                  capture_mode):
    """Save complete pre-acquired bytes; failure leaves an unusable directory.

    This does not interpret a provider payload's success flag or certify the
    contents. Caller must not pass credentials in raw bytes or query values.
    """
    if not isinstance(raw, bytes) or not raw:
        raise ValueError('NONEMPTY_BYTES_REQUIRED')
    if not isinstance(dataset, str) or not dataset.strip():
        raise ValueError('DATASET_REQUIRED')
    if capture_mode not in MODES:
        raise ValueError('CAPTURE_MODE_REQUIRED')
    if type(status_code) is not int or status_code != 200:
        raise ValueError('HTTP_SUCCESS_REQUIRED')
    query = _safe_query(query)
    source_url = _source(source_url)
    started, completed = _time(request_started_at), _time(response_completed_at)
    if not started <= completed <= _utc_now():
        raise ValueError('LOCAL_TIME_ORDER_INVALID')
    store = Path(root)
    store.mkdir(parents=True, exist_ok=True)
    snapshot_id = 'local-' + uuid4().hex
    directory = store / snapshot_id
    directory.mkdir()  # Collision is an error, never an overwrite.
    raw_path = directory / 'raw.bin'
    with raw_path.open('xb') as stream:
        stream.write(raw)
        stream.flush()
        import os
        os.fsync(stream.fileno())
    digest = hashlib.sha256(raw).hexdigest()
    if hashlib.sha256(raw_path.read_bytes()).hexdigest() != digest:
        raise ValueError('WRITE_INTEGRITY_FAILED')
    saved = _utc_now()
    if saved < completed:
        raise ValueError('LOCAL_TIME_ORDER_INVALID')
    metadata = {
        'schema_version': SCHEMA, 'local_snapshot_id': snapshot_id,
        'dataset': dataset, 'query_parameters_without_secrets': query,
        'source_url_without_secrets': source_url,
        'request_started_at': started.isoformat(),
        'response_completed_at': completed.isoformat(),
        'saved_at': saved.isoformat(), 'status_code': status_code,
        'capture_mode': capture_mode, 'raw_file': 'raw.bin',
        'raw_bytes': len(raw), 'sha256': digest,
        'provider_revision_id': None, 'published_at': None,
        'available_at': None, 'revision_timestamp': None,
        'source_verified': False, 'production_eligible': False,
        'execution_readiness': 'BLOCKED',
        'limitations': ['LOCAL_OBSERVATION_ONLY', 'LOCAL_CLOCK_NOT_AUTHENTICATED',
                        'PROVIDER_PAYLOAD_NOT_VALIDATED', 'NO_PRE_CAPTURE_HISTORY'],
    }
    # Partial JSON on interrupted write is rejected by verify_snapshot.
    with (directory / 'complete.json').open('x', encoding='utf-8') as stream:
        json.dump(metadata, stream, ensure_ascii=False, indent=2, allow_nan=False)
        stream.flush()
        os.fsync(stream.fileno())
    return verify_snapshot(directory)


def verify_snapshot(directory):
    """Verify local integrity and scope, never provider authenticity."""
    directory = Path(directory)
    if directory.is_symlink():
        raise ValueError('SYMLINK_REJECTED')
    for name in ('raw.bin', 'complete.json'):
        if (directory / name).is_symlink():
            raise ValueError('SYMLINK_REJECTED')
    try:
        metadata = json.loads((directory / 'complete.json').read_text(encoding='utf-8'))
        raw = (directory / 'raw.bin').read_bytes()
    except (OSError, ValueError) as exc:
        raise ValueError('INCOMPLETE_OR_INVALID_SNAPSHOT') from exc
    if not isinstance(metadata, dict):
        raise ValueError('INVALID_METADATA')
    if (metadata.get('schema_version') != SCHEMA or
            metadata.get('local_snapshot_id') != directory.name or
            metadata.get('raw_file') != 'raw.bin' or
            metadata.get('capture_mode') not in MODES or
            type(metadata.get('status_code')) is not int or metadata['status_code'] != 200 or
            not isinstance(metadata.get('dataset'), str) or not metadata['dataset'].strip()):
        raise ValueError('INVALID_METADATA')
    if (not raw or type(metadata.get('raw_bytes')) is not int or
            len(raw) != metadata['raw_bytes'] or
            hashlib.sha256(raw).hexdigest() != metadata.get('sha256')):
        raise ValueError('INTEGRITY_MISMATCH')
    _safe_query(metadata.get('query_parameters_without_secrets'))
    _source(metadata.get('source_url_without_secrets'))
    started = _time(metadata.get('request_started_at'))
    completed = _time(metadata.get('response_completed_at'))
    saved = _time(metadata.get('saved_at'))
    if not started <= completed <= saved:
        raise ValueError('LOCAL_TIME_ORDER_INVALID')
    if (any(metadata.get(field, 'MISSING') is not None for field in
            ('provider_revision_id', 'published_at', 'available_at', 'revision_timestamp')) or
            metadata.get('source_verified') is not False or
            metadata.get('production_eligible') is not False or
            metadata.get('execution_readiness') != 'BLOCKED'):
        raise ValueError('LOCAL_SNAPSHOT_CANNOT_CLAIM_PROVIDER_VERIFICATION')
    return metadata


def select_snapshot(root, *, dataset, query, decision_cutoff, capture_mode):
    """Select exact query/mode match completed and saved by cutoff (inclusive).

    Equal saved times use snapshot ID as a deterministic tie breaker, not a
    claim about provider revision order. Invalid snapshots are never selected.
    """
    if capture_mode not in MODES:
        raise ValueError('CAPTURE_MODE_REQUIRED')
    cutoff = _time(decision_cutoff)
    query = _safe_query(query)
    matches, rejected = [], []
    store = Path(root)
    for directory in sorted(store.iterdir()) if store.exists() else ():
        if not directory.is_dir():
            continue
        try:
            metadata = verify_snapshot(directory)
        except ValueError as exc:
            rejected.append({'snapshot_directory': directory.name, 'reason': str(exc)})
            continue
        if (metadata['dataset'] == dataset and metadata['query_parameters_without_secrets'] == query
                and metadata['capture_mode'] == capture_mode
                and _time(metadata['response_completed_at']) <= cutoff
                and _time(metadata['saved_at']) <= cutoff):
            matches.append(metadata)
    selected = max(matches, key=lambda m: (_time(m['saved_at']), m['local_snapshot_id'])) if matches else None
    return {'selected': selected, 'rejected': rejected, 'source_verified': False,
            'production_eligible': False, 'execution_readiness': 'BLOCKED'}
