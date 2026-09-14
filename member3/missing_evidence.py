"""
Member 3 - Missing Evidence Detector

Identifies important evidence that is not currently available
to properly validate a candidate cause.
"""


class MissingEvidenceDetector:
    """Detect evidence needed to validate a candidate explanation."""

    MISSING_EVIDENCE = {
        "Inventory shortage": [
            "Inventory availability data",
            "Stockout frequency",
            "Product-level inventory levels",
            "Sales comparison for products with adequate inventory",
            "Supplier delivery performance",
        ],
        "Marketing decline": [
            "Marketing campaign performance data",
            "Advertising spend before and during the decline",
            "Customer exposure to marketing campaigns",
            "Conversion rates",
            "Competitor marketing activity",
        ],
        "Pricing issue": [
            "Historical product prices",
            "Price changes during the decline",
            "Competitor pricing data",
            "Customer response to price changes",
            "Promotional pricing information",
        ],
        "Customer behavior": [
            "Customer purchase frequency",
            "Customer segment behavior",
            "Customer retention data",
            "Average order value changes",
            "Customer activity before and during the decline",
        ],
    }

    DEFAULT_EVIDENCE = [
        "Historical data before the decline",
        "Data during the decline",
        "Comparison with unaffected groups",
        "Relevant external factors",
        "Sample size information",
    ]

    def detect(self, candidate_cause):
        """Return evidence that is currently missing."""

        if not candidate_cause:
            return []

        cause = str(candidate_cause).strip()

        for known_cause, evidence in self.MISSING_EVIDENCE.items():
            if cause.lower() == known_cause.lower():
                return evidence

        return self.DEFAULT_EVIDENCE


def detect_missing_evidence(candidate_cause):
    """Convenience function for missing evidence detection."""
    detector = MissingEvidenceDetector()
    return detector.detect(candidate_cause)


if __name__ == "__main__":
    cause = "Inventory shortage"

    missing_evidence = detect_missing_evidence(cause)

    print("Candidate Cause:", cause)
    print("\nMissing Evidence:")

    for evidence in missing_evidence:
        print("-", evidence)