<div align="center">

<br/>

```
◆◆◆◆◆◆◆◆◆◆◆◆◆◆◆◆◆◆◆◆◆◆◆◆◆◆◆◆◆◆◆◆◆◆◆◆◆◆◆◆◆◆◆◆
◆                                                ◆
◆   ██████╗ ██╗  ██╗ █████╗ ██████╗ ████████╗     ◆
◆  ██╔════╝ ██║  ██║██╔══██╗██╔══██╗╚══██╔══╝     ◆
◆  ██║      ███████║███████║██████╔╝   ██║        ◆
◆  ██║      ██╔══██║██╔══██║██╔══██╗   ██║        ◆
◆  ╚██████╗ ██║  ██║██║  ██║██║  ██║   ██║        ◆
◆   ╚═════╝ ╚═╝  ╚═╝╚═╝  ╚═╝╚═╝  ╚═╝   ╚═╝        ◆
◆                                                ◆
◆            C  H  A  R  T   C  R  A  F  T        ◆
◆                                                ◆
◆◆◆◆◆◆◆◆◆◆◆◆◆◆◆◆◆◆◆◆◆◆◆◆◆◆◆◆◆◆◆◆◆◆◆◆◆◆◆◆◆◆◆◆
```

### **Python-powered dashboards that rival Power BI & Tableau.**

*Write Python. Get a stunning, interactive, real-time dashboard — instantly.*

<br/>

