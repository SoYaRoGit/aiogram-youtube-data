from aiogram import Router, html, F  # Импорт класса Router из модуля aiogram
from aiogram.types import Message, BufferedInputFile  # Импорт типов сообщений и файлов из модуля aiogram
from aiogram.filters import CommandStart, Command  # Импорт фильтров команд из модуля aiogram
from lexicon.lexicon_ru import LEXICON_RU  # Импорт русскоязычного лексикона из модуля lexicon_ru
from service.youtubeapiclientv3 import YouTubeAPIClientV3  # Импорт клиента YouTube API из модуля youtubeapiclientv3
from models.methods import DataBase  # Импорт методов моделей из модуля methods
from custom_filters.custom_filters import (  # Импорт пользовательских фильтров из модуля custom_filters
    VideoIdentifierFilter, 
    PlaylistIdentifierFilter,
    ChannelIdentifierFilter)
from utils.logger import logger  # Импорт логгера из модуля logger
from config.config import bot  # Импорт настроек бота из модуля config
from telegram_db_excel_service import send_excel_file  # Импорт функции отправки файлов Excel из telegram_db_excel_service

handler_router = Router()  # Создание объекта Router для управления обработчиками сообщений
service = YouTubeAPIClientV3()  # Создание объекта YouTubeAPIClientV3 для работы с API YouTube
database = DataBase()  # Создание объекта базы данных для взаимодействия с данными


# Description Handlers
@handler_router.message(CommandStart())  # Обработчик команды /start
async def cmd_start(message: Message):
    """
    Обработчик команды /start.

    Args:
        message (Message): Объект сообщения, содержащий информацию о команде.

    Returns:
        None
    """
    await message.delete()  # Удаление сообщения с командой /start
    await message.answer(
        text=LEXICON_RU['cmd_start'].format(message.from_user.username)  # Отправка ответного сообщения с приветствием
    )
    logger.info(f'Вызов команды /start пользователем: {message.from_user.full_name} | {message.from_user.id}')  # Логирование вызова команды /start


@handler_router.message(F.text == '/help_video')  # Обработчик сообщений с текстом /help_video
async def cmd_help_video(message: Message):
    """
    Обработчик команды /help_video.

    Args:
        message (Message): Объект сообщения, содержащий информацию о команде.

    Returns:
        None
    """
    await message.delete()  # Удаление сообщения с командой /help_video
    await message.answer(
        text=LEXICON_RU['cmd_help_video']  # Отправка ответного сообщения с помощью по видео
    )
    logger.info(f'Вызов команды /help_video пользователем: {message.from_user.full_name} | {message.from_user.id}')  # Логирование вызова команды /help_video


@handler_router.message(F.text == '/help_playlist')  # Обработчик сообщений с текстом /help_playlist
async def cmd_help_playlist(message: Message):
    """
    Обработчик команды /help_playlist.

    Args:
        message (Message): Объект сообщения, содержащий информацию о команде.

    Returns:
        None
    """
    await message.delete()  # Удаление сообщения с командой /help_playlist
    await message.answer(
        text=LEXICON_RU['cmd_help_playlist']  # Отправка ответного сообщения с помощью по плейлистам
    )
    logger.info(f'Вызов команды /help_playlist пользователем: {message.from_user.full_name} | {message.from_user.id}')  # Логирование вызова команды /help_playlist


@handler_router.message(F.text == '/help_channel')  # Обработчик сообщений с текстом /help_channel
async def cmd_help_channel(message: Message):
    """
    Обработчик команды /help_channel.

    Args:
        message (Message): Объект сообщения, содержащий информацию о команде.

    Returns:
        None
    """
    await message.delete()  # Удаление сообщения с командой /help_channel
    await message.answer(
        text=LEXICON_RU['cmd_help_channel']  # Отправка ответного сообщения с помощью по каналам
    )
    logger.info(f'Вызов команды /help_channel пользователем: {message.from_user.full_name} | {message.from_user.id}')  # Логирование вызова команды /help_channel


@handler_router.message(F.text == '/help_export')  # Обработчик сообщений с текстом /help_export
async def cmd_help_export(message: Message):
    """
    Обработчик команды /help_export.

    Args:
        message (Message): Объект сообщения, содержащий информацию о команде.

    Returns:
        None
    """
    await message.delete()  # Удаление сообщения с командой /help_export
    await message.answer(
        text=LEXICON_RU['cmd_help_export']  # Отправка ответного сообщения с помощью по экспорту данных
    )
    logger.info(f'Вызов команды /help_export пользователем: {message.from_user.full_name} | {message.from_user.id}')  # Логирование вызова команды /help_export


@handler_router.message(Command('help'))  # Обработчик сообщений с командой /help
async def cmd_help(message: Message):
    """
    Обработчик команды /help.

    Args:
        message (Message): Объект сообщения, содержащий информацию о команде.

    Returns:
        None
    """
    await message.delete()  # Удаление сообщения с командой /help
    await message.answer(
        text=LEXICON_RU['cmd_help']  # Отправка ответного сообщения с общей справочной информацией
    )
    logger.info(f'Вызов команды /help пользователем: {message.from_user.full_name} | {message.from_user.id}')  # Логирование вызова команды /help


