"""
Member 3 - Confounder Detector

Checks whether another variable could influence both the
candidate cause and the observed sales outcome.
"""


class ConfoundDetector:
    """Detect plausible confounding factors."""

    CONFOUNDERS = {
        "Inventory shortage": [
            "Seasonality",
            "Customer demand",
            "Supplier performance",
            "Pricing",
            "Promotional activity",
        ],
        "Marketing decline": [
            "Seasonality",
            "Pricing",
            "Competitor activity",
            "Product availability",
            "Customer demand",
        ],
        "Pricing issue": [
            "Competitor pricing",
            "Seasonality",
            "Promotional activity",
            "Customer segment",
            "Product availability",
        ],
        "Customer behavior": [
            "Pricing",
            "Seasonality",
            "Product availability",
            "Marketing activity",
            "Competitor activity",
        ],
    }

    def detect(self, candidate_cause):
        """Return plausible confounders for a candidate cause."""

        if not candidate_cause:
            return []

        cause = str(candidate_cause).strip()

        for known_cause, confounders in self.CONFOUNDERS.items():
            if cause.lower() == known_cause.lower():
                return confounders

        return [
            "Seasonality",
            "Pricing",
            "Customer demand",
            "Product availability",
            "Competitor activity",
        ]


def detect_confounders(candidate_cause):
    """Convenience function for confounder detection."""
    detector = ConfoundDetector()
    return detector.detect(candidate_cause)


if __name__ == "__main__":
    cause = "Inventory shortage"

    confounders = detect_confounders(cause)

    print("Candidate Cause:", cause)
    print("\nPotential Confounders:")

    for confounder in confounders:
        print("-", confounder)