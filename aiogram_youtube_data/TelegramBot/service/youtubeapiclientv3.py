from datetime import timedelta
from urllib.parse import urlparse, parse_qs

from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
from isodate import parse_duration

from config.config import load_config_service_youtube
from custom_exceptions.custom_exceptions import (
    InvalidVideoIdFormatError, 
    InvalidPlaylistIdFormatError,
    InvalidChannelIdFormatError
)
from utils.logger import logger


class YouTubeAPIClientV3:
    def __init__(self) -> None:
        try:
            config = load_config_service_youtube()  # Загрузка конфигурации для сервиса YouTube
            # Инициализация ресурса YouTube API с использованием ключа разработчика из конфигурации
            self.__api_resource = build(
                serviceName='youtube',
                version='v3',
                developerKey=config.service_youtube.api_key_service_youtube_v3
            )
        except Exception as e:
            # Регистрация ошибки, если инициализация не удалась, и вызов исключения ValueError
            error_message = f'Произошла ошибка при создании ресурса YouTube API. Проверьте API_KEY_SERVICE_YOUTUBE: {e}'
            logger.error(error_message)
            raise ValueError(error_message)

        # Инициализация внутренних классов для взаимодействия с различными ресурсами
        self.video = YouTubeAPIClientV3.__Video(self.__api_resource)
        self.playlist = YouTubeAPIClientV3.__Playlist(self.__api_resource)
        self.channel = YouTubeAPIClientV3.__Channel(self.__api_resource)
        
        logger.info('Сервис YouTubeAPIClientV3 был успешно инициализирован')
        
        
    class __Video:
        """
        Класс для получения информации о видео из YouTube API.

        Attributes:
            _access__api_resource: Ресурс доступа к YouTube API.

        Methods:
            get_info(video_identifier: str) -> dict:
                Получает информацию о видео по его идентификатору.
            __format_duration(duration_iso8601: str) -> str:
                Преобразует длительность видео из формата ISO 8601 в удобочитаемый формат.
            __extract_video_identifier(video_identifier: str) -> str:
                Извлекает идентификатор видео из переданной строки.

        Raises:
            HttpError: Если происходит HTTP-ошибка при запросе к YouTube API.
            ValueError: Если идентификатор видео неверного формата или нет информации о видео.

        """
        def __init__(self, access) -> None:
            """
            Инициализация объекта класса.

            Args:
                access: Ресурс доступа к YouTube API.

            """
            self._access__api_resource = access
        
        
        def get_info(self, video_identifier: str) -> dict:
            """
            Получает информацию о видео из YouTube API по его идентификатору.

            Args:
                video_identifier: Идентификатор видео (URL или ID).

            Returns:
                dict: Словарь с данными о видео.

            Raises:
                HttpError: Если происходит HTTP-ошибка при запросе к YouTube API.
                ValueError: Если идентификатор видео неверного формата или нет информации о видео.

            """
            try:
                video_identifier = self.__extract_video_identifier(video_identifier)

                video_info_response: dict = self._access__api_resource.videos().list(
                    part=['snippet', 'contentDetails', 'statistics'],
                    id=video_identifier
                ).execute()

                item: dict = video_info_response.get('items', [])[0]

                if not item:
                    raise ValueError('No video information found')

                snippet: dict = item.get('snippet', {})
                content_details: dict = item.get('contentDetails', {})
                statistics: dict = item.get('statistics', {})

                video_data: dict = {
                    'kind': item.get('kind', 'Нет данных'),
                    'etag': item.get('etag', 'Нет данных'),
                    'id_video': item.get('id', 'Нет данных'),
                    'publishedAt': snippet.get('publishedAt', 'Нет данных'),
                    'channelId': snippet.get('channelId', 'Нет данных'),
                    'title': snippet.get('title', 'Нет данных'),
                    'thumbnails_url': snippet['thumbnails'].get('standard', {}).get('url', 'Нет данных'),
                    'thumbnails_width': snippet['thumbnails'].get('standard', {}).get('width', 'Нет данных'),
                    'thumbnails_height': snippet['thumbnails'].get('standard', {}).get('height', 'Нет данных'),
                    'channelTitle': snippet.get('channelTitle', 'Нет данных'),
                    'tags': snippet.get('tags', []),
                    'categoryId': snippet.get('categoryId', 'Нет данных'),
                    'liveBroadcastContent': snippet.get('liveBroadcastContent', 'Нет данных'),
                    'defaultLanguage': snippet.get('defaultLanguage', 'Нет данных'),
                    'defaultAudioLanguage': snippet.get('defaultAudioLanguage', 'Нет данных'),
                    'duration': self.__format_duration(content_details.get('duration', 'Нет данных')),
                    'dimension': content_details.get('dimension', 'Нет данных'),
                    'definition': content_details.get('definition', 'Нет данных'),
                    'caption': content_details.get('caption', 'Нет данных'),
                    'licensedContent': content_details.get('licensedContent', 'Нет данных'),
                    'regionRestriction_allowed': content_details.get('regionRestriction', {}).get('allowed', 'Нет данных'),
                    'regionRestriction_blocked': content_details.get('regionRestriction', {}).get('blocked', 'Нет данных'),
                    'contentRating': content_details.get('contentRating', {}).get('russiaRating', 'Нет данных'),
                    'viewCount': statistics.get('viewCount', 'Нет данных'),
                    'likeCount': statistics.get('likeCount', 'Нет данных'),
                    'commentCount': statistics.get('commentCount', 'Нет данных')
                }

                return video_data
                
            except HttpError as e:
                logger.error(f'HTTP Error occurred: {e}')
                raise
            except ValueError as ve:
                logger.error(f'ValueError occurred: {ve}')
                raise
            except Exception as ex:
                logger.error(f'An unexpected error occurred: {ex}')
                raise

        def __format_duration(self, duration_iso8601: str) -> str:
            """
            Преобразует длительность видео из формата ISO 8601 в удобочитаемый формат.

            Args:
                duration_iso8601: Длительность видео в формате ISO 8601.

            Returns:
                str: Длительность видео в удобочитаемом формате.

            """
            if duration_iso8601 == 'Нет данных':
                return duration_iso8601

            video_duration_seconds = parse_duration(duration_iso8601).total_seconds()
            video_duration_formatted = str(timedelta(seconds=video_duration_seconds))
            return video_duration_formatted

        def __extract_video_identifier(self, video_identifier: str) -> str:
            """
            Извлекает идентификатор видео из переданной строки.

            Args:
                video_identifier: Строка с URL или ID видео.

            Returns:
                str: Идентификатор видео.

            Raises:
                InvalidVideoIdFormatError: Если идентификатор видео неверного формата.

            """
            if 'https://youtu.be/' in video_identifier:
                # Если сообщение содержит строку 'https://youtu.be/', извлекаем идентификатор видео
                segments = video_identifier.split("/")
                video_identifier = segments[-1]
                if "?" in video_identifier:
                    video_identifier = video_identifier.split("?")[0]
                    
                # Проверяем длину идентификатора
                if len(video_identifier) == 11:
                    return video_identifier
                else:
                    return InvalidVideoIdFormatError(video_identifier)
            elif 'https://www.youtube.com/' in video_identifier:
                # Если сообщение содержит строку 'https://www.youtube.com/', извлекаем идентификатор видео из параметра запроса 'v'
                parse_url_video = urlparse(video_identifier)
                query_params = parse_qs(parse_url_video.query)
                
                if 'v' in query_params:
                    video_identifier = query_params['v'][0]
                    
                # Проверяем, является ли идентификатор строкой длины 11
                if video_identifier and all(
                    (
                        isinstance(video_identifier, str), 
                        len(video_identifier) == 11
                    )
                ):
                    return video_identifier
            return InvalidVideoIdFormatError(video_identifier)
    
    
    class __Playlist():
        """
        Класс для получения информации о плейлисте из YouTube API.

        Attributes:
            _access__api_resource: Ресурс доступа к YouTube API.

        Methods:
            get_info(playlist_identifier: str) -> dict:
                Получает информацию о плейлисте по его идентификатору.
            __get_info_playlists_duration(playlist_identifier) -> str:
                Получает общую продолжительность видео в плейлисте.
            __extract_playlist_identifier(playlist_identifier: str) -> str:
                Извлекает идентификатор плейлиста из переданной строки.

        Raises:
            HttpError: Если происходит HTTP-ошибка при запросе к YouTube API.
            ValueError: Если идентификатор плейлиста неверного формата или нет информации о плейлисте.

        """
        def __init__(self, access) -> None:
            """
            Инициализация объекта класса.

            Args:
                access: Ресурс доступа к YouTube API.

            """
            self._access__api_resource = access
        
        
        def get_info(self, playlist_identifier: str) -> dict:
            """
            Получает информацию о плейлисте из YouTube API по его идентификатору.

            Args:
                playlist_identifier: Идентификатор плейлиста (URL или ID).

            Returns:
                dict: Словарь с данными о плейлисте.

            Raises:
                HttpError: Если происходит HTTP-ошибка при запросе к YouTube API.
                ValueError: Если идентификатор плейлиста неверного формата или нет информации о плейлисте.

            """
            try:
                playlist_identifier: str = self.__extract_playlist_identifier(playlist_identifier)
                playlist_info_response: dict = self._access__api_resource.playlists().list(
                    part=['snippet', 'status', 'contentDetails'],
                    id=playlist_identifier
                ).execute()
                
                item: dict = playlist_info_response.get('items', [])[0]
                
                if not item:
                    raise ValueError('No video information found')
                
                snippet: dict = item.get('snippet', {})
                content_details: dict = item.get('contentDetails', {})
                status: dict = item.get('status', {})
                
                playlist_data: dict = {
                    'kind': item.get('kind', 'Нет данных'),
                    'etag': item.get('etag', 'Нет данных'),
                    'id_playlist': item.get('id', 'Нет данных'),
                    'publishedAt': snippet.get('publishedAt', 'Нет данных'),
                    'channelId': snippet.get('channelId', 'Нет данных'),
                    'title': snippet.get('title', 'Нет данных'),
                    'thumbnails_url': snippet['thumbnails'].get('standard', {}).get('url', 'Нет данных'),
                    'thumbnails_width': snippet['thumbnails'].get('standard', {}).get('width', 'Нет данных'),
                    'thumbnails_height': snippet['thumbnails'].get('standard', {}).get('height', 'Нет данных'),
                    'channelTitle': snippet.get('channelTitle', 'Нет данных'),
                    'privacyStatus': status.get('privacyStatus', 'Нет данных'),
                    'itemCount': content_details.get('itemCount', 'Нет данных'),
                    'duration': self.__get_info_playlists_duration(playlist_identifier)
                }
                
                return playlist_data
            
            
            except HttpError as e:
                logger.error(f'HTTP Error occurred: {e}')
                raise
            except ValueError as ve:
                logger.error(f'ValueError occurred: {ve}')
                raise
            except Exception as ex:
                logger.error(f'An unexpected error occurred: {ex}')
                raise
        
        
        def __get_info_playlists_duration(self, playlist_identifier) -> str:
            """
            Получает общую продолжительность видео в плейлисте.

            Args:
                playlist_identifier: Идентификатор плейлиста.

            Returns:
                str: Общая продолжительность видео в плейлисте в формате "часы:минуты:секунды".

            Raises:
                Exception: Если происходит ошибка при получении данных о видео.

            """
            try:
                next_page_token = None
                video_ids = []
                
                while True:
                    playlist_info_for_duration = self._access__api_resource.playlistItems().list(
                        part='contentDetails',
                        playlistId=playlist_identifier,
                        maxResults=50,
                        pageToken=next_page_token
                    ).execute()
                    
                    items = playlist_info_for_duration.get('items', [])
                    for item in items:
                        content_details = item.get('contentDetails', {})
                        video_id = content_details.get('videoId', '')
                        if video_id:
                            video_ids.append(video_id)

                    next_page_token = playlist_info_for_duration.get('nextPageToken')

                    if not next_page_token:
                        break
                    
            except Exception as e:
                print(f'Произошла ошибка при получении данных о странице плейлиста: {e}')
                return 'Нет данных'
            
            try:
                duration_formatted = 0
                
                for video in video_ids:
                    video_info = self._access__api_resource.videos().list(
                        part='contentDetails',
                        id=video
                    ).execute()
                    
                    content_details = video_info.get('items', [{}])[0].get('contentDetails', {})
                    duration_str = content_details.get('duration', 'PT0S')
                    duration_seconds = parse_duration(duration_str).total_seconds()
                    duration_formatted += duration_seconds
                
                hours = int(duration_formatted // 3600)
                minutes = int((duration_formatted % 3600) // 60)
                seconds = int(duration_formatted % 60)
                duration_formatted = f'{hours:}:{minutes:}:{seconds:}'
                
                return duration_formatted
            
            except Exception as e:
                print(f'Произошла ошибка при получении данных о видео!: {e}')
            

        def __extract_playlist_identifier(self, playlist_identifier: str) -> str:  
            """
            Извлекает идентификатор плейлиста из переданной строки.

            Args:
                playlist_identifier: Строка с URL или ID плейлиста.

            Returns:
                str: Идентификатор плейлиста.

            Raises:
                InvalidPlaylistIdFormatError: Если идентификатор плейлиста неверного формата.

            """          
            parsed_url = urlparse(playlist_identifier)
            query_params = parse_qs(parsed_url.query)

            if 'list' in query_params:
                playlist_identifier = query_params['list'][0]

            if playlist_identifier and all(
                (
                    isinstance(playlist_identifier, str), 
                    playlist_identifier.startswith('PL'), 
                    len(playlist_identifier) == 34)
            ):
                return playlist_identifier

            raise InvalidPlaylistIdFormatError(playlist_identifier)
    
    
    class __Channel:
        """
        Класс для получения информации о канале из YouTube API.

        Attributes:
            _access__api_resource: Ресурс доступа к YouTube API.

        Methods:
            get_info(channel_identifier: str) -> dict:
                Получает информацию о канале по его идентификатору.
            __extract_channel_identifier(channel_identifier: str) -> str:
                Извлекает идентификатор канала из переданной строки URL.

        Raises:
            HttpError: Если происходит HTTP-ошибка при запросе к YouTube API.
            ValueError: Если идентификатор канала неверного формата или нет информации о канале.

        """
        def __init__(self, access) -> None:
            """
            Инициализация объекта класса.

            Args:
                access: Ресурс доступа к YouTube API.

            """
            self._access__api_resource = access
        
        
        def get_info(self, channel_identifier: str) -> dict:
            """
            Получает информацию о канале из YouTube API по его идентификатору.

            Args:
                channel_identifier: Идентификатор канала (URL или имя канала).

            Returns:
                dict: Словарь с данными о канале.

            Raises:
                HttpError: Если происходит HTTP-ошибка при запросе к YouTube API.
                ValueError: Если идентификатор канала неверного формата или нет информации о канале.

            """
            try:
                channel_identifier: str = self.__extract_channel_identifier(channel_identifier)
                channel_info_response: dict = self._access__api_resource.channels().list(
                    part=['snippet', 'statistics', 'status'],
                    forHandle=channel_identifier
                ).execute()
                
                item: dict = channel_info_response.get('items', [])[0]
                
                if not item:
                    raise ValueError('No video information found')
                
                snippet: dict = item.get('snippet', {})
                statistics: dict = item.get('statistics', {})
                status: dict = item.get('status', {})
                
                channel_data: dict = {
                    'kind': item.get('kind', 'Нет данных'),
                    'etag': item.get('etag', 'Нет данных'),
                    'id_channel': item.get('id', 'Нет данных'),
                    'title': snippet.get('title', 'Нет данных'),
                    'publishedAt': snippet.get('publishedAt', 'Нет данных'),
                    'thumbnails_url': snippet['thumbnails'].get('default ', {}).get('url', 'Нет данных'),
                    'thumbnails_width': snippet['thumbnails'].get('default ', {}).get('width', 'Нет данных'),
                    'thumbnails_height': snippet['thumbnails'].get('default', {}).get('height', 'Нет данных'),
                    'viewCount': statistics.get('viewCount', 'Нет данных'),
                    'subscriberCount': statistics.get('subscriberCount', 'Нет данных'),
                    'hiddenSubscriberCount': statistics.get('hiddenSubscriberCount', 'Нет данных'),
                    'videoCount': statistics.get('videoCount', 'Нет данных'),
                    'privacyStatus': status.get('privacyStatus', 'Нет данных'),
                    'longUploadsStatus': status.get('longUploadsStatus', 'Нет данных'),
                    'madeForKids': status.get('madeForKids', 'Нет данных'),
                }
                
                return channel_data
            
            except HttpError as e:
                logger.error(f'HTTP Error occurred: {e}')
                raise
            except ValueError as ve:
                logger.error(f'ValueError occurred: {ve}')
                raise
            except Exception as ex:
                logger.error(f'An unexpected error occurred: {ex}')
                raise
        
        def __extract_channel_identifier(self, channel_identifier: str) -> str:
            """
            Извлекает идентификатор канала из переданной строки URL.

            Args:
                channel_identifier: Строка с URL или именем канала.

            Returns:
                str: Идентификатор канала.

            Raises:
                InvalidChannelIdFormatError: Если идентификатор канала неверного формата.

            """
            if "youtube.com" not in channel_identifier:
                raise InvalidChannelIdFormatError(channel_identifier)
        
            parsed_url = urlparse(channel_identifier)
            
            if not parsed_url.path:
                raise InvalidChannelIdFormatError(channel_identifier)
            
            parts = parsed_url.path.split('@')
            if len(parts) < 2:
                raise ValueError("URL не содержит символа @ или имя канала после него")
            
            channel_name = parts[-1]
            return channel_name