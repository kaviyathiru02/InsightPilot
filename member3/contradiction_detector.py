"""
Member 3 - Contradictory Evidence Detector

Identifies evidence that conflicts with a candidate cause.
"""


class ContradictionDetector:
    """Detect evidence that weakens a candidate explanation."""

    CONTRADICTIONS = {
        "Inventory shortage": [
            "Some products may show normal inventory availability "
            "despite the sales decline.",
            "If sales declined in locations with adequate inventory, "
            "inventory shortage may not explain the entire decline.",
            "If stockouts were rare, inventory shortage is less likely "
            "to be the primary cause.",
        ],
        "Marketing decline": [
            "Sales may have declined even where marketing activity remained stable.",
            "If customers exposed to normal marketing also reduced purchases, "
            "marketing may not explain the decline.",
            "Stable campaign performance would weaken the marketing hypothesis.",
        ],
        "Pricing issue": [
            "Sales may have declined even where prices remained unchanged.",
            "If competitors also experienced a decline, pricing may not be "
            "the primary explanation.",
            "Stable customer demand despite price changes would weaken the hypothesis.",
        ],
        "Customer behavior": [
            "Some customer segments may show stable purchasing behavior.",
            "If sales declined without a measurable behavior change, "
            "customer behavior may not be the main cause.",
            "External factors may explain the sales decline instead.",
        ],
    }

    DEFAULT_CONTRADICTIONS = [
        "Some unaffected groups may show the same outcome.",
        "The outcome may have occurred before the candidate cause appeared.",
        "Another variable may explain the observed change.",
        "The available evidence may not establish causation.",
    ]

    def detect(self, candidate_cause):
        """Return potential contradictory evidence."""

        if not candidate_cause:
            return []

        cause = str(candidate_cause).strip()

        for known_cause, contradictions in self.CONTRADICTIONS.items():
            if cause.lower() == known_cause.lower():
                return contradictions

        return self.DEFAULT_CONTRADICTIONS


def detect_contradictions(candidate_cause):
    """Convenience function for contradiction detection."""
    detector = ContradictionDetector()
    return detector.detect(candidate_cause)


if __name__ == "__main__":
    cause = "Inventory shortage"

    contradictions = detect_contradictions(cause)

    print("Candidate Cause:", cause)
    print("\nPotential Contradictory Evidence:")

    for contradiction in contradictions:
        print("-", contradiction)