"""
Core data models for ChartCraft.
Every model serialises to a JSON-safe dict via .to_spec().
"""

from __future__ import annotations

import uuid
from dataclasses import dataclass, field
from typing import Any, Callable, Dict, List, Optional, Union


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

def _uid() -> str:
    return str(uuid.uuid4())[:8]


DataSource = Union[
    dict,
    list,
    Callable,
    Any,  # pandas DataFrame / SQL result
]


# ---------------------------------------------------------------------------
# Filter
# ---------------------------------------------------------------------------

FILTER_TYPES = {
    "select", "multi_select", "date_range", "slider", "text", "toggle",
}


@dataclass
class Filter:
    """Interactive slicer / filter widget."""

    name: str
    label: str = ""
    type: str = "select"          # one of FILTER_TYPES
    options: Optional[List] = None
    default: Any = None
    scope: str = "page"           # "page" | "app"
    placeholder: str = ""
    id: str = field(default_factory=_uid)

    def __post_init__(self):
        if not self.label:
            self.label = self.name.replace("_", " ").title()
        if self.type not in FILTER_TYPES:
            raise ValueError(f"Filter type must be one of {FILTER_TYPES}")

    def to_spec(self) -> dict:
        return {
            "id": self.id,
            "name": self.name,
            "label": self.label,
            "type": self.type,
            "options": self.options,
            "default": self.default,
            "scope": self.scope,
            "placeholder": self.placeholder,
        }


# ---------------------------------------------------------------------------
# KPI
# ---------------------------------------------------------------------------

@dataclass
class KPI:
    """Single metric card with optional sparkline and real-time refresh."""

    title: str
    value: Any = None
    change: Optional[float] = None
    change_label: str = "vs prev"
    prefix: str = ""
    suffix: str = ""
    icon: str = ""
    color: str = ""
    sparkline: Optional[List[float]] = None
    refresh: Optional[int] = None
    data_fn: Optional[Callable] = None
    linked_filters: List[str] = field(default_factory=list)
    id: str = field(default_factory=_uid)

    def resolve(self, filters: dict = None) -> Any:
        """Call data_fn if present, return resolved value."""
        if self.data_fn:
            try:
                import inspect
                sig = inspect.signature(self.data_fn)
                if len(sig.parameters) > 0:
                    return self.data_fn(filters or {})
                return self.data_fn()
            except Exception as e:
                return f"Error: {e}"
        return self.value

    def to_spec(self, filters: dict = None) -> dict:
        value = self.resolve(filters)
        return {
            "id": self.id,
            "type": "kpi",
            "title": self.title,
            "value": str(value) if value is not None else "",
            "change": self.change,
            "change_label": self.change_label,
            "prefix": self.prefix,
            "suffix": self.suffix,
            "icon": self.icon,
            "color": self.color,
            "sparkline": self.sparkline,
            "refresh": self.refresh,
            "linked_filters": self.linked_filters,
        }


# ---------------------------------------------------------------------------
# Base Chart
# ---------------------------------------------------------------------------

