from langchain_google_genai import ChatGoogleGenerativeAI
from dotenv import load_dotenv
from candidate_profile import CandidateProfile
from pypdf import PdfReader
import os

load_dotenv()

GEMINI_API_KEY= os.getenv("GEMINI_API_KEY")

llm = ChatGoogleGenerativeAI(
    model="gemini-3.5-flash",
    google_api_key=GEMINI_API_KEY,
    temperature=0
)

structured_llm = llm.with_structured_output(
    CandidateProfile
)

def extract_resume_text(pdf_path):
    reader = PdfReader(pdf_path)
    text = ""
    for page in reader.pages:
        page_text = page.extract_text()

        if page_text:
            text+=page_text

    return text

def parse_resume(pdf_path):
    resume_text = extract_resume_text(pdf_path)

    prompt = f"""
    You are a resume information extraction assistant.

Analyze the resume below and extract the candidate's information.

Resume:
{resume_text}

Important instructions:

- Extract only information that is actually present in the resume.
- Do not invent skills, experience, education, projects, or preferences.
- For target roles, infer them only when the resume clearly indicates the candidate's career direction.
- For preferred locations and work modes, use the resume only if those preferences are explicitly mentioned.
- Keep technical skills specific and useful for job matching.
"""

    response = structured_llm.invoke(prompt)

    return response


# 5. Test

if __name__ == "__main__":

    resume_path = "resume.pdf"

    result = parse_resume(resume_path)

    print("\nCandidate Profile:\n")

    print(result)

    print("\nName:")
    print(result.name)

    print("\nSkills:")
    print(result.skills)

    print("\nProjects:")
    print(result.projects)