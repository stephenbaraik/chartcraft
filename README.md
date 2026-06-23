<div align="center">

<br/>

```
       ◆◆◆◆◆◆◆◆◆◆◆◆◆◆◆◆◆◆◆◆◆◆◆◆◆◆◆◆◆◆◆◆◆◆◆◆◆◆◆◆◆◆◆◆◆◆◆◆       ◆
       ◆                                                          ◆
       ◆      ██████╗ ██╗  ██╗ █████╗ ██████╗ ████████╗            ◆
       ◆     ██╔════╝ ██║  ██║██╔══██╗██╔══██╗╚══██╔══╝            ◆
       ◆     ██║      ███████║███████║██████╔╝   ██║               ◆
       ◆     ██║      ██╔══██║██╔══██║██╔══██╗   ██║               ◆
       ◆     ╚██████╗ ██║  ██║██║  ██║██║  ██║   ██║               ◆
       ◆      ╚═════╝ ╚═╝  ╚═╝╚═╝  ╚═╝╚═╝  ╚═╝   ╚═╝               ◆
       ◆                                                          ◆
       ◆                   C  H  A  R  T   C  R  A  F  T           ◆
       ◆                                                          ◆
       ◆◆◆◆◆◆◆◆◆◆◆◆◆◆◆◆◆◆◆◆◆◆◆◆◆◆◆◆◆◆◆◆◆◆◆◆◆◆◆◆◆◆◆◆◆◆◆◆◆◆◆◆◆◆◆◆       ◆
```

### **Python-powered dashboards that rival Power BI & Tableau.**

*Write Python. Get a stunning, interactive, real-time dashboard — instantly.*

<br/>

