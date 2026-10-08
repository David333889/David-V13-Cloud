import json
from pathlib import Path
import shutil
from uuid import uuid4
import unittest
from datetime import datetime, timezone
from unittest.mock import patch

from research.wp4_local_snapshot_store import save_snapshot, select_snapshot, verify_snapshot


class LocalSnapshotTests(unittest.TestCase):
    def setUp(self):
        scratch = Path(__file__).resolve().parent.parent / '.test-work'
        scratch.mkdir(exist_ok=True)
        self.root = scratch / ('test-' + uuid4().hex)
        self.root.mkdir()
        self.addCleanup(shutil.rmtree, self.root)

    def save(self, **changes):
        args = dict(dataset='TaiwanStockPriceAdj', query={'data_id': 'SYNTHETIC'},
                    source_url='https://example.invalid/data',
                    request_started_at='2026-10-08T09:00:00+08:00',
                    response_completed_at='2026-10-08T09:01:00+08:00',
                    status_code=200, capture_mode='SYNTHETIC')
        args.update(changes)
        with patch('research.wp4_local_snapshot_store._utc_now',
                   return_value=datetime(2026, 10, 8, 1, 2, tzinfo=timezone.utc)):
            return save_snapshot(self.root, b'{"synthetic": true}', **args)

    def select(self, **changes):
        args = dict(dataset='TaiwanStockPriceAdj', query={'data_id': 'SYNTHETIC'},
                    decision_cutoff='2026-10-08T09:02:00+08:00', capture_mode='SYNTHETIC')
        args.update(changes)
        return select_snapshot(self.root, **args)

    def test_roundtrip_preserves_bytes_and_null_provider_fields(self):
        result = self.save()
        directory = self.root / result['local_snapshot_id']
        self.assertEqual((directory / 'raw.bin').read_bytes(), b'{"synthetic": true}')
        self.assertEqual(verify_snapshot(directory), result)
        for field in ('provider_revision_id', 'published_at', 'available_at', 'revision_timestamp'):
            self.assertIsNone(result[field])
        self.assertFalse(result['source_verified'])
        self.assertFalse(result['production_eligible'])

    def test_new_snapshot_never_changes_old_bytes(self):
        first = self.save()
        old = (self.root / first['local_snapshot_id'] / 'complete.json').read_bytes()
        second = self.save()
        self.assertNotEqual(first['local_snapshot_id'], second['local_snapshot_id'])
        self.assertEqual((self.root / first['local_snapshot_id'] / 'complete.json').read_bytes(), old)

    def test_collision_fails_without_overwrite(self):
        with patch('research.wp4_local_snapshot_store.uuid4') as uuid:
            uuid.return_value.hex = 'a' * 32
            first = self.save()
            with self.assertRaises(FileExistsError):
                self.save()
        self.assertEqual(verify_snapshot(self.root / first['local_snapshot_id']), first)

    def test_cutoff_includes_exact_saved_time_and_excludes_earlier_cutoff(self):
        self.save()
        self.assertIsNotNone(self.select()['selected'])
        self.assertIsNone(self.select(decision_cutoff='2026-10-08T09:01:59+08:00')['selected'])
        self.assertIsNotNone(self.select(decision_cutoff='2026-10-08T01:02:00Z')['selected'])

    def test_scope_and_synthetic_real_modes_do_not_mix(self):
        self.save()
        for change in ({'capture_mode': 'LOCAL_OBSERVATION'}, {'dataset': 'TaiwanStockPrice'},
                       {'query': {'data_id': 'DIFFERENT'}}):
            self.assertIsNone(self.select(**change)['selected'])

    def test_corruption_excluded_with_reason(self):
        result = self.save()
        (self.root / result['local_snapshot_id'] / 'raw.bin').write_bytes(b'changed')
        selected = self.select()
        self.assertIsNone(selected['selected'])
        self.assertEqual(selected['rejected'][0]['reason'], 'INTEGRITY_MISMATCH')

    def test_incomplete_and_invalid_json_excluded(self):
        (self.root / 'incomplete').mkdir()
        (self.root / 'incomplete' / 'raw.bin').write_bytes(b'partial')
        (self.root / 'incomplete' / 'complete.json').write_text('{')
        selected = self.select()
        self.assertIsNone(selected['selected'])
        self.assertEqual(len(selected['rejected']), 1)

    def test_invalid_times_rejected_before_write(self):
        for change in ({'response_completed_at': '2026-10-08T09:01:00'},
                       {'request_started_at': '2026-10-08T09:03:00+08:00'},
                       {'response_completed_at': '2026-10-08T09:04:00+08:00'}):
            with self.subTest(change=change), self.assertRaises(ValueError):
                self.save(**change)
        self.assertEqual(list(self.root.iterdir()), [])

    def test_secrets_in_keys_and_url_rejected_before_write(self):
        for change in ({'query': {'Authorization': 'sensitive'}},
                       {'query': {'nested': [{'api_token': 'sensitive'}]}},
                       {'source_url': 'https://example.invalid/data?token=sensitive'},
                       {'source_url': 'https://user:password@example.invalid/data'}):
            with self.subTest(change=change), self.assertRaises(ValueError):
                self.save(**change)
        self.assertEqual(list(self.root.iterdir()), [])

    def test_failed_http_and_invalid_query_rejected(self):
        for change in ({'status_code': 500}, {'status_code': True}, {'query': {'x': float('nan')}},
                       {'query': []}, {'capture_mode': 'UNKNOWN'}):
            with self.subTest(change=change), self.assertRaises(ValueError):
                self.save(**change)
        self.assertEqual(list(self.root.iterdir()), [])

    def test_metadata_cannot_promote_provider_verification(self):
        result = self.save()
        directory = self.root / result['local_snapshot_id']
        result['published_at'] = '2026-01-01T00:00:00Z'
        (directory / 'complete.json').write_text(json.dumps(result))
        self.assertIsNone(self.select()['selected'])

    def test_equal_time_selection_is_deterministic_and_blocked(self):
        first, second = self.save(), self.save()
        result = self.select()
        expected = max(first['local_snapshot_id'], second['local_snapshot_id'])
        self.assertEqual(result['selected']['local_snapshot_id'], expected)
        self.assertFalse(result['production_eligible'])
        self.assertEqual(result['execution_readiness'], 'BLOCKED')


if __name__ == '__main__':
    unittest.main()
