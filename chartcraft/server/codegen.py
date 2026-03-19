"""
Code generator — converts builder canvas state to a valid Python script.
"""

from __future__ import annotations
from typing import Any, Dict, List


CHART_TYPE_MAP = {
    "bar": "cc.Bar",
    "line": "cc.Line",
    "area": "cc.Area",
    "pie": "cc.Pie",
    "donut": "cc.Donut",
    "scatter": "cc.Scatter",
    "heatmap": "cc.Heatmap",
    "radar": "cc.Radar",
    "waterfall": "cc.Waterfall",
    "funnel": "cc.Funnel",
    "treemap": "cc.Treemap",
    "sankey": "cc.Sankey",
    "gauge": "cc.Gauge",
    "candlestick": "cc.Candlestick",
    "histogram": "cc.Histogram",
    "boxplot": "cc.BoxPlot",
    "table": "cc.Table",
    "metric": "cc.Metric",
}


def _fmt_val(v: Any) -> str:
    if isinstance(v, str):
        return repr(v)
    if isinstance(v, bool):
        return "True" if v else "False"
    if isinstance(v, list):
        return "[" + ", ".join(_fmt_val(x) for x in v) + "]"
    return str(v)


def _widget_to_code(w: Dict, indent: str = "        ") -> str:
    wtype = w.get("type", "bar")
    constructor = CHART_TYPE_MAP.get(wtype, "cc.Bar")

    args = []

    # Data
    data = w.get("data")
    if data:
        args.append(f"data={_fmt_val(data)}")

    # Axis columns
    if w.get("x"):
        args.append(f"x={repr(w['x'])}")
    if w.get("y"):
        args.append(f"y={repr(w['y'])}")

    # Common display
    if w.get("title"):
        args.append(f"title={repr(w['title'])}")
    if w.get("subtitle"):
        args.append(f"subtitle={repr(w['subtitle'])}")

    # Colors
    if w.get("colors"):
        args.append(f"colors={_fmt_val(w['colors'])}")
    elif w.get("palette"):
        args.append(f"palette={repr(w['palette'])}")

    # Layout
    args.append(f"col={w.get('col', 0)}")
    args.append(f"colspan={w.get('colspan', 12)}")
    if w.get("height", 400) != 400:
        args.append(f"height={w['height']}")

    # Refresh
    if w.get("refresh"):
        args.append(f"refresh={w['refresh']}")

    # Chart-specific options
    opts = w.get("options", {})
    for k, v in opts.items():
        if v not in (None, False, "", []):
            args.append(f"{k}={_fmt_val(v)}")

    lines = [f"{constructor}("]
    for i, arg in enumerate(args):
        comma = "," if i < len(args) - 1 else ""
        lines.append(f"{indent}    {arg}{comma}")
    lines.append(f"{indent})")
    return "\n".join(lines)


def generate(state: Dict) -> str:
    """
    Convert builder canvas state dict to a Python script string.

    state = {
        "title": str,
        "theme": str,
        "widgets": [{ type, title, col, colspan, height, colors, options, ... }]
    }
    """
    title = state.get("title", "Dashboard")
    theme = state.get("theme", "default")
    widgets = state.get("widgets", [])
    pages = state.get("pages", [{"path": "/", "widgets": widgets, "title": title}])

    lines = [
        "import chartcraft as cc",
        "",
        f'app = cc.App("{title}", theme="{theme}")',
        "",
    ]

    for page in pages:
        page_path = page.get("path", "/")
        page_title = page.get("title", title)
        page_widgets = page.get("widgets", [])
        fn_name = page_path.strip("/").replace("/", "_").replace("-", "_") or "home"

        lines += [
            f'@app.page("{page_path}")',
            f"def {fn_name}():",
            f'    """{"Overview" if page_path == "/" else page_title}"""',
            f"    return cc.Dashboard(",
            f"        title={repr(page_title)},",
        ]

        # KPIs
        kpis = [w for w in page_widgets if w.get("type") == "kpi"]
        if kpis:
            lines.append("        kpis=[")
            for k in kpis:
                v = k.get("value", "")
                chg = k.get("change")
                kpi_args = [f"title={repr(k.get('title', ''))}", f"value={repr(str(v))}"]
                if chg is not None:
                    kpi_args.append(f"change={chg}")
                lines.append(f"            cc.KPI({', '.join(kpi_args)}),")
            lines.append("        ],")

        # Charts
        charts = [w for w in page_widgets if w.get("type") not in ("kpi", "filter")]
        if charts:
            lines.append("        charts=[")
            for w in charts:
                code = _widget_to_code(w, indent="            ")
                lines.append(f"            {code},")
            lines.append("        ],")

        lines += [
            "    )",
            "",
        ]

    lines += [
        'if __name__ == "__main__":',
        "    app.run()",
        "",
    ]

    return "\n".join(lines)
