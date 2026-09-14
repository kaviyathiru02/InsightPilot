import json
from pathlib import Path


BASE_DIR = Path(__file__).resolve().parent.parent
DATA_DIR = BASE_DIR / "data"


def load_json_file(filename):
    """
    Load a JSON file from the shared data directory.
    """
    file_path = DATA_DIR / filename

    if not file_path.exists():
        return {
            "success": False,
            "error": f"{filename} was not found."
        }

    try:
        with open(file_path, "r", encoding="utf-8") as file:
            data = json.load(file)

        return {
            "success": True,
            "data": data
        }

    except json.JSONDecodeError:
        return {
            "success": False,
            "error": f"{filename} contains invalid JSON."
        }

    except Exception as e:
        return {
            "success": False,
            "error": str(e)
        }


def get_member1_analysis():
    """
    Get the data analysis produced by Member 1.
    """
    return load_json_file("member1_output.json")


def get_member2_insights():
    """
    Get the insights and candidate root causes produced by Member 2.
    """
    return load_json_file("member2_output.json")


def get_member3_validation():
    """
    Get the root-cause validation produced by Member 3.
    """
    return load_json_file("member3_output.json")


def get_all_analysis():
    """
    Load outputs from Members 1, 2, and 3.
    """
    return {
        "member1": get_member1_analysis(),
        "member2": get_member2_insights(),
        "member3": get_member3_validation()
    }


if __name__ == "__main__":
    result = get_all_analysis()

    print("InsightPilot - Member 4")
    print("=" * 40)

    for member, output in result.items():
        if output["success"]:
            print(f"{member}: Loaded successfully")
        else:
            print(f"{member}: ERROR - {output['error']}")