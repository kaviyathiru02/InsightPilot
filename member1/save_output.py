import json
from data_processor import process_data


result = process_data(
    "data/realistic_sales_v2.csv",
    metric="sales",
    date_column="date",
    granularity="month"
)


with open(
    "data/member1_output.json",
    "w",
    encoding="utf-8"
) as file:

    json.dump(
        result,
        file,
        indent=4
    )


print("=" * 70)
print("MEMBER 1 PROCESSING COMPLETE")
print("=" * 70)

print("\nOutput saved to:")
print("data/member1_output.json")