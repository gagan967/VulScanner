from logging.config import fileConfig
import sys
import os

from sqlalchemy import create_engine, pool
from alembic import context

# Add backend folder to sys.path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

# Import your Base and models
from app.database import Base
from app.models import Software, Vulnerability

# Alembic Config object
config = context.config
fileConfig(config.config_file_name)
target_metadata = Base.metadata

def get_url():
    return "postgresql://postgres:5555@localhost/vulnscan"

def run_migrations_offline():
    url = get_url()
    context.configure(
        url=url,
        target_metadata=target_metadata,
        literal_binds=True,
        dialect_opts={"paramstyle": "named"}
    )
    with context.begin_transaction():
        context.run_migrations()

def run_migrations_online():
    connectable = create_engine(get_url(), poolclass=pool.NullPool)
    with connectable.connect() as connection:
        context.configure(connection=connection, target_metadata=target_metadata)
        with context.begin_transaction():
            context.run_migrations()

if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()
