"""
◆ ChartCraft — Example multi-page dashboard.
Run:  python example_app.py
Then: http://localhost:8050
"""

import chartcraft as cc

app = cc.App("Sales Analytics", theme="midnight")


@app.page("/")
def overview():
    """Overview"""
    return cc.Dashboard(
        title="Sales Overview",
        subtitle="Real-time performance metrics",
        kpis=[
            cc.KPI("Total Revenue", "$4.2M",  change=12.5, prefix="", suffix=""),
            cc.KPI("Active Users",  "45,231",  change=-3.2),
            cc.KPI("Conversion",   "4.8%",    change=0.5),
            cc.KPI("Avg Order",    "$94.20",  change=7.1),
        ],
        filters=[
            cc.Filter("region", label="Region", type="select",
                      options=["All", "North", "South", "East", "West"]),
            cc.Filter("period", label="Period", type="select",
                      options=["This Month", "Last Month", "Q1", "Q2", "Q3", "Q4"]),
        ],
        charts=[
            cc.Line(
                {"month": ["Jan","Feb","Mar","Apr","May","Jun","Jul","Aug","Sep","Oct","Nov","Dec"],
                 "revenue": [310,280,350,420,390,480,510,460,530,490,610,720],
                 "target":  [300,300,350,400,400,450,500,500,500,550,600,650]},
                x="month", y=["revenue", "target"],
                title="Monthly Revenue vs Target",
                col=0, colspan=8, height=320,
                colors=["#8B5CF6", "#3F3F46"],
            ),
            cc.Donut(
                {"Enterprise": 45, "Professional": 30, "Starter": 25},
                title="Plan Distribution",
                col=8, colspan=4, height=320,
                colors=["#8B5CF6", "#EC4899", "#06B6D4"],
                inner_radius="55%",
                center_text="Plans",
            ),
            cc.Bar(
                {"region": ["North", "South", "East", "West", "Central"],
                 "q1": [120, 95, 140, 88, 110],
                 "q2": [135, 105, 155, 92, 125],
                 "q3": [150, 115, 165, 100, 135]},
                x="region", y=["q1", "q2", "q3"],
                title="Sales by Region (Grouped)",
                col=0, colspan=6, height=300,
                grouped=True,
            ),
            cc.Waterfall(
                {"label": ["Revenue","COGS","Gross","Marketing","OpEx","EBITDA"],
                 "value": [500, -180, 0, -60, -40, 0]},
                x="label", y="value",
                title="P&L Waterfall",
                col=6, colspan=6, height=300,
                colors=["#10B981", "#10B981", "#6366F1", "#EF4444", "#EF4444", "#8B5CF6"],
            ),
            cc.SectionHeader(title="KPI Details", subtitle="Granular view", col=0, colspan=12),
            cc.Gauge(72, title="Customer Satisfaction", col=0, colspan=3, height=240),
            cc.Gauge(88, title="SLA Compliance",         col=3, colspan=3, height=240),
            cc.Gauge(55, title="Pipeline Health",        col=6, colspan=3, height=240),
            cc.Gauge(94, title="Team Velocity",          col=9, colspan=3, height=240),
        ],
    )


@app.page("/products")
def products():
    """Products"""
    return cc.Dashboard(
        title="Product Analytics",
        subtitle="SKU performance & trends",
        charts=[
            cc.Treemap(
                {"name": "root", "children": [
                    {"name": "Electronics", "value": 420, "children": [
                        {"name": "Laptops", "value": 180},
                        {"name": "Phones",  "value": 150},
                        {"name": "Tablets", "value": 90},
                    ]},
                    {"name": "Clothing", "value": 280, "children": [
                        {"name": "Men",   "value": 140},
                        {"name": "Women", "value": 140},
                    ]},
                    {"name": "Home", "value": 190},
                    {"name": "Sports", "value": 110},
                ]},
                title="Revenue by Category",
                col=0, colspan=7, height=380,
            ),
            cc.Funnel(
                {"stage": ["Awareness","Interest","Consideration","Intent","Purchase"],
                 "count": [10000, 6200, 3800, 1900, 850]},
                x="stage", y="count",
                title="Purchase Funnel",
                col=7, colspan=5, height=380,
            ),
            cc.Scatter(
                [{"price": p, "rating": r, "sales": s}
                 for p, r, s in [
                     (29.99,4.2,1200),(49.99,4.5,950),(19.99,3.8,1800),
                     (99.99,4.8,400),(14.99,3.5,2200),(79.99,4.3,620),
                     (34.99,4.1,1050),(59.99,4.6,780),(24.99,3.9,1400),
                 ]],
                x="price", y="rating",
                title="Price vs Rating (by Sales Volume)",
                col=0, colspan=6, height=300,
            ),
            cc.Radar(
                {"metric": ["Quality","Price","Speed","Support","Features"],
                 "product_a": [90,70,80,85,75],
                 "product_b": [75,90,70,65,85]},
                x="metric", y=["product_a","product_b"],
                title="Product Comparison Radar",
                col=6, colspan=6, height=300,
            ),
        ],
    )


