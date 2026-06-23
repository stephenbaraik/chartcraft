"""
Customization framework for ChartCraft v1.

Full customization system with no presets.
Every aspect of charts and dashboards can be customized.
"""

from typing import Dict, Any, List
class CustomizationSystem:
    """
    Complete customization system for ChartCraft v1.
    
    This system provides full control over every aspect of charts
    and dashboards without any presets.
    """
    
    def __init__(self):
        # Default customization (minimal - no presets)
        self.theme = {
            # Visual styling
            'background': '#ffffff',
            'header_background': '#f8f9fa',
            'card_background': '#ffffff',
            'title_color': '#333333',
            'text_color': '#666666',
            
            # Chart-specific styling
            'bar_color': '#4ECDC4',
            'line_color': '#45B7D1',
            'pie_colors': ['#FF6B6B', '#4ECDC4', '#45B7D1', '#96CEB4', '#FFEAA7'],
            'grid': True,
            'grid_color': '#e0e0e0',
            'grid_width': 1,
            
            # Display settings
            'legend': True,
            'legend_position': 'bottom',
            'tooltip': True,
            'animation': True,
            
            # Interaction
            'zoom': True,
            'pan': True,
            'select': True,
            
            # Font settings
            'font_family': 'Arial, sans-serif',
            'font_size': 12,
            'font_weight': 'normal'
        }
        
        # Chart customization
        self.chart_defaults = {
            'bar': {
                'width': 0.8,
                'color': None,
                'border': False,
                'border_color': '#333333',
                'border_width': 1
            },
            'line': {
                'smooth': False,
                'show_dots': True,
                'dot_size': 3,
                'line_width': 2
            },
            'area': {
                'opacity': 0.7,
                'smooth': False
            },
            'pie': {
                'donut': False,
                'inner_radius': '0%',
                'outer_radius': '100%',
                'start_angle': 0,
                'min_angle': 0
            },
            'scatter': {
                'symbol_size': 20,
                'symbol_type': 'circle'
            },
            'histogram': {
                'bin_count': 10,
                'show_frequency': True,
                'show_cumulative': False
            },
            'heatmap': {
                'color_scheme': 'viridis',
                'show_values': True
            },
            'radar': {
                'shape': 'polygon',
                'axis_name': True
            },
            'waterfall': {
                'show_axis': True,
                'connecter_color': '#666666'
            },
            'gauge': {
                'start_angle': 180,
                'end_angle': 0,
                'min': 0,
                'max': 100,
                'axis': True
            },
            'candlestick': {
                'up_color': '#00ff00',
                'down_color': '#ff0000',
                'show_ma': False
            },
            'table': {
                'striped': True,
                'border': True,
                'pagination': False,
                'page_size': 10
            },
            'metric': {
                'threshold': None,
                'threshold_color': '#ff0000',
                'show_trend': True
            },
            'sankey': {
                'node_width': 20,
                'node_gap': 5,
                'link_width': 1
            },
            'treemap': {
                'width': '100%',
                'height': '100%',
                'level': 0
            },
            'funnel': {
                'x': 'center',
                'y': 'center',
                'width': '80%',
                'height': '80%'
            }
        }
        
        # Dashboard customization
        self.dashboard_defaults = {
            'layout': 'grid',
            'columns': 2,
            'spacing': 20,
            'padding': 20,
            'background_color': '#ffffff',
            'border_radius': 8,
            'shadow': True,
            'max_width': 1200,
            'responsive': True
        }
    
    def set_theme(self, **kwargs):
        """
        Set theme options (no presets - full customization).
        
        Args:
            **kwargs: Theme options to set
            
        Examples:
            # Custom colors
            theme.set_theme(
                background='#1a1a1a',
                title_color='#ffffff',
                bar_color='#00ff00'
            )
            
            # Chart-specific settings
            theme.set_theme(
                grid=True,
                grid_color='#333333',
                legend=True,
                tooltip=True,
                animation=False
            )
        """
        self.theme.update(kwargs)
        return self
    
    def reset_theme(self):
        """Reset theme to defaults (no presets)."""
        self.theme = {
            'background': '#ffffff',
            'header_background': '#f8f9fa',
            'card_background': '#ffffff',
            'title_color': '#333333',
            'text_color': '#666666',
            'bar_color': '#4ECDC4',
            'line_color': '#45B7D1',
            'pie_colors': ['#FF6B6B', '#4ECDC4', '#45B7D1', '#96CEB4', '#FFEAA7'],
            'grid': True,
            'grid_color': '#e0e0e0',
            'grid_width': 1,
            'legend': True,
            'legend_position': 'bottom',
            'tooltip': True,
            'animation': True,
            'zoom': True,
            'pan': True,
            'select': True,
            'font_family': 'Arial, sans-serif',
            'font_size': 12,
            'font_weight': 'normal'
        }
        return self
    
    def set_chart_defaults(self, chart_type: str, **kwargs):
        """
        Set defaults for a specific chart type.
        
        Args:
            chart_type: Type of chart ("bar", "line", "area", etc.)
            **kwargs: Chart type defaults
            
        Examples:
            # Custom bar chart defaults
            theme.set_chart_defaults('bar', 
                width=0.9,
                color='#ff0000',
                border=True
            )
            
            # Custom line chart defaults
            theme.set_chart_defaults('line',
                smooth=True,
                show_dots=False,
                line_width=3
            )
        """
        if chart_type in self.chart_defaults:
            self.chart_defaults[chart_type].update(kwargs)
        else:
            raise ValueError(f"Unknown chart type: {chart_type}")
        return self
    
    def set_dashboard_defaults(self, **kwargs):
        """
        Set dashboard defaults.
        
        Args:
            **kwargs: Dashboard defaults
            
        Examples:
            # Custom dashboard defaults
            theme.set_dashboard_defaults(
                layout='vertical',
                columns=1,
                spacing=30,
                padding=30
            )
        """
        self.dashboard_defaults.update(kwargs)
        return self
    
    def apply_theme(self, theme_name: str):
        """
        Apply a named theme (convenience function).
        
        Args:
            theme_name: Name of theme to apply
            
        Examples:
            # Apply dark theme
            theme.apply_theme('dark')
            
            # Apply light theme
            theme.apply_theme('light')
            
            # Apply vibrant theme
            theme.apply_theme('vibrant')
        """
        themes = {
            'dark': {
                'background': '#1a1a1a',
                'header_background': '#2d2d2d',
                'card_background': '#2d2d2d',
                'title_color': '#ffffff',
                'text_color': '#cccccc',
                'grid_color': '#444444',
                'bar_color': '#00ff00'
            },
            'light': {
                'background': '#ffffff',
                'header_background': '#f8f9fa',
                'card_background': '#ffffff',
                'title_color': '#333333',
                'text_color': '#666666',
                'grid_color': '#e0e0e0',
                'bar_color': '#4ECDC4'
            },
            'vibrant': {
                'background': '#2c3e50',
                'header_background': '#34495e',
                'card_background': '#34495e',
                'title_color': '#ecf0f1',
                'text_color': '#bdc3c7',
                'grid_color': '#7f8c8d',
                'bar_color': '#e74c3c',
                'animation': True
            }
        }
        
        if theme_name in themes:
            self.theme.update(themes[theme_name])
        else:
            raise ValueError(f"Unknown theme: {theme_name}")
        return self
    
    def get_theme(self) -> Dict[str, Any]:
        """Get current theme."""
        return self.theme.copy()
    
    def get_chart_defaults(self, chart_type: str = None) -> Dict[str, Any]:
        """
        Get chart defaults.
        
        Args:
            chart_type: Specific chart type, or None for all defaults
            
        Returns:
            Chart defaults dictionary
        """
        if chart_type:
            return self.chart_defaults.get(chart_type, {})
        return self.chart_defaults.copy()
    
    def get_dashboard_defaults(self) -> Dict[str, Any]:
        """Get dashboard defaults."""
        return self.dashboard_defaults.copy()
    
    def export_theme(self) -> Dict[str, Any]:
        """Export current theme."""
        return {
            'theme': self.theme,
            'chart_defaults': self.chart_defaults,
            'dashboard_defaults': self.dashboard_defaults
        }
    
    def import_theme(self, theme_data: Dict[str, Any]):
        """
        Import theme from dictionary.
        
        Args:
            theme_data: Theme data dictionary
        """
        if 'theme' in theme_data:
            self.theme.update(theme_data['theme'])
        if 'chart_defaults' in theme_data:
            self.chart_defaults.update(theme_data['chart_defaults'])
        if 'dashboard_defaults' in theme_data:
            self.dashboard_defaults.update(theme_data['dashboard_defaults'])
        return self
