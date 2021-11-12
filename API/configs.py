import os

BASE_PATH = os.path.dirname(os.path.abspath(__file__))


class Config(object):
    """
        Flask Config
    """
    SECRET_KEY = os.urandom(16)
    SESSION_COOKIE_NAME = 'BWASP'
    # SQLALCHEMY_DATABASE_URI = f'sqlite:///{os.path.join(BASE_PATH, "databases/BWASP.db")}'
    SQLALCHEMY_BINDS = {
        "BWASP": f'sqlite:///{os.path.join(BASE_PATH, "databases/BWASP.db")}',
        "CVE": f'sqlite:///{os.path.join(BASE_PATH, "databases/CVE.db")}'
    }
    SQLALCHEMY_COMMIT_ON_TEARDOWN = True
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    ERROR_404_HELP = False

    def __init__(self):
        pass


class Developments_config(Config):
    """
        Flask Config for Development
    """
    DEBUG = True


class Production_config(Config):
    """
        Flask Config for Production
    """
    pass
