"""
Python AST parser — converts a generated ChartCraft Python script back into
builder canvas state (the "Python → canvas" direction).

Only handles code produced by codegen.generate(); arbitrary user code is not
supported but gracefully degrades — unknown constructs are skipped.
"""

from __future__ import annotations
import ast
import json
from typing import Any, Dict, List, Optional


# ─── Reverse map: constructor name → widget type ────────────────────────────

CONSTRUCTOR_MAP = {
    "cc.Bar":         "bar",
    "cc.Line":        "line",
    "cc.Area":        "area",
    "cc.Pie":         "pie",
    "cc.Donut":       "donut",
    "cc.Scatter":     "scatter",
    "cc.Bubble":      "bubble",
    "cc.Heatmap":     "heatmap",
    "cc.Radar":       "radar",
    "cc.Waterfall":   "waterfall",
    "cc.Funnel":      "funnel",
    "cc.Treemap":     "treemap",
    "cc.Sankey":      "sankey",
    "cc.Gauge":       "gauge",
    "cc.Candlestick": "candlestick",
    "cc.Histogram":   "histogram",
    "cc.BoxPlot":     "boxplot",
    "cc.Table":       "table",
    "cc.Metric":      "metric",
    "cc.KPI":         "kpi",
    "cc.SectionHeader": "section_header",
    "cc.Divider":     "divider",
    "cc.Spacer":      "spacer",
    "cc.TextBlock":   "textblock",
    "cc.Filter":      "filter",
}

# Default canvas positions/sizes per type
TYPE_DEFAULTS = {
    "kpi":          (0,   0, 240, 120),
    "filter":       (0,   0, 200, 60),
    "section_header": (0, 0, 960, 48),
    "divider":      (0,   0, 960, 12),
    "spacer":       (0,   0, 960, 40),
    "textblock":    (0,   0, 480, 120),
    "gauge":        (0,   0, 280, 260),
    "table":        (0,   0, 960, 360),
}
DEFAULT_WIDGET = (0, 0, 480, 320)


# ─── AST value extraction ────────────────────────────────────────────────────

def _eval_node(node: ast.expr) -> Any:
    """Safely evaluate a constant AST node to a Python value."""
    if isinstance(node, ast.Constant):
        return node.value
    if isinstance(node, ast.List):
        return [_eval_node(el) for el in node.elts]
    if isinstance(node, ast.Dict):
        return {_eval_node(k): _eval_node(v) for k, v in zip(node.keys, node.values)}
    if isinstance(node, ast.Tuple):
        return tuple(_eval_node(el) for el in node.elts)
    if isinstance(node, ast.UnaryOp) and isinstance(node.op, ast.USub):
        val = _eval_node(node.operand)
        return -val if isinstance(val, (int, float)) else val
    if isinstance(node, ast.Name):
        return node.id  # e.g. None, True, False variable refs
    # For attribute access like cc.KPI — return the dotted name
    if isinstance(node, ast.Attribute):
        v = _eval_node(node.value)
        if isinstance(v, str):
            return f"{v}.{node.attr}"
        return node.attr
    return None


def _call_name(node: ast.Call) -> str:
    """Return the full dotted call name e.g. 'cc.Bar'."""
    func = node.func
    if isinstance(func, ast.Attribute):
        prefix = _call_name_expr(func.value)
        return f"{prefix}.{func.attr}" if prefix else func.attr
    if isinstance(func, ast.Name):
        return func.id
    return ""


def _call_name_expr(expr: ast.expr) -> str:
    if isinstance(expr, ast.Name):
        return expr.id
    if isinstance(expr, ast.Attribute):
        p = _call_name_expr(expr.value)
        return f"{p}.{expr.attr}" if p else expr.attr
    return ""


def _parse_call_kwargs(node: ast.Call) -> Dict[str, Any]:
    """Extract keyword arguments from a Call node."""
    kwargs = {}
    for kw in node.keywords:
        if kw.arg:
            kwargs[kw.arg] = _eval_node(kw.value)
    # Also handle positional args for types like Gauge(value, ...)
    if node.args:
        kwargs["__pos__"] = [_eval_node(a) for a in node.args]
    return kwargs


# ─── Widget builders ─────────────────────────────────────────────────────────

_widget_counter = 0

def _uid() -> str:
    global _widget_counter
    _widget_counter += 1
    return f"parsed_{_widget_counter:04d}"