# Global customization system
_customization = CustomizationSystem()
def theme(**kwargs):
    """
    Set theme options (no presets - full customization).
    
    Args:
        **kwargs: Theme options to set
        
    Examples:
        # Custom colors
        theme(
            background='#1a1a1a',
            title_color='#ffffff',
            bar_color='#00ff00'
        )
        
        # Chart-specific settings
        theme(
            grid=True,
            grid_color='#333333',
            legend=True,
            tooltip=True,
            animation=False
        )
    """
    _customization.set_theme(**kwargs)
def reset_theme():
    """Reset theme to defaults (no presets)."""
    _customization.reset_theme()
def set_theme(theme_name: str):
    """
    Apply a named theme (convenience function).
    
    Args:
        theme_name: Name of theme to apply
        
    Examples:
        # Apply dark theme
        set_theme('dark')
        
        # Apply light theme
        set_theme('light')
        
        # Apply vibrant theme
        set_theme('vibrant')
    """
    _customization.apply_theme(theme_name)
def set_chart_defaults(chart_type: str, **kwargs):
    """
    Set defaults for a specific chart type.
    
    Args:
        chart_type: Type of chart ("bar", "line", "area", etc.)
        **kwargs: Chart type defaults
        
    Examples:
        # Custom bar chart defaults
        set_chart_defaults('bar', 
            width=0.9,
            color='#ff0000',
            border=True
        )
    """
    _customization.set_chart_defaults(chart_type, **kwargs)
