import os

BASE_PATH = os.path.dirname(os.path.abspath(__file__))


class Config(object):
    SECRET_KEY = os.urandom(16)
    SESSION_COOKIE_NAME = 'BWASP'
    SQLALCHEMY_DATABASE_URI = f'sqlite:///{os.path.join(BASE_PATH, "databases/BWASP.db")}'
    SQLALCHEMY_COMMIT_ON_TEARDOWN = True
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    def __init__(self):
        pass


class DevelopmentsConfig(Config):
    DEBUG = True
    SQLALCHEMY_DATABASE_URI = f'sqlite:///{os.path.join(BASE_PATH,"databases/CHART.db")}'
    SQLALCHEMY_COMMIT_ON_TEARDOWN = True
    SQLALCHEMY_TRACK_MODIFICATIONS = False

