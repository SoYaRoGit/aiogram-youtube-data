from aiogram import Router
from aiogram.types import Message
from aiogram.filters import CommandStart, CommandObject, Command
from lexicon.lexicon_ru import LEXICON_RU


handler_router = Router()


@handler_router.message(CommandStart())
async def cmd_start(message: Message):
    await message.delete()
    await message.answer(
        text=LEXICON_RU['cmd_start'].format(message.from_user.username)
    )