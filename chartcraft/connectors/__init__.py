from .sql import SQLConnector
from .csv_connector import CSVConnector
from .api import APIConnector


def connect_sql(connection_string: str) -> SQLConnector:
    """Connect to a SQL database. Supports sqlite:/// and SQLAlchemy URIs."""
    return SQLConnector(connection_string)


def connect_csv(path: str) -> CSVConnector:
    """Connect to a CSV/TSV file or directory of CSV files."""
    return CSVConnector(path)


def connect_api(base_url: str, headers: dict = None) -> APIConnector:
    """Connect to a REST API."""
    return APIConnector(base_url, headers=headers)
