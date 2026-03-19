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

    return cc.Page(
        title="Executive Dashboard",
        subtitle="Sample Superstore · FY2018 · United States retail operations",
        kpis=[
            cc.stat("Annual Revenue", f"${rev / 1000:,.0f}K", change=growth),
            cc.stat(
                "Gross Profit",
                f"${prof / 1000:,.0f}K",
                change=round((prof - fy17["profit"]) / fy17["profit"] * 100, 1),
            ),
            cc.stat("Profit Margin", f"{margin}%", change=1.2),
            cc.stat("Total Orders", f"{fy18['orders']:,}", change=23.6),
        ],
        content=[
            cc.section(
                "Momentum & Mix",
                cc.trend_line(
                    fy18_monthly,
                    x="month",
                    y=["revenue", "profit"],
                    title="Revenue vs Profit  ($)",
                    col=0,
                    colspan=8,
                    height=340,
                    colors=["#60A5FA", "#FB7185"],
                ),
                cc.spotlight_donut(
                    {r["category"]: r["sales"] for r in cat_mix},
                    title="Revenue by Category",
                    col=8,
                    colspan=4,
                    height=340,
                    center_text="Mix",
                    colors=["#8B5CF6", "#14B8A6", "#F59E0B"],
                ),
                subtitle="A cleaner look at the sales engine behind FY2018 performance",
            ),
            cc.note(
                "West leads the business in both volume and contribution, while Furniture still lags the broader margin profile.",
                col=0,
                colspan=12,
            ),
            cc.section(
                "Regional Performance & Top States",
                cc.comparison_bars(
                    region_rev,
                    x="region",
                    y=["sales", "profit"],
                    title="Revenue & Profit by Region  ($)",
                    col=0,
                    colspan=5,
                    height=300,
                    colors=["#22C55E", "#F59E0B"],
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
                cc.ranked_bars(
                    top_states,
                    x="state",
                    y="sales",
                    title="Top 10 States  ($ Sales)",
                    col=7,
                    colspan=5,
                    height=300,
                    colors=["#0EA5E9"],
                ),
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

    return cc.Page(
        title="Sales Deep-Dive",
        subtitle="Trends · mix shifts · top movers — tuned for narrative analysis",
        filters=[
            cc.Filter(
                "year",
                label="Year",
                type="select",
                options=["All", "2015", "2016", "2017", "2018"],
            ),
        ],
        kpis=[
            cc.sql_kpi(
                "Revenue",
                db,
                lambda f: (
                    f"SELECT ROUND(SUM(sales)) AS revenue FROM orders {_where(f)}"
                ),
                field="revenue",
                formatter=lambda v, _f: f"${v:,.0f}",
            ),
            cc.sql_kpi(
                "Profit",
                db,
                lambda f: (
                    f"SELECT ROUND(SUM(profit)) AS profit FROM orders {_where(f)}"
                ),
                field="profit",
                formatter=lambda v, _f: f"${v:,.0f}",
            ),
            cc.sql_kpi(
                "Total Orders",
                db,
                lambda f: (
                    f"SELECT COUNT(DISTINCT order_id) AS orders FROM orders {_where(f)}"
                ),
                field="orders",
                formatter=lambda v, _f: f"{v:,}",
            ),
            cc.sql_kpi(
                "Avg Order Value",
                db,
                lambda f: (
                    f"SELECT ROUND(SUM(sales) / COUNT(DISTINCT order_id)) AS aov FROM orders {_where(f)}"
                ),
                field="aov",
                formatter=lambda v, _f: f"${v:,.0f}",
            ),
        ],
        content=[
            cc.section(
                "Sales Arc",
                cc.sql_area(
                    db,
                    lambda f: (
                        f"""
                        SELECT
                            strftime('%Y', order_date) || '-' ||
                            CASE WHEN CAST(strftime('%m', order_date) AS INT) < 10
                                 THEN '0' || CAST(strftime('%m', order_date) AS INT)
                                 ELSE CAST(strftime('%m', order_date) AS TEXT)
                            END AS month,
                            ROUND(SUM(sales)) AS sales,
                            ROUND(SUM(profit)) AS profit
                        FROM orders {_where(f)}
                        GROUP BY month ORDER BY month
                    """
                    ),
                    x="month",
                    y=["sales", "profit"],
                    title="Monthly Revenue vs Profit  ($)",
                    col=0,
                    colspan=8,
                    height=320,
                    colors=["#F97316", "#FB7185"],
                    smooth=True,
                    gradient=True,
                    linked_filters=["year"],
                ),
                cc.sql_bar(
                    db,
                    lambda f: (
                        f"SELECT segment, ROUND(SUM(sales)) AS sales, ROUND(SUM(profit)) AS profit FROM orders {_where(f)} GROUP BY segment ORDER BY sales DESC"
                    ),
                    x="segment",
                    y=["sales", "profit"],
                    title="Revenue by Segment  ($)",
                    col=8,
                    colspan=4,
                    height=320,
                    colors=["#8B5CF6", "#14B8A6"],
                    grouped=True,
                    linked_filters=["year"],
                ),
                subtitle="Pick a year above to compress the story into a single operating window",
            ),
            cc.note(
                "The orange revenue area intentionally leads the page, while profit stays visible as a second signal rather than fighting for attention.",
                col=0,
                colspan=12,
            ),
            cc.section(
                "Category & Sub-Category Analysis",
                cc.comparison_bars(
                    data_fn=_subcat_profit,
                    x="sub_category",
                    y=["sales", "profit"],
                    title="Revenue & Profit by Sub-Category  ($)",
                    col=0,
                    colspan=7,
                    height=340,
                    colors=["#60A5FA", "#22C55E"],
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
                    positive_color="#22C55E",
                    negative_color="#EF4444",
                    linked_filters=["year"],
                ),
            ),
            cc.section(
                "Top Products by Revenue",
                cc.ranked_bars(
                    data_fn=_top_products,
                    x="product_name",
                    y="sales",
                    title="Top 10 Products  ($ Sales)",
                    col=0,
                    colspan=12,
                    height=360,
                    colors=["#6366F1"],
                    linked_filters=["year"],
                ),
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

    return cc.Page(
        title="Customer Intelligence",
        subtitle="Segment mix · account quality · geographic concentration",
        filters=[
            cc.Filter(
                "segment",
                label="Segment",
                type="select",
                options=["All", "Consumer", "Corporate", "Home Office"],
            ),
        ],
        kpis=[
            cc.stat(
                "Total Customers",
                data_fn=lambda f={}: f"{_customer_summary(f)['customers']:,}",
            ),
            cc.stat("Top Segment", data_fn=_top_segment),
            cc.stat(
                "Avg Rev / Customer",
                data_fn=lambda f={}: (
                    f"${_customer_summary(f)['avg_rev_per_customer']:,.0f}"
                ),
            ),
            cc.stat(
                "Orders", data_fn=lambda f={}: f"{_customer_summary(f)['orders']:,}"
            ),
        ],
        content=[
            cc.section(
                "Segment Breakdown",
                cc.spotlight_donut(
                    data_fn=lambda f={}: {
                        r["segment"]: r["sales"] for r in _segments(f)
                    },
                    title="Revenue by Segment",
                    col=0,
                    colspan=3,
                    height=300,
                    center_text="Sales",
                    colors=["#8B5CF6", "#0EA5E9", "#22C55E"],
                    linked_filters=["segment"],
                ),
                cc.comparison_bars(
                    data_fn=_segments,
                    x="segment",
                    y=["sales", "profit"],
                    title="Sales & Profit by Segment  ($)",
                    col=3,
                    colspan=4,
                    height=300,
                    colors=["#A855F7", "#14B8A6"],
                    linked_filters=["segment"],
                ),
                cc.ranked_bars(
                    data_fn=_region_geo,
                    x="region",
                    y="sales",
                    title="Sales by Region  ($)",
                    col=7,
                    colspan=5,
                    height=300,
                    colors=["#0EA5E9"],
                    linked_filters=["segment"],
                ),
                subtitle="Pick a segment to see the portfolio recompose itself across revenue, regions, and account value",
            ),
            cc.section(
                "Geographic Performance",
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
                    color_scale=["#0F172A", "#1D4ED8", "#38BDF8", "#BAE6FD"],
                    show_labels=True,
                    linked_filters=["segment"],
                ),
                cc.spotlight_donut(
                    data_fn=lambda f={}: {
                        r["segment"]: r["customers"] for r in _segments(f)
                    },
                    title="Customers by Segment",
                    col=4,
                    colspan=4,
                    height=280,
                    center_text="Accounts",
                    colors=["#8B5CF6", "#06B6D4", "#10B981"],
                    linked_filters=["segment"],
                ),
                cc.ranked_bars(
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
            ),
            cc.section(
                "Top Accounts",
                cc.data_table(
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
                    linked_filters=["segment"],
                ),
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

    return cc.Page(
        title="Product Performance",
        subtitle="Category structure · unit momentum · margin pressure from discounting",
        filters=[
            cc.Filter(
                "category",
                label="Category",
                type="select",
                options=["All", "Technology", "Office Supplies", "Furniture"],
            ),
        ],
        kpis=[
            cc.stat(
                "Units Sold", data_fn=lambda f={}: f"{_product_summary(f)['units']:,}"
            ),
            cc.stat("Top Category", data_fn=_top_category),
            cc.stat(
                "Avg Profit Margin",
                data_fn=lambda f={}: f"{_product_summary(f)['margin_pct']}%",
            ),
            cc.stat(
                "Avg Discount",
                data_fn=lambda f={}: f"{_product_summary(f)['avg_discount']}%",
            ),
        ],
        content=[
            cc.section(
                "Category Overview",
                cc.comparison_bars(
                    data_fn=_cat_summary,
                    x="category",
                    y=["sales", "profit"],
                    title="Revenue & Profit by Category  ($)",
                    col=0,
                    colspan=4,
                    height=300,
                    colors=["#7C3AED", "#22C55E"],
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
                cc.ranked_bars(
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
                subtitle="This page leans into structure first: what sells, what scales, and what actually keeps margin intact",
            ),
            cc.note(
                "Technology remains the cleanest profit story, while Furniture carries more unit weight than economic quality.",
                col=0,
                colspan=12,
            ),
            cc.section(
                "Profitability & Discount Impact",
                cc.Treemap(
                    data_fn=_tree_data,
                    title="Revenue Treemap  ($ Sales)",
                    col=0,
                    colspan=6,
                    height=360,
                    drill_down=True,
                    linked_filters=["category"],
                ),
                cc.insight_scatter(
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
            ),
            cc.section(
                "Sub-Category & Top Products",
                cc.ranked_bars(
                    data_fn=_subcat_profit,
                    x="sub_category",
                    y="profit",
                    title="Profit by Sub-Category  ($)",
                    col=0,
                    colspan=7,
                    height=340,
                    colors=["#22C55E"],
                    linked_filters=["category"],
                ),
                cc.ranked_bars(
                    data_fn=_top_profit,
                    x="product_name",
                    y="profit",
                    title="Top 10 Products by Profit  ($)",
                    col=7,
                    colspan=5,
                    height=340,
                    colors=["#0EA5E9"],
                    linked_filters=["category"],
                ),
            ),
        ],
    )


# ─────────────────────────────────────────────────────────────────────────────

if __name__ == "__main__":
    app.run()
