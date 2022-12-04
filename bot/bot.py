import logging
from aiogram import Bot, types, Dispatcher, filters
from aiogram.utils.executor import start_webhook

from settings import BOT_TOKEN, WEBHOOK_PATH, WEBAPP_HOST, WEBAPP_PORT, WEBHOOK_URL

bot = Bot(token=BOT_TOKEN)
dp = Dispatcher(bot)


async def on_startup(dp):
    logging.warning('Starting connection.')
    await bot.set_webhook(WEBHOOK_URL, drop_pending_updates=True)


def main():
    logging.basicConfig(level=logging.INFO)
    start_webhook(
        dispatcher=dp,
        webhook_path=WEBHOOK_PATH,
        skip_updates=True,
        on_startup=on_startup,
        host=WEBAPP_HOST,
        port=WEBAPP_PORT,
    )
