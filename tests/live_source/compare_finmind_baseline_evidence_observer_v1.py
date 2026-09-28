# Gate 28D.2K-2B - FinMind Baseline Evidence Observer V1.
#
# Read-only observer test.
# No live fetch, normalization, compatibility establishment,
# provider switching, Core input, scoring, decision,
# or persistence.

import importlib


def main():
    print(
        "=== GATE 28D.2K-2B - FINMIND BASELINE "
        "EVIDENCE OBSERVER V1 ==="
    )

    try:
        module = importlib.import_module(
            "v14.finmind_baseline_evidence_observer"
        )
    except ModuleNotFoundError:
        print(
            "[EXPECTED RED] FinMind baseline evidence "
            "observer module not found"
        )
        raise SystemExit(1)

    observe = getattr(
        module,
        "observe_finmind_baseline_evidence",
        None,
    )

    assert callable(observe)

    evidence = {
        "status_code": 200,
        "content_type": "application/json",
        "size_bytes": 256,
        "payload": {
            "data": [
                {
                    "date": "2026-09-23",
                    "stock_id": "2330",
                    "open": 1000,
                    "max": 1010,
                    "min": 995,
                    "close": 1005,
                    "Trading_Volume": 12345678,
                    "extra_raw_field": "must-not-leak",
                }
            ]
        },
    }

    result = observe(
        evidence=evidence,
        stock_id="2330",
        trading_date="2026-09-23",
    )

    assert result.get("allowed") is True

    observed = result.get("observed")

    assert isinstance(observed, dict)

    assert tuple(observed.keys()) == (
        "date",
        "stock_id",
        "open",
        "max",
        "min",
        "close",
        "Trading_Volume",
    )

    assert observed["date"] == "2026-09-23"
    assert observed["stock_id"] == "2330"
    assert observed["open"] == 1000
    assert observed["max"] == 1010
    assert observed["min"] == 995
    assert observed["close"] == 1005
    assert observed["Trading_Volume"] == 12345678

    assert "payload" not in result
    assert "evidence" not in result
    assert "extra_raw_field" not in repr(result)

    print("[PASS] RAW_EVIDENCE accepted")
    print("[PASS] exact baseline fields observed")
    print("[PASS] extra raw fields excluded")
    print("[PASS] raw payload excluded")

    # Fail-closed: invalid evidence must be denied.
    invalid = observe(
        evidence={},
        stock_id="2330",
        trading_date="2026-09-23",
    )

    assert invalid.get("allowed") is False
    assert invalid.get("reason") == "HTTP_ERROR"

    print("[PASS] invalid evidence denied")

    # Fail-closed: requested baseline record must exist.
    not_found = observe(
        evidence=evidence,
        stock_id="2317",
        trading_date="2026-09-23",
    )

    assert not_found.get("allowed") is False
    assert (
        not_found.get("reason")
        == "BASELINE_RECORD_NOT_FOUND"
    )

    print("[PASS] missing baseline record denied")

    # Fail-closed: baseline record must be unique.
    duplicate_evidence = {
        **evidence,
        "payload": {
            "data": [
                dict(evidence["payload"]["data"][0]),
                dict(evidence["payload"]["data"][0]),
            ]
        },
    }

    duplicate = observe(
        evidence=duplicate_evidence,
        stock_id="2330",
        trading_date="2026-09-23",
    )

    assert duplicate.get("allowed") is False
    assert (
        duplicate.get("reason")
        == "BASELINE_RECORD_NOT_UNIQUE"
    )

    print("[PASS] duplicate baseline record denied")

    # Fail-closed: all required evidence fields must exist.
    missing_field_record = dict(
        evidence["payload"]["data"][0]
    )
    missing_field_record.pop("Trading_Volume")

    missing_field_evidence = {
        **evidence,
        "payload": {
            "data": [missing_field_record]
        },
    }

    missing_field = observe(
        evidence=missing_field_evidence,
        stock_id="2330",
        trading_date="2026-09-23",
    )

    assert missing_field.get("allowed") is False
    assert (
        missing_field.get("reason")
        == "REQUIRED_EVIDENCE_FIELDS_MISSING"
    )

    print("[PASS] missing required field denied")
    print(
        "FINMIND BASELINE EVIDENCE OBSERVER V1: PASS"
    )


if __name__ == "__main__":
    main()
