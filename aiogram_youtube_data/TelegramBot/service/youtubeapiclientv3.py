from datetime import timedelta
from urllib.parse import urlparse, parse_qs

from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
from isodate import parse_duration

from config.config import load_config_service_youtube
from custom_exceptions.custom_exceptions import InvalidVideoIdFormatError
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
            error_message = f'An exception occurred while creating the YouTube API resource. Check API_KEY_SERVICE_YOUTUBE: {e}'
            logger.error(error_message)
            raise ValueError(error_message)

        self.video = YouTubeAPIClientV3.__Video(self.__api_resource)
        logger.info('YouTubeAPIClientV3 service launched successfully')
        
        
    class __Video:
        def __init__(self, access) -> None:
            self._access__api_resource = access
        
        
        def get_info(self, video_identifier: str) -> dict:
            try:
                video_identifier = self.__extract_video_video_identifier(video_identifier)
                video_info_response: dict = self._access__api_resource.videos().list(
                    part=['snippet', 'contentDetails', 'statistics'],
                    id=video_identifier
                ).execute()

                item = video_info_response.get('items', [])[0]

                if not item:
                    raise ValueError('No video information found')

                snippet = item.get('snippet', {})
                content_details = item.get('contentDetails', {})
                statistics = item.get('statistics', {})

                video_info: dict = {
                    'kind': item.get('kind', 'Нет данных'),
                    'etag': item.get('etag', 'Нет данных'),
                    'id': item.get('id', 'Нет данных'),
                    'publishedAt': snippet.get('publishedAt', 'Нет данных'),
                    'channelId': snippet.get('channelId', 'Нет данных'),
                    'title': snippet.get('title', 'Нет данных'),
                    'description': snippet.get('description', 'Нет данных'),
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

                return video_info
                
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
            if duration_iso8601 == 'Нет данных':
                return duration_iso8601

            video_duration_seconds = parse_duration(duration_iso8601).total_seconds()
            video_duration_formatted = str(timedelta(seconds=video_duration_seconds))
            return video_duration_formatted

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
            
            raise InvalidVideoIdFormatError(video_identifier)