"""Authentication utilities — API key hashing, password hashing, session cookies.

API key format: ``sf_live_`` prefix + 32 random bytes (base62).
Storage: SHA-256 hash in ``api_keys.key_hash``.

Password hashing: bcrypt via hash_password() / verify_password().

Session auth: itsdangerous signed cookie ``senderfit_session`` containing customer_id.
Protected routes use ``get_current_customer()`` dependency.
"""

import hashlib
import logging
import os
import secrets
import string
from typing import Any

import bcrypt
from itsdangerous import URLSafeTimedSerializer, BadSignature, SignatureExpired

logger = logging.getLogger(__name__)

# ---------------------------------------------------------------------------
# API Key utilities
# ---------------------------------------------------------------------------

_KEY_PREFIX = "sf_live_"
_KEY_RANDOM_LENGTH = 32
_BASE62 = string.ascii_letters + string.digits


def generate_api_key() -> str:
    """Generate a new plaintext API key with the ``sf_live_`` prefix."""
    random_part = "".join(secrets.choice(_BASE62) for _ in range(_KEY_RANDOM_LENGTH))
    return f"{_KEY_PREFIX}{random_part}"


def hash_api_key(plaintext_key: str) -> str:
    """Return the SHA-256 hex digest of a plaintext API key."""
    return hashlib.sha256(plaintext_key.encode()).hexdigest()


def authenticate_api_key(key: str, conn) -> Any | None:
    """Look up an API key and return the customer row, or None.

    Falls back to the BATCH_API_KEY env var for backward compatibility.
    If conn is None, only the legacy env var fallback is checked.
    """
    from src.db import get_customer_by_api_key_hash

    if key and conn is not None:
        key_hash = hash_api_key(key)
        customer = get_customer_by_api_key_hash(conn, key_hash)
        if customer:
            return customer

    legacy_key = os.environ.get("BATCH_API_KEY", "")
    if legacy_key and key == legacy_key:
        return {"id": 0, "email": "legacy", "name": "Legacy API Key"}

    return None


# ---------------------------------------------------------------------------
# Password hashing (bcrypt)
# ---------------------------------------------------------------------------

def hash_password(plaintext: str) -> str:
    """Hash a password with bcrypt. Returns a string safe for DB storage."""
    return bcrypt.hashpw(plaintext.encode(), bcrypt.gensalt()).decode()


def verify_password(plaintext: str, hashed: str) -> bool:
    """Verify a plaintext password against a bcrypt hash."""
    return bcrypt.checkpw(plaintext.encode(), hashed.encode())


# ---------------------------------------------------------------------------
# Session cookie (itsdangerous)
# ---------------------------------------------------------------------------

SESSION_COOKIE_NAME = "senderfit_session"
SESSION_MAX_AGE = 86400 * 7  # 7 days


_serializer: URLSafeTimedSerializer | None = None
_serializer_secret: str | None = None


def _get_serializer() -> URLSafeTimedSerializer:
    global _serializer, _serializer_secret
    secret = os.environ.get("SECRET_KEY", "")
    if not secret:
        if not os.environ.get("SENDERFIT_SKIP_DB"):
            raise RuntimeError(
                "SECRET_KEY is not set. This is required in production. "
                "Generate one: python -c \"import secrets; print(secrets.token_hex(32))\""
            )
        logger.warning(
            "SECRET_KEY is not set — using insecure default (dev mode). "
            "Set SECRET_KEY in production."
        )
        secret = "dev-secret-change-me"
    # Re-create if SECRET_KEY changed (supports test isolation)
    if _serializer is None or _serializer_secret != secret:
        _serializer = URLSafeTimedSerializer(secret)
        _serializer_secret = secret
    return _serializer


def create_session_token(customer_id: int) -> str:
    """Create a signed session token containing the customer_id."""
    return _get_serializer().dumps({"cid": customer_id})


def decode_session_token(token: str) -> int | None:
    """Decode a session token and return the customer_id, or None if invalid/expired."""
    try:
        data = _get_serializer().loads(token, max_age=SESSION_MAX_AGE)
        return data.get("cid")
    except (BadSignature, SignatureExpired):
        return None


def get_current_customer_id(request) -> int | None:
    """Extract customer_id from the session cookie on a request, or None."""
    token = request.cookies.get(SESSION_COOKIE_NAME)
    if not token:
        return None
    return decode_session_token(token)


# ---------------------------------------------------------------------------
# CSRF token (itsdangerous-based, scoped to session)
# ---------------------------------------------------------------------------

CSRF_MAX_AGE = 3600  # 1 hour


def generate_csrf_token(session_id: str = "") -> str:
    """Generate a signed CSRF token scoped to the given session identifier."""
    s = _get_serializer()
    return s.dumps({"csrf": True, "sid": session_id})


def validate_csrf_token(token: str, session_id: str = "") -> bool:
    """Validate a CSRF token. Returns True if valid and not expired."""
    try:
        data = _get_serializer().loads(token, max_age=CSRF_MAX_AGE)
        return data.get("csrf") is True and data.get("sid", "") == session_id
    except (BadSignature, SignatureExpired):
        return False
