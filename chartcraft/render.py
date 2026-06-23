"""
HTML rendering for ChartCraft v1.

Renders dashboard specs into interactive ECharts-powered HTML pages.
"""

from typing import Dict, Any
import json
import webbrowser
import time
from http.server import HTTPServer, BaseHTTPRequestHandler
from threading import Thread


def _build_charts_js(spec: Dict[str, Any]) -> str:
    """Build JavaScript that renders all charts via ECharts."""
    charts_json = json.dumps(spec.get('charts', []))
    columns = spec.get('columns', 2)

    return f"""
        var chartsData = {charts_json};
        var container = document.getElementById('charts-container');

        function getChartOption(chartSpec, idx) {{
            var data = chartSpec.data || {{}};
            var opts = chartSpec.options || {{}};
            var chartType = opts.chart_type || 'bar';
            var title = chartSpec.title || 'Chart ' + (idx + 1);

            var keys = Object.keys(data);
            if (keys.length === 0) {{
                return {{ title: {{ text: title, left: 'center' }}, xAxis: {{}}, yAxis: {{}}, series: [] }};
            }}

            // Determine x column and y column(s)
            var xCol = opts.x || keys[0];
            var yCols = opts.y ? (Array.isArray(opts.y) ? opts.y : [opts.y]) : keys.slice(1);
            if (yCols.length === 0 && keys.length >= 2) yCols = [keys[1]];

            var categories = data[xCol] || [];
            var colors = opts.colors || undefined;

            var option = {{
                title: {{ text: title, left: 'center', textStyle: {{ fontSize: 14 }} }},
                tooltip: {{ trigger: 'axis' }},
                grid: {{ left: '10%', right: '8%', top: '15%', bottom: '12%' }},
                animation: true,
                animationDuration: 800,
            }};

            if (chartType === 'pie' || chartType === 'donut') {{
                var pieData = [];
                var labelCol = xCol;
                var valueCol = yCols[0];
                if (categories.length > 0 && data[valueCol]) {{
                    for (var i = 0; i < categories.length; i++) {{
                        pieData.push({{
                            name: String(categories[i]),
                            value: data[valueCol][i]
                        }});
                    }}
                }} else {{
                    // Fallback: first key is name, second is value
                    var labelKey = keys[0];
                    var valKey = keys[1] || keys[0];
                    for (var i = 0; i < (data[labelKey] || []).length; i++) {{
                        pieData.push({{
                            name: String(data[labelKey][i]),
                            value: data[valKey][i]
                        }});
                    }}
                }}

                var isDonut = chartType === 'donut';
                option = {{
                    title: {{ text: title, left: 'center', textStyle: {{ fontSize: 14 }} }},
                    tooltip: {{ trigger: 'item', formatter: '{{b}}: {{c}} ({{d}}%)' }},
                    series: [{{
                        type: 'pie',
                        radius: isDonut ? ['40%', '65%'] : '70%',
                        center: ['50%', '55%'],
                        data: pieData,
                        label: {{ formatter: '{{b}}\\n{{d}}%', fontSize: 11 }},
                        emphasis: {{ itemStyle: {{ shadowBlur: 10, shadowColor: 'rgba(0,0,0,0.3)' }} }},
                        itemStyle: colors ? {{ color: function(params) {{
                            return colors[params.dataIndex % colors.length];
                        }} }} : undefined
                    }}]
                }};
                return option;
            }}

            if (chartType === 'bar' || chartType === 'line' || chartType === 'area' ||
                chartType === 'scatter') {{
                var isArea = chartType === 'area';
                var isScatter = chartType === 'scatter';
                var smooth = opts.smooth === true || opts.line_smooth === true;

                option.xAxis = {{
                    type: 'category',
                    data: categories,
                    axisLabel: {{ rotate: categories.length > 8 ? 45 : 0 }}
                }};
                option.yAxis = {{ type: 'value' }};
                option.series = [];

                yCols.forEach(function(col, i) {{
                    var seriesData = data[col] || [];
                    var item = {{
                        name: col,
                        type: isScatter ? 'scatter' : 'line',
                        data: seriesData,
                        smooth: smooth,
                        symbolSize: isScatter ? 10 : 4,
                        lineStyle: {{ width: 2 }},
                    }};
                    if (chartType === 'bar') {{
                        item.type = 'bar';
                        item.barWidth = '60%';
                    }}
                    if (isArea) {{
                        item.areaStyle = {{ opacity: 0.3 }};
                    }}
                    if (colors && colors[i]) {{
                        item.itemStyle = {{ color: colors[i] }};
                        if (item.lineStyle) item.lineStyle.color = colors[i];
                    }}
                    option.series.push(item);
                }});
                return option;
            }}

            // Gauge
            if (chartType === 'gauge') {{
                var val = data[yCols[0]] ? data[yCols[0]][0] : 0;
                return {{
                    series: [{{
                        type: 'gauge',
                        center: ['50%', '60%'],
                        startAngle: 210,
                        endAngle: -30,
                        min: opts.min || 0,
                        max: opts.max || 100,
                        data: [{{ value: val, name: title }}],
                        title: {{ fontSize: 13 }},
                        detail: {{ fontSize: 16, formatter: '{{value}}' }}
                    }}]
                }};
            }}

            // Radar
            if (chartType === 'radar') {{
                var indicator = categories.map(function(c) {{ return {{ name: c, max: opts.max || 100 }}; }});
                var radarSeries = yCols.map(function(col) {{
                    return {{
                        name: col,
                        value: data[col] || [],
                        areaStyle: {{ opacity: 0.2 }}
                    }};
                }});
                return {{
                    radar: {{ indicator: indicator, center: ['50%', '55%'], radius: '65%' }},
                    series: [{{
                        type: 'radar',
                        data: radarSeries
                    }}]
                }};
            }}

            // Heatmap
            if (chartType === 'heatmap') {{
                var heatmapData = [];
                var xKeys = data[xCol] || [];
                var yKey = yCols[0];
                var yValues = data[yKey] || [];
                for (var i = 0; i < Math.min(xKeys.length, yValues.length); i++) {{
                    heatmapData.push([i, 0, yValues[i]]);
                }}
                return {{
                    xAxis: {{ type: 'category', data: xKeys, axisLabel: {{ rotate: 45 }} }},
                    yAxis: {{ type: 'category', data: [''] }},
                    visualMap: {{ min: Math.min.apply(null, yValues), max: Math.max.apply(null, yValues), calculable: true }},
                    series: [{{
                        type: 'heatmap',
                        data: heatmapData,
                        label: {{ show: true }}
                    }}]
                }};
            }}

            // Funnel
            if (chartType === 'funnel') {{
                var funnelData = [];
                for (var i = 0; i < categories.length; i++) {{
                    funnelData.push({{ name: String(categories[i]), value: data[yCols[0]][i] }});
                }}
                return {{
                    series: [{{
                        type: 'funnel',
                        left: '10%',
                        right: '10%',
                        data: funnelData,
                        label: {{ formatter: '{{b}}: {{c}}' }}
                    }}]
                }};
            }}

            return option;
        }}

        function renderCharts() {{
            var cards = container.querySelectorAll('.chart-card');
            chartsData.forEach(function(chartSpec, idx) {{
                var chartEl = document.getElementById('chart-' + idx);
                if (!chartEl) return;
                var myChart = echarts.init(chartEl);
                var option = getChartOption(chartSpec, idx);
                myChart.setOption(option);
                window.addEventListener('resize', function() {{ myChart.resize(); }});
            }});
        }}

        renderCharts();
"""


