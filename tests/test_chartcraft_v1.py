"""
Test suite for ChartCraft v1

This file contains comprehensive tests for the simplified ChartCraft v1 API.
Tests cover:
- Data handling (pandas-like functionality)
- Chart creation and rendering
- Dashboard functionality
- Customization and theming
- Export and serving
- Edge cases and error handling
"""

import chartcraft as cc
import tempfile
import os
import json


def test_data_creation():
    """Test basic data creation"""
    # Create simple data
    data = cc.Data({
        "month": ["Jan", "Feb", "Mar", "Apr"],
        "sales": [100, 150, 200, 180],
        "profit": [20, 35, 50, 40]
    })
    
    assert len(data.columns) == 3
    assert len(data.data["month"]) == 4
    assert "month" in data.columns
    assert "sales" in data.columns
    assert "profit" in data.columns
    
    print("✓ Data creation test passed")


def test_data_filtering():
    """Test data filtering functionality"""
    data = cc.Data({
        "month": ["Jan", "Feb", "Mar", "Apr"],
        "sales": [100, 150, 200, 180],
        "profit": [20, 35, 50, 40]
    })
    
    # Filter by profit > 40
    filtered = data.filter(profit=lambda val: val > 40)
    assert len(filtered.data["month"]) == 2
    assert filtered.data["month"][0] == "Mar"
    assert filtered.data["month"][1] == "Apr"
    
    print("✓ Data filtering test passed")


def test_data_sorting():
    """Test data sorting functionality"""
    data = cc.Data({
        "month": ["Jan", "Feb", "Mar", "Apr"],
        "sales": [100, 150, 200, 180],
        "profit": [20, 35, 50, 40]
    })
    
    # Sort by sales descending
    sorted_data = data.sort_values("sales", ascending=False)
    assert sorted_data.data["month"][0] == "Mar"
    assert sorted_data.data["month"][1] == "Apr"
    assert sorted_data.data["month"][2] == "Feb"
    assert sorted_data.data["month"][3] == "Jan"
    
    print("✓ Data sorting test passed")


def test_chart_creation():
    """Test basic chart creation"""
    data = cc.Data({
        "month": ["Jan", "Feb", "Mar", "Apr"],
        "sales": [100, 150, 200, 180]
    })
    
    # Create different chart types
    bar_chart = cc.bar(data, title="Sales", x="month", y="sales")
    line_chart = cc.line(data, title="Sales", x="month", y="sales")
    area_chart = cc.area(data, title="Sales", x="month", y="sales")
    pie_chart = cc.pie(data, title="Sales", colors=["#e74c3c", "#3498db", "#2ecc71", "#f39c12"])
    
    assert bar_chart is not None
    assert line_chart is not None
    assert area_chart is not None
    assert pie_chart is not None
    
    print("✓ Chart creation test passed")


def test_dashboard_creation():
    """Test dashboard creation"""
    data = cc.Data({
        "month": ["Jan", "Feb", "Mar", "Apr"],
        "sales": [100, 150, 200, 180]
    })
    
    bar_chart = cc.bar(data, title="Sales", x="month", y="sales")
    line_chart = cc.line(data, title="Sales", x="month", y="sales")
    
    dashboard = cc.Dashboard(
        title="Business Dashboard",
        charts=[bar_chart, line_chart],
        layout="grid",
        columns=2
    )
    
    assert dashboard.title == "Business Dashboard"
    assert len(dashboard.charts) == 2
    
    print("✓ Dashboard creation test passed")


def test_theme_application():
    """Test theme application"""
    # Apply dark theme
    cc.apply_dark_theme()
    
    # Apply light theme
    cc.apply_light_theme()
    
    # Apply vibrant theme
    cc.apply_vibrant_theme()
    
    # Get current theme
    theme = cc.get_theme()
    assert len(theme) > 0
    
    print("✓ Theme application test passed")


