"""
Superstore Financial Dashboard — ChartCraft v1

A stunning, interactive executive dashboard built on 10,800 real
Superstore orders. Spot revenue trends, profit leaks, regional
winners, and category performance — all from 50 lines of Python.

Usage:
    python example_app.py
    # → http://localhost:8050
"""

import csv
from collections import defaultdict

import chartcraft as cc

# ── 1. Load & aggregate 10,800 orders ──────────────────────────────

with open("data/superstore.csv") as f:
    raw = list(csv.DictReader(f))

# Helper: safe float
def sf(val):
    try:
        return float(val)
    except (ValueError, TypeError):
        return 0.0


# ── Monthly trends ──────────────────────────────────────────────────

monthly = defaultdict(lambda: {"sales": 0, "profit": 0, "orders": 0, "discount": 0.0})
for r in raw:
    d = r.get("Order Date")
    if d and "/" in d:
        parts = d.split("/")
        key = f"{parts[0]}/{parts[2]}"
    else:
        key = "?"
    s = sf(r.get("Sales"))
    monthly[key]["sales"] += s
    monthly[key]["profit"] += sf(r.get("Profit"))
    monthly[key]["orders"] += 1
    monthly[key]["discount"] += sf(r.get("Discount"))

non_null_months = [k for k in monthly if k != "?"]
sorted_months = sorted(non_null_months, key=lambda k: (int(k.split("/")[1]), int(k.split("/")[0])))
months = sorted_months
month_sales = [round(monthly[m]["sales"], 2) for m in sorted_months]
month_profit = [round(monthly[m]["profit"], 2) for m in sorted_months]
month_orders = [monthly[m]["orders"] for m in sorted_months]

# Total metrics
total_sales = sum(month_sales)
total_profit = sum(month_profit)
total_orders = sum(month_orders)
total_discount = sum(monthly[m]["discount"] for m in sorted_months)
avg_discount_pct = round(total_discount / total_orders * 100, 1) if total_orders else 0
margin_pct = round(total_profit / total_sales * 100, 1) if total_sales else 0

month_data = cc.Data({
    "month": months,
    "Revenue ($K)": [round(s / 1000, 1) for s in month_sales],
    "Profit ($K)": [round(p / 1000, 1) for p in month_profit],
})


# ── Category & sub-category ─────────────────────────────────────────

cat_stats = defaultdict(lambda: {"sales": 0, "profit": 0, "orders": 0})
sub_stats = defaultdict(lambda: {"sales": 0, "profit": 0, "orders": 0})
for r in raw:
    c = r.get("Category") or "Unknown"
    sc = r.get("Sub-Category") or "Unknown"
    s = sf(r.get("Sales"))
    cat_stats[c]["sales"] += s
    cat_stats[c]["profit"] += sf(r.get("Profit"))
    cat_stats[c]["orders"] += 1
    sub_stats[sc]["sales"] += s
    sub_stats[sc]["profit"] += sf(r.get("Profit"))
    sub_stats[sc]["orders"] += 1

cat_names = list(cat_stats.keys())
cat_sales = [round(cat_stats[c]["sales"], 2) for c in cat_names]
cat_profit = [round(cat_stats[c]["profit"], 2) for c in cat_names]

cat_data = cc.Data({
    "category": cat_names,
    "Revenue": cat_sales,
    "Profit": cat_profit,
})

# Sub-category top 10 by revenue
sub_sorted = sorted(sub_stats.items(), key=lambda x: x[1]["sales"], reverse=True)
top_sub = sub_sorted[:10]
sc_names = [s[0] for s in top_sub]
sc_sales = [round(s[1]["sales"], 2) for s in top_sub]
sc_profit = [round(s[1]["profit"], 2) for s in top_sub]

subcat_data = cc.Data({
    "subcategory": sc_names,
    "Revenue": sc_sales,
    "Profit": sc_profit,
})


# ── Segment analysis ────────────────────────────────────────────────

seg_stats = defaultdict(lambda: {"sales": 0, "profit": 0, "orders": 0})
for r in raw:
    seg = r.get("Segment") or "Unknown"
    s = sf(r.get("Sales"))
    seg_stats[seg]["sales"] += s
    seg_stats[seg]["profit"] += sf(r.get("Profit"))
    seg_stats[seg]["orders"] += 1

seg_names = list(seg_stats.keys())
seg_sales = [round(seg_stats[s]["sales"], 2) for s in seg_names]
seg_profit = [round(seg_stats[s]["profit"], 2) for s in seg_names]

seg_data = cc.Data({
    "segment": seg_names,
    "Revenue": seg_sales,
    "Profit": seg_profit,
})


# ── Region breakdown ────────────────────────────────────────────────

region_stats = defaultdict(lambda: {"sales": 0, "orders": 0})
for r in raw:
    reg = r.get("Region") or "Unknown"
    s = sf(r.get("Sales"))
    region_stats[reg]["sales"] += s
    region_stats[reg]["orders"] += 1

reg_names = list(region_stats.keys())
reg_sales = [round(region_stats[r]["sales"], 2) for r in reg_names]

region_data = cc.Data({
    "region": reg_names,
    "Revenue": reg_sales,
})


# ── Top 10 states ───────────────────────────────────────────────────

