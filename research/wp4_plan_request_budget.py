"""Offline candidate: consume a local plan budget before invoking an action.

Only cooperating callers sharing this trusted local store are covered.
No provider access, credential handling, deletion or reset facility.
"""
import hashlib
import json
import os
from pathlib import Path
from datetime import datetime, timezone

class RequestBudget:
    def __init__(self, root, plan_id, query):
        if not isinstance(plan_id, str) or not plan_id.strip():
            raise ValueError('PLAN_ID_REQUIRED')
        self.root = Path(root)
        if not self.root.is_dir() or self.root.is_symlink():
            raise ValueError('TRUSTED_EXISTING_STORE_REQUIRED')
        self.plan_id = plan_id
        # Plan id owns the budget. Changing the query cannot reset it.
        self.path = self.root / (hashlib.sha256(plan_id.encode()).hexdigest() + '.used')
        self.query_hash = hashlib.sha256(json.dumps(query, sort_keys=True, separators=(',', ':'), allow_nan=False).encode()).hexdigest()

    def execute(self, action):
        if not callable(action):
            return {'allowed': False, 'reason': 'ACTION_REQUIRED'}
        try:
            fd = os.open(self.path, os.O_WRONLY | os.O_CREAT | os.O_EXCL, 0o600)
        except FileExistsError:
            return {'allowed': False, 'reason': 'PLAN_BUDGET_USED'}
        except OSError:
            return {'allowed': False, 'reason': 'BUDGET_RESERVATION_FAILED'}
        try:
            with os.fdopen(fd, 'wb') as handle:
                handle.write(json.dumps({'plan_id': self.plan_id, 'query_hash': self.query_hash,
                    'state': 'USED_BEFORE_ACTION', 'reserved_at': datetime.now(timezone.utc).isoformat()}).encode())
                handle.flush()
                os.fsync(handle.fileno())
        except OSError:
            # Leave even an incomplete marker consumed. Never remove or retry.
            return {'allowed': False, 'reason': 'BUDGET_RECORD_FAILED'}
        try:
            action()
        except Exception:
            return {'allowed': False, 'reason': 'ACTION_FAILED_BUDGET_CONSUMED'}
        return {'allowed': True, 'budget_consumed': True}
