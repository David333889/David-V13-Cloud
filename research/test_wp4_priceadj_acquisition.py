import json
import os
from pathlib import Path
import shutil
import subprocess
import sys
from concurrent.futures import ThreadPoolExecutor
import unittest
from unittest.mock import patch
from uuid import uuid4

from research.wp4_plan_request_budget import RequestBudget
from research.wp4_priceadj_acquisition import acquire_once, build_no_retry_session, LIMIT
from research.wp4_priceadj_intake import save_validated_priceadj

QUERY = dict(dataset='TaiwanStockPriceAdj',data_id='2330',start_date='2026-10-07',end_date='2026-10-07')
PLAN = 'PRICEADJ_2330_20261007_FIRST_OBSERVATION'
RAW = json.dumps(dict(status=200,data=[dict(stock_id='2330',date='2026-10-07',open=10,max=12,min=9,close=11,
    Trading_Volume=100,Trading_money=1000,Trading_turnover=2,spread=1)])).encode()

class AcquisitionTests(unittest.TestCase):
    def setUp(self):
        self.repo=Path(__file__).resolve().parent.parent
        anchor=(self.repo/'.test-work').resolve()
        self.root=anchor/('acquisition-'+uuid4().hex)
        self.root.mkdir(parents=True)
        def cleanup():
            target=self.root.resolve()
            if target.parent!=anchor or not target.name.startswith('acquisition-'):
                raise ValueError('unsafe cleanup target')
            shutil.rmtree(target)
        self.addCleanup(cleanup)
        (self.root/'budget').mkdir();(self.root/'snapshots').mkdir()
        self.counts=dict(factory=0,get=0,read=0,close=0)

    def options(self,chunks=(RAW,),status=200,close_error=False):
        counts=self.counts
        class Response:
            status_code=status
            def iter_content(self,chunk_size):
                for chunk in chunks:
                    counts['read']+=1
                    yield chunk
            def close(self):
                counts['close']+=1
                if close_error:raise RuntimeError('synthetic secret')
        class Session:
            def get(self,*args,**kwargs):
                counts['get']+=1
                if kwargs.get('headers') != {'Authorization': 'Bearer SYNTHETIC_NOT_REAL'} or kwargs['params'] != QUERY:
                    raise AssertionError('credential must be header-only')
                if kwargs['allow_redirects'] is not False or kwargs['stream'] is not True:
                    raise AssertionError('unsafe request options')
                return Response()
            def close(self):
                counts['close']+=1
                if close_error:raise RuntimeError('synthetic secret')
        def factory():counts['factory']+=1;return Session()
        return dict(budget_root=self.root/'budget',snapshot_root=self.root/'snapshots',plan_id=PLAN,query=QUERY,
            token='SYNTHETIC_NOT_REAL',session_factory=factory,membership_confirmed=True,
            calendar_confirmed=True,execution_authorized=True,capture_mode='SYNTHETIC')

    def test_defaults_and_wrong_scope_fail_before_factory(self):
        opts=self.options();opts.pop('execution_authorized')
        self.assertEqual(acquire_once(**opts)['reason'],'PREREQUISITES_NOT_CONFIRMED')
        opts=self.options();opts['query']=dict(QUERY,data_id='OTHER')
        self.assertEqual(acquire_once(**opts)['reason'],'FIXED_PLAN_SCOPE_REQUIRED')
        self.assertEqual(self.counts['factory'],0)

    def test_exact_raw_saved_once_with_blocked_authority(self):
        opts=self.options(chunks=(RAW[:8],RAW[8:]))
        first=acquire_once(**opts);second=acquire_once(**opts)
        self.assertTrue(first['allowed']);self.assertEqual(second['reason'],'PLAN_BUDGET_USED')
        snap=first['observation']['snapshot']
        self.assertEqual((self.root/'snapshots'/snap['local_snapshot_id']/'raw.bin').read_bytes(),RAW)
        self.assertLessEqual(snap['request_started_at'],snap['response_completed_at'])
        self.assertLessEqual(snap['response_completed_at'],snap['saved_at'])
        self.assertFalse(first['production_eligible']);self.assertEqual(first['execution_readiness'],'BLOCKED')
        self.assertEqual(self.counts['get'],1)

    def test_oversize_stops_without_save_or_retry(self):
        opts=self.options(chunks=(b'x'*LIMIT,b'y',b'not-read'))
        self.assertFalse(acquire_once(**opts)['allowed'])
        self.assertEqual(acquire_once(**opts)['reason'],'PLAN_BUDGET_USED')
        self.assertEqual(self.counts['read'],2);self.assertEqual(self.counts['close'],2)
        self.assertEqual(list((self.root/'snapshots').iterdir()),[])

    def test_http_failure_does_not_read_body(self):
        opts=self.options(status=403)
        self.assertFalse(acquire_once(**opts)['allowed'])
        self.assertEqual(acquire_once(**opts)['reason'],'PLAN_BUDGET_USED')
        self.assertEqual(self.counts['get'],1);self.assertEqual(self.counts['read'],0)

    def test_cleanup_failure_preserves_saved_receipt(self):
        result=acquire_once(**self.options(close_error=True))
        self.assertTrue(result['allowed'])
        self.assertEqual(result['cleanup_warnings'],['RESPONSE_CLOSE_FAILED','SESSION_CLOSE_FAILED'])
        self.assertNotIn('synthetic secret',json.dumps(result))

    def test_save_then_exception_is_unknown_and_budget_consumed(self):
        def save_then_fail(*args,**kwargs):
            save_validated_priceadj(*args,**kwargs)
            raise RuntimeError('synthetic interruption')
        opts=self.options()
        with patch('research.wp4_priceadj_acquisition.save_validated_priceadj',side_effect=save_then_fail):
            result=acquire_once(**opts)
        self.assertEqual(result['acquisition_outcome'],'FAILED_OR_UNKNOWN')
        self.assertIsNone(result['observation'])
        self.assertEqual(len(list((self.root/'snapshots').iterdir())),1)
        self.assertEqual(acquire_once(**opts)['reason'],'PLAN_BUDGET_USED')

    def test_budget_survives_process_and_parallel_calls(self):
        budget=self.root/'budget'
        first=RequestBudget(budget,'restart',QUERY).execute(lambda:None)
        self.assertTrue(first['allowed'])
        code="from research.wp4_plan_request_budget import RequestBudget;import sys;print(RequestBudget(sys.argv[1],'restart',{}).execute(lambda:None)['reason'])"
        result=subprocess.run([sys.executable,'-c',code,str(budget)],cwd=self.repo,capture_output=True,text=True,check=True)
        self.assertEqual(result.stdout.strip(),'PLAN_BUDGET_USED')
        with ThreadPoolExecutor(max_workers=12) as pool:
            values=list(pool.map(lambda _:RequestBudget(budget,'parallel',QUERY).execute(lambda:None),range(24)))
        self.assertEqual(sum(x['allowed'] for x in values),1)

    def test_budget_sync_failure_never_calls_action(self):
        calls=[]
        with patch('research.wp4_plan_request_budget.os.fsync',side_effect=OSError('synthetic')):
            result=RequestBudget(self.root/'budget','sync',QUERY).execute(lambda:calls.append(1))
        self.assertEqual(result['reason'],'BUDGET_RECORD_FAILED');self.assertEqual(calls,[])
        self.assertEqual(RequestBudget(self.root/'budget','sync',QUERY).execute(lambda:None)['reason'],'PLAN_BUDGET_USED')

    def test_standard_transport_redirect_is_not_followed(self):
        import requests
        from requests.adapters import HTTPAdapter
        session=build_no_retry_session()
        self.assertFalse(session.trust_env)
        self.assertEqual(session.get_adapter('https://example.test').max_retries.total,0)
        session.close()
        sent=[]
        def send(adapter,request,**kwargs):
            sent.append(dict(kwargs, auth_header_matches=request.headers.get('Authorization') == 'Bearer SYNTHETIC_NOT_REAL', token_in_url='token=' in request.url or 'SYNTHETIC_NOT_REAL' in request.url))
            response=requests.Response();response.status_code=302;response.request=request;response.url=request.url
            response._content=b'';response._content_consumed=True
            response.headers['Location']='https://example.test/forbidden'
            return response
        opts=self.options();opts['session_factory']=build_no_retry_session
        with patch.object(HTTPAdapter,'send',new=send):
            self.assertFalse(acquire_once(**opts)['allowed'])
            self.assertEqual(acquire_once(**opts)['reason'],'PLAN_BUDGET_USED')
        self.assertEqual(len(sent),1);self.assertTrue(sent[0]['verify']);self.assertEqual(sent[0]['proxies'],{})
        self.assertTrue(sent[0]['auth_header_matches']);self.assertFalse(sent[0]['token_in_url'])

if __name__=='__main__':unittest.main()
