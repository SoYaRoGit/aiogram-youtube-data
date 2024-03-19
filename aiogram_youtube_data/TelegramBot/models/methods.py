import sqlite3
import logging
from config.config import load_config_database
from typing import Dict, Any

class DataBase:
    def __init__(self) -> None:
        config = load_config_database()
        self.__path_database = config.database.path_database
        self.__create_table_video()
        self.__create_table_playlist()
        

    def save_video_info(self, video_info: Dict[str, Any]) -> None:
        try:
            with sqlite3.connect(self.__path_database) as connection:
                cursor = connection.cursor()
                cursor.execute("SELECT * FROM video_info WHERE id = ?", (video_info['id'],))
                existing_data = cursor.fetchone()
                
                if existing_data:
                    self.__update_table_video(cursor, video_info, existing_data)
                else:
                    self.__insert_table_video(cursor, video_info)

        except sqlite3.Error as e:
            logging.error(f'Произошла ошибка при сохранении данных видео: {e}')

    def __create_table_video(self) -> None:
        try:
            with sqlite3.connect(self.__path_database) as connection:
                cursor = connection.cursor()
                cursor.execute("""
                    CREATE TABLE IF NOT EXISTS video_info (
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
            logging.error(f'Произошла ошибка при создании таблицы видео: {e}')

    def __update_table_video(self, cursor: sqlite3.Cursor, video_info: Dict[str, Any], existing_data: tuple) -> None:
        if (
            existing_data[23] != video_info['viewCount']
            or existing_data[24] != video_info['likeCount']
            or existing_data[25] != video_info['commentCount']
        ):
            update_query = """
            UPDATE video_info SET
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

    def __insert_table_video(self, cursor: sqlite3.Cursor, video_info: Dict[str, Any]) -> None:
        insert_query = """
        INSERT INTO video_info (
            id, 
            kind, 
            etag, 
            publishedAt, 
            channelId, 
            title, 
            thumbnails_url, 
            thumbnails_width,
            thumbnails_height, 
            channelTitle, tags, 
            categoryId, 
            liveBroadcastContent, 
            defaultLanguage,
            defaultAudioLanguage, 
            duration, 
            dimension, 
            definition, 
            caption, 
            licensedContent,
            regionRestriction_allowed, 
            regionRestriction_blocked, 
            contentRating, 
            viewCount, 
            likeCount,
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
    
    
    def save_playlist_info(self, playlist_info: Dict[str, Any]) -> None:
        try:
            with sqlite3.connect(self.__path_database) as connection:
                cursor = connection.cursor()
                cursor.execute('SELECT * FROM playlist_info WHERE id = ?', (playlist_info['id'],))
                existing_data = cursor.fetchone()
                
                if existing_data:
                    self.__update_table_playlist(cursor, playlist_info, existing_data)
                else:
                    self.__insert_table_playlist(cursor, playlist_info)
                    
        except sqlite3.Error as e:
            logging.error(f'Произошла ошибка при сохранении данных плейлиста: {e}')
    
    def __create_table_playlist(self) -> None:
        try:
            with sqlite3.connect(self.__path_database) as connection:
                cursor = connection.cursor()
                cursor.execute("""
                    CREATE TABLE IF NOT EXISTS playlist_info ( 
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
                        privacyStatus TEXT,
                        itemCount INTEGER,
                        duration TEXT
                    )
                """)
        except sqlite3.Error as e:
            logging.error(f'Произошла ошибка при создании таблицы плейлиста: {e}')
        
    def __update_table_playlist(self, cursor: sqlite3.Cursor, playlist_info: Dict[str, Any], existing_data: tuple) -> None:
        if (
            existing_data[5] != playlist_info['title']
            or existing_data[9] != playlist_info['channelTitle']
            or existing_data[10] != playlist_info['privacyStatus']
            or existing_data[11] != playlist_info['itemCount']
            or existing_data[12] != playlist_info['duration']
        ):
            update_query = """
            UPDATE playlist_info SET
                title = ?,
                channelTitle = ?,
                privacyStatus = ?,
                itemCount = ?,
                duration = ?
            WHERE id = ?
            """
            cursor.execute(update_query, (
                playlist_info['title'],
                playlist_info['channelTitle'],
                playlist_info['privacyStatus'],
                playlist_info['itemCount'],
                playlist_info['duration']
            ))
            
    def __insert_table_playlist(self, cursor: sqlite3.Cursor, playlist_info: Dict[str, Any]) -> None:
        insert_query = """
        INSERT INTO playlist_info (
            id,
            kind,
            etag,
            publishedAt,
            channelId,
            title,
            thumbnails_url,
            thumbnails_width,
            thumbnails_height,
            channelTitle,
            privacyStatus,
            itemCount,
            duration
        ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """
        cursor.execute(insert_query, (
            playlist_info['id'],
            playlist_info.get('kind', ''),
            playlist_info.get('etag', ''),
            playlist_info.get('publishedAt', ''),
            playlist_info.get('channelId', ''),
            playlist_info.get('title', ''),
            playlist_info.get('thumbnails_url', ''),
            playlist_info.get('thumbnails_width', 0),
            playlist_info.get('thumbnails_height', 0),
            playlist_info.get('channelTitle', ''),
            playlist_info.get('privacyStatus', ''),
            playlist_info.get('itemCount', 0),
            playlist_info.get('duration', '')
        ))