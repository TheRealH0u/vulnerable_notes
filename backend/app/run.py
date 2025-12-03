from application.util import generate
from application import create_app
from application.models import db, Users, Note
from werkzeug.security import generate_password_hash
import os
import random
import time
import socket
import psycopg2

basedir = os.path.abspath(os.path.dirname(__file__))

def initialize():
    # Wait for Postgres to be reachable to avoid startup race conditions
    pg_host = os.environ.get('POSTGRES_HOST', 'vuln_notes_db')
    pg_port = int(os.environ.get('POSTGRES_PORT', 5432))
    retries = int(os.environ.get('DB_RETRIES', 10))
    delay = int(os.environ.get('DB_RETRY_DELAY', 3))

    for attempt in range(1, retries + 1):
        try:
            # quick DNS resolution + TCP connect check
            sock = socket.create_connection((pg_host, pg_port), timeout=3)
            sock.close()
            # try a lightweight psycopg2 connect to be sure
            conn = psycopg2.connect(host=pg_host, port=pg_port, dbname=os.environ.get('POSTGRES_DB', 'testdb'), user=os.environ.get('POSTGRES_USER', 'user'), password=os.environ.get('POSTGRES_PASSWORD', 'password'), connect_timeout=3)
            conn.close()
            break
        except Exception as e:
            print(f"Database not ready (attempt {attempt}/{retries}): {e}")
            if attempt == retries:
                print("Exceeded max retries waiting for database; continuing and letting SQLAlchemy raise the final error.")
                break
            time.sleep(delay)

    # Only create tables if they don't exist
    db.create_all()


app = create_app()
# Initialization (schema creation and seeding) should be run explicitly once
# (for example via an entrypoint script or by applying `backend/db_seed.sql`).
# Avoid running seeding on import so multiple Gunicorn workers don't race.

#app.run(host='0.0.0.0', port=5000, debug=False, use_evalex=False)
