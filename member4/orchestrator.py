from tools import (
    get_member1_analysis,
    get_member2_insights,
    get_member3_validation
)


def collect_all_analysis():
    """
    Collect analysis from Member 1, Member 2, and Member 3.
    """

    member1 = get_member1_analysis()
    member2 = get_member2_insights()
    member3 = get_member3_validation()

    return {
        "member1": member1,
        "member2": member2,
        "member3": member3
    }


def build_analysis_context():
    """
    Build a simple context that Member 4 can use
    to make evidence-aware recommendations.
    """

    analysis = collect_all_analysis()

    if not analysis["member1"]["success"]:
        return {
            "success": False,
            "error": "Member 1 analysis could not be loaded."
        }

    if not analysis["member2"]["success"]:
        return {
            "success": False,
            "error": "Member 2 insights could not be loaded."
        }

    if not analysis["member3"]["success"]:
        return {
            "success": False,
            "error": "Member 3 validation could not be loaded."
        }

    return {
        "success": True,
        "member1": analysis["member1"]["data"],
        "member2": analysis["member2"]["data"],
        "member3": analysis["member3"]["data"]
    }


if __name__ == "__main__":
    print("InsightPilot - Member 4 Orchestrator")
    print("=" * 45)

    result = build_analysis_context()

    if result["success"]:
        print("Member 1 analysis: Loaded")
        print("Member 2 insights: Loaded")
        print("Member 3 validation: Loaded")
        print()
        print("All analysis successfully collected.")
    else:
        print("ERROR:", result["error"])