"""
CSV / TSV connector — zero dependencies, auto type detection.
"""

from __future__ import annotations
import csv
import os
from pathlib import Path
from typing import Dict, List, Any, Optional


def _coerce(value: str) -> Any:
    """Try to coerce a string to int, float, or leave as str."""
    v = value.strip()
    if v == "" or v.lower() in ("null", "none", "na", "n/a"):
        return None
    try:
        return int(v)
    except ValueError:
        pass
    try:
        return float(v)
    except ValueError:
        pass
    return v


class CSVConnector:
    def __init__(self, path: str):
        self.path = Path(path)
        self._cache: Dict[str, List[Dict[str, Any]]] = {}
        self._load()

    def _load(self):
        if self.path.is_dir():
            for f in self.path.glob("*.csv"):
                self._read_file(f)
            for f in self.path.glob("*.tsv"):
                self._read_file(f, delimiter="\t")
        elif self.path.suffix.lower() == ".tsv":
            self._read_file(self.path, delimiter="\t")
        else:
            self._read_file(self.path)

    def _read_file(self, path: Path, delimiter: str = ","):
        with open(path, newline="", encoding="utf-8-sig") as f:
            reader = csv.DictReader(f, delimiter=delimiter)
            rows = [
                {k: _coerce(v) for k, v in row.items() if k}
                for row in reader
            ]
        table_name = path.stem
        self._cache[table_name] = rows

    def tables(self) -> List[str]:
        return list(self._cache.keys())

    def query(self, table: str) -> List[Dict[str, Any]]:
        if table not in self._cache:
            raise KeyError(f"Table '{table}' not found. Available: {self.tables()}")
        return self._cache[table]

    def query_as_columns(self, table: str) -> Dict[str, List[Any]]:
        rows = self.query(table)
        if not rows:
            return {}
        cols = list(rows[0].keys())
        return {col: [row.get(col) for row in rows] for col in cols}

    def reload(self):
        """Re-read files from disk."""
        self._cache.clear()
        self._load()

    def __repr__(self):
        return f"CSVConnector({self.path!r}, tables={self.tables()})"
