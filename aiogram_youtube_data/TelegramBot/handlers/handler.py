from aiogram import Router, F, html
from aiogram.types import Message, BufferedInputFile
from aiogram.filters import CommandStart, Command
from lexicon.lexicon_ru import LEXICON_RU
from service.youtubeapiclientv3 import YouTubeAPIClientV3
from models.methods import DataBase
from custom_filters.custom_filters import (
    VideoIdentifierFilter, 
    PlaylistIdentifierFilter,
    ChannelIdentifierFilter)
from utils.logger import logger
from config.config import bot
from telegram_db_excel_service import send_excel_file


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


@handler_router.message(F.text == '/help_video')
async def cmd_help_video(message: Message):
    await message.delete()
    await message.answer(
        text=LEXICON_RU['cmd_help_video']
    )
    logger.info(f'Вызов команды /help_video пользователем: {message.from_user.full_name} | {message.from_user.id}')


@handler_router.message(F.text == '/help_playlist')
async def cmd_help_playlist(message: Message):
    await message.delete()
    await message.answer(
        text=LEXICON_RU['cmd_help_playlist']
    )
    logger.info(f'Вызов команды /help_playlist пользователем: {message.from_user.full_name} | {message.from_user.id}')


@handler_router.message(F.text == '/help_channel')
async def cmd_help_channel(message: Message):
    await message.delete()
    await message.answer(
        text=LEXICON_RU['cmd_help_channel']
    )
    logger.info(f'Вызов команды /help_channel пользователем: {message.from_user.full_name} | {message.from_user.id}')

@handler_router.message(F.text == '/help_export')
async def cmd_help_export(message: Message):
    await message.delete()
    await message.answer(
        text=LEXICON_RU['cmd_help_export']
    )
    logger.info(f'Вызов команды /help_export пользователем: {message.from_user.full_name} | {message.from_user.id}')


@handler_router.message(Command('help'))
async def cmd_help(message: Message):
    await message.delete()
    await message.answer(
        text=LEXICON_RU['cmd_help']
    )
    logger.info(f'Вызов команды /help пользователем: {message.from_user.full_name} | {message.from_user.id}')


# Handlers for receiving data
@handler_router.message(PlaylistIdentifierFilter())
async def cmd_playlist(message: Message):    
    try:
        playlist_info: dict = serive.playlist.get_info(message.text)
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
        logger.info(f'Данные о плейлисте: {str(playlist_info["id_playlist"])} были успешно отправлены пользователю: {message.from_user.full_name} | {message.from_user.id}')
        database.save_playlist_info(playlist_info)
    except Exception as e:
        logger.error(f'Произошла ошибка: {e}')
        return 


@handler_router.message(VideoIdentifierFilter())
async def cmd_video(message: Message):
    try:
        video_info: dict = serive.video.get_info(message.text)
    except Exception as e:
        logger.error(f'Произошла ошибка при получении данных о видео пользователем: {message.from_user.full_name} | {message.from_user.id} | Идентификатор: {message.text}')
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


@handler_router.message(ChannelIdentifierFilter())
async def cmd_channel(message: Message):    
    try:
        channel_info: dict = serive.channel.get_info(message.text)
    except Exception as e:
        logger.error(f'Произошла ошибка: {e}')
        return
    
    try:
        entities = message.entities or []
        for item in entities:
            if item.type in channel_info.keys():
                channel_info[item.type] = item.extract_from(message.text)
        await message.reply(
            f'📹 Информация о канале\n'
            f'🔒 Тип ресурса: {html.quote(str(channel_info["kind"]))}\n'
            f'🔑 Механизм кеширования: {html.quote(str(channel_info["etag"]))}\n'
            f'🆔 Идентификатор: {html.quote(str(channel_info["id_channel"]))}\n'
            f'🎬 Название: {html.quote(str(channel_info["title"]))}\n'
            f'🕒 Дата и время создания канала: {html.quote(str(channel_info["publishedAt"]))}\n'
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
        logger.info(f'Данные о канале: {str(channel_info["title"])} были успешно отправлены пользователю: {message.from_user.full_name} | {message.from_user.id}')
        database.save_channel_info(channel_info)
    except Exception as e:
        logger.error(f'Произошла ошибка: {e}')
        return 


@handler_router.message(Command('export'))
async def cmd_export(message: Message):
    excel_file = send_excel_file()
    await bot.send_document(message.from_user.id, document=BufferedInputFile(excel_file.read(), 'db_data.xlsx'))
    logger.info(f'Произведена выгрузка данных /export для польователя: {message.from_user.full_name} | {message.from_user.id}')
    

@handler_router.message()
async def cmd_empty(message: Message):
    await message.reply(text='Введеная неизвестная команда или идентификатор')
    logger.info(f'Введена неизвестная команда или идентификатор: {message.from_user.full_name} | {message.from_user.id} | Текст: {message.text}')