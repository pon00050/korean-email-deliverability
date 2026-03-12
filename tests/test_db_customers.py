"""Tests for customer and API key CRUD in src/db.py."""

import pytest

from src.db import (
    create_customer,
    get_customer_by_email,
    get_customer_by_id,
    create_api_key,
    get_customer_by_api_key_hash,
    revoke_api_key,
    list_api_keys,
)


# conn fixture is in tests/conftest.py


class TestCustomers:
    def test_create_and_get_by_email(self, conn):
        cid = create_customer(conn, email="test@example.com", name="Test User")
        row = get_customer_by_email(conn, "test@example.com")
        assert row is not None
        assert row["id"] == cid
        assert row["email"] == "test@example.com"
        assert row["name"] == "Test User"
        assert row["active"] in (1, True)

    def test_get_by_email_not_found(self, conn):
        assert get_customer_by_email(conn, "nobody@example.com") is None

    def test_get_by_id(self, conn):
        cid = create_customer(conn, email="test@example.com")
        row = get_customer_by_id(conn, cid)
        assert row is not None
        assert row["email"] == "test@example.com"

    def test_get_by_id_not_found(self, conn):
        assert get_customer_by_id(conn, 9999) is None

    def test_duplicate_email_raises(self, conn):
        create_customer(conn, email="dup@example.com")
        with pytest.raises(Exception):
            create_customer(conn, email="dup@example.com")

    def test_create_with_password_hash(self, conn):
        cid = create_customer(conn, email="pw@example.com", password_hash="hashed123")
        row = get_customer_by_email(conn, "pw@example.com")
        assert row["password_hash"] == "hashed123"


class TestApiKeys:
    def test_create_and_lookup(self, conn):
        cid = create_customer(conn, email="c@example.com")
        kid = create_api_key(conn, customer_id=cid, key_hash="abc123hash", label="test key")
        assert kid is not None

        customer = get_customer_by_api_key_hash(conn, "abc123hash")
        assert customer is not None
        assert customer["id"] == cid

    def test_lookup_nonexistent_hash(self, conn):
        assert get_customer_by_api_key_hash(conn, "nonexistent") is None

    def test_revoked_key_returns_none(self, conn):
        cid = create_customer(conn, email="c@example.com")
        create_api_key(conn, customer_id=cid, key_hash="revoke_me")
        revoke_api_key(conn, "revoke_me")
        assert get_customer_by_api_key_hash(conn, "revoke_me") is None

    def test_list_api_keys(self, conn):
        cid = create_customer(conn, email="c@example.com")
        create_api_key(conn, customer_id=cid, key_hash="key1", label="first")
        create_api_key(conn, customer_id=cid, key_hash="key2", label="second")
        keys = list_api_keys(conn, cid)
        assert len(keys) == 2
        labels = {k["label"] for k in keys}
        assert labels == {"first", "second"}

    def test_key_label_defaults_empty(self, conn):
        cid = create_customer(conn, email="c@example.com")
        create_api_key(conn, customer_id=cid, key_hash="nolabel")
        keys = list_api_keys(conn, cid)
        assert keys[0]["label"] == ""
