# ChartCraft

Build polished dashboard apps in Python with core chart primitives, readable page presets, SQL-backed components, and opinionated page builders — all kept in Python while giving you a visual builder, multi-page apps, and export flows that feel product-ready.

[Getting Started](docs/getting-started.md) · [Presets and Page Builders](docs/presets-and-page-builders.md) · [Data Sources](docs/data-sources.md) · [API Reference](docs/api-reference.md)

## Install

```bash
pip install chartcraft
```

Optional extras:

```bash
pip install "chartcraft[sql]"
pip install "chartcraft[pdf]"
pip install "chartcraft[full]"
```

## Quick Start

```python
import chartcraft as cc

app = cc.App("Revenue Review")

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
                    col=0,
                    colspan=8,
                    height=320,
                ),
                cc.spotlight_donut(
                    {"Direct": 52, "Partner": 31, "Online": 17},
                    title="Channel Mix",
                    col=8,
                    colspan=4,
                    center_text="Q1",
                ),
            ),
            cc.note("Revenue stays ahead of plan while profit improves each month."),
            cc.section(
                "Leaders",
                cc.ranked_bars(
                    [
                        {"rep": "Avery", "revenue": 92},
                        {"rep": "Noah", "revenue": 84},
                        {"rep": "Mia", "revenue": 79},
                    ],
                    x="rep",
                    y="revenue",
                    title="Top Reps",
                    col=0,
                    colspan=6,
                ),
                cc.data_table(
                    [
                        {"region": "West", "revenue": 168, "profit": 43},
                        {"region": "East", "revenue": 137, "profit": 31},
                        {"region": "Central", "revenue": 102, "profit": 24},
                    ],
                    title="Regional Detail",
                    col=6,
                    colspan=6,
                    columns=["region", "revenue", "profit"],
                    page_size=5,
                ),
            ),
        ],
    )

app.run()
```

## Layout Helpers

- `cc.Page(...)` wraps `cc.Dashboard` and accepts `title`, `subtitle`, `kpis`, `filters`, `content`, `charts`, `cols`, `refresh`, `background`, and `icon`.
- `cc.section(title, *content, subtitle="", col=0, colspan=12)` inserts a section header plus the content that follows it.
- `cc.note(content, col=0, colspan=12, font_size="0.95rem", align="left")` adds narrative text to a page.
- `cc.stat(title, value=None, **kwargs)` is a thin shortcut for `cc.KPI(...)`.

## Chart Presets

These helpers return standard chart classes with practical defaults:

- `cc.trend_line(*args, colors=None, show_dots=False, smooth=True, **kwargs)`
- `cc.trend_area(*args, colors=None, smooth=True, gradient=True, **kwargs)`
- `cc.comparison_bars(*args, colors=None, grouped=True, show_values=False, **kwargs)`
- `cc.ranked_bars(*args, colors=None, horizontal=True, show_values=True, **kwargs)`
- `cc.spotlight_donut(*args, colors=None, inner_radius="64%", center_text="", **kwargs)`
- `cc.insight_scatter(*args, min_radius=8, max_radius=24, **kwargs)`
- `cc.data_table(*args, page_size=8, sortable=True, searchable=True, **kwargs)`

```python
page = cc.Page(
    title="Pipeline Review",
    content=[
        cc.section(
            "Coverage",
            cc.trend_area(
                [
                    {"week": "W1", "pipeline": 210, "won": 38},
                    {"week": "W2", "pipeline": 225, "won": 41},
                    {"week": "W3", "pipeline": 239, "won": 44},
                ],
                x="week",
                y=["pipeline", "won"],
                title="Pipeline vs Wins",
                col=0,
                colspan=7,
            ),
            cc.comparison_bars(
                [
                    {"team": "North", "quota": 110, "actual": 103},
                    {"team": "South", "quota": 95, "actual": 98},
                ],
                x="team",
                y=["quota", "actual"],
                title="Quota vs Actual",
                col=7,
                colspan=5,
            ),
        )
    ],
)
```

## SQL Helpers

Use SQL helpers when your component should query through a connector at render time or when filters change.

```python
import chartcraft as cc

db = cc.connect_sql("sqlite:///sales.db")

sales_page = cc.Page(
    title="SQL Example",
    filters=[
        cc.Filter("year", options=["All", "2024", "2025"]),
    ],
    kpis=[
        cc.sql_kpi(
            "Revenue",
            db,
            lambda f: (
                "SELECT ROUND(SUM(revenue)) AS revenue FROM monthly_sales"
                if f.get("year") in (None, "All")
                else f"SELECT ROUND(SUM(revenue)) AS revenue FROM monthly_sales WHERE year = {int(f['year'])}"
            ),
            field="revenue",
            formatter=lambda v, _f: f"${v:,.0f}",
            linked_filters=["year"],
        ),
    ],
    content=[
        cc.section(
            "Trend",
            cc.sql_line(
                db,
                "SELECT month, revenue, profit FROM monthly_sales ORDER BY month",
                x="month",
                y=["revenue", "profit"],
                title="Monthly Performance",
                col=0,
                colspan=8,
            ),
            cc.sql_table(
                db,
                "SELECT month, revenue, profit FROM monthly_sales ORDER BY month",
                title="Monthly Rows",
                col=8,
                colspan=4,
                columns=["month", "revenue", "profit"],
            ),
        )
    ],
)
```

Available helpers:

- `cc.sql_kpi(title, connector, sql, *, params=None, field=None, formatter=None, **kwargs)`
- `cc.sql_line(connector, sql, *, params=None, **kwargs)`
- `cc.sql_area(connector, sql, *, params=None, **kwargs)`
- `cc.sql_bar(connector, sql, *, params=None, **kwargs)`
- `cc.sql_donut(connector, sql, *, params=None, **kwargs)`
- `cc.sql_scatter(connector, sql, *, params=None, **kwargs)`
- `cc.sql_table(connector, sql, *, params=None, **kwargs)`

## `from_sql()` on Core Classes

`cc.KPI`, `cc.Line`, `cc.Area`, `cc.Bar`, `cc.Donut`, `cc.Scatter`, and `cc.Table` also support `from_sql()` at runtime.

```python
db = cc.connect_sql("sqlite:///sales.db")

chart = cc.Line.from_sql(
    db,
    "SELECT month, revenue FROM monthly_sales ORDER BY month",
    x="month",
    y="revenue",
    title="Revenue",
)

kpi = cc.KPI.from_sql(
    "Revenue",
    db,
    "SELECT ROUND(SUM(revenue)) AS revenue FROM monthly_sales",
    field="revenue",
    formatter=lambda v, _f: f"${v:,.0f}",
)
```

## Page Builders

Use a page builder when your layout already matches a common dashboard narrative:

- `cc.executive_page(...)`
- `cc.sales_page(...)`
- `cc.customer_page(...)`
- `cc.product_page(...)`

Each builder returns a `cc.Dashboard` and composes sections for you. See `docs/presets-and-page-builders.md` for focused examples.
