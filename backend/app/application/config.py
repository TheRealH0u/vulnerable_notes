from application.util import generate
import os

basedir = os.path.abspath(os.path.dirname(__file__))

class Config(object):
    SECRET_KEY = 'WLIXBKQrE4uNoBGf5bvdACmKQMNzPjrkwSpqnkwODH0ShIcOW0Zt2y9WspsCxaiL'
    SESSION_COOKIE_HTTPONLY = True
    REMEMBER_COOKIE_HTTPONLY = True
    # SESSION_COOKIE_SAMESITE = 'None'
    DB_USER = os.getenv('POSTGRES_USER', 'user')
    DB_PASSWORD = os.getenv('POSTGRES_PASSWORD', 'password')
    DB_HOST = os.getenv('POSTGRES_HOST', 'localhost')
    DB_PORT = os.getenv('POSTGRES_PORT', '5432')
    DB_NAME = os.getenv('POSTGRES_DB', 'mydatabase')

    SQLALCHEMY_DATABASE_URI = (
        f'postgresql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}'
    )

class ProductionConfig(Config):
    pass

class DevelopmentConfig(Config):
    DEBUG = True

class TestingConfig(Config):
    TESTING = True
