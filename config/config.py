class BaseConfig(object):
    """Holds default configuration options."""

    DEBUG = False
    TESTING = False
    SECRET_KEY = "F12Zr47j\3yX R~X@H!jmM]Lwf/,?KT"
    SQLALCHEMY_DATABASE_URI = 'sqlite:///bucketlist.db'


class DevelopmentConfig(BaseConfig):
    """Holds development configuration options."""

    DEBUG = True
    TESTING = True
    SECRET_KEY = "F12Zr47j\3yX R~X@H!jmM]Lwf/,?KT"
    SQLALCHEMY_DATABASE_URI = 'sqlite:///bucketlist.db'


class TestingConfig(BaseConfig):
    """Holds test configuration options."""

    DEBUG = True
    TESTING = True
    SECRET_KEY = "F12Zr47j\3yX R~X@H!jmM]Lwf/,?KT"
    SQLALCHEMY_DATABASE_URI = 'sqlite:///memory'


class ProductionConfig(BaseConfig):
    """Holds production configuration options."""

    DEBUG = False
    TESTING = False
    SECRET_KEY = "F12Zr47j\3yX R~X@H!jmM]Lwf/,?KT"
    SQLALCHEMY_DATABASE_URI = 'sqlite:///bucketlist.db'

config = {
    'development': DevelopmentConfig,
    'testing': TestingConfig,
    'production': ProductionConfig
}
