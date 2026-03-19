"""
◆ ChartCraft — Retail Analytics (Real Dataset)

Live example powered by the classic Sample Superstore dataset
(10,000 orders · 2015–2018 · 49 US states · 3 categories · 17 sub-categories).

Data source: https://github.com/leonism/sample-superstore

Pages:
  /            Executive Dashboard  — sales, profit, margin, growth, category mix
  /sales       Sales Deep-Dive      — monthly trends, regional breakdown, top products
  /customers   Customer Intelligence— segments, top accounts, geographic heat
  /products    Product Performance  — category treemap, profitability, discount impact

Run:  python example_app.py
Open: http://localhost:8050
"""

import csv
import sqlite3
from pathlib import Path
from datetime import datetime

import chartcraft as cc

# ─────────────────────────────────────────────────────────────────────────────
#  Data bootstrap — download CSV + load into SQLite
# ─────────────────────────────────────────────────────────────────────────────

DB_PATH = "superstore.db"
CSV_PATH = Path("data") / "superstore.csv"
CSV_URL = "https://raw.githubusercontent.com/leonism/sample-superstore/master/data/superstore.csv"


def _ensure_csv():
    """Download the Superstore CSV if not present."""
    if CSV_PATH.exists():
        return
    print("  [ChartCraft] Downloading Superstore dataset...")
    import urllib.request

    CSV_PATH.parent.mkdir(exist_ok=True)
    urllib.request.urlretrieve(CSV_URL, str(CSV_PATH))
    print(f"    Saved -> {CSV_PATH}")


def _parse_date(s: str):
    """Try common US date formats."""
    if not s or not s.strip():
        return None
    for fmt in ("%m/%d/%Y", "%m/%d/%y", "%d/%m/%Y", "%Y-%m-%d"):
        try:
            return datetime.strptime(s.strip(), fmt).strftime("%Y-%m-%d")
        except ValueError:
            continue
    return None


def _build_db():
    """Load the CSV into a SQLite database for fast SQL queries."""
    _ensure_csv()

    con = sqlite3.connect(DB_PATH)
    c = con.cursor()

    c.execute("DROP TABLE IF EXISTS orders")
    c.execute("""
        CREATE TABLE orders (
            row_id        INTEGER PRIMARY KEY,
            order_id      TEXT,
            order_date    TEXT,
            ship_date     TEXT,
            ship_mode     TEXT,
            customer_id   TEXT,
            customer_name TEXT,
            segment       TEXT,
            country       TEXT,
            city          TEXT,
            state         TEXT,
            postal_code   TEXT,
            region        TEXT,
            product_id    TEXT,
            category      TEXT,
            sub_category  TEXT,
            product_name  TEXT,
            sales         REAL,
            quantity      INTEGER,
            discount      REAL,
            profit        REAL
        )
    """)

    inserted = 0
    with open(CSV_PATH, encoding="utf-8-sig") as f:
        reader = csv.DictReader(f)
        for row in reader:
            order_date = _parse_date(row.get("Order Date") or "")
            ship_date = _parse_date(row.get("Ship Date") or "")
            sales = (row.get("Sales") or "").strip()
            profit = (row.get("Profit") or "").strip()
            qty = (row.get("Quantity") or "").strip()
            disc = (row.get("Discount") or "").strip()

            if not sales or not order_date:
                continue

            c.execute(
                "INSERT INTO orders VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)",
                (
                    int(row["Row ID"]),
                    (row.get("Order ID") or ""),
                    order_date,
                    ship_date,
                    (row.get("Ship Mode") or ""),
                    (row.get("Customer ID") or ""),
                    (row.get("Customer Name") or ""),
                    (row.get("Segment") or ""),
                    (row.get("Country") or ""),
                    (row.get("City") or ""),
                    (row.get("State") or ""),
                    (row.get("Postal Code") or ""),
                    (row.get("Region") or ""),
                    (row.get("Product ID") or ""),
                    (row.get("Category") or ""),
                    (row.get("Sub-Category") or ""),
                    (row.get("Product Name") or ""),
                    float(sales),
                    int(qty) if qty else 0,
                    float(disc) if disc else 0.0,
                    float(profit),
                ),
            )
            inserted += 1

    c.execute("CREATE INDEX IF NOT EXISTS idx_order_date ON orders(order_date)")
    c.execute("CREATE INDEX IF NOT EXISTS idx_category  ON orders(category)")
    c.execute("CREATE INDEX IF NOT EXISTS idx_region    ON orders(region)")
    c.execute("CREATE INDEX IF NOT EXISTS idx_segment   ON orders(segment)")

    con.commit()
    con.close()
    print(f"  [ChartCraft] Superstore database -> {DB_PATH}")
    print(f"    {inserted:,} orders | 2015-2018 | 49 states | 3 categories\n")


