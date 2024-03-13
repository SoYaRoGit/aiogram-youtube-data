import re
from aiogram import Router, F
from aiogram.types import Message
from aiogram.filters import CommandStart, CommandObject, Command
from lexicon.lexicon_ru import LEXICON_RU


handler_router = Router()

# Description Handlers
@handler_router.message(CommandStart())
async def cmd_start(message: Message):
    await message.delete()
    await message.answer(
        text=LEXICON_RU['cmd_start'].format(message.from_user.username)
    )


@handler_router.message(F.text == '/help video')
async def cmd_help_video(message: Message):
    await message.delete()
    await message.answer(
        text=LEXICON_RU['cmd_help_video']
    )


@handler_router.message(F.text == '/help playlist')
async def cmd_help_playlist(message: Message):
    await message.delete()
    await message.answer(
        text=LEXICON_RU['cmd_help_playlist']
    )


@handler_router.message(F.text == '/help channel')
async def cmd_help_channel(message: Message):
    await message.delete()
    await message.answer(
        text=LEXICON_RU['cmd_help_channel']
    )


@handler_router.message(F.text == '/help export')
async def cmd_help_export(message: Message):
    await message.delete()
    await message.answer(
        text=LEXICON_RU['cmd_help_export']
    )


@handler_router.message(Command('help'))
async def cmd_help(message: Message):
    await message.delete()
    await message.answer(
        text=LEXICON_RU['cmd_help']
    )


# Handlers for receiving data
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