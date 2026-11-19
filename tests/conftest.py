import json
import time
from types import SimpleNamespace
import jwt
import pytest
import requests
from cryptography.hazmat.primitives.asymmetric import rsa


@pytest.fixture(autouse=True)
def forbid_unmocked_provider_calls(monkeypatch):
    monkeypatch.setenv("GROQ_API_KEY", "synthetic-unit-test-key-not-real")
    def blocked(*args, **kwargs):
        raise AssertionError("A unit test attempted a real provider request")
    monkeypatch.setattr(requests.Session, "post", blocked)


@pytest.fixture
def signing_key():
    return rsa.generate_private_key(public_exponent=65537, key_size=2048)


@pytest.fixture
def auth_setup(monkeypatch, signing_key):
    issuer = "https://synthetic-issuer.example.invalid"
    audience = "medopsis-synthetic-test"
    monkeypatch.setenv("MEDOPSIS_AUTH_ISSUER", issuer)
    monkeypatch.setenv("MEDOPSIS_AUTH_AUDIENCE", audience)
    monkeypatch.setenv("MEDOPSIS_AUTH_JWKS_URL", issuer + "/jwks")
    def token(**changes):
        claims = {"iss": issuer, "aud": audience, "sub": "synthetic-user", "exp": int(time.time()) + 300}
        claims.update(changes)
        return jwt.encode(claims, signing_key, algorithm="RS256", headers={"kid": "synthetic-key", "jku": "https://attacker.example.invalid/ignored"})
    return SimpleNamespace(token=token, public_key=signing_key.public_key(), issuer=issuer, audience=audience)
