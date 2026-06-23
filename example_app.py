"""
Example Application for ChartCraft v1

This file demonstrates the new simplified ChartCraft v1 API with:
- Pandas-like data handling
- Simple, intuitive chart creation
- Stunning visuals (better than Power BI/Tableau)
- Full customization capabilities
- Real-world usage examples

ChartCraft v1 is a minimalist, pandas-like approach to creating
interactive dashboards with full customization and no presets.
"""

import chartcraft as cc

# Example 1: Basic Pandas-like Data Handling
print("=== Example 1: Pandas-like Data Handling ===")

# Create data like pandas DataFrame
data = cc.Data({
    "month": ["Jan", "Feb", "Mar", "Apr", "May", "Jun"],
    "sales": [100, 150, 200, 180, 220, 250],
    "profit": [20, 35, 50, 40, 60, 70],
    "expenses": [80, 115, 150, 140, 160, 180]
})

# Pandas-like operations
print(f"Original data: {data}")
print(f"Data shape: {len(data.columns)} columns x {len(data.data['month'])} rows")

# Filter data
profitable_data = data.filter(profit=lambda val: val > 40)
print(f"\nFiltered data (profit > 40): {profitable_data}")

# Sort data
sorted_data = data.sort_values("sales", ascending=False)
print(f"\nSorted by sales: {sorted_data.head()}")

# Get basic statistics
stats = data.describe()
print(f"\nBasic statistics:\n{stats}")

# Example 2: Simple Chart Creation
print("\n\n=== Example 2: Simple Chart Creation ===")

# Create charts with stunning visuals
bar_chart = cc.bar(
    data,
    title="Monthly Sales Performance",
    x="month",
    y="sales",
    color="linear-gradient(135deg, #667eea 0%, #764ba2 100%)",
    width=800,
    height=400,
    bar_border_radius=8,
    bar_shadow="0 4px 12px rgba(0, 0, 0, 0.15)"
)

line_chart = cc.line(
    data,
    title="Profit Trend",
    x="month",
    y="profit",
    color="#3498db",
    line_smooth=True,
    line_width=3,
    show_dots=True,
    dot_size=6
)

area_chart = cc.area(
    data,
    title="Expenses Overview",
    x="month",
    y="expenses",
    color="linear-gradient(135deg, #e74c3c 0%, #f39c12 100%)",
    opacity=0.7,
    smooth=True
)

pie_chart = cc.pie(
    data,
    title="Quarterly Distribution",
    colors=["#e74c3c", "#3498db", "#2ecc71", "#f39c12", "#9b59b6"],
    donut=True,
    inner_radius="60%",
    label_show=True,
    label_position="outside"
)

print(f"Created {len([bar_chart, line_chart, area_chart, pie_chart])} charts with stunning visuals")

# Example 3: Dashboard Creation
print("\n\n=== Example 3: Dashboard Creation ===")

dashboard = cc.Dashboard(
    title="Business Analytics Dashboard",
    charts=[bar_chart, line_chart, area_chart, pie_chart],
    layout="grid",
    columns=2,
    spacing=20
)

print(f"Created dashboard: {dashboard}")
print(f"Dashboard contains {len(dashboard.charts)} charts")

# Example 4: Enhanced Customization
print("\n\n=== Example 4: Enhanced Customization ===")

# Apply stunning theme
cc.theme(
    background="#1a1a1a",
    header_background="linear-gradient(135deg, #2c3e50 0%, #34495e 100%)",
    card_background="#2d2d2d",
    title_color="#ecf0f1",
    text_color="#bdc3c7",
    grid_color="#34495e",
    legend_background="rgba(44, 62, 80, 0.9)",
    legend_border_color="#3498db",
    tooltip_background="rgba(0, 0, 0, 0.9)",
    tooltip_border_color="#3498db",
    font_family="'Inter', sans-serif",
    font_size=14,
    animation=True,
    animation_duration=800
)

# Create charts with custom styling
custom_bar = cc.bar(
    data,
    title="Custom Styled Bar Chart",
    x="month",
    y="sales",
    color="#00ff00",
    width=900,
    height=500,
    bar_border_radius=12,
    bar_shadow="0 8px 24px rgba(0, 0, 0, 0.3)",
    grid=True,
    grid_color="#34495e",
    legend=True,
    legend_position="top",
    legend_background="rgba(44, 62, 80, 0.95)",
    tooltip=True,
    tooltip_background="rgba(0, 0, 0, 0.95)",
    tooltip_border_color="#00ff00",
    tooltip_border_width=2
)

