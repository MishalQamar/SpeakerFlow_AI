from logging.config import fileConfig

from alembic import context
from sqlalchemy import create_engine, pool

from database.speaking_request_db import SpeakingRequestBase
from speakerflow_ai.web_app.config import load_config

config = context.config

if config.config_file_name is not None:
    fileConfig(config.config_file_name)

app_config = load_config()
config.set_main_option("sqlalchemy.url", app_config.SQLALCHEMY_DATABASE_URI)

target_metadata = SpeakingRequestBase.metadata


def run_migrations_offline() -> None:
    url = config.get_main_option("sqlalchemy.url")
    context.configure(
        url=url,
        target_metadata=target_metadata,
        literal_binds=True,
        compare_type=True,
    )

    with context.begin_transaction():
        context.run_migrations()


def run_migrations_online() -> None:
    url = config.get_main_option("sqlalchemy.url")
    connectable = create_engine(url, poolclass=pool.NullPool)

    with connectable.connect() as connection:
        context.configure(
            connection=connection,
            target_metadata=target_metadata,
            compare_type=True,
        )

        with context.begin_transaction():
            context.run_migrations()


if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()
