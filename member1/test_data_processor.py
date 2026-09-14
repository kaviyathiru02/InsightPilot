from data_processor import process_data


result = process_data(
    "data/realistic_sales_v2.csv",
    metric="sales",
    date_column="date",
    granularity="month"
)


print("=" * 70)
print("INSIGHTPILOT - MEMBER 1 DATA PROCESSOR")
print("=" * 70)


print("\nDATASET")
print("-" * 70)
print(result["dataset"])


print("\nVALIDATION")
print("-" * 70)
print(result["validation"])


print("\nPROFILE")
print("-" * 70)
print(result["profile"])


print("\nOVERALL CHANGE")
print("-" * 70)
print(result["overall_change"])


print("\nDIMENSION ANALYSIS")
print("-" * 70)

for dimension, analysis in result["dimension_analysis"].items():

    print(f"\n{dimension}:")
    print(analysis)