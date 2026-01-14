from application.util import generate
import os

basedir = os.path.abspath(os.path.dirname(__file__))

class Config(object):
    SECRET_KEY = 'WLIXBKQrE4uNoBGf5bvdACmKQMNzPjrkwSpqnkwODH0ShIcOW0Zt2y9WspsCxaiL'
    SESSION_COOKIE_HTTPONLY = True
    REMEMBER_COOKIE_HTTPONLY = True
    # SESSION_COOKIE_SAMESITE = 'None'

    # Prefer DATABASE_URL if provided; otherwise use a local SQLite file.
    # Example for Postgres (optional override):
    #   DATABASE_URL=postgresql://user:password@host:5432/dbname
    DEFAULT_SQLITE_PATH = os.path.join(basedir, 'app.db')
    SQLALCHEMY_DATABASE_URI = os.getenv('DATABASE_URL', f'sqlite:///{DEFAULT_SQLITE_PATH}')
    SQLALCHEMY_TRACK_MODIFICATIONS = False

class ProductionConfig(Config):
    pass

class DevelopmentConfig(Config):
    DEBUG = True

class TestingConfig(Config):
    TESTING = True
