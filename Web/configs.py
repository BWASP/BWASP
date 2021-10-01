import os

BASE_DIR = os.path.abspath(os.path.abspath(__file__))
DB_FILE = os.path.join(BASE_DIR, 'db.sqlite')


class Config(object):
    SECRET_KEY = os.urandom(16)
    DEBUG = True
    SESSION_COOKIE_NAME = 'BWASP'
    SQLALCHEMY_DATABASE_URI = 'sqlite:///databases/BWASP.db'
    SQLALCHEMY_COMMIT_ON_TEARDOWN = True
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    def __init__(self):
        pass