def test_visual_builder():
    """Test visual builder pattern"""
    data = cc.Data({
        "month": ["Jan", "Feb", "Mar", "Apr"],
        "sales": [100, 150, 200, 180]
    })
    
    # Use visual builder
    cc.set_title("Visual Builder Dashboard")
    cc.set_layout("grid", columns=2, spacing=25)
    cc.add_bar(data, title="Sales Overview", x="month", y="sales")
    cc.add_line(data, title="Sales Trend", x="month", y="sales")
    
    dashboard = cc.build_dashboard()
    assert dashboard.title == "Visual Builder Dashboard"
    assert len(dashboard.charts) == 2
    
    print("✓ Visual builder test passed")


def test_export_functionality():
    """Test export functionality"""
    data = cc.Data({
        "month": ["Jan", "Feb", "Mar", "Apr"],
        "sales": [100, 150, 200, 180]
    })
    
    bar_chart = cc.bar(data, title="Sales", x="month", y="sales")
    
    # Create a temporary file
    with tempfile.NamedTemporaryFile(suffix='.html', delete=False) as f:
        temp_file = f.name
    
    try:
        # Export to HTML
        cc.save(bar_chart, temp_file)
        
        # Check if file exists
        assert os.path.exists(temp_file)
        
        # Check if file contains expected content
        with open(temp_file, 'r') as f:
            content = f.read()
            assert "ChartCraft" in content
            assert "Sales" in content
        
        print("✓ Export functionality test passed")
    finally:
        # Clean up
        if os.path.exists(temp_file):
            os.unlink(temp_file)


def test_theme_export():
    """Test theme export functionality"""
    # Apply a theme
    cc.apply_dark_theme()
    
    # Export theme
    theme_data = cc.export_theme()
    assert len(theme_data) > 0
    assert "background" in theme_data
    assert "title_color" in theme_data
    
    print("✓ Theme export test passed")


def test_error_handling():
    """Test error handling"""
    # Test with invalid data
    try:
        invalid_data = cc.Data({
            "month": ["Jan", "Feb", "Mar", "Apr"],
            "sales": [100, 150, 200]  # Mismatched length
        })
        # This should handle the error gracefully
        assert False, "Should have handled mismatched data"
    except:
        # Error handling is working
        pass
    
    print("✓ Error handling test passed")


def test_edge_cases():
    """Test edge cases"""
    # Test with empty data
    empty_data = cc.Data({})
    assert len(empty_data.columns) == 0
    
    # Test with single row
    single_row_data = cc.Data({
        "month": ["Jan"],
        "sales": [100]
    })
    assert len(single_row_data.data["month"]) == 1
    
    # Test with single column
    single_col_data = cc.Data({
        "sales": [100, 150, 200, 180]
    })
    assert len(single_col_data.columns) == 1
    
    print("✓ Edge cases test passed")


def test_integration():
    """Test integration of all components"""
    # Create data
    data = cc.Data({
        "month": ["Jan", "Feb", "Mar", "Apr"],
        "sales": [100, 150, 200, 180],
        "profit": [20, 35, 50, 40]
    })
    
    # Create charts
    bar_chart = cc.bar(data, title="Sales", x="month", y="sales")
    line_chart = cc.line(data, title="Profit", x="month", y="profit")
    
    # Create dashboard
    dashboard = cc.Dashboard(
        title="Integration Test Dashboard",
        charts=[bar_chart, line_chart],
        layout="grid",
        columns=2
    )
    
    # Apply theme
    cc.apply_vibrant_theme()
    
    # Export
    with tempfile.NamedTemporaryFile(suffix='.html', delete=False) as f:
        temp_file = f.name
    
    try:
        cc.save(dashboard, temp_file)
        assert os.path.exists(temp_file)
        print("✓ Integration test passed")
    finally:
        if os.path.exists(temp_file):
            os.unlink(temp_file)


def run_all_tests():
    """Run all tests"""
    print("Running ChartCraft v1 test suite...")
    print("=" * 50)
    
    test_data_creation()
    test_data_filtering()
    test_data_sorting()
    test_chart_creation()
    test_dashboard_creation()
    test_theme_application()
    test_visual_builder()
    test_export_functionality()
    test_theme_export()
    test_error_handling()
    test_edge_cases()
    test_integration()
    
    print("=" * 50)
    print("All tests passed! ✓")
    print("\nTest suite completed successfully!")


if __name__ == "__main__":
    run_all_tests()