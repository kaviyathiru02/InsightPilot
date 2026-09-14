from data_loader import load_data
from validator import validate_data


df = load_data("data/realistic_sales_v2.csv")

report = validate_data(df)

print("DATA VALIDATION REPORT")
print("======================")

print("Rows:", report["rows"])
print("Columns:", report["columns"])

print("\nMissing Values:")
print(report["missing_values"])

print("\nDuplicate Rows:")
print(report["duplicate_rows"])

print("\nNumeric Columns:")
print(report["numeric_columns"])

print("\nData Types:")
print(report["data_types"])

print("\nDate Columns:")
print(report["date_columns"])

print("\nInvalid Dates:")
print(report["invalid_dates"])

print("\nWarnings:")
print(report["warnings"])

print("\nOverall Status:")
print(report["status"])