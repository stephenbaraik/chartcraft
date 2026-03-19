# API Reference

Complete reference for all ChartCraft Python classes, methods, and parameters.

---

## `cc.App` / `cc.AppServer`

The top-level object holding pages, theme, and server configuration.

### Constructor

```python
app = cc.App(
    title: str,
    theme: str = "default",
)
```

| Parameter | Type | Default | Description |
|-----------|------|---------|-------------|
| `title` | str | required | App title shown in browser tab and nav bar |
| `theme` | str | `"default"` | Theme name — see [Themes & Colors](themes-and-colors.md) |

### `@app.page(path)`

Decorator to register a dashboard page at a URL path.

```python
@app.page("/")
def home():
    """Home"""          # Docstring becomes the nav label
    return cc.Dashboard(...)

@app.page("/sales")
def sales():
    """Sales"""
    return cc.Dashboard(...)
```

The decorated function must return a `cc.Dashboard` and is called on every browser request to that path.

### `app.run()`

Start the HTTP server.

```python
app.run(
    host: str = "localhost",
    port: int = 8050,
    open_browser: bool = True,
    password: str = None,
    token: str = None,
)
```

| Parameter | Type | Default | Description |
|-----------|------|---------|-------------|
| `host` | str | `"localhost"` | Bind address. Use `"0.0.0.0"` to expose on the network. |
| `port` | int | `8050` | Port number |
| `open_browser` | bool | `True` | Auto-open browser when server starts |
| `password` | str | `None` | HTTP Basic Auth password (username is always `admin`) |
| `token` | str | `None` | Bearer token — accept via `?token=` or `Authorization: Bearer` |

Blocks until `Ctrl+C`.

### `app.save()`

Export one page as a standalone HTML file.

```python
path = app.save(
    path: str,
    page: str = "/",
    theme: str = None,
) -> str
```

### `app.save_all()`

Export all registered pages as separate HTML files.

```python
paths = app.save_all(
    output_dir: str,
    theme: str = None,
) -> list[str]
```

### `app.to_html()`

Return dashboard HTML as a string.

```python
html = app.to_html(page: str = "/", theme: str = None) -> str
```

### `app.set_theme()`

Change the active theme.

```python
app.set_theme("frost")
```

---

## `cc.quick_dashboard()`

Create and optionally export a dashboard without creating an App.

```python
cc.quick_dashboard(
    title: str,
    charts: list,
    theme: str = "default",
    kpis: list = None,
    save_path: str = None,
) -> str
```

---

## Presets and Page Builders

### `cc.Page(...)`

Higher-level page constructor that returns a `cc.Dashboard`.

```python
cc.Page(
    title: str = "",
    subtitle: str = "",
    kpis: list[KPI] = [],
    filters: list[Filter] = [],
    content: list = [],
    charts: list = [],
    cols: int = 12,
    refresh: int = None,
    background: str = "",
    icon: str = "",
)
```

### Layout helpers

```python
cc.section(title, *content, subtitle="", col=0, colspan=12)
cc.note(content, col=0, colspan=12, font_size="0.95rem", align="left")
cc.stat(title, value=None, **kwargs)
```

### Chart-style helpers

```python
cc.trend_line(*args, colors=None, show_dots=False, smooth=True, **kwargs)
cc.trend_area(*args, colors=None, smooth=True, gradient=True, **kwargs)
cc.comparison_bars(*args, colors=None, grouped=True, show_values=False, **kwargs)
cc.ranked_bars(*args, colors=None, horizontal=True, show_values=True, **kwargs)
cc.spotlight_donut(*args, colors=None, inner_radius="64%", center_text="", **kwargs)
cc.insight_scatter(*args, min_radius=8, max_radius=24, **kwargs)
cc.data_table(*args, page_size=8, sortable=True, searchable=True, **kwargs)
```

### Opinionated page builders

```python
cc.executive_page(title, subtitle="", kpis=None, hero=None, hero_subtitle="", performance=None, note_text="", content=None, filters=None, icon="")
cc.sales_page(title, subtitle="", filters=None, kpis=None, trend=None, trend_subtitle="", analysis=None, ranking=None, note_text="", icon="")
cc.customer_page(title, subtitle="", filters=None, kpis=None, mix=None, mix_subtitle="", geography=None, accounts=None, icon="")
cc.product_page(title, subtitle="", filters=None, kpis=None, overview=None, overview_subtitle="", note_text="", profitability=None, leaders=None, icon="")
```

---

## SQL Helpers