def _kw_to_widget(cname: str, kwargs: Dict, x: int = 0, y: int = 0) -> Optional[Dict]:
    wtype = CONSTRUCTOR_MAP.get(cname)
    if not wtype:
        return None

    pos_args = kwargs.pop("__pos__", [])
    dx, dy, dw, dh = TYPE_DEFAULTS.get(wtype, DEFAULT_WIDGET)

    # col/colspan → canvas width estimate (12-col @ 80px each = 960px)
    col     = kwargs.get("col", 0)
    colspan = kwargs.get("colspan", 12)
    height  = kwargs.get("height", dh)
    canvas_w = int(colspan / 12 * 960)
    canvas_x = int(col / 12 * 960) + x
    canvas_y = y

    w = {
        "id":       _uid(),
        "type":     wtype,
        "x":        canvas_x,
        "y":        canvas_y,
        "w":        canvas_w,
        "h":        height,
        "zIndex":   1,
        "col":      col,
        "colspan":  colspan,
        "title":    kwargs.get("title", ""),
        "subtitle": kwargs.get("subtitle", ""),
        "colors":   kwargs.get("colors"),
        "palette":  kwargs.get("palette"),
        "refresh":  kwargs.get("refresh"),
        "animate":  True,
        "tooltip":  True,
    }

    # Data
    data = kwargs.get("data")
    if data:
        try:
            w["customData"] = json.dumps(data, default=str)
        except Exception:
            pass

    # Axis columns
    if "x" in kwargs:
        w["x_col"] = kwargs["x"]
    if "y" in kwargs:
        w["y_col"] = kwargs["y"] if isinstance(kwargs["y"], str) else json.dumps(kwargs["y"])

    # KPI
    if wtype == "kpi":
        if pos_args:
            w["title"] = pos_args[0] if len(pos_args) > 0 else w["title"]
            w["value"] = str(pos_args[1]) if len(pos_args) > 1 else ""
        else:
            w["value"] = str(kwargs.get("value", ""))
        w["change"] = kwargs.get("change")
        w["w"] = 240
        w["h"] = 120

    # Gauge: first positional arg is the value
    elif wtype == "gauge":
        if pos_args:
            w["gauge_value"] = pos_args[0]
        w["w"] = canvas_w
        w["h"] = height

    # Chart-specific options
    opts = {}
    for k in ("grouped", "stacked", "horizontal", "show_values",
              "smooth", "show_dots", "dash",
              "gradient", "inner_radius", "center_text", "label_position",
              "shape", "show_total", "orientation", "gap", "drill_down",
              "node_width", "page_size", "sortable", "searchable",
              "bins", "show_outliers", "log_scale", "bubble_size",
              "color_scale"):
        if k in kwargs:
            opts[k] = kwargs[k]
    if opts:
        w["options"] = opts

    return w


# ─── Page parser ─────────────────────────────────────────────────────────────

def _parse_dashboard_call(call_node: ast.Call, page_path: str, page_title: str) -> Dict:
    """Parse a cc.Dashboard(...) call and return a page state dict."""
    kwargs = _parse_call_kwargs(call_node)
    title   = kwargs.get("title", page_title)
    widgets = []
    y_cursor = 0

    # KPIs
    kpis_node = kwargs.get("kpis")
    if isinstance(kpis_node, list):
        kx = 0
        for item in kpis_node:
            if isinstance(item, dict) and item.get("__call__"):
                w = _kw_to_widget(item["__call__"], item.get("kwargs", {}), x=kx, y=y_cursor)
                if w:
                    widgets.append(w)
                    kx += w["w"]
        if kpis_node:
            y_cursor += 120

    # Charts
    charts_node = kwargs.get("charts")
    if isinstance(charts_node, list):
        # We need the actual parsed objects, not evaluated values
        # The list elements should be dicts with __call__ info from our AST walk
        row_h = 0
        last_col_end = 0
        for item in charts_node:
            if not isinstance(item, dict) or "__call__" not in item:
                continue
            cname = item["__call__"]
            ckw   = item.get("kwargs", {})
            col     = ckw.get("col", 0)
            colspan = ckw.get("colspan", 12)
            height  = ckw.get("height", 320)
            # Start new row when col resets
            if col < last_col_end - colspan:
                y_cursor += row_h
                row_h = 0
            w = _kw_to_widget(cname, dict(ckw), x=int(col/12*960), y=y_cursor)
            if w:
                widgets.append(w)
                row_h = max(row_h, height)
                last_col_end = col + colspan
        y_cursor += row_h

    return {"path": page_path, "title": title, "widgets": widgets}


# ─── Full AST walk ────────────────────────────────────────────────────────────

