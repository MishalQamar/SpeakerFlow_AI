from collections.abc import Generator

import pytest
from database.speaking_request_db import SpeakingRequestBase
from sqlalchemy import Engine, create_engine
from sqlalchemy.orm import Session, sessionmaker
from web_app.config import load_config


@pytest.fixture(scope="session")
def database_engine() -> Generator[Engine, None, None]:
    engine = create_engine(load_config().SQLALCHEMY_DATABASE_URI, echo=False)
    yield engine
    engine.dispose()


@pytest.fixture
def database_session(database_engine: Engine) -> Generator[Session, None, None]:
    SpeakingRequestBase.metadata.create_all(bind=database_engine)

    session_factory = sessionmaker(bind=database_engine)
    session = session_factory()

    try:
        yield session
    finally:
        session.rollback()
        session.close()
        SpeakingRequestBase.metadata.drop_all(bind=database_engine)
