"""Import statements."""
import os

class BaseConfig(object):
    """Holds default configuration options."""

    DEBUG = True
    TESTING = True
    SECRET_KEY = ""
    SQLALCHEMY_DATABASE_URI = 'sqlite:///bucketlist.db'

class TestingConfig(object):
    pass