class _CallCollector(ast.NodeVisitor):
    """Collect all cc.XYZ(...) Call nodes as structured dicts."""

    def __init__(self):
        self.calls: List[Dict] = []  # {"__call__": name, "kwargs": {...}}

    def visit_Call(self, node: ast.Call):
        name = _call_name(node)
        if name.startswith("cc."):
            kwargs = {}
            pos = []
            for kw in node.keywords:
                if kw.arg:
                    val = self._resolve(kw.value)
                    kwargs[kw.arg] = val
            for arg in node.args:
                pos.append(self._resolve(arg))
            entry = {"__call__": name, "kwargs": kwargs}
            if pos:
                entry["kwargs"]["__pos__"] = pos
            self.calls.append(entry)
        self.generic_visit(node)

    def _resolve(self, node: ast.expr) -> Any:
        """Recursively resolve a node — if it's a cc.XYZ() call, return a call-dict."""
        if isinstance(node, ast.Call):
            name = _call_name(node)
            if name.startswith("cc."):
                kwargs = {}
                pos = []
                for kw in node.keywords:
                    if kw.arg:
                        kwargs[kw.arg] = self._resolve(kw.value)
                for arg in node.args:
                    pos.append(self._resolve(arg))
                if pos:
                    kwargs["__pos__"] = pos
                return {"__call__": name, "kwargs": kwargs}
        if isinstance(node, ast.List):
            return [self._resolve(el) for el in node.elts]
        if isinstance(node, ast.Dict):
            return {self._resolve(k): self._resolve(v) for k, v in zip(node.keys, node.values)}
        return _eval_node(node)


def parse_code(code: str) -> Dict:
    """
    Parse a ChartCraft Python script and return a builder canvas state dict:

    {
        "title": str,
        "theme": str,
        "pages": [{"path": str, "title": str, "widgets": [...]}]
    }

    Returns {"error": str} on parse failure.
    """
    global _widget_counter
    _widget_counter = 0

    try:
        tree = ast.parse(code)
    except SyntaxError as e:
        return {"error": f"SyntaxError: {e}"}

    collector = _CallCollector()
    collector.visit(tree)

    # ── Extract app title & theme ──────────────────────────────────────────
    title = "Dashboard"
    theme = "midnight"
    for c in collector.calls:
        if c["__call__"] == "cc.App":
            kw = c["kwargs"]
            pos = kw.get("__pos__", [])
            if pos:
                title = str(pos[0])
            else:
                title = str(kw.get("title", kw.get("name", title)))
            theme = str(kw.get("theme", theme))
            break

    # ── Walk function defs decorated with @app.page(...) ──────────────────
    pages = []
    y_base = 0  # stagger pages vertically

    for node in ast.walk(tree):
        if not isinstance(node, ast.FunctionDef):
            continue

        page_path = None
        for dec in node.decorator_list:
            if isinstance(dec, ast.Call):
                dname = _call_name(dec)
                if dname == "app.page":
                    args = dec.args
                    if args:
                        page_path = _eval_node(args[0])
                    break

        if page_path is None:
            continue

        # Find cc.Dashboard call inside the function body
        page_title = page_path.strip("/") or "Overview"
        fn_collector = _CallCollector()
        fn_collector.visit(node)

        dashboard_call_data = None
        for c in fn_collector.calls:
            if c["__call__"] == "cc.Dashboard":
                dashboard_call_data = c
                break

        if not dashboard_call_data:
            pages.append({"path": page_path, "title": page_title, "widgets": []})
            continue

        # Rebuild the page from the structured call data
        kw = dashboard_call_data["kwargs"]
        pg_title = kw.get("title", page_title)
        widgets  = []
        y_cursor = y_base

        # KPIs
        kpis_data = kw.get("kpis", [])
        if isinstance(kpis_data, list):
            kx = 0
            for item in kpis_data:
                if isinstance(item, dict) and "__call__" in item:
                    kpi_kw = dict(item["kwargs"])
                    w = _kw_to_widget(item["__call__"], kpi_kw, x=kx, y=y_cursor)
                    if w:
                        w["w"] = 240
                        w["h"] = 120
                        widgets.append(w)
                        kx += 240
            if kpis_data:
                y_cursor += 130

        # Charts
        charts_data = kw.get("charts", [])
        if isinstance(charts_data, list):
            row_h    = 0
            last_end = 0
            for item in charts_data:
                if not isinstance(item, dict) or "__call__" not in item:
                    continue
                ckw     = dict(item["kwargs"])
                col     = int(ckw.get("col") or 0)
                colspan = int(ckw.get("colspan") or 12)
                height  = int(ckw.get("height") or 320)
                cx      = int(col / 12 * 960)
                # New row when col jumps back
                if col < last_end - colspan:
                    y_cursor += row_h + 12
                    row_h = 0
                w = _kw_to_widget(item["__call__"], ckw, x=cx, y=y_cursor)
                if w:
                    widgets.append(w)
                    row_h    = max(row_h, height)
                    last_end = col + colspan
            y_cursor += row_h + 20

        y_base = y_cursor

        # Re-assign sequential z-indices
        for i, w in enumerate(widgets):
            w["zIndex"] = i + 1

        pages.append({"path": page_path, "title": pg_title, "widgets": widgets})

    if not pages:
        pages = [{"path": "/", "title": title, "widgets": []}]

    return {"title": title, "theme": theme, "pages": pages}
