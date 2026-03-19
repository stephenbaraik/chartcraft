"""
Code generator — converts builder canvas state to a valid Python script,
a Jupyter notebook (.ipynb), or a Docker project archive.
"""

from __future__ import annotations
import io
import json
import zipfile
from typing import Any, Dict, List


CHART_TYPE_MAP = {
    "bar":          "cc.Bar",
    "line":         "cc.Line",
    "area":         "cc.Area",
    "pie":          "cc.Pie",
    "donut":        "cc.Donut",
    "scatter":      "cc.Scatter",
    "bubble":       "cc.Bubble",
    "heatmap":      "cc.Heatmap",
    "radar":        "cc.Radar",
    "waterfall":    "cc.Waterfall",
    "funnel":       "cc.Funnel",
    "treemap":      "cc.Treemap",
    "sankey":       "cc.Sankey",
    "gauge":        "cc.Gauge",
    "candlestick":  "cc.Candlestick",
    "histogram":    "cc.Histogram",
    "boxplot":      "cc.BoxPlot",
    "table":        "cc.Table",
    "metric":       "cc.Metric",
    "section_header": "cc.SectionHeader",
    "divider":      "cc.Divider",
    "spacer":       "cc.Spacer",
    "textblock":    "cc.TextBlock",
}

# Per-type extra kwargs that should be emitted when non-default
CHART_OPTS = {
    "bar":         [("horizontal", False), ("stacked", False), ("grouped", False), ("show_values", False)],
    "line":        [("smooth", True), ("show_dots", True), ("dash", False)],
    "area":        [("smooth", True), ("stacked", False), ("gradient", True)],
    "pie":         [("label_position", "outside")],
    "donut":       [("inner_radius", "60%"), ("center_text", ""), ("label_position", "outside")],
    "scatter":     [("size", None), ("log_scale", False)],
    "bubble":      [("size", None)],
    "radar":       [("shape", "polygon")],
    "waterfall":   [("show_total", True)],
    "funnel":      [("orientation", "vertical"), ("gap", 2)],
    "treemap":     [("drill_down", True)],
    "sankey":      [("orientation", "horizontal"), ("node_width", 20)],
    "gauge":       [],   # value is positional
    "candlestick": [("show_volume", False)],
    "histogram":   [("bins", 20)],
    "boxplot":     [("show_outliers", True)],
    "table":       [("page_size", 10), ("sortable", True), ("searchable", False)],
    "metric":      [],
    "heatmap":     [],
}


def _fmt_val(v: Any) -> str:
    if v is None:
        return "None"
    if isinstance(v, str):
        return repr(v)
    if isinstance(v, bool):
        return "True" if v else "False"
    if isinstance(v, list):
        items = ", ".join(_fmt_val(x) for x in v)
        return f"[{items}]"
    if isinstance(v, dict):
        pairs = ", ".join(f"{repr(k)}: {_fmt_val(vv)}" for k, vv in v.items())
        return "{" + pairs + "}"
    return str(v)


