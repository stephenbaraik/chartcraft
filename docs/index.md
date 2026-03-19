# ChartCraft Documentation

ChartCraft supports three authoring layers:

- core dashboard classes like `cc.Dashboard`, `cc.Line`, and `cc.Bar`
- composable helpers like `cc.Page`, `cc.section`, `cc.stat`, and `cc.ranked_bars`
- opinionated page builders like `cc.executive_page`, `cc.sales_page`, `cc.customer_page`, and `cc.product_page`

Use this documentation to choose the level that matches how quickly you want to move.

## Start Here

| Guide | What it covers |
|---|---|
| [Getting Started](getting-started.md) | Install ChartCraft, run a first app, and learn the recommended modern API |
| [Presets and Page Builders](presets-and-page-builders.md) | `Page`, `section`, chart presets, SQL helpers, and opinionated page builders |
| [Chart Types](charts.md) | Raw chart classes, options, and expected data shapes |
| [Data Sources](data-sources.md) | SQL, CSV, API connectors, plus SQL-backed component helpers |
| [Filters & Interactivity](filters-and-interactivity.md) | Filter controls, linked filters, and dynamic dashboard behavior |
| [Export & Deployment](export-and-deployment.md) | HTML export, combined multi-page PDF export, notebooks, Docker |
| [API Reference](api-reference.md) | Full public API, including presets and SQL helper constructors |

## Recommended Workflow

1. Start with `cc.Page(...)` if you want a flexible but clean dashboard structure.
2. Use `cc.executive_page(...)`, `cc.sales_page(...)`, `cc.customer_page(...)`, or `cc.product_page(...)` when your dashboard matches a common analytics story.
3. Use `cc.sql_kpi(...)`, `cc.sql_line(...)`, `cc.sql_area(...)`, `cc.sql_bar(...)`, and related helpers when your app is SQL-first.
4. Drop down to raw chart classes when you need exact control over layout or behavior.

## Minimal Example

```python
import chartcraft as cc

app = cc.App("Revenue Review", theme="frost")

@app.page("/")
def overview():
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
                cc.trend_line(
                    {
                        "month": ["Jan", "Feb", "Mar", "Apr"],
                        "revenue": [180, 205, 221, 247],
                        "profit": [28, 32, 34, 41],
                    },
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
            )
        ],
    )

app.run()
```
