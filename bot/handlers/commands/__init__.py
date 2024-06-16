from aiogram import Router
from aiogram.filters import Command

# from bot.filters.chat_type import ChatTypeFilter
# from bot.handlers.commands.comments_get import cmd_get_comments
# from bot.handlers.commands.get_in_json import cmd_get_users
# from bot.handlers.commands.group_games import cmd_casino_in_group, cmd_basketball_in_group
# from bot.handlers.commands.test_buttons import cmd_random, send_random_value
from bot.handlers.commands.start import cmd_start


def commands_register(router: Router):
    router.message.register(cmd_start, Command(commands='start'))
    # router.message.register(scheduler)
    # router.callback_query.register(cmd_cancel, text='cancel')
    # router.message.register(cmd_random, Command(commands='random'))
    # router.callback_query.register(send_random_value, text='random_value')
    # router.callback_query.register(cmd_input_info, text='profile_yes')
    # router.callback_query.register(cmd_no_info, text='profile_no')
    # router.message.register(cmd_get_users, Command(commands='get_users'))
    # router.message.register(cmd_get_comments, Command(commands='get_comments'))
    # router.message.register(cmd_casino_in_group, ChatTypeFilter(chat_type=["group", "supergroup"]),
    #                         Command(commands='casino'))
    # router.message.register(cmd_basketball_in_group, ChatTypeFilter(chat_type=["group", "supergroup"]),
    #                         Command(commands='basketball'))