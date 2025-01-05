from typing import List
from alembic import command
from alembic.config import Config
from src.core.config import settings

def run_migrations() -
    """Run alembic migrations."""
    alembic_cfg = Config("alembic.ini")
    command.upgrade(alembic_cfg, "head")

def create_migration(message: str) -
    """Create new migration."""
    alembic_cfg = Config("alembic.ini")
    command.revision(alembic_cfg, message=message, autogenerate=True)
