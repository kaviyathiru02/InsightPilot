import pandas as pd
import numpy as np
from pathlib import Path


# ============================================================
# CONFIGURATION
# ============================================================

SEED = 42

np.random.seed(SEED)

NUM_ROWS = 20000

START_DATE = "2025-01-01"
END_DATE = "2026-06-30"


# ============================================================
# OUTPUT DIRECTORY
# ============================================================

BASE_DIR = Path(__file__).resolve().parent.parent

DATA_DIR = BASE_DIR / "data"

DATA_DIR.mkdir(
    parents=True,
    exist_ok=True
)


# ============================================================
# BUSINESS DIMENSIONS
# ============================================================

REGIONS = [
    "North",
    "South",
    "East",
    "West"
]

PRODUCTS = [
    "Product A",
    "Product B",
    "Product C",
    "Product D"
]

CATEGORIES = {
    "Product A": "Electronics",
    "Product B": "Electronics",
    "Product C": "Home",
    "Product D": "Home"
}

CHANNELS = [
    "Online",
    "Store",
    "Partner"
]

CUSTOMER_TYPES = [
    "New",
    "Returning"
]

CUSTOMER_SEGMENTS = [
    "Premium",
    "Standard",
    "Budget"
]
# ============================================================
# PRODUCT PRICES
# ============================================================

