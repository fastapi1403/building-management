from sqlalchemy import event
from sqlalchemy.engine import Engine
from datetime import datetime
from src.core.config import settings

@event.listens_for(Engine, "connect")
def set_sqlite_pragma(dbapi_connection, connection_record):
    """Set SQLite pragmas on connect."""
    cursor = dbapi_connection.cursor()
    cursor.execute("PRAGMA foreign_keys=ON")
    cursor.close()

@event.listens_for(Engine, "before_cursor_execute")
def add_query_markers(conn, cursor, statement, parameters, context, executemany):
    """Add query markers for monitoring."""
    conn.info.setdefault('query_start_time', []).append(datetime.utcnow())

@event.listens_for(Engine, "after_cursor_execute")
def log_query_timing(conn, cursor, statement, parameters, context, executemany):
    """Log query execution time."""
    total = datetime.utcnow() - conn.info['query_start_time'].pop(-1)
    if total.total_seconds()   # Log slow queries
        print(f"Long running query detected: {total.total_seconds():.2f} seconds")
