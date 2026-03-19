"""
JSON serialiser that handles numpy/pandas types gracefully.
"""

import json
import datetime
from typing import Any


class CCEncoder(json.JSONEncoder):
    def default(self, obj):
        # numpy scalars
        try:
            import numpy as np
            if isinstance(obj, (np.integer,)):
                return int(obj)
            if isinstance(obj, (np.floating,)):
                return float(obj)
            if isinstance(obj, np.ndarray):
                return obj.tolist()
        except ImportError:
            pass

        # pandas NA / NaT
        try:
            import pandas as pd
            if pd.isna(obj):
                return None
        except (ImportError, TypeError, ValueError):
            pass

        # dates
        if isinstance(obj, (datetime.date, datetime.datetime)):
            return obj.isoformat()

        return super().default(obj)


def dumps(obj: Any, **kwargs) -> str:
    return json.dumps(obj, cls=CCEncoder, **kwargs)


def loads(s: str) -> Any:
    return json.loads(s)
