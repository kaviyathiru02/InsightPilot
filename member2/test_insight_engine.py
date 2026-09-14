import json

from insight_engine import generate_insights


with open(
    "data/member1_output.json",
    "r",
    encoding="utf-8"
) as file:
    member1_output = json.load(file)


insights = generate_insights(member1_output)


print("=" * 70)
print("INSIGHTPILOT - MEMBER 2 INSIGHT ENGINE")
print("=" * 70)

for insight in insights:
    print(insight)

print("=" * 70)
print(f"Total insights generated: {len(insights)}")