def _render_html(spec: Dict[str, Any]) -> str:
    """Render dashboard spec to a complete HTML page with ECharts."""
    columns = spec.get('columns', 2)
    charts = spec.get('charts', [])
    spacing = spec.get('spacing', 20)

    # Build chart card HTML
    cards_html = ""
    for i, chart_spec in enumerate(charts):
        title = chart_spec.get('title', f'Chart {i+1}')
        height = chart_spec.get('options', {}).get('height', 300)
        cards_html += f'''
            <div class="chart-card">
                <div class="chart-title">{title}</div>
                <div id="chart-{i}" style="height: {height}px;"></div>
            </div>
        '''

    charts_js = _build_charts_js(spec)

    html = f"""<!DOCTYPE html>
<html>
<head>
    <meta charset="utf-8">
    <meta name="viewport" content="width=device-width, initial-scale=1">
    <title>{spec.get('title', 'ChartCraft Dashboard')}</title>
    <script src="https://cdn.jsdelivr.net/npm/echarts@5.5.0/dist/echarts.min.js"></script>
    <style>
        * {{ margin: 0; padding: 0; box-sizing: border-box; }}
        body {{
            font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
            background: #f5f5f5;
            color: #333;
            padding: 24px;
        }}
        .dashboard {{ max-width: 1400px; margin: 0 auto; }}
        .header {{
            text-align: center;
            margin-bottom: 24px;
            padding: 28px 20px;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            border-radius: 12px;
            color: white;
        }}
        .header h1 {{ font-size: 28px; font-weight: 700; letter-spacing: -0.5px; }}
        .charts-container {{
            display: grid;
            grid-template-columns: repeat({columns}, 1fr);
            gap: {spacing}px;
        }}
        .chart-card {{
            background: white;
            border-radius: 10px;
            padding: 16px;
            box-shadow: 0 1px 3px rgba(0,0,0,0.08), 0 1px 2px rgba(0,0,0,0.06);
            transition: box-shadow 0.2s;
        }}
        .chart-card:hover {{ box-shadow: 0 4px 12px rgba(0,0,0,0.1); }}
        .chart-title {{
            font-size: 15px;
            font-weight: 600;
            margin-bottom: 8px;
            color: #374151;
        }}
        .footer {{
            text-align: center;
            margin-top: 24px;
            padding: 16px;
            color: #9ca3af;
            font-size: 12px;
        }}
        @media (max-width: 768px) {{
            .charts-container {{ grid-template-columns: 1fr; }}
            body {{ padding: 12px; }}
            .header h1 {{ font-size: 22px; }}
        }}
    </style>
</head>
<body>
    <div class="dashboard">
        <div class="header">
            <h1>{spec.get('title', 'ChartCraft Dashboard')}</h1>
        </div>
        <div class="charts-container" id="charts-container">
            {cards_html}
        </div>
        <div class="footer">
            Generated by ChartCraft v1 &middot; Powered by ECharts
        </div>
    </div>
    <script>
    {charts_js}
    </script>
</body>
</html>"""
    return html


