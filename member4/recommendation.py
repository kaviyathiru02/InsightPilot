def generate_recommendation(analysis):
    """
    Generate an evidence-aware recommendation using
    Member 1, Member 2, and Member 3 outputs.
    """

    if not analysis.get("success"):
        return {
            "success": False,
            "error": "Analysis data is not available."
        }

    member2 = analysis["member2"]
    member3 = analysis["member3"]

    # Get validated root cause information
    validated_causes = member3.get("validated_root_causes", [])

    if not validated_causes:
        return {
            "success": False,
            "error": "No validated root cause data was found."
        }

    validation = validated_causes[0]

    # These values are inside validated_root_causes[0]
    candidate_cause = validation.get(
        "candidate_cause",
        "Unknown"
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

    recommendation = validation.get(
        "recommendation",
        "Investigate the main contributing factors before taking action."
    )

    # Never present an uncertain cause as confirmed
    if (
        validation_status == "UNCERTAIN"
        or reliability_level == "LOW"
    ):

        final_message = (
            f"{candidate_cause} is a leading candidate, "
            f"but it is NOT confirmed. "
            f"The evidence reliability is {reliability_level} "
            f"with a score of {reliability_score}/100, "
            f"and the validation status is {validation_status}. "
            f"Additional evidence should be collected before "
            f"making major operational decisions."
        )

        return {
            "success": True,
            "status": "CAUTION",
            "recommendation": final_message,
            "candidate_cause": candidate_cause,
            "validation_status": validation_status,
            "reliability_level": reliability_level,
            "reliability_score": reliability_score
        }

    # If evidence is sufficiently reliable
    final_message = (
        f"The analysis supports {candidate_cause} as a likely cause. "
        f"Recommended action: {recommendation}"
    )

    return {
        "success": True,
        "status": "RECOMMENDED",
        "recommendation": final_message,
        "candidate_cause": candidate_cause,
        "validation_status": validation_status,
        "reliability_level": reliability_level,
        "reliability_score": reliability_score
    }


if __name__ == "__main__":
    print("InsightPilot - Recommendation Engine")
    print("=" * 45)
    print("Recommendation module loaded successfully.")