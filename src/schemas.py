"""Pydantic v2 models for structured Gemini responses."""

from __future__ import annotations

from pydantic import BaseModel, Field


class Scenario(BaseModel):
    """A single practice scenario with real-world conflict."""

    title: str = Field(..., description="Short, memorable title for the scenario.")
    category: str = Field(
        ...,
        description="Topic group, e.g. work, sales, relationships.",
    )
    context: str = Field(
        ...,
        description="Background setup — who, where, what is at stake.",
    )
    core_conflict: str = Field(
        ...,
        description="The central tension or disagreement driving the situation.",
    )
    user_role: str = Field(
        ...,
        description="Role the user plays in the scenario.",
    )
    opposing_role: str = Field(
        ...,
        description="Role or party pushing back against the user.",
    )
    question: str = Field(
        ...,
        description="The prompt the user must respond to.",
    )
    skill_focus: list[str] = Field(
        ...,
        min_length=1,
        description="Skills this scenario trains, e.g. persuasion, decision-making.",
    )
    difficulty: str = Field(
        ...,
        description="Difficulty label, e.g. easy, medium, hard.",
    )
    hidden_traps: list[str] = Field(
        default_factory=list,
        description="Subtle pitfalls a weak answer might fall into.",
    )
    success_criteria: list[str] = Field(
        ...,
        min_length=1,
        description="What a strong answer should demonstrate.",
    )


class ScenarioList(BaseModel):
    """Collection of scenarios returned for one practice session."""

    scenarios: list[Scenario] = Field(
        ...,
        min_length=1,
        description="Generated scenarios for the user to choose from.",
    )


class ScoreBreakdown(BaseModel):
    """Per-dimension scores for a user's answer."""

    focus: int = Field(..., ge=0, le=100, description="Stays on the core issue.")
    clarity: int = Field(..., ge=0, le=100, description="Easy to follow.")
    logic: int = Field(..., ge=0, le=100, description="Reasoning is coherent.")
    decision_quality: int = Field(
        ...,
        ge=0,
        le=100,
        description="Chooses a sensible course of action.",
    )
    counter_argument: int = Field(
        ...,
        ge=0,
        le=100,
        description="Anticipates or addresses pushback.",
    )
    persuasiveness: int = Field(
        ...,
        ge=0,
        le=100,
        description="Likely to move the listener.",
    )
    concision: int = Field(
        ...,
        ge=0,
        le=100,
        description="Says enough without rambling.",
    )
    practicality: int = Field(
        ...,
        ge=0,
        le=100,
        description="Actionable in a real situation.",
    )

    def dimension_values(self) -> list[int]:
        """All eight scores in a stable order (for averaging)."""
        return [
            self.focus,
            self.clarity,
            self.logic,
            self.decision_quality,
            self.counter_argument,
            self.persuasiveness,
            self.concision,
            self.practicality,
        ]

    @property
    def average(self) -> float:
        """Unrounded mean of all dimensions."""
        values = self.dimension_values()
        return sum(values) / len(values)


class Feedback(BaseModel):
    """Full coaching feedback after the user's first answer."""

    total_score: int = Field(..., ge=0, le=100, description="Overall score.")
    scores: ScoreBreakdown
    user_intent_summary: str = Field(
        ...,
        description="What the user seems to be trying to communicate.",
    )
    what_user_probably_meant: list[str] = Field(
        ...,
        min_length=1,
        description="Underlying points the user likely intended.",
    )
    what_user_actually_said: list[str] = Field(
        ...,
        min_length=1,
        description="What the written answer actually conveys.",
    )
    gap_analysis: list[str] = Field(
        ...,
        min_length=1,
        description="Gaps between intent and delivery.",
    )
    strengths: list[str] = Field(
        default_factory=list,
        description="What worked in the answer.",
    )
    weaknesses: list[str] = Field(
        default_factory=list,
        description="What weakened the answer.",
    )
    why_listener_may_ignore: list[str] = Field(
        ...,
        min_length=1,
        description="Reasons a listener might dismiss or tune out.",
    )
    missing_points: list[str] = Field(
        default_factory=list,
        description="Important points left unsaid.",
    )
    better_answer_10s: str = Field(
        ...,
        description="Improved answer ~10 seconds long.",
    )
    better_answer_30s: str = Field(
        ...,
        description="Improved answer ~30 seconds long.",
    )
    better_answer_90s: str = Field(
        ...,
        description="Improved answer ~90 seconds long.",
    )
    sharp_closing_sentence: str = Field(
        ...,
        description="One punchy closing line.",
    )
    counter_question: str = Field(
        ...,
        description="Challenging counter-argument or question for round two.",
    )
    next_micro_drill: str = Field(
        ...,
        description="Short follow-up exercise suggestion.",
    )
    main_lesson_today: str = Field(
        ...,
        description="Single key takeaway for the session.",
    )


class CounterFeedback(BaseModel):
    """Feedback after the user responds to the counter-argument."""

    score: int = Field(..., ge=0, le=100, description="Rebuttal score.")
    strong_points: list[str] = Field(
        default_factory=list,
        description="What landed well in the rebuttal.",
    )
    weak_points: list[str] = Field(
        default_factory=list,
        description="What weakened the rebuttal.",
    )
    better_counter_response: str = Field(
        ...,
        description="A stronger version of the user's rebuttal.",
    )
    final_advice: str = Field(
        ...,
        description="Closing coaching advice for the session.",
    )


def validate_score_consistency(
    total_score: int,
    scores: ScoreBreakdown,
    *,
    tolerance: int = 15,
    strict: bool = False,
) -> bool:
    """
    Check whether total_score is roughly aligned with the dimension average.

    Gemini may round total_score differently; default tolerance is ±15 points.
    Set strict=True to raise ValueError instead of returning False.
    """
    avg = round(scores.average)
    ok = abs(total_score - avg) <= tolerance
    if strict and not ok:
        raise ValueError(
            f"total_score ({total_score}) differs from dimension average "
            f"({avg}) by more than {tolerance} points."
        )
    return ok
