import pandas as pd
import numpy as np
from pathlib import Path


# Reproducible dataset
np.random.seed(42)


# ============================================================
# CONFIGURATION
# ============================================================

NUM_ROWS = 12000

START_DATE = "2025-01-01"
END_DATE = "2026-06-30"


# ============================================================
# BUSINESS DIMENSIONS
# ============================================================

regions = [
    "North",
    "South",
    "East",
    "West"
]

products = [
    "Product A",
    "Product B",
    "Product C",
    "Product D"
]

categories = {
    "Product A": "Electronics",
    "Product B": "Electronics",
    "Product C": "Home",
    "Product D": "Home"
}

channels = [
    "Online",
    "Store",
    "Partner"
]

customer_types = [
    "New",
    "Returning"
]

customer_segments = [
    "Premium",
    "Standard",
    "Budget"
]


# ============================================================
# PRODUCT PRICES
# ============================================================

base_prices = {
    "Product A": 120,
    "Product B": 180,
    "Product C": 95,
    "Product D": 150
}


# ============================================================
# GENERATE DATES
# ============================================================

dates = pd.date_range(
    start=START_DATE,
    end=END_DATE,
    freq="D"
)

selected_dates = np.random.choice(
    dates,
    size=NUM_ROWS
)


# ============================================================
# GENERATE BASIC DIMENSIONS
# ============================================================

df = pd.DataFrame({
    "date": selected_dates,

    "region": np.random.choice(
        regions,
        size=NUM_ROWS,
        p=[0.25, 0.25, 0.25, 0.25]
    ),

    "product": np.random.choice(
        products,
        size=NUM_ROWS,
        p=[0.28, 0.30, 0.22, 0.20]
    ),

    "channel": np.random.choice(
        channels,
        size=NUM_ROWS,
        p=[0.45, 0.40, 0.15]
    ),

    "customer_type": np.random.choice(
        customer_types,
        size=NUM_ROWS,
        p=[0.40, 0.60]
    ),

    "customer_segment": np.random.choice(
        customer_segments,
        size=NUM_ROWS,
        p=[0.20, 0.55, 0.25]
    )
})


df["date"] = pd.to_datetime(df["date"])

df["category"] = df["product"].map(categories)


# ============================================================
# MONTH / SEASONALITY
# ============================================================

df["month"] = df["date"].dt.month

seasonality = {
    1: 0.92,
    2: 0.95,
    3: 1.00,
    4: 1.02,
    5: 1.04,
    6: 0.98,
    7: 1.03,
    8: 1.05,
    9: 0.99,
    10: 1.06,
    11: 1.12,
    12: 1.18
}

df["seasonality"] = df["month"].map(seasonality)


# ============================================================
# PRICE
# ============================================================

df["price"] = df["product"].map(base_prices)

df["price"] = (
    df["price"]
    * np.random.normal(
        1.0,
        0.05,
        NUM_ROWS
    )
)


# ============================================================
# DISCOUNT
# ============================================================

df["discount_pct"] = np.random.normal(
    8,
    3,
    NUM_ROWS
)

df["discount_pct"] = df["discount_pct"].clip(
    0,
    25
)


# ============================================================
# BASE UNITS
# ============================================================

product_units = {
    "Product A": 32,
    "Product B": 38,
    "Product C": 42,
    "Product D": 28
}

df["base_units"] = df["product"].map(
    product_units
)


# Channel effects

channel_effect = {
    "Online": 1.08,
    "Store": 1.00,
    "Partner": 0.88
}

df["channel_effect"] = df["channel"].map(
    channel_effect
)


# Region effects

region_effect = {
    "North": 1.05,
    "South": 1.00,
    "East": 0.95,
    "West": 1.02
}

df["region_effect"] = df["region"].map(
    region_effect
)


# Customer effects

customer_effect = {
    "New": 0.90,
    "Returning": 1.10
}

df["customer_effect"] = df["customer_type"].map(
    customer_effect
)


# ============================================================
# INVENTORY AVAILABILITY
# ============================================================

df["inventory_availability"] = np.random.normal(
    0.96,
    0.025,
    NUM_ROWS
)

df["inventory_availability"] = df[
    "inventory_availability"
].clip(
    0.75,
    1.00
)


# ============================================================
# 🔥 HIDDEN BUSINESS EVENT
#
# June 2026:
#
# South + Product B + Online
# experiences an inventory shortage.
#
# This should become the main root-cause signal.
# ============================================================

