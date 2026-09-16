from pydantic import BaseModel, Field
from langchain_google_genai import ChatGoogleGenerativeAI
from dotenv import load_dotenv
from candidate_profile import CandidateProfile
from job_extractor import JobInformation
import os

load_dotenv()


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


GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")


llm = ChatGoogleGenerativeAI(
    model="gemini-3.6-flash",
    google_api_key=GEMINI_API_KEY,
    temperature=0
)


structure_llm = llm.with_structured_output(MatchResult)


def calculate_rule_score(
    candidate: CandidateProfile,
    job: JobInformation
):

    score = 0
    breakdown = {}

    # Experience
    if candidate.experience and job.experience:
        score += 20
        breakdown["experience"] = 20
    else:
        breakdown["experience"] = 0

    # Education
    if candidate.education:
        score += 5
        breakdown["education"] = 5
    else:
        breakdown["education"] = 0

    # Location
    preferred_locations = [
        location.lower().strip()
        for location in candidate.preferred_locations
    ]

    job_location = job.location.lower().strip()

    if job_location in preferred_locations:
        score += 5
        breakdown["location"] = 5
    else:
        breakdown["location"] = 0

    # Work Mode
    if candidate.preferred_work_modes:

        job_work_mode = getattr(
            job,
            "work_mode",
            ""
        ).lower().strip()

        preferred_modes = [
            mode.lower().strip()
            for mode in candidate.preferred_work_modes
        ]

        if job_work_mode in preferred_modes:
            score += 5
            breakdown["work_mode"] = 5
        else:
            breakdown["work_mode"] = 0

    else:
        breakdown["work_mode"] = 0

    return score, breakdown


def calculate_final_score(
    rule_score: int,
    ai_score: int
):

    # Convert rule score from 0-35 to 0-100
    normalized_rule_score = (
        rule_score / 35
    ) * 100

    # Hybrid weighting
    rule_weight = 0.30
    ai_weight = 0.70

    final_score = (
        normalized_rule_score * rule_weight
        + ai_score * ai_weight
    )

    # Keep score between 0 and 100
    final_score = max(
        0,
        min(100, final_score)
    )

    return round(final_score)
def calculate_skill_score(candidate: CandidateProfile, job: JobInformation):
    candidate_skills = {
        skill.lower().strip()
        for skill in candidate.skills
    }

    job_skills = {
        skill.lower().strip()
        for skill in job.skills
    }

    if not job_skills:
        return 0, [], []

    matched_skills = candidate_skills.intersection(job_skills)
    missing_skills = job_skills - candidate_skills

    score = round(
        (len(matched_skills) / len(job_skills)) * 40
    )

    return score, sorted(matched_skills), sorted(missing_skills)

def match_job(
    candidate: CandidateProfile,
    job: JobInformation
):

    prompt = f"""
You are an expert AI career matching assistant.

Compare the candidate profile with the job information.

CANDIDATE PROFILE:

{candidate.model_dump_json(indent=2)}


JOB INFORMATION:

{job.model_dump_json(indent=2)}


Analyze:

1. How well the candidate's skills match the job requirements.
2. Whether the candidate's experience is relevant.
3. Whether the candidate's projects are relevant.
4. Whether the candidate's education fits the role.
5. Any important missing skills.
6. Any eligibility or experience concerns.
7. Overall suitability for the position.
8. Consider the candidate's target roles.
9. Consider the relevance of the candidate's projects to the job.
10. Give a realistic overall score from 0 to 100.

Do not automatically give a high score.

Scoring guideline:

90-100:
Strong Match

75-89:
Good Match

60-74:
Possible Match

40-59:
Weak Match

0-39:
Poor Match

Return a structured MatchResult.
"""

    response = structure_llm.invoke(prompt)

    return response


if __name__ == "__main__":

    candidate = CandidateProfile(
        name="Sai",

        education=[
            "B.Tech Computer Science & Business Systems"
        ],

        graduation_year=2027,

        experience=[
            "Agentic AI Engineer",
            "AI & Prompt Engineering Intern"
        ],

        skills=[
            "Python",
            "LangChain",
            "RAG",
            "AI Agents",
            "n8n",
            "Gemini",
            "OpenAI",
            "ChromaDB",
            "Pinecone",
            "AWS EC2"
        ],

        projects=[
            "AI Shopping Agent",
            "Multi-Source RAG Support Assistant",
            "AI Email Order Tracker"
        ],

        target_roles=[
            "Agentic AI Engineer",
            "Automation Engineer"
        ],

        preferred_locations=[
            "Chennai",
            "Bangalore",
            "Hyderabad",
            "Dubai"
        ],

        preferred_work_modes=[
            "onsite",
            "hybrid",
            "remote"
        ]
    )


    job = JobInformation(
        company="Example AI Company",

        role="Junior Agentic AI Engineer",

        location="Bangalore",

        skills=[
            "Python",
            "LangChain",
            "RAG",
            "AI Agents",
            "LangGraph",
            "AWS"
        ],

        experience="0-2 years",

        salary="Not mentioned",

        application_link="https://example.com/apply"
    )


    # Rule-based score
    rule_score, breakdown = calculate_rule_score(
        candidate,
        job
    )


    print("\n========== RULE SCORE ==========\n")

    print(
        "Rule Score:",
        rule_score,
        "/ 35"
    )

    print("\nBreakdown:")

    for factor, points in breakdown.items():
        print(
            f"- {factor}: {points}"
        )


    # Gemini AI matching
    result = match_job(
        candidate,
        job
    )


    # Final hybrid score
    final_score = calculate_final_score(
        rule_score,
        result.overall_score
    )


    print("\n========== JOB MATCH ==========\n")

    print(
        "AI Score:",
        result.overall_score,
        "/ 100"
    )

    print(
        "Final Match Score:",
        final_score,
        "/ 100"
    )

    print(
        "Recommendation:",
        result.recommendation
    )


    print("\nMatched Skills:")

    for skill in result.matched_skills:
        print("-", skill)


    print("\nMissing Skills:")

    for skill in result.missing_skills:
        print("-", skill)


    print("\nStrengths:")

    for strength in result.strengths:
        print("-", strength)


    print("\nConcerns:")

    for concern in result.concerns:
        print("-", concern)


    print("\nExplanation:")

    print(result.explanation)

    skill_score, matched_skills, missing_skills = calculate_skill_score(
    candidate,
    job
)

print("\n========== SKILL SCORE ==========\n")
print("Skill Score:", skill_score, "/ 40")

print("Matched Skills:")
for skill in matched_skills:
    print("-", skill)

print("Missing Skills:")
for skill in missing_skills:
    print("-", skill)