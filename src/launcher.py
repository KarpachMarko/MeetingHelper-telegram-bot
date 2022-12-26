import logging

from aiogram import Dispatcher
from aiogram.utils import executor

from bot.meeting_bot import MeetingBot
from settings import WEBHOOK_PATH, WEBAPP_HOST, WEBAPP_PORT, WEBHOOK_URL, BOT_TOKEN

meeting_bot = MeetingBot(BOT_TOKEN)
meeting_bot.initialize_dispatcher()
dp = meeting_bot.dispatcher


async def on_startup(dispatcher: Dispatcher):
    logging.warning('Starting connection.')
    await meeting_bot.bot.set_webhook(WEBHOOK_URL, drop_pending_updates=True)


def start():
    logging.basicConfig(level=logging.INFO)
    executor.start_webhook(
        dispatcher=meeting_bot.dispatcher,
        webhook_path=WEBHOOK_PATH,
        skip_updates=True,
        on_startup=on_startup,
        host=WEBAPP_HOST,
        port=WEBAPP_PORT,
    )


if __name__ == '__main__':
    executor.start_polling(meeting_bot.dispatcher, skip_updates=True)
