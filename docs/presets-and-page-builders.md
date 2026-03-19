# Presets and Page Builders

ChartCraft presets keep page code short while still returning normal core classes like `cc.KPI`, `cc.Line`, `cc.Bar`, `cc.Donut`, `cc.Scatter`, `cc.Table`, and `cc.Dashboard`.

## Layout Helpers
### `cc.Page()`

`cc.Page()` wraps `cc.Dashboard()` and accepts `title`, `subtitle`, `kpis`, `filters`, `content`, `charts`, `cols`, `refresh`, `background`, and `icon`.

```python
import chartcraft as cc

page = cc.Page(
    title="Operations Review",
    subtitle="Weekly snapshot",
    kpis=[cc.stat("Orders", "12,480", change=6.1)],
    content=[
        cc.section(
            "Momentum",
            cc.trend_line(
                [
                    {"week": "W1", "orders": 2900, "returns": 105},
                    {"week": "W2", "orders": 3040, "returns": 99},
                    {"week": "W3", "orders": 3185, "returns": 92},
                ],
                x="week",
                y=["orders", "returns"],
                title="Orders vs Returns",
                col=0,
                colspan=8,
            ),
            cc.spotlight_donut(
                {"Standard": 61, "Express": 27, "Pickup": 12},
                title="Fulfillment Mix",
                col=8,
                colspan=4,
                center_text="Share",
            ),
            subtitle="Preset helpers with standard grid placement",
        ),
        cc.note("Orders are rising while returns trend down."),
    ],
)
```

### `cc.section()`, `cc.note()`, and `cc.stat()`

```python
section = cc.section(
    "Top Regions",
    cc.ranked_bars(
        [{"region": "West", "revenue": 420}, {"region": "East", "revenue": 365}],
        x="region",
        y="revenue",
        title="Revenue by Region",
        col=0,
        colspan=6,
    ),
    cc.data_table(
        [{"region": "West", "revenue": 420, "orders": 3800}],
        title="Regional Detail",
        columns=["region", "revenue", "orders"],
        col=6,
        colspan=6,
    ),
    subtitle="Highest revenue first",
)

note = cc.note("Enterprise demand remains strongest in the West region.")
stat = cc.stat("Net Revenue", "$2.4M", change=8.7, change_label="vs last month")
```

## Chart Presets
These helpers return chart instances with tuned defaults:

- `cc.trend_line(*args, colors=None, show_dots=False, smooth=True, **kwargs)`
- `cc.trend_area(*args, colors=None, smooth=True, gradient=True, **kwargs)`
- `cc.comparison_bars(*args, colors=None, grouped=True, show_values=False, **kwargs)`
- `cc.ranked_bars(*args, colors=None, horizontal=True, show_values=True, **kwargs)`
- `cc.spotlight_donut(*args, colors=None, inner_radius="64%", center_text="", **kwargs)`
- `cc.insight_scatter(*args, min_radius=8, max_radius=24, **kwargs)`
- `cc.data_table(*args, page_size=8, sortable=True, searchable=True, **kwargs)`

```python
content = [
    cc.trend_area(
        [
            {"month": "Jan", "revenue": 120, "profit": 24},
            {"month": "Feb", "revenue": 132, "profit": 29},
            {"month": "Mar", "revenue": 148, "profit": 35},
        ],
        x="month",
        y=["revenue", "profit"],
        title="Revenue and Profit",
        col=0,
        colspan=6,
    ),
    cc.comparison_bars(
        [
            {"segment": "Enterprise", "target": 180, "actual": 192},
            {"segment": "SMB", "target": 140, "actual": 134},
        ],
        x="segment",
        y=["target", "actual"],
        title="Target vs Actual",
        col=6,
        colspan=6,
    ),
    cc.insight_scatter(
        [
            {"product": "Alpha", "revenue": 210, "margin": 32, "orders": 140},
            {"product": "Beta", "revenue": 178, "margin": 24, "orders": 190},
        ],
        x="revenue",
        y="margin",
        size="orders",
        title="Revenue vs Margin",
        col=0,
        colspan=6,
    ),
    cc.data_table(
        [{"product": "Alpha", "revenue": 210, "margin": 32}],
        title="Product Detail",
        columns=["product", "revenue", "margin"],
        col=6,
        colspan=6,
    ),
]
```

