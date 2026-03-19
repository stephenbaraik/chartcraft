"""
Server-Sent Events manager.
Tracks all open SSE connections and broadcasts events to them.
"""

from __future__ import annotations
import threading
import time
from typing import Dict, List, Callable, Any


class SSEClient:
    def __init__(self, wfile):
        self.wfile = wfile
        self.alive = True
        self._lock = threading.Lock()

    def send(self, event: str, data: str) -> bool:
        """Send a single SSE event. Returns False if client disconnected."""
        try:
            with self._lock:
                msg = f"event: {event}\ndata: {data}\n\n"
                self.wfile.write(msg.encode("utf-8"))
                self.wfile.flush()
            return True
        except (BrokenPipeError, ConnectionResetError, OSError):
            self.alive = False
            return False


class SSEManager:
    def __init__(self):
        self._clients: List[SSEClient] = []
        self._lock = threading.Lock()
        self._refresh_threads: Dict[str, threading.Thread] = {}

    def add_client(self, wfile) -> SSEClient:
        client = SSEClient(wfile)
        with self._lock:
            self._clients.append(client)
        return client

    def remove_client(self, client: SSEClient):
        with self._lock:
            self._clients = [c for c in self._clients if c is not client]

    def broadcast(self, event: str, data: str):
        """Send an event to all connected clients, removing dead ones."""
        dead = []
        with self._lock:
            clients = list(self._clients)
        for client in clients:
            if not client.send(event, data):
                dead.append(client)
        if dead:
            with self._lock:
                self._clients = [c for c in self._clients if c not in dead]

    def client_count(self) -> int:
        with self._lock:
            return len(self._clients)

    # ------------------------------------------------------------------
    # Refresh threads — one per (component_id, interval)
    # ------------------------------------------------------------------

    def start_refresh(self, component_id: str, data_fn: Callable, interval: int,
                      serialise_fn: Callable = None):
        """
        Spawn a background thread that calls data_fn every `interval` seconds
        and broadcasts the result via SSE.
        """
        key = f"{component_id}:{interval}"
        if key in self._refresh_threads and self._refresh_threads[key].is_alive():
            return  # already running

        def _loop():
            import json
            from chartcraft.core.serializer import dumps
            while True:
                time.sleep(interval)
                if self.client_count() == 0:
                    continue
                try:
                    result = data_fn()
                    if serialise_fn:
                        payload = serialise_fn(result)
                    else:
                        payload = dumps({"id": component_id, "data": result})
                    self.broadcast("refresh", payload)
                except Exception as e:
                    self.broadcast("error", dumps({"id": component_id, "error": str(e)}))

        t = threading.Thread(target=_loop, daemon=True, name=f"cc-refresh-{component_id}")
        t.start()
        self._refresh_threads[key] = t

    def stop_all(self):
        """Signal threads to stop (they are daemon threads, so they die with process)."""
        self._refresh_threads.clear()


# Global singleton used by the HTTP server
_manager = SSEManager()


def get_manager() -> SSEManager:
    return _manager
