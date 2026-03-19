# Filters & Interactivity

ChartCraft dashboards support interactive filters, cross-filtering between charts, drill-down actions, and URL-encoded filter state.

---

## Filter Types

Add filters to any dashboard with `cc.Filter`:

```python
cc.Dashboard(
    filters=[
        cc.Filter("region",    label="Region",     type="select",       options=["All", "North", "South"]),
        cc.Filter("tiers",     label="Plan",        type="multi_select", options=["Enterprise", "Pro", "Free"]),
        cc.Filter("date",      label="Date Range",  type="date_range"),
        cc.Filter("threshold", label="Min Revenue", type="slider",       options=[0, 100000], default=10000),
        cc.Filter("search",    label="Search",      type="text",         placeholder="Search customers..."),
        cc.Filter("live",      label="Live Mode",   type="toggle",       default=False),
    ],
    charts=[...],
)
```

### Filter Parameters

| Parameter | Type | Description |
|-----------|------|-------------|
| `name` | str | Unique identifier, used to read the filter value in `data_fn` |
| `label` | str | Display label shown above the control |
| `type` | str | Control type — see table below |
| `options` | list or callable | Choices for `select`/`multi_select`; `[min, max]` for `slider` |
| `default` | any | Initial value |
| `placeholder` | str | Placeholder text for `text` inputs |
| `scope` | str | `"page"` (default) or `"app"` (applies to all pages) |

### Filter Control Types

| `type` | UI | `options` format | Value in filters |
|--------|-----|-----------------|-----------------|
| `select` | Dropdown | `["A", "B", "C"]` | `"A"` (string) |
| `multi_select` | Multi-select dropdown | `["A", "B", "C"]` | `["A", "C"]` (list) |
| `date_range` | Date picker (start/end) | not required | `{"start": "2024-01-01", "end": "2024-12-31"}` |
| `slider` | Range slider | `[min, max]` | `42` (number) |
| `text` | Search input | not required | `"search query"` (string) |
| `toggle` | On/Off switch | not required | `True` or `False` |

---

## Connecting Filters to Charts

Charts re-query data when their linked filters change. Use `linked_filters` and `data_fn` together:

```python
@app.page("/")
def sales():
    return cc.Dashboard(
        filters=[
            cc.Filter("region", label="Region", type="select",
                      options=["All", "North", "South", "East", "West"]),
            cc.Filter("period", label="Period",  type="select",
                      options=["This Month", "Last Month", "Q1", "Q2"]),
        ],
        charts=[
            cc.Line(
                data_fn=lambda filters={}: get_sales_data(
                    region=filters.get("region", "All"),
                    period=filters.get("period", "This Month"),
                ),
                x="month", y="revenue",
                title="Monthly Revenue",
                linked_filters=["region", "period"],   # Re-fetch when either changes
                col=0, colspan=12,
            ),
        ],
    )

def get_sales_data(region, period):
    sql = "SELECT month, SUM(revenue) revenue FROM sales WHERE 1=1"
    params = {}
    if region != "All":
        sql += " AND region = :region"
        params["region"] = region
    sql += " GROUP BY month ORDER BY month"
    return db.query_dict(sql, params)
```

**How it works:** When the user changes a filter, the browser sends the new filter state to the server, which calls `data_fn(filters)` with the current filter values. The result is pushed to the browser via SSE.

---

## Cascading Filters

Filter options can depend on the values of other filters. Pass a callable to `options`:

```python
def region_options():
    return ["All"] + [r["region"] for r in db.query_dict("SELECT DISTINCT region FROM sales")]

def city_options(filters):
    region = filters.get("region", "All")
    if region == "All":
        return ["All"]
    return ["All"] + [
        r["city"] for r in
        db.query_dict("SELECT DISTINCT city FROM sales WHERE region = :r", {"r": region})
    ]

cc.Dashboard(
    filters=[
        cc.Filter("region", label="Region", type="select",
                  options=region_options),   # callable — called at page load

        cc.Filter("city", label="City", type="select",
                  options=city_options,      # callable — receives current filters
                  depends_on=["region"]),    # Re-fetches options when region changes
    ],
    charts=[...],
)
```

When `region` changes, the server automatically calls `city_options({"region": "North"})` and sends the updated city options to the browser.

---

## Cross-Filtering

