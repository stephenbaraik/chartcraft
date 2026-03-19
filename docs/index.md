# ◆ ChartCraft Documentation

**Python-powered dashboards that rival Power BI & Tableau.**

Build stunning, interactive, real-time dashboards with pure Python — or design them visually with the drag-and-drop Dashboard Builder. No HTML, no JavaScript, no frontend skills required.

---

## What is ChartCraft?

ChartCraft is a Python library that turns your data into beautiful, interactive dashboards served directly in the browser. Write Python code, or use the visual builder — they stay in perfect sync.

```python
import chartcraft as cc

app = cc.App("Sales Dashboard", theme="midnight")

@app.page("/")
def home():
    return cc.Dashboard(
        title="Sales Overview",
        kpis=[cc.KPI("Revenue", "$1.2M", change=12.5)],
        charts=[cc.Bar({"Q1": 100, "Q2": 200, "Q3": 150, "Q4": 300}, title="Quarterly")],
    )

app.run()  # → http://localhost:8050
```

---

## Documentation

| Guide | What you'll learn |
|-------|------------------|
| [Getting Started](getting-started.md) | Install, run your first dashboard, key concepts |
| [Chart Types](charts.md) | All 18+ chart types with examples and options |
| [Themes & Colors](themes-and-colors.md) | 11 themes, 16 palettes, color picker, custom branding |
| [Data Sources](data-sources.md) | Connect to SQL, CSV files, REST APIs |
| [Filters & Interactivity](filters-and-interactivity.md) | Dropdowns, sliders, cross-filtering, drill-down |
| [Real-Time Data](realtime.md) | SSE streaming, auto-refresh, live KPIs |
| [Visual Builder](builder.md) | Drag-and-drop UI, bidirectional code sync |
| [Export & Deployment](export-and-deployment.md) | HTML, PDF, Jupyter, Docker, multi-page sites |
| [Authentication](authentication.md) | Password protection, Bearer tokens |
| [API Reference](api-reference.md) | Complete Python API — every class, method, parameter |

---

## Key Features

- **18 chart types** — Bar, Line, Area, Pie, Donut, Scatter, Heatmap, Radar, Gauge, Candlestick, and more
- **Zero required dependencies** — stdlib only; optional extras for SQL and PDF
- **Real-time streaming** — Server-Sent Events push data updates to the browser every N seconds
- **Visual builder** — Figma-like drag-and-drop canvas that generates Python code
- **Bidirectional sync** — edit Python code and the builder canvas stays in sync
- **11 built-in themes** — dark, light, and specialized; fully customizable
- **16 color palettes** + professional HSV color picker with harmonies
- **SQL, CSV, REST API** connectors with zero required dependencies for SQLite and CSV
- **Interactive filters** — cascading dropdowns, sliders, date ranges, cross-filtering
- **Export anywhere** — standalone HTML, Jupyter notebooks, Docker, PDF

---

## Installation

```bash
pip install chartcraft
```

**With database support:**
```bash
pip install "chartcraft[sql]"       # SQLAlchemy for PostgreSQL/MySQL/SQL Server
pip install "chartcraft[pg]"        # PostgreSQL
pip install "chartcraft[mysql]"     # MySQL
pip install "chartcraft[pandas]"    # DataFrame support
pip install "chartcraft[pdf]"       # PDF export via Playwright
pip install "chartcraft[full]"      # Everything
```

---

## Quick Example

```python
import chartcraft as cc

# 1. Create the app
app = cc.App("Analytics", theme="midnight")

# 2. Connect to data
db = cc.connect_sql("sqlite:///data.db")

# 3. Define a page
@app.page("/")
def overview():
    data = db.query_dict("SELECT month, revenue FROM sales")
    return cc.Dashboard(
        title="Sales Overview",
        kpis=[
            cc.KPI("Revenue", "$4.2M", change=12.5),
            cc.KPI("Users",   "45K",   change=-3.2),
        ],
        filters=[
            cc.Filter("region", label="Region", type="select",
                      options=["All", "North", "South"]),
        ],
        charts=[
            cc.Line(data, x="month", y="revenue",
                    title="Monthly Revenue", col=0, colspan=8),
            cc.Donut({"Enterprise": 45, "Pro": 30, "Free": 25},
                     title="Plan Split", col=8, colspan=4),
        ],
    )

# 4. Run
app.run()  # Opens browser at http://localhost:8050
```

---

## Minimum Requirements

- Python 3.11+
- Any modern browser (Chrome, Firefox, Safari, Edge)
- No database required (SQLite is built into Python)
