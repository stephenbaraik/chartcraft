"""
Dashboard class for ChartCraft v1.

Simple dashboard creation with flexible layout options.
"""

from typing import List, Dict, Any
from .charts import Chart
class Dashboard:
    """Simple dashboard for organizing charts."""
    
    def __init__(self, title: str = "", charts: List[Chart] = None, 
                 layout: str = "grid", columns: int = 2, spacing: int = 20):
        """
        Initialize dashboard.
        
        Args:
            title: Dashboard title
            charts: List of charts to display
            layout: Layout type ("grid", "vertical", "horizontal")
            columns: Number of columns for grid layout
            spacing: Spacing between charts
        """
        self.title = title
        self.charts = charts or []
        self.layout = layout
        self.columns = columns
        self.spacing = spacing
    
    def __repr__(self):
        return f"Dashboard(title={self.title}, charts={len(self.charts)}, layout={self.layout})"
    
    def add_chart(self, chart: Chart):
        """Add a chart to the dashboard."""
        self.charts.append(chart)
    
    def to_spec(self) -> Dict[str, Any]:
        """Convert dashboard to specification dictionary."""
        return {
            'title': self.title,
            'layout': self.layout,
            'columns': self.columns,
            'spacing': self.spacing,
            'charts': [chart.to_spec() for chart in self.charts]
        }