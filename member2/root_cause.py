import pandas as pd


def find_root_causes(csv_path):
    df = pd.read_csv(csv_path)
    df["date"] = pd.to_datetime(df["date"])

    df["month"] = df["date"].dt.to_period("M")

    months = sorted(df["month"].unique())

    previous_month = months[-2]
    current_month = months[-1]

    previous = df[df["month"] == previous_month]
    current = df[df["month"] == current_month]

    grouped_previous = (
        previous
        .groupby(["region", "product", "channel"])
        .agg(
            sales=("sales", "sum"),
            inventory=("inventory_availability", "mean")
        )
        .reset_index()
    )

    grouped_current = (
        current
        .groupby(["region", "product", "channel"])
        .agg(
            sales=("sales", "sum"),
            inventory=("inventory_availability", "mean")
        )
        .reset_index()
    )

    merged = grouped_previous.merge(
        grouped_current,
        on=["region", "product", "channel"],
        suffixes=("_previous", "_current")
    )

    merged["sales_change_pct"] = (
        (merged["sales_current"] - merged["sales_previous"])
        / merged["sales_previous"]
    ) * 100

    causes = []

    for _, row in merged.iterrows():

        if (
            row["sales_change_pct"] < -20
            and row["inventory_current"] < 0.70
        ):
            causes.append({
                "region": row["region"],
                "product": row["product"],
                "channel": row["channel"],
                "sales_change_pct": round(
                    row["sales_change_pct"], 2
                ),
                "inventory_availability": round(
                    row["inventory_current"], 3
                ),
                "root_cause": "Inventory shortage",
                "recommendation": (
                    "Increase inventory availability and "
                    "prioritize replenishment."
                )
            })

    return causes