@dataclass
class _BaseChart:
    """Common fields shared by every chart type."""

    data: DataSource = None
    x: Optional[str] = None
    y: Optional[Union[str, List[str]]] = None
    title: str = ""
    subtitle: str = ""
    colors: Optional[List[str]] = None
    palette: Optional[str] = None
    col: int = 0
    colspan: int = 12
    height: int = 400
    refresh: Optional[int] = None
    data_fn: Optional[Callable] = None
    linked_filters: List[str] = field(default_factory=list)
    # Interaction
    tooltip: bool = True
    click_action: Optional[str] = None   # "drill" | "filter" | "navigate"
    click_target: Optional[str] = None   # page path or filter name
    # Animation
    animate: bool = True
    animate_duration: int = 800
    # Position (used by builder)
    id: str = field(default_factory=_uid)

    # chart_type is set by subclasses
    chart_type: str = field(init=False, default="base")

    def _resolve_data(self, filters: dict = None) -> DataSource:
        if self.data_fn:
            try:
                import inspect
                sig = inspect.signature(self.data_fn)
                if len(sig.parameters) > 0:
                    return self.data_fn(filters or {})
                return self.data_fn()
            except Exception as e:
                return {"error": str(e)}
        return self.data

    def _normalise(self, raw: DataSource) -> dict:
        """Convert any supported data format into {labels, datasets}."""
        if raw is None:
            return {"labels": [], "datasets": []}

        # Error passthrough
        if isinstance(raw, dict) and "error" in raw and len(raw) == 1:
            return {"error": raw["error"], "labels": [], "datasets": []}

        try:
            # pandas DataFrame
            if hasattr(raw, "to_dict"):
                raw = raw.to_dict(orient="records")

            # dict of scalars → pie/bar style {"label": value}
            if isinstance(raw, dict) and not any(isinstance(v, (list, tuple)) for v in raw.values()):
                return {
                    "labels": list(raw.keys()),
                    "datasets": [{"label": "Value", "data": list(raw.values())}],
                }

            # dict of lists → {"month": [...], "sales": [...]}
            if isinstance(raw, dict):
                x_col = self.x or list(raw.keys())[0]
                y_cols = self.y if isinstance(self.y, list) else (
                    [self.y] if self.y else [k for k in raw.keys() if k != x_col]
                )
                return {
                    "labels": raw.get(x_col, []),
                    "datasets": [{"label": col, "data": raw.get(col, [])} for col in y_cols],
                }

            # list of dicts → [{"month": "Jan", "sales": 100}, ...]
            if isinstance(raw, list) and raw and isinstance(raw[0], dict):
                x_col = self.x or list(raw[0].keys())[0]
                y_cols = self.y if isinstance(self.y, list) else (
                    [self.y] if self.y else [k for k in raw[0].keys() if k != x_col]
                )
                labels = [row.get(x_col, "") for row in raw]
                datasets = [
                    {"label": col, "data": [row.get(col) for row in raw]}
                    for col in y_cols
                ]
                return {"labels": labels, "datasets": datasets}

            # list of tuples (SQL results)
            if isinstance(raw, list) and raw and isinstance(raw[0], (list, tuple)):
                if len(raw[0]) == 2:
                    return {
                        "labels": [str(r[0]) for r in raw],
                        "datasets": [{"label": "Value", "data": [r[1] for r in raw]}],
                    }
                # multi-column
                labels = [str(r[0]) for r in raw]
                datasets = [
                    {"label": f"Col {i+1}", "data": [r[i] for r in raw]}
                    for i in range(1, len(raw[0]))
                ]
                return {"labels": labels, "datasets": datasets}

        except Exception as e:
            return {"error": str(e), "labels": [], "datasets": []}

        return {"labels": [], "datasets": []}

    def to_spec(self, filters: dict = None) -> dict:
        raw = self._resolve_data(filters)
        normalised = self._normalise(raw)
        return {
            "id": self.id,
            "type": self.chart_type,
            "title": self.title,
            "subtitle": self.subtitle,
            "data": normalised,
            "colors": self.colors,
            "palette": self.palette,
            "col": self.col,
            "colspan": self.colspan,
            "height": self.height,
            "refresh": self.refresh,
            "linked_filters": self.linked_filters,
            "tooltip": self.tooltip,
            "click_action": self.click_action,
            "click_target": self.click_target,
            "animate": self.animate,
            "animate_duration": self.animate_duration,
            "options": self._chart_options(),
        }

    def _chart_options(self) -> dict:
        """Override in subclasses to add chart-specific ECharts options."""
        return {}


# ---------------------------------------------------------------------------
# Chart subclasses — one per chart type
# ---------------------------------------------------------------------------

@dataclass
class Bar(_BaseChart):
    horizontal: bool = False
    stacked: bool = False
    grouped: bool = False
    show_values: bool = False

    def __post_init__(self):
        self.chart_type = "bar"

    def _chart_options(self):
        return {
            "horizontal": self.horizontal,
            "stacked": self.stacked,
            "grouped": self.grouped,
            "show_values": self.show_values,
        }


@dataclass
class Line(_BaseChart):
    smooth: bool = True
    show_dots: bool = True
    dash: bool = False
    fill: bool = False

    def __post_init__(self):
        self.chart_type = "line"

    def _chart_options(self):
        return {
            "smooth": self.smooth,
            "show_dots": self.show_dots,
            "dash": self.dash,
            "fill": self.fill,
        }


@dataclass
class Area(_BaseChart):
    smooth: bool = True
    stacked: bool = False
    gradient: bool = True

    def __post_init__(self):
        self.chart_type = "area"

    def _chart_options(self):
        return {"smooth": self.smooth, "stacked": self.stacked, "gradient": self.gradient}


@dataclass
class Pie(_BaseChart):
    label_position: str = "outside"   # "outside" | "inside" | "none"
    explode: Optional[List[int]] = None

    def __post_init__(self):
        self.chart_type = "pie"

    def _chart_options(self):
        return {"label_position": self.label_position, "explode": self.explode}


