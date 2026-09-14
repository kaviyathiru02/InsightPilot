from data_loader import load_data
from dimension_analysis import analyze_dimension


# Load data
df = load_data("data/realistic_sales_v2.csv")


# Analyze region
result = analyze_dimension(
    df,
    metric="sales",
    date_column="date",
    dimension="region",
    granularity="month"
)


print("DIMENSION CHANGE ANALYSIS")
print("=========================")

print("\nDimension:")
print(result["dimension"])

print("\nPrevious Period:")
print(result["previous_period"])

print("Current Period:")
print(result["current_period"])

print("\nResults:")

for item in result["results"]:

    print(
        f"\n{item['dimension_value']}"
    )

    print(
        f"  Previous: "
        f"{item['previous_value']}"
    )

    print(
        f"  Current: "
        f"{item['current_value']}"
    )

    print(
        f"  Change: "
        f"{item['absolute_change']}"
    )

    print(
        f"  Change %: "
        f"{item['percentage_change']}%"
    )

    print(
        f"  Direction: "
        f"{item['direction']}"
    )