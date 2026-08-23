from dataclasses import dataclass


@dataclass(frozen=True)
class Recommendation:
    """
    Represents the final AI recommendation produced by the
    Recommendation Engine.
    """

    summary: str
    recommendation: str
    rationale: str