from aiogram import Router, F, html
from aiogram.types import Message
from aiogram.filters import CommandStart, CommandObject, Command
from lexicon.lexicon_ru import LEXICON_RU
from service.youtubeapiclientv3 import YouTubeAPIClientV3
from models.methods import DataBase
from utils.logger import logger



handler_router = Router()
serive = YouTubeAPIClientV3()
database = DataBase()


# Description Handlers
@handler_router.message(CommandStart())
async def cmd_start(message: Message):
    await message.delete()
    await message.answer(
        text=LEXICON_RU['cmd_start'].format(message.from_user.username)
    )
    logger.info(f'Вызов команды /start пользователем: {message.from_user.full_name} | {message.from_user.id}')


@handler_router.message(F.text == '/help video')
async def cmd_help_video(message: Message):
    await message.delete()
    await message.answer(
        text=LEXICON_RU['cmd_help_video']
    )
    logger.info(f'Вызов команды /help video пользователем: {message.from_user.full_name} | {message.from_user.id}')


@handler_router.message(F.text == '/help playlist')
async def cmd_help_playlist(message: Message):
    await message.delete()
    await message.answer(
        text=LEXICON_RU['cmd_help_playlist']
    )
    logger.info(f'Вызов команды /help playlist пользователем: {message.from_user.full_name} | {message.from_user.id}')


@handler_router.message(F.text == '/help channel')
async def cmd_help_channel(message: Message):
    await message.delete()
    await message.answer(
        text=LEXICON_RU['cmd_help_channel']
    )
    logger.info(f'Вызов команды /help playlist пользователем: {message.from_user.full_name} | {message.from_user.id}')

@handler_router.message(F.text == '/help export')
async def cmd_help_export(message: Message):
    await message.delete()
    await message.answer(
        text=LEXICON_RU['cmd_help_export']
    )
    logger.info(f'Вызов команды /help export пользователем: {message.from_user.full_name} | {message.from_user.id}')


@handler_router.message(Command('help'))
async def cmd_help(message: Message):
    await message.delete()
    await message.answer(
        text=LEXICON_RU['cmd_help']
    )
    logger.info(f'Вызов команды /help пользователем: {message.from_user.full_name} | {message.from_user.id}')


# Handlers for receiving data
@handler_router.message(Command('video'))
async def cmd_video(message: Message, command: CommandObject):
    if command.args is None:
        await message.reply("Вы не указали идентификатор видео. Пожалуйста, укажите идентификатор.")
        logger.warning(f'Указан неправильный идентификатор видео пользователем: {message.from_user.full_name} | {message.from_user.id} | Идентификатор: {command.args}')
        return
    
    try:
        video_info: dict = serive.video.get_info(command.args)
    except Exception as e:
        logger.error(f'Произошла ошибка при получении данных о видео пользователем: {message.from_user.full_name} | {message.from_user.id} | Идентификатор: {command.args}')
        return
    
    try:
        entities = message.entities or []
        for item in entities:
            if item.type in video_info.keys():
                video_info[item.type] = item.extract_from(message.text)
        await message.reply(
            f'📹 Информация о видео\n'
            f'🔒 Тип ресурса: {html.quote(str(video_info["kind"]))}\n'
            f'🔑 Механизм кеширования: {html.quote(str(video_info["etag"]))}\n'
            f'🆔 Идентификатор: {html.quote(str(video_info["id_video"]))}\n'
            f'🕒 Дата и время публикации: {html.quote(str(video_info["publishedAt"]))}\n'
            f'📺 Название канала: {html.quote(str(video_info["channelTitle"]))}\n'
            f'👤 Идентификатор канала: {html.quote(str(video_info["channelId"]))}\n'
            f'🎬 Название: {html.quote(str(video_info["title"]))}\n'
            f'🖼️ URL Изображения: {html.quote(str(video_info["thumbnails_url"]))}\n'
            f'📏 Ширина изображения: {html.quote(str(video_info["thumbnails_width"]))}\n'
            f'📐 Высота изображения: {html.quote(str(video_info["thumbnails_height"]))}\n'
            f'🏷️ Используемые теги: {html.quote(str(video_info["tags"]))}\n'
            f'📚 Категория видео YouTube: {html.quote(str(video_info["categoryId"]))}\n'
            f'📡 Предстоящая/активная трансляция: {html.quote(str(video_info["liveBroadcastContent"]))}\n'
            f'🗣️ Язык текста в свойствах: {html.quote(str(video_info["defaultLanguage"]))}\n'
            f'🎙️ Язык звуковой дорожки: {html.quote(str(video_info["defaultAudioLanguage"]))}\n'
            f'⏱️ Продолжительность: {html.quote(str(video_info["duration"]))}\n'
            f'🔄 3D/2D: {html.quote(str(video_info["dimension"]))}\n'
            f'🎞️ Формат видео: {html.quote(str(video_info["definition"]))}\n'
            f'📝 Субтитры доступны: {html.quote(str(video_info["caption"]))}\n'
            f'🔏 Лицензионный контент: {html.quote(str(video_info["licensedContent"]))}\n'
            f'🌐 Доступные страны: {html.quote(str(video_info["regionRestriction_allowed"]))}\n'
            f'🚫 Заблокированные страны: {html.quote(str(video_info["regionRestriction_blocked"]))}\n'
            f'📊 Рейтинг (МКРФ - Россия): {html.quote(str(video_info["contentRating"]))}\n'
            f'👀 Просмотры: {html.quote(str(video_info["viewCount"]))}\n'
            f'👍 Лайки: {html.quote(str(video_info["likeCount"]))}\n'
            f'💬 Комментарии: {html.quote(str(video_info["commentCount"]))}\n'
        )
        logger.info(f'Данные о видео: {str(video_info["id_video"])} были успешно отправлены пользователю: {message.from_user.full_name} | {message.from_user.id}')
        database.save_video_info(video_info)
    except Exception as e:
        logger.error(f'Произошла ошибка в момент отправки данных о видео | Пользователь: {message.from_user.full_name} | {message.from_user.id} | Идентификатор: {str(video_info["id_video"])} | {e}')
        return