def set_dashboard_defaults(**kwargs):
    """
    Set dashboard defaults.
    
    Args:
        **kwargs: Dashboard defaults
        
    Examples:
        # Custom dashboard defaults
        set_dashboard_defaults(
            layout='vertical',
            columns=1,
            spacing=30,
            padding=30
        )
    """
    _customization.set_dashboard_defaults(**kwargs)
def get_theme() -> Dict[str, Any]:
    """Get current theme."""
    return _customization.get_theme()
def get_chart_defaults(chart_type: str = None) -> Dict[str, Any]:
    """
    Get chart defaults.
    
    Args:
        chart_type: Specific chart type, or None for all defaults
        
    Returns:
        Chart defaults dictionary
    """
    return _customization.get_chart_defaults(chart_type)
def get_dashboard_defaults() -> Dict[str, Any]:
    """Get dashboard defaults."""
    return _customization.get_dashboard_defaults()
def export_theme() -> Dict[str, Any]:
    """Export current theme."""
    return _customization.export_theme()
def import_theme(theme_data: Dict[str, Any]):
    """
    Import theme from dictionary.
    
    Args:
        theme_data: Theme data dictionary
    """
    _customization.import_theme(theme_data)
# Convenience functions for common customizations
def apply_dark_theme():
    """Apply dark theme (convenience function)."""
    _customization.apply_theme('dark')

def apply_light_theme():
    """Apply light theme (convenience function)."""
    _customization.apply_theme('light')

def apply_vibrant_theme():
    """Apply vibrant theme (convenience function)."""
    _customization.apply_theme('vibrant')

# List available themes (for information)
def list_themes() -> List[str]:
    """List available theme names."""
    return ['dark', 'light', 'vibrant']