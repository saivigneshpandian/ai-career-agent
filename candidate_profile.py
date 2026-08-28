from pydantic import BaseModel, Field

class CandidateProfile(BaseModel):
    name: str =Field(
        description ="Candidate full name"
    )

    education: list[str] = Field(
        description="Candidate's educational qualifications"
    )

    graduation_year: int = Field(
        description="Expected or completed graduation year"
    )

    experience: list[str] = Field(
        description="Professional work experience"
    )

    skills: list[str] = Field(
        description="Technical and professional skills"
    )

    projects: list[str] = Field(
        description="Important technical projects"
    )

    target_roles: list[str] = Field(
        description="Job roles the candidate is targeting"
    )

    preferred_locations: list[str] = Field(
        description="Preferred job locations"
    )

    preferred_work_modes: list[str] = Field(
        description="Preferred work modes such as onsite, hybrid, or remote"
    )