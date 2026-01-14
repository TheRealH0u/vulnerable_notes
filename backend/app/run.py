from application import create_app
from application.models import db
import os

basedir = os.path.abspath(os.path.dirname(__file__))

app = create_app()

# Ensure tables exist (especially for SQLite default).
try:
    with app.app_context():
        db.create_all()
except Exception:
    pass

# If running directly (not via gunicorn), you could enable this:
# if __name__ == '__main__':
#     app.run(host='0.0.0.0', port=8081)