[![Python](https://img.shields.io/badge/Python-3.11%2B-3776AB?style=for-the-badge&logo=python&logoColor=white)](https://python.org)
[![ECharts](https://img.shields.io/badge/ECharts-5.5-E14329?style=for-the-badge&logo=apache&logoColor=white)](https://echarts.apache.org)
[![License](https://img.shields.io/badge/License-MIT-10B981?style=for-the-badge)](LICENSE)
[![Dependencies](https://img.shields.io/badge/Dependencies-Zero-8B5CF6?style=for-the-badge)](#)
[![Server](https://img.shields.io/badge/Server-SSE%20Streaming-EC4899?style=for-the-badge)](#)

<br/>

[**Quickstart**](#-quickstart) · [**Charts**](docs/charts.md) · [**Builder**](docs/builder.md) · [**Docs**](docs/index.md)

<br/>

</div>

---

<br/>

## The Pitch

> **One codebase. Two workflows. Zero friction.**

Most tools make you choose — write code *or* use a visual interface. ChartCraft refuses that tradeoff. The **Dashboard Builder** is a full-screen drag-and-drop canvas that generates live Python code as you design. Edit the Python — the canvas updates. Drag a widget — the code updates. They are always in sync.

No build step. No npm. No JavaScript knowledge required. Just Python.

<br/>

```
  You write Python         ◄───►      You drag & drop
        │                                    │
        ▼                                    ▼
  ┌─────────────┐               ┌────────────────────┐
  │  @app.page  │               │   /builder canvas  │
  │  cc.Bar()   │  ◄──  SSE ──► │  drag, resize,     │
  │  cc.Line()  │               │  color pick, align  │
  └─────────────┘               └────────────────────┘
        │                                    │
        └──────────────┬─────────────────────┘
                       ▼
            http://localhost:8050
```

<br/>

---

<br/>

## ⚡ Quickstart

```bash
pip install chartcraft
```

```python
import chartcraft as cc

app = cc.App("Sales Intelligence", theme="midnight")

@app.page("/")
def overview():
    return cc.Dashboard(
        title="Sales Overview",
        subtitle="Real-time performance · Updated live",
        kpis=[
            cc.KPI("Revenue",    "$4.2M",  change=+12.5),
            cc.KPI("Users",      "45,231", change=-3.2),
            cc.KPI("Conversion", "4.8%",   change=+0.5),
            cc.KPI("NPS",        "72",     change=+5.0),
        ],
        filters=[
            cc.Filter("region", label="Region", type="select",
                      options=["All", "North", "South", "East", "West"]),
        ],
        charts=[
            cc.Line(
                {"month": ["Jan","Feb","Mar","Apr","May","Jun"],
                 "revenue": [310, 280, 350, 420, 390, 480],
                 "target":  [300, 300, 350, 400, 400, 450]},
                x="month", y=["revenue", "target"],
                title="Revenue vs Target",
                col=0, colspan=8, smooth=True,
                colors=["#8B5CF6", "#3F3F46"],
            ),
            cc.Donut(
                {"Enterprise": 45, "Professional": 30, "Starter": 25},
                title="Plan Distribution",
                col=8, colspan=4,
                inner_radius="55%", center_text="Plans",
            ),
        ],
    )

app.run()
# ◆ ChartCraft  →  http://localhost:8050
# Builder       →  http://localhost:8050/builder
```

<br/>

---

<br/>

## 📊 18+ Chart Types

Built on **Apache ECharts 5.5** with GPU-accelerated canvas rendering.

<br/>

| Category | Types |
|----------|-------|
| **Trend** | `cc.Line` · `cc.Area` · `cc.Bar` |
| **Part-to-Whole** | `cc.Pie` · `cc.Donut` · `cc.Treemap` · `cc.Funnel` |
| **Distribution** | `cc.Scatter` · `cc.Bubble` · `cc.Histogram` · `cc.BoxPlot` · `cc.Heatmap` |
| **Comparison** | `cc.Radar` · `cc.Waterfall` · `cc.Gauge` |
| **Specialized** | `cc.Candlestick` · `cc.Sankey` · `cc.Table` · `cc.Metric` |
| **Layout** | `cc.SectionHeader` · `cc.Divider` · `cc.Spacer` · `cc.TextBlock` |

<br/>

Every chart accepts the same mental model:

```python
#           data          position    size
cc.Bar(  monthly_sales,  col=0,  colspan=8,  height=360,

#       title          colors              refresh
        title="Sales", colors=["#8B5CF6"], refresh=5  )
#                                                  ↑
#                                        push new data every 5s via SSE
```

<br/>

---

<br/>

## 🎨 Themes

11 built-in themes. Switch live in the browser — no reload required.

<br/>

```
  midnight   │ ████ deep purple bg · purple accent
  obsidian   │ ████ pitch black  · cyan accent
  default    │ ████ dark zinc    · indigo accent
  ember      │ ████ warm dark    · orange accent
  jade       │ ████ forest dark  · green accent
  candy      │ ████ pink dark    · magenta accent
  arctic     │ ████ ice dark     · sky blue accent
  retro      │ ████ vintage teal · gold accent
  ──────────────────────────────────────────────
  frost      │ ░░░░ clean light  · blue accent
  slate      │ ░░░░ professional · navy accent
  scientific │ ░░░░ academic     · slate accent
```

```python
app = cc.App("Dashboard", theme="midnight")

# Override on any individual chart
cc.Bar(data, palette="sunset")

# Build your own
cc.register_theme("brand", cc.Theme(
    bg="#0A0A0A", accent="#FF6B00",
    font_display="Outfit", palette="aurora",
))
```

<br/>

---

<br/>

## ⚡ Real-Time Streaming

ChartCraft uses **Server-Sent Events** to push full chart spec updates to every connected browser. No WebSocket library. No polling. Zero frontend code.

```python
import time, math, random

@app.page("/live")
def live():
    return cc.Dashboard(
        title="Live Metrics",
        kpis=[
            # Refreshes every 4 seconds — calls data_fn on a background thread
            cc.KPI("Active Sessions",
                   data_fn=lambda: f"{random.randint(1200, 1800):,}",
                   refresh=4),
        ],
        charts=[
            # Full chart spec is pushed via SSE — browser animates the update
            cc.Line(
                data_fn=lambda: [
                    {"ts": int(time.time()) - i * 5,
                     "value": round(50 + 20 * math.sin(time.time() / 10 - i * 0.3), 2)}
                    for i in range(60, -1, -1)
                ],
                x="ts", y="value",
                title="Live Event Stream",
                refresh=3, smooth=True, show_dots=False,
                col=0, colspan=12,
            ),
        ],
    )
```

Each component refreshes **independently** on its own interval. A KPI can update every 2 seconds while a chart updates every 30.

<br/>

---

<br/>

## 🔌 Connect to Anything

```python
# SQLite — zero extra dependencies
db = cc.connect_sql("sqlite:///analytics.db")

# PostgreSQL
db = cc.connect_sql("postgresql://user:pass@host:5432/db")

# MySQL
db = cc.connect_sql("mysql+pymysql://user:pass@host/db")

# CSV files or entire directory
csv = cc.connect_csv("./data/")

# Any REST API
api = cc.connect_api("https://api.example.com",
                     headers={"Authorization": "Bearer ..."})
```

```python
# Use it directly in charts — re-executes on every refresh
cc.Line(
    data_fn=lambda: db.query_dict(
        "SELECT month, SUM(revenue) revenue FROM sales GROUP BY month"
    ),
    x="month", y="revenue",
    refresh=30,
)
```

<br/>

---

<br/>

## 🖱️ Visual Dashboard Builder

Open `http://localhost:8050/builder` and design without writing a single line.

```
┌──────────────────────────────────────────────────────────────────┐
│  ◆ ChartCraft Builder                          [Save] [Export ▾] │
├──────────┬───────────────────────────────────────┬───────────────┤
│          │                                       │               │
│  CHARTS  │          CANVAS                       │  PROPERTIES   │
│          │                                       │               │
│  ▸ Bar   │   ╔══════════════╗  ╔══════════╗      │  ┌─ Data ────┐ │
│  ▸ Line  │   ║              ║  ║          ║      │  │ SQL editor│ │
│  ▸ Pie   │   ║   Bar Chart  ║  ║  Donut   ║      │  │ Run ►     │ │
│  ▸ Area  │   ║   ░░░▓▓▓███  ║  ║  ◉ 45%  ║      │  └───────────┘ │
│  ▸ Gauge │   ╚══════════════╝  ╚══════════╝      │  ┌─ Style ───┐ │
│  ▸ ...   │                                       │  │ 🎨 Colors │ │
│          │   ╔════════════════════════════╗      │  │ Palette ▾ │ │
│  FILTERS │   ║    Line Chart — Revenue    ║      │  └───────────┘ │
│  ▸ Drop  │   ║  ∿∿∿∿∿∿∿∿∿∿∿∿∿∿∿∿∿∿∿∿∿∿  ║      │  ┌─ Layout ──┐ │
│  ▸ Slide │   ╚════════════════════════════╝      │  │ col  span │ │
│  ▸ Date  │                                       │  │  0    8   │ │
│          │                                       │  └───────────┘ │
├──────────┴───────────────────────────────────────┴───────────────┤
│  CODE PREVIEW  ●                                      [Parse]    │
│  cc.Bar(data, x="month", y="revenue", col=0, colspan=8)          │
└──────────────────────────────────────────────────────────────────┘
```

- **Drag** any chart from the sidebar onto the canvas
- **Resize** with 8-point handles · **Multi-select** with Shift+click
- **Color picker** — HSV wheel, palettes, harmonies, gradient editor
- **Undo / Redo** — full history stack (`Ctrl+Z` / `Ctrl+Shift+Z`)
- **Code panel** — edit Python directly · canvas updates instantly
- **Export** to `.py`, `.ipynb`, or Docker `.zip` in one click

<br/>

---

<br/>

## 🔄 Bidirectional Sync

The builder and your Python code are two views of the same state.

```
  Drag chart to col 4         ──►   col=4 appears in code panel
  Set color to #8B5CF6        ──►   colors=["#8B5CF6"] in code
  Type col=8 in code panel    ──►   widget snaps to column 8
  Paste a full page() block   ──►   canvas rebuilds from scratch
```

The generated code is always valid, always runnable:

```bash
python my_exported_dashboard.py
# → http://localhost:8050  (identical to what you designed)
```

<br/>

---

<br/>

## 🔒 Authentication

```python
# HTTP Basic Auth (browser login prompt · username: admin)
app.run(password="my-password")

# Bearer token (for APIs and scripts)
app.run(token="my-token")
# → http://localhost:8050/?token=my-token

# Both simultaneously
app.run(password="pw", token="api-key")
```

<br/>

---

<br/>

## 📦 Export Everywhere

```python
# Self-contained HTML — no server, no Python, share via email or S3
app.save("dashboard.html")
app.save_all("dist/")          # → dist/index.html, dist/sales.html, ...

# Jupyter notebook (.ipynb) — runnable cells, shareable
# → GET /api/export/notebook

# Docker project — Dockerfile + compose + app.py in a .zip
# → GET /api/export/docker

# PDF via Playwright (pip install "chartcraft[pdf]")
# → GET /api/export/pdf?page=/
```

<br/>

---

<br/>

## ⚖️ How It Compares

<br/>

|  | **ChartCraft** | Power BI | Tableau | Plotly Dash | Streamlit |
|--|:-:|:-:|:-:|:-:|:-:|
| Pure Python API | ✅ | ❌ | ❌ | ✅ | ✅ |
| Drag-and-drop visual builder | ✅ | ✅ | ✅ | ❌ | ❌ |
| Bidirectional code ↔ canvas | ✅ | ❌ | ❌ | ❌ | ❌ |
| Zero required dependencies | ✅ | ❌ | ❌ | ❌ | ❌ |
| Real-time SSE push | ✅ | ❌ | ❌ | ✅ | ✅ |
| Self-hosted & open source | ✅ | ❌ | ❌ | ✅ | ✅ |
| Export to standalone HTML | ✅ | limited | limited | ❌ | ❌ |
| PDF / Jupyter / Docker export | ✅ | partial | partial | ❌ | ❌ |
| No build step / no npm | ✅ | ✅ | ✅ | ❌ | ✅ |

<br/>

---

<br/>

## 🛠 Tech Stack

<br/>

```
  Python 3.11+  ──  http.server · threading · sqlite3 · ast (all stdlib)
  ECharts 5.5   ──  GPU canvas · 20+ chart types · responsive · ARIA
  Preact 10     ──  3KB React-compatible · no build step · CDN only
  SSE           ──  text/event-stream · auto-reconnect · zero deps
  SQLite        ──  project persistence · connector registry · stdlib
```

<br/>

---

<br/>

## 📁 Structure

```
chartcraft/
├── core/
│   ├── models.py          ← all chart types, KPI, Dashboard, Filter
│   ├── theme.py           ← 11 themes, Theme dataclass, CSS export
│   └── colors.py          ← 16 palettes, ColorScale, harmony generators
├── connectors/
│   ├── sql.py             ← SQLite (stdlib) + SQLAlchemy optional
│   ├── csv_connector.py   ← CSV / TSV, auto type detection
│   └── api.py             ← REST connector, urllib only
├── server/
│   ├── handler.py         ← HTTP routes + auth + TTL spec cache
│   ├── sse.py             ← SSE manager, broadcast, refresh threads
│   ├── codegen.py         ← canvas state → Python + .ipynb + Docker
│   ├── parser.py          ← Python AST → canvas state
│   ├── projects.py        ← SQLite project save/load
│   └── query_api.py       ← SQL execution + connector registry
├── builder/
│   ├── builder.html       ← visual builder SPA (Preact + HTM)
│   └── components/
│       └── color_picker.js ← HSV wheel · palettes · harmonies · gradient
└── static/
    └── viewer.html        ← dashboard viewer SPA (vanilla JS + ECharts)
```

<br/>

---

<br/>

## 📚 Documentation

<br/>

| | Guide | What's inside |
|--|-------|---------------|
| 🚀 | [Getting Started](docs/getting-started.md) | Install, first dashboard, core concepts, grid layout |
| 📊 | [Chart Types](docs/charts.md) | All 18+ types — examples, options, data format per type |
| 🎨 | [Themes & Colors](docs/themes-and-colors.md) | Themes, palettes, custom branding, color utilities |
| 🔌 | [Data Sources](docs/data-sources.md) | SQL, CSV, REST — all methods and connection strings |
| 🎛 | [Filters & Interactivity](docs/filters-and-interactivity.md) | Filter types, cascading, cross-filtering, URL state |
| ⚡ | [Real-Time Data](docs/realtime.md) | SSE internals, refresh intervals, LIVE badge |
| 🖱 | [Visual Builder](docs/builder.md) | Canvas, color picker, code sync, keyboard shortcuts |
| 📦 | [Export & Deployment](docs/export-and-deployment.md) | HTML, PDF, Jupyter, Docker, nginx, cloud platforms |
| 🔒 | [Authentication](docs/authentication.md) | Basic auth, bearer tokens, env vars, security |
| 📖 | [API Reference](docs/api-reference.md) | Every class, method, parameter, HTTP endpoint |

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
