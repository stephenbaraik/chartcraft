# Chart Types

ChartCraft includes 18+ chart types powered by Apache ECharts 5.5. Every chart shares a common set of parameters, plus type-specific options.

---

## Common Parameters

All chart types accept these parameters:

| Parameter | Type | Default | Description |
|-----------|------|---------|-------------|
| `data` | any | required | Dict, list, DataFrame, or callable |
| `x` | str | `None` | Column name for x-axis / categories |
| `y` | str or list | `None` | Column name(s) for y-axis / values |
| `title` | str | `""` | Chart title |
| `subtitle` | str | `""` | Chart subtitle |
| `colors` | list[str] | `None` | Custom hex colors (e.g. `["#6366F1", "#EC4899"]`) |
| `palette` | str | `None` | Named palette (e.g. `"aurora"`, `"sunset"`) |
| `col` | int | `0` | Grid column start (0–11) |
| `colspan` | int | `12` | Grid columns spanned (1–12) |
| `height` | int | `400` | Chart height in pixels |
| `refresh` | int | `None` | Auto-refresh interval in seconds |
| `data_fn` | callable | `None` | Function called to fetch live data |
| `linked_filters` | list[str] | `[]` | Filter names that trigger data re-fetch |
| `tooltip` | bool | `True` | Show tooltip on hover |
| `animate` | bool | `True` | Enable entry animations |
| `animate_duration` | int | `800` | Animation duration in milliseconds |
| `click_action` | str | `None` | `"filter"` or `"navigate"` on bar/point click |
| `click_target` | str | `None` | Filter name or URL path for click action |

---

## Bar Chart

Vertical or horizontal bars. Supports grouped and stacked variants.

```python
# Simple dict
cc.Bar({"Jan": 100, "Feb": 200, "Mar": 150}, title="Sales")

# Multi-series with column names
cc.Bar(
    {"region": ["North","South","East","West"],
     "q1": [120, 95, 140, 88],
     "q2": [135, 105, 155, 92]},
    x="region", y=["q1", "q2"],
    title="Sales by Region",
    col=0, colspan=8,
    grouped=True,           # Side-by-side bars
    # stacked=True,         # Stacked bars
    # horizontal=True,      # Flip axes
    # show_values=True,     # Show value labels on bars
)
```

| Option | Type | Default | Description |
|--------|------|---------|-------------|
| `horizontal` | bool | `False` | Flip to horizontal bars |
| `stacked` | bool | `False` | Stack series on top of each other |
| `grouped` | bool | `False` | Side-by-side bars (multi-series) |
| `show_values` | bool | `False` | Display value labels above each bar |

---

## Line Chart

Time-series lines. Supports multiple series, smooth curves, and dot markers.

```python
cc.Line(
    {"month": ["Jan","Feb","Mar","Apr","May","Jun"],
     "revenue": [310, 280, 350, 420, 390, 480],
     "target":  [300, 300, 350, 400, 400, 450]},
    x="month", y=["revenue", "target"],
    title="Revenue vs Target",
    col=0, colspan=12,
    smooth=True,            # Smooth curve interpolation
    show_dots=True,         # Show dot markers at data points
    colors=["#8B5CF6", "#3F3F46"],
)
```

| Option | Type | Default | Description |
|--------|------|---------|-------------|
| `smooth` | bool | `False` | Smooth curve instead of straight lines |
| `show_dots` | bool | `True` | Show point markers |
| `dash` | bool | `False` | Dashed line style |
| `fill` | bool | `False` | Fill area under the line |

---

## Area Chart

Line chart with filled area. Great for showing volume over time.

```python
cc.Area(
    {"month": ["Jan","Feb","Mar","Apr","May"],
     "new_users":  [1200, 1400, 1100, 1600, 1900],
     "lost_users": [200,  180,  220,  160,  190]},
    x="month", y=["new_users", "lost_users"],
    title="User Acquisition vs Churn",
    col=0, colspan=12,
    colors=["#10B981", "#EF4444"],
    stacked=False,          # True = stacked area chart
    gradient=True,          # Gradient fill (fades to transparent)
)
```

| Option | Type | Default | Description |
|--------|------|---------|-------------|
| `smooth` | bool | `False` | Smooth curves |
| `stacked` | bool | `False` | Stack series areas |
| `gradient` | bool | `True` | Gradient fill effect |

---

## Pie Chart

Proportional segments as a circle.

