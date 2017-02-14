import settings


class Config(object):
    SQLALCHEMY_DATABASE_URI = settings.DATABASE_URIS.get('Config')
    SQLALCHEMY_TRACK_MODIFICATIONS = True
    PYLTI_CONFIG = settings.PYLTI_CONFIG


class BaseConfig(object):
    DEBUG = False
    TESTING = False
    SQLALCHEMY_DATABASE_URI = settings.DATABASE_URIS.get('BaseConfig')
    SQLALCHEMY_TRACK_MODIFICATIONS = True
    PYLTI_CONFIG = settings.PYLTI_CONFIG


class DevelopmentConfig(BaseConfig):
    DEBUG = True
    TESTING = True
    SQLALCHEMY_DATABASE_URI = settings.DATABASE_URIS.get('DevelopmentConfig')
    # make the warning shut up until Flask-SQLAlchemy v3 comes out
    SQLALCHEMY_TRACK_MODIFICATIONS = True
    PYLTI_CONFIG = settings.PYLTI_CONFIG


class TestingConfig(BaseConfig):
    DEBUG = False
    TESTING = True
    SQLALCHEMY_DATABASE_URI = settings.DATABASE_URIS.get('TestingConfig')
    SQLALCHEMY_TRACK_MODIFICATIONS = True
    PYLTI_CONFIG = settings.PYLTI_CONFIG
