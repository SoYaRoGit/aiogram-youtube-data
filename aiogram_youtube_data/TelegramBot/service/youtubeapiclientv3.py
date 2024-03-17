from datetime import timedelta
from urllib.parse import urlparse, parse_qs

from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
from isodate import parse_duration

from config.config import load_config_service_youtube
from custom_exceptions.custom_exceptions import (
    InvalidVideoIdFormatError, 
    InvalidPlaylistIdFormatError)
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
        self.playlist = YouTubeAPIClientV3.__Playlist(self.__api_resource)
        logger.info('YouTubeAPIClientV3 service launched successfully')
        
        
    class __Video:
        def __init__(self, access) -> None:
            self._access__api_resource = access
        
        
        def get_info(self, video_identifier: str) -> dict:
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
                    'id': item.get('id', 'Нет данных'),
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
            if duration_iso8601 == 'Нет данных':
                return duration_iso8601

            video_duration_seconds = parse_duration(duration_iso8601).total_seconds()
            video_duration_formatted = str(timedelta(seconds=video_duration_seconds))
            return video_duration_formatted

        def __extract_video_identifier(self, video_identifier: str) -> str:
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
    
    
    class __Playlist():
        def __init__(self, access) -> None:
            self._access__api_resource = access
        
        
        def get_info(self, playlist_identifier: str) -> dict:
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
                
                playlsit_data: dict = {
                    'king': item.get('king', 'Нет данных'),
                    'etag': item.get('etag', 'Нет данных'),
                    'id': item.get('id', 'Нет данных'),
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
                
                return playlsit_data
            
            
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