from pydantic import BaseModel, Field


class MatchResult(BaseModel):

    overall_score: int = Field(
        description="Overall match score from 0 to 100"
    )

    recommendation: str = Field(
        description="Final recommendation such as Strong Match, Good Match, Possible Match, or Poor Match"
    )

    matched_skills: list[str] = Field(
        description="Skills from the job that the candidate already has"
    )

    missing_skills: list[str] = Field(
        description="Important job skills that the candidate does not clearly have"
    )

    strengths: list[str] = Field(
        description="Reasons why the candidate is a strong fit"
    )

    concerns: list[str] = Field(
        description="Potential weaknesses, eligibility issues, or concerns"
    )

    explanation: str = Field(
        description="Clear explanation of why the candidate matches or does not match the job"
    )