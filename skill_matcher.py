from candidate_profile import CandidateProfile
from job_extractor import JobInformation


def normalize_skill(skill: str) -> str:
    """
    Converts a skill into a consistent format
    so that small differences in capitalization
    or spacing do not affect matching.
    """

    return (
        skill
        .lower()
        .strip()
        .replace("-", " ")
        .replace("_", " ")
    )


def calculate_skill_match(
    candidate: CandidateProfile,
    job: JobInformation
):
    """
    Compares the candidate's skills with the
    skills required by the job.

    Returns:
        matched_skills
        missing_skills
        skill_match_percentage
    """

    # Normalize candidate skills

    candidate_skills = {
        normalize_skill(skill)
        for skill in candidate.skills
    }

    # Normalize job-required skills

    job_skills = {
        normalize_skill(skill)
        for skill in job.skills
    }

    # Find matching skills

    matched_skills = sorted(
        job_skills.intersection(candidate_skills)
    )

    # Find missing skills

    missing_skills = sorted(
        job_skills.difference(candidate_skills)
    )

    # Calculate percentage

    if not job_skills:
        skill_match_percentage = 0

    else:
        skill_match_percentage = (
            len(matched_skills)
            / len(job_skills)
        ) * 100

    return (
        matched_skills,
        missing_skills,
        round(skill_match_percentage)
    )


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


    matched_skills, missing_skills, percentage = calculate_skill_match(
        candidate,
        job
    )


    print("\n========== SKILL MATCH ==========\n")

    print(
        "Skill Match:",
        percentage,
        "%"
    )


    print("\nMatched Skills:")

    for skill in matched_skills:
        print("-", skill)


    print("\nMissing Skills:")

    for skill in missing_skills:
        print("-", skill)