# Example 5: Advanced Data Manipulation
print("\n\n=== Example 5: Advanced Data Manipulation ===")

# Create more complex data
complex_data = cc.Data({
    "product": ["A", "B", "C", "D", "E", "F", "G", "H"],
    "q1_sales": [100, 150, 200, 120, 180, 90, 160, 140],
    "q2_sales": [120, 180, 220, 150, 200, 110, 190, 170],
    "q3_sales": [140, 200, 240, 180, 220, 130, 210, 190],
    "q4_sales": [160, 220, 260, 200, 240, 150, 230, 210]
})

# Create time series data
time_series_data = cc.Data({
    "date": ["2024-01-01", "2024-01-02", "2024-01-03", "2024-01-04", "2024-01-05"],
    "temperature": [20, 22, 25, 23, 26],
    "humidity": [60, 65, 70, 68, 72],
    "pressure": [1013, 1015, 1012, 1014, 1016]
})

# Create charts from complex data
quarterly_chart = cc.bar(
    complex_data,
    title="Quarterly Sales by Product",
    x="product",
    y="q4_sales",
    colors=["#e74c3c", "#3498db", "#2ecc71", "#f39c12", "#9b59b6", "#1abc9c", "#34495e", "#95a5a6"],
    bar_border_radius=6,
    grid=True,
    legend=True,
    legend_position="top",
    animation=True
)

time_series_chart = cc.line(
    time_series_data,
    title="Weather Monitoring",
    x="date",
    y=["temperature", "humidity"],
    line_smooth=True,
    show_dots=True,
    dot_size=8,
    legend=True,
    legend_position="top",
    grid=True,
    grid_color="#e8f0f8",
    animation=True
)

# Example 6: Visual Builder Pattern
print("\n\n=== Example 6: Visual Builder Pattern ===")

# Using the visual builder pattern
cc.set_title("Advanced Analytics Dashboard")
cc.set_layout("grid", columns=2, spacing=25)

# Add charts using visual builder
cc.add_bar(data, title="Sales Overview", x="month", y="sales")
cc.add_line(data, title="Profit Trend", x="month", y="profit")
cc.add_pie(data, title="Distribution", colors=["#e74c3c", "#3498db", "#2ecc71"])
cc.add_scatter(time_series_data, title="Weather Correlation", x="temperature", y="humidity")

# Build dashboard from visual builder
dashboard2 = cc.build_dashboard()
print(f"Created dashboard from visual builder: {dashboard2}")

# Example 7: Export and Serve
print("\n\n=== Example 7: Export and Serve ===")

# Export to HTML
cc.save(dashboard, "business_dashboard.html")
print("✓ Exported dashboard to 'business_dashboard.html'")

# Export all dashboards
cc.save_all(dashboard2, "dashboards/")
print("✓ Exported all dashboards to 'dashboards/' directory")

# Serve locally (uncomment to run)
# cc.serve(dashboard, port=8050)
# print("✓ Dashboard served at http://localhost:8050")

# Example 8: Theme Management
print("\n\n=== Example 8: Theme Management ===")

# Apply different themes
cc.apply_dark_theme()
print("✓ Applied dark theme")

cc.apply_light_theme()
print("✓ Applied light theme")

cc.apply_vibrant_theme()
print("✓ Applied vibrant theme")

# Get current theme
theme = cc.get_theme()
print(f"✓ Current theme has {len(theme)} properties")

# Example 9: Data Export/Import
print("\n\n=== Example 9: Data Export/Import ===")

# Export theme
theme_data = cc.export_theme()
print(f"✓ Exported theme with {len(theme_data)} sections")

# Import theme (example)
# cc.import_theme(theme_data)

print("\n\n=== Summary ===")
print("ChartCraft v1 provides:")
print("✓ Pandas-like data handling")
print("✓ Simple, intuitive chart creation")
print("✓ Stunning visuals (better than Power BI/Tableau)")
print("✓ Full customization capabilities")
print("✓ Visual builder pattern")
print("✓ Export/import functionality")
print("✓ Theme management")
print("✓ Real-time serving")
print("\nAll examples demonstrate the simplified, powerful API of ChartCraft v1!")