"""
SQL connector — SQLite (stdlib) with optional SQLAlchemy for Postgres/MySQL/MSSQL.
"""

from __future__ import annotations
from typing import List, Dict, Any, Optional


class SQLConnector:
    def __init__(self, connection_string: str):
        self.connection_string = connection_string
        self._engine = None
        self._sqlite_conn = None
        self._use_sqlalchemy = not connection_string.startswith("sqlite:///")
        self._connect()

    def _connect(self):
        if self._use_sqlalchemy:
            try:
                import sqlalchemy
                self._engine = sqlalchemy.create_engine(self.connection_string)
            except ImportError:
                raise ImportError(
                    "sqlalchemy is required for non-SQLite databases. "
                    "Install it with: pip install sqlalchemy"
                )
        else:
            import sqlite3
            path = self.connection_string.replace("sqlite:///", "")
            self._sqlite_conn = sqlite3.connect(path, check_same_thread=False)
            self._sqlite_conn.row_factory = sqlite3.Row

    # ------------------------------------------------------------------
    # Query methods
    # ------------------------------------------------------------------

    def query(self, sql: str, params=None) -> List[tuple]:
        """Execute SQL, return list of tuples."""
        if self._use_sqlalchemy:
            import sqlalchemy
            with self._engine.connect() as conn:
                result = conn.execute(sqlalchemy.text(sql), params or {})
                return [tuple(row) for row in result]
        else:
            cur = self._sqlite_conn.cursor()
            cur.execute(sql, params or [])
            return [tuple(row) for row in cur.fetchall()]

    def query_dict(self, sql: str, params=None) -> List[Dict[str, Any]]:
        """Execute SQL, return list of dicts."""
        if self._use_sqlalchemy:
            import sqlalchemy
            with self._engine.connect() as conn:
                result = conn.execute(sqlalchemy.text(sql), params or {})
                keys = list(result.keys())
                return [dict(zip(keys, row)) for row in result]
        else:
            cur = self._sqlite_conn.cursor()
            cur.execute(sql, params or [])
            rows = cur.fetchall()
            if not rows:
                return []
            keys = [desc[0] for desc in cur.description]
            return [dict(zip(keys, row)) for row in rows]

    def query_df(self, sql: str, params=None):
        """Execute SQL, return pandas DataFrame."""
        try:
            import pandas as pd
        except ImportError:
            raise ImportError("pandas is required for query_df(). pip install pandas")
        if self._use_sqlalchemy:
            return pd.read_sql(sql, self._engine, params=params)
        else:
            import pandas as pd
            return pd.read_sql_query(sql, self._sqlite_conn, params=params)

    def execute(self, sql: str, params=None) -> None:
        """Execute a non-SELECT statement (INSERT, UPDATE, CREATE, etc.)."""
        if self._use_sqlalchemy:
            import sqlalchemy
            with self._engine.begin() as conn:
                conn.execute(sqlalchemy.text(sql), params or {})
        else:
            cur = self._sqlite_conn.cursor()
            cur.execute(sql, params or [])
            self._sqlite_conn.commit()

    def tables(self) -> List[str]:
        """Return list of all table names."""
        if self._use_sqlalchemy:
            import sqlalchemy
            insp = sqlalchemy.inspect(self._engine)
            return insp.get_table_names()
        else:
            rows = self.query("SELECT name FROM sqlite_master WHERE type='table' ORDER BY name")
            return [r[0] for r in rows]

    def schema(self, table: str) -> List[Dict[str, str]]:
        """Return column names and types for a table."""
        if self._use_sqlalchemy:
            import sqlalchemy
            insp = sqlalchemy.inspect(self._engine)
            cols = insp.get_columns(table)
            return [{"name": c["name"], "type": str(c["type"])} for c in cols]
        else:
            rows = self.query(f"PRAGMA table_info('{table}')")
            return [{"name": r[1], "type": r[2]} for r in rows]

    def close(self):
        if self._sqlite_conn:
            self._sqlite_conn.close()
        if self._engine:
            self._engine.dispose()

    def __repr__(self):
        return f"SQLConnector({self.connection_string!r})"