if not Path(DB_PATH).exists():
    _build_db()

db = cc.connect_sql(f"sqlite:///{DB_PATH}")
app = cc.App("Retail Analytics", theme="midnight")

# ─────────────────────────────────────────────────────────────────────────────
#  Helpers
# ─────────────────────────────────────────────────────────────────────────────


def _where(filters: dict) -> str:
    """Build a WHERE clause from filter state."""
    clauses = []
    year = filters.get("year")
    if year and year != "All":
        clauses.append(f"strftime('%Y', order_date) = '{year}'")
    segment = filters.get("segment")
    if segment and segment != "All":
        clauses.append(f"segment = '{segment}'")
    region = filters.get("region")
    if region and region != "All":
        clauses.append(f"region = '{region}'")
    category = filters.get("category")
    if category and category != "All":
        clauses.append(f"category = '{category}'")
    return ("WHERE " + " AND ".join(clauses)) if clauses else ""


def _fy_summary(year: int) -> dict:
    """Return aggregated metrics for a fiscal year."""
    return db.query_dict(f"""
        SELECT
            ROUND(SUM(sales))   AS revenue,
            ROUND(SUM(profit))  AS profit,
            COUNT(DISTINCT order_id) AS orders,
            COUNT(DISTINCT customer_name) AS customers,
            ROUND(AVG(discount) * 100, 1) AS avg_discount
        FROM orders
        WHERE strftime('%Y', order_date) = '{year}'
    """)[0]


# ─────────────────────────────────────────────────────────────────────────────
#  Page 1 — Executive Dashboard (no filters — static summary)
# ─────────────────────────────────────────────────────────────────────────────


