import os

BASE_PATH = os.path.dirname(os.path.abspath(__file__))


class Config(object):
    """
        Flask Config
    """
    SECRET_KEY = os.urandom(16)
    SESSION_COOKIE_NAME = 'BWASP'
    SQLALCHEMY_DATABASE_URI = "mysql+pymysql://root:BWASPENGINE1234@bwasp-database-1/BWASP?charset=utf8"
    SQLALCHEMY_BINDS = {
        "BWASP": "mysql+pymysql://root:BWASPENGINE1234@bwasp-database-1/BWASP?charset=utf8",
        "JOB": f'sqlite:///{os.path.join(BASE_PATH, "databases/JOB.db")}',
        "CVE": f'sqlite:///{os.path.join(BASE_PATH, "databases/CVE.db")}'
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
