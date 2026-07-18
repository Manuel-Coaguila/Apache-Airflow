#!/usr/bin/env python3
"""
Create/update Airflow connections from ops/connections/connections.json.

Usage:
    docker compose run --rm airflow-cli python /opt/airflow/ops/connections/create_connections.py
"""
import json
import sys

from sqlalchemy import create_engine
from sqlalchemy.orm import Session

from airflow import settings
from airflow.models.connection import Connection

JSON_PATH = "/opt/airflow/ops/connections/connections.json"


def upsert_connection(session: Session, conn_id: str, conn_type: str,
                      host: str = "", port: int = 0, login: str = "",
                      password: str = "", schema: str = "",
                      extra: str = "") -> str:
    existing = session.query(Connection).filter(
        Connection.conn_id == conn_id
    ).first()

    if existing:
        existing.conn_type = conn_type
        existing.host = host
        existing.port = port
        existing.login = login
        existing.password = password
        existing.schema = schema
        existing.extra = extra
        session.flush()
        return "UPDATED"

    conn = Connection(
        conn_id=conn_id,
        conn_type=conn_type,
        host=host,
        port=port,
        login=login,
        password=password,
        schema=schema,
        extra=extra,
    )
    session.add(conn)
    session.flush()
    return "CREATED"


def main() -> int:
    engine = create_engine(settings.SQL_ALCHEMY_CONN)
    with Session(engine) as session:
        with open(JSON_PATH) as f:
            data = json.load(f)

        results = []
        for entry in data:
            conn_id = entry.get("conn_id", "").strip()
            if not conn_id:
                continue

            action = upsert_connection(
                session,
                conn_id=conn_id,
                conn_type=entry.get("conn_type", "").strip(),
                host=entry.get("host", "").strip(),
                port=int(entry.get("port", 0)),
                login=entry.get("login", "").strip(),
                password=entry.get("password", "").strip(),
                schema=entry.get("schema", "").strip(),
                extra=entry.get("extra", "").strip(),
            )
            results.append(f"  {action}: {conn_id}")

        session.commit()

        print()
        for r in results:
            print(r)
        print("=" * 40)
        print(f"  Total: {len(results)}")
        print("=" * 40)
        return 0


if __name__ == "__main__":
    sys.exit(main())