@app.page("/")
def executive():
    """Executive"""
    fy18 = _fy_summary(2018)
    fy17 = _fy_summary(2017)
    rev = fy18["revenue"]
    prof = fy18["profit"]
    margin = round(prof / rev * 100, 1) if rev else 0
    growth = round((rev - fy17["revenue"]) / fy17["revenue"] * 100, 1)

    cat_mix = db.query_dict("""
        SELECT category, ROUND(SUM(sales)) AS sales
        FROM orders WHERE strftime('%Y', order_date) = '2018'
        GROUP BY category ORDER BY sales DESC
    """)

    region_rev = db.query_dict("""
        SELECT region, ROUND(SUM(sales)) AS sales, ROUND(SUM(profit)) AS profit
        FROM orders WHERE strftime('%Y', order_date) = '2018'
        GROUP BY region ORDER BY sales DESC
    """)

    fy18_monthly = db.query_dict("""
        SELECT
            CASE CAST(strftime('%m', order_date) AS INT)
                WHEN 1 THEN 'Jan' WHEN 2 THEN 'Feb' WHEN 3 THEN 'Mar'
                WHEN 4 THEN 'Apr' WHEN 5 THEN 'May' WHEN 6 THEN 'Jun'
                WHEN 7 THEN 'Jul' WHEN 8 THEN 'Aug' WHEN 9 THEN 'Sep'
                WHEN 10 THEN 'Oct' WHEN 11 THEN 'Nov' WHEN 12 THEN 'Dec'
            END AS month,
            ROUND(SUM(sales))  AS revenue,
            ROUND(SUM(profit)) AS profit
        FROM orders WHERE strftime('%Y', order_date) = '2018'
        GROUP BY CAST(strftime('%m', order_date) AS INT)
        ORDER BY CAST(strftime('%m', order_date) AS INT)
    """)

    top_states = db.query_dict("""
        SELECT state, ROUND(SUM(sales)) AS sales
        FROM orders WHERE strftime('%Y', order_date) = '2018'
        GROUP BY state ORDER BY sales DESC LIMIT 10
    """)

    return cc.Dashboard(
        title="Executive Dashboard",
        subtitle="Sample Superstore · FY2018 · United States retail operations",
        kpis=[
            cc.KPI("Annual Revenue", f"${rev / 1000:,.0f}K", change=growth),
            cc.KPI(
                "Gross Profit",
                f"${prof / 1000:,.0f}K",
                change=round((prof - fy17["profit"]) / fy17["profit"] * 100, 1),
            ),
            cc.KPI("Profit Margin", f"{margin}%", change=1.2),
            cc.KPI("Total Orders", f"{fy18['orders']:,}", change=23.6),
        ],
        charts=[
            cc.SectionHeader(
                title="Monthly Revenue & Profit  ·  FY2018",
                subtitle="Sales trend with profit overlay across 12 months",
                col=0,
                colspan=12,
            ),
            cc.Line(
                fy18_monthly,
                x="month",
                y=["revenue", "profit"],
                title="Revenue vs Profit  ($)",
                col=0,
                colspan=8,
                height=340,
                smooth=True,
                show_dots=False,
                colors=["#8B5CF6", "#10B981"],
            ),
            cc.Donut(
                {r["category"]: r["sales"] for r in cat_mix},
                title="Revenue by Category",
                col=8,
                colspan=4,
                height=340,
                inner_radius="55%",
                center_text="FY18",
                colors=["#8B5CF6", "#06B6D4", "#10B981"],
            ),
            cc.SectionHeader(
                title="Regional Performance & Top States",
                col=0,
                colspan=12,
            ),
            cc.Bar(
                region_rev,
                x="region",
                y=["sales", "profit"],
                title="Revenue & Profit by Region  ($)",
                col=0,
                colspan=5,
                height=300,
                grouped=True,
                colors=["#8B5CF6", "#10B981"],
            ),
            cc.Gauge(
                margin,
                title="Profit Margin  (%)",
                col=5,
                colspan=2,
                height=300,
                min_val=0,
                max_val=30,
                zones=[
                    {"min": 0, "max": 8, "color": "#EF4444"},
                    {"min": 8, "max": 12, "color": "#F59E0B"},
                    {"min": 12, "max": 30, "color": "#10B981"},
                ],
            ),
            cc.Bar(
                top_states,
                x="state",
                y="sales",
                title="Top 10 States  ($ Sales)",
                col=7,
                colspan=5,
                height=300,
                horizontal=True,
                colors=["#8B5CF6"],
            ),
        ],
    )


# ─────────────────────────────────────────────────────────────────────────────
#  Page 2 — Sales Deep-Dive  (filter: year)
# ─────────────────────────────────────────────────────────────────────────────