```python
cc.Pie(
    {"Enterprise": 45, "Professional": 30, "Starter": 25},
    title="Plan Distribution",
    col=0, colspan=6,
    label_position="outside",   # "outside", "inside", or "none"
    explode=[0],                # Index of segment to pull out
)
```

| Option | Type | Default | Description |
|--------|------|---------|-------------|
| `label_position` | str | `"outside"` | `"outside"`, `"inside"`, or `"none"` |
| `explode` | list[int] | `[]` | Indices of segments to pull out for emphasis |

---

## Donut Chart

Pie with a hollow center. Supports center text labels.

```python
cc.Donut(
    {"Enterprise": 45, "Professional": 30, "Starter": 25},
    title="Plan Split",
    col=8, colspan=4,
    inner_radius="55%",         # Size of center hole (CSS or %)
    center_text="Plans",        # Text displayed in the center
    label_position="none",
)
```

| Option | Type | Default | Description |
|--------|------|---------|-------------|
| `inner_radius` | str | `"50%"` | Size of the center hole |
| `center_text` | str | `""` | Label displayed in the center |
| `label_position` | str | `"outside"` | `"outside"`, `"inside"`, or `"none"` |

---

## Scatter Chart

X/Y point plot for correlation analysis.

```python
cc.Scatter(
    [{"price": 29.99, "rating": 4.2, "sales": 1200},
     {"price": 49.99, "rating": 4.5, "sales": 950},
     {"price": 19.99, "rating": 3.8, "sales": 1800}],
    x="price",
    y="rating",
    title="Price vs Rating",
    col=0, colspan=6,
)
```

| Option | Type | Default | Description |
|--------|------|---------|-------------|
| `size` | str | `None` | Column to use for point size (bubble chart) |
| `group` | str | `None` | Column to use for color grouping |
| `min_radius` | int | `4` | Minimum bubble radius in pixels |
| `max_radius` | int | `30` | Maximum bubble radius in pixels |

---

## Bubble Chart

Scatter chart where a third data dimension drives point size.

```python
# Bubble is an alias for Scatter with a size column
cc.Bubble(
    data,
    x="gdp",
    y="life_expectancy",
    size="population",      # Drives bubble size
    group="continent",      # Drives bubble color
    title="Global Development Indicators",
)
```

---

## Heatmap

Color-encoded matrix for showing patterns across two categorical dimensions.

```python
import random
random.seed(42)

cc.Heatmap(
    {
        "x_labels": ["Jan", "Feb", "Mar", "Apr", "May", "Jun"],
        "y_labels": ["<25", "25-34", "35-44", "45-54", "55+"],
        "matrix": [[random.randint(20, 100) for _ in range(6)] for _ in range(5)],
    },
    title="Cohort Retention by Age Group",
    col=0, colspan=6,
    color_scale=["#0F0F23", "#4F46E5", "#818CF8"],  # Low → High
    show_labels=True,
)
```

| Option | Type | Default | Description |
|--------|------|---------|-------------|
| `color_scale` | list[str] | theme default | Colors for low/mid/high values |
| `show_labels` | bool | `False` | Show value text inside each cell |

---

## Radar Chart

Spider/web chart for comparing multiple metrics across categories.

```python
cc.Radar(
    {"metric": ["Quality", "Price", "Speed", "Support", "Features"],
     "product_a": [90, 70, 80, 85, 75],
     "product_b": [75, 90, 70, 65, 85]},
    x="metric", y=["product_a", "product_b"],
    title="Product Comparison",
    col=0, colspan=6,
    shape="polygon",        # "polygon" or "circle"
    fill=True,              # Fill area inside the radar lines
)
```

| Option | Type | Default | Description |
|--------|------|---------|-------------|
| `shape` | str | `"polygon"` | `"polygon"` or `"circle"` grid shape |
| `fill` | bool | `True` | Fill the area enclosed by each series |

---

## Waterfall Chart

Shows cumulative effect of sequential positive and negative values.

```python
cc.Waterfall(
    {"label": ["Revenue", "COGS", "Gross", "Marketing", "OpEx", "EBITDA"],
     "value": [500, -180, 0, -60, -40, 0]},
    x="label", y="value",
    title="P&L Waterfall",
    col=0, colspan=8,
    show_total=True,                        # Highlight total bars
    positive_color="#10B981",               # Green for gains
    negative_color="#EF4444",               # Red for losses
)
```

Use `0` values for subtotal/total bars (rendered in the accent color).