def _widget_to_code(w: Dict, indent: str = "        ") -> str:
    wtype = w.get("type", "bar")
    constructor = CHART_TYPE_MAP.get(wtype, "cc.Bar")
    i4 = indent + "    "
    args: List[str] = []

    # ── Gauge: first positional arg ──────────────────────────────────────
    if wtype == "gauge":
        val = w.get("gauge_value", w.get("value", 0))
        args.append(_fmt_val(val))

    # ── SectionHeader / Divider / Spacer / TextBlock ─────────────────────
    elif wtype == "section_header":
        if w.get("title"):
            args.append(f"title={repr(w['title'])}")
        if w.get("subtitle"):
            args.append(f"subtitle={repr(w['subtitle'])}")
        args.append(f"col={w.get('col', 0)}")
        args.append(f"colspan={w.get('colspan', 12)}")
        return constructor + "(" + ", ".join(args) + ")"
    elif wtype in ("divider", "spacer"):
        args.append(f"col={w.get('col', 0)}")
        args.append(f"colspan={w.get('colspan', 12)}")
        return constructor + "(" + ", ".join(args) + ")"
    elif wtype == "textblock":
        args.append(f"content={repr(w.get('content', ''))}")
        args.append(f"col={w.get('col', 0)}")
        args.append(f"colspan={w.get('colspan', 12)}")
        return constructor + "(" + ", ".join(args) + ")"

    else:
        # ── Data ─────────────────────────────────────────────────────────
        custom = w.get("customData")
        if custom:
            try:
                data = json.loads(custom) if isinstance(custom, str) else custom
                args.append(f"data={_fmt_val(data)}")
            except Exception:
                args.append(f"data={repr(custom)}")

        # ── Axis columns ─────────────────────────────────────────────────
        x_col = w.get("x_col") or w.get("x")
        y_col = w.get("y_col") or w.get("y")
        if x_col:
            args.append(f"x={repr(x_col)}")
        if y_col:
            # y can be str or list
            try:
                y_val = json.loads(y_col) if (isinstance(y_col, str) and y_col.startswith("[")) else y_col
            except Exception:
                y_val = y_col
            args.append(f"y={_fmt_val(y_val)}")

    # ── Common display ────────────────────────────────────────────────────
    if w.get("title"):
        args.append(f"title={repr(w['title'])}")
    if w.get("subtitle"):
        args.append(f"subtitle={repr(w['subtitle'])}")

    # ── Colors ────────────────────────────────────────────────────────────
    if w.get("colors"):
        args.append(f"colors={_fmt_val(w['colors'])}")
    elif w.get("palette"):
        args.append(f"palette={repr(w['palette'])}")

    # ── Layout ────────────────────────────────────────────────────────────
    args.append(f"col={w.get('col', 0)}")
    args.append(f"colspan={w.get('colspan', 12)}")
    default_h = 320 if wtype not in ("gauge",) else 260
    if w.get("h", default_h) != default_h:
        args.append(f"height={w['h']}")

    # ── Refresh ───────────────────────────────────────────────────────────
    if w.get("refresh"):
        args.append(f"refresh={w['refresh']}")

    # ── Chart-specific options ────────────────────────────────────────────
    opts = w.get("options", {}) or {}
    for opt_key, default_val in CHART_OPTS.get(wtype, []):
        val = opts.get(opt_key, w.get(opt_key, default_val))
        if val != default_val and val is not None:
            args.append(f"{opt_key}={_fmt_val(val)}")

    # ── Multi-line formatting ─────────────────────────────────────────────
    if len(args) <= 3:
        return constructor + "(" + ", ".join(args) + ")"

    lines = [f"{constructor}("]
    for idx, arg in enumerate(args):
        comma = "," if idx < len(args) - 1 else ""
        lines.append(f"{i4}{arg}{comma}")
    lines.append(f"{indent})")
    return "\n".join(lines)


def _kpi_to_code(k: Dict, indent: str = "            ") -> str:
    args = [repr(k.get("title", "")), repr(str(k.get("value", "")))]
    if k.get("change") is not None:
        args.append(f"change={k['change']}")
    if k.get("prefix") is not None:
        args.append(f"prefix={repr(k['prefix'])}")
    if k.get("suffix") is not None:
        args.append(f"suffix={repr(k['suffix'])}")
    return f"cc.KPI({', '.join(args)})"


def _filter_to_code(f: Dict, indent: str = "            ") -> str:
    fid   = f.get("filter_id") or f.get("id", "filter1")
    label = f.get("label", fid)
    ftype = f.get("filter_type", "select")
    opts  = f.get("filter_options", [])
    args  = [repr(fid), f"label={repr(label)}", f"type={repr(ftype)}"]
    if opts:
        args.append(f"options={_fmt_val(opts)}")
    return f"cc.Filter({', '.join(args)})"


# ─── Python script generation ────────────────────────────────────────────────

