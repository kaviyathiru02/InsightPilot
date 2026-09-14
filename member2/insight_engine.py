def generate_insights(member1_output):
    """
    Generate business insights from Member 1 analysis.
    """

    insights = []

    overall = member1_output["overall_change"]

    # Overall business change
    if overall["direction"] == "decrease":
        insights.append({
            "type": "overall",
            "severity": "high",
            "message": (
                f"Sales decreased by "
                f"{abs(overall['percentage_change'])}% "
                f"from {overall['previous_period']} "
                f"to {overall['current_period']}."
            )
        })

    # Dimension analysis
    dimensions = member1_output["dimension_analysis"]

    for dimension, analysis in dimensions.items():

        if "error" in analysis:
            continue

        for result in analysis["results"]:

            percentage = result["percentage_change"]

            if percentage is None:
                continue

            if percentage <= -20:
                severity = "high"

            elif percentage <= -10:
                severity = "medium"

            else:
                continue

            insights.append({
                "type": dimension,
                "dimension_value": result["dimension_value"],
                "severity": severity,
                "percentage_change": percentage,
                "message": (
                    f"{dimension} "
                    f"'{result['dimension_value']}' "
                    f"decreased by {abs(percentage)}%."
                )
            })

    return insights