# Building Management System

## Description
A modern building management system built with FastAPI.

## Installation
```bash
pip install -r requirements.txt
```

## Usage
```bash
uvicorn src.main:app --reload
```

## Alembic

Initialize Alembic
```bash
# In project root
alembic init migrations
```

Configure alembic.ini
```python
# alembic.ini
sqlalchemy.url = driver://user:pass@localhost/dbname

# For SQLite
sqlalchemy.url = sqlite:///./app.db

# For PostgreSQL
sqlalchemy.url = postgresql://user:password@localhost/dbname
```

Update env.py

```python
# migrations/env.py
from logging.config import fileConfig
from sqlalchemy import engine_from_config
from sqlalchemy import pool
from alembic import context

# Import your models
from sqlmodel import SQLModel as Base  # Adjust import path as needed
target_metadata = Base.metadata
from src.models import *

# other configurations...
```

Create a New Migration

```bash
# Generate migration script
alembic revision --autogenerate -m "initial"
```

