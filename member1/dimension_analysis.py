import pandas as pd


def analyze_dimension(
    df,
    metric,
    date_column,
    dimension,
    granularity="month"
):
    """
    Compare a metric across values of a dimension
    between the latest two time periods.
    """

    data = df.copy()

    # -----------------------------
    # 1. Validate columns
    # -----------------------------

    if metric not in data.columns:
        raise ValueError(
            f"Metric '{metric}' not found."
        )

    if date_column not in data.columns:
        raise ValueError(
            f"Date column '{date_column}' not found."
        )

    if dimension not in data.columns:
        raise ValueError(
            f"Dimension '{dimension}' not found."
        )

    # -----------------------------
    # 2. Convert dates
    # -----------------------------

    data[date_column] = pd.to_datetime(
        data[date_column],
        errors="coerce",
        format="mixed"
    )

    data = data.dropna(
        subset=[date_column]
    )

    # -----------------------------
    # 3. Create periods
    # -----------------------------

    if granularity == "month":

        data["_period"] = (
            data[date_column]
            .dt.to_period("M")
        )

    elif granularity == "week":

        data["_period"] = (
            data[date_column]
            .dt.to_period("W")
        )

    elif granularity == "day":

        data["_period"] = (
            data[date_column]
            .dt.to_period("D")
        )

    elif granularity == "quarter":

        data["_period"] = (
            data[date_column]
            .dt.to_period("Q")
        )

    elif granularity == "year":

        data["_period"] = (
            data[date_column]
            .dt.to_period("Y")
        )

    else:
        raise ValueError(
            "Unsupported granularity."
        )

    # -----------------------------
    # 4. Find latest two periods
    # -----------------------------

    periods = sorted(
        data["_period"].unique()
    )

    if len(periods) < 2:
        raise ValueError(
            "At least two periods are required."
        )

    previous_period = periods[-2]
    current_period = periods[-1]

    # -----------------------------
    # 5. Filter periods
    # -----------------------------

    previous_data = data[
        data["_period"] == previous_period
    ]

    current_data = data[
        data["_period"] == current_period
    ]

    # -----------------------------
    # 6. Aggregate by dimension
    # -----------------------------

    previous_values = (
        previous_data
        .groupby(dimension)[metric]
        .sum()
    )

    current_values = (
        current_data
        .groupby(dimension)[metric]
        .sum()
    )

    # -----------------------------
    # 7. Combine dimension values
    # -----------------------------

    all_values = sorted(
        set(previous_values.index)
        | set(current_values.index)
    )

    results = []

    for value in all_values:

        previous = float(
            previous_values.get(value, 0)
        )

        current = float(
            current_values.get(value, 0)
        )

        change = current - previous

        if previous != 0:

            change_percent = (
                change / previous
            ) * 100

        else:

            change_percent = None

        if change > 0:
            direction = "increase"

        elif change < 0:
            direction = "decrease"

        else:
            direction = "no_change"

        results.append({
            "dimension_value": str(value),
            "previous_value": previous,
            "current_value": current,
            "absolute_change": round(
                change,
                2
            ),
            "percentage_change": (
                round(
                    change_percent,
                    2
                )
                if change_percent is not None
                else None
            ),
            "direction": direction
        })

    # -----------------------------
    # 8. Return result
    # -----------------------------

    return {
        "dimension": dimension,
        "previous_period": str(
            previous_period
        ),
        "current_period": str(
            current_period
        ),
        "results": results
    }