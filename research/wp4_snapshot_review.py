"""Offline file import and snapshot review CLI. Never fetches market data."""
import argparse
import hashlib
import json
from pathlib import Path

from research.wp4_local_snapshot_store import select_snapshot
from research.wp4_priceadj_intake import DATASET, save_validated_priceadj, validate_priceadj_response


def review_selected_priceadj(root, query, *, decision_cutoff, capture_mode):
    selection = select_snapshot(root, dataset=DATASET, query=query,
                                decision_cutoff=decision_cutoff, capture_mode=capture_mode)
    result = {'research_only': True, 'source_verified': False, 'production_eligible': False,
              'execution_readiness': 'BLOCKED', 'selected_snapshot_id': None,
              'assessment': None, 'review_required': True,
              'rejected_snapshots': selection['rejected'], 'issues': []}
    selected = selection['selected']
    if selected is None:
        result['issues'].append('NO_ELIGIBLE_LOCAL_SNAPSHOT')
        return result
    directory = Path(root) / selected['local_snapshot_id']
    try:
        raw = (directory / 'raw.bin').read_bytes()
        if len(raw) != selected['raw_bytes'] or hashlib.sha256(raw).hexdigest() != selected['sha256']:
            raise ValueError('INTEGRITY_CHANGED_DURING_REVIEW')
        assessment = validate_priceadj_response(raw, query, status_code=selected['status_code'])
    except (OSError, ValueError) as exc:
        result['issues'].append(str(exc))
        return result
    result['selected_snapshot_id'] = selected['local_snapshot_id']
    result['assessment'] = assessment
    result['review_required'] = bool(assessment['warnings'])
    # Review-required concerns content warnings only; authority stays BLOCKED.
    return result


def main(argv=None):
    parser = argparse.ArgumentParser(description='Offline PriceAdj import/review; no provider authentication.')
    parser.add_argument('operation', choices=('import', 'review'))
    parser.add_argument('--store', required=True)
    parser.add_argument('--query-file', required=True)
    parser.add_argument('--mode', choices=('SYNTHETIC', 'LOCAL_OBSERVATION'), default='SYNTHETIC')
    parser.add_argument('--raw-file')
    parser.add_argument('--http-status', type=int)
    parser.add_argument('--request-started-at')
    parser.add_argument('--response-completed-at')
    parser.add_argument('--decision-cutoff')
    args = parser.parse_args(argv)
    try:
        query = json.loads(Path(args.query_file).read_text(encoding='utf-8-sig'))
        if args.operation == 'import':
            if not all((args.raw_file, args.request_started_at, args.response_completed_at)) or args.http_status is None:
                parser.error('import requires raw file, actual HTTP status and aware request/completion times')
            raw = Path(args.raw_file).read_bytes()
            result = save_validated_priceadj(
                args.store, raw, query, request_started_at=args.request_started_at,
                response_completed_at=args.response_completed_at, status_code=args.http_status, capture_mode=args.mode,
            )
        else:
            if not args.decision_cutoff:
                parser.error('review requires an aware decision cutoff')
            result = review_selected_priceadj(args.store, query, decision_cutoff=args.decision_cutoff,
                                              capture_mode=args.mode)
        print(json.dumps(result, ensure_ascii=False, indent=2))
        return 0 if not result.get('issues') else 1
    except (OSError, ValueError) as exc:
        # Do not echo raw response or credential-bearing request values.
        print(json.dumps({'error': type(exc).__name__, 'execution_readiness': 'BLOCKED'}))
        return 1


if __name__ == '__main__':
    raise SystemExit(main())
