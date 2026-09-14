import pandas as pd


def profile_data(df, date_columns=None):
    """
    Analyze the structure of the dataset and return
    a structured data profile.
    """

    profile = {}

    # -----------------------------
    # 1. Basic information
    # -----------------------------
    profile["rows"] = len(df)
    profile["columns"] = len(df.columns)

    # -----------------------------
    # 2. Numeric columns
    # -----------------------------
    numeric_columns = (
        df.select_dtypes(include="number")
        .columns
        .tolist()
    )

    profile["numeric_columns"] = numeric_columns

    # -----------------------------
    # 3. Date columns
    # -----------------------------
    if date_columns is None:
        date_columns = []

    profile["date_columns"] = date_columns

    # -----------------------------
    # 4. Dimension candidates
    # -----------------------------
    dimensions = []

    for column in df.columns:

        if column in numeric_columns:
            continue

        if column in date_columns:
            continue

        dimensions.append(column)

    profile["dimensions"] = dimensions

    # -----------------------------
    # 5. Date range
    # -----------------------------
    profile["date_range"] = {}

    if date_columns:

        date_column = date_columns[0]

        dates = pd.to_datetime(
            df[date_column],
            errors="coerce",
            format="mixed"
        )

        valid_dates = dates.dropna()

        if not valid_dates.empty:
            profile["date_range"] = {
                "start": valid_dates.min().strftime("%Y-%m-%d"),
                "end": valid_dates.max().strftime("%Y-%m-%d")
            }

    # -----------------------------
    # 6. Unique values
    # -----------------------------
    unique_values = {}

    for column in dimensions:

        values = (
            df[column]
            .dropna()
            .unique()
            .tolist()
        )

        unique_values[column] = values

    profile["unique_values"] = unique_values

    return profile