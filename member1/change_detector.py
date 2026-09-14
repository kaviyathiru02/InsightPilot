import pandas as pd


def detect_change(
    df,
    metric,
    date_column,
    granularity="auto"
):
    """
    Detect change in a metric between the
    latest two time periods.

    granularity:
        auto
        day
        week
        month
        quarter
        year
    """

    data = df.copy()

    # -----------------------------------
    # 1. Convert date column
    # -----------------------------------

    data[date_column] = pd.to_datetime(
        data[date_column],
        errors="coerce",
        format="mixed"
    )

    data = data.dropna(
        subset=[date_column]
    )

    if data.empty:
        raise ValueError(
            "No valid dates found."
        )

    # -----------------------------------
    # 2. Validate metric
    # -----------------------------------

    if metric not in data.columns:
        raise ValueError(
            f"Metric '{metric}' not found."
        )

    if not pd.api.types.is_numeric_dtype(
        data[metric]
    ):
        raise ValueError(
            f"Metric '{metric}' must be numeric."
        )

    # -----------------------------------
    # 3. Determine granularity
    # -----------------------------------

    if granularity == "auto":

        unique_dates = data[date_column].dt.normalize().nunique()

        date_span = (
            data[date_column].max()
            - data[date_column].min()
        ).days

        if unique_dates <= 12:
            granularity = "month"

        elif date_span <= 31:
            granularity = "day"

        elif date_span <= 120:
            granularity = "week"

        else:
            granularity = "month"

    # -----------------------------------
    # 4. Create time periods
    # -----------------------------------

    if granularity == "day":

        data["_period"] = (
            data[date_column]
            .dt.to_period("D")
        )

    elif granularity == "week":

        data["_period"] = (
            data[date_column]
            .dt.to_period("W")
        )

    elif granularity == "month":

        data["_period"] = (
            data[date_column]
            .dt.to_period("M")
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

    # -----------------------------------
    # 5. Aggregate metric by period
    # -----------------------------------

    period_values = (
        data.groupby("_period")[metric]
        .sum()
        .sort_index()
    )

    if len(period_values) < 2:
        raise ValueError(
            "At least two time periods "
            "are required."
        )

    # -----------------------------------
    # 6. Get latest two periods
    # -----------------------------------

    previous_period = period_values.index[-2]
    current_period = period_values.index[-1]

    previous_value = period_values.iloc[-2]
    current_value = period_values.iloc[-1]

    # -----------------------------------
    # 7. Calculate change
    # -----------------------------------

    absolute_change = (
        current_value - previous_value
    )

    if previous_value != 0:

        percentage_change = (
            absolute_change
            / previous_value
        ) * 100

    else:

        percentage_change = None

    # -----------------------------------
    # 8. Determine direction
    # -----------------------------------

    if absolute_change > 0:

        direction = "increase"

    elif absolute_change < 0:

        direction = "decrease"

    else:

        direction = "no_change"

    # -----------------------------------
    # 9. Return structured result
    # -----------------------------------

    return {
        "metric": metric,

        "granularity": granularity,

        "previous_period": str(
            previous_period
        ),

        "current_period": str(
            current_period
        ),

        "previous_value": float(
            previous_value
        ),

        "current_value": float(
            current_value
        ),

        "absolute_change": float(
            absolute_change
        ),

        "percentage_change": (
            round(
                float(percentage_change),
                2
            )
            if percentage_change is not None
            else None
        ),

        "direction": direction
    }