state_stats = defaultdict(lambda: {"sales": 0, "profit": 0})
for r in raw:
    st = r.get("State") or "Unknown"
    s = sf(r.get("Sales"))
    state_stats[st]["sales"] += s
    state_stats[st]["profit"] += sf(r.get("Profit"))

state_sorted = sorted(state_stats.items(), key=lambda x: x[1]["sales"], reverse=True)
top_states = state_sorted[:10]
st_names = [s[0] for s in top_states]
st_sales = [round(s[1]["sales"], 2) for s in top_states]
st_profit = [round(s[1]["profit"], 2) for s in top_states]

state_data = cc.Data({
    "state": st_names,
    "Revenue": st_sales,
    "Profit": st_profit,
})


# ── Ship-mode (operational) ─────────────────────────────────────────

ship_stats = defaultdict(lambda: {"sales": 0, "orders": 0})
for r in raw:
    sm = r.get("Ship Mode") or "Unknown"
    ship_stats[sm]["sales"] += sf(r.get("Sales"))
    ship_stats[sm]["orders"] += 1

ship_names = list(ship_stats.keys())
ship_orders = [ship_stats[s]["orders"] for s in ship_names]
ship_sales = [round(ship_stats[s]["sales"], 2) for s in ship_names]

ship_data = cc.Data({
    "mode": ship_names,
    "Orders": ship_orders,
    "Revenue": ship_sales,
})


# ── Scatter: 500 samples for performance ────────────────────────────

import random
sample = random.sample(raw, min(500, len(raw)))
scatter_x, scatter_y = [], []
for r in sample:
    disc = sf(r.get("Discount"))
    prof = sf(r.get("Profit"))
    scatter_x.append(disc)
    scatter_y.append(prof)

scatter_data = cc.Data({
    "discount": scatter_x,
    "profit": scatter_y,
})


# ====================================================================
#  DASHBOARD
# ====================================================================

# Theme — sleek dark executive look
cc.theme(
    background="#0f0f1a",
    card_background="#1a1a2e",
    title_color="#ffffff",
    text_color="#b0b0cc",
    header_background="linear-gradient(135deg, #0f0f1a 0%, #1a1a2e 50%, #16213e 100%)",
)

dashboard = cc.Dashboard(
    title="Superstore Financial Intelligence",
    layout="grid",
    columns=2,
    spacing=24,
    charts=[
        # Chart 1 — Monthly Revenue & Profit (trend, full-width)
        cc.line(
            month_data,
            x="month",
            y=["Revenue ($K)", "Profit ($K)"],
            title="Monthly Revenue & Profit",
            colors=["#7C3AED", "#10B981"],
            smooth=True,
            show_dots=True,
            line_width=3,
            height=360,
            legend=True,
            legend_position="top",
        ),
        # Chart 2 — Sales by Category
        cc.bar(
            cat_data,
            x="category",
            y="Revenue",
            title="Revenue by Category",
            colors=["#7C3AED"],
            bar_border_radius=8,
            bar_shadow="0 4px 12px rgba(0,0,0,0.2)",
            height=320,
            legend=False,
        ),
        # Chart 3 — Regional split (donut)
        cc.donut(
            region_data,
            x="region",
            y="Revenue",
            title="Revenue by Region",
            colors=["#7C3AED", "#10B981", "#F59E0B", "#3B82F6"],
            inner_radius="55%",
            height=320,
            legend=True,
            legend_position="bottom",
        ),
        # Chart 4 — Segment comparison
        cc.bar(
            seg_data,
            x="segment",
            y="Revenue",
            title="Revenue by Customer Segment",
            colors=["#10B981"],
            bar_border_radius=8,
            height=320,
            legend=False,
        ),
        # Chart 5 — Top 10 sub-categories
        cc.bar(
            subcat_data,
            x="subcategory",
            y="Revenue",
            title="Top 10 Sub-Categories by Revenue",
            colors=["#F59E0B"],
            bar_border_radius=6,
            height=340,
            legend=False,
        ),
        # Chart 6 — Top 10 states
        cc.bar(
            state_data,
            x="state",
            y="Revenue",
            title="Top 10 States by Revenue",
            colors=["#3B82F6"],
            bar_border_radius=6,
            height=340,
            legend=False,
        ),
        # Chart 7 — Discount vs Profit scatter
        cc.scatter(
            scatter_data,
            x="discount",
            y="profit",
            title="Discount Rate vs Profit (Sample of 500 Orders)",
            colors=["#EF4444"],
            height=320,
            legend=False,
        ),
        # Chart 8 — Monthly order volume
        cc.area(
            cc.Data({
                "month": months,
                "Orders": month_orders,
            }),
            x="month",
            y="Orders",
            title="Monthly Order Volume",
            colors=["#8B5CF6"],
            smooth=True,
            height=320,
            legend=False,
        ),
    ],
)

# Print key metrics
print(f"◆  Superstore Financial Dashboard")
print(f"   Total Revenue:  ${total_sales:,.2f}")
print(f"   Total Profit:   ${total_profit:,.2f}")
print(f"   Margin:         {margin_pct}%")
print(f"   Total Orders:   {total_orders:,}")
print(f"   Avg Discount:   {avg_discount_pct}%")
print()

# Serve
cc.serve(dashboard, port=8050)
