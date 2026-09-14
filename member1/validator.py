import pandas as pd


def validate_data(df):
    """
    Validate the uploaded dataset and return
    a structured data quality report.
    """

    report = {}

    # -----------------------------
    # 1. Basic dataset information
    # -----------------------------
    report["rows"] = len(df)
    report["columns"] = len(df.columns)

    # -----------------------------
    # 2. Missing values
    # -----------------------------
    missing_values = df.isnull().sum()

    report["missing_values"] = (
        missing_values[missing_values > 0].to_dict()
    )

    # -----------------------------
    # 3. Duplicate rows
    # -----------------------------
    report["duplicate_rows"] = int(
        df.duplicated().sum()
    )

    # -----------------------------
    # 4. Numeric columns
    # -----------------------------
    report["numeric_columns"] = (
        df.select_dtypes(include="number")
        .columns
        .tolist()
    )

    # -----------------------------
    # 5. Data types
    # -----------------------------
    report["data_types"] = {
        column: str(dtype)
        for column, dtype in df.dtypes.items()
    }

    # -----------------------------
    # 6. Date detection
    # -----------------------------
    date_columns = []

    for column in df.columns:

        # Do not treat numeric columns as dates
        if pd.api.types.is_numeric_dtype(df[column]):
            continue

        converted = pd.to_datetime(
            df[column],
            errors="coerce",
            format="mixed"
        )

        valid_dates = converted.notna().sum()

        if len(df) > 0 and valid_dates / len(df) >= 0.8:
            date_columns.append(column)

    report["date_columns"] = date_columns

    # -----------------------------
    # 7. Invalid date count
    # -----------------------------
    invalid_dates = {}

    for column in date_columns:

        converted = pd.to_datetime(
            df[column],
            errors="coerce",
            format="mixed"
        )

        invalid_count = int(
            converted.isna().sum()
        )

        if invalid_count > 0:
            invalid_dates[column] = invalid_count

    report["invalid_dates"] = invalid_dates

    # -----------------------------
    # 8. Warnings
    # -----------------------------
    warnings = []

    if report["missing_values"]:
        warnings.append(
            "Missing values detected."
        )

    if report["duplicate_rows"] > 0:
        warnings.append(
            "Duplicate rows detected."
        )

    if report["invalid_dates"]:
        warnings.append(
            "Invalid dates detected."
        )

    report["warnings"] = warnings

    # -----------------------------
    # 9. Overall status
    # -----------------------------
    if warnings:
        report["status"] = "WARNING"
    else:
        report["status"] = "GOOD"

    return report