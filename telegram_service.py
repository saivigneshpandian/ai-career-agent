import os

from dotenv import load_dotenv
from telegram import Bot


load_dotenv()


TELEGRAM_BOT_TOKEN = os.getenv(
    "TELEGRAM_BOT_TOKEN"
)


if not TELEGRAM_BOT_TOKEN:
    raise ValueError(
        "TELEGRAM_BOT_TOKEN not found"
    )


bot = Bot(
    token=TELEGRAM_BOT_TOKEN
)


async def send_telegram_message(
    chat_id,
    message
):

    await bot.send_message(
        chat_id=chat_id,
        text=message
    )