@handler_router.message(Command('playlist'))
async def cmd_playlist(message: Message, command: CommandObject):
    if command.args is None:
        await message.reply("Вы не указали идентификатор плейлиста. Пожалуйста, укажите идентификатор.")
        return
    
    try:
        playlist_info: dict = serive.playlist.get_info(command.args)
    except Exception as e:
        logger.error(f'Произошла ошибка: {e}')
        return
    
    try:
        entities = message.entities or []
        for item in entities:
            if item.type in playlist_info.keys():
                playlist_info[item.type] = item.extract_from(message.text)
        await message.reply(
            f'📹 Информация о плейлисте\n'
            f'🔒 Тип ресурса: {html.quote(str(playlist_info["kind"]))}\n'
            f'🔑 Механизм кеширования: {html.quote(str(playlist_info["etag"]))}\n'
            f'🆔 Идентификатор: {html.quote(str(playlist_info["id_playlist"]))}\n'
            f'🕒 Дата и время публикации: {html.quote(str(playlist_info["publishedAt"]))}\n'
            f'👤 Идентификатор канала: {html.quote(str(playlist_info["channelId"]))}\n'
            f'🎬 Название: {html.quote(str(playlist_info["title"]))}\n'
            f'🖼️ URL Изображения: {html.quote(str(playlist_info["thumbnails_url"]))}\n'
            f'📏 Ширина изображения: {html.quote(str(playlist_info["thumbnails_width"]))}\n'
            f'📐 Высота изображения: {html.quote(str(playlist_info["thumbnails_height"]))}\n'
            f'🔏 Статус конфиденциальности: {html.quote(str(playlist_info["privacyStatus"]))}\n'
            f'👀 Количество видео: {html.quote(str(playlist_info["itemCount"]))}\n'
            f'⏱️ Продолжительность плейлиста: {html.quote(str(playlist_info["duration"]))}\n'
        )
        database.save_playlist_info(playlist_info)
    except Exception as e:
        logger.error(f'Произошла ошибка: {e}')
        return 

@handler_router.message(Command('channel'))
async def cmd_channel(message: Message, command: CommandObject):
    if command.args is None:
        await message.reply("Вы не указали идентификатор плейлиста. Пожалуйста, укажите идентификатор.")
        return
    
    try:
        channel_info: dict = serive.channel.get_info(command.args)
    except Exception as e:
        logger.error(f'Произошла ошибка: {e}')
        return
    
    try:
        entities = message.entities or []
        for item in entities:
            if item.type in channel_info.keys():
                channel_info[item.type] = item.extract_from(message.text)
        await message.reply(
            f'📹 Информация о плейлисте\n'
            f'🔒 Тип ресурса: {html.quote(str(channel_info["kind"]))}\n'
            f'🔑 Механизм кеширования: {html.quote(str(channel_info["etag"]))}\n'
            f'🆔 Идентификатор: {html.quote(str(channel_info["id_channel"]))}\n'
            f'🎬 Название: {html.quote(str(channel_info["title"]))}\n'
            f'🕒 Дата и время публикации: {html.quote(str(channel_info["publishedAt"]))}\n'
            f'🖼️ URL Изображения: {html.quote(str(channel_info["thumbnails_url"]))}\n'
            f'📏 Ширина изображения: {html.quote(str(channel_info["thumbnails_width"]))}\n'
            f'📐 Высота изображения: {html.quote(str(channel_info["thumbnails_height"]))}\n'
            f'👀 Количесто просмотров: {html.quote(str(channel_info["viewCount"]))}\n'
            f'📐 Количество подписчиков: {html.quote(str(channel_info["subscriberCount"]))}\n'
            f'🔑 Является ли количество подписчиков канала общедоступным: {html.quote(str(channel_info["hiddenSubscriberCount"]))}\n'
            f'👀 Количество видео: {html.quote(str(channel_info["videoCount"]))}\n'
            f'🔏 Статус конфиденциальности: {html.quote(str(channel_info["privacyStatus"]))}\n'
            f'🕒 Может ли канал загружать видео продолжительностью более 15 минут: {html.quote(str(channel_info["longUploadsStatus"]))}\n'
            f'👀 Обозначен ли канал как предназначенный для детей: {html.quote(str(channel_info["madeForKids"]))}'
        )
        database.save_channel_info(channel_info)
    except Exception as e:
        logger.error(f'Произошла ошибка: {e}')
        return 


@handler_router.message(Command('export'))
async def cmd_export(message: Message, command: CommandObject):
    message.reply_document