BASE_PRICES = {
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
# GENERATE BUSINESS DIMENSIONS
# ============================================================

df = pd.DataFrame({

    "date": selected_dates,

    "region": np.random.choice(
        REGIONS,
        size=NUM_ROWS,
        p=[0.25, 0.25, 0.25, 0.25]
    ),

    "product": np.random.choice(
        PRODUCTS,
        size=NUM_ROWS,
        p=[0.28, 0.30, 0.22, 0.20]
    ),

    "channel": np.random.choice(
        CHANNELS,
        size=NUM_ROWS,
        p=[0.45, 0.40, 0.15]
    ),

    "customer_type": np.random.choice(
        CUSTOMER_TYPES,
        size=NUM_ROWS,
        p=[0.40, 0.60]
    ),

    "customer_segment": np.random.choice(
        CUSTOMER_SEGMENTS,
        size=NUM_ROWS,
        p=[0.20, 0.55, 0.25]
    )
})


df["date"] = pd.to_datetime(df["date"])


# Product category

df["category"] = df["product"].map(
    CATEGORIES
)


# ============================================================
# SEASONALITY
# ============================================================

df["month"] = df["date"].dt.month

SEASONALITY = {
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

df["seasonality"] = df["month"].map(
    SEASONALITY
)


# ============================================================
# PRICE
# ============================================================

df["price"] = df["product"].map(
    BASE_PRICES
)

df["price"] *= np.random.normal(
    1.0,
    0.05,
    NUM_ROWS
)


# ============================================================
# DISCOUNT
# ============================================================

df["discount_pct"] = np.random.normal(
    8,
    3,
    NUM_ROWS
)

df["discount_pct"] = df[
    "discount_pct"
].clip(
    0,
    25
)


# ============================================================
# MARKETING SPEND
# ============================================================

df["marketing_spend"] = np.random.normal(
    5000,
    1000,
    NUM_ROWS
)

df["marketing_spend"] = df[
    "marketing_spend"
].clip(
    1500,
    9000
)


# ============================================================
# COMPETITOR PRICE INDEX
#
# 1.00 = approximately equal to our price
# < 1.00 = competitor is cheaper
# > 1.00 = competitor is more expensive
# ============================================================

df["competitor_price_index"] = np.random.normal(
    1.02,
    0.08,
    NUM_ROWS
)

df["competitor_price_index"] = df[
    "competitor_price_index"
].clip(
    0.75,
    1.30
)


# ============================================================
# CUSTOMER SATISFACTION
# ============================================================

df["customer_satisfaction"] = np.random.normal(
    4.1,
    0.35,
    NUM_ROWS
)

df["customer_satisfaction"] = df[
    "customer_satisfaction"
].clip(
    1.0,
    5.0
)


# ============================================================
# BUSINESS EFFECTS
# ============================================================

PRODUCT_UNITS = {
    "Product A": 32,
    "Product B": 38,
    "Product C": 42,
    "Product D": 28
}

CHANNEL_EFFECT = {
    "Online": 1.08,
    "Store": 1.00,
    "Partner": 0.88
}

REGION_EFFECT = {
    "North": 1.05,
    "South": 1.00,
    "East": 0.95,
    "West": 1.02
}

CUSTOMER_EFFECT = {
    "New": 0.90,
    "Returning": 1.10
}


df["base_units"] = df["product"].map(
    PRODUCT_UNITS
)

df["channel_effect"] = df["channel"].map(
    CHANNEL_EFFECT
)

df["region_effect"] = df["region"].map(
    REGION_EFFECT
)

df["customer_effect"] = df[
    "customer_type"
].map(
    CUSTOMER_EFFECT
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
# SCENARIO 1 — DOMINANT + INTERACTING ROOT CAUSE
#
# In June 2026:
#
# South + Product B + Online
# experiences an inventory shortage.
#
# IMPORTANT:
# We do NOT make the entire South region fail.
# The problem is concentrated in a specific combination.
# ============================================================

interaction_condition = (
    (df["date"] >= "2026-06-01")
    &
    (df["date"] <= "2026-06-30")
    &
    (df["region"] == "South")
    &
    (df["product"] == "Product B")
    &
    (df["channel"] == "Online")
)


df.loc[
    interaction_condition,
    "inventory_availability"
] = np.random.uniform(
    0.45,
    0.65,
    interaction_condition.sum()
)


# ============================================================
# SCENARIO 2 — CUSTOMER MIX SHIFT
#
# During June, South gets a higher proportion
# of NEW customers.
#
# This is a secondary signal.
# ============================================================

mix_condition = (
    (df["date"] >= "2026-06-01")
    &
    (df["date"] <= "2026-06-30")
    &
    (df["region"] == "South")
)


mix_indices = df.index[mix_condition]

np.random.seed(100)

df.loc[
    mix_indices,
    "customer_type"
] = np.random.choice(
    ["New", "Returning"],
    size=len(mix_indices),
    p=[0.68, 0.32]
)


# ============================================================
# SCENARIO 3 — DISCOUNT CHANGE
#
# South + Online has more discounting.
#
# This creates another plausible explanation.
# ============================================================

discount_condition = (
    (df["date"] >= "2026-06-01")
    &
    (df["date"] <= "2026-06-30")
    &
    (df["region"] == "South")
    &
    (df["channel"] == "Online")
)


df.loc[
    discount_condition,
    "discount_pct"
] += np.random.uniform(
    4,
    9,
    discount_condition.sum()
)


df["discount_pct"] = df[
    "discount_pct"
].clip(
    0,
    30
)


# ============================================================
# SCENARIO 4 — COMPETITOR PRESSURE
#
# Competitors become slightly more competitive
# in South during June.
#
# This is intentionally weaker than the inventory event.
# ============================================================

competitor_condition = (
    (df["date"] >= "2026-06-01")
    &
    (df["date"] <= "2026-06-30")
    &
    (df["region"] == "South")
)


df.loc[
    competitor_condition,
    "competitor_price_index"
] -= np.random.uniform(
    0.03,
    0.07,
    competitor_condition.sum()
)


df["competitor_price_index"] = df[
    "competitor_price_index"
].clip(
    0.70,
    1.30
)


# ============================================================
# SCENARIO 5 — CUSTOMER SATISFACTION
#
# Small decline in satisfaction in the affected area.
# Again, this is deliberately weaker than the main cause.
# ============================================================

satisfaction_condition = (
    (df["date"] >= "2026-06-01")
    &
    (df["date"] <= "2026-06-30")
    &
    (df["region"] == "South")
)


df.loc[
    satisfaction_condition,
    "customer_satisfaction"
] -= np.random.uniform(
    0.10,
    0.30,
    satisfaction_condition.sum()
)


df["customer_satisfaction"] = df[
    "customer_satisfaction"
].clip(
    1.0,
    5.0
)
# ============================================================
# CALCULATE UNITS SOLD
# ============================================================

# Random business variation.
# This prevents the dataset from being perfectly predictable.

noise = np.random.normal(
    1.0,
    0.12,
    NUM_ROWS
)


# Base unit calculation

df["units"] = (
    df["base_units"]
    * df["channel_effect"]
    * df["region_effect"]
    * df["customer_effect"]
    * df["seasonality"]
    * df["inventory_availability"]
    * noise
)


# ============================================================
# INVENTORY SHORTAGE IMPACT
#
# The affected South + Product B + Online combination
# receives an additional reduction in units.
#
# This makes the interaction meaningful.
# ============================================================

df.loc[
    interaction_condition,
    "units"
] *= np.random.uniform(
    0.55,
    0.75,
    interaction_condition.sum()
)


# ============================================================
# COMPETITOR PRESSURE IMPACT
#
# When competitors become cheaper, demand decreases slightly.
# ============================================================

competitor_impact = (
    1
    - (
        1.02 - df["competitor_price_index"]
    ).clip(
        lower=0
    ) * 0.8
)


df["units"] *= competitor_impact


# ============================================================
# MARKETING IMPACT
#
# Higher marketing spend provides a modest demand lift.
# ============================================================

marketing_effect = (
    df["marketing_spend"] / 5000
).clip(
    0.7,
    1.3
)

marketing_effect = (
    0.85
    + 0.15 * marketing_effect
)

df["units"] *= marketing_effect


# ============================================================
# CUSTOMER SATISFACTION IMPACT
#
# Satisfaction has a small influence on demand.
# ============================================================

satisfaction_effect = (
    0.85
    + (
        df["customer_satisfaction"] / 5
    ) * 0.15
)

df["units"] *= satisfaction_effect


# ============================================================
# CLEAN UNITS
# ============================================================

df["units"] = df["units"].clip(
    lower=1
)

df["units"] = df[
    "units"
].round().astype(int)


# ============================================================
# RETURNS
# ============================================================

df["returns"] = (
    df["units"]
    * np.random.uniform(
        0.01,
        0.06,
        NUM_ROWS
    )
).round().astype(int)


# A small increase in returns in the affected area.

df.loc[
    interaction_condition,
    "returns"
] += np.random.randint(
    1,
    4,
    interaction_condition.sum()
)


# ============================================================
# CALCULATE REALIZED SALES
# ============================================================

df["sales"] = (
    df["units"]
    * df["price"]
    * (
        1
        - df["discount_pct"] / 100
    )
)


# Subtract returned product value.

df["sales"] -= (
    df["returns"]
    * df["price"]
)


# Add realistic measurement/business noise.

df["sales"] *= np.random.normal(
    1.0,
    0.04,
    NUM_ROWS
)


# Sales cannot be negative.

df["sales"] = df[
    "sales"
].clip(
    lower=0
).round(2)
# ============================================================
# KEEP ONLY BUSINESS-FACING COLUMNS
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
        "inventory_availability",
        "marketing_spend",
        "competitor_price_index",
        "customer_satisfaction"
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
# SAVE MAIN DATASET
# ============================================================

output_path = (
    DATA_DIR
    / "realistic_sales_v2.csv"
)

df.to_csv(
    output_path,
    index=False
)


# ============================================================
# BASIC SUMMARY
# ============================================================

print("=" * 60)
print("INSIGHTPILOT DATASET GENERATED")
print("=" * 60)

print()

print("Rows:", len(df))
print("Columns:", len(df.columns))

print()

print(
    "Date Range:",
    df["date"].min().date(),
    "→",
    df["date"].max().date()
)

print()

print("Metrics:")

print(
    [
        "sales",
        "units",
        "price",
        "discount_pct",
        "returns",
        "inventory_availability",
        "marketing_spend",
        "competitor_price_index",
        "customer_satisfaction"
    ]
)

print()

print("Dimensions:")

print(
    [
        "region",
        "product",
        "category",
        "channel",
        "customer_type",
        "customer_segment"
    ]
)

print()

print("Saved to:")

print(output_path)

print()

print(
    "Primary scenario:"
)

print(
    "June 2026 → South + Product B + Online "
    "inventory shortage"
)

print("=" * 60)