"""Tests for src/auth.py — API key generation, hashing, and authentication."""

import os
from unittest.mock import patch

from src.auth import generate_api_key, hash_api_key, authenticate_api_key
from src.db import create_customer, create_api_key, revoke_api_key


# conn fixture is in tests/conftest.py


class TestKeyGeneration:
    def test_key_has_prefix(self):
        key = generate_api_key()
        assert key.startswith("sf_live_")

    def test_key_length(self):
        key = generate_api_key()
        assert len(key) == len("sf_live_") + 32

    def test_keys_are_unique(self):
        keys = {generate_api_key() for _ in range(10)}
        assert len(keys) == 10


class TestKeyHashing:
    def test_hash_is_deterministic(self):
        key = "sf_live_abc123"
        assert hash_api_key(key) == hash_api_key(key)

    def test_different_keys_different_hashes(self):
        assert hash_api_key("sf_live_aaa") != hash_api_key("sf_live_bbb")

    def test_hash_is_hex_string(self):
        h = hash_api_key("sf_live_test")
        assert len(h) == 64  # SHA-256 hex digest
        assert all(c in "0123456789abcdef" for c in h)


class TestAuthenticate:
    def test_valid_key_returns_customer(self, conn):
        cid = create_customer(conn, email="c@example.com")
        key = generate_api_key()
        create_api_key(conn, customer_id=cid, key_hash=hash_api_key(key))

        with patch.dict(os.environ, {"BATCH_API_KEY": ""}, clear=False):
            result = authenticate_api_key(key, conn)
        assert result is not None
        assert result["id"] == cid

    def test_invalid_key_returns_none(self, conn):
        with patch.dict(os.environ, {"BATCH_API_KEY": ""}, clear=False):
            result = authenticate_api_key("sf_live_bogus", conn)
        assert result is None

    def test_revoked_key_returns_none(self, conn):
        cid = create_customer(conn, email="c@example.com")
        key = generate_api_key()
        key_hash = hash_api_key(key)
        create_api_key(conn, customer_id=cid, key_hash=key_hash)
        revoke_api_key(conn, key_hash)

        with patch.dict(os.environ, {"BATCH_API_KEY": ""}, clear=False):
            result = authenticate_api_key(key, conn)
        assert result is None

    def test_legacy_env_var_fallback(self, conn):
        with patch.dict(os.environ, {"BATCH_API_KEY": "legacy-secret"}, clear=False):
            result = authenticate_api_key("legacy-secret", conn)
        assert result is not None
        assert result["id"] == 0  # synthetic legacy customer

    def test_empty_key_with_no_env_var(self, conn):
        with patch.dict(os.environ, {"BATCH_API_KEY": ""}, clear=False):
            result = authenticate_api_key("", conn)
        assert result is None