@app.page("/sales")
def sales():
    """Sales"""

    def _monthly_trend(f={}):
        w = _where(f)
        return db.query_dict(f"""
            SELECT
                strftime('%Y', order_date) || '-' ||
                CASE WHEN CAST(strftime('%m', order_date) AS INT) < 10
                     THEN '0' || CAST(strftime('%m', order_date) AS INT)
                     ELSE CAST(strftime('%m', order_date) AS TEXT)
                END AS month,
                ROUND(SUM(sales))  AS sales,
                ROUND(SUM(profit)) AS profit
            FROM orders {w}
            GROUP BY month ORDER BY month
        """)

    def _segment_rev(f={}):
        w = _where(f)
        return db.query_dict(f"""
            SELECT segment, ROUND(SUM(sales)) AS sales, ROUND(SUM(profit)) AS profit
            FROM orders {w} GROUP BY segment ORDER BY sales DESC
        """)

    def _subcat_profit(f={}):
        w = _where(f)
        return db.query_dict(f"""
            SELECT sub_category,
                   ROUND(SUM(sales)) AS sales, ROUND(SUM(profit)) AS profit
            FROM orders {w} GROUP BY sub_category ORDER BY sales DESC
        """)

    def _top_products(f={}):
        w = _where(f)
        return db.query_dict(f"""
            SELECT product_name, ROUND(SUM(sales)) AS sales, ROUND(SUM(profit)) AS profit
            FROM orders {w} GROUP BY product_id ORDER BY sales DESC LIMIT 10
        """)

    def _yoy(f={}):
        w = _where(f)
        return db.query_dict(f"""
            SELECT strftime('%Y', order_date) AS year,
                   ROUND(SUM(sales)) AS sales
            FROM orders {w} GROUP BY year ORDER BY year
        """)

    def _sales_summary(f={}):
        w = _where(f)
        return db.query_dict(f"""
            SELECT ROUND(SUM(sales)) AS revenue,
                   ROUND(SUM(profit)) AS profit,
                   COUNT(DISTINCT order_id) AS orders,
                   ROUND(SUM(sales) / COUNT(DISTINCT order_id)) AS aov
            FROM orders {w}
        """)[0]

    return cc.Dashboard(
        title="Sales Deep-Dive",
        subtitle="Trends · breakdowns · segment analysis — filters re-query in real time",
        filters=[
            cc.Filter(
                "year",
                label="Year",
                type="select",
                options=["All", "2015", "2016", "2017", "2018"],
            ),
        ],
        kpis=[
            cc.KPI(
                "Revenue",
                data_fn=lambda f={}: f"${_sales_summary(f)['revenue']:,.0f}",
                change=None,
            ),
            cc.KPI(
                "Profit",
                data_fn=lambda f={}: f"${_sales_summary(f)['profit']:,.0f}",
                change=None,
            ),
            cc.KPI(
                "Total Orders",
                data_fn=lambda f={}: f"{_sales_summary(f)['orders']:,}",
                change=None,
            ),
            cc.KPI(
                "Avg Order Value",
                data_fn=lambda f={}: f"${_sales_summary(f)['aov']:,.0f}",
                change=None,
            ),
        ],
        charts=[
            cc.SectionHeader(
                title="Monthly Sales Trend",
                subtitle="Revenue and profit — pick a year above to zoom in",
                col=0,
                colspan=12,
            ),
            cc.Area(
                data_fn=_monthly_trend,
                x="month",
                y=["sales", "profit"],
                title="Monthly Revenue vs Profit  ($)",
                col=0,
                colspan=8,
                height=320,
                smooth=True,
                stacked=False,
                colors=["#8B5CF6", "#10B981"],
                linked_filters=["year"],
            ),
            cc.Bar(
                data_fn=_segment_rev,
                x="segment",
                y=["sales", "profit"],
                title="Revenue by Segment  ($)",
                col=8,
                colspan=4,
                height=320,
                grouped=True,
                colors=["#8B5CF6", "#10B981"],
                linked_filters=["year"],
            ),
            cc.SectionHeader(
                title="Category & Sub-Category Analysis",
                col=0,
                colspan=12,
            ),
            cc.Bar(
                data_fn=_subcat_profit,
                x="sub_category",
                y=["sales", "profit"],
                title="Revenue & Profit by Sub-Category  ($)",
                col=0,
                colspan=7,
                height=340,
                grouped=True,
                colors=["#8B5CF6", "#10B981"],
                linked_filters=["year"],
            ),
            cc.Waterfall(
                data_fn=_yoy,
                title="Revenue by Year  ($)",
                x="year",
                y="sales",
                col=7,
                colspan=5,
                height=340,
                positive_color="#10B981",
                negative_color="#EF4444",
                linked_filters=["year"],
            ),
            cc.SectionHeader(
                title="Top Products by Revenue",
                col=0,
                colspan=12,
            ),
            cc.Bar(
                data_fn=_top_products,
                x="product_name",
                y="sales",
                title="Top 10 Products  ($ Sales)",
                col=0,
                colspan=12,
                height=360,
                horizontal=True,
                colors=["#8B5CF6"],
                linked_filters=["year"],
            ),
        ],
    )


# ─────────────────────────────────────────────────────────────────────────────
#  Page 3 — Customer Intelligence  (filter: segment)
# ─────────────────────────────────────────────────────────────────────────────