@dataclass
class Donut(_BaseChart):
    inner_radius: str = "60%"
    center_text: str = ""
    label_position: str = "outside"

    def __post_init__(self):
        self.chart_type = "donut"

    def _chart_options(self):
        return {
            "inner_radius": self.inner_radius,
            "center_text": self.center_text,
            "label_position": self.label_position,
        }


@dataclass
class Scatter(_BaseChart):
    size: Optional[str] = None        # column name for bubble size
    group: Optional[str] = None       # column name for colour grouping
    min_radius: int = 4
    max_radius: int = 40

    def __post_init__(self):
        self.chart_type = "scatter"

    def _normalise(self, raw):
        """Scatter expects list of {x, y[, size, group]} dicts."""
        if raw is None:
            return {"points": []}
        if hasattr(raw, "to_dict"):
            raw = raw.to_dict(orient="records")
        if isinstance(raw, list) and raw and isinstance(raw[0], dict):
            x_col = self.x or "x"
            y_col = (self.y[0] if isinstance(self.y, list) else self.y) or "y"
            points = []
            for row in raw:
                p = {"x": row.get(x_col), "y": row.get(y_col)}
                if self.size:
                    p["size"] = row.get(self.size)
                if self.group:
                    p["group"] = row.get(self.group)
                points.append(p)
            return {"points": points}
        return {"points": []}

    def _chart_options(self):
        return {
            "size_col": self.size,
            "group_col": self.group,
            "min_radius": self.min_radius,
            "max_radius": self.max_radius,
        }


# Bubble is just Scatter with a size column
Bubble = Scatter


@dataclass
class Heatmap(_BaseChart):
    color_scale: List[str] = field(default_factory=lambda: ["#313695", "#4575b4", "#74add1", "#abd9e9", "#e0f3f8", "#ffffbf", "#fee090", "#fdae61", "#f46d43", "#d73027", "#a50026"])
    show_labels: bool = True

    def __post_init__(self):
        self.chart_type = "heatmap"

    def _normalise(self, raw):
        """Heatmap expects a 2-D matrix dict: {x_labels, y_labels, matrix}."""
        if isinstance(raw, dict) and "matrix" in raw:
            return raw
        # Try to build matrix from list of dicts with x, y, value cols
        if isinstance(raw, list) and raw and isinstance(raw[0], dict):
            x_col = self.x or list(raw[0].keys())[0]
            y_col = (self.y[0] if isinstance(self.y, list) else self.y) or list(raw[0].keys())[1]
            v_col = list(raw[0].keys())[-1]
            xs = sorted(set(r[x_col] for r in raw))
            ys = sorted(set(r[y_col] for r in raw))
            val_map = {(r[x_col], r[y_col]): r[v_col] for r in raw}
            matrix = [[val_map.get((x, y), 0) for x in xs] for y in ys]
            return {"x_labels": xs, "y_labels": ys, "matrix": matrix}
        return {"x_labels": [], "y_labels": [], "matrix": []}

    def _chart_options(self):
        return {"color_scale": self.color_scale, "show_labels": self.show_labels}


@dataclass
class Radar(_BaseChart):
    shape: str = "polygon"     # "polygon" | "circle"
    fill: bool = True

    def __post_init__(self):
        self.chart_type = "radar"

    def _chart_options(self):
        return {"shape": self.shape, "fill": self.fill}


@dataclass
class Waterfall(_BaseChart):
    show_total: bool = True
    positive_color: str = ""
    negative_color: str = ""

    def __post_init__(self):
        self.chart_type = "waterfall"

    def _chart_options(self):
        return {
            "show_total": self.show_total,
            "positive_color": self.positive_color,
            "negative_color": self.negative_color,
        }


@dataclass
class Funnel(_BaseChart):
    orientation: str = "vertical"    # "vertical" | "horizontal"
    gap: int = 2
    show_labels: bool = True

    def __post_init__(self):
        self.chart_type = "funnel"

    def _chart_options(self):
        return {
            "orientation": self.orientation,
            "gap": self.gap,
            "show_labels": self.show_labels,
        }


@dataclass
class Treemap(_BaseChart):
    drill_down: bool = True
    show_breadcrumb: bool = True

    def __post_init__(self):
        self.chart_type = "treemap"

    def _normalise(self, raw):
        """Treemap expects {name, value[, children]} tree structure."""
        if isinstance(raw, dict) and "name" in raw:
            return raw
        if isinstance(raw, list):
            # flat list of {name, value} → wrap
            return {"name": "root", "children": raw}
        return {"name": "root", "children": []}

    def _chart_options(self):
        return {"drill_down": self.drill_down, "show_breadcrumb": self.show_breadcrumb}


