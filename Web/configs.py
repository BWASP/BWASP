import os

BASE_PATH = os.path.dirname(os.path.abspath(__file__))


class Config(object):
    """
        Flask Config
    """
    SECRET_KEY = os.urandom(16)
    SESSION_COOKIE_NAME = 'BWASP'
    SQLALCHEMY_DATABASE_URI = f'sqlite:///{os.path.join(BASE_PATH, "databases/BWASP.db")}'
    """
    SQLALCHEMY_BINDS = {
        # "BWASP": f'sqlite:///{os.path.join(BASE_PATH, "databases/BWASP.db")}',
        # "CHART": f'sqlite:///{os.path.join(BASE_PATH, "databases/CHART.db")}'
    }
    """
    SQLALCHEMY_COMMIT_ON_TEARDOWN = True
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    def __init__(self):
        pass


class DevelopmentsConfig(Config):
    """
        Flask Config for Development
    """
    DEBUG = True


class ProductionConfig(Config):
    """
        Flask Config for Production
    """
    pass