def generate(state: Dict) -> str:
    """
    Convert builder canvas state dict to a Python script string.

    state = {
        "title": str,
        "theme": str,
        "widgets": [...],           # for single-page
        "pages": [{                 # for multi-page
            "path": str,
            "title": str,
            "widgets": [...]
        }]
    }
    """
    title   = state.get("title", "Dashboard")
    theme   = state.get("theme", "midnight")
    widgets = state.get("widgets", [])
    pages   = state.get("pages", [{"path": "/", "widgets": widgets, "title": title}])

    lines = [
        "import chartcraft as cc",
        "",
        f'app = cc.App({repr(title)}, theme={repr(theme)})',
        "",
    ]

    for page in pages:
        page_path    = page.get("path", "/")
        page_title   = page.get("title", title)
        page_widgets = page.get("widgets", [])
        fn_name      = page_path.strip("/").replace("/", "_").replace("-", "_") or "home"

        lines += [
            f'@app.page({repr(page_path)})',
            f"def {fn_name}():",
            f'    """{page_title}"""',
            f"    return cc.Dashboard(",
            f"        title={repr(page_title)},",
        ]

        # Subtitle
        subtitle = page.get("subtitle", "")
        if subtitle:
            lines.append(f"        subtitle={repr(subtitle)},")

        # Filters
        filters = [w for w in page_widgets if w.get("type") == "filter"]
        if filters:
            lines.append("        filters=[")
            for f in filters:
                lines.append(f"            {_filter_to_code(f)},")
            lines.append("        ],")

        # KPIs
        kpis = [w for w in page_widgets if w.get("type") == "kpi"]
        if kpis:
            lines.append("        kpis=[")
            for k in kpis:
                lines.append(f"            {_kpi_to_code(k)},")
            lines.append("        ],")

        # Charts (everything except kpi/filter)
        charts = [w for w in page_widgets
                  if w.get("type") not in ("kpi", "filter")]
        if charts:
            lines.append("        charts=[")
            for w in charts:
                code = _widget_to_code(w, indent="            ")
                # Handle multiline widget code
                for ci, cl in enumerate(code.split("\n")):
                    if ci == 0:
                        lines.append(f"            {cl}")
                    else:
                        lines.append(cl)
                lines[-1] += ","
            lines.append("        ],")

        lines += ["    )", ""]

    lines += ['if __name__ == "__main__":', "    app.run()", ""]
    return "\n".join(lines)


# ─── Jupyter notebook export ─────────────────────────────────────────────────

def generate_notebook(state: Dict) -> str:
    """Return a .ipynb JSON string wrapping the generated Python code."""
    code = generate(state)
    title = state.get("title", "Dashboard")

    cells = [
        {
            "cell_type": "markdown",
            "metadata": {},
            "source": [f"# {title}\n\nGenerated by [ChartCraft](https://github.com/stephenbaraik/chartcraft)."],
        },
        {
            "cell_type": "code",
            "execution_count": None,
            "metadata": {},
            "outputs": [],
            "source": ["# Install ChartCraft if needed\n", "# !pip install chartcraft\n"],
        },
        {
            "cell_type": "code",
            "execution_count": None,
            "metadata": {},
            "outputs": [],
            "source": code.splitlines(keepends=True),
        },
    ]

    notebook = {
        "nbformat": 4,
        "nbformat_minor": 5,
        "metadata": {
            "kernelspec": {"display_name": "Python 3", "language": "python", "name": "python3"},
            "language_info": {"name": "python", "version": "3.11.0"},
        },
        "cells": cells,
    }
    return json.dumps(notebook, indent=2)


# ─── Docker project export ────────────────────────────────────────────────────

_DOCKERFILE = """\
FROM python:3.11-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY app.py .

EXPOSE 8050

CMD ["python", "app.py"]
"""

_REQUIREMENTS = "chartcraft\n"

_DOCKER_COMPOSE = """\
version: "3.9"
services:
  dashboard:
    build: .
    ports:
      - "8050:8050"
    environment:
      - CC_HOST=0.0.0.0
      - CC_PORT=8050
"""

_README = """\
# ChartCraft Dashboard

## Run locally

```bash
pip install chartcraft
python app.py
```

Open http://localhost:8050

## Run with Docker

```bash
docker compose up --build
```

Open http://localhost:8050
"""


def generate_docker_zip(state: Dict) -> bytes:
    """Return a ZIP archive bytes containing app.py + Dockerfile + docker-compose.yml."""
    code = generate(state)
    buf = io.BytesIO()
    with zipfile.ZipFile(buf, "w", zipfile.ZIP_DEFLATED) as zf:
        zf.writestr("app.py", code)
        zf.writestr("Dockerfile", _DOCKERFILE)
        zf.writestr("requirements.txt", _REQUIREMENTS)
        zf.writestr("docker-compose.yml", _DOCKER_COMPOSE)
        zf.writestr("README.md", _README)
    return buf.getvalue()