@dataclass
class Sankey(_BaseChart):
    """flows: list of (source, target, value) tuples."""
    orientation: str = "horizontal"
    node_width: int = 20
    node_gap: int = 8

    def __post_init__(self):
        self.chart_type = "sankey"

    def _normalise(self, raw):
        if isinstance(raw, list):
            links = []
            nodes_set = set()
            for item in raw:
                if isinstance(item, (list, tuple)) and len(item) >= 3:
                    src, tgt, val = item[0], item[1], item[2]
                    links.append({"source": str(src), "target": str(tgt), "value": val})
                    nodes_set.add(str(src))
                    nodes_set.add(str(tgt))
                elif isinstance(item, dict):
                    links.append(item)
                    nodes_set.add(str(item.get("source", "")))
                    nodes_set.add(str(item.get("target", "")))
            return {"nodes": [{"name": n} for n in nodes_set], "links": links}
        return {"nodes": [], "links": []}

    def _chart_options(self):
        return {
            "orientation": self.orientation,
            "node_width": self.node_width,
            "node_gap": self.node_gap,
        }


@dataclass
class Gauge(_BaseChart):
    value: float = 0
    min_val: float = 0
    max_val: float = 100
    zones: Optional[List[dict]] = None    # [{"min": 0, "max": 60, "color": "#10B981"}, ...]
    arc_width: str = "18%"
    show_pointer: bool = True

    def __post_init__(self):
        self.chart_type = "gauge"
        # Allow positional value as data
        if self.data is None and self.value is not None:
            self.data = self.value

    def _normalise(self, raw):
        val = raw if isinstance(raw, (int, float)) else self.value
        return {"value": val, "min": self.min_val, "max": self.max_val}

    def _chart_options(self):
        return {
            "zones": self.zones or [
                {"min": 0, "max": 60, "color": "#10B981"},
                {"min": 60, "max": 80, "color": "#F59E0B"},
                {"min": 80, "max": 100, "color": "#EF4444"},
            ],
            "arc_width": self.arc_width,
            "show_pointer": self.show_pointer,
        }


@dataclass
class Candlestick(_BaseChart):
    show_volume: bool = False
    ma_lines: Optional[List[int]] = None    # e.g. [5, 20, 60]

    def __post_init__(self):
        self.chart_type = "candlestick"

    def _normalise(self, raw):
        """Expects list of {date, open, high, low, close[, volume]} dicts."""
        if isinstance(raw, list) and raw:
            if isinstance(raw[0], dict):
                return {"ohlc": raw}
            if isinstance(raw[0], (list, tuple)):
                return {"ohlc": [
                    {"date": r[0], "open": r[1], "high": r[2], "low": r[3], "close": r[4]}
                    for r in raw
                ]}
        return {"ohlc": []}

    def _chart_options(self):
        return {"show_volume": self.show_volume, "ma_lines": self.ma_lines or []}


@dataclass
class Histogram(_BaseChart):
    bins: int = 20
    show_density: bool = False

    def __post_init__(self):
        self.chart_type = "histogram"

    def _chart_options(self):
        return {"bins": self.bins, "show_density": self.show_density}


@dataclass
class BoxPlot(_BaseChart):
    show_outliers: bool = True
    notched: bool = False

    def __post_init__(self):
        self.chart_type = "boxplot"

    def _chart_options(self):
        return {"show_outliers": self.show_outliers, "notched": self.notched}


@dataclass
class Table(_BaseChart):
    columns: Optional[List[str]] = None
    page_size: int = 20
    sortable: bool = True
    searchable: bool = True
    striped: bool = True

    def __post_init__(self):
        self.chart_type = "table"

    def _normalise(self, raw):
        if raw is None:
            return {"columns": [], "rows": []}
        if hasattr(raw, "to_dict"):
            cols = list(raw.columns)
            rows = raw.values.tolist()
            return {"columns": cols, "rows": rows}
        if isinstance(raw, list) and raw and isinstance(raw[0], dict):
            cols = self.columns or list(raw[0].keys())
            rows = [[row.get(c) for c in cols] for row in raw]
            return {"columns": cols, "rows": rows}
        if isinstance(raw, list) and raw and isinstance(raw[0], (list, tuple)):
            return {"columns": self.columns or [], "rows": [list(r) for r in raw]}
        return {"columns": [], "rows": []}

    def _chart_options(self):
        return {
            "page_size": self.page_size,
            "sortable": self.sortable,
            "searchable": self.searchable,
            "striped": self.striped,
        }