problem_condition = (
    (df["date"] >= "2026-06-01")
    &
    (df["region"] == "South")
    &
    (df["product"] == "Product B")
    &
    (df["channel"] == "Online")
)


# Inventory shortage

df.loc[
    problem_condition,
    "inventory_availability"
] = np.random.uniform(
    0.45,
    0.65,
    problem_condition.sum()
)


# ============================================================
# ADDITIONAL MIX SHIFT
#
# South region gets more New customers
# during the problem period.
# ============================================================

mix_shift_condition = (
    (df["date"] >= "2026-06-01")
    &
    (df["region"] == "South")
)

mix_indices = df.index[mix_shift_condition]

np.random.seed(100)

df.loc[
    mix_indices,
    "customer_type"
] = np.random.choice(
    ["New", "Returning"],
    size=len(mix_indices),
    p=[0.65, 0.35]
)


# ============================================================
# DISCOUNT CHANGE
#
# South + Online sees higher discounting.
# This creates another factor that the agent
# must investigate.
# ============================================================

discount_condition = (
    (df["date"] >= "2026-06-01")
    &
    (df["region"] == "South")
    &
    (df["channel"] == "Online")
)

df.loc[
    discount_condition,
    "discount_pct"
] += np.random.uniform(
    5,
    10,
    discount_condition.sum()
)

df["discount_pct"] = df[
    "discount_pct"
].clip(
    0,
    30
)


# ============================================================
# CALCULATE UNITS
# ============================================================

noise = np.random.normal(
    1.0,
    0.12,
    NUM_ROWS
)

df["units"] = (
    df["base_units"]
    * df["channel_effect"]
    * df["region_effect"]
    * df["customer_effect"]
    * df["seasonality"]
    * df["inventory_availability"]
    * noise
)


# Additional reduction caused by
# severe shortage in the hidden event.

df.loc[
    problem_condition,
    "units"
] *= np.random.uniform(
    0.55,
    0.75,
    problem_condition.sum()
)


df["units"] = df["units"].clip(
    lower=1
).round().astype(int)


# ============================================================
# RETURNS
# ============================================================

return_rate = np.random.uniform(
    0.01,
    0.06,
    NUM_ROWS
)

df["returns"] = (
    df["units"] * return_rate
).round().astype(int)


# Slightly higher returns during
# the problematic period.

df.loc[
    problem_condition,
    "returns"
] += np.random.randint(
    1,
    4,
    problem_condition.sum()
)


# ============================================================
# SALES
# ============================================================

df["sales"] = (
    df["units"]
    * df["price"]
    * (1 - df["discount_pct"] / 100)
)


# Remove returned items from realized sales

df["sales"] -= (
    df["returns"]
    * df["price"]
)


# Random business noise

df["sales"] *= np.random.normal(
    1.0,
    0.04,
    NUM_ROWS
)


df["sales"] = df["sales"].clip(
    lower=0
).round(2)


# ============================================================
# REMOVE INTERNAL CALCULATION COLUMNS
# ============================================================

df = df[
    [
        "date",
        "region",
        "product",
        "category",
        "channel",
        "customer_type",
        "customer_segment",
        "sales",
        "units",
        "price",
        "discount_pct",
        "returns",
        "inventory_availability"
    ]
]


# ============================================================
# SORT DATA
# ============================================================

df = df.sort_values(
    "date"
).reset_index(
    drop=True
)


# ============================================================
# SAVE DATASET
# ============================================================

output_path = (
    Path(__file__).resolve().parent.parent
    / "data"
    / "realistic_sales.csv"
)

df.to_csv(
    output_path,
    index=False
)


# ============================================================
# SUMMARY
# ============================================================

print("=" * 60)
print("INSIGHTPILOT REALISTIC DATASET GENERATED")
print("=" * 60)

print()

print("Rows:", len(df))
print("Columns:", len(df.columns))

print()

print("Date Range:")
print(
    df["date"].min().date(),
    "→",
    df["date"].max().date()
)

print()

print("Regions:")
print(
    df["region"].unique().tolist()
)

print()

print("Products:")
print(
    df["product"].unique().tolist()
)

print()

print("Channels:")
print(
    df["channel"].unique().tolist()
)

print()

print("Total Sales:")
print(
    round(df["sales"].sum(), 2)
)

print()

print("Dataset saved to:")
print(output_path)

print()

print("Hidden scenario:")
print(
    "June 2026: South + Product B + Online "
    "inventory shortage"
)

print("=" * 60)