```python
cc.sql_kpi(title, connector, sql, params=None, field=None, formatter=None, **kwargs)
cc.sql_line(connector, sql, params=None, **kwargs)
cc.sql_area(connector, sql, params=None, **kwargs)
cc.sql_bar(connector, sql, params=None, **kwargs)
cc.sql_donut(connector, sql, params=None, **kwargs)
cc.sql_scatter(connector, sql, params=None, **kwargs)
cc.sql_table(connector, sql, params=None, **kwargs)
```

`sql` may be:

- a SQL string
- a callable that receives the active filter state and returns a SQL string
- a callable that returns `(sql, params)`

At runtime, core classes also expose:

```python
cc.KPI.from_sql(...)
cc.Line.from_sql(...)
cc.Area.from_sql(...)
cc.Bar.from_sql(...)
cc.Donut.from_sql(...)
cc.Scatter.from_sql(...)
cc.Table.from_sql(...)
```

---

## `cc.Dashboard`

The page layout. Contains KPIs, charts, and filters.

```python
cc.Dashboard(
    title: str = "",
    subtitle: str = "",
    kpis: list[KPI] = [],
    charts: list = [],
    filters: list[Filter] = [],
    cols: int = 12,
    refresh: int = None,
    background: str = None,
    icon: str = "",
)
```

| Parameter | Type | Default | Description |
|-----------|------|---------|-------------|
| `title` | str | `""` | Large heading at the top of the page |
| `subtitle` | str | `""` | Secondary text below the title |
| `kpis` | list | `[]` | `cc.KPI` instances — displayed as cards at the top |
| `charts` | list | `[]` | Chart instances arranged in the 12-column grid |
| `filters` | list | `[]` | `cc.Filter` instances — displayed above charts |
| `cols` | int | `12` | Grid width (almost always 12) |
| `refresh` | int | `None` | Full page auto-refresh interval in seconds |
| `background` | str | `None` | Override background color for this page |
| `icon` | str | `""` | Emoji or icon character in the page title |

### Fluent API

```python
dash = (
    cc.Dashboard(title="Sales")
    .add_kpi("Revenue", "$1.2M", change=12.5)
    .add_kpi("Users", "45K", change=-3.2)
    .add_chart(cc.Bar({"Q1": 100, "Q2": 200}, title="Sales"))
    .add_filter("region", label="Region", type="select", options=["All","North"])
)
```

---

## `cc.KPI`

Metric card displayed at the top of the dashboard.

```python
cc.KPI(
    title: str,
    value: Any = None,
    change: float = None,
    change_label: str = "vs prev",
    prefix: str = "",
    suffix: str = "",
    icon: str = "",
    color: str = "",
    sparkline: list[float] = None,
    refresh: int = None,
    data_fn: callable = None,
    linked_filters: list[str] = [],
)
```

| Parameter | Type | Description |
|-----------|------|-------------|
| `title` | str | Card label |
| `value` | any | Displayed value (string, number, etc.) |
| `change` | float | Percentage change — positive=green up, negative=red down |
| `change_label` | str | Label next to the change indicator (default `"vs prev"`) |
| `prefix` | str | Text before the value (e.g. `"$"`) |
| `suffix` | str | Text after the value (e.g. `"%"`) |
| `icon` | str | Emoji icon shown next to the title |
| `color` | str | Accent color for the card stripe |
| `sparkline` | list[float] | Mini trend line data (small chart inside the card) |
| `refresh` | int | Auto-refresh interval in seconds |
| `data_fn` | callable | Function that returns the value — called on refresh |
| `linked_filters` | list[str] | Filter names that trigger `data_fn` re-call |

---

## `cc.Filter`

Interactive filter control displayed above charts.

```python
cc.Filter(
    name: str,
    label: str = "",
    type: str = "select",
    options: list or callable = None,
    default: Any = None,
    scope: str = "page",
    placeholder: str = "",
)
```

| Parameter | Type | Description |
|-----------|------|-------------|
| `name` | str | Unique identifier — used to read the value in `data_fn(filters)` |
| `label` | str | Display label above the control |
| `type` | str | Control type: `"select"`, `"multi_select"`, `"date_range"`, `"slider"`, `"text"`, `"toggle"` |
| `options` | list or callable | Choices for select/multi_select; `[min, max]` for slider; callable for dynamic options |
| `default` | any | Initial value |
| `scope` | str | `"page"` (this page only) or `"app"` (all pages) |
| `placeholder` | str | Placeholder text for text inputs |

---

## Chart Base Parameters

All chart types accept these parameters in addition to their type-specific options:

| Parameter | Type | Default | Description |
|-----------|------|---------|-------------|
| `data` | any | required | Data: dict, list, DataFrame, or callable |
| `x` | str | `None` | X-axis column name |
| `y` | str or list | `None` | Y-axis column name(s) |
| `title` | str | `""` | Chart title |
| `subtitle` | str | `""` | Chart subtitle |
| `colors` | list[str] | `None` | Custom hex colors per series |
| `palette` | str | `None` | Named palette name |
| `col` | int | `0` | Grid start column (0–11) |
| `colspan` | int | `12` | Grid columns spanned (1–12) |
| `height` | int | `400` | Chart height in pixels |
| `refresh` | int | `None` | SSE auto-refresh interval in seconds |
| `data_fn` | callable | `None` | Function returning data (for dynamic/real-time) |
| `linked_filters` | list[str] | `[]` | Filter names that trigger data re-fetch |
| `tooltip` | bool | `True` | Show hover tooltips |
| `animate` | bool | `True` | Entry animations |
| `animate_duration` | int | `800` | Animation duration in ms |
| `click_action` | str | `None` | `"filter"` or `"navigate"` on click |
| `click_target` | str | `None` | Filter name or URL path for click action |

---

## Chart Type Reference

### `cc.Bar`

```python
cc.Bar(data, x=None, y=None,
       horizontal=False, stacked=False, grouped=False, show_values=False,
       **base_params)
```

### `cc.Line`

```python
cc.Line(data, x=None, y=None,
        smooth=False, show_dots=True, dash=False, fill=False,
        **base_params)
```

### `cc.Area`

```python
cc.Area(data, x=None, y=None,
        smooth=False, stacked=False, gradient=True,
        **base_params)
```

### `cc.Pie`

```python
cc.Pie(data,
       label_position="outside", explode=[],
       **base_params)
```

### `cc.Donut`

```python
cc.Donut(data,
         inner_radius="50%", center_text="", label_position="outside",
         **base_params)
```

### `cc.Scatter` / `cc.Bubble`

```python
cc.Scatter(data, x=None, y=None,
           size=None, group=None, min_radius=4, max_radius=30,
           **base_params)
```

### `cc.Heatmap`

```python
cc.Heatmap(data, x=None, y=None,
           color_scale=None, show_labels=False,
           **base_params)
```

Data format: `{"x_labels": [...], "y_labels": [...], "matrix": [[...], ...]}`

### `cc.Radar`

```python
cc.Radar(data, x=None, y=None,
         shape="polygon", fill=True,
         **base_params)
```

### `cc.Waterfall`

```python
cc.Waterfall(data, x=None, y=None,
             show_total=True, positive_color=None, negative_color=None,
             **base_params)
```

### `cc.Funnel`

```python
cc.Funnel(data, x=None, y=None,
          orientation="vertical", gap=2, show_labels=True,
          **base_params)
```

### `cc.Treemap`

```python
cc.Treemap(data,
           drill_down=True, show_breadcrumb=True,
           **base_params)
```

Data format: `{"name": "root", "children": [{"name": ..., "value": ..., "children": [...]}]}`

### `cc.Sankey`

```python
cc.Sankey(data,
          orientation="horizontal", node_width=20, node_gap=8,
          **base_params)
```

Data format: list of `(source, target, value)` tuples.

### `cc.Gauge`

```python
cc.Gauge(value,
         min_val=0, max_val=100, arc_width=18, show_pointer=True,
         zones=[],
         **base_params)
```

`zones` format: `[{"min": 0, "max": 40, "color": "#EF4444"}, ...]`

### `cc.Candlestick`

```python
cc.Candlestick(data, x=None,
               show_volume=True, ma_lines=[],
               **base_params)
```

Data needs columns: `open`, `high`, `low`, `close`. Optional `volume`.

### `cc.Histogram`

```python
cc.Histogram(data, y=None,
             bins=10, show_density=False,
             **base_params)
```

### `cc.BoxPlot`

```python
cc.BoxPlot(data, x=None, y=None,
           show_outliers=True, notched=False,
           **base_params)
```

### `cc.Table`

```python
cc.Table(data, x=None, y=None,
         columns=None, page_size=10,
         sortable=True, searchable=False, striped=True,
         **base_params)
```

### `cc.Metric`

```python
cc.Metric(value=None,
          sparkline=None, trend=None,
          **base_params)
```

---

## Layout Widgets

### `cc.SectionHeader`

```python
cc.SectionHeader(title, subtitle="", col=0, colspan=12)
```

### `cc.Divider`

```python
cc.Divider(col=0, colspan=12, color=None, thickness=1)
```

### `cc.Spacer`

```python
cc.Spacer(col=0, colspan=12, height=24)
```

