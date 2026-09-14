from orchestrator import build_analysis_context
from recommendation import generate_recommendation


def local_recommendation(user_question, analysis, recommendation):
    """
    Local Member 4 recommendation.
    Does not depend on Gemini.
    """

    member1 = analysis["member1"]
    member3 = analysis["member3"]

    # ==============================================
    # OVERALL CHANGE
    # ==============================================

    overall = member1.get("overall_change", {})

    previous_sales = overall.get(
        "previous_value", 0
    )

    current_sales = overall.get(
        "current_value", 0
    )

    absolute_change = overall.get(
        "absolute_change", 0
    )

    percentage_change = overall.get(
        "percentage_change", 0
    )

    previous_period = overall.get(
        "previous_period", "previous period"
    )

    current_period = overall.get(
        "current_period", "current period"
    )

    # ==============================================
    # DIMENSION ANALYSIS
    # ==============================================

    dimension_analysis = member1.get(
        "dimension_analysis", {}
    )

    regions = dimension_analysis.get(
        "region", {}
    ).get("results", [])

    products = dimension_analysis.get(
        "product", {}
    ).get("results", [])

    channels = dimension_analysis.get(
        "channel", {}
    ).get("results", [])

    customer_types = dimension_analysis.get(
        "customer_type", {}
    ).get("results", [])

    # ==============================================
    # HELPER
    # ==============================================

    def get_change(results, name):

        for item in results:

            value = item.get(
                "dimension_value",
                ""
            )

            if value.lower() == name.lower():

                return item.get(
                    "percentage_change",
                    0
                )

        return 0

    north_change = get_change(
        regions,
        "North"
    )

    south_change = get_change(
        regions,
        "South"
    )

    online_change = get_change(
        channels,
        "Online"
    )

    returning_change = get_change(
        customer_types,
        "Returning"
    )

    product_b_change = get_change(
        products,
        "Product B"
    )

    # ==============================================
    # MEMBER 3 VALIDATION
    # ==============================================

    validated_causes = member3.get(
        "validated_root_causes",
        []
    )

    if validated_causes:

        validation = validated_causes[0]

    else:

        validation = {}

    candidate_cause = validation.get(
        "candidate_cause",
        "No confirmed root cause"
    )

    validation_status = validation.get(
        "validation_status",
        "UNKNOWN"
    )

    reliability_level = validation.get(
        "reliability_level",
        "UNKNOWN"
    )

    reliability_score = validation.get(
        "evidence_reliability_score",
        0
    )

    alternative_causes = validation.get(
        "alternative_causes",
        []
    )

    missing_evidence = validation.get(
        "missing_evidence",
        []
    )

    region = validation.get(
        "region",
        "South"
    )

    product = validation.get(
        "product",
        "Product B"
    )

    channel = validation.get(
        "channel",
        "Online"
    )

    candidate_sales_change = validation.get(
        "sales_change_pct",
        0
    )

    inventory_availability = validation.get(
        "inventory_availability",
        0
    )

    # ==============================================
    # BUILD RESPONSE
    # ==============================================

    lines = []

    lines.append(
        "InsightPilot Business Analysis"
    )

    lines.append("")

    lines.append(
        f"Overall sales decreased by "
        f"{abs(percentage_change):.2f}% "
        f"from {previous_period} to {current_period}."
    )

    lines.append(
        f"Sales changed from "
        f"${previous_sales:,.2f} to "
        f"${current_sales:,.2f}."
    )

    lines.append(
        f"The total decrease was "
        f"${abs(absolute_change):,.2f}."
    )

    lines.append("")

    lines.append(
        "Important observed changes"
    )

    lines.append(
        f"North region: {north_change:.2f}%"
    )

    lines.append(
        f"South region: {south_change:.2f}%"
    )

    lines.append(
        f"Online channel: {online_change:.2f}%"
    )

    lines.append(
        f"Returning customers: "
        f"{returning_change:.2f}%"
    )

    lines.append(
        f"Product B: {product_b_change:.2f}%"
    )

    lines.append("")

    lines.append(
        "Possible root cause"
    )

    lines.append(
        f"{candidate_cause} is a leading candidate "
        f"for the {region} / {product} / {channel} segment."
    )

    lines.append(
        f"Sales in this segment changed by "
        f"{candidate_sales_change:.2f}%."
    )

    lines.append(
        f"Observed inventory availability was "
        f"{inventory_availability:.3f}."
    )

    lines.append("")

    lines.append(
        "Evidence validation"
    )

    lines.append(
        f"Validation status: {validation_status}"
    )

    lines.append(
        f"Evidence reliability: {reliability_level}"
    )

    lines.append(
        f"Reliability score: "
        f"{reliability_score:.1f}/100"
    )

    lines.append("")

    lines.append(
        "Important caution"
    )

    lines.append(
        "The inventory shortage is NOT confirmed "
        "as the root cause."
    )

    lines.append(
        "The available evidence is limited, so the "
        "business should not make major decisions "
        "based only on this candidate cause."
    )

    lines.append("")

    lines.append(
        "Alternative explanations"
    )

    for cause in alternative_causes:

        lines.append(
            f"- {cause}"
        )

    lines.append("")

    lines.append(
        "Missing evidence"
    )

    for evidence in missing_evidence:

        lines.append(
            f"- {evidence}"
        )

    lines.append("")

    lines.append(
        "Recommended next steps"
    )

    lines.append(
        "1. Investigate historical inventory and "
        "stockout records."
    )

    lines.append(
        "2. Analyze returning-customer behavior "
        "because returning customer sales declined "
        "substantially."
    )

    lines.append(
        "3. Audit the online sales funnel for possible "
        "conversion or customer-experience problems."
    )

    lines.append(
        "4. Review pricing, promotions, and seasonal "
        "demand changes."
    )

    lines.append(
        "5. Check supplier delivery performance and "
        "product-level inventory availability."
    )

    lines.append("")

    lines.append(
        "Decision guidance"
    )

    lines.append(
        "Prioritize investigation and targeted "
        "corrective actions rather than assuming "
        "inventory shortage is the sole cause of "
        "the overall sales decline."
    )

    return "\n".join(lines)


# ==============================================
# MAIN FUNCTION
# ==============================================

def run_insightpilot(user_question):

    analysis = build_analysis_context()

    if not analysis["success"]:

        return (
            "Unable to load analysis data: "
            + analysis["error"]
        )

    recommendation = generate_recommendation(
        analysis
    )

    if not recommendation["success"]:

        return (
            "Unable to generate recommendation: "
            + recommendation["error"]
        )

    return local_recommendation(
        user_question,
        analysis,
        recommendation
    )


# ==============================================
# TEST
# ==============================================

if __name__ == "__main__":

    print(
        "InsightPilot Member 4 Agent"
    )

    print("=" * 40)

    question = (
        "Why did sales decrease from May 2026 "
        "to June 2026 and what should the "
        "business do next?"
    )

    response = run_insightpilot(
        question
    )

    print()

    print(response)