# Handlers for receiving data
@handler_router.message(PlaylistIdentifierFilter())  # Обработчик сообщений, прошедших фильтр PlaylistIdentifierFilter
async def cmd_playlist(message: Message):    
    """
    Обработчик команд, содержащих идентификаторы плейлистов YouTube.

    Args:
        message (Message): Объект сообщения с информацией о команде и содержимом.

    Returns:
        None
    """
    try:
        playlist_info: dict = service.playlist.get_info(message.text)  # Получение информации о плейлисте
    except Exception as e:
        logger.error(f'Произошла ошибка: {e}')  # Логирование ошибки
        return
    
    try:
        entities = message.entities or []  # Получение сущностей сообщения (если есть)
        for item in entities:
            if item.type in playlist_info.keys():
                playlist_info[item.type] = item.extract_from(message.text)  # Извлечение информации из сущностей сообщения
        # Отправка информации о плейлисте пользователю
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
        logger.info(f'Данные о плейлисте: {str(playlist_info["id_playlist"])} были успешно отправлены пользователю: {message.from_user.full_name} | {message.from_user.id}')  # Логирование успешной отправки информации о плейлисте
        database.save_playlist_info(playlist_info)  # Сохранение информации о плейлисте в базе данных
    except Exception as e:
        logger.error(f'Произошла ошибка: {e}')  # Логирование ошибки
        return


@handler_router.message(VideoIdentifierFilter())  # Обработчик сообщений, прошедших фильтр VideoIdentifierFilter
async def cmd_video(message: Message):
    """
    Обработчик команд, содержащих идентификаторы видео YouTube.

    Args:
        message (Message): Объект сообщения с информацией о команде и содержимом.

    Returns:
        None
    """
    try:
        video_info: dict = service.video.get_info(message.text)  # Получение информации о видео
    except Exception as e:
        logger.error(f'Произошла ошибка при получении данных о видео пользователем: {message.from_user.full_name} | {message.from_user.id} | Идентификатор: {message.text}')  # Логирование ошибки
        return
    
    try:
        entities = message.entities or []  # Получение сущностей сообщения (если есть)
        for item in entities:
            if item.type in video_info.keys():
                video_info[item.type] = item.extract_from(message.text)  # Извлечение информации из сущностей сообщения
        # Отправка информации о видео пользователю
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
        logger.info(f'Данные о видео: {str(video_info["id_video"])} были успешно отправлены пользователю: {message.from_user.full_name} | {message.from_user.id}')  # Логирование успешной отправки информации о видео
        database.save_video_info(video_info)  # Сохранение информации о видео в базе данных
    except Exception as e:
        logger.error(f'Произошла ошибка в момент отправки данных о видео | Пользователь: {message.from_user.full_name} | {message.from_user.id} | Идентификатор: {str(video_info["id_video"])} | {e}')  # Логирование ошибки
        return


@handler_router.message(ChannelIdentifierFilter())  # Обработчик сообщений, прошедших фильтр ChannelIdentifierFilter
async def cmd_channel(message: Message):    
    """
    Обработчик команд, содержащих идентификаторы каналов на YouTube.

    Args:
        message (Message): Объект сообщения с информацией о команде и содержимом.

    Returns:
        None
    """
    try:
        channel_info: dict = service.channel.get_info(message.text)  # Получение информации о канале
    except Exception as e:
        logger.error(f'Произошла ошибка: {e}')  # Логирование ошибки
        return
    
    try:
        entities = message.entities or []  # Получение сущностей сообщения (если есть)
        for item in entities:
            if item.type in channel_info.keys():
                channel_info[item.type] = item.extract_from(message.text)  # Извлечение информации из сущностей сообщения
        # Отправка информации о канале пользователю
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
        logger.info(f'Данные о канале: {str(channel_info["title"])} были успешно отправлены пользователю: {message.from_user.full_name} | {message.from_user.id}')  # Логирование успешной отправки информации о канале
        database.save_channel_info(channel_info)  # Сохранение информации о канале в базе данных
    except Exception as e:
        logger.error(f'Произошла ошибка: {e}')  # Логирование ошибки
        return


@handler_router.message(Command('export'))  # Обработчик сообщений, содержащих команду /export
async def cmd_export(message: Message):
    """
    Обработчик команды /export, который отправляет пользователю файл Excel с данными из базы данных.

    Args:
        message (Message): Объект сообщения с информацией о команде и отправителе.

    Returns:
        None
    """
    excel_file = send_excel_file()  # Генерация файла Excel с данными из базы данных
    await bot.send_document(message.from_user.id, document=BufferedInputFile(excel_file.read(), 'db_data.xlsx'))  # Отправка файла пользователю
    logger.info(f'Произведена выгрузка данных /export для польователя: {message.from_user.full_name} | {message.from_user.id}')  # Логирование события выгрузки данных


@handler_router.message()  # Обработчик всех сообщений (без фильтрации)
async def cmd_empty(message: Message):
    """
    Обработчик для сообщений, не соответствующих ни одной из предыдущих команд.

    Args:
        message (Message): Объект сообщения с информацией о отправителе и тексте сообщения.

    Returns:
        None
    """
    await message.reply(text='Введеная неизвестная команда или идентификатор')  # Отправка ответного сообщения о неизвестной команде
    logger.info(f'Введена неизвестная команда или идентификатор: {message.from_user.full_name} | {message.from_user.id} | Текст: {message.text}')  # Логирование события