### `cc.TextBlock`

```python
cc.TextBlock(content, col=0, colspan=12, font_size=14, align="left")
```

---

## Connectors

### `cc.connect_sql()`

```python
db = cc.connect_sql(connection_string: str) -> SQLConnector
```

**SQLConnector methods:**

| Method | Returns | Description |
|--------|---------|-------------|
| `query(sql, params=None)` | `list[tuple]` | Execute SQL, return rows as tuples |
| `query_dict(sql, params=None)` | `list[dict]` | Execute SQL, return rows as dicts |
| `query_df(sql, params=None)` | `DataFrame` | Execute SQL, return pandas DataFrame |
| `execute(sql, params=None)` | `None` | Non-SELECT statement |
| `tables()` | `list[str]` | List all table names |
| `schema(table)` | `list[dict]` | Columns: `[{"name": ..., "type": ...}]` |
| `close()` | `None` | Release connection |

### `cc.connect_csv()`

```python
csv = cc.connect_csv(path: str) -> CSVConnector
```

**CSVConnector methods:**

| Method | Returns | Description |
|--------|---------|-------------|
| `tables()` | `list[str]` | List table names (one per file) |
| `query(table)` | `list[dict]` | Read table as list of dicts |
| `query_as_columns(table)` | `dict[str, list]` | Read table as dict of columns |
| `reload()` | `None` | Re-read files from disk |

### `cc.connect_api()`

```python
api = cc.connect_api(base_url: str, headers: dict = None) -> APIConnector
```

**APIConnector methods:**

| Method | Returns | Description |
|--------|---------|-------------|
| `get(endpoint, params=None)` | any | HTTP GET, return parsed JSON |
| `post(endpoint, data=None)` | any | HTTP POST with JSON body |
| `put(endpoint, data=None)` | any | HTTP PUT with JSON body |
| `delete(endpoint)` | any | HTTP DELETE |
| `set_header(key, value)` | `APIConnector` | Add/update request header (fluent) |

---

## Theme & Color Functions

### Theme Management

```python
cc.get_theme(name: str) -> Theme
cc.register_theme(name: str, theme: Theme) -> None
cc.list_themes() -> list[str]
```

### Palette Management

```python
cc.get_palette(name: str) -> list[str]
cc.list_palettes() -> list[str]
cc.auto_colors(n: int, palette: str = "aurora") -> list[str]
```

### Color Utilities

```python
cc.lighten(hex_color: str, amount: float = 0.2) -> str
cc.darken(hex_color: str, amount: float = 0.2) -> str
cc.opacity(hex_color: str, alpha: float = 0.5) -> str   # Returns rgba()
```

### Color Harmonies

```python
cc.complementary(hex_color: str) -> list[str]           # 2 colors
cc.triadic(hex_color: str) -> list[str]                  # 3 colors
cc.analogous(hex_color: str, steps=3, angle=30) -> list[str]
cc.split_complementary(hex_color: str) -> list[str]     # 3 colors
```

### `cc.ColorScale`

```python
scale = cc.ColorScale(stops: list[str])

scale.at(t: float) -> str          # Interpolate at position 0.0–1.0
scale.generate(n: int) -> list[str]  # n evenly-spaced colors
```

---

## HTTP API Endpoints

These serve the running ChartCraft server automatically. Useful for programmatic access.

| Method | Path | Description |
|--------|------|-------------|
| GET | `/api/spec?page=...` | Dashboard JSON spec |
| GET | `/api/events` | SSE stream (keep-alive) |
| GET | `/api/themes` | All theme definitions |
| GET | `/api/pages` | Navigation structure |
| GET | `/api/palettes` | All color palettes |
| POST | `/api/filter` | Apply filters, get updated spec |
| POST | `/api/layout` | Builder state → Python code |
| POST | `/api/parse` | Python code → builder state |
| GET | `/api/projects` | List saved projects |
| GET | `/api/projects/{id}` | Load a project |
| POST | `/api/projects` | Save a project |
| DELETE | `/api/projects/{id}` | Delete a project |
| GET | `/api/connections` | List registered connectors |
| POST | `/api/connections` | Register a connector |
| DELETE | `/api/connections/{id}` | Delete a connector |
| POST | `/api/query` | Execute SQL query |
| GET | `/api/schema?conn_id=...` | Database schema |
| GET | `/api/filter_options?filter_id=...` | Get cascading filter options |
| GET | `/api/export/pdf?page=...` | Export page as PDF |
| GET/POST | `/api/export/notebook` | Download Jupyter .ipynb |
| GET/POST | `/api/export/docker` | Download Docker .zip |
