import importlib


class FakeResponse:
    status_code = 200
    headers = {
        "Content-Type": "application/json",
    }
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
        self.calls = []

    def get(
        self,
        url,
        headers=None,
        timeout=None,
        params=None,
        allow_redirects=False,
    ):
        self.calls.append(
            {
                "url": url,
                "headers": headers,
                "timeout": timeout,
                "params": params,
                "allow_redirects": allow_redirects,
            }
        )

        return FakeResponse()


class FakeSessionFactory:
    def __init__(self):
        self.calls = 0
        self.sessions = []

    def __call__(self):
        self.calls += 1

        session = FakeSession()
        self.sessions.append(session)

        return session


def main():
    print(
        "=== GATE 28D.2C - FINMIND QUERY TOKEN "
        "TRANSPORT CONTRACT V1 ==="
    )

    module = importlib.import_module(
        "v14.controlled_live_fetch"
    )

    execute = getattr(
        module,
        "execute_controlled_fetch",
    )

    secret = "TEST_RUNTIME_SECRET_ONLY"

    factory = FakeSessionFactory()

    result = execute(
        env={
            "FINMIND_API_TOKEN": secret,
        },
        session_factory=factory,
        url="https://api.finmindtrade.com/api/v4/data",
        timeout=10,
        params={
            "dataset": "TaiwanStockPrice",
            "data_id": "2330",
            "start_date": "2026-09-23",
            "end_date": "2026-09-23",
        },
    )

    assert result.get("allowed") is True

    assert factory.calls == 1
    assert len(factory.sessions) == 1

    calls = factory.sessions[0].calls

    assert len(calls) == 1

    call = calls[0]

    params = call.get("params")
    headers = call.get("headers")

    assert isinstance(params, dict)

    assert params.get("dataset") == "TaiwanStockPrice"
    assert params.get("data_id") == "2330"
    assert params.get("start_date") == "2026-09-23"
    assert params.get("end_date") == "2026-09-23"

    # FinMind member API token must be transported
    # as the documented query parameter.
    assert params.get("token") == secret

    # Member API-token path must not also emit Bearer auth.
    assert not headers
    assert "Authorization" not in headers

    # Secret must remain transport-only.
    public_text = repr(result)

    assert secret not in public_text
    assert "Authorization" not in public_text
    assert "Bearer" not in public_text

    print("[PASS] runtime token transported as query parameter")
    print("[PASS] Bearer authorization header absent")
    print("[PASS] exactly one fake GET")
    print("[PASS] public evidence excludes runtime secret")

    print(
        "=== GATE 28D.2C FINMIND QUERY TOKEN "
        "TRANSPORT RESULT: PASS ==="
    )


if __name__ == "__main__":
    main()
