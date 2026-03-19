"""
HTTP request handler — serves the viewer SPA, builder SPA, and all API routes.
"""

from __future__ import annotations
import json
import os
import threading
import time
import traceback
from http.server import BaseHTTPRequestHandler
from pathlib import Path
from typing import TYPE_CHECKING
from urllib.parse import urlparse, parse_qs

from chartcraft.core.serializer import dumps, loads
from chartcraft.server.sse import get_manager

if TYPE_CHECKING:
    from chartcraft.server.app_server import AppServer


STATIC_DIR = Path(__file__).parent.parent / "static"
BUILDER_DIR = Path(__file__).parent.parent / "builder"


class CCHandler(BaseHTTPRequestHandler):
    """One instance per request. `self.server_ref` is the AppServer."""

    server_ref: "AppServer" = None   # injected by AppServer

    def log_message(self, fmt, *args):
        # Suppress default noisy logging; could route to a logger later
        pass

    # ------------------------------------------------------------------
    # Route dispatch
    # ------------------------------------------------------------------

    def do_GET(self):
        parsed = urlparse(self.path)
        path = parsed.path.rstrip("/") or "/"
        qs = parse_qs(parsed.query)

        routes = {
            "/":                    self._serve_viewer,
            "/builder":             self._serve_builder,
            "/api/spec":            self._api_spec,
            "/api/events":          self._api_events,
            "/api/themes":          self._api_themes,
            "/api/pages":           self._api_pages,
            "/api/palettes":        self._api_palettes,
            "/api/projects":        self._api_projects_list,
            "/api/export/notebook": self._api_export_notebook,
            "/api/export/docker":   self._api_export_docker,
            "/api/connections":     self._api_connections_list,
            "/api/schema":          self._api_schema,
            "/api/filter_options":  self._api_filter_options,
        }

        # Dynamic page routes (everything that matches a registered page)
        if path in self.server_ref.pages:
            self._serve_viewer(page_path=path)
            return

        handler = routes.get(path)
        if handler:
            handler()
        elif path.startswith("/static/"):
            self._serve_static(path[len("/static/"):])
        elif path.startswith("/builder/components/"):
            self._serve_builder_component(path[len("/builder/components/"):])
        elif path.startswith("/api/projects/"):
            self._api_project_by_id(path)
        else:
            self._send_404()

    def do_POST(self):
        parsed = urlparse(self.path)
        path = parsed.path.rstrip("/") or "/"

        routes = {
            "/api/filter":          self._api_filter,
            "/api/layout":          self._api_layout,
            "/api/refresh":         self._api_refresh,
            "/api/parse":           self._api_parse,
            "/api/projects":        self._api_projects_save,
            "/api/export/notebook": self._api_export_notebook,
            "/api/export/docker":   self._api_export_docker,
            "/api/query":           self._api_query,
            "/api/connections":     self._api_connections_save,
        }
        handler = routes.get(path)
        if handler:
            handler()
        elif path.startswith("/api/projects/"):
            self._api_project_by_id(path)
        else:
            self._send_404()

    def do_DELETE(self):
        parsed = urlparse(self.path)
        path = parsed.path.rstrip("/") or "/"
        if path.startswith("/api/projects/"):
            self._api_project_delete(path)
        elif path.startswith("/api/connections/"):
            self._api_connection_delete(path)
        else:
            self._send_404()

    # ------------------------------------------------------------------
    # Viewer & Builder SPAs
    # ------------------------------------------------------------------

    def _serve_viewer(self, page_path: str = None):
        page_path = page_path or urlparse(self.path).path or "/"
        page_fn = self.server_ref.pages.get(page_path)
        if not page_fn:
            self._send_404()
            return

        try:
            dashboard = page_fn()
            theme = self.server_ref.theme_obj
            spec = dashboard.to_spec()
            nav = self._build_nav(current=page_path)

            html = self._load_template("viewer.html")
            html = html.replace("{{THEME_CSS}}", theme.to_css_vars())
            html = html.replace("{{ECHARTS_THEME}}", dumps(theme.to_echarts_theme()))
            html = html.replace("{{SPEC}}", dumps(spec))
            html = html.replace("{{NAV}}", dumps(nav))
            html = html.replace("{{TITLE}}", self.server_ref.title)
            html = html.replace("{{THEME_NAME}}", theme.name)
            html = html.replace("{{THEME_LIST}}", dumps(list(self.server_ref._themes_list())))

            # Start refresh threads — push full specs via SSE
            sse = get_manager()
            from chartcraft.core.serializer import dumps as cc_dumps
            for comp_id, spec_fn, interval in dashboard.refreshable_specs():
                sse.start_refresh(
                    comp_id, spec_fn, interval,
                    serialise_fn=lambda s, _id=comp_id: cc_dumps({"id": _id, "spec": s}),
                )

            self._send_html(html)
        except Exception:
            self._send_error(traceback.format_exc())

    def _serve_builder(self):
        html = self._load_template("builder.html", base=BUILDER_DIR)
        theme = self.server_ref.theme_obj
        html = html.replace("{{THEME_CSS}}", theme.to_css_vars())
        html = html.replace("{{TITLE}}", self.server_ref.title)
        self._send_html(html)

    # ------------------------------------------------------------------
    # API routes
    # ------------------------------------------------------------------

    def _api_spec(self):
        qs = parse_qs(urlparse(self.path).query)
        page_path = qs.get("page", ["/"])[0]
        filter_state = {}  # filters handled separately via POST /api/filter

        page_fn = self.server_ref.pages.get(page_path)
        if not page_fn:
            self._send_json({"error": f"Page '{page_path}' not found"}, status=404)
            return

        dashboard = page_fn()
        spec = dashboard.to_spec(filter_state)
        self._send_json(spec)

    def _api_events(self):
        """Open an SSE stream — keeps connection alive."""
        self.send_response(200)
        self.send_header("Content-Type", "text/event-stream")
        self.send_header("Cache-Control", "no-cache")
        self.send_header("X-Accel-Buffering", "no")
        self.send_header("Access-Control-Allow-Origin", "*")
        self.end_headers()

        sse = get_manager()
        client = sse.add_client(self.wfile)

        # Send initial heartbeat
        client.send("connected", dumps({"ts": time.time()}))

        # Keep alive with heartbeats every 15s
        try:
            while client.alive:
                time.sleep(15)
                if not client.send("heartbeat", dumps({"ts": time.time()})):
                    break
        finally:
            sse.remove_client(client)

    def _api_themes(self):
        from chartcraft.core.theme import THEMES
        self._send_json({name: t.to_dict() for name, t in THEMES.items()})

    def _api_pages(self):
        self._send_json(self._build_nav())

    def _api_palettes(self):
        from chartcraft.core.colors import PALETTES
        self._send_json(PALETTES)

    def _api_filter(self):
        """Receive filter state, re-query dashboard, return updated spec."""
        body = self._read_body()
        try:
            payload = loads(body)
            page_path = payload.get("page", "/")
            filter_state = payload.get("filters", {})
        except Exception:
            self._send_json({"error": "Invalid JSON"}, status=400)
            return

        page_fn = self.server_ref.pages.get(page_path)
        if not page_fn:
            self._send_json({"error": f"Page '{page_path}' not found"}, status=404)
            return

        dashboard = page_fn()
        spec = dashboard.to_spec(filter_state)

        # Broadcast updated spec to all SSE clients
        sse = get_manager()
        sse.broadcast("dashboard-update", dumps({"page": page_path, "spec": spec}))

        self._send_json(spec)

    def _api_layout(self):
        """Receive builder layout state, generate Python code."""
        body = self._read_body()
        try:
            payload = loads(body)
        except Exception:
            self._send_json({"error": "Invalid JSON"}, status=400)
            return

        try:
            from chartcraft.server.codegen import generate
            code = generate(payload)
            self._send_json({"code": code})
        except Exception:
            self._send_json({"error": traceback.format_exc()}, status=500)

    def _api_refresh(self):
        """Force a manual refresh of a component."""
        body = self._read_body()
        try:
            payload = loads(body)
            comp_id = payload.get("id")
        except Exception:
            self._send_json({"error": "Invalid JSON"}, status=400)
            return
        self._send_json({"ok": True, "id": comp_id})

    def _api_parse(self):
        """Parse Python code → builder canvas state (bidirectional sync)."""
        body = self._read_body()
        try:
            payload = loads(body)
            code = payload.get("code", "")
        except Exception:
            self._send_json({"error": "Invalid JSON"}, status=400)
            return
        try:
            from chartcraft.server.parser import parse_code
            state = parse_code(code)
            self._send_json(state)
        except Exception:
            self._send_json({"error": traceback.format_exc()}, status=500)

    def _api_projects_list(self):
        """GET /api/projects — list all saved projects."""
        try:
            from chartcraft.server.projects import list_projects
            self._send_json(list_projects())
        except Exception:
            self._send_json({"error": traceback.format_exc()}, status=500)

    def _api_projects_save(self):
        """POST /api/projects — save or update a project."""
        body = self._read_body()
        try:
            payload = loads(body)
        except Exception:
            self._send_json({"error": "Invalid JSON"}, status=400)
            return
        try:
            from chartcraft.server.projects import save_project
            project_id = payload.get("id") or str(int(time.time() * 1000))
            name  = payload.get("name", "Untitled")
            state = payload.get("state", {})
            result = save_project(project_id, name, state)
            self._send_json(result)
        except Exception:
            self._send_json({"error": traceback.format_exc()}, status=500)

    def _api_project_by_id(self, path: str):
        """GET /api/projects/{id} — load a single project."""
        project_id = path.split("/api/projects/", 1)[-1].rstrip("/")
        try:
            from chartcraft.server.projects import get_project
            p = get_project(project_id)
            if p is None:
                self._send_json({"error": "Not found"}, status=404)
            else:
                self._send_json(p)
        except Exception:
            self._send_json({"error": traceback.format_exc()}, status=500)

    def _api_project_delete(self, path: str):
        """DELETE /api/projects/{id} — delete a project."""
        project_id = path.split("/api/projects/", 1)[-1].rstrip("/")
        try:
            from chartcraft.server.projects import delete_project
            ok = delete_project(project_id)
            self._send_json({"ok": ok})
        except Exception:
            self._send_json({"error": traceback.format_exc()}, status=500)

    def _api_export_notebook(self):
        """GET or POST /api/export/notebook — download .ipynb."""
        if self.command == "POST":
            body = self._read_body()
            try:
                state = loads(body)
            except Exception:
                self._send_json({"error": "Invalid JSON"}, status=400)
                return
        else:
            state = {"title": "Dashboard", "pages": []}

        try:
            from chartcraft.server.codegen import generate_notebook
            nb = generate_notebook(state)
            data = nb.encode("utf-8")
            title = state.get("title", "dashboard").replace(" ", "_").lower()
            self.send_response(200)
            self.send_header("Content-Type", "application/json")
            self.send_header("Content-Disposition", f'attachment; filename="{title}.ipynb"')
            self.send_header("Content-Length", str(len(data)))
            self.end_headers()
            self.wfile.write(data)
        except Exception:
            self._send_json({"error": traceback.format_exc()}, status=500)

    def _api_export_docker(self):
        """GET or POST /api/export/docker — download Docker zip."""
        if self.command == "POST":
            body = self._read_body()
            try:
                state = loads(body)
            except Exception:
                self._send_json({"error": "Invalid JSON"}, status=400)
                return
        else:
            state = {"title": "Dashboard", "pages": []}

        try:
            from chartcraft.server.codegen import generate_docker_zip
            data = generate_docker_zip(state)
            title = state.get("title", "dashboard").replace(" ", "_").lower()
            self.send_response(200)
            self.send_header("Content-Type", "application/zip")
            self.send_header("Content-Disposition", f'attachment; filename="{title}_docker.zip"')
            self.send_header("Content-Length", str(len(data)))
            self.end_headers()
            self.wfile.write(data)
        except Exception:
            self._send_json({"error": traceback.format_exc()}, status=500)

    # ------------------------------------------------------------------
    # Phase 5 — Query API, Connections, Filter Options
    # ------------------------------------------------------------------

    def _api_query(self):
        """POST /api/query — execute SQL against a registered or inline connector."""
        body = self._read_body()
        try:
            payload = loads(body)
        except Exception:
            self._send_json({"error": "Invalid JSON"}, status=400)
            return
        try:
            from chartcraft.server.query_api import execute_query, get_connector_str
            conn_str = payload.get("conn_str") or get_connector_str(payload.get("conn_id", ""))
            if not conn_str:
                self._send_json({"error": "No connection string provided"}, status=400)
                return
            sql   = payload.get("sql", "").strip()
            limit = int(payload.get("limit", 500))
            result = execute_query(conn_str, sql, limit=limit)
            self._send_json(result)
        except Exception:
            self._send_json({"error": traceback.format_exc()}, status=500)

    def _api_schema(self):
        """GET /api/schema?conn_id=...&conn_str=... — return tables + columns."""
        qs = parse_qs(urlparse(self.path).query)
        try:
            from chartcraft.server.query_api import get_schema, get_connector_str
            conn_str = qs.get("conn_str", [""])[0] or get_connector_str(qs.get("conn_id", [""])[0])
            if not conn_str:
                self._send_json({"error": "No connection string provided"}, status=400)
                return
            self._send_json(get_schema(conn_str))
        except Exception:
            self._send_json({"error": traceback.format_exc()}, status=500)

    def _api_connections_list(self):
        """GET /api/connections — list all registered connectors."""
        try:
            from chartcraft.server.query_api import list_connectors
            self._send_json(list_connectors())
        except Exception:
            self._send_json({"error": traceback.format_exc()}, status=500)

    def _api_connections_save(self):
        """POST /api/connections — register or update a connector."""
        body = self._read_body()
        try:
            payload = loads(body)
        except Exception:
            self._send_json({"error": "Invalid JSON"}, status=400)
            return
        try:
            from chartcraft.server.query_api import save_connector
            import time as _time
            conn_id  = payload.get("id") or str(int(_time.time() * 1000))
            name     = payload.get("name", "Connector")
            conn_str = payload.get("conn_str", "")
            if not conn_str:
                self._send_json({"error": "conn_str required"}, status=400)
                return
            result = save_connector(conn_id, name, conn_str)
            self._send_json(result)
        except Exception:
            self._send_json({"error": traceback.format_exc()}, status=500)

    def _api_connection_delete(self, path: str):
        """DELETE /api/connections/{id} — delete a connector."""
        conn_id = path.split("/api/connections/", 1)[-1].rstrip("/")
        try:
            from chartcraft.server.query_api import delete_connector
            ok = delete_connector(conn_id)
            self._send_json({"ok": ok})
        except Exception:
            self._send_json({"error": traceback.format_exc()}, status=500)

    def _api_filter_options(self):
        """
        GET /api/filter_options?page=...&filter_id=...&filters=base64json
        Returns updated option list for a dependent filter based on current filter state.
        """
        qs = parse_qs(urlparse(self.path).query)
        try:
            import base64
            page_path = qs.get("page", ["/"])[0]
            filter_id = qs.get("filter_id", [""])[0]
            raw_f     = qs.get("filters", ["{}"])[0]
            try:
                filter_state = json.loads(base64.b64decode(raw_f + "==").decode())
            except Exception:
                filter_state = {}

            page_fn = self.server_ref.pages.get(page_path)
            if not page_fn:
                self._send_json({"error": "Page not found"}, status=404)
                return

            dashboard = page_fn()
            # Find the filter with this id
            target = next((f for f in dashboard.filters if f.id == filter_id or f.name == filter_id), None)
            if not target:
                self._send_json({"options": []})
                return

            # If filter has a callable options source, call it with current filters
            options = target.options
            if callable(options):
                try:
                    import inspect
                    sig = inspect.signature(options)
                    options = options(filter_state) if len(sig.parameters) > 0 else options()
                except Exception:
                    options = []

            self._send_json({"id": filter_id, "options": options or []})
        except Exception:
            self._send_json({"error": traceback.format_exc()}, status=500)

    # ------------------------------------------------------------------
    # Static files
    # ------------------------------------------------------------------

    def _serve_static(self, rel_path: str):
        full = STATIC_DIR / rel_path
        if not full.exists():
            self._send_404()
            return
        ext = full.suffix.lower()
        mime = {
            ".js": "application/javascript",
            ".css": "text/css",
            ".png": "image/png",
            ".svg": "image/svg+xml",
            ".ico": "image/x-icon",
        }.get(ext, "application/octet-stream")
        data = full.read_bytes()
        self.send_response(200)
        self.send_header("Content-Type", mime)
        self.send_header("Content-Length", str(len(data)))
        self.end_headers()
        self.wfile.write(data)

    def _serve_builder_component(self, rel_path: str):
        """Serve JS/CSS files from the builder/components/ directory."""
        full = BUILDER_DIR / "components" / rel_path
        if not full.exists():
            self._send_404()
            return
        ext = full.suffix.lower()
        mime = {
            ".js":  "application/javascript",
            ".css": "text/css",
        }.get(ext, "application/octet-stream")
        data = full.read_bytes()
        self.send_response(200)
        self.send_header("Content-Type", mime)
        self.send_header("Content-Length", str(len(data)))
        self.end_headers()
        self.wfile.write(data)

    # ------------------------------------------------------------------
    # Helpers
    # ------------------------------------------------------------------

    def _load_template(self, name: str, base: Path = None) -> str:
        base = base or STATIC_DIR
        path = base / name
        if path.exists():
            return path.read_text(encoding="utf-8")
        raise FileNotFoundError(f"Template not found: {path}")

    def _build_nav(self, current: str = None) -> list:
        return [
            {
                "path": path,
                "label": fn.__doc__ or fn.__name__.replace("_", " ").title(),
                "active": path == current,
            }
            for path, fn in self.server_ref.pages.items()
        ]

    def _read_body(self) -> str:
        length = int(self.headers.get("Content-Length", 0))
        return self.rfile.read(length).decode("utf-8")

    def _send_html(self, html: str, status: int = 200):
        data = html.encode("utf-8")
        self.send_response(status)
        self.send_header("Content-Type", "text/html; charset=utf-8")
        self.send_header("Content-Length", str(len(data)))
        self.end_headers()
        self.wfile.write(data)

    def _send_json(self, obj, status: int = 200):
        data = dumps(obj).encode("utf-8")
        self.send_response(status)
        self.send_header("Content-Type", "application/json")
        self.send_header("Content-Length", str(len(data)))
        self.send_header("Access-Control-Allow-Origin", "*")
        self.end_headers()
        self.wfile.write(data)

    def _send_404(self):
        self._send_html("<h1>404 Not Found</h1>", status=404)

    def _send_error(self, detail: str):
        html = f"<h1>Server Error</h1><pre>{detail}</pre>"
        self._send_html(html, status=500)
