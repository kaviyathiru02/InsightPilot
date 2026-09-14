"""
Member 3 - Validation Engine

Combines all validation modules to evaluate
whether a candidate cause can be trusted.
"""

from alternative_causes import AlternativeCauseChecker
from devils_advocate import DevilsAdvocate
from counterfactual import CounterfactualAnalyzer
from confound_detector import ConfoundDetector
from contradiction_detector import ContradictionDetector
from missing_evidence import MissingEvidenceDetector
from evidence_reliability import EvidenceReliabilityScorer


class ValidationEngine:
    """Validate a candidate cause using multiple evidence checks."""

    def __init__(self):
        self.alternative_checker = AlternativeCauseChecker()
        self.devils_advocate = DevilsAdvocate()
        self.counterfactual = CounterfactualAnalyzer()
        self.confound_detector = ConfoundDetector()
        self.contradiction_detector = ContradictionDetector()
        self.missing_evidence_detector = MissingEvidenceDetector()
        self.reliability_scorer = EvidenceReliabilityScorer()

    def validate(
        self,
        candidate_cause,
        supporting_evidence=0,
        sample_size=0,
        data_quality="GOOD",
    ):
        """Run the complete validation pipeline."""

        alternatives = self.alternative_checker.check(candidate_cause)

        challenges = self.devils_advocate.challenge(candidate_cause)

        counterfactual = self.counterfactual.analyze(candidate_cause)

        confounders = self.confound_detector.detect(candidate_cause)

        contradictions = self.contradiction_detector.detect(candidate_cause)

        missing_evidence = self.missing_evidence_detector.detect(
            candidate_cause
        )

        reliability_score = self.reliability_scorer.calculate(
            supporting_evidence=supporting_evidence,
            contradictory_evidence=len(contradictions),
            sample_size=sample_size,
            data_quality=data_quality,
            missing_evidence=len(missing_evidence),
            confounders=len(confounders),
        )

        reliability_level = self.reliability_scorer.get_reliability_level(
            reliability_score
        )

        # Validation decision is based on evidence reliability.
        if reliability_score >= 75:
            validation_status = "VALIDATED"
        elif reliability_score < 40:
            validation_status = "REJECTED"
        else:
            validation_status = "UNCERTAIN"

        limitations = []

        if missing_evidence:
            limitations.append(
                "Important evidence is missing."
            )

        if contradictions:
            limitations.append(
                "Contradictory evidence exists."
            )

        if confounders:
            limitations.append(
                "Potential confounding factors were identified."
            )

        return {
            "candidate_cause": candidate_cause,
            "alternative_causes": alternatives,
            "devils_advocate_challenges": challenges,
            "counterfactual_analysis": counterfactual,
            "potential_confounders": confounders,
            "contradictory_evidence": contradictions,
            "missing_evidence": missing_evidence,
            "evidence_reliability_score": reliability_score,
            "reliability_level": reliability_level,
            "validation_status": validation_status,
            "limitations": limitations,
        }


if __name__ == "__main__":
    engine = ValidationEngine()

    result = engine.validate(
        candidate_cause="Inventory shortage",
        supporting_evidence=3,
        sample_size=20000,
        data_quality="GOOD",
    )

    print("=" * 70)
    print("MEMBER 3 VALIDATION ENGINE")
    print("=" * 70)

    print("\nCandidate Cause:")
    print(result["candidate_cause"])

    print("\nEvidence Reliability Score:")
    print(result["evidence_reliability_score"])

    print("\nReliability Level:")
    print(result["reliability_level"])

    print("\nValidation Status:")
    print(result["validation_status"])

    print("\nAlternative Causes:")
    for cause in result["alternative_causes"]:
        print("-", cause)

    print("\nDevil's Advocate Challenges:")
    for challenge in result["devils_advocate_challenges"]:
        print("-", challenge)

    print("\nPotential Confounders:")
    for confounder in result["potential_confounders"]:
        print("-", confounder)

    print("\nContradictory Evidence:")
    for contradiction in result["contradictory_evidence"]:
        print("-", contradiction)

    print("\nMissing Evidence:")
    for evidence in result["missing_evidence"]:
        print("-", evidence)

    print("\nLimitations:")
    for limitation in result["limitations"]:
        print("-", limitation)