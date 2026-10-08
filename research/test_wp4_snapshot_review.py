from contextlib import redirect_stdout
from datetime import datetime, timezone
import io
import json
from pathlib import Path
import shutil
import unittest
from uuid import uuid4

from research.test_wp4_priceadj_intake import payload, query, encode
from research.wp4_priceadj_intake import save_validated_priceadj
from research.wp4_snapshot_review import main, review_selected_priceadj


class SnapshotReviewTests(unittest.TestCase):
    def setUp(self):
        self.root = Path(__file__).resolve().parent.parent / '.test-work' / ('review-' + uuid4().hex)
        self.root.mkdir(parents=True)
        self.addCleanup(shutil.rmtree, self.root)
        self.store = self.root / 'store'
        self.now = datetime.now(timezone.utc).isoformat()

    def save(self, value=None):
        return save_validated_priceadj(self.store, encode(value or payload()), query(),
            request_started_at=self.now, response_completed_at=self.now, status_code=200,
            capture_mode='SYNTHETIC')

    def review(self, **change):
        args = dict(decision_cutoff=datetime.now(timezone.utc).isoformat(), capture_mode='SYNTHETIC')
        args.update(change)
        return review_selected_priceadj(self.store, query(), **args)

    def test_successful_selection_is_revalidated_and_never_authorizes(self):
        saved = self.save()
        result = self.review()
        self.assertEqual(result['selected_snapshot_id'], saved['snapshot']['local_snapshot_id'])
        self.assertTrue(result['assessment']['schema_and_scope_valid'])
        self.assertFalse(result['production_eligible'])
        self.assertEqual(result['execution_readiness'], 'BLOCKED')

    def test_empty_and_cross_mode_store_never_yield_selected_data(self):
        self.assertIn('NO_ELIGIBLE_LOCAL_SNAPSHOT', self.review()['issues'])
        self.save()
        self.assertIn('NO_ELIGIBLE_LOCAL_SNAPSHOT', self.review(capture_mode='LOCAL_OBSERVATION')['issues'])

    def test_zero_price_still_requires_review(self):
        value = payload()
        value['data'][0]['open'] = 0
        self.save(value)
        self.assertTrue(self.review()['review_required'])

    def test_cli_import_and_review_preserve_raw_and_default_to_synthetic(self):
        raw_file, query_file = self.root / 'raw.json', self.root / 'query.json'
        raw_file.write_bytes(encode(payload()))
        query_file.write_text(json.dumps(query()))
        common = ['--store', str(self.store), '--query-file', str(query_file)]
        with redirect_stdout(io.StringIO()) as output:
            code = main(['import', *common, '--raw-file', str(raw_file),
                         '--request-started-at', self.now, '--response-completed-at', self.now, '--http-status', '200'])
        self.assertEqual(code, 0)
        saved = json.loads(output.getvalue())
        self.assertEqual(saved['snapshot']['capture_mode'], 'SYNTHETIC')
        with redirect_stdout(io.StringIO()) as output:
            code = main(['review', *common, '--decision-cutoff', datetime.now(timezone.utc).isoformat()])
        self.assertEqual(code, 0)
        self.assertFalse(json.loads(output.getvalue())['production_eligible'])


if __name__ == '__main__':
    unittest.main()
