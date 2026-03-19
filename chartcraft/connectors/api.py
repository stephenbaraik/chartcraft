"""
REST API connector — zero dependencies (urllib).
"""

from __future__ import annotations
import json
import urllib.request
import urllib.parse
import urllib.error
from typing import Any, Dict, Optional


class APIConnector:
    def __init__(self, base_url: str, headers: Optional[Dict[str, str]] = None, timeout: int = 30):
        self.base_url = base_url.rstrip("/")
        self.headers = {"Content-Type": "application/json", "Accept": "application/json"}
        if headers:
            self.headers.update(headers)
        self.timeout = timeout

    def _request(self, method: str, endpoint: str, params: dict = None, data: Any = None) -> Any:
        url = self.base_url + "/" + endpoint.lstrip("/")
        if params:
            url += "?" + urllib.parse.urlencode(params)

        body = json.dumps(data).encode() if data else None
        req = urllib.request.Request(url, data=body, method=method)
        for k, v in self.headers.items():
            req.add_header(k, v)

        try:
            with urllib.request.urlopen(req, timeout=self.timeout) as resp:
                raw = resp.read().decode("utf-8")
                try:
                    return json.loads(raw)
                except json.JSONDecodeError:
                    return raw
        except urllib.error.HTTPError as e:
            raise RuntimeError(f"HTTP {e.code} from {url}: {e.read().decode()}")
        except urllib.error.URLError as e:
            raise RuntimeError(f"Connection error to {url}: {e.reason}")

    def get(self, endpoint: str, params: dict = None) -> Any:
        return self._request("GET", endpoint, params=params)

    def post(self, endpoint: str, data: Any = None) -> Any:
        return self._request("POST", endpoint, data=data)

    def put(self, endpoint: str, data: Any = None) -> Any:
        return self._request("PUT", endpoint, data=data)

    def delete(self, endpoint: str) -> Any:
        return self._request("DELETE", endpoint)

    def set_header(self, key: str, value: str) -> "APIConnector":
        self.headers[key] = value
        return self

    def __repr__(self):
        return f"APIConnector({self.base_url!r})"