| Option | Type | Default | Description |
|--------|------|---------|-------------|
| `show_total` | bool | `True` | Highlight subtotal/total bars distinctly |
| `positive_color` | str | theme success | Color for positive (upward) bars |
| `negative_color` | str | theme danger | Color for negative (downward) bars |

---

## Funnel Chart

Shows progressive narrowing through stages of a pipeline or process.

```python
cc.Funnel(
    {"stage":  ["Awareness", "Interest", "Consideration", "Intent", "Purchase"],
     "count":  [10000,         6200,         3800,           1900,    850]},
    x="stage", y="count",
    title="Purchase Funnel",
    col=0, colspan=6,
    orientation="vertical",     # "vertical" or "horizontal"
    gap=5,                       # Gap between funnel segments in pixels
    show_labels=True,
)
```

| Option | Type | Default | Description |
|--------|------|---------|-------------|
| `orientation` | str | `"vertical"` | `"vertical"` or `"horizontal"` |
| `gap` | int | `2` | Pixel gap between segments |
| `show_labels` | bool | `True` | Show percentage and count labels |

---

## Treemap

Hierarchical data as nested rectangles. Supports drill-down.

```python
cc.Treemap(
    {"name": "root", "children": [
        {"name": "Electronics", "value": 420, "children": [
            {"name": "Laptops", "value": 180},
            {"name": "Phones",  "value": 150},
        ]},
        {"name": "Clothing", "value": 280},
        {"name": "Home",     "value": 190},
    ]},
    title="Revenue by Category",
    col=0, colspan=7,
    drill_down=True,            # Click to zoom into child nodes
    show_breadcrumb=True,       # Show path breadcrumb when drilled in
)
```

| Option | Type | Default | Description |
|--------|------|---------|-------------|
| `drill_down` | bool | `True` | Enable click-to-drill-in behavior |
| `show_breadcrumb` | bool | `True` | Show breadcrumb navigation when drilled in |

---

## Sankey Diagram

Flow diagram showing quantities moving between nodes.

```python
cc.Sankey(
    [
        ("Web", "Landing", 5000),
        ("Organic", "Landing", 3000),
        ("Landing", "Signup", 4200),
        ("Landing", "Bounce", 3800),
        ("Signup", "Active", 3100),
        ("Signup", "Inactive", 1100),
    ],
    title="User Journey",
    col=0, colspan=12, height=400,
    orientation="horizontal",
    node_width=20,
    node_gap=10,
)
```

Data format: list of `(source, target, value)` tuples.

| Option | Type | Default | Description |
|--------|------|---------|-------------|
| `orientation` | str | `"horizontal"` | `"horizontal"` or `"vertical"` |
| `node_width` | int | `20` | Width of node rectangles in pixels |
| `node_gap` | int | `8` | Gap between nodes at the same level |

---

## Gauge Chart

Single numeric value displayed as a gauge or speedometer.

```python
cc.Gauge(
    72,                 # Current value
    title="Customer Satisfaction",
    col=0, colspan=3, height=240,
    min_val=0,
    max_val=100,
    arc_width=18,
    show_pointer=True,
    zones=[
        {"min": 0,  "max": 40,  "color": "#EF4444"},   # Danger
        {"min": 40, "max": 70,  "color": "#F59E0B"},   # Warning
        {"min": 70, "max": 100, "color": "#10B981"},   # Good
    ],
)
```

| Option | Type | Default | Description |
|--------|------|---------|-------------|
| `min_val` | float | `0` | Minimum value |
| `max_val` | float | `100` | Maximum value |
| `arc_width` | int | `18` | Thickness of the gauge arc |
| `show_pointer` | bool | `True` | Show needle pointer |
| `zones` | list[dict] | `[]` | Color zones: `[{"min":0,"max":50,"color":"#hex"}]` |

---

## Candlestick Chart

OHLC financial chart for stock or price data.

```python
cc.Candlestick(
    {"date":  ["2024-01-02", "2024-01-03", "2024-01-04"],
     "open":  [150.0, 152.5, 149.0],
     "high":  [154.5, 156.0, 153.5],
     "low":   [148.5, 151.0, 147.5],
     "close": [152.5, 149.0, 152.0],
     "volume":[1200000, 980000, 1450000]},
    x="date",
    title="AAPL Daily",
    col=0, colspan=12,
    show_volume=True,           # Show volume bar chart below
    ma_lines=[20, 50],          # Moving average overlays
)
```