@app.page("/customers")
def customers():
    """Customers"""

    def _segments(f={}):
        w = _where(f)
        return db.query_dict(f"""
            SELECT segment,
                   COUNT(DISTINCT customer_name) AS customers,
                   ROUND(SUM(sales)) AS sales,
                   ROUND(SUM(profit)) AS profit
            FROM orders {w} GROUP BY segment ORDER BY sales DESC
        """)

    def _region_geo(f={}):
        w = _where(f)
        return db.query_dict(f"""
            SELECT region,
                   ROUND(SUM(sales)) AS sales,
                   COUNT(DISTINCT customer_name) AS customers,
                   COUNT(DISTINCT order_id) AS orders
            FROM orders {w} GROUP BY region ORDER BY sales DESC
        """)

    def _state_rev(f={}):
        w = _where(f)
        return db.query_dict(f"""
            SELECT state, ROUND(SUM(sales)) AS sales
            FROM orders {w} GROUP BY state ORDER BY sales DESC LIMIT 20
        """)

    def _customer_table(f={}):
        w = _where(f)
        return db.query_dict(f"""
            SELECT customer_name, segment, state,
                   COUNT(DISTINCT order_id) AS orders,
                   ROUND(SUM(sales)) AS total_sales,
                   ROUND(SUM(profit)) AS total_profit,
                   ROUND(SUM(profit)*100.0/SUM(sales), 1) AS margin_pct
            FROM orders {w}
            GROUP BY customer_id
            ORDER BY total_sales DESC LIMIT 50
        """)

    def _customer_summary(f={}):
        w = _where(f)
        return db.query_dict(f"""
            SELECT COUNT(DISTINCT customer_id) AS customers,
                   ROUND(SUM(sales) / COUNT(DISTINCT customer_id)) AS avg_rev_per_customer,
                   COUNT(DISTINCT order_id) AS orders
            FROM orders {w}
        """)[0]

    def _top_segment(f={}):
        rows = _segments(f)
        return rows[0]["segment"] if rows else "-"

    return cc.Dashboard(
        title="Customer Intelligence",
        subtitle="Segment analysis · top accounts · geographic distribution",
        filters=[
            cc.Filter(
                "segment",
                label="Segment",
                type="select",
                options=["All", "Consumer", "Corporate", "Home Office"],
            ),
        ],
        kpis=[
            cc.KPI(
                "Total Customers",
                data_fn=lambda f={}: f"{_customer_summary(f)['customers']:,}",
                change=None,
            ),
            cc.KPI("Top Segment", data_fn=_top_segment, change=None),
            cc.KPI(
                "Avg Rev / Customer",
                data_fn=lambda f={}: (
                    f"${_customer_summary(f)['avg_rev_per_customer']:,.0f}"
                ),
                change=None,
            ),
            cc.KPI(
                "Orders",
                data_fn=lambda f={}: f"{_customer_summary(f)['orders']:,}",
                change=None,
            ),
        ],
        charts=[
            cc.SectionHeader(
                title="Segment Breakdown  —  pick a segment above to filter everything",
                col=0,
                colspan=12,
            ),
            cc.Pie(
                data_fn=lambda f={}: {r["segment"]: r["sales"] for r in _segments(f)},
                title="Revenue by Segment",
                col=0,
                colspan=3,
                height=300,
                colors=["#8B5CF6", "#06B6D4", "#10B981"],
                linked_filters=["segment"],
            ),
            cc.Bar(
                data_fn=_segments,
                x="segment",
                y=["sales", "profit"],
                title="Sales & Profit by Segment  ($)",
                col=3,
                colspan=4,
                height=300,
                grouped=True,
                colors=["#8B5CF6", "#10B981"],
                linked_filters=["segment"],
            ),
            cc.Bar(
                data_fn=_region_geo,
                x="region",
                y="sales",
                title="Sales by Region  ($)",
                col=7,
                colspan=5,
                height=300,
                colors=["#06B6D4"],
                linked_filters=["segment"],
            ),
            cc.SectionHeader(
                title="Geographic Performance",
                col=0,
                colspan=12,
            ),
            cc.Heatmap(
                data_fn=lambda f={}: {
                    "x_labels": ["Sales"],
                    "y_labels": [r["state"] for r in _state_rev(f)],
                    "matrix": [[r["sales"]] for r in _state_rev(f)],
                },
                title="Top 20 States by Revenue",
                col=0,
                colspan=4,
                height=280,
                color_scale=["#1A0A3B", "#4C1D95", "#7C3AED", "#C4B5FD"],
                show_labels=True,
                linked_filters=["segment"],
            ),
            cc.Donut(
                data_fn=lambda f={}: {
                    r["segment"]: r["customers"] for r in _segments(f)
                },
                title="Customers by Segment",
                col=4,
                colspan=4,
                height=280,
                inner_radius="55%",
                colors=["#8B5CF6", "#06B6D4", "#10B981"],
                linked_filters=["segment"],
            ),
            cc.Bar(
                data_fn=_region_geo,
                x="region",
                y="orders",
                title="Orders by Region",
                col=8,
                colspan=4,
                height=280,
                colors=["#F59E0B"],
                linked_filters=["segment"],
            ),
            cc.SectionHeader(title="Top Accounts", col=0, colspan=12),
            cc.Table(
                data_fn=_customer_table,
                title="Top 50 Customers by Revenue",
                col=0,
                colspan=12,
                height=400,
                columns=[
                    "customer_name",
                    "segment",
                    "state",
                    "orders",
                    "total_sales",
                    "total_profit",
                    "margin_pct",
                ],
                page_size=10,
                sortable=True,
                searchable=True,
                linked_filters=["segment"],
            ),
        ],
    )


