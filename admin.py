"""Admin CLI for Senderfit — API key provisioning and management.

Usage:
    python admin.py create-key --email customer@example.com [--label "production"]
    python admin.py revoke-key <key-hash-prefix>
    python admin.py list-keys [--customer-email customer@example.com]

Requires DATABASE_URL environment variable to be set.
"""

import os
import sys

import typer

app = typer.Typer(help="Senderfit admin CLI — API key management")


def _get_conn():
    url = os.environ.get("DATABASE_URL")
    if not url:
        typer.echo("ERROR: DATABASE_URL environment variable is not set", err=True)
        raise typer.Exit(1)
    import psycopg
    return psycopg.connect(url)


@app.command()
def create_key(
    email: str = typer.Option(..., help="Customer email address"),
    label: str = typer.Option("", help="Optional label for this key"),
):
    """Create a new API key for a customer. Creates the customer if not found."""
    from src.auth import generate_api_key, hash_api_key
    from src.db import create_customer, get_customer_by_email, create_api_key

    conn = _get_conn()
    try:
        customer = get_customer_by_email(conn, email)
        if not customer:
            cid = create_customer(conn, email=email)
            typer.echo(f"Created customer: {email} (id={cid})")
        else:
            cid = customer["id"]
            typer.echo(f"Found customer: {email} (id={cid})")

        plaintext = generate_api_key()
        key_hash = hash_api_key(plaintext)
        create_api_key(conn, customer_id=cid, key_hash=key_hash, label=label)

        typer.echo(f"\nAPI Key (show once, save it now):\n  {plaintext}")
        typer.echo(f"\nKey hash (for reference): {key_hash[:16]}...")
    finally:
        conn.close()


@app.command()
def revoke_key(
    key_hash_prefix: str = typer.Argument(help="First 16+ chars of the key hash"),
):
    """Revoke an API key by its hash prefix."""
    from src.db import revoke_api_key

    conn = _get_conn()
    try:
        # Find the full hash matching the prefix
        safe_prefix = key_hash_prefix.replace("%", r"\%").replace("_", r"\_")
        cur = conn.execute(
            "SELECT key_hash FROM api_keys WHERE key_hash LIKE %s AND active = TRUE",
            (f"{safe_prefix}%",),
        )
        rows = cur.fetchall()
        if not rows:
            typer.echo("No active key found with that prefix.")
            raise typer.Exit(1)
        if len(rows) > 1:
            typer.echo(f"Ambiguous prefix — matches {len(rows)} keys. Use more characters.")
            raise typer.Exit(1)

        full_hash = rows[0][0]
        revoke_api_key(conn, full_hash)
        typer.echo(f"Revoked key: {full_hash[:16]}...")
    finally:
        conn.close()


@app.command()
def list_keys(
    customer_email: str = typer.Option("", help="Filter by customer email"),
):
    """List API keys, optionally filtered by customer email."""
    from src.db import get_customer_by_email, list_api_keys

    conn = _get_conn()
    try:
        if customer_email:
            customer = get_customer_by_email(conn, customer_email)
            if not customer:
                typer.echo(f"No customer found: {customer_email}")
                raise typer.Exit(1)
            keys = list_api_keys(conn, customer["id"])
            typer.echo(f"Keys for {customer_email}:")
        else:
            cur = conn.execute("SELECT * FROM api_keys ORDER BY created_at DESC")
            keys = cur.fetchall()
            typer.echo("All API keys:")

        if not keys:
            typer.echo("  (none)")
            return

        for k in keys:
            status = "active" if k["active"] in (True, 1) else "revoked"
            label_str = f" [{k['label']}]" if k["label"] else ""
            typer.echo(f"  {k['key_hash'][:16]}...  {status}{label_str}  (customer_id={k['customer_id']})")
    finally:
        conn.close()


if __name__ == "__main__":
    app()
