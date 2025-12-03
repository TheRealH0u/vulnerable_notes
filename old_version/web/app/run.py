from application.util import generate
from application import create_app
from application.models import db, Users, Note
from werkzeug.security import generate_password_hash
import os
import random

basedir = os.path.abspath(os.path.dirname(__file__))

def initialize():
    # Only create tables if they don't exist
    db.create_all()

    # --- Create users (ensure admin is created first) ---
    if not Users.query.filter_by(username='admin').first():
        admin = Users(
            username='admin',
            email='ctf{You_Found_The_Flag!!!}',
            password=generate_password_hash('#ThisIsSomeLongAssPasswordThatYouWillNeverGetBecauseItsSoLong123!!!!!')
        )
        db.session.add(admin)
    else:
        admin = Users.query.filter_by(username='admin').first()

    # second user: bob (keep your existing bob)
    if not Users.query.filter_by(username='bob').first():
        bob = Users(
            username='bob',
            email='bob@example.com',
            password=generate_password_hash('password')
        )
        db.session.add(bob)
    else:
        bob = Users.query.filter_by(username='bob').first()

    # third user: alice
    if not Users.query.filter_by(username='alice').first():
        alice = Users(
            username='alice',
            email='alice@example.com',
            password=generate_password_hash('AliceIsCool1')
        )
        db.session.add(alice)
    else:
        alice = Users.query.filter_by(username='alice').first()

    # Commit users so they have IDs
    db.session.commit()

    # --- Seed notes only if there are no notes yet (so reruns are idempotent) ---
    if Note.query.count() == 0:
        notes_to_add = []

        # 5 notes for alice
        for i in range(1, 6):
            notes_to_add.append(
                Note(
                    user_id=alice.id,
                    title=f"Alice Note {i}",
                    content=f"This is Alice's note #{i}."
                )
            )

        # 5 notes for bob
        for i in range(1, 6):
            notes_to_add.append(
                Note(
                    user_id=bob.id,
                    title=f"Bob Note {i}",
                    content=f"This is Bob's note #{i}."
                )
            )

        # Prepare admin's single note and insert it somewhere in-between
        admin_note = Note(
            user_id=admin.id,
            title="Admin Special Note",
            content="This note belongs to admin."
        )
        # Insert admin note at a random middle position (not at start or end)
        insert_position = random.randint(2, max(2, len(notes_to_add) - 1))
        notes_to_add.insert(insert_position, admin_note)

        # Add and commit all notes
        db.session.add_all(notes_to_add)
        db.session.commit()

        # Print seeded credentials and note mapping for lab users
        print("=== Lab Seed Complete ===")
        print("Users created (plaintext passwords shown for lab use):")
        print("  admin  -> #ThisIsSomeLongAssPasswordThatYouWillNeverGetBecauseItsSoLong123!!!!!")
        print("  bob    -> password")
        print("  alice  -> AliceIsCool1")
        print("")
        print("Notes (id : owner_username : title):")
        for n in Note.query.order_by(Note.id).all():
            print(f"  {n.id} : {n.user.username} : {n.title}")
        print("=========================")
    else:
        print("Notes already exist; skipping note seeding.")


app = create_app()
with app.app_context():
    initialize()

#app.run(host='0.0.0.0', port=5000, debug=False, use_evalex=False)