# ChartCraft v1 - Simplified Dashboard Library

A minimalist, pandas-like approach to creating interactive dashboards with full customization.

## Philosophy

- **Simple API**: Like pandas, intuitive and consistent
- **No presets**: Full control over every aspect
- **Easy customization**: Modify anything, no limits
- **Minimal structure**: Fewer files, clearer purpose
- **Pandas-like syntax**: Familiar data handling patterns

## File Structure

```
chartcraft/
├── __init__.py              # Public API
├── data.py                  # Data handling (pandas-like)
├── charts.py                # Chart creation functions
├── dashboard.py             # Dashboard class
├── render.py                # HTML rendering
└── themes.py                # Customization system
```

## Core Modules

### 1. data.py - Pandas-like Data Handling
```python
# Import
import chartcraft as cc

# Simple data structures (like pandas Series/DataFrame)
cc.Data({"x": [1, 2, 3], "y": [10, 20, 30]})
cc.Series([1, 2, 3], name="values")
cc.DataFrame({"col1": [1, 2], "col2": [3, 4]})

# Easy transformations
cc.Data({"x": [1, 2, 3], "y": [10, 20, 30]}).rename(columns={"x": "time"})
cc.Data({"x": [1, 2, 3], "y": [10, 20, 30]}).filter(x=lambda val: val > 1)
```

### 2. charts.py - Simple Chart Creation
```python
# Basic charts (no presets)
cc.bar(data, title="My Chart")
cc.line(data, title="Line Chart")
cc.scatter(data, title="Scatter Plot")
cc.pie(data, title="Pie Chart")
cc.histogram(data, title="Histogram")

# Customization (everything is customizable)
cc.bar(
    data,
    title="My Chart",
    x="category",
    y="value",
    color="#FF6B6B",
    width=800,
    height=400,
    grid=True,
    legend=True,
    tooltip=True
)
```

### 3. dashboard.py - Dashboard Class
```python
# Simple dashboard creation
cc.Dashboard(
    title="My Dashboard",
    charts=[
        cc.bar(data1, title="Chart 1"),
        cc.line(data2, title="Chart 2"),
    ],
    layout="grid",  # "grid", "vertical", "horizontal"
    columns=2,
    spacing=20
)
```

### 4. render.py - HTML Rendering
```python
# Simple rendering
html = cc.render(dashboard)
cc.save(dashboard, "my_dashboard.html")
cc.serve(dashboard, port=8050)  # Start local server
```

### 5. themes.py - Customization System
```python
# Full customization (no presets)
cc.theme(
    background="#ffffff",
    font_family="Arial, sans-serif",
    font_size=12,
    colors=["#FF6B6B", "#4ECDC4", "#45B7D1"],
    grid=True,
    grid_color="#e0e0e0",
    grid_width=1,
    legend=True,
    tooltip=True,
    animation=True
)
```

## API Examples

### Basic Usage
```python
import chartcraft as cc

# Create simple data
data = cc.Data({
    "category": ["A", "B", "C"],
    "value": [10, 20, 30]
})

# Create charts
bar_chart = cc.bar(data, title="Simple Bar Chart")
line_chart = cc.line(data, title="Simple Line Chart")

# Create dashboard
dashboard = cc.Dashboard(
    title="My Dashboard",
    charts=[bar_chart, line_chart]
)

# Render or serve
cc.render(dashboard)
# or
cc.serve(dashboard)
```

### Advanced Customization
```python
# Full control over every aspect
cc.theme(
    # Visual styling
    background="#1a1a1a",
    font_family="monospace",
    font_size=14,
    colors=["#00ff00", "#ff0000", "#0000ff"],
    
    # Chart-specific settings
    bar_width=0.8,
    line_smooth=True,
    pie_donut=False,
    
    # Display settings
    grid=True,
    grid_color="#333333",
    legend=True,
    tooltip=True,
    animation=True,
    
    # Interaction
    zoom=True,
    pan=True,
    select=True
)

# Create charts with custom styling
cc.bar(
    data,
    title="Custom Chart",
    color="#00ff00",  # Single color or palette
    width=1000,
    height=500,
    border=True,
    border_color="#ffffff",
    border_width=2
)
```

### Pandas-like Operations
```python
# Data manipulation (pandas-like)
data = cc.Data({
    "x": [1, 2, 3, 4, 5],
    "y": [10, 20, 15, 25, 30],
    "category": ["A", "B", "A", "B", "A"]
})

# Filter and transform
filtered = data.filter(y=lambda val: val > 15)
renamed = data.rename(columns={"x": "time", "y": "value"})
sorted = data.sort_values("value", ascending=False)

# Create charts from transformed data
cc.line(renamed, title="Transformed Data")
```

## Key Differences from Original ChartCraft

| Feature | Original ChartCraft | Simplified ChartCraft v1 |
|---------|-------------------|--------------------------|
| **API Size** | 50+ exported functions | 10-15 core functions |
| **Presets** | 11 built-in themes | No presets, full customization |
| **File Structure** | 5 directories | 1 flat structure |
| **Complexity** | High | Minimal |
| **Customization** | Limited | Complete |
| **Learning Curve** | Steep | Gentle (pandas-like) |

## Installation

```bash
pip install chartcraft
```

## Quick Start

```python
import chartcraft as cc

# Create data
data = cc.Data({
    "month": ["Jan", "Feb", "Mar", "Apr"],
    "sales": [100, 150, 200, 180],
    "profit": [20, 35, 50, 40]
})

# Create charts
cc.bar(data, title="Sales", x="month", y="sales")
cc.line(data, title="Profit", x="month", y="profit")

# Create dashboard
dashboard = cc.Dashboard(
    title="Business Metrics",
    charts=[
        cc.bar(data, title="Sales", x="month", y="sales"),
        cc.line(data, title="Profit", x="month", y="profit")
    ]
)

# Serve locally
cc.serve(dashboard)
```

## Design Goals

1. **Simplicity**: Easy to learn and use
2. **Flexibility**: Full customization
3. **Consistency**: Pandas-like patterns
4. **Performance**: Minimal overhead
5. **Extensibility**: Easy to add new features

This simplified version removes all presets, complex configurations, and unnecessary complexity while maintaining full customization capabilities.