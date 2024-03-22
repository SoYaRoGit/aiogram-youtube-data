from aiogram import Bot
from aiogram.types import BotCommand

from lexicon.lexicon_ru import LEXICON_COMMANDS_RU


def get_command_menu() -> list[BotCommand]:
    command_menu = [
        BotCommand(
            command=command,
            description=description
        ) for command, description in LEXICON_COMMANDS_RU.items()
    ]
    return command_menu


# Функция для настройки кнопки Menu бота
async def set_main_menu(bot: Bot):
    await bot.set_my_commands(get_command_menu())