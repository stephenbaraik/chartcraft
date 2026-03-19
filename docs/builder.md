# Visual Dashboard Builder

Navigate to `http://localhost:8050/builder` while your app is running.

---

## Getting Started

1. Run your app: `python app.py`
2. Open `http://localhost:8050/builder` in your browser
3. Drag chart types from the left sidebar onto the canvas
4. Adjust properties in the right panel
5. See live Python code generated in real-time in the bottom panel
6. Click **Save** to persist your design as a project

---

## Interface Overview

```
+------------------------------------------------------------------+
|  TOOLBAR (top bar)                                               |
|  [Undo] [Redo] [Align ▼] [Save] [Export ▼] [Projects ▼]        |
+----------+----------------------------------------+--------------+
|          |                                        |              |
|  CHART   |         CANVAS                         |  PROPERTIES  |
|  LIBRARY |                                        |  PANEL       |
|  (left)  |   Drag-and-drop chart widgets          |  (right)     |
|          |   Live ECharts previews                |              |
|  Bar     |                                        |  [Data]      |
|  Line    |   [Chart A]  [Chart B]                 |  [Style]     |
|  Pie     |                                        |  [Layout]    |
|  ...     |       [Chart C — full width]           |  [Anim]      |
|          |                                        |              |
+----------+----------------------------------------+--------------+
|  CODE PREVIEW (bottom, collapsible)                              |
|  import chartcraft as cc                                         |
|  @app.page("/")                                                  |
|  def home(): ...                                                 |
+------------------------------------------------------------------+
```

---

## Canvas

### Adding Charts

Drag a chart type from the left sidebar onto the canvas. It appears with sample data and a resize handle.

### Moving Charts

Click and drag any chart to reposition it. The canvas snaps to a 12-column grid.

### Resizing Charts

Drag the resize handle (bottom-right corner) to change size. Width snaps to grid columns (1–12). Minimum sizes are enforced per chart type.

### Selecting Multiple Charts

- **Shift + click** each chart, or
- **Click and drag** on empty canvas space to marquee-select

With multiple charts selected, use the toolbar to:
- **Align** — Align Left, Center, Right, Top, Middle, Bottom
- **Distribute** — Space evenly horizontally or vertically
- **Delete** — Remove all selected charts

### Undo / Redo

- **Undo:** `Ctrl+Z` (or the Undo button)
- **Redo:** `Ctrl+Shift+Z` (or the Redo button)

The full history of every drag, resize, color change, and data edit is tracked.

### Z-Order (Layering)

Right-click any chart to access:
- Bring to Front
- Send to Back
- Move Forward
- Move Backward

---

## Chart Library (Left Sidebar)

Draggable chart types organized by category:

| Category | Charts |
|----------|--------|
| **Charts** | Bar, Line, Area, Pie, Donut, Scatter, Bubble, Heatmap, Radar, Waterfall, Funnel, Treemap, Sankey, Gauge, Candlestick, Histogram, Box Plot |
| **KPIs** | KPI Card, Metric |
| **Layout** | Divider, Spacer, Section Header, Text Block |
| **Filters** | Dropdown, Multi-Select, Date Range, Slider, Search |
| **Tables** | Data Table |

---

## Properties Panel (Right Sidebar)

When a chart is selected, the Properties Panel shows five tabs:

### Data Tab

Configure the data source for the selected chart:

- **Connection** — Select a registered SQL connection or "Inline Data"
- **SQL Query** — Write SQL directly; click **Run** to preview results
- **Schema Browser** — Expand tables and columns from the connected database
- **X Axis / Y Axis** — Map query columns to chart axes
- **Refresh Interval** — Set live refresh in seconds (blank = static)

### Style Tab

Visual customization:

- **Color Picker** — Click any color swatch to open the full HSV color picker
- **Palette** — Select one of 16 named palettes for automatic series colors
- **Font** — Choose title and label fonts
- **Border** — Border radius, color, width
- **Opacity** — Chart card opacity

Every color property opens the full [color picker](themes-and-colors.md) with wheel, sliders, palette swatches, color harmonies, and gradient editor.

### Layout Tab

Exact positioning controls:

- **Column** (0–11) and **Span** (1–12) — Grid position
- **Height** — Chart height in pixels
- **Padding** — Internal spacing

### Animation Tab

