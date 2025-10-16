from fastapi.testclient import TestClient
import os

from main import app


def test_root():
    client = TestClient(app)
    r = client.get("/")
    assert r.status_code == 200
    assert r.json().get("status") == "ok"


def test_verify_endpoint(monkeypatch):
    client = TestClient(app)
    # Set VERIFY_TOKEN env variable for the test
    monkeypatch.setenv("VERIFY_TOKEN", "test-token")
    # call endpoint with matching token
    r = client.get("/webhook/?hub.mode=subscribe&hub.challenge=123&hub.verify_token=test-token")
    assert r.status_code == 200
    assert r.text == "123"


def test_receive_webhook(monkeypatch):
    sent = {}

    def fake_send(to, text):
        sent['to'] = to
        sent['text'] = text
        return {"mocked": True}

    monkeypatch.setenv("WHATSAPP_TOKEN", "dummy")
    monkeypatch.setenv("WHATSAPP_PHONE_NUMBER_ID", "123")
    # patch the send_text_message function
    import app.whatsapp_api as wa
    monkeypatch.setattr(wa, "send_text_message", fake_send)

    client = TestClient(app)
    payload = {
        "entry": [
            {
                "changes": [
                    {
                        "value": {
                            "messages": [
                                {"from": "1111", "text": {"body": "Hello"}}
                            ]
                        }
                    }
                ]
            }
        ]
    }
    r = client.post("/webhook/", json=payload)
    assert r.status_code == 200
    assert sent['to'] == "1111"
    assert "Hello" in sent['text'] or "hello" in sent['text'].lower()
