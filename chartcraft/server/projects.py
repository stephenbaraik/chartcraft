"""
Builder project persistence — saves/loads named builder states using stdlib sqlite3.
Database is created automatically at chartcraft/builder/projects.db.
"""

from __future__ import annotations
import json
import sqlite3
import time
from pathlib import Path
from typing import Any, Dict, List, Optional

DB_PATH = Path(__file__).parent.parent / "builder" / "projects.db"


def _conn() -> sqlite3.Connection:
    DB_PATH.parent.mkdir(parents=True, exist_ok=True)
    con = sqlite3.connect(str(DB_PATH))
    con.row_factory = sqlite3.Row
    con.execute("""
        CREATE TABLE IF NOT EXISTS projects (
            id          TEXT PRIMARY KEY,
            name        TEXT NOT NULL,
            state_json  TEXT NOT NULL,
            updated_at  REAL NOT NULL
        )
    """)
    con.commit()
    return con


def list_projects() -> List[Dict]:
    with _conn() as con:
        rows = con.execute(
            "SELECT id, name, updated_at FROM projects ORDER BY updated_at DESC"
        ).fetchall()
    return [{"id": r["id"], "name": r["name"], "updated_at": r["updated_at"]} for r in rows]


def get_project(project_id: str) -> Optional[Dict]:
    with _conn() as con:
        row = con.execute(
            "SELECT id, name, state_json, updated_at FROM projects WHERE id = ?",
            (project_id,)
        ).fetchone()
    if row is None:
        return None
    return {
        "id":         row["id"],
        "name":       row["name"],
        "state":      json.loads(row["state_json"]),
        "updated_at": row["updated_at"],
    }


def save_project(project_id: str, name: str, state: Dict) -> Dict:
    now = time.time()
    state_json = json.dumps(state)
    with _conn() as con:
        con.execute("""
            INSERT INTO projects (id, name, state_json, updated_at)
            VALUES (?, ?, ?, ?)
            ON CONFLICT(id) DO UPDATE SET
                name       = excluded.name,
                state_json = excluded.state_json,
                updated_at = excluded.updated_at
        """, (project_id, name, state_json, now))
        con.commit()
    return {"id": project_id, "name": name, "updated_at": now}


def delete_project(project_id: str) -> bool:
    with _conn() as con:
        cur = con.execute("DELETE FROM projects WHERE id = ?", (project_id,))
        con.commit()
    return cur.rowcount > 0
