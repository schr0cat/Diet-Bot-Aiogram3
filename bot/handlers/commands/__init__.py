from aiogram import Router
from aiogram.filters import Command, StateFilter
from bot.handlers.commands.start import (cmd_start, change_minute, add_minute, InputTime, change_second, add_second,
                                         cmd_set_interval, change_data)


def commands_register(router: Router):
    router.message.register(cmd_start, Command(commands='start'))
    router.message.register(cmd_set_interval, Command(commands='set'))
    router.message.register(change_second, Command(commands='sec'))
    router.message.register(change_minute, Command(commands='min'))

    router.message.register(change_data, StateFilter(InputTime.choosing_data))
    router.message.register(add_minute, StateFilter(InputTime.choosing_minutes))
    router.message.register(add_second, StateFilter(InputTime.choosing_seconds))
