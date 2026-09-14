from data_loader import load_data
from validator import validate_data
from profiler import profile_data
from dimension_analysis import analyze_dimension


# Load data
df = load_data("data/realistic_sales_v2.csv")


# Validate data
validation = validate_data(df)


# Profile data
profile = profile_data(
    df,
    validation["date_columns"]
)


# Get the first date column
date_column = validation["date_columns"][0]


# Analyze every discovered dimension
for dimension in profile["dimensions"]:

    print("\n")
    print("=" * 50)
    print(f"DIMENSION: {dimension}")
    print("=" * 50)

    result = analyze_dimension(
        df=df,
        metric="sales",
        date_column=date_column,
        dimension=dimension,
        granularity="month"
    )

    for item in result["results"]:

        print(
            f"{item['dimension_value']}: "
            f"{item['percentage_change']}% "
            f"({item['direction']})"
        )