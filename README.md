<div align="center">

# ◆ ChartCraft

**Python-powered dashboards that rival Power BI & Tableau.**

Write Python. Get a stunning, interactive, real-time dashboard — instantly.

[![Python 3.11+](https://img.shields.io/badge/python-3.11%2B-blue?style=flat-square)](https://python.org)
[![Zero Dependencies](https://img.shields.io/badge/dependencies-zero-brightgreen?style=flat-square)](#)
[![MIT License](https://img.shields.io/badge/license-MIT-green?style=flat-square)](LICENSE)
[![ECharts 5.5](https://img.shields.io/badge/charts-ECharts%205.5-orange?style=flat-square)](https://echarts.apache.org)

</div>

---

```python
import chartcraft as cc

app = cc.App("Sales Dashboard", theme="midnight")

@app.page("/")
def home():
    return cc.Dashboard(
        title="Sales Overview",
        kpis=[
            cc.KPI("Revenue", "$4.2M",  change=12.5),
            cc.KPI("Users",   "45,231", change=-3.2),
            cc.KPI("NPS",     "72",     change=5.0),
        ],
        charts=[
            cc.Line(data, x="month", y=["revenue", "target"],
                    title="Revenue vs Target", col=0, colspan=8),
            cc.Donut({"Enterprise": 45, "Pro": 30, "Free": 25},
                     title="Plan Split",        col=8, colspan=4),
        ],
    )

app.run()  # → http://localhost:8050
```

---

## Why ChartCraft?

Most dashboard tools make you choose: write code *or* use a GUI. ChartCraft does both — simultaneously.

The **Dashboard Builder** at `/builder` is a Figma-like drag-and-drop canvas. Every widget you place generates Python code in real-time. Every Python change reflects on the canvas. They stay in perfect sync — always.

| | ChartCraft | Power BI / Tableau | Plotly Dash | Streamlit |
|--|:---:|:---:|:---:|:---:|
| Pure Python API | ✅ | ❌ | ✅ | ✅ |
| Visual drag-and-drop builder | ✅ | ✅ | ❌ | ❌ |
| Bidirectional code ↔ canvas sync | ✅ | ❌ | ❌ | ❌ |
| Zero required dependencies | ✅ | ❌ | ❌ | ❌ |
| Real-time SSE streaming | ✅ | ❌ | ✅ | ✅ |
| Self-hosted & open source | ✅ | ❌ | ✅ | ✅ |
| Export to HTML / Docker / PDF | ✅ | limited | ❌ | ❌ |

---

## Features

**18+ Chart Types** — Bar, Line, Area, Pie, Donut, Scatter, Bubble, Heatmap, Radar, Waterfall, Funnel, Treemap, Sankey, Gauge, Candlestick, Histogram, Box Plot, Table — all powered by Apache ECharts 5.5.

**Visual Dashboard Builder** — A full-screen drag-and-drop canvas with live ECharts previews, 8-point resize handles, multi-select, alignment tools, undo/redo, snap-to-grid, and a properties panel with 5 tabs.

**Professional Color Picker** — HSV wheel, RGB/HSL/Hex inputs, EyeDropper API, 16 palette swatches, color harmonies, and a multi-stop gradient editor. Every color you pick writes to the Python code.

**Real-Time Streaming** — Server-Sent Events push full chart spec updates to the browser. Each chart refreshes independently on its own interval. Auto-reconnects on disconnect.

**Interactive Filters** — Dropdowns, multi-select, date range, sliders, text search, and toggles. Cascading options, cross-chart filtering, and filter state encoded in the URL for bookmarkable views.

**Zero Required Dependencies** — SQLite and CSV connectors use Python stdlib only. Add `sqlalchemy` for PostgreSQL/MySQL/SQL Server. Add `playwright` for PDF export.

**Export Everywhere** — Static HTML (no server needed), Jupyter `.ipynb`, Docker project zip, Playwright PDF.

**11 Built-in Themes** · **16 Color Palettes** · **HTTP Auth** · **Lazy Loading** · **ARIA Accessibility** · **Mobile-Responsive**

---

## Installation

```bash
pip install chartcraft
```

With optional extras:

```bash
pip install "chartcraft[sql]"      # PostgreSQL, MySQL, SQL Server
pip install "chartcraft[pg]"       # PostgreSQL (includes psycopg2)
pip install "chartcraft[pandas]"   # Pandas DataFrame support
pip install "chartcraft[pdf]"      # PDF export via Playwright
pip install "chartcraft[full]"     # Everything
```

**Requires Python 3.11+**

---

## Quick Start

### 1 — Static data

```python
import chartcraft as cc

app = cc.App("Analytics", theme="midnight")

@app.page("/")
def overview():
    return cc.Dashboard(
        title="Q4 Overview",
        kpis=[
            cc.KPI("Revenue",    "$4.2M", change=12.5),
            cc.KPI("Conversion", "4.8%",  change=0.5),
        ],
        charts=[
            cc.Bar(
                {"Q1": 100, "Q2": 200, "Q3": 150, "Q4": 300},
                title="Quarterly Sales", col=0, colspan=8,
            ),
            cc.Donut(
                {"Enterprise": 45, "Pro": 30, "Free": 25},
                title="Plan Mix", col=8, colspan=4,
            ),
        ],
    )

app.run()
```

### 2 — Connect to a database

```python
db = cc.connect_sql("sqlite:///analytics.db")
# or: cc.connect_sql("postgresql://user:pass@host/db")

@app.page("/")
def overview():
    data = db.query_dict("SELECT month, revenue FROM sales ORDER BY month")
    return cc.Dashboard(
        charts=[cc.Line(data, x="month", y="revenue", title="Monthly Revenue")],
    )
```

### 3 — Real-time data

```python
@app.page("/live")
def live():
    return cc.Dashboard(
        title="Live Metrics",
        kpis=[
            cc.KPI("Active Users", data_fn=lambda: str(get_user_count()), refresh=5),
        ],
        charts=[
            cc.Line(
                data_fn=lambda: db.query_dict("SELECT ts, value FROM metrics ORDER BY ts DESC LIMIT 100"),
                x="ts", y="value", title="Live Stream",
                refresh=3, smooth=True,
            ),
        ],
    )
```

### 4 — Multi-page with filters

```python
@app.page("/sales")
def sales():
    return cc.Dashboard(
        filters=[
            cc.Filter("region", label="Region", type="select",
                      options=["All", "North", "South", "East", "West"]),
        ],
        charts=[
            cc.Bar(
                data_fn=lambda f={}: db.query_dict(
                    "SELECT month, revenue FROM sales WHERE region=:r GROUP BY month",
                    {"r": f.get("region", "All")}
                ),
                x="month", y="revenue", title="Sales by Month",
                linked_filters=["region"],
            ),
        ],
    )
```

### 5 — Visual Builder

```bash
python app.py
# Then open: http://localhost:8050/builder
```

Drag chart types onto the canvas → adjust properties → see Python generated live → click Export.

---

## Themes

Switch themes in the browser with the **◆** button — or set them in code:

```python
app = cc.App("Dashboard", theme="midnight")   # or: frost, obsidian, ember, jade, ...
```

| `default` | `midnight` | `obsidian` | `frost` | `ember` |
|-----------|-----------|-----------|--------|--------|
| Dark indigo | Deep purple | Pitch black + cyan | Clean light blue | Warm dark orange |

| `jade` | `slate` | `candy` | `arctic` | `retro` | `scientific` |
|--------|--------|--------|---------|--------|-------------|
| Forest green | Professional light | Pink dark | Ice blue | Vintage gold | Academic light |

---

## Data Formats

ChartCraft accepts anything Python developers work with:

```python
# Dict of scalars
{"Chrome": 65, "Firefox": 20, "Safari": 15}

# Dict of lists (multi-series)
{"month": ["Jan","Feb","Mar"], "revenue": [100, 200, 150], "cost": [80, 90, 95]}

# List of dicts (SQL-style records)
[{"month": "Jan", "revenue": 100}, {"month": "Feb", "revenue": 200}]

# SQL query result
db.query_dict("SELECT region, SUM(revenue) FROM sales GROUP BY region")

# Pandas DataFrame
pd.DataFrame({"x": [1, 2, 3], "y": [4, 5, 6]})

# Callable for real-time data
lambda: db.query_dict("SELECT * FROM live_metrics ORDER BY ts DESC LIMIT 50")
```

---

## Export

```python
# Standalone HTML — no server needed
app.save("dashboard.html")
app.save_all("output/")              # All pages → output/index.html, output/sales.html, ...

# PDF (requires chartcraft[pdf])
# GET http://localhost:8050/api/export/pdf?page=/

# Jupyter Notebook
# GET http://localhost:8050/api/export/notebook

# Docker project
# GET http://localhost:8050/api/export/docker
```

---

## Authentication

```python
app.run(password="my-password")          # HTTP Basic Auth (username: admin)
app.run(token="my-api-token")            # Bearer token or ?token= query param
app.run(password="pw", token="token")    # Both
```

---

## Documentation

| Guide | Description |
|-------|-------------|
| [Getting Started](docs/getting-started.md) | Install, run your first dashboard, core concepts |
| [Chart Types](docs/charts.md) | All 18+ chart types — examples, options, data formats |
| [Themes & Colors](docs/themes-and-colors.md) | Themes, palettes, custom branding, color utilities |
| [Data Sources](docs/data-sources.md) | SQL, CSV, REST API connectors — all methods |
| [Filters & Interactivity](docs/filters-and-interactivity.md) | Filter types, cascading, cross-filtering, URL state |
| [Real-Time Data](docs/realtime.md) | SSE streaming, refresh intervals, live KPIs |
| [Visual Builder](docs/builder.md) | Drag-and-drop canvas, color picker, code sync |
| [Export & Deployment](docs/export-and-deployment.md) | HTML, PDF, Jupyter, Docker, nginx, cloud |
| [Authentication](docs/authentication.md) | Password and token auth, security notes |
| [API Reference](docs/api-reference.md) | Every class, method, and parameter |

---

## Project Structure

```
chartcraft/
├── core/
│   ├── models.py          # Chart, KPI, Dashboard, Filter classes
│   ├── theme.py           # 11 built-in themes + custom theme API
│   └── colors.py          # 16 palettes, ColorScale, color utilities
├── connectors/
│   ├── sql.py             # SQLite (stdlib) + SQLAlchemy for other databases
│   ├── csv_connector.py   # CSV / TSV file connector
│   └── api.py             # REST API connector (urllib, zero deps)
├── server/
│   ├── handler.py         # HTTP request handler — all API routes
│   ├── sse.py             # Server-Sent Events connection manager
│   ├── codegen.py         # Canvas state → Python code
│   ├── parser.py          # Python code → canvas state (AST)
│   ├── projects.py        # SQLite project persistence
│   └── query_api.py       # SQL query execution + connector registry
├── builder/
│   ├── builder.html       # Visual builder SPA
│   └── components/
│       └── color_picker.js  # HSV color picker component
└── static/
    └── viewer.html        # Dashboard viewer SPA
```

---

## Tech Stack

| Layer | Technology | Why |
|-------|-----------|-----|
| Backend | Python 3.11+ stdlib | Zero deps: `http.server`, `threading`, `sqlite3`, `ast` |
| Real-time | Server-Sent Events | No library; server→client push; auto-reconnect |
| Charts | Apache ECharts 5.5 (CDN) | 20+ chart types, GPU canvas, responsive, accessible |
| Builder UI | Preact 10 + HTM (CDN) | 3KB React-compatible, no build step required |
| Styling | CSS Custom Properties | Theme switching with zero JavaScript |
| Persistence | SQLite | Projects and connector registry — stdlib only |

---

## License

MIT — free for personal and commercial use.

---

<div align="center">

**◆ ChartCraft** — Python-powered dashboards for everyone.

</div>