[![Python](https://img.shields.io/badge/Python-3.11%2B-3776AB?style=for-the-badge&logo=python&logoColor=white)](https://python.org)
[![ECharts](https://img.shields.io/badge/ECharts-5.5-E14329?style=for-the-badge&logo=apache&logoColor=white)](https://echarts.apache.org)
[![License](https://img.shields.io/badge/License-MIT-10B981?style=for-the-badge)](LICENSE)
[![Dependencies](https://img.shields.io/badge/Dependencies-Zero-8B5CF6?style=for-the-badge)](#)

<br/>

</div>

---

<br/>

## Quickstart

**Zero dependencies.** Build and serve a financial dashboard on 10,800 real orders in under 50 lines.

```bash
pip install chartcraft
```

```python
import chartcraft as cc

# Data — like pandas, no pandas required
data = cc.Data({
    "month": ["Jan", "Feb", "Mar", "Apr", "May", "Jun"],
    "revenue": [310, 280, 350, 420, 390, 480],
    "profit": [62, 39, 53, 76, 70, 96],
})

dashboard = cc.Dashboard(
    title="Sales Overview",
    charts=[
        cc.bar(data, x="month", y="revenue", title="Revenue"),
        cc.line(data, x="month", y="profit", title="Profit"),
    ],
)

cc.serve(dashboard)
# ◆ ChartCraft → http://localhost:8050
```

Ready-made example on real data:

```bash
python example_app.py
# ◆ Superstore Financial Dashboard
#   Total Revenue: $2,297,200.85
#   Total Profit:  $286,397.06
#   Margin:        12.5%
# ◆ ChartCraft → http://localhost:8050
```

Opens a full interactive dashboard with line, bar, donut, scatter, and area charts — built from 10,800 real Superstore orders.

<br/>

---

<br/>

## Chart Types

Built on **Apache ECharts 5.5** (CDN-loaded). Every chart is a function that takes a `Data` object, an `x` column, a `y` column, and optional styling.

| Function | Type |
|----------|------|
| `cc.bar()` | Vertical / horizontal bar |
| `cc.line()` | Line / multi-series line |
| `cc.area()` | Area / stacked area |
| `cc.pie()` | Pie chart |
| `cc.donut()` | Donut chart |
| `cc.scatter()` | Scatter plot |
| `cc.bubble()` | Bubble chart |
| `cc.histogram()` | Histogram |
| `cc.boxplot()` | Box plot |
| `cc.heatmap()` | Heatmap |
| `cc.radar()` | Radar / spider |
| `cc.waterfall()` | Waterfall chart |
| `cc.gauge()` | Single-value gauge |
| `cc.candlestick()` | Candlestick / OHLC |
| `cc.table()` | Data table |
| `cc.metric()` | Single KPI value |
| `cc.sankey()` | Sankey / flow diagram |
| `cc.treemap()` | Treemap |
| `cc.funnel()` | Funnel chart |

```python
cc.line(data, x="month", y="revenue", title="Revenue Trend",
        smooth=True, colors=["#7C3AED"])
```

<br/>

---

<br/>

## Dashboard

```python
cc.Dashboard(
    title="Executive Dashboard",
    charts=[chart1, chart2, chart3],
    layout="grid",     # grid | free
    columns=2,         # grid columns
    spacing=20,        # gap between cards
)
```

| Option | Default | Description |
|--------|---------|-------------|
| `title` | `""` | Dashboard heading |
| `charts` | `[]` | List of Chart objects |
| `layout` | `"grid"` | Grid or free-form |
| `columns` | `2` | Number of grid columns |
| `spacing` | `20` | Gap between chart cards |
| `theme` | `None` | Pre-built theme name |

Save to self-contained HTML (no server needed):

```python
cc.save(dashboard, "dashboard.html")
```

<br/>

---

<br/>

## Data

```python
# From a dict of lists
data = cc.Data({
    "month": ["Jan", "Feb", "Mar"],
    "sales": [100, 150, 200],
})

# From a list of dicts (auto-converted)
data = cc.DataFrame([
    {"month": "Jan", "sales": 100},
    {"month": "Feb", "sales": 150},
])

# Slice columns
data["month"]   # Series
data[["sales"]]  # DataFrame
```

The `Data` class provides a familiar pandas-like interface — column access, slicing, filtering — with zero external dependencies.

<br/>

---

<br/>

## Themes

```python
# Apply a pre-built theme
cc.theme(background="#0f0f1a", card_background="#1a1a2e")

# Shortcuts
cc.apply_dark_theme()
cc.apply_light_theme()
cc.apply_vibrant_theme()

# Export theme as CSS
css = cc.export_theme()

# Reset
cc.reset_theme()
```

<br/>

---

<br/>

## Serving

```python
# Local dev server (default port 8050)
cc.serve(dashboard)

# Custom port
cc.serve(dashboard, port=8080)

# Export to HTML (standalone, no Python needed)
cc.save(dashboard, "report.html")

# Export all pages
cc.save_all("dist/")
```

The server uses Python's stdlib `http.server` — no dependencies beyond Python 3.11+.

<br/>

---

<br/>

## Visual Builder

Programmatic chart assembly without manual JSON:

```python
import chartcraft as cc
from chartcraft.visual_builder import set_title, add_bar, add_line, build_dashboard

set_title("Custom Dashboard")
add_bar(data, x="month", y="revenue")
add_line(data, x="month", y="profit")
dashboard = build_dashboard()
cc.serve(dashboard)
```

<br/>

---

<br/>

## Connect to Data

```python
# CSV file
from chartcraft.connectors.csv_connector import read_csv
data = read_csv("data/superstore.csv")

# SQL
from chartcraft.connectors.sql import SQLConnector
db = SQLConnector("sqlite:///analytics.db")
rows = db.query("SELECT month, SUM(sales) FROM sales GROUP BY month")
```

Connectors are optional, lazily imported, and work with any data source that returns rows.

<br/>

---

<br/>

## Comparison

|  | **ChartCraft** | Power BI | Tableau | Plotly Dash | Streamlit |
|--|:-:|:-:|:-:|:-:|:-:|
| Pure Python API | ✅ | ❌ | ❌ | ✅ | ✅ |
| Zero dependencies | ✅ | ❌ | ❌ | ❌ | ❌ |
| Self-hosted & open source | ✅ | ❌ | ❌ | ✅ | ✅ |
| Export to standalone HTML | ✅ | limited | limited | ❌ | ❌ |
| ECharts-powered rendering | ✅ | ❌ | ❌ | ❌ | ❌ |
| No build step / no npm | ✅ | ✅ | ✅ | ❌ | ✅ |
| Real data example included | ✅ | ❌ | ❌ | ❌ | ❌ |

<br/>

---

<br/>

## Tech Stack

```
Python 3.11+     http.server · threading · csv · collections (all stdlib)
ECharts 5.5      GPU canvas · 19+ chart types · responsive
No build step    No npm · No node · No webpack
```

<br/>

---

<br/>

## Structure

```
chartcraft/
├── __init__.py            # Public API — Data, charts, serve, save
├── data.py                # Data, Series, DataFrame classes
├── charts.py              # 19 chart functions (bar, line, pie, …)
├── dashboard.py           # Dashboard container
├── render.py              # HTML renderer + HTTP server
├── themes.py              # Theme presets and customization
├── visual_builder.py      # Programmatic builder helpers
├── core/
│   ├── models.py          # Chart model dataclasses
│   ├── theme.py           # Theme data structures
│   ├── colors.py          # Color utilities
│   └── serializer.py      # JSON serialization
├── server/
│   ├── app_server.py      # ThreadingHTTPServer
│   ├── handler.py         # HTTP request handler
│   ├── parser.py          # Dashboard parsing
│   ├── codegen.py         # HTML/JS code generation
│   ├── query_api.py       # SQL query REST API
│   ├── projects.py        # Project management
│   └── sse.py             # Server-Sent Events
├── connectors/
│   ├── sql.py             # SQL connector
│   ├── csv_connector.py   # CSV reader
│   └── api.py             # REST API connector
├── builder/               # Visual builder UI
└── static/
    └── viewer.html        # Dashboard viewer template
```

<br/>

---

<br/>

## Documentation

| Guide | Contents |
|-------|---------|
| Getting Started | Install, first dashboard, core concepts |
| Chart Types | All 19 types — examples, options, data format |
| Themes & Colors | Theme presets, custom CSS, color palettes |
| Data Sources | CSV, SQL, REST — all connection methods |
| Deployment | Self-contained HTML, custom ports, nginx |

<br/>

---

<br/>

<div align="center">

```
◆◆◆◆◆◆◆◆◆◆◆◆◆◆◆◆◆◆◆◆◆◆◆◆◆◆◆◆◆◆◆◆◆◆◆
◆                                   ◆
◆   pip install chartcraft          ◆
◆                                   ◆
◆◆◆◆◆◆◆◆◆◆◆◆◆◆◆◆◆◆◆◆◆◆◆◆◆◆◆◆◆◆◆◆◆◆◆
```

**MIT License** · Built with Python · Powered by ECharts

</div>
