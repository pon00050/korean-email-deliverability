"""Tests for POST /batch — Phase 3 B2B Enrichment API.

All DNS/scan activity is mocked via _default_scan_executor so no real network
calls are made. The FastAPI TestClient is reused from test_routes.py patterns.
"""

import sys
from types import ModuleType
from unittest.mock import MagicMock, patch

import pytest
from fastapi.testclient import TestClient

from src.models import CheckResult


# ---------------------------------------------------------------------------
# Stub psycopg before app.py is imported (no libpq in CI)
# ---------------------------------------------------------------------------

def _make_psycopg_stub():
    stub = ModuleType("psycopg")
    stub.connect = MagicMock(
        side_effect=RuntimeError("psycopg not available — use get_db mock")
    )
    return stub


try:
    import psycopg  # noqa: F401
except ImportError:
    sys.modules.setdefault("psycopg", _make_psycopg_stub())


# ---------------------------------------------------------------------------
# Shared test fixtures
# ---------------------------------------------------------------------------

def _fake_results() -> list[CheckResult]:
    return [
        CheckResult(name="SPF",            status="pass", score=100, message_ko="SPF 레코드 정상"),
        CheckResult(name="DKIM",           status="fail", score=0,   message_ko="DKIM 레코드 없음"),
        CheckResult(name="DMARC",          status="fail", score=0,   message_ko="DMARC 레코드 없음"),
        CheckResult(name="PTR",            status="pass", score=100, message_ko="PTR 레코드 정상"),
        CheckResult(name="KISA RBL",       status="pass", score=100, message_ko="차단 목록 없음"),
        CheckResult(name="KISA 화이트도메인", status="error", score=0,  message_ko="서비스 종료"),
        CheckResult(name="국제 블랙리스트",  status="pass", score=100, message_ko="국제 블랙리스트 없음"),
    ]


def _fake_scores() -> dict:
    return {
        "overall": 75,
        "grade": "B",
        "naver": 68,
        "naver_label": "보통 — 일부 이메일이 스팸함에 분류될 수 있음",
    }


@pytest.fixture
def client():
    """TestClient with scheduler and DB patched out."""
    import app as app_module

    with (
        patch.object(app_module, "get_db", side_effect=RuntimeError("no db in batch tests")),
        patch.object(app_module, "BackgroundScheduler"),
        TestClient(app_module.app, raise_server_exceptions=True) as c,
    ):
        yield c


# ---------------------------------------------------------------------------
# Test 1: Happy path — JSON response
# ---------------------------------------------------------------------------

@patch("src.batch._default_scan_executor")
def test_batch_json_happy_path(mock_exec, client):
    mock_exec.return_value = (_fake_results(), _fake_scores())

    resp = client.post("/batch", json={"domains": ["a.co.kr", "b.co.kr"]})

    assert resp.status_code == 200
    data = resp.json()
    assert data["count"] == 2
    assert data["results"][0]["domain"] == "a.co.kr"
    assert data["results"][1]["domain"] == "b.co.kr"
    assert data["results"][0]["overall"] == 75
    assert data["results"][0]["grade"] == "B"
    assert "SPF" in data["results"][0]["checks"]
    assert data["results"][0]["checks"]["SPF"]["status"] == "pass"
    assert "scanned_at" in data


# ---------------------------------------------------------------------------
# Test 2: CSV output
# ---------------------------------------------------------------------------

@patch("src.batch._default_scan_executor")
def test_batch_csv_output(mock_exec, client):
    mock_exec.return_value = (_fake_results(), _fake_scores())

    resp = client.post("/batch", json={"domains": ["a.co.kr"], "format": "csv"})

    assert resp.status_code == 200
    assert "text/csv" in resp.headers["content-type"]
    text = resp.text
    lines = [l for l in text.splitlines() if l]
    assert len(lines) == 2  # header + 1 data row
    header = lines[0]
    assert "domain" in header
    assert "overall" in header
    assert "spf_status" in header
    assert "intl_bl_score" in header
    data_row = lines[1]
    assert "a.co.kr" in data_row
    assert "75" in data_row


# ---------------------------------------------------------------------------
# Test 3: Auth rejects bad key when BATCH_API_KEY is set
# ---------------------------------------------------------------------------

@patch("src.batch._default_scan_executor")
def test_batch_auth_rejects_bad_key(mock_exec, client, monkeypatch):
    monkeypatch.setenv("BATCH_API_KEY", "secret-key")
    mock_exec.return_value = (_fake_results(), _fake_scores())

    resp = client.post(
        "/batch",
        json={"domains": ["a.co.kr"]},
        headers={"X-API-Key": "wrong-key"},
    )

    assert resp.status_code == 401


# ---------------------------------------------------------------------------
# Test 4: Auth disabled when BATCH_API_KEY is not set
# ---------------------------------------------------------------------------

@patch("src.batch._default_scan_executor")
def test_batch_auth_disabled_when_env_unset(mock_exec, client, monkeypatch):
    monkeypatch.delenv("BATCH_API_KEY", raising=False)
    mock_exec.return_value = (_fake_results(), _fake_scores())

    # No key header at all — should still pass
    resp = client.post("/batch", json={"domains": ["a.co.kr"]})

    assert resp.status_code == 200


# ---------------------------------------------------------------------------
# Test 5: Too many domains → 422
# ---------------------------------------------------------------------------

def test_batch_too_many_domains(client):
    domains = [f"domain{i}.co.kr" for i in range(51)]
    resp = client.post("/batch", json={"domains": domains})
    assert resp.status_code == 422


# ---------------------------------------------------------------------------
# Test 6: No valid domains (all items lack '.') → 422
# ---------------------------------------------------------------------------

def test_batch_no_valid_domains(client):
    resp = client.post("/batch", json={"domains": ["localhost", "nodot"]})
    assert resp.status_code == 422


# ---------------------------------------------------------------------------
# Test 7: One domain errors — others still returned; errored domain has "error" key
# ---------------------------------------------------------------------------

def test_batch_one_domain_errors(client):
    def _side_effect(domain):
        if domain == "bad.co.kr":
            raise RuntimeError("DNS timeout")
        return (_fake_results(), _fake_scores())

    with patch("src.batch._default_scan_executor", side_effect=_side_effect):
        resp = client.post(
            "/batch",
            json={"domains": ["good.co.kr", "bad.co.kr"]},
        )

    assert resp.status_code == 200
    data = resp.json()
    assert data["count"] == 2

    by_domain = {r["domain"]: r for r in data["results"]}
    assert "error" in by_domain["bad.co.kr"]
    assert "overall" in by_domain["good.co.kr"]
