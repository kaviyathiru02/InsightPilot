from root_cause import find_root_causes


causes = find_root_causes("data/realistic_sales_v2.csv")


print("=" * 70)
print("INSIGHTPILOT - ROOT CAUSE DETECTOR")
print("=" * 70)

for cause in causes:
    print(cause)

print("=" * 70)
print(f"Total root causes detected: {len(causes)}")