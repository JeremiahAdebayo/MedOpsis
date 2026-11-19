from fastapi.testclient import TestClient


def test_chat_requires_application_authentication():
    import backend.app.main as entrypoint
    assert hasattr(entrypoint, "app"), "The chat API has not been implemented"
    response = TestClient(entrypoint.app).post("/chat", json={"language": "en", "messages": [{"role": "user", "content": "Synthetic test message"}]})
    assert response.status_code == 401
    assert response.json()["detail"]["code"] == "authentication_required"
