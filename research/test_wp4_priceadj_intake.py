import copy
from datetime import datetime, timezone
import json
from pathlib import Path
import shutil
import unittest
from uuid import uuid4

from research.wp4_priceadj_intake import validate_priceadj_response, save_validated_priceadj


def query():
    return dict(dataset='TaiwanStockPriceAdj', data_id='SYNTHETIC', start_date='2026-10-01', end_date='2026-10-02')


def payload():
    return {'status': 200, 'msg': 'success', 'data': [dict(
        stock_id='SYNTHETIC', date='2026-10-01', open=10, max=12, min=9, close=11,
        Trading_Volume=100, Trading_money=1000, Trading_turnover=2, spread=-1)]}


def encode(value):
    return json.dumps(value).encode()


class PriceAdjIntakeTests(unittest.TestCase):
    def test_valid_bounded_response_keeps_all_authority_blocked(self):
        value = payload()
        before = copy.deepcopy(value)
        result = validate_priceadj_response(encode(value), query(), status_code=200)
        self.assertTrue(result['schema_and_scope_valid'])
        self.assertFalse(result['calendar_completeness_verified'])
        self.assertFalse(result['source_verified'])
        self.assertFalse(result['production_eligible'])
        self.assertEqual(value, before)

    def test_bad_envelopes_and_http_are_rejected(self):
        for value in ({'status': 400, 'data': payload()['data']}, {'data': []},
                      {'status': True, 'data': []}, {'status': 200, 'data': []}, []):
            with self.subTest(value=value), self.assertRaises(ValueError):
                validate_priceadj_response(encode(value), query(), status_code=200)
        with self.assertRaises(ValueError):
            validate_priceadj_response(encode(payload()), query(), status_code=401)

    def test_exact_scope_and_duplicates_required(self):
        for change in ({'stock_id': 'OTHER'}, {'date': '2026-10-03'}, {'date': '20261001'}):
            value = payload()
            value['data'][0].update(change)
            with self.subTest(change=change), self.assertRaises(ValueError):
                validate_priceadj_response(encode(value), query(), status_code=200)
        value = payload()
        value['data'].append(copy.deepcopy(value['data'][0]))
        with self.assertRaises(ValueError):
            validate_priceadj_response(encode(value), query(), status_code=200)

    def test_missing_bad_numeric_and_negative_prices_rejected(self):
        for field, bad in (('close', None), ('close', True), ('close', '11'), ('close', -1),
                           ('max', float('inf')), ('spread', float('nan')),
                           ('close', 10 ** 400), ('Trading_Volume', 1.5)):
            value = payload()
            value['data'][0][field] = bad
            with self.subTest(field=field, bad=bad), self.assertRaises(ValueError):
                validate_priceadj_response(encode(value), query(), status_code=200)
        value = payload()
        del value['data'][0]['close']
        with self.assertRaises(ValueError):
            validate_priceadj_response(encode(value), query(), status_code=200)

    def test_emerging_open_is_not_forced_inside_high_low(self):
        for opening in (0, 30):
            value = payload()
            value['data'][0]['open'] = opening
            result = validate_priceadj_response(encode(value), query(), status_code=200)
            self.assertTrue(result['schema_and_scope_valid'])
            self.assertEqual(bool(result['warnings']), opening == 0)

    def test_query_limits_and_duplicate_json_keys_rejected(self):
        for change in ({'api_token': 'secret'}, {'end_date': '2026-09-01'}, {'dataset': 'TaiwanStockPrice'}):
            q = query()
            q.update(change)
            with self.subTest(change=change), self.assertRaises(ValueError):
                validate_priceadj_response(encode(payload()), q, status_code=200)
        for args in ({'max_rows': 0}, {'max_bytes': 1}):
            with self.assertRaises(ValueError):
                validate_priceadj_response(encode(payload()), query(), status_code=200, **args)
        with self.assertRaises(ValueError):
            validate_priceadj_response(b'{"status":200,"status":400,"data":[]}', query(), status_code=200)

    def test_validated_save_keeps_exact_bytes_and_rejected_response_unwritten(self):
        root = Path(__file__).resolve().parent.parent / '.test-work' / ('intake-' + uuid4().hex)
        root.mkdir(parents=True)
        self.addCleanup(shutil.rmtree, root)
        now = datetime.now(timezone.utc).isoformat()
        options = dict(request_started_at=now, response_completed_at=now,
                       status_code=200, capture_mode='SYNTHETIC')
        with self.assertRaises(ValueError):
            save_validated_priceadj(root, b'{"status":400,"data":[]}', query(), **options)
        self.assertEqual(list(root.iterdir()), [])
        raw = encode(payload())
        result = save_validated_priceadj(root, raw, query(), **options)
        self.assertEqual((root / result['snapshot']['local_snapshot_id'] / 'raw.bin').read_bytes(), raw)
        self.assertFalse(result['snapshot']['source_verified'])


if __name__ == '__main__':
    unittest.main()
