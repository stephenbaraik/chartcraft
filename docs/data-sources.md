# Data Sources

ChartCraft connects to SQL databases, CSV files, and REST APIs. SQLite and CSV work with zero additional dependencies. Other databases require optional extras.

---

## SQL Databases

### SQLite (zero dependencies)

```python
db = cc.connect_sql("sqlite:///analytics.db")
```

SQLite files are created automatically if they don't exist.

### PostgreSQL

```bash
pip install "chartcraft[pg]"
```

```python
db = cc.connect_sql("postgresql://user:password@localhost:5432/mydb")
```

### MySQL

```bash
pip install "chartcraft[mysql]"
```

```python
db = cc.connect_sql("mysql+pymysql://user:password@localhost/mydb")
```

### SQL Server

```bash
pip install "chartcraft[mssql]"
```

```python
db = cc.connect_sql("mssql+pyodbc://user:password@server/mydb")
```

### SQLConnector Methods

```python
db = cc.connect_sql("sqlite:///data.db")

# Query — returns list of tuples
rows = db.query("SELECT region, revenue FROM sales WHERE year = 2024")
# → [(region1, revenue1), (region2, revenue2), ...]

# Query dict — returns list of dicts (use this for charts)
rows = db.query_dict("SELECT region, revenue FROM sales")
# → [{"region": "North", "revenue": 120000}, ...]

# Query DataFrame (requires chartcraft[pandas])
df = db.query_df("SELECT * FROM sales")

# Execute non-SELECT statements
db.execute("INSERT INTO events (type, ts) VALUES ('load', CURRENT_TIMESTAMP)")

# Schema introspection
tables = db.tables()
# → ["sales", "customers", "products", "events"]

columns = db.schema("sales")
# → [{"name": "id", "type": "INTEGER"}, {"name": "region", "type": "TEXT"}, ...]

# Always close when done (if not using in-line with data_fn)
db.close()
```

### Using SQL Data in Charts

Pass the query result directly:

```python
db = cc.connect_sql("sqlite:///data.db")

@app.page("/")
def overview():
    sales_data = db.query_dict(
        "SELECT month, SUM(revenue) as revenue FROM sales GROUP BY month ORDER BY month"
    )
    return cc.Dashboard(
        charts=[
            cc.Line(sales_data, x="month", y="revenue", title="Monthly Revenue"),
        ]
    )
```

For real-time data that re-runs the query on every refresh:

```python
cc.Line(
    data_fn=lambda: db.query_dict("SELECT ts, value FROM metrics ORDER BY ts DESC LIMIT 100"),
    x="ts", y="value",
    title="Live Metrics",
    refresh=5,
)
```

---

## CSV Files

```python
# Single CSV file
csv = cc.connect_csv("sales.csv")

# Directory — loads all .csv and .tsv files
csv = cc.connect_csv("./data/")
```

### CSVConnector Methods

```python
# List available tables (one per file, named by filename without extension)
csv.tables()
# → ["sales", "customers", "products"]

# Query a table — returns list of dicts
rows = csv.query("sales")
# → [{"month": "Jan", "revenue": "100000"}, ...]

# Query as column dict (better for charting)
cols = csv.query_as_columns("sales")
# → {"month": ["Jan", "Feb", "Mar"], "revenue": [100000, 200000, 150000]}

# Reload from disk (if files change)
csv.reload()
```

### CSV Data Types

ChartCraft automatically coerces CSV values:
- Integers: `"100"` → `100`
- Floats: `"3.14"` → `3.14`
- Null/empty/`NA`/`None` → `None`
- Everything else: string

```python
# Use column data directly in charts
cols = csv.query_as_columns("sales")

cc.Bar(cols, x="month", y="revenue", title="Monthly Sales")
```

---

## REST APIs

```python
api = cc.connect_api(
    "https://api.example.com",
    headers={"Authorization": "Bearer YOUR_TOKEN"},
)
```

### APIConnector Methods

