"""Tests for session auth — password hashing, session tokens, login/register flows."""

import os
from unittest.mock import patch

import pytest

from src.auth import (
    hash_password, verify_password,
    create_session_token, decode_session_token,
    _get_serializer,
)


class TestPasswordHashing:
    def test_hash_and_verify(self):
        pw = "testpassword123"
        h = hash_password(pw)
        assert verify_password(pw, h)

    def test_wrong_password_fails(self):
        h = hash_password("correct")
        assert not verify_password("wrong", h)

    def test_hashes_are_unique(self):
        h1 = hash_password("same")
        h2 = hash_password("same")
        assert h1 != h2  # bcrypt uses random salt


class TestSessionTokens:
    def test_create_and_decode(self):
        with patch.dict(os.environ, {"SECRET_KEY": "test-secret"}):
            token = create_session_token(42)
            cid = decode_session_token(token)
            assert cid == 42

    def test_invalid_token_returns_none(self):
        with patch.dict(os.environ, {"SECRET_KEY": "test-secret"}):
            assert decode_session_token("bogus-token") is None

    def test_different_secret_fails(self):
        with patch.dict(os.environ, {"SECRET_KEY": "secret-a"}):
            token = create_session_token(1)
        with patch.dict(os.environ, {"SECRET_KEY": "secret-b"}):
            assert decode_session_token(token) is None


class TestSecretKeyFailClosed:
    def test_missing_secret_key_raises_without_skip_db(self):
        """Without SECRET_KEY and without SENDERFIT_SKIP_DB, _get_serializer must raise."""
        env = {"SECRET_KEY": "", "SENDERFIT_SKIP_DB": ""}
        with patch.dict(os.environ, env, clear=False):
            os.environ.pop("SECRET_KEY", None)
            os.environ.pop("SENDERFIT_SKIP_DB", None)
            # Reset cached serializer so _get_serializer re-evaluates
            import src.auth
            src.auth._serializer = None
            src.auth._serializer_secret = None
            with pytest.raises(RuntimeError, match="SECRET_KEY"):
                _get_serializer()

    def test_missing_secret_key_allowed_with_skip_db(self):
        """With SENDERFIT_SKIP_DB=1 and no SECRET_KEY, fallback is used (no error)."""
        env = {"SENDERFIT_SKIP_DB": "1"}
        with patch.dict(os.environ, env, clear=False):
            os.environ.pop("SECRET_KEY", None)
            import src.auth
            src.auth._serializer = None
            src.auth._serializer_secret = None
            serializer = _get_serializer()
            assert serializer is not None