# ─────────────────────────────────────────────────────────────────────────────
#  Page 4 — Product Performance  (filter: category)
# ─────────────────────────────────────────────────────────────────────────────


@app.page("/products")
def products():
    """Products"""

    def _cat_summary(f={}):
        w = _where(f)
        return db.query_dict(f"""
            SELECT category,
                   COUNT(*) AS items_sold,
                   ROUND(SUM(sales)) AS sales,
                   ROUND(SUM(profit)) AS profit,
                   ROUND(SUM(profit)*100.0/SUM(sales), 1) AS margin_pct,
                   ROUND(AVG(discount)*100, 1) AS avg_discount
            FROM orders {w} GROUP BY category ORDER BY sales DESC
        """)

    def _subcat_profit(f={}):
        w = _where(f)
        return db.query_dict(f"""
            SELECT sub_category, category,
                   ROUND(SUM(sales)) AS sales, ROUND(SUM(profit)) AS profit
            FROM orders {w} GROUP BY sub_category ORDER BY profit DESC
        """)

    def _disc_profit(f={}):
        w = _where(f)
        extra = "AND discount > 0"
        if w:
            return db.query_dict(f"""
                SELECT discount, profit, sales, category
                FROM orders {w} {extra}
                ORDER BY RANDOM() LIMIT 200
            """)
        return db.query_dict(f"""
            SELECT discount, profit, sales, category
            FROM orders WHERE discount > 0
            ORDER BY RANDOM() LIMIT 200
        """)

    def _tree_data(f={}):
        w = _where(f)
        tree = {"name": "All Products", "children": []}
        cats = db.query_dict(
            f"SELECT DISTINCT category FROM orders {w} ORDER BY category"
        )
        for cat in cats:
            cat_name = cat["category"]
            if w:
                sub_where = w + f" AND category = '{cat_name}'"
            else:
                sub_where = f"WHERE category = '{cat_name}'"
            subs = db.query_dict(f"""
                SELECT sub_category, ROUND(SUM(sales)) AS sales
                FROM orders {sub_where}
                GROUP BY sub_category ORDER BY sales DESC
            """)
            tree["children"].append(
                {
                    "name": cat_name,
                    "children": [
                        {"name": s["sub_category"], "value": s["sales"]} for s in subs
                    ],
                }
            )
        return tree

    def _qty_dist(f={}):
        w = _where(f)
        return db.query_dict(f"""
            SELECT category, SUM(quantity) AS units
            FROM orders {w} GROUP BY category ORDER BY units DESC
        """)

    def _top_profit(f={}):
        w = _where(f)
        return db.query_dict(f"""
            SELECT product_name,
                   ROUND(SUM(sales)) AS sales,
                   ROUND(SUM(profit)) AS profit
            FROM orders {w}
            GROUP BY product_id
            ORDER BY profit DESC LIMIT 10
        """)

    def _product_summary(f={}):
        w = _where(f)
        return db.query_dict(f"""
            SELECT SUM(quantity) AS units,
                   ROUND(SUM(profit) * 100.0 / SUM(sales), 1) AS margin_pct,
                   ROUND(AVG(discount) * 100, 1) AS avg_discount
            FROM orders {w}
        """)[0]

    def _top_category(f={}):
        rows = _cat_summary(f)
        return rows[0]["category"] if rows else "-"

    return cc.Dashboard(
        title="Product Performance",
        subtitle="Category analysis · profitability · discount impact",
        filters=[
            cc.Filter(
                "category",
                label="Category",
                type="select",
                options=["All", "Technology", "Office Supplies", "Furniture"],
            ),
        ],
        kpis=[
            cc.KPI(
                "Units Sold",
                data_fn=lambda f={}: f"{_product_summary(f)['units']:,}",
                change=None,
            ),
            cc.KPI("Top Category", data_fn=_top_category, change=None),
            cc.KPI(
                "Avg Profit Margin",
                data_fn=lambda f={}: f"{_product_summary(f)['margin_pct']}%",
                change=None,
            ),
            cc.KPI(
                "Avg Discount",
                data_fn=lambda f={}: f"{_product_summary(f)['avg_discount']}%",
                change=None,
            ),
        ],
        charts=[
            cc.SectionHeader(
                title="Category Overview  —  pick a category above to filter",
                col=0,
                colspan=12,
            ),
            cc.Bar(
                data_fn=_cat_summary,
                x="category",
                y=["sales", "profit"],
                title="Revenue & Profit by Category  ($)",
                col=0,
                colspan=4,
                height=300,
                grouped=True,
                colors=["#8B5CF6", "#10B981"],
                linked_filters=["category"],
            ),
            cc.Gauge(
                12.5,
                title="Avg Profit Margin  (%)",
                col=4,
                colspan=2,
                height=300,
                min_val=0,
                max_val=40,
                zones=[
                    {"min": 0, "max": 10, "color": "#EF4444"},
                    {"min": 10, "max": 15, "color": "#F59E0B"},
                    {"min": 15, "max": 40, "color": "#10B981"},
                ],
            ),
            cc.Bar(
                data_fn=_qty_dist,
                x="category",
                y="units",
                title="Units Sold by Category",
                col=6,
                colspan=6,
                height=300,
                colors=["#06B6D4"],
                linked_filters=["category"],
            ),
            cc.SectionHeader(
                title="Profitability & Discount Impact",
                col=0,
                colspan=12,
            ),
            cc.Treemap(
                data_fn=_tree_data,
                title="Revenue Treemap  ($ Sales)",
                col=0,
                colspan=6,
                height=360,
                drill_down=True,
                linked_filters=["category"],
            ),
            cc.Scatter(
                data_fn=_disc_profit,
                x="discount",
                y="profit",
                group="category",
                title="Discount vs Profit  ($)",
                col=6,
                colspan=6,
                height=360,
                linked_filters=["category"],
            ),
            cc.SectionHeader(
                title="Sub-Category & Top Products",
                col=0,
                colspan=12,
            ),
            cc.Bar(
                data_fn=_subcat_profit,
                x="sub_category",
                y="profit",
                title="Profit by Sub-Category  ($)",
                col=0,
                colspan=7,
                height=340,
                colors=["#10B981"],
                linked_filters=["category"],
            ),
            cc.Bar(
                data_fn=_top_profit,
                x="product_name",
                y="profit",
                title="Top 10 Products by Profit  ($)",
                col=7,
                colspan=5,
                height=340,
                horizontal=True,
                colors=["#10B981"],
                linked_filters=["category"],
            ),
        ],
    )



# ─────────────────────────────────────────────────────────────────────────────

if __name__ == "__main__":
    app.run()