```python
# GET request
users = api.get("/users", params={"limit": 100, "active": True})
# → parsed JSON (dict or list)

# POST request
response = api.post("/events", data={"type": "page_view", "user_id": 123})

# PUT request
api.put("/users/42", data={"name": "Updated Name"})

# DELETE request
api.delete("/sessions/abc123")

# Fluent header chaining
api.set_header("X-Request-ID", "abc123").get("/data")
```

### Example: Real-time API Chart

```python
api = cc.connect_api("https://api.coinbase.com")

cc.Line(
    data_fn=lambda: api.get("/v2/prices/BTC-USD/historic", params={"period": "day"}),
    x="time", y="price",
    title="BTC Price (24h)",
    refresh=30,
)
```

---

## Using Data in Dashboards

### Static data (computed once at page load)

```python
@app.page("/")
def overview():
    data = db.query_dict("SELECT ...")   # Runs once when page loads
    return cc.Dashboard(
        charts=[cc.Bar(data, title="Sales")]
    )
```

### Dynamic data (re-fetched on each browser request)

```python
@app.page("/")
def overview():
    # Runs fresh on every browser request (no caching)
    return cc.Dashboard(
        charts=[
            cc.Bar(
                data_fn=lambda: db.query_dict("SELECT ..."),
                title="Sales",
            )
        ]
    )
```

### Real-time data (pushed via SSE every N seconds)

```python
cc.Line(
    data_fn=lambda: db.query_dict("SELECT ts, value FROM metrics ORDER BY ts DESC LIMIT 100"),
    x="ts", y="value",
    title="Live Stream",
    refresh=5,      # Server pushes new data every 5 seconds
)
```

See [Real-Time Data](realtime.md) for full details.

---

## Filter-Linked Queries

Charts can re-query data when filters change:

```python
@app.page("/")
def overview():
    return cc.Dashboard(
        filters=[
            cc.Filter("region", label="Region", type="select",
                      options=["All", "North", "South", "East", "West"]),
        ],
        charts=[
            cc.Bar(
                data_fn=lambda filters={}: db.query_dict(
                    "SELECT month, revenue FROM sales WHERE region = :region",
                    params={"region": filters.get("region", "All")}
                ) if filters.get("region", "All") != "All" else
                    db.query_dict("SELECT month, SUM(revenue) revenue FROM sales GROUP BY month"),
                x="month", y="revenue",
                title="Sales by Month",
                linked_filters=["region"],    # Re-fetches when "region" filter changes
            ),
        ],
    )
```

See [Filters & Interactivity](filters-and-interactivity.md) for full details.

---

## Connection String Reference

| Database | Connection String Format |
|----------|------------------------|
| SQLite | `sqlite:///path/to/file.db` |
| SQLite (memory) | `sqlite:///:memory:` |
| PostgreSQL | `postgresql://user:pass@host:5432/db` |
| MySQL | `mysql+pymysql://user:pass@host:3306/db` |
| SQL Server | `mssql+pyodbc://user:pass@host/db` |
| CSV file | `/path/to/file.csv` |
| CSV directory | `/path/to/data/` |
| REST API | `https://api.example.com` (base URL) |

---

## SQL Query Builder (Visual Builder)

In the visual builder at `/builder`, each chart has a **Data** tab with:

- **Connection** dropdown — select a registered connector
- **SQL editor** — write queries with syntax highlighting
- **Run** button — preview query results (first 500 rows)
- **Schema browser** — browse tables and columns from the connected DB
- **Column mapper** — point x/y axes to query columns

Registered connectors are saved to `chartcraft/builder/connectors.json` and persist between sessions.

To register a connector programmatically (available in the builder):

```python
# POST to /api/connections
import requests
requests.post("http://localhost:8050/api/connections", json={
    "name": "Production DB",
    "conn_str": "postgresql://user:pass@prod-host/analytics",
})
```

Or add it directly through the builder UI — click the **+** button in the connection dropdown.
