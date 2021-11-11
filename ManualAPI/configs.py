import os

BASE_PATH = os.path.dirname(os.path.abspath(__file__))


class Config(object):
    """
        Flask Config
    """
    SECRET_KEY = os.urandom(16)
    SESSION_COOKIE_NAME = 'BWASP'

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
