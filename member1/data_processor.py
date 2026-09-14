from data_loader import load_data
from validator import validate_data
from profiler import profile_data
from change_detector import detect_change
from dimension_analysis import analyze_dimension


def process_data(
    file_path,
    metric="sales",
    date_column="date",
    granularity="month"
):
    """
    Run the complete Member 1 data analysis pipeline.

    Returns one structured dictionary that can be
    passed to Member 2.
    """

    # -----------------------------------
    # 1. Load data
    # -----------------------------------

    df = load_data(file_path)

    # -----------------------------------
    # 2. Validate data
    # -----------------------------------

    validation = validate_data(df)

    # -----------------------------------
    # 3. Profile data
    # -----------------------------------

    date_columns = [date_column]

    profile = profile_data(
        df,
        date_columns=date_columns
    )

    # -----------------------------------
    # 4. Detect overall metric change
    # -----------------------------------

    overall_change = detect_change(
        df,
        metric=metric,
        date_column=date_column,
        granularity=granularity
    )

    # -----------------------------------
    # 5. Analyze dimensions
    # -----------------------------------

    dimension_results = {}

    dimensions = profile["dimensions"]

    for dimension in dimensions:

        try:

            result = analyze_dimension(
                df,
                metric=metric,
                date_column=date_column,
                dimension=dimension,
                granularity=granularity
            )

            dimension_results[dimension] = result

        except Exception as error:

            dimension_results[dimension] = {
                "error": str(error)
            }

    # -----------------------------------
    # 6. Build final Member 1 output
    # -----------------------------------

    return {
        "dataset": {
            "file": file_path,
            "rows": profile["rows"],
            "columns": profile["columns"]
        },

        "validation": validation,

        "profile": profile,

        "overall_change": overall_change,

        "dimension_analysis": dimension_results
    }