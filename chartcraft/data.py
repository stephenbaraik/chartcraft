"""
Pandas-like data structures for ChartCraft v1.

Provides Data, Series, and DataFrame classes with simple operations
for creating and manipulating chart data.
"""

from typing import Dict, List, Any, Callable, Optional
import copy
class Data:
    """Simple data structure for charts (pandas-like)."""
    
    def __init__(self, data: Dict[str, List[Any]]):
        """
        Initialize data from a dictionary.
        
        Args:
            data: Dictionary mapping column names to lists of values
        """
        self.data = data
        self.columns = list(data.keys())
    
    def __repr__(self):
        return f"Data(columns={self.columns}, shape={len(self.columns)}x{len(self.data[self.columns[0]]) if self.columns else 0})"
    
    def rename(self, columns: Dict[str, str]) -> 'Data':
        """Rename columns (pandas-like)."""
        new_data = {}
        for col, values in self.data.items():
            new_col = columns.get(col, col)
            new_data[new_col] = values
        return Data(new_data)
    
    def filter(self, **conditions) -> 'Data':
        """Filter data based on column conditions (pandas-like)."""
        filtered_data = {}
        for col, values in self.data.items():
            if col in conditions:
                condition = conditions[col]
                if callable(condition):
                    filtered_data[col] = [v for v in values if condition(v)]
                else:
                    filtered_data[col] = values
            else:
                filtered_data[col] = values
        return Data(filtered_data)
    
    def sort_values(self, column: str, ascending: bool = True) -> 'Data':
        """Sort data by column values (pandas-like)."""
        if column not in self.data:
            raise ValueError(f"Column '{column}' not found")
        
        # Get indices for sorting
        indices = sorted(range(len(self.data[column])), 
                         key=lambda i: self.data[column][i],
                         reverse=not ascending)
        
        # Reorder all columns
        sorted_data = {}
        for col, values in self.data.items():
            sorted_data[col] = [values[i] for i in indices]
        
        return Data(sorted_data)
    
    def head(self, n: int = 5) -> 'Data':
        """Get first n rows (pandas-like)."""
        if not self.columns:
            return self
        
        limited_data = {}
        for col in self.columns:
            limited_data[col] = self.data[col][:n]
        
        return Data(limited_data)
    
    def describe(self) -> Dict[str, Any]:
        """Get basic statistics (pandas-like)."""
        stats = {}
        for col, values in self.data.items():
            if all(isinstance(v, (int, float)) for v in values):
                stats[col] = {
                    'mean': sum(values) / len(values),
                    'min': min(values),
                    'max': max(values),
                    'count': len(values)
                }
        return stats
class Series:
    """Simple series data structure (pandas-like)."""
    
    def __init__(self, data: List[Any], name: str = None):
        """
        Initialize series.
        
        Args:
            data: List of values
            name: Series name
        """
        self.data = data
        self.name = name
    
    def __repr__(self):
        return f"Series(name={self.name}, length={len(self.data)})"
    
    def rename(self, name: str) -> 'Series':
        """Rename series (pandas-like)."""
        return Series(self.data, name)
class DataFrame:
    """Simple DataFrame structure (pandas-like)."""
    
    def __init__(self, data: Dict[str, List[Any]]):
        """
        Initialize DataFrame.
        
        Args:
            data: Dictionary mapping column names to lists of values
        """
        self.data = data
        self.columns = list(data.keys())
    
    def __repr__(self):
        return f"DataFrame(columns={self.columns}, shape={len(self.columns)}x{len(self.data[self.columns[0]]) if self.columns else 0})"
    
    def head(self, n: int = 5) -> 'DataFrame':
        """Get first n rows (pandas-like)."""
        if not self.columns:
            return self
        
        limited_data = {}
        for col in self.columns:
            limited_data[col] = self.data[col][:n]
        
        return DataFrame(limited_data)
    
    def describe(self) -> Dict[str, Any]:
        """Get basic statistics (pandas-like)."""
        return Data(self.data).describe()
# Convenience functions for easy data creation
def from_dict(data: Dict[str, List[Any]]) -> Data:
    """Create Data from dictionary (pandas-like)."""
    return Data(data)

def from_records(records: List[Dict[str, Any]]) -> Data:
    """Create Data from list of records (pandas-like)."""
    if not records:
        return Data({})
    
    # Get all unique keys
    columns = set()
    for record in records:
        columns.update(record.keys())
    
    # Initialize data structure
    data = {col: [] for col in columns}
    
    # Fill data
    for record in records:
        for col in columns:
            data[col].append(record.get(col))
    
    return Data(data)