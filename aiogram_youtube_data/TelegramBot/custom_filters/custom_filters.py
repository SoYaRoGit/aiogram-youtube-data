from aiogram.filters import BaseFilter
from aiogram.types import Message
from urllib.parse import urlparse, parse_qs


class VideoIdentifierFilter(BaseFilter):
    async def __call__(self, message: Message) -> bool:
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
                
            # Проверяем, является ли идентификатор строкой длины 11
            if video_identifier and all(
                (
                    isinstance(video_identifier, str), 
                    len(video_identifier) == 11
                )
            ):
                return True
        return False

