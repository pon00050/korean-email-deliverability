"""Shared pytest fixtures for the test suite."""
import sqlite3

import pytest

from src.db import create_tables


@pytest.fixture
def conn():
    """Return a fresh in-memory SQLite connection with schema applied."""
    c = sqlite3.connect(
        ":memory:",
        detect_types=sqlite3.PARSE_DECLTYPES | sqlite3.PARSE_COLNAMES,
    )
    c.row_factory = sqlite3.Row
    create_tables(c)
    yield c
    c.close()
