import os
from dotenv import load_dotenv

import sys
import pathlib
from logging.config import fileConfig

from sqlalchemy import engine_from_config, MetaData, Table
from sqlalchemy import pool

from alembic import context

# this is the Alembic Config object, which provides
# access to the values within the .ini file in use.
config = context.config
sys.path.append(os.getcwd())

# Interpret the config file for Python logging.
# This line sets up loggers basically.
if config.config_file_name is not None:
    fileConfig(config.config_file_name)


def combine_metadata(*args):
    meta = MetaData()
    for metadata_temp in args:
        for metadata in metadata_temp:
            for t in metadata.tables.values():
                t.tometadata(meta)
    return meta


meta_list = list()

for file in [file for file in os.listdir(str(pathlib.Path(__file__).parent.parent) + "/models/") if
             file != '__pycache__' and file != '__init__.py']:
    p, m = file.rsplit('.', 1)
    module_in_file = __import__("models." + str(p))
    files_module_in_directory = getattr(module_in_file, p)

    new_model = []
    for item in files_module_in_directory.__dict__:
        try:
            files_module = getattr(files_module_in_directory, item)
            if isinstance(files_module, Table) is True:
                meta_list.append(files_module.metadata)
        except Exception as e:
            print(e)

target_metadata = combine_metadata(meta_list)
# other values from the config, defined by the needs of env.py,alembic revision -m "create account table"
# can be acquired:
# my_important_option = config.get_main_option("my_important_option")
# ... etc.


def run_migrations_offline() -> None:
    """Run migrations in 'offline' mode.

    This configures the context with just a URL
    and not an Engine, though an Engine is acceptable
    here as well.  By skipping the Engine creation
    we don't even need a DBAPI to be available.

    Calls to context.execute() here emit the given string to the
    script output.

    """
    load_dotenv()
    url = f"{os.getenv('DB_TYPE')}://{os.getenv('DB_USER')}:{os.getenv('DB_PASS')}@" \
          f"{os.getenv('DB_HOST')}:{os.getenv('DB_PORT')}/{os.getenv('DB_NAME')}"
    context.configure(
        url=url,
        target_metadata=target_metadata,
        literal_binds=True,
        dialect_opts={"paramstyle": "named"},
    )

    with context.begin_transaction():
        context.run_migrations()


def run_migrations_online() -> None:
    """Run migrations in 'online' mode.

    In this scenario we need to create an Engine
    and associate a connection with the context.

    """
    load_dotenv()
    url = f"{os.getenv('DB_TYPE')}://{os.getenv('DB_USER')}:{os.getenv('DB_PASS')}@" \
          f"{os.getenv('DB_HOST')}:{os.getenv('DB_PORT')}/{os.getenv('DB_NAME')}"
    print(url)

    config_dict = dict()
    config_dict['sqlalchemy.url'] = url

    connectable = engine_from_config(
        config_dict,
        prefix="sqlalchemy.",
        poolclass=pool.NullPool,
    )

    with connectable.connect() as connection:
        context.configure(
            connection=connection, target_metadata=target_metadata
        )

        with context.begin_transaction():
            context.run_migrations()


if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()
