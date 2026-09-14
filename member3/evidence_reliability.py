"""
Member 3 - Evidence Reliability Scorer

Calculates an Evidence Reliability Score using:
- Supporting evidence
- Contradictory evidence
- Sample size
- Data quality
- Missing evidence
- Confounders
"""


class EvidenceReliabilityScorer:
    """Calculate a transparent evidence reliability score."""

    def calculate(
        self,
        supporting_evidence=0,
        contradictory_evidence=0,
        sample_size=0,
        data_quality="GOOD",
        missing_evidence=0,
        confounders=0,
    ):
        """
        Calculate evidence reliability from 0 to 100.

        Higher score = stronger and more reliable evidence.
        """

        # Start with a neutral score.
        score = 50.0

        # Supporting evidence increases reliability.
        score += min(supporting_evidence * 8, 24)

        # Contradictory evidence decreases reliability.
        score -= min(contradictory_evidence * 8, 24)

        # Sample size contribution.
        if sample_size >= 10000:
            score += 15
        elif sample_size >= 5000:
            score += 10
        elif sample_size >= 1000:
            score += 5
        elif sample_size > 0:
            score += 2
        else:
            score -= 10

        # Data quality contribution.
        quality = str(data_quality).strip().upper()

        if quality == "GOOD":
            score += 10
        elif quality == "FAIR":
            score += 5
        elif quality == "POOR":
            score -= 10
        else:
            score -= 5

        # Missing evidence reduces reliability.
        score -= min(missing_evidence * 4, 20)

        # Confounders reduce reliability.
        score -= min(confounders * 3, 15)

        # Keep score between 0 and 100.
        score = max(0, min(100, score))

        return round(score, 2)

    def get_reliability_level(self, score):
        """Convert the reliability score into a simple level."""

        if score >= 75:
            return "HIGH"
        elif score >= 50:
            return "MEDIUM"
        else:
            return "LOW"


def calculate_evidence_reliability(
    supporting_evidence=0,
    contradictory_evidence=0,
    sample_size=0,
    data_quality="GOOD",
    missing_evidence=0,
    confounders=0,
):
    """Convenience function for evidence reliability calculation."""

    scorer = EvidenceReliabilityScorer()

    score = scorer.calculate(
        supporting_evidence=supporting_evidence,
        contradictory_evidence=contradictory_evidence,
        sample_size=sample_size,
        data_quality=data_quality,
        missing_evidence=missing_evidence,
        confounders=confounders,
    )

    level = scorer.get_reliability_level(score)

    return {
        "evidence_reliability_score": score,
        "reliability_level": level,
    }


if __name__ == "__main__":
    # Example evidence for the Inventory shortage hypothesis.
    result = calculate_evidence_reliability(
        supporting_evidence=3,
        contradictory_evidence=2,
        sample_size=20000,
        data_quality="GOOD",
        missing_evidence=5,
        confounders=5,
    )

    print("Evidence Reliability Score")
    print("=" * 40)
    print("Score:", result["evidence_reliability_score"])
    print("Reliability Level:", result["reliability_level"])