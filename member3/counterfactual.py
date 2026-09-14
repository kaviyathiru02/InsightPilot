"""
Member 3 - Counterfactual Challenge

Tests whether the outcome would still be expected if the
candidate cause were removed.
"""


class CounterfactualAnalyzer:
    """Perform a simple rule-based counterfactual challenge."""

    COUNTERFACTUALS = {
        "Inventory shortage": {
            "question": (
                "If inventory availability were normal, "
                "would the sales decline still be expected?"
            ),
            "expected_effect": (
                "If sales remain below normal despite adequate inventory, "
                "inventory shortage is unlikely to be the only cause."
            ),
            "evidence_needed": [
                "Inventory availability before and during the decline",
                "Sales for products with adequate inventory",
                "Stockout frequency",
            ],
        },
        "Marketing decline": {
            "question": (
                "If marketing activity had remained normal, "
                "would the sales decline still be expected?"
            ),
            "expected_effect": (
                "If sales still declined with normal marketing activity, "
                "marketing decline is unlikely to be the main cause."
            ),
            "evidence_needed": [
                "Marketing spend before and during the decline",
                "Campaign activity",
                "Sales from exposed and unexposed customers",
            ],
        },
        "Pricing issue": {
            "question": (
                "If prices had remained unchanged, "
                "would the sales decline still be expected?"
            ),
            "expected_effect": (
                "If sales still declined without a price change, "
                "pricing is unlikely to be the main cause."
            ),
            "evidence_needed": [
                "Historical prices",
                "Competitor prices",
                "Sales before and after price changes",
            ],
        },
        "Customer behavior": {
            "question": (
                "If customer behavior had remained unchanged, "
                "would the sales decline still be expected?"
            ),
            "expected_effect": (
                "If sales still declined with stable customer behavior, "
                "customer behavior is unlikely to be the main cause."
            ),
            "evidence_needed": [
                "Customer purchase frequency",
                "Customer segment trends",
                "Repeat purchase rates",
            ],
        },
    }

    def analyze(self, candidate_cause):
        """Return a counterfactual challenge for the candidate cause."""

        if not candidate_cause:
            return {
                "candidate_cause": None,
                "counterfactual_question": None,
                "expected_effect": None,
                "evidence_needed": [],
            }

        cause = str(candidate_cause).strip()

        for known_cause, details in self.COUNTERFACTUALS.items():
            if cause.lower() == known_cause.lower():
                return {
                    "candidate_cause": cause,
                    "counterfactual_question": details["question"],
                    "expected_effect": details["expected_effect"],
                    "evidence_needed": details["evidence_needed"],
                }

        return {
            "candidate_cause": cause,
            "counterfactual_question": (
                f"If '{cause}' were removed, "
                "would the sales decline still be expected?"
            ),
            "expected_effect": (
                "If the decline remains, the candidate cause "
                "may not be the primary explanation."
            ),
            "evidence_needed": [
                "Evidence from comparable periods",
                "Evidence from unaffected groups",
                "Evidence before and after the suspected cause",
            ],
        }


def counterfactual_challenge(candidate_cause):
    """Convenience function for counterfactual analysis."""
    analyzer = CounterfactualAnalyzer()
    return analyzer.analyze(candidate_cause)


if __name__ == "__main__":
    cause = "Inventory shortage"

    result = counterfactual_challenge(cause)

    print("Candidate Cause:", result["candidate_cause"])
    print("\nCounterfactual Question:")
    print(result["counterfactual_question"])

    print("\nExpected Effect:")
    print(result["expected_effect"])

    print("\nEvidence Needed:")
    for evidence in result["evidence_needed"]:
        print("-", evidence)