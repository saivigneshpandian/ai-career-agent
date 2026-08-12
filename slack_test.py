'''import os

from dotenv import load_dotenv
from slack_sdk import WebClient


# -----------------------------------------
# 1. Load environment variables
# -----------------------------------------

load_dotenv()


# -----------------------------------------
# 2. Get Slack Bot Token
# -----------------------------------------

SLACK_BOT_TOKEN = os.getenv("SLACK_BOT_TOKEN")

if not SLACK_BOT_TOKEN:
    raise ValueError("SLACK_BOT_TOKEN is not found in .env")


# -----------------------------------------
# 3. Create Slack API client
# -----------------------------------------

client = WebClient(
    token=SLACK_BOT_TOKEN
)


# -----------------------------------------
# 4. Test Slack authentication
# -----------------------------------------

def test_slack_connection():

    response = client.auth_test()

    print("Slack connected successfully! ✅")
    print("Bot:", response["user"])
    print("Workspace:", response["team"])


# -----------------------------------------
# 5. Get available public channels
# -----------------------------------------

def get_channels():

    response = client.conversations_list(
        types="public_channel"
    )

    channels = response["channels"]

    print("\nAvailable Channels:\n")

    for channel in channels:

        print(
            "Channel:",
            channel["name"],
            "| ID:",
            channel["id"]
        )

    return channels


# -----------------------------------------
# 6. Send Slack message
# -----------------------------------------

def send_slack_message(channel_id, message):

    response = client.chat_postMessage(
        channel=channel_id,
        text=message
    )

    print("\nMessage sent successfully! ✅")
    print("Channel ID:", channel_id)

    return response


# -----------------------------------------
# 7. Main program
# -----------------------------------------

if __name__ == "__main__":

    # Test connection
    test_slack_connection()

    # Get channels
    channels = get_channels()

    # Send message to the first available channel
    if channels:

        channel_id = "C0BQAACGCP2"

        send_slack_message(
            channel_id,
            "🚨 Interview email detected!"
        )

    else:

        print("No public channels found.")

    print("Message sent successfully! ✅")
    print("Message timestamp:", response["ts"])'''


from slack_service import send_slack_message

CHANNEL_ID = "C0BQAACGCP2"


response = send_slack_message(
    CHANNEL_ID,
    "🚀 AI Career Agent Slack service is working!"
)


print("Message sent successfully! ✅")
print("Message timestamp:", response["ts"])