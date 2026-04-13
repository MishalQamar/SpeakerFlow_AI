import os


class BaseConfig:
    DEBUG = False
    TESTING = False
    APP_ENVIRONMENT = "local"
    SQLALCHEMY_DATABASE_URI = None


class LocalConfig(BaseConfig):
    DEBUG = True
    APP_ENVIRONMENT = "local"
    SQLALCHEMY_DATABASE_URI = "postgresql+psycopg://app:speakerflow@localhost:5432/speakerflow"


class TestConfig(BaseConfig):
    DEBUG = True
    TESTING = True
    APP_ENVIRONMENT = "test"
    SQLALCHEMY_DATABASE_URI = "postgresql+psycopg://app:speakerflow@localhost:5432/speakerflow_test"


CONFIGS = {
    "local": LocalConfig,
    "test": TestConfig,
}


def load_config():
    return CONFIGS.get(os.getenv("APP_ENVIRONMENT"), LocalConfig)()