| Option | Type | Default | Description |
|--------|------|---------|-------------|
| `show_volume` | bool | `True` | Show volume bars below the OHLC chart |
| `ma_lines` | list[int] | `[]` | Moving average periods to overlay (e.g. `[20, 50, 200]`) |

---

## Histogram

Distribution chart showing frequency of values across bins.

```python
cc.Histogram(
    {"values": [23, 45, 12, 67, 34, 89, 23, 45, 56, 78, 34, 23, 90, 12]},
    y="values",
    title="Order Value Distribution",
    col=0, colspan=8,
    bins=10,
    show_density=True,          # Overlay probability density curve
)
```

| Option | Type | Default | Description |
|--------|------|---------|-------------|
| `bins` | int | `10` | Number of histogram bins |
| `show_density` | bool | `False` | Overlay a KDE density curve |

---

## Box Plot

Statistical distribution: median, quartiles, and outliers.

```python
cc.BoxPlot(
    {"group": ["A","A","A","A","B","B","B","B"],
     "value": [10, 20, 15, 25, 30, 35, 28, 40]},
    x="group", y="value",
    title="Score Distribution by Group",
    col=0, colspan=8,
    show_outliers=True,
    notched=False,
)
```

| Option | Type | Default | Description |
|--------|------|---------|-------------|
| `show_outliers` | bool | `True` | Plot individual outlier points |
| `notched` | bool | `False` | Show notched box (confidence interval around median) |

---

## Table

Sortable, searchable data table with pagination.

```python
cc.Table(
    [{"Customer": "Acme Corp",   "Revenue": "$48,200", "Status": "Active"},
     {"Customer": "GlobalTech",  "Revenue": "$12,400", "Status": "Active"},
     {"Customer": "StartupXYZ",  "Revenue": "$2,100",  "Status": "At Risk"}],
    title="Customer Accounts",
    col=0, colspan=12, height=360,
    columns=["Customer", "Revenue", "Status"],   # Subset/order columns
    page_size=10,                                  # Rows per page
    sortable=True,
    searchable=True,
    striped=True,
)
```

| Option | Type | Default | Description |
|--------|------|---------|-------------|
| `columns` | list[str] | `None` | Which columns to show and in what order |
| `page_size` | int | `10` | Rows per page |
| `sortable` | bool | `True` | Click column headers to sort |
| `searchable` | bool | `False` | Show a search box above the table |
| `striped` | bool | `True` | Alternating row background color |

---

## Metric

Single prominent value with optional sparkline and trend indicator.

```python
cc.Metric(
    value="$4.2M",
    title="Total Revenue",
    col=0, colspan=3, height=200,
    sparkline=[5, 6, 4, 8, 7, 9, 8],   # Mini trend line
    trend=12.5,                           # Positive = green up arrow
)
```

| Option | Type | Default | Description |
|--------|------|---------|-------------|
| `value` | any | `None` | The displayed value |
| `sparkline` | list[float] | `None` | Mini trend line data |
| `trend` | float | `None` | Trend percentage; positive=up arrow, negative=down arrow |

---

## Layout Widgets

These aren't charts — they're structural elements for organizing your dashboard.

### SectionHeader

```python
cc.SectionHeader(
    title="Quarterly Breakdown",
    subtitle="Regional performance Q3 2024",
    col=0, colspan=12,
)
```

### Divider

```python
cc.Divider(col=0, colspan=12, color="#333333", thickness=1)
```

### Spacer

```python
cc.Spacer(col=0, colspan=12, height=24)
```

### TextBlock

```python
cc.TextBlock(
    content="This dashboard shows live sales performance updated every 30 seconds.",
    col=0, colspan=12,
    font_size=14,
    align="left",          # "left", "center", "right"
)
```

---

## Tips

**Multiple y-axis columns:** Pass `y` as a list to plot multiple series on one chart:
```python
cc.Line(data, x="month", y=["revenue", "cost", "profit"])
```

**Custom colors per series:** Length of `colors` list maps to series order:
```python
cc.Bar(data, colors=["#6366F1", "#EC4899", "#22D3EE"])
```

**Callable data for real-time:** Pass `data_fn` instead of `data` to refresh automatically:
```python
cc.Line(data_fn=lambda: db.query_dict("SELECT ..."), refresh=5)
```

**Chart height:** Default is `400px`. For compact layouts, `height=240` or `height=300` works well.
