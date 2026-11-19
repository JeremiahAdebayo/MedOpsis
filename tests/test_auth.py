import importlib
import importlib.util
from types import SimpleNamespace
import time
import pytest
from fastapi import HTTPException


def auth_module():
    assert importlib.util.find_spec("ai_services.chat.auth") is not None, "JWT verification is missing"
    return importlib.import_module("ai_services.chat.auth")


@pytest.mark.parametrize("changes,expected", [({}, 200), ({"iss": "wrong"}, 401), ({"aud": "wrong"}, 401), ({"exp": 1}, 401), ({"sub": ""}, 401)])
def test_jwt_signature_and_claim_verification(monkeypatch, auth_setup, changes, expected):
    auth = auth_module()
    seen = []
    class ControlledKeys:
        def get_signing_key_from_jwt(self, token):
            return SimpleNamespace(key=auth_setup.public_key)
    def configured_client(url):
        seen.append(url)
        return ControlledKeys()
    monkeypatch.setattr(auth, "jwks_client", configured_client)
    token = auth_setup.token(**changes)
    if expected == 200:
        assert auth.authorize_token(token) == "synthetic-user"
        assert seen == [auth_setup.issuer + "/jwks"]
    else:
        with pytest.raises(HTTPException) as exc:
            auth.authorize_token(token)
        assert exc.value.status_code == expected


def test_auth_configuration_fails_closed(monkeypatch, auth_setup):
    auth = auth_module()
    monkeypatch.delenv("MEDOPSIS_AUTH_AUDIENCE")
    with pytest.raises(HTTPException) as exc:
        auth.authorize_token(auth_setup.token())
    assert exc.value.status_code == 503
