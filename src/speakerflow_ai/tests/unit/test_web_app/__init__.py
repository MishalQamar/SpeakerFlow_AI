from web_app.config import LocalConfig, TestConfig, load_config


def test_load_config_defaults_to_local(monkeypatch):
    """
    GIVEN no APP_ENVIRONMENT is set
    WHEN load_config is called
    THEN LocalConfig is returned
    """
    monkeypatch.delenv("APP_ENVIRONMENT", raising=False)

    config = load_config()

    assert isinstance(config, LocalConfig)


def test_load_config_returns_test_config(monkeypatch):
    """
    GIVEN APP_ENVIRONMENT is set to test
    WHEN load_config is called
    THEN TestConfig is returned
    """
    monkeypatch.setenv("APP_ENVIRONMENT", "test")

    config = load_config()

    assert isinstance(config, TestConfig)
