#!/usr/bin/env python3
"""
Generate a SQL seed file matching the data previously created by initialize() in run.py.

This script will compute password hashes using Werkzeug's generate_password_hash if available.
If Werkzeug is not installed in the environment running this script, it falls back to a PBKDF2-SHA256
implementation that produces a string in the same format: pbkdf2:sha256:<iterations>$<salt>$<hash>

It writes the SQL to ../db_seed.sql (relative to this script's directory).
"""
import os
from pathlib import Path
import secrets
import hashlib

try:
    # Prefer Werkzeug if installed
    from werkzeug.security import generate_password_hash
    USE_WERKZEUG = True
except Exception:
    USE_WERKZEUG = False

DEFAULT_ITER = 260000

def fallback_generate_password_hash(password: str, iterations: int = DEFAULT_ITER, salt_bytes: int = 8) -> str:
    salt = secrets.token_hex(salt_bytes)
    dk = hashlib.pbkdf2_hmac('sha256', password.encode('utf-8'), salt.encode('utf-8'), iterations)
    return f"pbkdf2:sha256:{iterations}${salt}${dk.hex()}"


def gen_hash(pw: str) -> str:
    if USE_WERKZEUG:
        # Werkzeug's default method format is: pbkdf2:sha256:<iterations>$<salt>$<hash>
        return generate_password_hash(pw)
    else:
        return fallback_generate_password_hash(pw)


def main():
    script_dir = Path(__file__).resolve().parent
    out_path = script_dir.parent / 'db_seed.sql'

    # Passwords from app initialize
    admin_pw = '#ThisIsSomeLongAssPasswordThatYouWillNeverGetBecauseItsSoLong123!!!!!'
    bob_pw = 'password'
    alice_pw = 'AliceIsCool1'

    admin_hash = gen_hash(admin_pw)
    bob_hash = gen_hash(bob_pw)
    alice_hash = gen_hash(alice_pw)

    # Prepare SQL content
    sql_lines = []
    sql_lines.append('-- Seed users')
    sql_lines.append("INSERT INTO users (id, username, email, password) VALUES")
    # Escape braces in the admin email so str.format doesn't treat them as placeholders
    sql_lines.append("  (1, 'admin', 'ctf{{You_Found_The_Flag!!!}}', '{}'),".format(admin_hash))
    sql_lines.append("  (2, 'bob', 'bob@example.com', '{}'),".format(bob_hash))
    sql_lines.append("  (3, 'alice', 'alice@example.com', '{}');".format(alice_hash))
    sql_lines.append("")
    sql_lines.append("-- Reset users sequence")
    sql_lines.append("SELECT setval(pg_get_serial_sequence('users','id'), (SELECT MAX(id) FROM users));")
    sql_lines.append("")

    # Seed notes: 5 for alice (user_id=3), 5 for bob (user_id=2), 1 admin note (user_id=1)
    sql_lines.append('-- Seed notes')
    sql_lines.append("INSERT INTO note (id, user_id, title, content, created_at, updated_at) VALUES")
    nid = 1
    # Alice notes (1-5)
    for i in range(1, 6):
        title = f"Alice Note {i}"
        content = f"This is Alice''s note #{i}."
        sql_lines.append("  ({nid}, 3, '{title}', '{content}', NOW(), NOW()),".format(nid=nid, title=title.replace("'","''"), content=content.replace("'","''")))
        nid += 1

    # Admin special note
    title = "Admin Special Note"
    content = "This note belongs to admin."
    sql_lines.append("  ({nid}, 1, '{title}', '{content}', NOW(), NOW()),".format(nid=nid, title=title.replace("'","''"), content=content.replace("'","''")))
    nid += 1

    # Bob notes
    for i in range(1, 6):
        title = f"Bob Note {i}"
        content = f"This is Bob''s note #{i}."
        comma = ',' if i < 5 else ';'
        sql_lines.append("  ({nid}, 2, '{title}', '{content}', NOW(), NOW()){comma}".format(nid=nid, title=title.replace("'","''"), content=content.replace("'","''"), comma=comma))
        nid += 1

    sql_lines.append("")
    sql_lines.append("-- Reset note sequence")
    sql_lines.append("SELECT setval(pg_get_serial_sequence('note','id'), (SELECT MAX(id) FROM note));")

    # Write file
    out_path.write_text('\n'.join(sql_lines))
    print(f"Wrote SQL seed to: {out_path}")


if __name__ == '__main__':
    main()
