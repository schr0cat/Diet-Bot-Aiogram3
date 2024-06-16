import asyncio

from aiogram import Router, Bot, Dispatcher, BaseMiddleware
from aiogram.types import BotCommand, TelegramObject, Message

from apscheduler.schedulers.asyncio import AsyncIOScheduler

from bot.handlers.commands import commands_register
from bot.handlers.commands.start import register_states_handler
from bot.utils.config_reader import config
from bot.utils.logger import logger


bot = Bot(token=config.token)
dp = Dispatcher()


async def set_bot_commands(bot: Bot):
    commands = [
        BotCommand(command='start', description="Запустить бота"),
    ]
    await bot.set_my_commands(commands)


async def start_up():
    default_router = Router()
    # Создаем экземпляр бота, передаем токен, устанавливаем мод кодировки.
    bot = Bot(token=config.token)
    # Создаем экземпляр диспетчера бота.
    dp = Dispatcher()
    # Привязываем к нему роутер.
    dp.include_router(default_router)

    # scheduler = AsyncIOScheduler()
    # timezone='Europe/Moscow'
    # scheduler.start()

    logger.info("Запуск бота.")
    commands_register(default_router)
    register_states_handler(default_router)

    await set_bot_commands(bot)
    await dp.start_polling(bot, allowed_updates=dp.resolve_used_update_types(), config=config)


if __name__ == '__main__':
    try:
        loop = asyncio.new_event_loop()
        loop.run_until_complete(start_up())
    except (KeyboardInterrupt, SystemExit):
        logger.error("Бот остановлен !")
