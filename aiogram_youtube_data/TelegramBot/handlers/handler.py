from aiogram import Router, F, html
from aiogram.types import Message
from aiogram.filters import CommandStart, CommandObject, Command
from lexicon.lexicon_ru import LEXICON_RU
from service.youtubeapiclientv3 import YouTubeAPIClientV3
from custom_exceptions.custom_exceptions import InvalidVideoIdFormatError



handler_router = Router()
serive = YouTubeAPIClientV3()

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
    if command.args is None:
        await message.reply("Вы не указали идентификатор видео. Пожалуйста, укажите идентификатор.")
        return
    
    try:
        video_data: dict = serive.video.get_info(command.args)
    except InvalidVideoIdFormatError as e:
        await message.reply(str(e))
    
    try:
        entities = message.entities or []
        for item in entities:
            if item.type in video_data.keys():
                video_data[item.type] = item.extract_from(message.text)
        await message.reply(
            f'📹 Информация о видео\n'
            f'🔒 Тип ресурса: {html.quote(str(video_data["kind"]))}\n'
            f'🔑 Механизм кеширования: {html.quote(str(video_data["etag"]))}\n'
            f'🆔 Идентификатор: {html.quote(str(video_data["id"]))}\n'
            f'🕒 Дата и время публикации: {html.quote(str(video_data["publishedAt"]))}\n'
            f'📺 Название канала: {html.quote(str(video_data["channelTitle"]))}\n'
            f'👤 Идентификатор канала: {html.quote(str(video_data["channelId"]))}\n'
            f'🎬 Название: {html.quote(str(video_data["title"]))}\n'
            f'🖼️ URL Изображения: {html.quote(str(video_data["thumbnails_url"]))}\n'
            f'📏 Ширина изображения: {html.quote(str(video_data["thumbnails_width"]))}\n'
            f'📐 Высота изображения: {html.quote(str(video_data["thumbnails_height"]))}\n'
            f'🏷️ Используемые теги: {html.quote(str(video_data["tags"]))}\n'
            f'📚 Категория видео YouTube: {html.quote(str(video_data["categoryId"]))}\n'
            f'📡 Предстоящая/активная трансляция: {html.quote(str(video_data["liveBroadcastContent"]))}\n'
            f'🗣️ Язык текста в свойствах: {html.quote(str(video_data["defaultLanguage"]))}\n'
            f'🎙️ Язык звуковой дорожки: {html.quote(str(video_data["defaultAudioLanguage"]))}\n'
            f'⏱️ Продолжительность: {html.quote(str(video_data["duration"]))}\n'
            f'🔄 3D/2D: {html.quote(str(video_data["dimension"]))}\n'
            f'🎞️ Формат видео: {html.quote(str(video_data["definition"]))}\n'
            f'📝 Субтитры доступны: {html.quote(str(video_data["caption"]))}\n'
            f'🔏 Лицензионный контент: {html.quote(str(video_data["licensedContent"]))}\n'
            f'🌐 Доступные страны: {html.quote(str(video_data["regionRestriction_allowed"]))}\n'
            f'🚫 Заблокированные страны: {html.quote(str(video_data["regionRestriction_blocked"]))}\n'
            f'📊 Рейтинг (МКРФ - Россия): {html.quote(str(video_data["contentRating"]))}\n'
            f'👀 Просмотры: {html.quote(str(video_data["viewCount"]))}\n'
            f'👍 Лайки: {html.quote(str(video_data["likeCount"]))}\n'
            f'💬 Комментарии: {html.quote(str(video_data["commentCount"]))}\n'
        )
    except Exception as e:
        await message.reply(str(e))


@handler_router.message(Command('playlist'))
async def cmd_playlist(message: Message, command: CommandObject):
    ...


@handler_router.message(Command('channel'))
async def cmd_channel(message: Message, command: CommandObject):
    ...


@handler_router.message(Command('export'))
async def cmd_export(message: Message, command: CommandObject):
    ...