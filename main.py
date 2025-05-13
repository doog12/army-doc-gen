from aiogram import Bot, Dispatcher
from aiogram.enums import ParseMode
from aiogram.fsm.storage.memory import MemoryStorage
from aiogram.types import BotCommand
from aiogram.client.default import DefaultBotProperties
import asyncio
import os
from dotenv import load_dotenv
import logging

from handlers import auth, callbacks, faq, help

logging.basicConfig(
    level=logging.INFO,  # или DEBUG, если нужно подробней
    format="%(asctime)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger(__name__)

load_dotenv()
BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")

async def main():
    bot = Bot(
    token=BOT_TOKEN,
    default=DefaultBotProperties(parse_mode=ParseMode.MARKDOWN)
    )
    dp = Dispatcher(storage=MemoryStorage())

    # Регистрация роутеров
    dp.include_router(auth.router)
    # dp.include_router(start.router)
    dp.include_router(callbacks.router)
    dp.include_router(faq.router)
    dp.include_router(help.router)

    # Команды бота (если хочешь)
    await bot.set_my_commands([
        BotCommand(command="start", description="Почати роботу"),
        BotCommand(command="faq", description="FAQ"),
        BotCommand(command="help", description="Помощь")
    ])

    while True:
        try:
        #    logger.info("Запуск polling...")
           await dp.start_polling(bot)
           logger.info("Polling завершен.")
        except Exception as e:
           logger.error(f"Ошибка во время polling: {e}")
           await asyncio.sleep(5)
if __name__ == "__main__":
    asyncio.run(main())
