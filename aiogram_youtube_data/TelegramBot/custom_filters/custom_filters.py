from aiogram.filters import BaseFilter
from aiogram.types import Message
from urllib.parse import urlparse, parse_qs


class VideoIdentifierFilter(BaseFilter):
    """
    Фильтр для проверки сообщений на наличие ссылок на видео YouTube и извлечения идентификаторов видео.

    Attributes:
        message (Message): Объект сообщения для проверки.
    """

    async def __call__(self, message: Message) -> bool:
        """
        Проверяет сообщение на наличие ссылок на видео YouTube и извлекает идентификаторы видео.

        Args:
            message (Message): Объект сообщения для проверки.

        Returns:
            bool: True, если сообщение содержит ссылку на видео YouTube с правильным форматом идентификатора, в противном случае False.
        """
        if 'https://youtu.be/' in message.text:
            # Если сообщение содержит строку 'https://youtu.be/', извлекаем идентификатор видео
            segments = message.text.split("/")
            video_identifier = segments[-1]
            if "?" in video_identifier:
                video_identifier = video_identifier.split("?")[0]
                
            # Проверяем длину идентификатора
            return len(video_identifier) == 11
        elif 'https://www.youtube.com/' in message.text:
            # Если сообщение содержит строку 'https://www.youtube.com/', извлекаем идентификатор видео из параметра запроса 'v'
            parse_url_video = urlparse(message.text)
            query_params = parse_qs(parse_url_video.query)
            
            if 'v' in query_params:
                video_identifier = query_params['v'][0]
            else:
                return False
                
            # Проверяем, является ли идентификатор строкой длины 11
            if video_identifier and all(
                (
                    isinstance(video_identifier, str), 
                    len(video_identifier) == 11
                )
            ):
                return True
        return False
    

class PlaylistIdentifierFilter(BaseFilter):
    """
    Фильтр для проверки сообщений на наличие ссылок на плейлисты YouTube и извлечения идентификаторов плейлистов.

    Attributes:
        message (Message): Объект сообщения для проверки.
    """

    async def __call__(self, message: Message) -> bool:
        """
        Проверяет сообщение на наличие ссылок на плейлисты YouTube и извлекает идентификаторы плейлистов.

        Args:
            message (Message): Объект сообщения для проверки.

        Returns:
            bool: True, если сообщение содержит ссылку на плейлист YouTube с правильным форматом идентификатора, в противном случае False.
        """
        parsed_url = urlparse(message.text)
        query_params = parse_qs(parsed_url.query)

        if 'list' in query_params:
            playlist_identifier = query_params['list'][0]
        else:
            return False

        if playlist_identifier and all(
            (
                isinstance(playlist_identifier, str), 
                playlist_identifier.startswith('PL'), 
                len(playlist_identifier) == 34)
        ):
            return True

        return False


class ChannelIdentifierFilter(BaseFilter):
    """
    Фильтр для проверки сообщений на наличие ссылок на каналы YouTube.

    Attributes:
        message (Message): Объект сообщения для проверки.
    """

    async def __call__(self, message: Message) -> bool:
        """
        Проверяет сообщение на наличие ссылок на каналы YouTube.

        Args:
            message (Message): Объект сообщения для проверки.

        Returns:
            bool: True, если сообщение содержит ссылку на канал YouTube, в противном случае False.
        """
        if "youtube.com" not in message.text:
            return False
        
        parsed_url = urlparse(message.text)
            
        if not parsed_url.path:
            return False
            
        parts = parsed_url.path.split('@')
        if len(parts) < 2:
            return False
            
        return True