Charts can filter each other by click. When a user clicks a bar, point, or segment, the click value becomes a filter for linked charts.

```python
cc.Bar(
    data,
    x="region", y="revenue",
    title="Revenue by Region",
    click_action="filter",       # Clicking a bar sets the "region" filter
    click_target="region",       # Filter name to update
    col=0, colspan=6,
)

cc.Line(
    data_fn=lambda filters={}: get_trend(region=filters.get("region")),
    x="month", y="revenue",
    title="Regional Trend",
    linked_filters=["region"],   # This chart re-fetches when "region" filter is set
    col=6, colspan=6,
)
```

**Flow:**
1. User clicks "North" bar on the Bar chart
2. `region = "North"` is set in the dashboard filter state
3. Line chart sees `"region"` in its `linked_filters` and re-fetches data
4. Line chart animates to show North's trend
5. The filter highlight persists — clicking the same bar again clears it

### Visual Feedback

When cross-filtering is active:
- The clicked element is highlighted; others are dimmed to 20% opacity
- An "×" chip appears at the top of the dashboard showing active filters
- Clearing the chip removes the filter

---

## URL Filter State

Filter state is encoded in the URL so users can bookmark and share filtered views:

```
http://localhost:8050/?filters=eyJyZWdpb24iOiJOb3J0aCIsInBlcmlvZCI6IlExIn0=
```

The `filters` query parameter is Base64-encoded JSON. This means:
- Browser Back/Forward works to navigate filter history
- Users can bookmark specific filtered views
- Sharing a URL shares the exact filtered state

Filter state is automatically restored when the page loads with a `filters` parameter.

---

## Auto-Apply Toggle

By default, filters apply immediately when changed. In the viewer, there is an **Auto-Apply** toggle:

- **On** (default): Each filter change triggers an immediate data refresh
- **Off**: Changes are queued and applied all at once when the user clicks **Apply**

This is useful for dashboards with slow queries where you don't want N queries for N filter changes.

---

## KPI Filters

KPIs can also react to filter changes:

```python
cc.KPI(
    "Revenue",
    data_fn=lambda filters={}: f"${get_revenue(region=filters.get('region', 'All')):,.0f}",
    refresh=None,                      # No time-based refresh
    linked_filters=["region"],         # Re-calculates when region filter changes
)
```

---

## Filter in Practice: Full Example

```python
import chartcraft as cc

db = cc.connect_sql("sqlite:///sales.db")
app = cc.App("Sales Dashboard", theme="midnight")

def revenue_by_month(region="All", period="2024"):
    sql = """
        SELECT month, SUM(revenue) as revenue
        FROM sales
        WHERE year = :year
    """
    params = {"year": period}
    if region != "All":
        sql += " AND region = :region"
        params["region"] = region
    sql += " GROUP BY month ORDER BY month"
    return db.query_dict(sql, params)

@app.page("/")
def overview():
    return cc.Dashboard(
        title="Sales Overview",
        filters=[
            cc.Filter("region", label="Region", type="select",
                      options=["All", "North", "South", "East", "West"]),
            cc.Filter("period", label="Year",   type="select",
                      options=["2022", "2023", "2024"], default="2024"),
        ],
        kpis=[
            cc.KPI("Revenue", data_fn=lambda f={}: f"${sum(r['revenue'] for r in revenue_by_month(**f)):,.0f}",
                   linked_filters=["region", "period"]),
        ],
        charts=[
            cc.Line(
                data_fn=lambda f={}: revenue_by_month(**f),
                x="month", y="revenue",
                title="Monthly Revenue",
                linked_filters=["region", "period"],
                col=0, colspan=8,
            ),
            cc.Bar(
                data_fn=lambda f={}: db.query_dict(
                    "SELECT region, SUM(revenue) revenue FROM sales WHERE year=:y GROUP BY region",
                    {"y": f.get("period", "2024")}
                ),
                x="region", y="revenue",
                title="By Region",
                linked_filters=["period"],
                click_action="filter",
                click_target="region",
                col=8, colspan=4,
            ),
        ],
    )

app.run()
```

---

## Filter API (Server)

Filters are applied server-side via `POST /api/filter`:

```json
{
  "page": "/",
  "filters": {
    "region": "North",
    "period": "2024"
  }
}
```

Response: Updated full dashboard spec with re-queried data.

This is handled automatically by the viewer — you don't need to call this endpoint yourself.
