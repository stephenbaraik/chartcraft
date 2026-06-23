"""
HTML rendering for ChartCraft v1.

Simple rendering functions for creating HTML output.
"""

from typing import Dict, Any
import json
import webbrowser
import time
from http.server import HTTPServer, BaseHTTPRequestHandler
from threading import Thread
class SimpleHTTPRequestHandler(BaseHTTPRequestHandler):
    """Simple HTTP request handler for serving dashboards."""
    
    def __init__(self, *args, dashboard_spec: Dict[str, Any] = None, **kwargs):
        self.dashboard_spec = dashboard_spec
        super().__init__(*args, **kwargs)
    
    def do_GET(self):
        """Handle GET requests."""
        if self.path == "/":
            self.send_response(200)
            self.send_header("Content-Type", "text/html; charset=utf-8")
            self.end_headers()
            
            html = self.generate_html()
            self.wfile.write(html.encode())
        elif self.path == "/api/dashboard":
            self.send_response(200)
            self.send_header("Content-Type", "application/json")
            self.end_headers()
            
            self.wfile.write(json.dumps(self.dashboard_spec).encode())
        else:
            self.send_response(404)
            self.end_headers()
    
    def generate_html(self) -> str:
        """Generate HTML for the dashboard."""
        return f"""
<!DOCTYPE html>
<html>
<head>
    <title>{self.dashboard_spec.get('title', 'ChartCraft Dashboard')}</title>
    <style>
        body {{
            font-family: Arial, sans-serif;
            margin: 0;
            padding: 20px;
            background-color: {self.get_theme_color('background')};
            color: #333;
        }}
        .dashboard {{
            max-width: 1200px;
            margin: 0 auto;
        }}
        .header {{
            text-align: center;
            margin-bottom: 30px;
            padding: 20px;
            background-color: {self.get_theme_color('header_background')};
            border-radius: 8px;
        }}
        .charts-container {{
            display: grid;
            grid-template-columns: repeat({self.dashboard_spec.get('columns', 2)}, 1fr);
            gap: {self.dashboard_spec.get('spacing', 20)}px;
        }}
        .chart-card {{
            background-color: {self.get_theme_color('card_background')};
            border-radius: 8px;
            padding: 20px;
            box-shadow: 0 2px 4px rgba(0,0,0,0.1);
        }}
        .chart-title {{
            font-size: 18px;
            font-weight: bold;
            margin-bottom: 15px;
            color: {self.get_theme_color('title_color')};
        }}
        @media (max-width: 768px) {{
            .charts-container {{
                grid-template-columns: 1fr;
            }}
        }}
    </style>
</head>
<body>
    <div class="dashboard">
        <div class="header">
            <h1>{self.dashboard_spec.get('title', 'ChartCraft Dashboard')}</h1>
        </div>
        
        <div class="charts-container">
            {self.generate_charts_html()}
        </div>
    </div>
    
    <script>
        // Chart rendering logic would go here
        console.log('ChartCraft Dashboard loaded');
        
        // Fetch dashboard data
        fetch('/api/dashboard')
            .then(response => response.json())
            .then(data => {{
                console.log('Dashboard data:', data);
                // Render charts using ECharts or similar library
            }})
            .catch(error => {{
                console.error('Error loading dashboard:', error);
            }});
    </script>
</body>
</html>
"""
    
    def get_theme_color(self, color_name: str) -> str:
        """Get theme color (simplified)."""
        themes = {
            'background': '#ffffff',
            'header_background': '#f8f9fa',
            'card_background': '#ffffff',
            'title_color': '#333333'
        }
        return themes.get(color_name, '#ffffff')
    
    def generate_charts_html(self) -> str:
        """Generate HTML for charts."""
        html = ""
        for i, chart_spec in enumerate(self.dashboard_spec.get('charts', [])):
            html += f'''
        <div class="chart-card">
            <div class="chart-title">{chart_spec.get('title', f'Chart {i+1}')}</div>
            <div id="chart-{i}" style="height: 300px;"></div>
        </div>
'''
        return html
def render(dashboard) -> str:
    """Render dashboard to HTML string."""
    spec = dashboard.to_spec()
    
    html = f"""
<!DOCTYPE html>
<html>
<head>
    <title>{spec.get('title', 'ChartCraft Dashboard')}</title>
    <style>
        body {{
            font-family: Arial, sans-serif;
            margin: 0;
            padding: 20px;
            background-color: #ffffff;
            color: #333;
        }}
        .dashboard {{
            max-width: 1200px;
            margin: 0 auto;
        }}
        .header {{
            text-align: center;
            margin-bottom: 30px;
            padding: 20px;
            background-color: #f8f9fa;
            border-radius: 8px;
        }}
        .charts-container {{
            display: grid;
            grid-template-columns: repeat({spec.get('columns', 2)}, 1fr);
            gap: 20px;
        }}
        .chart-card {{
            background-color: #ffffff;
            border-radius: 8px;
            padding: 20px;
            box-shadow: 0 2px 4px rgba(0,0,0,0.1);
        }}
        .chart-title {{
            font-size: 18px;
            font-weight: bold;
            margin-bottom: 15px;
            color: #333333;
        }}
        @media (max-width: 768px) {{
            .charts-container {{
                grid-template-columns: 1fr;
            }}
        }}
    </style>
</head>
<body>
    <div class="dashboard">
        <div class="header">
            <h1>{spec.get('title', 'ChartCraft Dashboard')}</h1>
        </div>
        
        <div class="charts-container">
    """
    
    for i, chart_spec in enumerate(spec.get('charts', [])):
        html += f'''
            <div class="chart-card">
                <div class="chart-title">{chart_spec.get('title', f'Chart {i+1}')}</div>
                <div id="chart-{i}" style="height: 300px;">
                    <p>Chart {i+1}: {chart_spec.get('chart_type', 'bar')} chart with data</p>
                    <pre>{json.dumps(chart_spec.get('data', {}), indent=2)}</pre>
                </div>
            </div>
        '''
    
    html += """
        </div>
    </div>
</body>
</html>
"""
    
    return html
def save(dashboard, path: str):
    """Save dashboard to HTML file."""
    html = render(dashboard)
    with open(path, 'w', encoding='utf-8') as f:
        f.write(html)
    print(f"◆ Exported → {path}")
def serve(dashboard, port: int = 8050):
    """Serve dashboard locally."""
    spec = dashboard.to_spec()
    
    def run_server():
        server = HTTPServer(('localhost', port), lambda *args: SimpleHTTPRequestHandler(*args, dashboard_spec=spec))
        print(f"◆ ChartCraft → http://localhost:{port}")
        server.serve_forever()
    
    # Start server in a separate thread
    thread = Thread(target=run_server)
    thread.daemon = True
    thread.start()
    
    # Open browser
    webbrowser.open(f'http://localhost:{port}')
    
    # Keep main thread alive
    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        print("\n◆ Server stopped")
class ThemeManager:
    """Simple theme manager (no presets)."""
    
    def __init__(self):
        self.current_theme = {}
    
    def set_theme(self, **kwargs):
        """Set theme options (no presets)."""
        self.current_theme.update(kwargs)
    
    def get_theme(self) -> Dict[str, Any]:
        """Get current theme."""
        return self.current_theme
    
    def reset(self):
        """Reset theme to defaults."""
        self.current_theme = {}
# Global theme manager
_theme_manager = ThemeManager()
def theme(**kwargs):
    """Set global theme (no presets)."""
    _theme_manager.set_theme(**kwargs)
def reset_theme():
    """Reset global theme."""
    _theme_manager.reset()