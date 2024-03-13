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


@handler_router.message(Command('help'))
async def cmd_help(message: Message):
    await message.delete()
    await message.answer(
        text=LEXICON_RU['cmd_help']
    )
    

@handler_router.message(Command('video'))
async def cmd_video(message: Message, command: CommandObject):
    ...


@handler_router.message(Command('playlist'))
async def cmd_playlist(message: Message, command: CommandObject):
    ...


@handler_router.message(Command('channel'))
async def cmd_channel(message: Message, command: CommandObject):
    ...


@handler_router.message(Command('export'))
async def cmd_export(message: Message, command: CommandObject):
    ...