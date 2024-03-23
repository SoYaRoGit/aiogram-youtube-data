from aiogram import Bot
from aiogram.types import BotCommand
from lexicon.lexicon_ru import LEXICON_COMMANDS_RU


def get_command_menu() -> list[BotCommand]:
    """
    Функция для получения списка команд и их описаний из словаря LEXICON_COMMANDS_RU.

    Returns:
        list[BotCommand]: Список объектов BotCommand, содержащих команды и их описания.
    """
    command_menu = [
        BotCommand(
            command=command,
            description=description
        ) for command, description in LEXICON_COMMANDS_RU.items()
    ]
    return command_menu


async def set_main_menu(bot: Bot):
    """
    Функция для установки команд бота как основного меню.

    Args:
        bot (Bot): Объект бота, для которого нужно установить команды.

    Returns:
        None
    """
    await bot.set_my_commands(get_command_menu())