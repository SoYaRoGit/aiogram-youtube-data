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
        
        
        def get_info(self, video_identifier: str) -> dict:
            self.__video_identifier = self.__extract_video_video_identifier(video_identifier)
            
        
        def __extract_video_video_identifier(self, video_identifier: str) -> str:
            parse_url_video = urlparse(video_identifier)
            query_params = parse_qs(parse_url_video.query)
            
            if 'v' in query_params:
                video_identifier = query_params['v'][0]
                
            if video_identifier and all(
                (
                    isinstance(video_identifier, str), 
                    len(video_identifier) == 11
                )
            ):
                return video_identifier
            
            raise ValueError('Invalid video ID format')