def render(dashboard) -> str:
    """Render dashboard to HTML string."""
    spec = dashboard.to_spec() if hasattr(dashboard, 'to_spec') else dashboard
    return _render_html(spec)


def save(dashboard, path: str):
    """Save dashboard to HTML file."""
    html = render(dashboard)
    with open(path, 'w', encoding='utf-8') as f:
        f.write(html)
    print(f"◆ Exported → {path}")


def save_all(dashboard, directory: str = "./"):
    """Export dashboard(s) to a directory."""
    import os
    os.makedirs(directory, exist_ok=True)
    path = os.path.join(directory, "dashboard.html")
    html = render(dashboard)
    with open(path, 'w', encoding='utf-8') as f:
        f.write(html)
    print(f"◆ Exported → {path}")


class SimpleHTTPRequestHandler(BaseHTTPRequestHandler):
    """Simple HTTP request handler for serving dashboards."""

    def __init__(self, *args, dashboard_spec: Dict[str, Any] = None, **kwargs):
        self.dashboard_spec = dashboard_spec
        super().__init__(*args, **kwargs)

    def do_GET(self):
        """Handle GET requests."""
        if self.path == "/":
            html = _render_html(self.dashboard_spec)
            body = html.encode("utf-8")
            self.send_response(200)
            self.send_header("Content-Type", "text/html; charset=utf-8")
            self.send_header("Content-Length", str(len(body)))
            self.send_header("Cache-Control", "no-cache")
            self.end_headers()
            self.wfile.write(body)
        elif self.path == "/api/dashboard":
            body = json.dumps(self.dashboard_spec).encode("utf-8")
            self.send_response(200)
            self.send_header("Content-Type", "application/json")
            self.send_header("Content-Length", str(len(body)))
            self.end_headers()
            self.wfile.write(body)
        else:
            self.send_response(404)
            self.send_header("Content-Type", "text/plain")
            self.end_headers()
            self.wfile.write(b"404 Not Found")

    def log_message(self, format, *args):
        """Suppress default logging."""
        pass


def serve(dashboard, port: int = 8050):
    """Serve dashboard locally."""
    spec = dashboard.to_spec() if hasattr(dashboard, 'to_spec') else dashboard

    def run_server():
        server = HTTPServer(
            ('localhost', port),
            lambda *args: SimpleHTTPRequestHandler(*args, dashboard_spec=spec)
        )
        print(f"◆ ChartCraft → http://localhost:{port}")
        server.serve_forever()

    thread = Thread(target=run_server)
    thread.daemon = True
    thread.start()

    webbrowser.open(f'http://localhost:{port}')

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


_theme_manager = ThemeManager()


def theme(**kwargs):
    """Set global theme (no presets)."""
    _theme_manager.set_theme(**kwargs)


def reset_theme():
    """Reset global theme."""
    _theme_manager.reset()
