"""
Member 3 - Alternative Cause Checker

Checks a candidate cause against plausible alternative explanations.
"""


class AlternativeCauseChecker:
    """Generate alternative explanations for a candidate cause."""

    ALTERNATIVE_CAUSES = {
        "Inventory shortage": [
            "Demand spike",
            "Pricing changes",
            "Seasonal demand variation",
            "Supplier delays",
            "Data recording issues",
        ],
        "Marketing decline": [
            "Seasonal demand variation",
            "Pricing changes",
            "Competitor activity",
            "Product availability",
            "Customer behavior changes",
        ],
        "Pricing issue": [
            "Competitor pricing",
            "Seasonal demand variation",
            "Product availability",
            "Customer segment changes",
            "Marketing changes",
        ],
        "Customer behavior": [
            "Pricing changes",
            "Product availability",
            "Competitor activity",
            "Seasonality",
            "Marketing changes",
        ],
    }

    def check(self, candidate_cause):
        """
        Return plausible alternatives for the candidate cause.

        Unknown causes receive a generic set of alternatives.
        """
        if not candidate_cause:
            return []

        cause = str(candidate_cause).strip()

        for known_cause, alternatives in self.ALTERNATIVE_CAUSES.items():
            if cause.lower() == known_cause.lower():
                return alternatives

        return [
            "Seasonal demand variation",
            "Pricing changes",
            "Product availability",
            "Competitor activity",
            "Data quality issues",
        ]


def generate_alternatives(candidate_cause):
    """Convenience function for generating alternative causes."""
    checker = AlternativeCauseChecker()
    return checker.check(candidate_cause)


if __name__ == "__main__":
    cause = "Inventory shortage"

    alternatives = generate_alternatives(cause)

    print("Candidate Cause:", cause)
    print("Alternative Causes:")

    for alternative in alternatives:
        print("-", alternative)