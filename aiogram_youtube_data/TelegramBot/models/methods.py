import sqlite3
import logging
from config.config import load_config_database
from typing import Dict, Any

class DataBase:
    def __init__(self) -> None:
        config = load_config_database()
        self.__path_database = config.database.path_database

    def save_video_info(self, video_info: Dict[str, Any]) -> None:
        try:
            self.__create_table_video()
            with sqlite3.connect(self.__path_database) as connection:
                cursor = connection.cursor()
                cursor.execute("SELECT * FROM video_data WHERE id = ?", (video_info['id'],))
                existing_data = cursor.fetchone()
                
                if existing_data:
                    self.__update_video_info(cursor, video_info, existing_data)
                else:
                    self.__insert_video_info(cursor, video_info)

        except sqlite3.Error as e:
            logging.error(f'Произошла ошибка при сохранении данных видео: {e}')

    def __create_table_video(self) -> None:
        try:
            with sqlite3.connect(self.__path_database) as connection:
                cursor = connection.cursor()
                cursor.execute("""
                    CREATE TABLE IF NOT EXISTS video_data (
                        id TEXT PRIMARY KEY,
                        kind TEXT,
                        etag TEXT,
                        publishedAt TEXT,
                        channelId TEXT,
                        title TEXT,
                        thumbnails_url TEXT,
                        thumbnails_width INTEGER,
                        thumbnails_height INTEGER,
                        channelTitle TEXT,
                        tags TEXT,
                        categoryId TEXT,
                        liveBroadcastContent TEXT,
                        defaultLanguage TEXT,
                        defaultAudioLanguage TEXT,
                        duration TEXT,
                        dimension TEXT,
                        definition TEXT,
                        caption TEXT,
                        licensedContent TEXT,
                        regionRestriction_allowed TEXT,
                        regionRestriction_blocked TEXT,
                        contentRating TEXT,
                        viewCount INTEGER,
                        likeCount INTEGER,
                        commentCount INTEGER
                    )
                """)
        except sqlite3.Error as e:
            logging.error(f'Произошла ошибка при создании таблицы: {e}')

    def __update_video_info(self, cursor: sqlite3.Cursor, video_info: Dict[str, Any], existing_data: tuple) -> None:
        if (
            existing_data[23] != video_info['viewCount']
            or existing_data[24] != video_info['likeCount']
            or existing_data[25] != video_info['commentCount']
        ):
            update_query = """
            UPDATE video_data SET
                viewCount = ?,
                likeCount = ?,
                commentCount = ?
            WHERE id = ?
            """
            cursor.execute(update_query, (
                video_info['viewCount'],
                video_info['likeCount'],
                video_info['commentCount'],
                video_info['id']
            ))

    def __insert_video_info(self, cursor: sqlite3.Cursor, video_info: Dict[str, Any]) -> None:
        insert_query = """
        INSERT INTO video_data (
            id, kind, etag, publishedAt, channelId, title, thumbnails_url, thumbnails_width,
            thumbnails_height, channelTitle, tags, categoryId, liveBroadcastContent, defaultLanguage,
            defaultAudioLanguage, duration, dimension, definition, caption, licensedContent,
            regionRestriction_allowed, regionRestriction_blocked, contentRating, viewCount, likeCount,
            commentCount
        ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """
        cursor.execute(insert_query, (
            video_info['id'],
            video_info.get('kind', ''),
            video_info.get('etag', ''),
            video_info.get('publishedAt', ''),
            video_info.get('channelId', ''),
            video_info.get('title', ''),
            video_info.get('thumbnails_url', ''),
            video_info.get('thumbnails_width', 0),
            video_info.get('thumbnails_height', 0),
            video_info.get('channelTitle', ''),
            ','.join(video_info.get('tags', [])),
            video_info.get('categoryId', ''),
            video_info.get('liveBroadcastContent', ''),
            video_info.get('defaultLanguage', ''),
            video_info.get('defaultAudioLanguage', ''),
            video_info.get('duration', ''),
            video_info.get('dimension', ''),
            video_info.get('definition', ''),
            video_info.get('caption', ''),
            video_info.get('licensedContent', ''),
            video_info.get('regionRestriction_allowed', ''),
            video_info.get('regionRestriction_blocked', ''),
            video_info.get('contentRating', ''),
            video_info.get('viewCount', 0),
            video_info.get('likeCount', 0),
            video_info.get('commentCount', 0)
        ))