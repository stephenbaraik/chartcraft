"""
◆ ChartCraft — Python-powered dashboards that rival Power BI & Tableau.

Quick start:
    import chartcraft as cc

    app = cc.App("My Dashboard", theme="midnight")

    @app.page("/")
    def home():
        return cc.Dashboard(
            title="Overview",
            kpis=[cc.KPI("Revenue", "$1.2M", change=12.5)],
            charts=[cc.Bar({"Q1": 100, "Q2": 200}, title="Sales", col=0, colspan=12)],
        )

    app.run()  # → http://localhost:8050
"""

from chartcraft.server.app_server import AppServer
from chartcraft.core.models import (
    Dashboard, Filter, KPI,
    Bar, Line, Area, Pie, Donut, Scatter, Bubble,
    Heatmap, Radar, Waterfall, Funnel, Treemap, Sankey,
    Gauge, Candlestick, Histogram, BoxPlot, Table, Metric,
    Divider, Spacer, TextBlock, SectionHeader,
)
from chartcraft.core.theme import (
    Theme, THEMES, get_theme, register_theme, list_themes,
)
from chartcraft.core.colors import (
    PALETTES, get_palette, list_palettes, auto_colors, ColorScale,
    lighten, darken, opacity,
    complementary, triadic, analogous, split_complementary,
)
from chartcraft.connectors import connect_sql, connect_csv, connect_api


def App(title: str, theme: str = "default") -> AppServer:
    """Create a ChartCraft application."""
    return AppServer(title=title, theme=theme)


def quick_dashboard(
    title: str,
    charts: list,
    theme: str = "default",
    kpis: list = None,
    save_path: str = None,
) -> str:
    """
    Quickly create and optionally export a dashboard without defining an App.

    Returns HTML string (or writes to save_path if provided).
    """
    app = AppServer(title=title, theme=theme)
    dashboard = Dashboard(title=title, kpis=kpis or [], charts=charts)

    @app.page("/")
    def _page():
        return dashboard

    html = app.to_html()
    if save_path:
        with open(save_path, "w", encoding="utf-8") as f:
            f.write(html)
        print(f"◆ Exported → {save_path}")
    return html


__version__ = "0.1.0"
__all__ = [
    "App", "AppServer", "quick_dashboard",
    "Dashboard", "Filter", "KPI",
    "Bar", "Line", "Area", "Pie", "Donut", "Scatter", "Bubble",
    "Heatmap", "Radar", "Waterfall", "Funnel", "Treemap", "Sankey",
    "Gauge", "Candlestick", "Histogram", "BoxPlot", "Table", "Metric",
    "Divider", "Spacer", "TextBlock", "SectionHeader",
    "Theme", "THEMES", "get_theme", "register_theme", "list_themes",
    "PALETTES", "get_palette", "list_palettes", "auto_colors", "ColorScale",
    "lighten", "darken", "opacity",
    "complementary", "triadic", "analogous", "split_complementary",
    "connect_sql", "connect_csv", "connect_api",
]
