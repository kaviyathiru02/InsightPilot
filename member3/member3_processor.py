"""
Member 3 - Validation Processor

Reads candidate root causes from Member 2 output,
runs the Member 3 validation engine,
and saves the validated results.
"""

import json

from validation_engine import ValidationEngine


INPUT_FILE = "data/member2_output.json"
OUTPUT_FILE = "data/member3_output.json"


def load_member2_output():
    """Load Member 2 output."""

    with open(INPUT_FILE, "r", encoding="utf-8") as file:
        return json.load(file)


def process_root_causes(data):
    """Validate every root cause produced by Member 2."""

    engine = ValidationEngine()

    validated_causes = []

    for root_cause in data.get("root_causes", []):
        candidate_cause = root_cause.get("root_cause", "")

        # Use the actual evidence available from Member 2.
        sales_change = root_cause.get("sales_change_pct", 0)
        inventory_availability = root_cause.get(
            "inventory_availability"
        )

        # Treat the root-cause record as supporting evidence.
        supporting_evidence = 1

        if sales_change != 0:
            supporting_evidence += 1

        if inventory_availability is not None:
            supporting_evidence += 1

        result = engine.validate(
        candidate_cause=candidate_cause,
        supporting_evidence=supporting_evidence,
        sample_size=20000,
        data_quality="GOOD",
        )

        # Preserve Member 2 information.
        result["region"] = root_cause.get("region")
        result["product"] = root_cause.get("product")
        result["channel"] = root_cause.get("channel")
        result["sales_change_pct"] = sales_change
        result["inventory_availability"] = inventory_availability
        result["recommendation"] = root_cause.get("recommendation")

        validated_causes.append(result)

    return validated_causes


def save_output(results):
    """Save Member 3 output."""

    output = {
        "validated_root_causes": results
    }

    with open(OUTPUT_FILE, "w", encoding="utf-8") as file:
        json.dump(output, file, indent=2)

    return output


def main():
    """Run the Member 3 validation pipeline."""

    data = load_member2_output()

    results = process_root_causes(data)

    output = save_output(results)

    print("=" * 70)
    print("MEMBER 3 OUTPUT CREATED")
    print("=" * 70)
    print("File:", OUTPUT_FILE)
    print("Candidate causes:", len(data.get("root_causes", [])))
    print("Validated results:", len(output["validated_root_causes"]))

    for result in output["validated_root_causes"]:
        print("\nCandidate Cause:", result["candidate_cause"])
        print(
            "Evidence Reliability Score:",
            result["evidence_reliability_score"],
        )
        print(
            "Reliability Level:",
            result["reliability_level"],
        )
        print(
            "Validation Status:",
            result["validation_status"],
        )


if __name__ == "__main__":
    main()