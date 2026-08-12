import os
from dotenv import load_dotenv
from langchain_google_genai import ChatGoogleGenerativeAI

load_dotenv()

GEMINI_API_KEY=os.getenv("GEMINI_API_KEY")

if not GEMINI_API_KEY:
    raise ValueError("GEMINI_API_KEY NOT FOUND IN .env")


llm=ChatGoogleGenerativeAI(model="gemini-3.5-flash",google_api_key=GEMINI_API_KEY,temperature=0)


response=llm.invoke("Explain what an ai agents is in 2 sentence")

print("Gemini connected sucessfully\n")
print("\nResponse:")
print(response.content[0]["text"])