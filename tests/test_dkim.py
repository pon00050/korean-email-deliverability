"""Tests for DKIM check — focused on _estimate_key_bits correctness."""
import base64
import pytest
from unittest.mock import patch

from src.checks.dkim import _estimate_key_bits, check_dkim


# ---------------------------------------------------------------------------
# DER / SPKI construction helpers (test-local only)
# ---------------------------------------------------------------------------

def _der_len(n: int) -> bytes:
    if n < 128:
        return bytes([n])
    if n < 256:
        return bytes([0x81, n])
    return bytes([0x82, n >> 8, n & 0xff])


def _make_rsa_spki_b64(key_bits: int) -> str:
    """Build a minimal SubjectPublicKeyInfo DER for an RSA key of the given size."""
    mod_bytes = key_bits // 8
    modulus = b"\x00" + b"\xab" * mod_bytes  # leading zero + dummy modulus
    exponent = b"\x01\x00\x01"  # 65537

    def der_int(data: bytes) -> bytes:
        return b"\x02" + _der_len(len(data)) + data

    def der_seq(data: bytes) -> bytes:
        return b"\x30" + _der_len(len(data)) + data

    def der_bitstring(data: bytes) -> bytes:
        payload = b"\x00" + data  # unused_bits = 0
        return b"\x03" + _der_len(len(payload)) + payload

    rsa_pub = der_seq(der_int(modulus) + der_int(exponent))
    alg_id = bytes.fromhex("300d06092a864886f70d0101010500")  # rsaEncryption OID + NULL
    spki = der_seq(alg_id + der_bitstring(rsa_pub))
    return base64.b64encode(spki).decode()


def _dkim_record(p: str) -> str:
    return f"v=DKIM1; k=rsa; p={p}"


# ---------------------------------------------------------------------------
# _estimate_key_bits — unit tests
# ---------------------------------------------------------------------------

class TestEstimateKeyBits:
    def test_1024_bit_key_returns_1024(self):
        record = _dkim_record(_make_rsa_spki_b64(1024))
        assert _estimate_key_bits(record) == 1024

    def test_2048_bit_key_returns_2048(self):
        record = _dkim_record(_make_rsa_spki_b64(2048))
        assert _estimate_key_bits(record) == 2048

    def test_no_p_field_returns_none(self):
        assert _estimate_key_bits("v=DKIM1; k=rsa;") is None

    def test_malformed_base64_returns_none(self):
        assert _estimate_key_bits("v=DKIM1; k=rsa; p=!!!notbase64!!!") is None


# ---------------------------------------------------------------------------
# check_dkim — message format when weak key detected
# ---------------------------------------------------------------------------

class TestCheckDkimWeakKeyMessage:
    def test_weak_key_message_shows_correct_bits(self):
        """The user-facing message must show the real key size, not the DER byte count."""
        record = _dkim_record(_make_rsa_spki_b64(1024))
        with patch("src.checks.dkim._lookup", return_value=record):
            result = check_dkim("example.co.kr", selector="test")
        assert result.status == "warn"
        assert "1024비트" in result.message_ko
        assert "1296비트" not in result.message_ko
