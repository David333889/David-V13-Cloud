from requests.structures import CaseInsensitiveDict

from v14.finmind_live_backend import FinMindReadOnlyBackend


class FakeResponse:
    status_code = 200

    headers = CaseInsensitiveDict(
        {
            "Content-Type":
                "application/json; charset=utf-8",
        }
    )

    content = b'{"data":[{"stock_id":"2330"}]}'

    def json(self):
        return {
            "data": [
                {
                    "date": "2026-09-23",
                    "stock_id": "2330",
                    "close": 1000,
                }
            ]
        }


class FakeSession:
    def __init__(self):
        self.calls = 0

    def get(self, *args, **kwargs):
        self.calls += 1
        return FakeResponse()


def main():
    print(
        "=== GATE 28D.2D - REAL RESPONSE HEADERS "
        "MAPPING CONTRACT V1 ==="
    )

    session = FakeSession()

    backend = FinMindReadOnlyBackend(
        session=session,
    )

    evidence = backend.get(
        url="https://api.finmindtrade.com/api/v4/data",
        headers={},
        timeout=10,
        params={
            "dataset": "TaiwanStockPrice",
            "data_id": "2330",
            "start_date": "2026-09-23",
            "end_date": "2026-09-23",
            "token": "TEST_RUNTIME_SECRET_ONLY",
        },
        allow_redirects=False,
    )

    assert session.calls == 1

    assert evidence.get("status_code") == 200

    assert evidence.get(
        "content_type"
    ) == "application/json; charset=utf-8"

    assert isinstance(
        evidence.get("payload"),
        dict,
    )

    assert len(
        evidence["payload"]["data"]
    ) == 1

    public_text = repr(evidence)

    assert "TEST_RUNTIME_SECRET_ONLY" not in public_text

    print("[PASS] CaseInsensitiveDict accepted")
    print("[PASS] Content-Type preserved")
    print("[PASS] JSON payload preserved")
    print("[PASS] exactly one fake GET")
    print("[PASS] secret excluded from evidence")

    print(
        "=== GATE 28D.2D REAL RESPONSE HEADERS "
        "MAPPING RESULT: PASS ==="
    )


if __name__ == "__main__":
    main()