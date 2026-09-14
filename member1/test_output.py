import json


with open(
    "data/member1_output.json",
    "r",
    encoding="utf-8"
) as file:

    result = json.load(file)


print("=" * 70)
print("MEMBER 1 OUTPUT TEST")
print("=" * 70)

print("\nDataset:")
print(result["dataset"])

print("\nValidation Status:")
print(result["validation"]["status"])

print("\nOverall Change:")
print(result["overall_change"])

print("\nDimensions:")
print(
    list(
        result["dimension_analysis"].keys()
    )
)