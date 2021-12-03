import os

BASE_PATH = os.path.dirname(os.path.abspath(__file__))


class Config(object):
    """
        Flask Config
    """
    SECRET_KEY = os.urandom(16)
    SESSION_COOKIE_NAME = 'BWASP'
    SQLALCHEMY_DATABASE_URI = f'sqlite:///{os.path.join(BASE_PATH, "databases/TEMP.db")}'
    SQLALCHEMY_BINDS = {
        "CVELIST": f'sqlite:///{os.path.join(BASE_PATH, "databases/CVELIST.db")}',
        "TASK_MANAGER": f'sqlite:///{os.path.join(BASE_PATH, "databases/TASK_MANAGER.db")}'
    }
    SQLALCHEMY_COMMIT_ON_TEARDOWN = True
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    ERROR_404_HELP = False
    SWAGGER_UI_DOC_EXPANSION = 'list'

    def __init__(self):
        pass
        """
        environ_db = os.environ.get("SQLALCHEMY_DATABASE_URI")
        if environ_db:
            self.SQLALCHEMY_BINDS["BWASP"] = environ_db
        """


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
