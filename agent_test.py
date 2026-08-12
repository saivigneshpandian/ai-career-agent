import os

from dotenv import load_dotenv
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.messages import ToolMessage

from gmail_tool import gmail_latest_emails


load_dotenv()

GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

llm = ChatGoogleGenerativeAI(
    model="gemini-3.5-flash",
    google_api_key=GEMINI_API_KEY,
    temperature=0
)

tools = [gmail_latest_emails]

llm_with_tools = llm.bind_tools(tools)


# 1. Ask Gemini
response = llm_with_tools.invoke(
    "Check my latest emails and tell me what emails I have."
)

print("\nTool Calls:")
print(response.tool_calls)


# 2. Execute the requested tool
tool_messages = []

for tool_call in response.tool_calls:

    if tool_call["name"] == "gmail_latest_emails":

        result = gmail_latest_emails.invoke(
            tool_call["args"]
        )

        tool_messages.append(
            ToolMessage(
                content=str(result),
                tool_call_id=tool_call["id"]
            )
        )


# 3. Send tool result back to Gemini
final_response = llm_with_tools.invoke(
    [
        {
            "role": "user",
            "content": "Check my latest emails and tell me what emails I have."
        },
        response,
        *tool_messages
    ]
)


# 4. Final AI answer
print("\nFinal AI Response:")
print(final_response.content)