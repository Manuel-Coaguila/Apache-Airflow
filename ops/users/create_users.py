#!/usr/bin/env python3
"""
One-shot creation of users from ops/users/users.csv.

Usage:
    docker compose run --rm airflow-cli python /opt/airflow/ops/users/create_users.py
"""
import csv
import sys

from sqlalchemy import create_engine
from sqlalchemy.orm import Session
from werkzeug.security import generate_password_hash

from airflow import settings
from airflow.providers.fab.auth_manager.models import Role, User

CSV_PATH = "/opt/airflow/ops/users/users.csv"


def main() -> int:
    engine = create_engine(settings.SQL_ALCHEMY_CONN)
    with Session(engine) as session:
        with open(CSV_PATH, newline="") as f:
            reader = csv.DictReader(f, skipinitialspace=True)
            created = skipped = errors = 0

            for row in reader:
                username = row.get("username", "").strip()
                if not username or username.startswith("#"):
                    continue

                label = f"  [{row['role'].strip()}] {username} ... "
                sys.stdout.write(label)
                sys.stdout.flush()

                try:
                    if session.query(User).filter(User.username == username).first():
                        print("SKIPPED (exists)")
                        skipped += 1
                        continue

                    role = session.query(Role).filter(Role.name == row["role"].strip()).first()
                    if not role:
                        print("ERROR (role not found)")
                        errors += 1
                        continue

                    user = User()
                    user.username = username
                    user.email = row.get("email", "").strip()
                    user.first_name = row.get("firstname", "").strip()
                    user.last_name = row.get("lastname", "").strip()
                    user.password = generate_password_hash(row.get("password", "").strip())
                    user.roles = [role]

                    session.add(user)
                    session.flush()
                    print("OK")
                    created += 1
                except Exception as e:
                    session.rollback()
                    print(f"ERROR ({e})")
                    errors += 1

        session.commit()
        print()
        print("=" * 40)
        print(f"  Created: {created}  Skipped: {skipped}  Errors: {errors}")
        print("=" * 40)
        return errors


if __name__ == "__main__":
    sys.exit(main())
