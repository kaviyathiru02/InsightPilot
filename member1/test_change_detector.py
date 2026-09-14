from data_loader import load_data
from change_detector import detect_change


# Load dataset
df = load_data("data/realistic_sales_v2.csv")


# Detect sales change
result = detect_change(
    df,
    metric="sales",
    date_column="date"
)


print("CHANGE DETECTION")
print("================")

print("\nMetric:")
print(result["metric"])

print("\nPrevious Period:")
print(result["previous_period"])

print("Previous Value:")
print(result["previous_value"])

print("\nCurrent Period:")
print(result["current_period"])

print("Current Value:")
print(result["current_value"])

print("\nAbsolute Change:")
print(result["absolute_change"])

print("\nPercentage Change:")
print(result["percentage_change"], "%")

print("\nDirection:")
print(result["direction"])