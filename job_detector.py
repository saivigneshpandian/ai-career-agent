from langchain_core import prompt_values
import os
from dotenv import load_dotenv
from langchain_google_genai import ChatGoogleGenerativeAI
from gmail_tool import gmail_latest_emails


load_dotenv()

GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

llm = ChatGoogleGenerativeAI(
    model="gemini-3.5-flash",
    google_api_key=GEMINI_API_KEY,
    temperature=0
)

def detect_job_email(email):
    prompt=f"""You are a job email classifier.

    Analyze the email below and determine whether it is related to a
    job opportunity.

    Return ONLY one of these two values:

    JOB
    NON_JOB

    Email:
    From: {email.get("from", "")}
    Subject: {email.get("subject", "")}
    Body: {email.get("body", "")}
    """

    response = llm.invoke(prompt)

    if isinstance(response.content, list):
        return response.content[0]["text"].strip()

    return response.content.strip()


# --------------------------------
# Test with Gmail
# --------------------------------

emails = gmail_latest_emails.invoke({})

print("\nJob Email Detection:\n")

for email in emails:

    result = detect_job_email(email)

    print("--------------------------------")
    print("Subject:", email.get("subject"))
    print("From:", email.get("from"))
    print("Classification:", result)