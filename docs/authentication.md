# Authentication

ChartCraft supports two authentication methods: HTTP Basic Auth (username/password) and Bearer token auth. Both protect all routes — the dashboard viewer, the builder, and all API endpoints.

---

## HTTP Basic Auth

Require a password to access the dashboard. The browser will show a native login prompt.

```python
app.run(password="my-secure-password")
```

- **Username:** `admin` (fixed)
- **Password:** whatever you set

When a user opens the dashboard, their browser shows a login dialog. After successful login, the browser caches the credentials for the session.

---

## Bearer Token Auth

Useful for API clients, scripts, and programmatic access.

```python
app.run(token="my-secret-api-token")
```

Clients authenticate by including the token in one of two ways:

### Via URL query parameter

```
http://localhost:8050/?token=my-secret-api-token
```

Share this URL with users and they're automatically logged in. Bookmark it to skip the login prompt.

### Via Authorization header

```
Authorization: Bearer my-secret-api-token
```

For API clients and scripts:

```python
import requests

response = requests.get(
    "http://localhost:8050/api/spec",
    headers={"Authorization": "Bearer my-secret-api-token"},
)
```

---

## Both Together

You can enable both password and token simultaneously — either one grants access:

```python
app.run(
    password="browser-password",     # For human users
    token="api-token-123",           # For scripts and API clients
)
```

---

## No Auth (Default)

When neither `password` nor `token` is set, the dashboard is open to anyone who can reach the server:

```python
app.run()   # No auth — open access
```

---

## Setting Auth via Environment Variables

```python
import os

app.run(
    host="0.0.0.0",
    port=8050,
    password=os.getenv("DASHBOARD_PASSWORD"),
    token=os.getenv("DASHBOARD_TOKEN"),
)
```

`.env` file (never commit to git):

```
DASHBOARD_PASSWORD=your-secure-password
DASHBOARD_TOKEN=your-api-token
```

---

## What Is Protected

When auth is configured, **every route** requires authentication:

- `GET /` — Dashboard viewer
- `GET /builder` — Visual builder
- `GET /api/*` — All API endpoints
- `POST /api/*` — All POST endpoints
- `GET /static/*` — Static assets

An unauthenticated request receives:

```
HTTP 401 Unauthorized
WWW-Authenticate: Basic realm="ChartCraft"
```

---

## Behind a Reverse Proxy

If you put ChartCraft behind nginx or a cloud load balancer and want to handle auth at the proxy level, do not set `password` or `token` in ChartCraft — let the proxy handle it:

```nginx
server {
    location / {
        auth_basic "ChartCraft";
        auth_basic_user_file /etc/nginx/.htpasswd;

        proxy_pass http://127.0.0.1:8050;
        proxy_buffering off;  # Required for SSE
    }
}
```

---

## Security Notes

- Passwords and tokens are transmitted in plain text over HTTP. **Always use HTTPS in production** — terminate TLS at a reverse proxy (nginx, Caddy, or a cloud load balancer).
- HTTP Basic Auth credentials are cached by the browser. Logging out requires either closing the browser or clearing credentials.
- Bearer token in the URL (`?token=...`) will appear in server access logs. Prefer the `Authorization` header for sensitive deployments.
- There is no built-in session management or token expiry — tokens are valid until you restart the app with a different token value.
