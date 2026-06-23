"""
Simple chart creation functions for ChartCraft v1.

Provides basic chart types with full customization options.
No presets - everything is customizable.
"""

from typing import Dict, List, Any, Optional
from .data import Data
class Chart:
    """Base chart class."""
    
    def __init__(self, data: Data, title: str = "", **kwargs):
        """
        Initialize chart.
        
        Args:
            data: Data object containing chart data
            title: Chart title
            **kwargs: Chart customization options
        """
        self.data = data
        self.title = title
        self.options = kwargs
    
    def to_spec(self) -> Dict[str, Any]:
        """Convert chart to specification dictionary."""
        return {
            'title': self.title,
            'data': self.data.data,
            'options': self.options
        }
# Chart creation functions
def bar(data: Data, title: str = "", **kwargs) -> Chart:
    """Create a bar chart."""
    return Chart(data, title, chart_type="bar", **kwargs)

def line(data: Data, title: str = "", **kwargs) -> Chart:
    """Create a line chart."""
    return Chart(data, title, chart_type="line", **kwargs)

def area(data: Data, title: str = "", **kwargs) -> Chart:
    """Create an area chart."""
    return Chart(data, title, chart_type="area", **kwargs)

def pie(data: Data, title: str = "", **kwargs) -> Chart:
    """Create a pie chart."""
    return Chart(data, title, chart_type="pie", **kwargs)

def donut(data: Data, title: str = "", **kwargs) -> Chart:
    """Create a donut chart."""
    return Chart(data, title, chart_type="donut", **kwargs)

def scatter(data: Data, title: str = "", **kwargs) -> Chart:
    """Create a scatter chart."""
    return Chart(data, title, chart_type="scatter", **kwargs)

def bubble(data: Data, title: str = "", **kwargs) -> Chart:
    """Create a bubble chart."""
    return Chart(data, title, chart_type="bubble", **kwargs)

def histogram(data: Data, title: str = "", **kwargs) -> Chart:
    """Create a histogram."""
    return Chart(data, title, chart_type="histogram", **kwargs)

def boxplot(data: Data, title: str = "", **kwargs) -> Chart:
    """Create a box plot."""
    return Chart(data, title, chart_type="boxplot", **kwargs)

def heatmap(data: Data, title: str = "", **kwargs) -> Chart:
    """Create a heatmap."""
    return Chart(data, title, chart_type="heatmap", **kwargs)

def radar(data: Data, title: str = "", **kwargs) -> Chart:
    """Create a radar chart."""
    return Chart(data, title, chart_type="radar", **kwargs)

def waterfall(data: Data, title: str = "", **kwargs) -> Chart:
    """Create a waterfall chart."""
    return Chart(data, title, chart_type="waterfall", **kwargs)

def gauge(data: Data, title: str = "", **kwargs) -> Chart:
    """Create a gauge chart."""
    return Chart(data, title, chart_type="gauge", **kwargs)

def candlestick(data: Data, title: str = "", **kwargs) -> Chart:
    """Create a candlestick chart."""
    return Chart(data, title, chart_type="candlestick", **kwargs)

def table(data: Data, title: str = "", **kwargs) -> Chart:
    """Create a table."""
    return Chart(data, title, chart_type="table", **kwargs)

def metric(data: Data, title: str = "", **kwargs) -> Chart:
    """Create a metric chart."""
    return Chart(data, title, chart_type="metric", **kwargs)

def sankey(data: Data, title: str = "", **kwargs) -> Chart:
    """Create a Sankey chart."""
    return Chart(data, title, chart_type="sankey", **kwargs)

def treemap(data: Data, title: str = "", **kwargs) -> Chart:
    """Create a treemap."""
    return Chart(data, title, chart_type="treemap", **kwargs)

def funnel(data: Data, title: str = "", **kwargs) -> Chart:
    """Create a funnel chart."""
    return Chart(data, title, chart_type="funnel", **kwargs)