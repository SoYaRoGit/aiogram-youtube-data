from aiogram import Router
from aiogram.types import Message
from aiogram.filters import CommandStart, CommandObject, Command


handler_router = Router()


@handler_router.message()
async def msg_echo(msg: Message):
    await msg.answer(
        text=f'{msg.text}'
    )