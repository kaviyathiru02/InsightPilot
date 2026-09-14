import json

from insight_engine import generate_insights
from root_cause import find_root_causes


def generate_member2_output():
    with open(
        "data/member1_output.json",
        "r",
        encoding="utf-8"
    ) as file:
        member1_output = json.load(file)

    insights = generate_insights(member1_output)

    root_causes = find_root_causes(
        "data/realistic_sales_v2.csv"
    )

    return {
        "overall_change": member1_output["overall_change"],
        "insights": insights,
        "root_causes": root_causes
    }


if __name__ == "__main__":

    output = generate_member2_output()

    with open(
        "data/member2_output.json",
        "w",
        encoding="utf-8"
    ) as file:
        json.dump(output, file, indent=2)

    print("=" * 70)
    print("MEMBER 2 OUTPUT CREATED")
    print("=" * 70)
    print("File: data/member2_output.json")
    print(f"Insights: {len(output['insights'])}")
    print(f"Root causes: {len(output['root_causes'])}")