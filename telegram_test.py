import os
import asyncio

from dotenv import load_dotenv
from telegram import Bot


load_dotenv()

TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")

CHAT_ID = "1186829217"


async def main():

    bot = Bot(token=TOKEN)

    await bot.send_message(
        chat_id=CHAT_ID,
        text="🚀 AI Career Agent connected successfully!"
    )

    print("Telegram notification sent successfully! ✅")


asyncio.run(main())