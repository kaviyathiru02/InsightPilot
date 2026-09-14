"""
Member 3 - Devil's Advocate

Challenges a candidate cause by asking:
"Is there another reason this evidence could exist?"
"""


class DevilsAdvocate:
    """Challenge candidate causes instead of automatically accepting them."""

    CHALLENGES = {
        "Inventory shortage": [
            "Could the sales decline be caused by lower customer demand instead?",
            "Could pricing changes have reduced sales rather than inventory availability?",
            "Could supplier delays be temporary rather than the main cause?",
            "Could the observed inventory shortage be a result of lower demand?",
        ],
        "Marketing decline": [
            "Could seasonality explain the sales decline instead?",
            "Could product availability be responsible for the decline?",
            "Could competitor activity have reduced customer purchases?",
            "Is there enough marketing data to prove that marketing caused the decline?",
        ],
        "Pricing issue": [
            "Could lower demand explain the decline instead?",
            "Could a competitor's actions be responsible?",
            "Could product availability have affected sales?",
            "Is there enough pricing data to establish a causal relationship?",
        ],
        "Customer behavior": [
            "Could pricing changes have changed customer behavior?",
            "Could product availability have influenced purchasing?",
            "Could seasonal effects explain the observed behavior?",
            "Could the apparent behavior change be caused by a data-quality issue?",
        ],
    }

    DEFAULT_CHALLENGES = [
        "Could another operational factor explain the same outcome?",
        "Could seasonality explain the observed change?",
        "Could pricing changes be responsible instead?",
        "Could product availability be responsible?",
        "Is there enough evidence to establish causation?",
    ]

    def challenge(self, candidate_cause):
        """
        Return skeptical challenges for a candidate cause.
        """
        if not candidate_cause:
            return []

        cause = str(candidate_cause).strip()

        for known_cause, challenges in self.CHALLENGES.items():
            if cause.lower() == known_cause.lower():
                return challenges

        return self.DEFAULT_CHALLENGES


def challenge_cause(candidate_cause):
    """Convenience function for challenging a candidate cause."""
    advocate = DevilsAdvocate()
    return advocate.challenge(candidate_cause)


if __name__ == "__main__":
    cause = "Inventory shortage"

    print("Candidate Cause:", cause)
    print("\nDevil's Advocate Challenges:")

    challenges = challenge_cause(cause)

    for challenge in challenges:
        print("-", challenge)