## SQL Helpers
SQL presets build query-backed components by wiring `data_fn` for you.

```python
import chartcraft as cc

db = cc.connect_sql("sqlite:///sales.db")

page = cc.Page(
    title="SQL Components",
    filters=[cc.Filter("year", options=["All", "2024", "2025"])],
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
        )
    ],
    content=[
        cc.section(
            "From SQL",
            cc.sql_line(
                db,
                "SELECT month, revenue, profit FROM monthly_sales ORDER BY month",
                x="month",
                y=["revenue", "profit"],
                title="Monthly Trend",
                col=0,
                colspan=8,
            ),
            cc.sql_table(
                db,
                "SELECT month, revenue, profit FROM monthly_sales ORDER BY month",
                title="Rows",
                columns=["month", "revenue", "profit"],
                col=8,
                colspan=4,
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
`cc.KPI`, `cc.Line`, `cc.Area`, `cc.Bar`, `cc.Donut`, `cc.Scatter`, and `cc.Table` also support `from_sql()`.

```python
chart = cc.Bar.from_sql(
    db,
    "SELECT region, revenue, profit FROM regional_sales ORDER BY revenue DESC",
    x="region",
    y=["revenue", "profit"],
    title="Regional Sales",
)

kpi = cc.KPI.from_sql(
    "Orders",
    db,
    "SELECT COUNT(*) AS orders FROM orders",
    field="orders",
)
```

## Page Builders
Page builders return complete `cc.Dashboard` objects with fixed section structure.

### `cc.executive_page()`
```python
executive = cc.executive_page(
    title="Executive Dashboard",
    kpis=[cc.stat("Revenue", "$4.8M", change=12.1)],
    hero=[cc.trend_line([{"month": "Jan", "revenue": 390}], x="month", y="revenue", title="Revenue")],
    hero_subtitle="Growth and mix",
    note_text="Enterprise remains the main growth engine.",
    performance=[cc.ranked_bars([{"state": "California", "revenue": 640}], x="state", y="revenue", title="Top States")],
)
```

### `cc.sales_page()`
```python
sales = cc.sales_page(
    title="Sales Deep Dive",
    kpis=[cc.stat("Average Deal", "$8,420", change=4.2)],
    trend=[cc.trend_area([{"month": "Jan", "sales": 320}], x="month", y="sales", title="Monthly Sales")],
    analysis=[cc.comparison_bars([{"segment": "Enterprise", "sales": 220, "profit": 54}], x="segment", y=["sales", "profit"], title="Segment Analysis")],
    ranking=[cc.ranked_bars([{"product": "Suite A", "sales": 96}], x="product", y="sales", title="Top Products")],
)
```

### `cc.customer_page()`
```python
customer = cc.customer_page(
    title="Customer Dashboard",
    kpis=[cc.stat("Active Accounts", "1,284", change=7.5)],
    mix=[cc.spotlight_donut({"Enterprise": 54, "SMB": 30, "Consumer": 16}, title="Segment Mix")],
    geography=[cc.comparison_bars([{"region": "West", "revenue": 420, "accounts": 180}], x="region", y=["revenue", "accounts"], title="Regional Accounts")],
    accounts=[cc.data_table([{"account": "Acme", "revenue": 82}], title="Top Accounts")],
)
```

### `cc.product_page()`
```python
product = cc.product_page(
    title="Product Dashboard",
    kpis=[cc.stat("SKUs Sold", "14,220", change=5.8)],
    overview=[cc.comparison_bars([{"category": "Hardware", "sales": 310, "profit": 76}], x="category", y=["sales", "profit"], title="Category Overview")],
    note_text="Software carries the best margin profile this quarter.",
    profitability=[cc.insight_scatter([{"product": "Alpha", "sales": 210, "profit": 32, "orders": 140}], x="sales", y="profit", size="orders", title="Sales vs Profit")],
    leaders=[cc.ranked_bars([{"product": "Alpha", "sales": 210}], x="product", y="sales", title="Top Products")],
)
```

Use a page builder when the built-in section names already match your story. Use `cc.Page()` when you need a custom flow.
