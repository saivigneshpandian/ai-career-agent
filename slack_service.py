import os

from dotenv import load_dotenv
from slack_sdk import WebClient

load_dotenv()

SLACK_BOT_TOKEN = os.getenv("SLACK_BOT_TOKEN")

if not SLACK_BOT_TOKEN:
    raise ValueError("SLACK_BOT_TOKEN not found")

client = WebClient(token=SLACK_BOT_TOKEN)


def send_slack_message(channel_id, message):
    """
    Send a text message to a Slack channel.
    """

    response = client.chat_postMessage(
        channel=channel_id,
        text=message
    )

    return response