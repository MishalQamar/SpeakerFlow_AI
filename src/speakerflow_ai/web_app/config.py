import os


class BaseConfig:
    DEBUG = False
    TESTING = False
    APP_ENVIRONMENT = "local"


class LocalConfig(BaseConfig):
    DEBUG = True
    APP_ENVIRONMENT = "local"


class TestConfig(BaseConfig):
    DEBUG = True
    TESTING = True
    APP_ENVIRONMENT = "test"


CONFIGS = {
    "local": LocalConfig,
    "test": TestConfig,
}


def load_config():
    return CONFIGS.get(os.getenv("APP_ENVIRONMENT"), LocalConfig)()
