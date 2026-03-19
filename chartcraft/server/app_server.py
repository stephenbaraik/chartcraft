"""
AppServer — wraps Python's http.server with multi-threaded request handling.
"""

from __future__ import annotations
import os
import sys
import threading
import webbrowser
from http.server import ThreadingHTTPServer
from typing import Callable, Dict, Optional

from chartcraft.core.theme import get_theme, THEMES, Theme
from chartcraft.server.handler import CCHandler


class AppServer:
    def __init__(self, title: str, theme: str = "default"):
        self.title = title
        self.pages: Dict[str, Callable] = {}
        self._theme_name = theme
        self.theme_obj: Theme = get_theme(theme)
        self._password: Optional[str] = None   # HTTP Basic Auth password (username = "admin")
        self._token: Optional[str] = None      # Bearer token / ?token= query param

    def _themes_list(self):
        return list(THEMES.keys())

    def page(self, path: str):
        """Decorator — register a dashboard page at the given URL path."""
        def decorator(fn: Callable) -> Callable:
            self.pages[path] = fn
            return fn
        return decorator

    def set_theme(self, name: str):
        self.theme_obj = get_theme(name)
        self._theme_name = name

    def run(
        self,
        host: str = "localhost",
        port: int = 8050,
        debug: bool = False,
        open_browser: bool = True,
        password: str = None,
        token: str = None,
    ):
        if password:
            self._password = password
        if token:
            self._token = token
        # Inject server reference into handler class
        CCHandler.server_ref = self

        server = ThreadingHTTPServer((host, port), CCHandler)
        url = f"http://{host}:{port}"

        print(f"\n  ◆ ChartCraft  →  {url}")
        print(f"  Builder       →  {url}/builder")
        print(f"  Theme         →  {self._theme_name}")
        print(f"  Pages         →  {list(self.pages.keys())}")
        print("\n  Press Ctrl+C to stop.\n")

        if open_browser:
            threading.Timer(0.5, lambda: webbrowser.open(url)).start()

        try:
            server.serve_forever()
        except KeyboardInterrupt:
            print("\n  ◆ ChartCraft stopped.")
            server.server_close()

    def save(self, path: str, page: str = "/", theme: str = None) -> str:
        """Export a dashboard page as a standalone HTML file."""
        if theme:
            self.set_theme(theme)
        page_fn = self.pages.get(page)
        if not page_fn:
            raise ValueError(f"Page '{page}' not registered.")
        dashboard = page_fn()
        html = self._render_static(dashboard)
        with open(path, "w", encoding="utf-8") as f:
            f.write(html)
        print(f"  ◆ Exported → {path}")
        return path

    def save_all(self, output_dir: str, theme: str = None) -> list:
        """Export all registered pages as separate HTML files into output_dir.

        Path mapping: '/' → 'index.html', '/products' → 'products.html'.
        Returns a list of file paths written.
        """
        import os as _os
        if theme:
            self.set_theme(theme)
        _os.makedirs(output_dir, exist_ok=True)
        written = []
        for page_path, page_fn in self.pages.items():
            if page_path == "/":
                filename = "index.html"
            else:
                filename = page_path.lstrip("/").replace("/", "_") + ".html"
            full_path = _os.path.join(output_dir, filename)
            dashboard = page_fn()
            html = self._render_static(dashboard)
            with open(full_path, "w", encoding="utf-8") as f:
                f.write(html)
            print(f"  ◆ Exported → {full_path}")
            written.append(full_path)
        return written

    def to_html(self, page: str = "/", theme: str = None) -> str:
        """Return the dashboard HTML as a string."""
        if theme:
            self.set_theme(theme)
        page_fn = self.pages.get(page)
        if not page_fn:
            raise ValueError(f"Page '{page}' not registered.")
        dashboard = page_fn()
        return self._render_static(dashboard)

    def _render_static(self, dashboard) -> str:
        from pathlib import Path
        from chartcraft.core.serializer import dumps
        static_dir = Path(__file__).parent.parent / "static"
        template = (static_dir / "viewer.html").read_text(encoding="utf-8")
        theme = self.theme_obj
        spec = dashboard.to_spec()
        html = template
        html = html.replace("{{THEME_CSS}}", theme.to_css_vars())
        html = html.replace("{{ECHARTS_THEME}}", dumps(theme.to_echarts_theme()))
        html = html.replace("{{SPEC}}", dumps(spec))
        html = html.replace("{{NAV}}", "[]")
        html = html.replace("{{TITLE}}", self.title)
        html = html.replace("{{THEME_NAME}}", theme.name)
        html = html.replace("{{THEME_LIST}}", dumps(self._themes_list()))
        # Remove SSE setup for static export
        html = html.replace("{{STATIC_MODE}}", "true")
        return html
