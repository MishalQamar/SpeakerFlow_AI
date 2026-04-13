from collections.abc import Generator
from pathlib import Path

import pytest
from alembic import command
from alembic.config import Config
from sqlalchemy import Engine, create_engine, text
from sqlalchemy.orm import Session, sessionmaker

from speakerflow_ai.web_app.config import load_config

# tests/conftest.py -> src/speakerflow_ai/tests -> src/speakerflow_ai -> src -> service root
_SERVICE_ROOT = Path(__file__).resolve().parent.parent.parent.parent
ALEMBIC_INI_PATH = _SERVICE_ROOT / "alembic.ini"

alembic_config = Config(str(ALEMBIC_INI_PATH))


@pytest.fixture(scope="session")
def database_engine() -> Generator[Engine, None, None]:
    engine = create_engine(load_config().SQLALCHEMY_DATABASE_URI, echo=False)
    command.upgrade(alembic_config, "head")
    yield engine
    command.downgrade(alembic_config, "base")
    engine.dispose()


@pytest.fixture
def database_session(database_engine: Engine) -> Generator[Session, None, None]:
    session_factory = sessionmaker(bind=database_engine)
    session = session_factory()

    try:
        yield session
    finally:
        session.rollback()
        session.close()
        with database_engine.begin() as conn:
            conn.execute(text("TRUNCATE TABLE speaking_requests RESTART IDENTITY"))