- **Enable Animation** — Toggle chart entry animations
- **Duration** — Animation time in milliseconds
- **Easing** — Curve type (ease-in, ease-out, bounce, etc.)

### Interaction Tab

- **Tooltip** — Enable/disable hover tooltips
- **Click Action** — What happens when a user clicks a data point
  - `filter` — Update a linked filter
  - `navigate` — Go to another page
- **Click Target** — Filter name or page path

---

## Color Picker

Click any color swatch in the Style tab to open the full-featured color picker:

| Tab | Description |
|-----|-------------|
| **Wheel** | HSV color wheel + saturation/brightness square. Drag cursor to pick any color. |
| **Sliders** | Precise hue, saturation, value, and alpha sliders. |
| **Palettes** | Click any of 16 ChartCraft palette swatches. Recent colors are also shown. |
| **Harmonies** | Auto-generate complementary, triadic, analogous, or split-complementary color sets. |
| **Gradient** | Build multi-stop gradients with an angle control and per-stop opacity. |

At the bottom: **Hex input** (type `#RRGGBB`) · **RGB values** · **HSL values** · **EyeDropper** (sample screen color, Chromium only)

Click **Apply** to confirm · **Cancel** to discard · **Reset** to revert to default

---

## Code Preview (Bottom Panel)

The code panel shows the Python equivalent of your current canvas design in real-time. It updates instantly on every change.

### Edit Code Directly

Click into the code panel to edit Python. The canvas updates to reflect your changes:

1. Edit any parameter (e.g. change `col=0` to `col=4`)
2. Click the **Parse** button (or press `Ctrl+Enter`)
3. The canvas repositions the widget to column 4

Parse errors are highlighted inline and the canvas keeps the last valid state.

### Dirty Badge

A **●** badge appears next to the Parse button when the code has been edited but not yet applied to the canvas.

---

## Saving Projects

### Save

Click **Save** in the toolbar (or `Ctrl+S`) to open the Save Dialog:
- **Project Name** — Enter a name
- **Save** — Writes to the browser's project store (SQLite)

Projects are listed in the **Projects** dropdown.

### Load

Open the **Projects** dropdown → click a project name to load it. The canvas and code update immediately.

### Delete

In the Projects dropdown, each project has a delete (×) button.

---

## Exporting

The **Export** dropdown has three options:

### Python (.py)

Downloads the current canvas state as a standalone Python file. Run it directly:

```bash
python my_dashboard.py
# → http://localhost:8050
```

### Jupyter Notebook (.ipynb)

Downloads a notebook with install, code, and run cells. Open in Jupyter:

```bash
jupyter notebook my_dashboard.ipynb
```

### Docker Project (.zip)

Downloads a complete Docker-ready project containing:
- `app.py` — dashboard code
- `Dockerfile` — Python 3.12-slim based
- `docker-compose.yml` — single-service compose file
- `README.md` — deployment instructions

Deploy anywhere:

```bash
unzip my_dashboard_docker.zip
cd my_dashboard
docker-compose up
# → http://localhost:8050
```

---

## Bidirectional Sync

The builder and code panel stay in sync:

| Action | Result |
|--------|--------|
| Drag a chart to a new position | `col` and `colspan` update in code |
| Change a color in the picker | `colors=[...]` updates in code |
| Set refresh interval | `refresh=N` appears in code |
| Edit `title=` in code panel | Chart title updates on canvas |
| Edit `col=` in code panel | Chart moves to new grid position |
| Paste in a completely new block | Canvas rebuilds from scratch |

The generated Python code is always valid and runnable — copy it and run `python app.py` to get an identical dashboard.

---

## Keyboard Shortcuts

| Shortcut | Action |
|----------|--------|
| `Ctrl+Z` | Undo |
| `Ctrl+Shift+Z` | Redo |
| `Ctrl+S` | Save project |
| `Ctrl+Enter` | Parse code panel |
| `Delete` | Delete selected widget(s) |
| `Shift+Click` | Add to selection |
| `Escape` | Deselect all |

---

## Tips

- **Start from code:** paste existing Python into the code panel and click Parse
- **Iterate fast:** change in builder, export to Python, modify, paste back
- **Schema browser:** connect a real DB in the Data tab to see actual table and column names
- **Color harmonies:** use the Harmonies tab in the color picker to auto-generate coherent sets for multi-series charts
