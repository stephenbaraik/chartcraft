<div align="center">

```
  ██████╗██╗  ██╗ █████╗ ██████╗ ████████╗
 ██╔════╝██║  ██║██╔══██╗██╔══██╗╚══██╔══╝
 ██║     ███████║███████║██████╔╝   ██║
 ██║     ██╔══██║██╔══██║██╔══██╗   ██║
 ╚██████╗██║  ██║██║  ██║██║  ██║   ██║
  ╚═════╝╚═╝  ╚═╝╚═╝  ╚═╝╚═╝  ╚═╝   ╚═╝
```

### Python-powered dashboards that rival Power BI & Tableau.

*Write Python. Get a stunning, interactive, real-time dashboard — instantly.*

<br/>

[![Python](https://img.shields.io/badge/Python-3.11%2B-3776AB?style=for-the-badge&logo=python&logoColor=white)](https://python.org)
[![ECharts](https://img.shields.io/badge/ECharts-5.5-E14329?style=for-the-badge&logo=apache&logoColor=white)](https://echarts.apache.org)
[![License](https://img.shields.io/badge/License-MIT-10B981?style=for-the-badge)](LICENSE)
[![Deps](https://img.shields.io/badge/Dependencies-Zero-8B5CF6?style=for-the-badge)](#)
[![SSE](https://img.shields.io/badge/Server-SSE%20Streaming-EC4899?style=for-the-badge)](#)

<br/>

[**Quickstart**](#-quickstart) · [**Docs**](docs/getting-started.md) · [**Presets & Builders**](docs/presets-and-page-builders.md) · [**Data Sources**](docs/data-sources.md) · [**API Reference**](docs/api-reference.md)

<br/>

</div>

---

## ◆ Three API Layers

Choose the level that matches how fast you want to move:

| Layer | What it is | Use when |
|-------|-----------|----------|
| **Core classes** | `cc.Dashboard`, `cc.Bar`, `cc.Line`, `cc.KPI`, `cc.Filter` | You need exact control |
| **Presets & helpers** | `cc.Page(...)`, `cc.section(...)`, `cc.trend_line(...)`, `cc.sql_kpi(...)` | You want clean, readable code |
| **Page builders** | `cc.executive_page(...)`, `cc.sales_page(...)`, `cc.customer_page(...)`, `cc.product_page(...)` | Your dashboard fits a common story |

The **Dashboard Builder** at `http://localhost:8050/builder` is a full drag-and-drop canvas that generates live Python code as you design — and stays in sync both ways. No build step. No npm. No JavaScript.

---

## ◆ Quickstart

```bash
pip install chartcraft
```

```python
import chartcraft as cc

app = cc.App("Revenue Review", theme="midnight")

@app.page("/")
def overview():
    monthly = [
        {"month": "Jan", "revenue": 120, "profit": 28},
        {"month": "Feb", "revenue": 138, "profit": 31},
        {"month": "Mar", "revenue": 149, "profit": 36},
    ]

    return cc.Page(
        title="Revenue Review",
        subtitle="Q1 snapshot",
        kpis=[
            cc.stat("Revenue", "$407K", change=11.4),
            cc.stat("Profit Margin", "24%", change=1.8),
        ],
        content=[
            cc.section(
                "Momentum",
                cc.trend_line(
                    monthly,
                    x="month",
                    y=["revenue", "profit"],
                    title="Revenue vs Profit",
                    col=0, colspan=8, height=320,
                ),
                cc.spotlight_donut(
                    {"Direct": 52, "Partner": 31, "Online": 17},
                    title="Channel Mix",
                    col=8, colspan=4,
                    center_text="Q1",
                ),
                subtitle="Tracking ahead of plan",
            ),
            cc.note("Revenue stays ahead of plan while profit improves each month."),
            cc.section(
                "Leaders",
                cc.ranked_bars(
                    [
                        {"rep": "Avery", "revenue": 92},
                        {"rep": "Noah",  "revenue": 84},
                        {"rep": "Mia",   "revenue": 79},
                    ],
                    x="rep", y="revenue",
                    title="Top Reps",
                    col=0, colspan=6,
                ),
                cc.data_table(
                    [
                        {"region": "West",    "revenue": 168, "profit": 43},
                        {"region": "East",    "revenue": 137, "profit": 31},
                        {"region": "Central", "revenue": 102, "profit": 24},
                    ],
                    title="Regional Detail",
                    columns=["region", "revenue", "profit"],
                    col=6, colspan=6, page_size=5,
                ),
            ),
        ],
    )

app.run()
# ◆ ChartCraft  →  http://localhost:8050
# Builder       →  http://localhost:8050/builder
```

---

## ◆ Layout Helpers

```python
cc.Page(title, subtitle="", kpis=[], filters=[], content=[], charts=[], cols=12, ...)
cc.section(title, *content, subtitle="", col=0, colspan=12)
cc.note(content, col=0, colspan=12)
cc.stat(title, value=None, **kwargs)       # thin shortcut for cc.KPI(...)
```

---

## ◆ Chart Presets

Return standard chart classes with tuned defaults:

```
cc.trend_line      smooth curve, no dots    — great for time series
cc.trend_area      filled area chart        — shows volume over time
cc.comparison_bars grouped bars             — compare target vs actual
cc.ranked_bars     horizontal, show values  — top-N rankings
cc.spotlight_donut donut with center label  — mix / composition
cc.insight_scatter sized scatter            — correlation analysis
cc.data_table      sortable + searchable    — tabular detail
```

---

## ◆ SQL Helpers

Wire a connector to charts so queries re-run on every refresh or filter change:

```python
db = cc.connect_sql("sqlite:///sales.db")

cc.Page(
    title="SQL Example",
    filters=[cc.Filter("year", options=["All", "2024", "2025"])],
    kpis=[
        cc.sql_kpi(
            "Revenue", db,
            lambda f: (
                "SELECT SUM(revenue) FROM monthly_sales"
                if f.get("year") in (None, "All")
                else f"SELECT SUM(revenue) FROM monthly_sales WHERE year = {f['year']}"
            ),
            field="revenue",
            formatter=lambda v, _f: f"${v:,.0f}",
            linked_filters=["year"],
        )
    ],
    content=[
        cc.section(
            "Trend",
            cc.sql_line(
                db,
                "SELECT month, revenue, profit FROM monthly_sales ORDER BY month",
                x="month", y=["revenue", "profit"],
                title="Monthly Performance",
                col=0, colspan=8,
            ),
            cc.sql_table(
                db,
                "SELECT month, revenue, profit FROM monthly_sales ORDER BY month",
                title="Rows",
                columns=["month", "revenue", "profit"],
                col=8, colspan=4,
            ),
        )
    ],
)
```

All helpers: `sql_kpi` · `sql_line` · `sql_area` · `sql_bar` · `sql_donut` · `sql_scatter` · `sql_table`

Core classes also support `.from_sql(...)` at runtime:
```python
cc.Bar.from_sql(db, "SELECT region, revenue FROM sales ORDER BY revenue DESC", x="region", y="revenue")
```

---

## ◆ Page Builders

Drop in a complete sectioned dashboard when your story fits a common narrative:

```python
cc.executive_page(title, kpis=[...], hero=[...], performance=[...], note_text="...")
cc.sales_page(title, kpis=[...], trend=[...], analysis=[...], ranking=[...])
cc.customer_page(title, kpis=[...], mix=[...], geography=[...], accounts=[...])
cc.product_page(title, kpis=[...], overview=[...], profitability=[...], leaders=[...])
```

---

## ◆ Real-Time Streaming

Server-Sent Events push full chart specs to every browser — no WebSocket, no polling, no frontend code:

```python
cc.Line(
    data_fn=lambda: db.query_dict("SELECT ts, value FROM metrics ORDER BY ts DESC LIMIT 100"),
    x="ts", y="value",
    title="Live Stream",
    refresh=3,          # push new data every 3 seconds
    smooth=True,
)
```

Each component refreshes on its own interval independently.

---

## ◆ Connect to Anything

```python
db  = cc.connect_sql("sqlite:///analytics.db")       # zero deps
db  = cc.connect_sql("postgresql://user:pass@host:5432/db")   # pip install "chartcraft[pg]"
csv = cc.connect_csv("sales.csv")
csv = cc.connect_csv("./data/")                      # load entire directory
api = cc.connect_api("https://api.example.com", headers={"Authorization": "Bearer ..."})
```

---

## ◆ Themes

11 built-in themes, switch live in the browser:

```
dark themes ──────────────────────────────────────────────────────────────
  midnight   ████  deep purple bg  · purple accent
  obsidian   ████  pitch black     · cyan accent
  default    ████  dark zinc      · indigo accent
  ember      ████  warm dark       · orange accent
  jade       ████  forest dark    · green accent
  candy      ████  pink dark       · magenta accent
  arctic     ████  ice dark        · sky blue accent
  retro      ████  vintage teal   · gold accent
light themes ─────────────────────────────────────────────────────────────
  frost      ░░░░  clean light    · blue accent
  slate      ░░░░  professional    · navy accent
  scientific ░░░░  academic        · slate accent
```

---

## ◆ How It Compares

| | ChartCraft | Power BI | Tableau | Plotly Dash | Streamlit |
|--|:-:|:-:|:-:|:-:|:-:|
| Pure Python API | ✅ | ❌ | ❌ | ✅ | ✅ |
| Drag-and-drop visual builder | ✅ | ✅ | ✅ | ❌ | ❌ |
| Bidirectional code ↔ canvas | ✅ | ❌ | ❌ | ❌ | ❌ |
| Zero required dependencies | ✅ | ❌ | ❌ | ❌ | ❌ |
| Real-time SSE push | ✅ | ❌ | ❌ | ✅ | ✅ |
| Export to standalone HTML | ✅ | limited | limited | ❌ | ❌ |
| No build step / no npm | ✅ | ✅ | ✅ | ❌ | ✅ |
| PDF / Jupyter / Docker export | ✅ | partial | partial | ❌ | ❌ |

---

## ◆ Tech Stack

```
  Python 3.11+  ──  stdlib only · threading · sqlite3
  ECharts 5.5  ──  GPU canvas · 18+ chart types · CDN only
  Preact 10     ──  3KB React-compatible · no build step
  SSE           ──  text/event-stream · auto-reconnect
```

---

## ◆ Documentation

| | Guide |
|--|-------|
| [🚀 Getting Started](docs/getting-started.md) | Install, first dashboard, core concepts |
| [📊 Presets & Page Builders](docs/presets-and-page-builders.md) | Layout helpers, chart presets, SQL helpers, page builders |
| [🗃 Data Sources](docs/data-sources.md) | SQL, CSV, REST connectors, filter-linked queries |
| [📈 Chart Types](docs/charts.md) | All 18+ chart types, options, data formats |
| [🎨 Themes & Colors](docs/themes-and-colors.md) | Themes, palettes, custom branding, color utilities |
| [🎛 Filters & Interactivity](docs/filters-and-interactivity.md) | Filter types, cross-filtering, URL state |
| [⚡ Real-Time Data](docs/realtime.md) | SSE internals, refresh intervals, LIVE badge |
| [🖱 Visual Builder](docs/builder.md) | Canvas, color picker, code sync, shortcuts |
| [📦 Export & Deployment](docs/export-and-deployment.md) | HTML, PDF, Jupyter, Docker, nginx |
| [🔒 Authentication](docs/authentication.md) | Basic auth, bearer tokens, env vars |
| [📖 API Reference](docs/api-reference.md) | Every class, method, parameter, HTTP endpoint |

---

<div align="center">

```
pip install chartcraft
```

**MIT License** · Built with Python · Powered by ECharts

</div>
