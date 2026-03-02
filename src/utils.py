"""Shared utility functions."""


def normalize_domain(raw: str) -> str:
    """Strip whitespace, lowercase, and remove URL scheme/trailing slash."""
    return raw.strip().lower().removeprefix("https://").removeprefix("http://").rstrip("/")