@dataclass
class Metric(_BaseChart):
    """Single large number / KPI visual (inline chart variant)."""
    value: Any = None
    sparkline: Optional[List[float]] = None
    trend: Optional[float] = None

    def __post_init__(self):
        self.chart_type = "metric"
        if self.data is None:
            self.data = self.value

    def _normalise(self, raw):
        return {"value": raw, "sparkline": self.sparkline, "trend": self.trend}


# ---------------------------------------------------------------------------
# Layout widgets
# ---------------------------------------------------------------------------

@dataclass
class Divider:
    col: int = 0
    colspan: int = 12
    color: str = ""
    thickness: int = 1
    id: str = field(default_factory=_uid)

    def to_spec(self, filters=None) -> dict:
        return {"id": self.id, "type": "divider", "col": self.col, "colspan": self.colspan,
                "color": self.color, "thickness": self.thickness}


@dataclass
class Spacer:
    col: int = 0
    colspan: int = 12
    height: int = 24
    id: str = field(default_factory=_uid)

    def to_spec(self, filters=None) -> dict:
        return {"id": self.id, "type": "spacer", "col": self.col,
                "colspan": self.colspan, "height": self.height}


@dataclass
class TextBlock:
    content: str = ""
    col: int = 0
    colspan: int = 12
    font_size: str = "1rem"
    align: str = "left"
    id: str = field(default_factory=_uid)

    def to_spec(self, filters=None) -> dict:
        return {"id": self.id, "type": "text", "content": self.content, "col": self.col,
                "colspan": self.colspan, "font_size": self.font_size, "align": self.align}


@dataclass
class SectionHeader:
    title: str = ""
    subtitle: str = ""
    col: int = 0
    colspan: int = 12
    id: str = field(default_factory=_uid)

    def to_spec(self, filters=None) -> dict:
        return {"id": self.id, "type": "section_header", "title": self.title,
                "subtitle": self.subtitle, "col": self.col, "colspan": self.colspan}


# ---------------------------------------------------------------------------
# Dashboard
# ---------------------------------------------------------------------------

@dataclass
class Dashboard:
    title: str = ""
    subtitle: str = ""
    kpis: List[KPI] = field(default_factory=list)
    charts: List[Any] = field(default_factory=list)
    filters: List[Filter] = field(default_factory=list)
    cols: int = 12
    refresh: Optional[int] = None
    background: str = ""          # override theme bg for this page
    icon: str = ""                # emoji or icon name for nav
    id: str = field(default_factory=_uid)

    # Fluent API
    def add_kpi(self, *args, **kwargs) -> "Dashboard":
        self.kpis.append(KPI(*args, **kwargs))
        return self

    def add_chart(self, chart) -> "Dashboard":
        self.charts.append(chart)
        return self

    def add_filter(self, *args, **kwargs) -> "Dashboard":
        self.filters.append(Filter(*args, **kwargs))
        return self

    def to_spec(self, filters: dict = None) -> dict:
        return {
            "id": self.id,
            "title": self.title,
            "subtitle": self.subtitle,
            "cols": self.cols,
            "refresh": self.refresh,
            "background": self.background,
            "filters": [f.to_spec() for f in self.filters],
            "kpis": [k.to_spec(filters) for k in self.kpis],
            "charts": [c.to_spec(filters) for c in self.charts],
        }

    def refreshable_components(self):
        """Yield (id, data_fn, interval) for all components with refresh set."""
        for kpi in self.kpis:
            if kpi.refresh and (kpi.data_fn or callable(kpi.value)):
                yield kpi.id, kpi.data_fn or (lambda: kpi.value), kpi.refresh
        for chart in self.charts:
            if hasattr(chart, "refresh") and chart.refresh and chart.data_fn:
                yield chart.id, chart.data_fn, chart.refresh

    def refreshable_specs(self, filters: dict = None):
        """
        Yield (id, spec_fn, interval) where spec_fn() returns the full component
        spec dict — used by SSE to push complete chart/KPI updates to the browser.
        """
        for kpi in self.kpis:
            if kpi.refresh and (kpi.data_fn or callable(kpi.value)):
                _k = kpi
                def _kspec(k=_k, f=filters):
                    return {"type": "kpi", **k.to_spec(f)}
                yield kpi.id, _kspec, kpi.refresh
        for chart in self.charts:
            if hasattr(chart, "refresh") and chart.refresh and chart.data_fn:
                _c = chart
                def _cspec(c=_c, f=filters):
                    return {"type": "chart", **c.to_spec(f)}
                yield chart.id, _cspec, chart.refresh
