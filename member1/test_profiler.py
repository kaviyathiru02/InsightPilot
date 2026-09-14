from data_loader import load_data
from validator import validate_data
from profiler import profile_data


# Load data
df = load_data("data/realistic_sales_v2.csv")


# Validate data
validation_report = validate_data(df)


# Create profile
profile = profile_data(
    df,
    validation_report["date_columns"]
)


print("DATA PROFILE")
print("============")

print("\nRows:")
print(profile["rows"])

print("\nColumns:")
print(profile["columns"])

print("\nNumeric Columns / Metrics:")
print(profile["numeric_columns"])

print("\nDate Columns:")
print(profile["date_columns"])

print("\nDimensions:")
print(profile["dimensions"])

print("\nDate Range:")
print(profile["date_range"])

print("\nUnique Values:")
for column, values in profile["unique_values"].items():
    print(f"{column}: {values}")