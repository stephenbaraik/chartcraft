"""
ChartCraft v1 - Simplified Dashboard Library

A minimalist, pandas-like approach to creating interactive dashboards with full customization.

This is the simplified version of ChartCraft v1, designed with:
- Simple API (like pandas)
- No presets (full customization)
- Minimal file structure
- Easy learning curve

Quick start:
    import chartcraft as cc

    # Create data (pandas-like)
    data = cc.Data({
        "month": ["Jan", "Feb", "Mar", "Apr"],
        "sales": [100, 150, 200, 180],
        "profit": [20, 35, 50, 40]
    })

    # Create charts
    bar_chart = cc.bar(data, title="Sales", x="month", y="sales")
    line_chart = cc.line(data, title="Profit", x="month", y="profit")

    # Create dashboard
    dashboard = cc.Dashboard(
        title="Business Metrics",
        charts=[bar_chart, line_chart]
    )

    # Serve locally
    cc.serve(dashboard)
"""

from .data import Data, Series, DataFrame
from .charts import (
    bar, line, area, pie, donut, scatter, bubble, histogram,
    boxplot, heatmap, radar, waterfall, gauge, candlestick,
    table, metric, sankey, treemap, funnel
)
from .dashboard import Dashboard
from .render import render, save, serve
from .themes import theme, reset_theme, apply_dark_theme, apply_light_theme, apply_vibrant_theme, get_theme, export_theme
from .visual_builder import set_title, set_layout, add_bar, add_line, build_dashboard

__version__ = "1.0.0"
__all__ = [
    # Data structures (pandas-like)
    "Data", "Series", "DataFrame",
    # Chart functions
    "bar", "line", "area", "pie", "donut", "scatter", "bubble",
    "histogram", "boxplot", "heatmap", "radar", "waterfall",
    "gauge", "candlestick", "table", "metric", "sankey",
    "treemap", "funnel",
    # Core functions
    "Dashboard", "render", "save", "serve", "theme", "reset_theme",
    # Theme customization
    "apply_dark_theme", "apply_light_theme", "apply_vibrant_theme",
    "get_theme", "export_theme",
    # Visual builder
    "set_title", "set_layout", "add_bar", "add_line", "build_dashboard",
]