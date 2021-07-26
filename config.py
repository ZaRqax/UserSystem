import os

class Config(object):
    DEBUG= True
    CSRF = True
    SECRET_KEY='DFFDSFSD'
    SQLALCHEMY_DATABASE_URI = 'postgesql://postgres:sfml@localhost/users'

class ProductionConfig(Config):
    DEBUG = False


class StagingConfig(Config):
    DEVELOPMENT = True
    DEBUG = True


class DevelopmentConfig(Config):
    DEVELOPMENT = True
    DEBUG = True


class TestingConfig(Config):
    TESTING = True