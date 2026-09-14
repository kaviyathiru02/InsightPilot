import pandas as pd
from pathlib import Path


# ============================================================
# LOAD DATA
# ============================================================

BASE_DIR = Path(__file__).resolve().parent.parent

DATA_PATH = BASE_DIR / "data" / "realistic_sales_v2.csv"

df = pd.read_csv(DATA_PATH)

df["date"] = pd.to_datetime(df["date"])


# ============================================================
# CREATE PERIODS
# ============================================================

previous = df[
    (df["date"] >= "2026-05-01") &
    (df["date"] <= "2026-05-31")
]

current = df[
    (df["date"] >= "2026-06-01") &
    (df["date"] <= "2026-06-30")
]


def sales_change(previous_df, current_df):

    previous_sales = previous_df["sales"].sum()
    current_sales = current_df["sales"].sum()

    change = current_sales - previous_sales

    change_pct = (
        change / previous_sales
    ) * 100

    return (
        previous_sales,
        current_sales,
        change,
        change_pct
    )


# ============================================================
# OVERALL CHANGE
# ============================================================

print("=" * 70)
print("SCENARIO VERIFICATION")
print("=" * 70)

print("\nOVERALL SALES CHANGE")
print("-" * 70)

prev, curr, change, pct = sales_change(
    previous,
    current
)

print(f"May Sales   : {prev:,.2f}")
print(f"June Sales  : {curr:,.2f}")
print(f"Change      : {change:,.2f}")
print(f"Change %    : {pct:.2f}%")


# ============================================================
# SOUTH
# ============================================================

print("\nSOUTH REGION")
print("-" * 70)

south_previous = previous[
    previous["region"] == "South"
]

south_current = current[
    current["region"] == "South"
]

prev, curr, change, pct = sales_change(
    south_previous,
    south_current
)

print(f"May Sales   : {prev:,.2f}")
print(f"June Sales  : {curr:,.2f}")
print(f"Change      : {change:,.2f}")
print(f"Change %    : {pct:.2f}%")


# ============================================================
# PRODUCT B
# ============================================================

print("\nPRODUCT B")
print("-" * 70)

b_previous = previous[
    previous["product"] == "Product B"
]

b_current = current[
    current["product"] == "Product B"
]

prev, curr, change, pct = sales_change(
    b_previous,
    b_current
)

print(f"May Sales   : {prev:,.2f}")
print(f"June Sales  : {curr:,.2f}")
print(f"Change      : {change:,.2f}")
print(f"Change %    : {pct:.2f}%")


# ============================================================
# ONLINE
# ============================================================

print("\nONLINE CHANNEL")
print("-" * 70)

online_previous = previous[
    previous["channel"] == "Online"
]

online_current = current[
    current["channel"] == "Online"
]

prev, curr, change, pct = sales_change(
    online_previous,
    online_current
)

print(f"May Sales   : {prev:,.2f}")
print(f"June Sales  : {curr:,.2f}")
print(f"Change      : {change:,.2f}")
print(f"Change %    : {pct:.2f}%")


# ============================================================
# INTERACTION
# SOUTH + PRODUCT B + ONLINE
# ============================================================

print("\nSOUTH + PRODUCT B + ONLINE")
print("-" * 70)

interaction_previous = previous[
    (previous["region"] == "South") &
    (previous["product"] == "Product B") &
    (previous["channel"] == "Online")
]

interaction_current = current[
    (current["region"] == "South") &
    (current["product"] == "Product B") &
    (current["channel"] == "Online")
]

prev, curr, change, pct = sales_change(
    interaction_previous,
    interaction_current
)

print(f"May Sales   : {prev:,.2f}")
print(f"June Sales  : {curr:,.2f}")
print(f"Change      : {change:,.2f}")
print(f"Change %    : {pct:.2f}%")


# ============================================================
# INVENTORY CHECK
# ============================================================

print("\nINVENTORY AVAILABILITY")
print("-" * 70)

print(
    "Overall June:",
    round(current["inventory_availability"].mean(), 3)
)

print(
    "South + Product B + Online:",
    round(
        interaction_current[
            "inventory_availability"
        ].mean(),
        3
    )
)


# ============================================================
# FINAL
# ============================================================

print("\n" + "=" * 70)
print("VERIFICATION COMPLETE")
print("=" * 70)