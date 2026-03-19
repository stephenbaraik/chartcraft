# ◆ ChartCraft

### Python-powered dashboards that rival Power BI & Tableau.

Build stunning, interactive, real-time dashboards with **pure Python** — or design them visually with the **drag-and-drop Dashboard Builder**. No HTML, no JavaScript, no frontend skills needed.

> **One codebase. Two workflows.** Write Python *or* drag-and-drop. The builder generates Python code. The code renders the builder. They stay in sync.

---

## Table of Contents

- [Quick Start](#-quick-start)
- [Visual Dashboard Builder](#-visual-dashboard-builder)
- [Color Picker System](#-color-picker-system)
- [Chart Types (17+)](#-chart-types)
- [Themes (11 built-in)](#-themes)
- [Database Connectors](#-database-connectors)
- [Real-Time Data](#-real-time-data)
- [Grid Layout System](#-grid-layout-system)
- [KPIs, Filters & Tables](#-kpis-filters--tables)
- [Export & Deployment](#-export--deployment)
- [Architecture](#-architecture)
- [Tech Stack](#-tech-stack)
- [API Reference](#-api-reference)
- [Implementation Guide for Claude Code](#-implementation-guide-for-claude-code)
- [File Structure](#-file-structure)
- [Acceptance Criteria](#-acceptance-criteria)

---

## 🚀 Quick Start

```bash
pip install chartcraft
```

```python
import chartcraft as cc

app = cc.App("Sales Dashboard", theme="midnight")

@app.page("/")
def home():
    return cc.Dashboard(
        title="Sales Overview",
        kpis=[
            cc.KPI("Revenue", "$1.2M", change=12.5),
            cc.KPI("Users", "45.2K", change=-3.2),
            cc.KPI("Conversion", "4.8%", change=0.5),
        ],
        charts=[
            cc.Bar({"Q1": 100, "Q2": 200, "Q3": 150, "Q4": 300},
                   title="Quarterly Sales", col=0, colspan=8),
            cc.Donut({"Enterprise": 45, "Pro": 30, "Free": 25},
                     title="Plan Split", col=8, colspan=4),
        ],
    )

app.run()  # → http://localhost:8050
```

That's it. A production-grade interactive dashboard is live in your browser.

Or open the **visual builder** at `http://localhost:8050/builder` to design dashboards by dragging, dropping, and picking colors — zero code required.

---

## 🖱️ Visual Dashboard Builder

The builder is the flagship feature — a full-screen Figma-like canvas where users design dashboards visually. ChartCraft generates equivalent Python code in real-time.

### Drag-and-Drop Canvas

- **Free-form placement** — drag chart widgets from the sidebar onto an infinite canvas. Place them anywhere.
- **Snap-to-grid** — optional 12-column grid with visual guide lines that appear while dragging. Toggle between free-form and grid modes.
- **Resize handles** — every chart and KPI card has 8-point resize handles (4 corners + 4 edges). Minimum size constraints per chart type.
- **Multi-select** — Shift+click or marquee-drag to select multiple widgets. Move, align, or resize as a group.
- **Z-ordering** — right-click context menu: Bring to Front, Send to Back, Move Forward, Move Backward.
- **Undo / Redo** — full history stack. Ctrl+Z / Ctrl+Shift+Z for all layout and style changes.
- **Responsive preview** — toggle between Desktop (1440px), Tablet (768px), and Mobile (375px) views.

### Widget Library (Left Sidebar)

Draggable widgets organized by category:

| Category | Widgets |
|----------|---------|
| **Charts** | Bar, Line, Area, Pie, Donut, Scatter, Bubble, Heatmap, Radar, Waterfall, Funnel, Treemap, Sankey, Gauge, Candlestick, Histogram, Box Plot |
| **KPIs** | Standard, Sparkline, Progress, Comparison, Trend |
| **Layout** | Divider, Spacer, Section Header, Text Block, Image, Container/Group |
| **Filters** | Dropdown, Multi-Select, Date Range, Slider, Search Box, Toggle |
| **Tables** | Data Table (sortable), Paginated Table, Pivot Table |

### Properties Panel (Right Sidebar)

When a widget is selected, a context-sensitive panel appears with five tabs:

| Tab | Controls |
|-----|----------|
| **Data** | Data source selector, SQL query editor, column-to-axis mapper, preview of first 10 rows, refresh interval |
| **Style** | Color pickers for every element, font selector, border radius slider, shadow toggle, opacity slider, gradient controls |
| **Layout** | Exact X/Y/W/H inputs, padding, margin, alignment, grid column/row overrides |
| **Animation** | Toggle animation, duration (ms), easing curve selector, stagger delay |
| **Interaction** | Tooltips on/off, hover effects, click actions (drill-down, filter, navigate) |

### Bidirectional Code Sync

A collapsible bottom panel shows the Python code equivalent of the current canvas state:

- Every drag, resize, or color change **instantly updates the code**.
- Users can **edit the code directly** — changes reflect on the canvas in real-time.
- Parse errors are highlighted inline.
- **Export** as a standalone `.py` file, Jupyter notebook (`.ipynb`), or Docker-ready project folder.

### Builder Layout

```
+------------------------------------------------------------------+
|  TOOLBAR (48px)                                                  |
|  [Undo] [Redo] [Save] [Export] [Theme: ___] [Preview] [Deploy]  |
+--------+--------------------------------------------+-----------+
|        |                                            |           |
| WIDGET |          CANVAS (flex: 1)                  | PROPERTIES|
| LIBRARY|                                            |   PANEL   |
| (240px)|    Drag-and-drop dashboard canvas          |  (320px)  |
|        |    with live chart previews                |           |
|  Bar   |                                            |  [Data]   |
|  Line  |    [Chart A]  [Chart B]                    |  [Style]  |
|  Pie   |                                            |  [Layout] |
|  ...   |         [Chart C - full width]             |  [Anim]   |
|        |                                            |           |
+--------+--------------------------------------------+-----------+
|  CODE PREVIEW (200px, collapsible)                              |
|  import chartcraft as cc                                        |
|  app = cc.App('Dashboard', theme='midnight')                    |
|  ...                                                            |
+------------------------------------------------------------------+
```

---

## 🎨 Color Picker System

Every visual element in ChartCraft is customizable via a professional-grade color picker.

### What Can Be Colored

- Bar colors, line colors, area fill gradients
- Chart background, card background
- Border colors, grid line colors
- Text colors (title, subtitle, labels, values)
- KPI card accent stripe
- Tooltip background and text
- Shadow colors with opacity

### Color Picker Features

```
+-----------------------------------+
|  Color Picker                 [x] |
+-----------------------------------+
|  +---------------------------+    |
|  |   [Hue Ring]              |    |
|  |     +---------------+     |    |
|  |     | SV Square     |     |    |
|  |     | (drag cursor) |     |    |
|  |     +---------------+     |    |
|  +---------------------------+    |
|                                   |
|  Alpha: [=======o--------] 75%    |
|                                   |
|  Hex: [#6366F1]     [Eyedropper]  |
|  R: [99]  G: [102]  B: [241]     |
|  H: [239] S: [95]   L: [67]      |
|                                   |
|  Theme Palette:                   |
|  [*][*][*][*][*][*][*][*][*][*]   |
|                                   |
|  Recent:                          |
|  [*][*][*][*][*][*][*][*]         |
|                                   |
|  Harmonies: [Comp] [Tri] [Analog] |
|                                   |
|  [Reset] [Cancel] [Apply]         |
+-----------------------------------+
```

| Component | Description |
|-----------|-------------|
| **HSV Color Wheel** | Circular hue ring (conic gradient SVG). Drag indicator to select hue (0-360°). |
| **SV Square** | Saturation (horizontal, 0-100%) × Value/Brightness (vertical, 100-0%). Nested inside the hue ring. |
| **Alpha Slider** | Horizontal opacity slider (0-100%). Enables semi-transparent colors. |
| **Hex Input** | Text field for `#RRGGBB` or `#RRGGBBAA`. Live validation. |
| **RGB Sliders** | Three range inputs (0-255). Bidirectionally synced with the wheel. |
| **HSL Sliders** | H (0-360), S (0-100), L (0-100). Bidirectionally synced. |
| **Eyedropper** | Invokes the `EyeDropper` Web API to sample any color on screen (Chromium). |
| **Palette Swatches** | 10 colors from the active theme palette, plus 8 recently-used colors. |
| **Gradient Editor** | Two-stop (or multi-stop) gradient builder with angle control and opacity sliders. For area fills and backgrounds. |
| **Color Harmonies** | Auto-suggest complementary, analogous, triadic, and split-complementary palettes from any selected color. |

### Color Picker State Model

HSV is the canonical representation. All other formats are derived:

```javascript
const colorState = signal({
  h: 0,        // Hue: 0-360
  s: 100,      // Saturation: 0-100
  v: 100,      // Value/Brightness: 0-100
  a: 100,      // Alpha: 0-100
});

// Derived (computed signals):
const hex = computed(() => hsvToHex(colorState.value));
const rgb = computed(() => hsvToRgb(colorState.value));
const hsl = computed(() => hsvToHsl(colorState.value));
```

Color changes are debounced at 16ms (60fps) and instantly update the target chart on the canvas.

### Using Custom Colors in Python

Colors selected in the builder appear in the generated code:

```python
cc.Bar(
    data, x="month", y="revenue",
    title="Sales",
    colors=["#6366F1", "#EC4899", "#22D3EE"],   # ← from color picker
    col=0, colspan=8,
)
```

Or set colors programmatically:

```python
# Per-chart custom colors
cc.Line(data, colors=["#FF6B6B", "#4ECDC4", "#45B7D1"])

# Use a named palette
cc.Bar(data, palette="sunset")

# Color utilities
cc.lighten("#6366F1", 0.3)       # → lighter shade
cc.darken("#6366F1", 0.3)        # → darker shade
cc.opacity("#6366F1", 0.5)       # → "rgba(99,102,241,0.5)"
cc.auto_colors(5, "aurora")      # → 5 colors from aurora palette

# Custom palette
scale = cc.ColorScale(["#FF0000", "#00FF00", "#0000FF"])
scale.generate(10)               # → 10 interpolated colors
```

---

## 📊 Chart Types

17 chart types built on Apache ECharts 5.5 with GPU-accelerated canvas rendering.

| Chart | Constructor | Data Shape | Key Options |
|-------|------------|------------|-------------|
| **Bar** | `cc.Bar(data, x, y)` | labels + datasets | `horizontal`, `stacked`, `grouped` |
| **Line** | `cc.Line(data, x, y)` | labels + datasets | `smooth`, `show_dots`, `dash` |
| **Area** | `cc.Area(data, x, y)` | labels + datasets | gradient fill, stacked |
| **Pie** | `cc.Pie(data)` | labels + values | label position, explode |
| **Donut** | `cc.Donut(data)` | labels + values | inner radius, center text |
| **Scatter** | `cc.Scatter(data, x, y)` | points `{x, y, size, group}` | size encoding, color groups |
| **Bubble** | `cc.Scatter(data, x, y, size)` | points with size | min/max radius |
| **Heatmap** | `cc.Heatmap(matrix)` | matrix + axis labels | color scale, cell labels |
| **Radar** | `cc.Radar(data)` | labels + datasets | polygon/circle shape, fill |
| **Waterfall** | `cc.Waterfall(data)` | labels + deltas | auto total bar, connectors |
| **Funnel** | `cc.Funnel(data)` | labels + values | orientation, gap, labels |
| **Treemap** | `cc.Treemap(data)` | `{name, value}` tree | drill-down, breadcrumb |
| **Sankey** | `cc.Sankey(flows)` | `[(src, tgt, val)]` | orientation, node width |
| **Gauge** | `cc.Gauge(value)` | value + min/max | zones, arc width, pointer |
| **Candlestick** | `cc.Candlestick(data)` | dates + OHLC | volume overlay, MA lines |
| **Table** | `cc.Table(data, x, y)` | columns + rows | sort, filter, paginate |
| **Metric** | `cc.Metric(value)` | single value | prefix, suffix, sparkline |

### Data Format Support

ChartCraft accepts anything Python developers work with:

```python
# Dict of scalars → Pie, Bar, Treemap
{"Chrome": 65, "Firefox": 20, "Safari": 15}

# Dict of lists → Line, Bar, Area
{"month": ["Jan", "Feb", "Mar"], "sales": [100, 200, 150]}

# List of dicts → Any chart
[{"month": "Jan", "sales": 100}, {"month": "Feb", "sales": 200}]

# SQL query results (list of tuples)
db.query("SELECT region, SUM(revenue) FROM sales GROUP BY region")

# Pandas DataFrame
df = pd.DataFrame({"x": [1, 2, 3], "y": [4, 5, 6]})

# Callable for real-time data
lambda: db.query("SELECT * FROM live_metrics")
```

---

## 🎨 Themes

11 built-in themes. Switch live in the browser with the ◆ Theme button.

| Theme | Style | Background | Accent |
|-------|-------|------------|--------|
| `default` | Modern dark | `#09090B` | Indigo `#6366F1` |
| `midnight` | Deep purple | `#070318` | Purple `#8B5CF6` |
| `obsidian` | Pitch black | `#0A0A0A` | Cyan `#06B6D4` |
| `frost` | Clean light | `#F0F4F8` | Blue `#0284C7` |
| `ember` | Warm dark | `#1A0A00` | Orange `#F97316` |
| `jade` | Green dark | `#021A0E` | Green `#10B981` |
| `slate` | Professional light | `#FFFFFF` | Navy `#1E40AF` |
| `candy` | Pink dark | `#1A0015` | Pink `#EC4899` |
| `arctic` | Ice blue dark | `#0B1120` | Sky `#38BDF8` |
| `retro` | Vintage teal | `#1D3557` | Gold `#E9C46A` |
| `scientific` | Academic light | `#FAFAFA` | Slate `#4E79A7` |

```python
app = cc.App("Dashboard", theme="midnight")

# Or per-chart:
cc.Bar(data, theme="frost")
```

### Theme Tokens

Every theme is a dataclass with 25+ design tokens:

| Category | Tokens | Purpose |
|----------|--------|---------|
| Backgrounds | `bg`, `bg_card`, `bg_elevated` | Page, card surface, hover states |
| Typography | `text`, `text_secondary`, `text_muted` | Primary, secondary, disabled |
| Accents | `accent`, `accent_secondary` | Brand color + companion |
| Semantic | `success`, `danger`, `warning` | Positive, negative, caution |
| Structure | `border`, `grid`, `shadow` | Borders, gridlines, shadows |
| Fonts | `font_display`, `font_body`, `font_mono` | Headings, body, data values |
| Shape | `radius`, `glass`, `animate` | Border radius, effects, motion |

### Custom Themes

```python
my_theme = cc.Theme(
    name="brand",
    palette="aurora",
    bg="#0A0A0A",
    bg_card="#1A1A1A",
    text="#FFFFFF",
    accent="#FF6B00",
    font_display="Outfit",
)
cc.register_theme("brand", my_theme)
app = cc.App("Dashboard", theme="brand")
```

### Color Palettes (16 built-in)

```python
cc.get_palette("aurora")       # Vibrant purples & pinks
cc.get_palette("sunset")       # Warm reds & oranges
cc.get_palette("ocean")        # Cool blues
cc.get_palette("forest")       # Natural greens
cc.get_palette("neon")         # Electric neons
cc.get_palette("pastel")       # Soft pastels
cc.get_palette("categorical")  # Tableau-inspired
cc.get_palette("diverging")    # Red ↔ Blue diverging scale
# + 8 more: midnight, corporate, minimal, earth, retro, candy, sequential_blues, sequential_greens
```

---

## 🔌 Database Connectors

### SQL Databases

```python
# SQLite (built-in, zero dependencies)
db = cc.connect_sql("sqlite:///analytics.db")

# PostgreSQL
db = cc.connect_sql("postgresql://user:pass@host:5432/db")

# MySQL
db = cc.connect_sql("mysql+pymysql://user:pass@host/db")

# SQL Server
db = cc.connect_sql("mssql+pyodbc://user:pass@host/db")
```

```python
# Query methods
db.query("SELECT * FROM sales")            # → list of tuples
db.query_dict("SELECT * FROM sales")       # → list of dicts
db.query_df("SELECT * FROM sales")         # → pandas DataFrame
db.tables()                                 # → ["sales", "users", ...]
db.schema("sales")                          # → [{"name": "id", "type": "INTEGER"}, ...]
```

### CSV / TSV Files

```python
data = cc.connect_csv("sales.csv")
data = cc.connect_csv("./data_folder/")     # All CSVs in folder

data.tables()                               # → ["sales"]
data.query("sales")                         # → list of dicts
data.query_as_columns("sales")              # → {"name": [...], "amount": [...]}
```

### REST APIs

```python
api = cc.connect_api(
    "https://api.example.com",
    headers={"Authorization": "Bearer ..."},
)
users = api.get("/users", params={"limit": 100})
api.post("/events", data={"type": "dashboard_view"})
```

### Connector Summary

| Connector | Connection String | Dependencies |
|-----------|------------------|--------------|
| SQLite | `sqlite:///path/to/db.sqlite` | None (stdlib) |
| PostgreSQL | `postgresql://user:pass@host/db` | sqlalchemy + psycopg2 |
| MySQL | `mysql+pymysql://user:pass@host/db` | sqlalchemy + pymysql |
| SQL Server | `mssql+pyodbc://user:pass@host/db` | sqlalchemy + pyodbc |
| CSV / TSV | File path or directory path | None (stdlib) |
| REST API | `https://api.example.com` | None (urllib) |
| WebSocket | `wss://stream.example.com` | websockets |
| Google Sheets | Sheet ID + credentials JSON | google-api-python-client |
| MongoDB | `mongodb://user:pass@host/db` | pymongo |

---

## ⚡ Real-Time Data

ChartCraft uses **Server-Sent Events (SSE)** for real-time data push. Add `refresh=N` to any chart or KPI:

```python
@app.page("/")
def live():
    return cc.Dashboard(
        title="Live Metrics",
        refresh=30,  # Full dashboard refresh every 30s

        kpis=[
            cc.KPI(
                "Active Users",
                data_fn=lambda: db.query("SELECT COUNT(*) FROM sessions")[0][0],
                refresh=5,  # This KPI refreshes every 5 seconds
            ),
        ],

        charts=[
            cc.Line(
                lambda: db.query_dict(
                    "SELECT ts, value FROM metrics ORDER BY ts DESC LIMIT 100"
                ),
                x="ts", y="value",
                title="Real-Time Stream",
                refresh=3,  # This chart refreshes every 3 seconds
            ),
        ],
    )
```

### How It Works

1. Server starts background threads per refreshable component.
2. Every N seconds, the thread calls the data function and serializes the result.
3. Server pushes the updated chart spec via SSE to all connected browsers.
4. Frontend receives the event and calls `echartsInstance.setOption()` — animated in-place update.
5. SSE auto-reconnects on disconnect (3-second retry).

Charts and KPIs update **independently** — no page reload needed.

---

## 📋 Grid Layout System

Dashboards use a **12-column grid** (same model as Bootstrap / CSS Grid):

```python
cc.Dashboard(
    charts=[
        # Full width (12 of 12 columns)
        cc.Line(data, title="Trend", col=0, colspan=12),

        # Two-column split (8 + 4)
        cc.Bar(data, title="Sales", col=0, colspan=8),
        cc.Pie(data, title="Split", col=8, colspan=4),

        # Three equal columns (4 + 4 + 4)
        cc.Gauge(85, title="CPU", col=0, colspan=4),
        cc.Gauge(62, title="Memory", col=4, colspan=4),
        cc.Gauge(91, title="Disk", col=8, colspan=4),

        # Custom height
        cc.Sankey(flows, title="Flow", col=0, colspan=12, height=500),
    ]
)
```

In the **visual builder**, grid positions are computed automatically from pixel coordinates:

```
col = round(x / canvasWidth * 12)
colspan = round(w / canvasWidth * 12)
```

---

## 📈 KPIs, Filters & Tables

### KPI Cards

```python
cc.KPI("Revenue", "$1.2M", change=12.5)                    # Basic
cc.KPI("Users", "45K", change=-3.2, change_label="vs Q3")  # Custom label
cc.KPI("Trend", "$8.4M", sparkline=[5,6,4,8,7,9,8])       # With sparkline
cc.KPI("Live", data_fn=lambda: get_count(), refresh=5)      # Real-time
cc.KPI("Price", prefix="$", suffix="/mo", data_fn=get_price)
```

### Interactive Filters

```python
cc.Dashboard(
    filters=[
        cc.Filter("region", label="Region", type="select",
                  options=["North", "South", "East", "West"]),
        cc.Filter("date", label="Date Range", type="date_range"),
        cc.Filter("search", label="Search", type="text"),
        cc.Filter("threshold", label="Min Revenue", type="slider",
                  options=[0, 1000000], default=100000),
    ],
    charts=[...],
)
```

### Data Tables

```python
cc.Table(
    data, x="name", y=["revenue", "cost", "margin"],
    title="Sales Detail",
    col=0, colspan=12,
)
```

Tables support sortable columns, pagination, and inline search.

---

## 💾 Export & Deployment

### Static HTML Export

```python
# No server needed — standalone HTML file
app.save("dashboard.html")

# Quick export without creating an App
cc.quick_dashboard(
    title="Report",
    charts=[cc.Bar(data, title="Sales")],
    theme="frost",
    save_path="report.html",
)
```

### Multi-Page Dashboards

```python
app = cc.App("Analytics Platform", theme="midnight")

@app.page("/")
def overview():
    return cc.Dashboard(title="Overview", charts=[...])

@app.page("/sales")
def sales():
    return cc.Dashboard(title="Sales", charts=[...])

@app.page("/users")
def users():
    return cc.Dashboard(title="Users", charts=[...])

app.run()
```

### Docker Deployment

```dockerfile
FROM python:3.12-slim
COPY . /app
WORKDIR /app
RUN pip install chartcraft sqlalchemy psycopg2-binary
EXPOSE 8050
CMD ["python", "app.py"]
```

---

## 🏗️ Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                     User Python Code                         │
│                      (app.py)                                │
└──────────────────────┬──────────────────────────────────────┘
                       │
                       ▼
┌──────────────────────────────────────────────────────────────┐
│              ChartCraft SDK (Pure Python)                     │
│                                                              │
│  ┌──────────┐  ┌──────────┐  ┌──────────┐  ┌────────────┐  │
│  │ Models   │  │ Themes   │  │ Colors   │  │ Connectors │  │
│  │ Chart    │  │ 11 built │  │ 16 pals  │  │ SQL/CSV/   │  │
│  │ KPI      │  │ -in +    │  │ HSV/RGB  │  │ API/WS     │  │
│  │ Dashboard│  │ custom   │  │ scales   │  │            │  │
│  └──────────┘  └──────────┘  └──────────┘  └────────────┘  │
│                       │                                      │
│              to_spec() → JSON                                │
└──────────────────────┬──────────────────────────────────────┘
                       │
                       ▼
┌──────────────────────────────────────────────────────────────┐
│               HTTP Server (stdlib)                            │
│                                                              │
│  GET /           → Serve Viewer SPA                          │
│  GET /builder    → Serve Dashboard Builder SPA               │
│  GET /api/spec   → Return dashboard JSON spec                │
│  GET /api/events → SSE real-time stream                      │
│  POST /api/layout→ Save builder state, generate Python code  │
│  POST /api/filter→ Apply filters, trigger data refresh       │
│                                                              │
│  ┌─────────────┐  ┌─────────────┐  ┌──────────────────┐    │
│  │ SSE Manager │  │ Refresh     │  │ Code Generator   │    │
│  │ broadcast() │  │ Threads     │  │ canvas → .py     │    │
│  └─────────────┘  └─────────────┘  └──────────────────┘    │
└──────────────────────┬──────────────────────────────────────┘
                       │
                       ▼
┌──────────────────────────────────────────────────────────────┐
│                Frontend (Browser)                             │
│                                                              │
│  ┌─────────────────────────┐  ┌────────────────────────┐    │
│  │   VIEWER MODE           │  │   BUILDER MODE         │    │
│  │   Vanilla JS + ECharts  │  │   Preact + ECharts     │    │
│  │   - Render spec as-is   │  │   - Drag-and-drop      │    │
│  │   - SSE listener        │  │   - Color picker       │    │
│  │   - Theme CSS vars      │  │   - Properties panel   │    │
│  │   - Responsive grid     │  │   - Live code preview  │    │
│  └─────────────────────────┘  └────────────────────────┘    │
└──────────────────────────────────────────────────────────────┘
```

### Data Flow: Dashboard Load

1. User runs `python app.py`. Server starts on port 8050.
2. Browser opens `/`. Server calls the `@app.page("/")` function.
3. Page function returns a `Dashboard` object.
4. Server calls `dashboard.to_spec()` → JSON serialization.
5. JSON + theme CSS injected into the HTML template.
6. Browser renders: parse spec → create ECharts instances → render KPIs.
7. If `refresh > 0`, browser opens SSE connection to `/api/events`.
8. Server spawns background threads per refreshable component.
9. On each tick: call data function → serialize → broadcast via SSE.
10. Browser receives event → `echartsInstance.setOption()` with animation.

### Data Flow: Builder Save

1. User designs dashboard in `/builder` via drag-and-drop.
2. Each change updates local state: `{ widgets: [{id, type, x, y, w, h, config, colors}] }`.
3. On Save: POST state to `/api/layout`.
4. Server generates Python code and writes to `app.py`.
5. Server hot-reloads page function and broadcasts SSE `dashboard-update`.
6. All connected viewers see the updated dashboard instantly.

---

## 🛠️ Tech Stack

| Layer | Technology | Why |
|-------|-----------|-----|
| **Backend** | Python 3.11+ stdlib | Zero deps for core. `http.server`, `threading`, `sqlite3`, `json`. |
| **API (upgrade)** | FastAPI (optional) | Async, auto-docs, validation. Use stdlib `http.server` for v1. |
| **Real-time** | Server-Sent Events | Simpler than WebSocket for server→client push. No library needed. |
| **Charts** | Apache ECharts 5.5+ (CDN) | 20+ chart types, GPU canvas, animations, responsive, accessible. |
| **Builder UI** | Preact 10.x + HTM (CDN) | 3KB React-compatible. No build step. JSX via tagged templates. |
| **State** | Preact Signals | Fine-grained reactivity. No Redux boilerplate. |
| **Drag & Drop** | Custom (PointerEvents) | Cross-device. No library overhead. |
| **Color Picker** | Custom Preact component | Full HSV wheel + sliders + eyedropper. |
| **Styling** | CSS Variables | Theme switching via CSS custom properties. No build step. |
| **Persistence** | SQLite (layouts) + filesystem (.py) | Layouts in SQLite. Generated code as .py files. |

---

## 📖 API Reference

### `cc.App`

```python
app = cc.App(title, theme="default", favicon="")
```

| Method | Description |
|--------|-------------|
| `@app.page(path)` | Decorator to register a dashboard page. Function must return `cc.Dashboard`. |
| `app.run(host, port, debug, open_browser)` | Start HTTP server. Blocks until Ctrl+C. |
| `app.save(path, page="/", theme=None)` | Export dashboard as standalone HTML. |
| `app.to_html(page="/", theme=None)` | Return HTML string (no file write). |

### `cc.Dashboard`

```python
cc.Dashboard(title, subtitle, kpis, charts, filters, cols=12, refresh=None)
```

| Method | Description |
|--------|-------------|
| `.add_kpi(title, value, ...)` | Fluent API to add a KPI. Returns self. |
| `.add_chart(chart)` | Fluent API to add a chart. Returns self. |
| `.add_filter(name, ...)` | Fluent API to add a filter. Returns self. |
| `.to_spec()` | Serialize to JSON-safe dict. |

### All Chart Constructors

Common parameters for every chart type:

| Parameter | Type | Description |
|-----------|------|-------------|
| `data` | any | Dict, list, DataFrame, callable, or SQL result tuples. |
| `x` | str | Column name for x-axis / categories. |
| `y` | str or list | Column name(s) for y-axis / values. |
| `title` | str | Chart title. |
| `subtitle` | str | Chart subtitle. |
| `colors` | list[str] | Custom hex colors. **This is what the color picker writes.** |
| `palette` | str | Named palette from `cc.PALETTES`. |
| `col` | int | Grid column start (0-11). |
| `colspan` | int | Grid columns spanned (1-12). |
| `height` | int | Chart height in pixels (default 400). |
| `refresh` | int | Auto-refresh interval in seconds. `None` = off. |

### `cc.KPI`

```python
cc.KPI(title, value, change, change_label, prefix, suffix, icon, color, sparkline, refresh, data_fn)
```

### Connectors

```python
db  = cc.connect_sql(connection_string)   # → SQLConnector
csv = cc.connect_csv(path)                # → CSVConnector
api = cc.connect_api(base_url, headers)   # → APIConnector
```

| Method | Returns | Description |
|--------|---------|-------------|
| `db.query(sql)` | list[tuple] | Execute SQL, return rows as tuples. |
| `db.query_dict(sql)` | list[dict] | Execute SQL, return rows as dicts. |
| `db.query_df(sql)` | DataFrame | Execute SQL, return pandas DataFrame. |
| `db.tables()` | list[str] | List all table names. |
| `db.schema(table)` | list[dict] | Column names and types. |
| `csv.query(table)` | list[dict] | Read CSV data as list of dicts. |
| `csv.query_as_columns(table)` | dict[str, list] | Read CSV as dict of columns. |
| `api.get(endpoint, params)` | any | HTTP GET, return parsed JSON. |
| `api.post(endpoint, data)` | any | HTTP POST, return parsed JSON. |

---

## 🔧 Implementation Guide for Claude Code

Build in this exact sequence. Each phase is independently testable.

### Phase 1: Core SDK (Week 1)

- [ ] `core/models.py` — all 17 chart types, KPI, Dashboard, Filter, DataSource classes with `to_spec()` JSON serialization
- [ ] `core/theme.py` — Theme dataclass with 25+ tokens, 11 built-in themes, `to_css_vars()` export
- [ ] `core/colors.py` — 16 palettes, `auto_colors()`, `ColorScale`, hex/rgb/hsl converters
- [ ] `server/handler.py` — HTTP request handler with all 11 API routes
- [ ] `server/sse.py` — SSE connection manager with broadcast
- [ ] `static/viewer.html` — SPA with ECharts rendering, tooltips, theme switching, SSE listener
- [ ] `connectors/` — SQL (SQLite + SQLAlchemy), CSV, REST API connectors
- [ ] **Test:** `python app.py` → full dashboard at `localhost:8050`

### Phase 2: Visual Builder Foundation (Week 2)

- [ ] `builder/builder.html` — Preact SPA (CDN, no build step)
- [ ] Canvas component — absolute positioning, PointerEvent drag
- [ ] Widget Library sidebar — 17 chart types as draggable items
- [ ] Resize handles — 8-point with min/max constraints
- [ ] Snap-to-grid — visual guide lines, toggle grid/free-form
- [ ] Undo/redo — full history stack
- [ ] Properties Panel — Data, Style, Layout tabs
- [ ] **Test:** drag charts, resize, see live ECharts previews on canvas

### Phase 3: Color Picker (Week 3)

- [ ] `ColorPicker` Preact component — HSV wheel + SV square + alpha slider
- [ ] Hex / RGB / HSL inputs — bidirectional sync
- [ ] EyeDropper API integration
- [ ] Palette swatches (theme + recent colors)
- [ ] Gradient editor for area fills
- [ ] Color harmony suggestions
- [ ] Wire picker to all chart properties
- [ ] **Test:** pick any color → chart updates in real-time on canvas

### Phase 4: Code Generation (Week 4)

- [ ] `server/codegen.py` — canvas state → valid Python script
- [ ] Code Preview panel — live Python code, collapsible bottom panel
- [ ] Bidirectional sync — code edits update canvas, canvas updates code
- [ ] Export — `.py`, `.ipynb`, Docker project
- [ ] Save — POST layout → SQLite → hot-reload
- [ ] **Test:** design in builder → export .py → run it → identical dashboard

### Phase 5: Real-Time & Connectors (Week 5)

- [ ] Per-chart refresh with background threads + SSE push
- [ ] WebSocket connector for sub-second streaming
- [ ] Data source config UI in properties panel (SQL editor)
- [ ] Filter interactivity — filter change re-queries linked charts
- [ ] Loading states and error handling
- [ ] **Test:** connect PostgreSQL → charts refresh every 5s with live data

### Phase 6: Polish & Deploy (Week 6)

- [ ] Responsive layout — desktop/tablet/mobile preview modes
- [ ] PDF export (headless Chrome / Playwright)
- [ ] Authentication — optional login with API key or OAuth
- [ ] Docker deployment — Dockerfile + docker-compose.yml
- [ ] Performance — lazy-load, virtualize large datasets
- [ ] Accessibility — ARIA labels, keyboard nav, high-contrast
- [ ] Documentation site — auto-generated from docstrings

---

## 📁 File Structure

```
chartcraft/
├── __init__.py                    # Public API: App, Dashboard, charts, connectors
├── core/
│   ├── __init__.py
│   ├── models.py                  # Chart, KPI, Dashboard, Filter, DataSource
│   ├── theme.py                   # Theme class, THEMES registry, CSS export
│   ├── colors.py                  # Palettes, ColorScale, hex/rgb/hsl utils
│   └── serializer.py              # JSON serialization (numpy/pandas support)
├── connectors/
│   ├── __init__.py                # Factory functions: connect_sql, connect_csv, connect_api
│   ├── sql.py                     # SQLConnector (SQLite stdlib + SQLAlchemy fallback)
│   ├── csv_connector.py           # CSV/TSV reader with auto type detection
│   ├── api.py                     # REST API connector with auth
│   └── websocket.py               # WebSocket streaming connector
├── server/
│   ├── __init__.py                # AppServer, start/stop
│   ├── handler.py                 # HTTP request handler, all API routes
│   ├── sse.py                     # SSE connection manager
│   └── codegen.py                 # Python code generator from builder state
├── builder/
│   ├── __init__.py
│   ├── builder.html               # Dashboard Builder SPA (Preact + HTM)
│   └── components/
│       ├── canvas.js              # Drag-and-drop canvas
│       ├── color_picker.js        # HSV wheel + sliders + eyedropper
│       ├── widget_library.js      # Left sidebar with draggable widgets
│       ├── properties_panel.js    # Right sidebar config panel
│       ├── code_preview.js        # Bottom panel with live Python code
│       └── toolbar.js             # Top bar: undo/redo/save/theme
├── static/
│   └── viewer.html                # Dashboard viewer SPA (vanilla JS + ECharts)
├── templates/
│   └── app_template.py            # Template for generated Python code
├── setup.py
└── README.md
```

---

## ✅ Acceptance Criteria

### Dashboard Builder
- [ ] Drag any of 17 chart types from sidebar onto canvas
- [ ] Charts render with live ECharts preview using sample data
- [ ] Drag to reposition with visual snap guides
- [ ] 8-point resize handles with min size constraints
- [ ] Multi-select and move/align as group
- [ ] Undo/redo for all layout and style changes
- [ ] Responsive preview: desktop / tablet / mobile

### Color Picker
- [ ] Click any color swatch → opens color picker popover
- [ ] HSV wheel allows smooth hue selection
- [ ] SV square allows smooth saturation/brightness selection
- [ ] Hex input validates `#RRGGBB` format
- [ ] RGB and HSL sliders bidirectionally synced with wheel
- [ ] Eyedropper works in Chromium browsers
- [ ] Theme palette swatches shown and clickable
- [ ] Color change instantly updates chart on canvas (60fps)
- [ ] Apply / Cancel / Reset to Default all work

### Code Generation
- [ ] Code preview panel shows valid Python at all times
- [ ] Running generated code produces identical dashboard
- [ ] Custom colors appear as `colors=["#hex", ...]`
- [ ] Layout positions appear as `col` / `colspan` / `height`

### Real-Time Data
- [ ] Charts with `refresh > 0` update without page reload
- [ ] SSE auto-reconnects on disconnect
- [ ] Multiple charts support different refresh intervals
- [ ] DB query errors show non-blocking error state (no crash)

### Performance
- [ ] Initial page load < 2 seconds (excluding data fetch)
- [ ] Canvas drag at 60fps
- [ ] Color picker interactions at 60fps
- [ ] 20-chart dashboard renders without jank
- [ ] SSE updates process in < 50ms per chart

---

## 📄 License

MIT — free for personal and commercial use.

---

<p align="center">
  <strong>◆ ChartCraft</strong><br>
  <em>Python-powered dashboards for everyone.</em>
</p>
