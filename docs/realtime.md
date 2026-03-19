# Real-Time Data

ChartCraft uses **Server-Sent Events (SSE)** to push data updates from the server to the browser. Charts and KPIs update live without any page reloads.

---

## How It Works

1. Browser loads the dashboard and opens a persistent SSE connection to `/api/events`
2. For every refreshable component, the server starts a background thread
3. Every N seconds, the thread calls the component's `data_fn()`, serializes the result, and broadcasts it via SSE
4. The browser receives the event and animates the chart to the new data
5. On disconnect, SSE auto-reconnects within 3 seconds

Each chart and KPI refreshes **independently** on its own interval.

---

## Adding Real-Time to Charts

Use `data_fn` + `refresh` on any chart:

```python
cc.Line(
    data_fn=lambda: db.query_dict(
        "SELECT ts, value FROM metrics ORDER BY ts DESC LIMIT 100"
    ),
    x="ts", y="value",
    title="Live Stream",
    refresh=3,          # Push new data every 3 seconds
)
```

`data_fn` is called in a background thread — slow queries won't block the web server.

---

## Real-Time KPIs

```python
cc.KPI(
    "Active Sessions",
    data_fn=lambda: str(db.query("SELECT COUNT(*) FROM sessions WHERE active=1")[0][0]),
    refresh=5,              # Update every 5 seconds
)

cc.KPI(
    "Events/sec",
    data_fn=lambda: f"{random.randint(800, 1200):,}",
    refresh=2,
)

cc.KPI(
    "Error Rate",
    data_fn=lambda: f"{get_error_rate():.2f}%",
    refresh=10,
)
```

KPI `data_fn` must return a string (the displayed value).

---

## Different Refresh Intervals

Every component has its own independent interval:

```python
cc.Dashboard(
    title="Live Metrics",
    kpis=[
        cc.KPI("Sessions",  data_fn=get_sessions, refresh=4),   # Every 4s
        cc.KPI("Revenue",   data_fn=get_revenue,  refresh=30),  # Every 30s
        cc.KPI("Errors",    data_fn=get_errors,   refresh=2),   # Every 2s
    ],
    charts=[
        cc.Line(data_fn=get_stream,  x="ts", y="value", refresh=3),   # Every 3s
        cc.Bar( data_fn=get_totals,  x="cat", y="amt",  refresh=60),  # Every 60s
    ],
)
```

The server runs one background thread per unique `(component_id, interval)` pair.

---

## Full-Page Refresh

Set `refresh` on the Dashboard itself to reload the entire page structure:

```python
cc.Dashboard(
    title="Hourly Report",
    refresh=3600,       # Reload page every hour
    charts=[...],
)
```

This triggers a full re-render of the dashboard spec (all charts, KPIs, filters) on all connected browsers simultaneously.

---

## Complete Real-Time Example

```python
import chartcraft as cc
import time
import math
import random

db = cc.connect_sql("sqlite:///metrics.db")
app = cc.App("Live Metrics", theme="obsidian")

def live_stream():
    """Returns last 60 data points."""
    now = time.time()
    return [
        {
            "ts": int(now - i * 5),
            "value": round(50 + 20 * math.sin(now / 10 - i * 0.3) + random.uniform(-5, 5), 2),
        }
        for i in range(60, -1, -1)
    ]

def active_users():
    return str(random.randint(1200, 1800))

def error_rate():
    return f"{random.uniform(0.05, 0.5):.2f}%"

@app.page("/")
def realtime():
    """Live Data"""
    return cc.Dashboard(
        title="Live Metrics",
        subtitle="Updates every few seconds",
        kpis=[
            cc.KPI("Active Users",   data_fn=active_users, refresh=4),
            cc.KPI("Events/sec",     data_fn=lambda: str(random.randint(800, 1200)), refresh=2),
            cc.KPI("Error Rate",     data_fn=error_rate,   refresh=5),
        ],
        charts=[
            cc.Line(
                data_fn=live_stream,
                x="ts", y="value",
                title="Live Event Stream",
                col=0, colspan=12, height=360,
                refresh=3,
                smooth=True,
                show_dots=False,
                colors=["#8B5CF6"],
            ),
        ],
    )

app.run()
```

---

## LIVE Badge

When any component has `refresh > 0`, the viewer shows a **LIVE** badge in the top-right of the nav bar. A timestamp below the badge shows when data was last updated.

---

## SSE Connection Details

- **URL:** `GET /api/events`
- **Protocol:** `text/event-stream` (W3C Server-Sent Events)
- **Events pushed by server:**

| Event | Payload | Description |
|-------|---------|-------------|
| `connected` | `{"ts": timestamp}` | Sent once on connect |
| `heartbeat` | `{"ts": timestamp}` | Sent every 15 seconds to keep the connection alive |
| `refresh` | `{"id": "chart-abc", "spec": {...}}` | Full chart or KPI spec update |
| `dashboard-update` | `{"page": "/", "spec": {...}}` | Full dashboard refresh |

- **Reconnect:** Browser automatically reconnects on disconnect (3-second retry)
- **Multiple tabs:** Each browser tab gets its own SSE connection; all receive the same broadcasts

---

## Performance Notes

- Background threads are deduplicated by component ID — registering the same component multiple times (e.g. on repeated page loads) reuses the existing thread
- `data_fn` is called in a background thread — blocking I/O (slow queries) won't delay other requests
- For very fast data (< 1 second), consider using a WebSocket connector instead
- Heavy dashboards with many `refresh` components: use longer intervals (≥ 5s) to avoid hammering the database

---

## Stopping Refresh

To disable refresh for a specific component, omit `refresh` or set it to `None`:

```python
cc.Line(data, refresh=None)     # No refresh (static)
cc.Line(data)                   # Same — default is None
```

To add a manual refresh button instead, the user can hard-reload the page (F5) or use a `cc.KPI` with a link to trigger a page refresh.
