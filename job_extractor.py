from langchain_google_genai import ChatGoogleGenerativeAI
from dotenv import load_dotenv
from pydantic import BaseModel, Field
import os


load_dotenv()

GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")


# 1. Define Job structure

class JobInformation(BaseModel):

    company: str = Field(
        description="Company name hiring for the role"
    )

    role: str = Field(
        description="Job role or position name"
    )

    location: str = Field(
        description="Job location"
    )

    skills: list[str] = Field(
        description="Required technical skills"
    )

    experience: str = Field(
        description="Required experience"
    )

    salary: str = Field(
        description="Salary information"
    )

    application_link: str = Field(
        description="Job application URL"
    )


# 2. Connect Gemini

llm = ChatGoogleGenerativeAI(
    model="gemini-3.5-flash",
    google_api_key=GEMINI_API_KEY,
    temperature=0
)


# 3. Create structured output model

structured_llm = llm.with_structured_output(
    JobInformation
)


# 4. Extraction function

def extract_job_information(email):

    prompt = f"""

You are a job information extraction assistant.

Extract job details from this email.

Subject:
{email["subject"]}


Body:
{email["body"]}


If information is missing:
Return "Not mentioned".

"""

    response = structured_llm.invoke(prompt)

    return response



# 5. Test

if __name__ == "__main__":

    test_email = {

        "subject":
        "AI Automation Engineer Internship",

        "body":
        """
        XYZ Technologies is hiring
        AI Automation Engineer Intern.

        Location:
        Remote India.

        Required skills:
        Python, LangChain, n8n,
        Generative AI.

        Apply:
        https://xyz.com/jobs
        """

    }


    result = extract_job_information(test_email)


    print("\nExtracted Job Object:\n")

    print(result)


    print("\nCompany:")
    print(result.company)

    print("\nSkills:")
    print(result.skills)