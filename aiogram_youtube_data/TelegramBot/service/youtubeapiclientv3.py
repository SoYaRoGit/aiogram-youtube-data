from googleapiclient.discovery import build
from isodate import parse_duration, parse_datetime
from config.config import load_config_service_youtube
from urllib.parse import urlparse, parse_qs
from pathlib import Path
from utils.logger import logger


class YouTubeAPIClientV3:
    def __init__(self) -> None:
        try:
            config = load_config_service_youtube()
            self.__api_resource = build(
                serviceName='youtube',
                version='v3',
                developerKey=config.service_youtube.api_key_service_youtube_v3
            )
        except Exception as e:
            logger.error(f'An exception occurred while creating the YouTube API resource. Check API_KEY_SERVICE_YOUTUBE: {e}')
            print(f'An exception occurred while creating the YouTube API resource. Check API_KEY_SERVICE_YOUTUBE: {e}')
        
        self.video = YouTubeAPIClientV3.__Video(self.__api_resource)

        logger.info('YouTubeAPIClientV3 service launched successfully')
        
        
    class __Video:
        def __init__(self, access) -> None:
            self._access__api_resource = access