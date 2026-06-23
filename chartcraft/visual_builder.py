"""
Visual building syntax for ChartCraft v1.

Simple, intuitive syntax for building charts and dashboards
with full customization (no presets).
"""

from typing import Dict, List, Any, Union
from .data import Data
from .charts import Chart
class VisualBuilder:
    """
    Simple visual builder for creating charts and dashboards.
    
    This class provides an easy-to-use API for building charts
    and dashboards with full customization.
    """
    
    def __init__(self):
        self.charts = []
        self.title = ""
        self.layout = "grid"
        self.columns = 2
        self.spacing = 20
    
    def set_title(self, title: str):
        """Set dashboard title."""
        self.title = title
        return self
    
    def set_layout(self, layout: str, columns: int = 2, spacing: int = 20):
        """
        Set dashboard layout.
        
        Args:
            layout: Layout type ("grid", "vertical", "horizontal")
            columns: Number of columns for grid layout
            spacing: Spacing between charts
        """
        self.layout = layout
        self.columns = columns
        self.spacing = spacing
        return self
    
    def add_bar(self, data: Data, title: str = "", **kwargs) -> 'VisualBuilder':
        """Add a bar chart."""
        chart = Chart(data, title, chart_type="bar", **kwargs)
        self.charts.append(chart)
        return self
    
    def add_line(self, data: Data, title: str = "", **kwargs) -> 'VisualBuilder':
        """Add a line chart."""
        chart = Chart(data, title, chart_type="line", **kwargs)
        self.charts.append(chart)
        return self
    
    def add_area(self, data: Data, title: str = "", **kwargs) -> 'VisualBuilder':
        """Add an area chart."""
        chart = Chart(data, title, chart_type="area", **kwargs)
        self.charts.append(chart)
        return self
    
    def add_pie(self, data: Data, title: str = "", **kwargs) -> 'VisualBuilder':
        """Add a pie chart."""
        chart = Chart(data, title, chart_type="pie", **kwargs)
        self.charts.append(chart)
        return self
    
    def add_scatter(self, data: Data, title: str = "", **kwargs) -> 'VisualBuilder':
        """Add a scatter chart."""
        chart = Chart(data, title, chart_type="scatter", **kwargs)
        self.charts.append(chart)
        return self
    
    def add_histogram(self, data: Data, title: str = "", **kwargs) -> 'VisualBuilder':
        """Add a histogram."""
        chart = Chart(data, title, chart_type="histogram", **kwargs)
        self.charts.append(chart)
        return self
    
    def add_chart(self, chart_type: str, data: Data, title: str = "", **kwargs) -> 'VisualBuilder':
        """
        Add a chart of any type (flexible).
        
        Args:
            chart_type: Type of chart ("bar", "line", "area", "pie", etc.)
            data: Data object
            title: Chart title
            **kwargs: Chart customization options
        """
        chart = Chart(data, title, chart_type=chart_type, **kwargs)
        self.charts.append(chart)
        return self
    
    def build(self):
        """Build dashboard from visual components."""
        from .dashboard import Dashboard
        return Dashboard(self.title, self.charts, self.layout, self.columns, self.spacing)
# Convenience functions for easy visual building
def create_bar(data: Data, title: str = "", **kwargs) -> Chart:
    """Create a bar chart (convenience function)."""
    return Chart(data, title, chart_type="bar", **kwargs)

def create_line(data: Data, title: str = "", **kwargs) -> Chart:
    """Create a line chart (convenience function)."""
    return Chart(data, title, chart_type="line", **kwargs)

def create_pie(data: Data, title: str = "", **kwargs) -> Chart:
    """Create a pie chart (convenience function)."""
    return Chart(data, title, chart_type="pie", **kwargs)

def create_scatter(data: Data, title: str = "", **kwargs) -> Chart:
    """Create a scatter chart (convenience function)."""
    return Chart(data, title, chart_type="scatter", **kwargs)

# Visual builder shortcuts
vb = VisualBuilder()

def set_title(title: str):
    """Set dashboard title using visual builder."""
    vb.set_title(title)
    return vb

def set_layout(layout: str, columns: int = 2, spacing: int = 20):
    """Set dashboard layout using visual builder."""
    vb.set_layout(layout, columns, spacing)
    return vb

def add_bar(data: Data, title: str = "", **kwargs):
    """Add bar chart using visual builder."""
    return vb.add_bar(data, title, **kwargs)

def add_line(data: Data, title: str = "", **kwargs):
    """Add line chart using visual builder."""
    return vb.add_line(data, title, **kwargs)

def add_pie(data: Data, title: str = "", **kwargs):
    """Add pie chart using visual builder."""
    return vb.add_pie(data, title, **kwargs)

def add_scatter(data: Data, title: str = "", **kwargs):
    """Add scatter chart using visual builder."""
    return vb.add_scatter(data, title, **kwargs)

def build_dashboard():
    """Build dashboard from visual builder."""
    return vb.build()

# Reset visual builder
def reset_visual_builder():
    """Reset visual builder to initial state."""
    global vb
    vb = VisualBuilder()