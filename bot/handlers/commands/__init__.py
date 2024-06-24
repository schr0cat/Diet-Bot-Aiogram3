from aiogram import Router
from aiogram.filters import Command, StateFilter
from bot.handlers.commands.start import (cmd_start, add_minute, InputTime,
                                         change_data, add_second, set_time_hours, set_time_minutes, cmd_cancel)


def commands_register(router: Router):
    router.message.register(cmd_start, Command(commands='start'))
    router.message.register(set_time_hours, StateFilter(InputTime.choosing_time_hour))
    router.message.register(set_time_minutes, StateFilter(InputTime.choosing_time_minute))
    router.message.register(cmd_cancel, Command(commands='cancel'))

    router.message.register(change_data, StateFilter(InputTime.choosing_data))
    router.message.register(add_minute, StateFilter(InputTime.choosing_minutes))
    router.message.register(add_second, StateFilter(InputTime.choosing_seconds))

