# Getting Started

## Installation

```bash
pip install chartcraft
```

Optional extras:

```bash
pip install "chartcraft[sql]"
pip install "chartcraft[pdf]"
pip install "chartcraft[full]"
```

Requirements: Python 3.11+, any modern browser.

---

## Your First Modern ChartCraft Page

Create `app.py`:

```python
import chartcraft as cc

app = cc.App("Revenue Review", theme="midnight")

@app.page("/")
def overview():
    monthly = [
        {"month": "Jan", "revenue": 180, "profit": 28},
        {"month": "Feb", "revenue": 205, "profit": 32},
        {"month": "Mar", "revenue": 221, "profit": 34},
        {"month": "Apr", "revenue": 247, "profit": 41},
    ]

    return cc.Page(
        title="Revenue Review",
        subtitle="A compact preset-driven dashboard",
        kpis=[
            cc.stat("Revenue", "$1.24M", change=8.4),
            cc.stat("Margin", "21.7%", change=1.3),
        ],
        content=[
            cc.section(
                "Momentum",
                cc.trend_area(
                    monthly,
                    x="month",
                    y=["revenue", "profit"],
                    title="Revenue vs Profit",
                    col=0,
                    colspan=8,
                    height=320,
                ),
                cc.spotlight_donut(
                    {"Enterprise": 52, "Mid-Market": 31, "SMB": 17},
                    title="Revenue Mix",
                    center_text="Q2",
                    col=8,
                    colspan=4,
                    height=320,
                ),
                subtitle="A compact story about pace and mix",
            ),
            cc.note(
                "Enterprise remains the primary growth engine while the margin profile stays broad-based."
            ),
        ],
    )

app.run()
```

Run it:

```bash
python app.py
```

Then open `http://localhost:8050`.

---

## Three API Levels

ChartCraft now supports three ways to build pages.

### 1. Core Components

Use the raw API when you want exact control.

```python
cc.Dashboard(
    title="Overview",
    kpis=[cc.KPI("Revenue", "$1.2M", change=12.5)],
    charts=[
        cc.Line(data, x="month", y="revenue", title="Revenue", col=0, colspan=8),
        cc.Donut(plan_mix, title="Plans", col=8, colspan=4),
    ],
)
```

### 2. Presets Layer

Use `cc.Page`, `cc.section`, `cc.note`, and chart presets when you want cleaner code.

```python
cc.Page(
    title="Overview",
    kpis=[cc.stat("Revenue", "$1.2M", change=12.5)],
    content=[
        cc.section(
            "Performance",
            cc.trend_line(data, x="month", y="revenue", title="Revenue", col=0, colspan=8),
            cc.spotlight_donut(plan_mix, title="Plans", col=8, colspan=4),
        )
    ],
)
```

### 3. Opinionated Page Builders

Use page builders when your dashboard fits a common analytics narrative.

```python
cc.sales_page(
    title="Sales Deep-Dive",
    filters=[cc.Filter("year", type="select", options=["All", "2023", "2024"])],
    kpis=[...],
    trend=[...],
    analysis=[...],
    ranking=[...],
)
```

---

## SQL-Backed Components

If your app is query-driven, use SQL helpers directly.

```python
import chartcraft as cc

db = cc.connect_sql("sqlite:///sales.db")

revenue = cc.sql_kpi(
    "Revenue",
    db,
    "SELECT ROUND(SUM(revenue)) AS revenue FROM orders",
    field="revenue",
    formatter=lambda v, _f: f"${v:,.0f}",
)

trend = cc.sql_line(
    db,
    "SELECT month, revenue, profit FROM monthly_sales ORDER BY month",
    x="month",
    y=["revenue", "profit"],
    title="Revenue vs Profit",
)
```

Core classes also support `from_sql(...)`:

```python
cc.KPI.from_sql(...)
cc.Bar.from_sql(...)
cc.Area.from_sql(...)
cc.Table.from_sql(...)
```

---

## Core Concepts

### App

`cc.App` holds routes, theme selection, and server configuration.

```python
app = cc.App("My App", theme="midnight")
```

### Pages

Register routes with `@app.page(path)`. The decorated function returns a dashboard object and is called on every browser request.

```python
@app.page("/")
def overview():
    return cc.Page(title="Overview", content=[...])

@app.page("/sales")
def sales():
    return cc.sales_page(title="Sales", kpis=[...], trend=[...])
```

### Grid Layout

Charts use a 12-column grid.

```python
cc.Line(data, col=0, colspan=8)
cc.Donut(data, col=8, colspan=4)
```

### Filters

Filter values flow into `data_fn(filters)` and SQL helpers.

```python
cc.Filter("year", type="select", options=["All", "2023", "2024"])
```

Use `linked_filters=["year"]` on charts or KPIs that re-query when the filter changes.

---

## Visual Builder

While your app is running, open `http://localhost:8050/builder`.

The builder gives you a drag-and-drop canvas, property editing, code sync, and export — without leaving the Python workflow.

---

## Next Steps

- [Presets and Page Builders](presets-and-page-builders.md)
- [Chart Types](charts.md)
- [Data Sources](data-sources.md)
- [Filters & Interactivity](filters-and-interactivity.md)
- [Export & Deployment](export-and-deployment.md)
