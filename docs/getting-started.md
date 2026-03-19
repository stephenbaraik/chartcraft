# Getting Started

## Installation

```bash
pip install chartcraft
```

Optional extras for additional features:

```bash
pip install "chartcraft[sql]"      # PostgreSQL, MySQL, SQL Server via SQLAlchemy
pip install "chartcraft[pg]"       # PostgreSQL (includes psycopg2)
pip install "chartcraft[mysql]"    # MySQL (includes pymysql)
pip install "chartcraft[pandas]"   # Pandas DataFrame support
pip install "chartcraft[pdf]"      # PDF export (Playwright + Chromium)
pip install "chartcraft[full]"     # All of the above
```

**Requirements:** Python 3.11+, any modern browser.

---

## Your First Dashboard

Create a file called `app.py`:

```python
import chartcraft as cc

app = cc.App("My Dashboard", theme="midnight")

@app.page("/")
def home():
    return cc.Dashboard(
        title="Sales Overview",
        kpis=[
            cc.KPI("Revenue", "$1.2M", change=12.5),
            cc.KPI("Users", "45,231", change=-3.2),
            cc.KPI("Conversion", "4.8%", change=0.5),
        ],
        charts=[
            cc.Bar(
                {"Q1": 100, "Q2": 200, "Q3": 150, "Q4": 300},
                title="Quarterly Sales",
                col=0, colspan=8,
            ),
            cc.Donut(
                {"Enterprise": 45, "Pro": 30, "Free": 25},
                title="Plan Distribution",
                col=8, colspan=4,
            ),
        ],
    )

app.run()
```

Run it:

```bash
python app.py
```

Your browser opens at `http://localhost:8050`. That's it.

---

## Core Concepts

### App

`cc.App` is the entry point. It holds your theme, pages, and server config.

```python
app = cc.App(
    title="My App",         # Shown in the browser tab and nav bar
    theme="midnight",       # One of 11 built-in themes
)
```

### Pages

Use `@app.page(path)` to register a URL path. The decorated function must return a `cc.Dashboard`.

```python
@app.page("/")
def overview():
    """Overview"""      # This docstring becomes the nav label
    return cc.Dashboard(...)

@app.page("/sales")
def sales():
    """Sales"""
    return cc.Dashboard(...)
```

Multiple pages automatically generate a navigation bar.

### Dashboard

`cc.Dashboard` is the page layout. It holds KPIs, charts, and filters.

```python
cc.Dashboard(
    title="Sales Overview",           # Large heading at top of page
    subtitle="Updated daily",         # Smaller text below title
    kpis=[...],                       # Metric cards at top
    charts=[...],                     # Charts in a 12-column grid
    filters=[...],                    # Filter controls (dropdowns, sliders, etc.)
    cols=12,                          # Grid width (default 12)
    refresh=60,                       # Auto-reload entire page every 60s
)
```

### Grid Layout

Charts are positioned using a **12-column grid**, the same model as Bootstrap:

```python
# Full width
cc.Bar(data, col=0, colspan=12)

# Two-column split: 8 + 4
cc.Line(data, col=0, colspan=8)
cc.Pie(data,  col=8, colspan=4)

# Three equal columns
cc.Gauge(85, col=0, colspan=4)
cc.Gauge(62, col=4, colspan=4)
cc.Gauge(91, col=8, colspan=4)
```

Each chart row fills from left to right. When columns sum to 12, a new row begins automatically.

### KPIs

KPI cards display a number, title, and optional trend indicator at the top of the dashboard.

```python
cc.KPI("Revenue", "$4.2M", change=12.5)          # Green arrow up
cc.KPI("Churn",   "2.4%",  change=-0.8)          # Red arrow down
cc.KPI("NPS",     "72",    change=5.0)
```

### Charts

Charts accept data in multiple formats. The simplest is a dict:

```python
cc.Bar({"Jan": 100, "Feb": 200, "Mar": 150}, title="Monthly Sales")
```

More complex data uses column names:

```python
cc.Line(
    {"month": ["Jan","Feb","Mar"], "revenue": [100, 200, 150], "target": [120, 180, 160]},
    x="month",
    y=["revenue", "target"],
    title="Revenue vs Target",
)
```

---

## Data Formats

ChartCraft accepts data in any of these forms:

```python
# 1. Dict of scalars (Pie, Bar, simple charts)
{"Chrome": 65, "Firefox": 20, "Safari": 15}

# 2. Dict of lists (multi-series charts)
{"month": ["Jan", "Feb", "Mar"], "sales": [100, 200, 150]}

# 3. List of dicts (table-like records)
[{"month": "Jan", "sales": 100}, {"month": "Feb", "sales": 200}]

# 4. SQL query results (list of dicts from query_dict)
db.query_dict("SELECT region, SUM(revenue) FROM sales GROUP BY region")

# 5. Pandas DataFrame (requires chartcraft[pandas])
import pandas as pd
df = pd.DataFrame({"x": [1, 2, 3], "y": [4, 5, 6]})

# 6. Callable for real-time data
lambda: db.query_dict("SELECT * FROM live_metrics ORDER BY ts DESC LIMIT 50")
```

---

## Running Options

```python
app.run(
    host="localhost",       # Bind address (use "0.0.0.0" to expose on network)
    port=8050,              # Port number
    open_browser=True,      # Auto-open browser on start
    password="secret",      # Enable HTTP Basic Auth (username: admin)
    token="my-api-token",   # Enable Bearer token auth
)
```

---

## Multi-Page Example

```python
import chartcraft as cc

app = cc.App("Analytics Platform", theme="midnight")

@app.page("/")
def overview():
    """Overview"""
    return cc.Dashboard(title="Overview", charts=[...])

@app.page("/sales")
def sales():
    """Sales"""
    return cc.Dashboard(title="Sales Detail", charts=[...])

@app.page("/customers")
def customers():
    """Customers"""
    return cc.Dashboard(title="Customer Intelligence", charts=[...])

app.run()
```

Each page gets its own nav link. All pages share the same theme.

---

## Visual Builder

Navigate to `http://localhost:8050/builder` while your app is running to access the visual drag-and-drop dashboard builder. Design dashboards by dragging widgets, adjusting properties, and picking colors — all without writing code. The builder generates Python code in real-time.

See the [Visual Builder guide](builder.md) for full details.

---

## Next Steps

- [Chart Types](charts.md) — Explore all 18+ chart types
- [Data Sources](data-sources.md) — Connect to databases and APIs
- [Themes & Colors](themes-and-colors.md) — Customize the look
- [Filters & Interactivity](filters-and-interactivity.md) — Add interactive controls
- [Real-Time Data](realtime.md) — Stream live data
