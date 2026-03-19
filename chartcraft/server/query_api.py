"""
Query API — executes SQL against registered connectors, serves schema,
and manages the connector registry (persisted as JSON alongside projects.db).
"""

from __future__ import annotations
import json
import traceback
from pathlib import Path
from typing import Any, Dict, List, Optional

REGISTRY_PATH = Path(__file__).parent.parent / "builder" / "connectors.json"


# ─── Connector registry ────────────────────────────────────────────────────

def _load_registry() -> Dict[str, Dict]:
    if REGISTRY_PATH.exists():
        try:
            return json.loads(REGISTRY_PATH.read_text())
        except Exception:
            pass
    return {}


def _save_registry(reg: Dict):
    REGISTRY_PATH.parent.mkdir(parents=True, exist_ok=True)
    REGISTRY_PATH.write_text(json.dumps(reg, indent=2))


def list_connectors() -> List[Dict]:
    reg = _load_registry()
    return [{"id": k, **v} for k, v in reg.items()]


def get_connector_str(conn_id: str) -> Optional[str]:
    return _load_registry().get(conn_id, {}).get("conn_str")


def save_connector(conn_id: str, name: str, conn_str: str) -> Dict:
    reg = _load_registry()
    reg[conn_id] = {"name": name, "conn_str": conn_str}
    _save_registry(reg)
    return {"id": conn_id, "name": name, "conn_str": conn_str}


def delete_connector(conn_id: str) -> bool:
    reg = _load_registry()
    if conn_id not in reg:
        return False
    del reg[conn_id]
    _save_registry(reg)
    return True


# ─── Query execution ───────────────────────────────────────────────────────

def _make_sql_connector(conn_str: str):
    from chartcraft.connectors.sql import SQLConnector
    return SQLConnector(conn_str)


def execute_query(conn_str: str, sql: str, limit: int = 500) -> Dict[str, Any]:
    """
    Execute a SQL query against conn_str and return:
      { columns: [...], rows: [[...], ...], row_count: N }
    or { error: "..." } on failure.
    """
    try:
        conn = _make_sql_connector(conn_str)
        rows_raw = conn.query(sql)
        conn.close()

        if not rows_raw:
            return {"columns": [], "rows": [], "row_count": 0}

        # Get column names from the first row if it's a dict; else use positional
        if isinstance(rows_raw[0], dict):
            columns = list(rows_raw[0].keys())
            rows = [[r.get(c) for c in columns] for r in rows_raw[:limit]]
        else:
            # tuple rows — get column names via query_dict
            conn2 = _make_sql_connector(conn_str)
            dict_rows = conn2.query_dict(sql)
            conn2.close()
            if dict_rows:
                columns = list(dict_rows[0].keys())
                rows = [[r.get(c) for c in columns] for r in dict_rows[:limit]]
            else:
                columns = [f"col{i}" for i in range(len(rows_raw[0]))]
                rows = [list(r) for r in rows_raw[:limit]]

        return {
            "columns": columns,
            "rows": rows,
            "row_count": len(rows_raw),
            "truncated": len(rows_raw) > limit,
        }
    except Exception as e:
        return {"error": str(e), "trace": traceback.format_exc()}


def get_schema(conn_str: str) -> Dict[str, Any]:
    """
    Return tables + columns for the database:
      { tables: [{ name, columns: [{ name, type }] }] }
    """
    try:
        conn = _make_sql_connector(conn_str)
        table_names = conn.tables()
        tables = []
        for t in table_names:
            try:
                cols = conn.schema(t)
            except Exception:
                cols = []
            tables.append({"name": t, "columns": cols})
        conn.close()
        return {"tables": tables}
    except Exception as e:
        return {"error": str(e)}
