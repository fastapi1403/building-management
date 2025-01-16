Installation and Initial Setup:
```bash
# Install alembic
pip install alembic

# Initialize alembic in your project
alembic init alembic
```

Update your alembic.ini file:
```ini
# alembic.ini
[alembic]
script_location = alembic
sqlalchemy.url = postgresql://user:password@localhost:5432/building_management
# Replace with your actual database URL
```

Modify alembic/env.py to use your SQLAlchemy models:
```python
# alembic/env.py
from logging.config import fileConfig
from sqlalchemy import engine_from_config
from sqlalchemy import pool
from sqlmodel import SQLModel
from alembic import context
from app.core.config import settings
from app.models import *  # Import all your SQLModel models here

# This is the Alembic Config object
config = context.config

# Interpret the config file for Python logging.
fileConfig(config.config_file_name)

# Set the database URL from your settings
config.set_main_option("sqlalchemy.url", settings.DATABASE_URL)

# Add your models' MetaData object here
target_metadata = SQLModel.metadata

# other values from the config, defined by the needs of env.py,
# can be acquired:
# ... rest of the default env.py content ...
```

To create a new migration:
```bash
# Create a new migration
alembic revision --autogenerate -m "create initial tables"
```

This will create a file in alembic/versions/ like:
```python
# alembic/versions/xxxxxxxxxxxx_create_initial_tables.py
from alembic import op
import sqlalchemy as sa

def upgrade():
    # Migration code goes here
    op.create_table(
        'buildings',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('name', sa.String(), nullable=False),
        sa.Column('created_at', sa.DateTime(), nullable=False),
        sa.Column('updated_at', sa.DateTime(), nullable=False),
        sa.PrimaryKeyConstraint('id')
    )

def downgrade():
    # Rollback code goes here
    op.drop_table('buildings')
```

Apply Migrations:
```bash
# Apply all pending migrations
alembic upgrade head

# Apply specific migration
alembic upgrade +1  # Apply next migration
alembic upgrade <revision_id>  # Apply specific revision

# Rollback migrations
alembic downgrade -1  # Rollback one migration
alembic downgrade <revision_id>  # Rollback to specific revision
```

Common Alembic Commands:
```bash
# Show current revision
alembic current

# Show migration history
alembic history

# Create a new migration (with autogenerate)
alembic revision --autogenerate -m "add new column"

# Create a new empty migration
alembic revision -m "create new table"

# Mark a migration as complete without running it
alembic stamp <revision_id>
```

Migration Tips:
```python
# Adding a column
op.add_column('table_name', sa.Column('column_name', sa.String()))

# Removing a column
op.drop_column('table_name', 'column_name')

# Adding an index
op.create_index('index_name', 'table_name', ['column_name'])

# Adding a foreign key
op.create_foreign_key(
    'fk_name', 'source_table', 'target_table',
    ['source_column'], ['target_column']
)
```

Handling Data Migrations:
```python
def upgrade():
    # Get connection
    connection = op.get_bind()
    
    # Execute data migration
    connection.execute(
        """
        UPDATE buildings 
        SET updated_by = 'fastapi1403'
        WHERE updated_by IS NULL
        """
    )
```

Error Handling:
```python
from alembic import op
import sqlalchemy as sa
from sqlalchemy.exc import SQLAlchemyError

def upgrade():
    try:
        # Your migration code here
        op.create_table(...)
    except SQLAlchemyError as e:
        print(f"Error during migration: {str(e)}")
        raise
```