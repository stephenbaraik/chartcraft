# Export & Deployment

ChartCraft dashboards can be exported as standalone HTML files, Jupyter notebooks, Docker projects, and PDFs — or served live from any Python-capable machine.

---

## Static HTML Export

Export a dashboard as a self-contained HTML file with no server required. Share it via email, upload to S3, or embed in a web page.

### Single Page

```python
app.save("dashboard.html")                          # Export "/" (home page)
app.save("sales.html", page="/sales")               # Export a specific page
app.save("report.html", page="/", theme="frost")    # Override theme
```

The generated HTML embeds ECharts from CDN and all dashboard data inline. It works offline once loaded.

### All Pages

Export every registered page into a directory:

```python
# Creates: output/index.html, output/sales.html, output/customers.html
paths = app.save_all("output/")
print(paths)
# → ['output/index.html', 'output/sales.html', 'output/customers.html']
```

Page path mapping:
- `/` → `index.html`
- `/sales` → `sales.html`
- `/admin/users` → `admin_users.html`

### HTML String

Get the HTML as a string without writing a file:

```python
html = app.to_html(page="/", theme="frost")
# Use html however you want — send as email body, write to S3, etc.
```

### Quick Dashboard (no App needed)

For one-off reports:

```python
cc.quick_dashboard(
    title="Weekly Report",
    charts=[
        cc.Bar({"Q1": 100, "Q2": 200}, title="Revenue"),
        cc.Donut({"Enterprise": 60, "Free": 40}, title="Plans"),
    ],
    theme="frost",
    save_path="report.html",
)
```

---

## PDF Export

Export a dashboard as a PDF via headless Chromium (Playwright).

**Install:**
```bash
pip install "chartcraft[pdf]"
playwright install chromium
```

### Server-Side PDF

```bash
GET http://localhost:8050/api/export/pdf?page=/
```

Or from the viewer: click the **PDF** button in the top-right nav bar.

The PDF uses the print CSS media query — charts are rendered full-width, the nav bar is hidden, and all backgrounds are included.

### Programmatic PDF

```python
import requests

response = requests.get("http://localhost:8050/api/export/pdf?page=/sales")
with open("sales_report.pdf", "wb") as f:
    f.write(response.content)
```

### Without Playwright (Browser Print)

If Playwright is not installed, the API returns:

```json
{
  "fallback": "print",
  "message": "Install playwright for PDF: pip install playwright && playwright install chromium"
}
```

In this case, use the browser's native print dialog (`Ctrl+P`). The dashboard has print CSS that hides the nav bar and formats charts for paper.

---

## Jupyter Notebook Export

Export the current dashboard as a runnable `.ipynb` notebook.

### From the Builder

Click **Export → Jupyter Notebook (.ipynb)**.

### Via API

```bash
POST http://localhost:8050/api/export/notebook
Content-Type: application/json

{ "title": "Sales Dashboard", "pages": [...] }
```

The downloaded notebook contains three cells:

```python
# Cell 1: Install
# pip install chartcraft

# Cell 2: Dashboard code (full, runnable Python)
import chartcraft as cc
app = cc.App("Sales Dashboard", theme="midnight")

@app.page("/")
def home():
    return cc.Dashboard(...)

# Cell 3: Run
app.run()
```

---

## Docker Export

Package the dashboard as a production-ready Docker project.

### From the Builder

Click **Export → Docker Project (.zip)**.

### Via API

```bash
POST http://localhost:8050/api/export/docker
Content-Type: application/json

{ "title": "My Dashboard" }
```

The downloaded `.zip` contains:

```
my_dashboard/
├── app.py               # Dashboard Python code
├── Dockerfile           # Python 3.12-slim
├── docker-compose.yml   # Single-service setup
└── README.md            # Deployment instructions
```

### Dockerfile

```dockerfile
FROM python:3.12-slim
WORKDIR /app
COPY . .
RUN pip install chartcraft
EXPOSE 8050
CMD ["python", "app.py"]
```

### Deploy

```bash
unzip my_dashboard_docker.zip
cd my_dashboard
docker-compose up -d
# → http://localhost:8050
```

### Production with database:

```dockerfile
FROM python:3.12-slim
WORKDIR /app
COPY . .
RUN pip install "chartcraft[pg]"     # Add your database driver
EXPOSE 8050
CMD ["python", "app.py"]
```

---

## Live Server Deployment

### Basic: Run directly

```python
app.run(host="0.0.0.0", port=8050)
```

Access from any machine on the network at `http://your-ip:8050`.

### With Authentication

```python
# HTTP Basic Auth (username: admin)
app.run(password="my-secure-password")

# Bearer token
app.run(token="my-secret-token")
```

With Bearer token, clients can authenticate via:
- URL: `http://localhost:8050/?token=my-secret-token`
- Header: `Authorization: Bearer my-secret-token`

See [Authentication](authentication.md) for details.

### Behind a Reverse Proxy (nginx)

```nginx
server {
    listen 80;
    server_name charts.example.com;

    location / {
        proxy_pass http://127.0.0.1:8050;
        proxy_http_version 1.1;
        proxy_set_header Connection "";           # Required for SSE
        proxy_buffering off;                      # Required for SSE
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
    }
}
```

**Important for SSE (real-time):** `proxy_buffering off` is required. Without it, real-time updates won't reach the browser.

### As a systemd Service

```ini
[Unit]
Description=ChartCraft Dashboard
After=network.target

[Service]
User=www-data
WorkingDirectory=/opt/dashboard
ExecStart=/usr/bin/python3 app.py
Restart=always
RestartSec=10

[Install]
WantedBy=multi-user.target
```

```bash
sudo systemctl enable chartcraft
sudo systemctl start chartcraft
```

---

## Cloud Deployment

### Railway / Render / Fly.io

Create `app.py`:
```python
import os
app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 8050)))
```

`Procfile`:
```
web: python app.py
```

### AWS EC2 / DigitalOcean Droplet

```bash
pip install chartcraft
python app.py &    # Or use systemd (above)
```

Open port 8050 in your security group / firewall.

### Google Cloud Run / AWS Fargate

Use the Docker export and push the image:

```bash
docker build -t my-dashboard .
docker tag my-dashboard gcr.io/my-project/my-dashboard
docker push gcr.io/my-project/my-dashboard
gcloud run deploy --image gcr.io/my-project/my-dashboard --port 8050
```

---

## Environment Variables

```python
import os

app.run(
    host=os.getenv("HOST", "0.0.0.0"),
    port=int(os.getenv("PORT", "8050")),
    password=os.getenv("DASHBOARD_PASSWORD"),
    token=os.getenv("DASHBOARD_TOKEN"),
)
```

Store secrets in `.env` (never commit to git):

```bash
DASHBOARD_PASSWORD=my-secure-password
DATABASE_URL=postgresql://user:pass@host/db
```

---

## Static Export vs Live Server

| | Static HTML | Live Server |
|--|-------------|-------------|
| Dependencies at runtime | None | Python + chartcraft |
| Real-time data | No | Yes (`refresh=N`) |
| Filters | No | Yes |
| Multi-page nav | No (separate files) | Yes |
| Share | Email / S3 / any host | Requires server |
| Best for | Reports, snapshots, archiving | Interactive dashboards, live ops |