@app.page("/customers")
def customers():
    """Customers"""
    import random
    random.seed(42)

    cohort_data = {
        "x_labels": ["Jan","Feb","Mar","Apr","May","Jun"],
        "y_labels": ["<25","25-34","35-44","45-54","55+"],
        "matrix": [[random.randint(20,100) for _ in range(6)] for _ in range(5)],
    }

    return cc.Dashboard(
        title="Customer Intelligence",
        kpis=[
            cc.KPI("Total Customers", "128,540", change=8.3),
            cc.KPI("Churn Rate",      "2.4%",    change=-0.8),
            cc.KPI("LTV",             "$820",    change=15.2),
            cc.KPI("NPS Score",       "72",      change=5.0),
        ],
        charts=[
            cc.Area(
                {"month": ["Jan","Feb","Mar","Apr","May","Jun","Jul","Aug"],
                 "new": [1200,1400,1100,1600,1900,1750,2100,2400],
                 "churned": [200,180,220,160,190,170,200,180]},
                x="month", y=["new","churned"],
                title="Customer Acquisition & Churn",
                col=0, colspan=8, height=300,
                colors=["#10B981","#EF4444"],
                stacked=False,
            ),
            cc.Heatmap(
                cohort_data,
                title="Cohort Retention by Age Group",
                col=8, colspan=4, height=300,
            ),
            cc.Table(
                [{"Customer":"Acme Corp","Tier":"Enterprise","Revenue":"$48,200","NPS":82,"Status":"✅ Active"},
                 {"Customer":"GlobalTech","Tier":"Pro","Revenue":"$12,400","NPS":71,"Status":"✅ Active"},
                 {"Customer":"StartupXYZ","Tier":"Starter","Revenue":"$2,100","NPS":45,"Status":"⚠️ At Risk"},
                 {"Customer":"MegaRetail","Tier":"Enterprise","Revenue":"$95,000","NPS":88,"Status":"✅ Active"},
                 {"Customer":"LocalBiz","Tier":"Starter","Revenue":"$890","NPS":38,"Status":"🔴 Churned"},
                 {"Customer":"TechGiant","Tier":"Pro","Revenue":"$31,500","NPS":79,"Status":"✅ Active"},
                 {"Customer":"SmallCo","Tier":"Starter","Revenue":"$1,200","NPS":55,"Status":"✅ Active"},
                 {"Customer":"BigBank","Tier":"Enterprise","Revenue":"$120,000","NPS":91,"Status":"✅ Active"}],
                title="Customer Accounts",
                col=0, colspan=12, height=360,
                page_size=5, sortable=True, searchable=True,
            ),
        ],
    )


@app.page("/realtime")
def realtime():
    """Live Data"""
    import time, math, random

    def live_kpi():
        return f"{random.randint(1200, 1800):,}"

    def live_stream():
        now = time.time()
        return [
            {"ts": int(now - i * 5), "value": round(50 + 20 * math.sin(now / 10 - i * 0.3) + random.uniform(-5, 5), 2)}
            for i in range(30, -1, -1)
        ]

    return cc.Dashboard(
        title="Live Metrics",
        subtitle="Real-time data stream — updates every few seconds",
        kpis=[
            cc.KPI("Active Sessions", data_fn=live_kpi, refresh=4),
            cc.KPI("Events/sec",      data_fn=lambda: str(random.randint(800, 1200)), refresh=2),
            cc.KPI("Error Rate",      data_fn=lambda: f"{random.uniform(0.1, 0.8):.2f}%", refresh=5),
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


if __name__ == "__main__":
    app.run()
