import sqlite3
from utils.logger import logger
from config.config import load_config_database
from typing import Dict, Any
from utils.logger import logger

class DataBase:
    def __init__(self) -> None:
        config = load_config_database()
        self.__path_database = config.database.path_database
        
        try:
            self.__create_table_video()
            logger.info(f'Таблица видео успешно инициализирована')
        except sqlite3.Error as e:
            logger.error(f'Произошла ошибка при инициализации таблицы видео: {e}')
        
        try:
            self.__create_table_playlist()
            logger.info(f'Таблица плейлист успешно инициализирована')
        except sqlite3.Error as e:
            logger.error(f'Произошла ошибка при инициализации таблицы плейлист: {e}')
            
        try:
            self.__create_table_channel()
            logger.info(f'Таблица канал успешно иинициализирована')
        except sqlite3.Error as e:
            logger.error(f'Произошла ошибка при инициализации таблицы канал: {e}')
        

    def save_video_info(self, video_info: Dict[str, Any]) -> None:
        try:
            with sqlite3.connect(self.__path_database) as connection:
                cursor = connection.cursor()
                cursor.execute("SELECT * FROM video_info WHERE id_video = ?", (video_info['id_video'],))
                existing_data = cursor.fetchone()
                
                if existing_data:
                    self.__update_table_video(cursor, video_info, existing_data)
                else:
                    self.__insert_table_video(cursor, video_info)

        except sqlite3.Error as e:
            logger.error(f'Произошла ошибка при сохранении данных видео: {e}')

    def __create_table_video(self) -> None:
        try:
            with sqlite3.connect(self.__path_database) as connection:
                cursor = connection.cursor()
                cursor.execute("""
                    CREATE TABLE IF NOT EXISTS video_info (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        kind TEXT,
                        etag TEXT,
                        id_video TEXT UNIQUE,
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
            logger.error(f'Произошла ошибка при создании таблицы видео: {e}')

    def __update_table_video(self, cursor: sqlite3.Cursor, video_info: Dict[str, Any], existing_data: tuple) -> None:
        existing_id, *_ = existing_data

        update_query = "UPDATE video_info SET "
        update_values = []

        for attr, value in video_info.items():
            if attr != 'id_video' and attr in video_info and video_info[attr] != existing_data[existing_data.index(attr) + 1]:
                update_query += f"{attr} = ?, "
                update_values.append(value)

        update_query = update_query.rstrip(", ") + " WHERE id_video = ?"
        update_values.append(existing_id)

        cursor.execute(update_query, update_values)

    def __insert_table_video(self, cursor: sqlite3.Cursor, video_info: Dict[str, Any]) -> None:
        insert_query = """
        INSERT INTO video_info (
            kind, etag, id_video, publishedAt, channelId, title,
            thumbnails_url, thumbnails_width, thumbnails_height, channelTitle,
            tags, categoryId, liveBroadcastContent, defaultLanguage,
            defaultAudioLanguage, duration, dimension, definition,
            caption, licensedContent, regionRestriction_allowed,
            regionRestriction_blocked, contentRating, viewCount,
            likeCount, commentCount
        ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """
        cursor.execute(insert_query, (
            video_info.get('kind', ''),
            video_info.get('etag', ''),
            video_info.get('id_video', ''),
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
                cursor.execute('SELECT * FROM playlist_info WHERE id_playlist = ?', (playlist_info['id_playlist'],))
                existing_data = cursor.fetchone()
                
                if existing_data:
                    self.__update_table_playlist(cursor, playlist_info, existing_data)
                else:
                    self.__insert_table_playlist(cursor, playlist_info)
                    
        except sqlite3.Error as e:
            logger.error(f'Произошла ошибка при сохранении данных плейлиста: {e}')
    
    def __create_table_playlist(self) -> None:
        try:
            with sqlite3.connect(self.__path_database) as connection:
                cursor = connection.cursor()
                cursor.execute("""
                    CREATE TABLE IF NOT EXISTS playlist_info ( 
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        kind TEXT,
                        etag TEXT,
                        id_playlist TEXT UNIQUE,
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
            logger.error(f'Произошла ошибка при создании таблицы плейлиста: {e}')
        
    def __update_table_playlist(self, cursor: sqlite3.Cursor, playlist_info: Dict[str, Any], existing_data: tuple) -> None:
        update_query = """
        UPDATE playlist_info SET
            kind = ?,
            etag = ?,
            publishedAt = ?,
            channelId = ?,
            title = ?,
            thumbnails_url = ?,
            thumbnails_width = ?,
            thumbnails_height = ?,
            channelTitle = ?,
            privacyStatus = ?,
            itemCount = ?,
            duration = ?
        WHERE id_playlist = ?
        """
        cursor.execute(update_query, (
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
            playlist_info.get('duration', ''),
            playlist_info['id_playlist']
        ))
            
    def __insert_table_playlist(self, cursor: sqlite3.Cursor, playlist_info: Dict[str, Any]) -> None:
        insert_query = """
        INSERT INTO playlist_info (
            kind, etag, id_playlist, publishedAt, channelId, title,
            thumbnails_url, thumbnails_width, thumbnails_height, channelTitle,
            privacyStatus, itemCount, duration
        ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """
        cursor.execute(insert_query, (
            playlist_info.get('kind', ''),
            playlist_info.get('etag', ''),
            playlist_info.get('id_playlist', ''),
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


    def save_channel_info(self, channel_info: dict) -> None:
        try:
            with sqlite3.connect(self.__path_database) as connection:
                cursor = connection.cursor()
                cursor.execute('SELECT * FROM channel_info WHERE id_channel = ?', (channel_info['id_channel'],))
                existing_data = cursor.fetchone()
                
                if existing_data:
                    self.__update_table_channel(cursor, channel_info, existing_data)
                else:
                    self.__insert_table_channel(cursor, channel_info)
                    
        except sqlite3.Error as e:
            logger.error(f'Произошла ошибка при сохранении данных канала: {e}')

    def __create_table_channel(self) -> None:
        try:
            with sqlite3.connect(self.__path_database) as connection:
                cursor = connection.cursor()
                cursor.execute("""
                    CREATE TABLE IF NOT EXISTS channel_info (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        kind TEXT,
                        etag TEXT,
                        id_channel TEXT UNIQUE,
                        title TEXT,
                        publishedAt TEXT,
                        thumbnails_url TEXT,
                        thumbnails_width INTEGER,
                        thumbnails_height INTEGER,
                        viewCount INTEGER,
                        subscriberCount INTEGER,
                        hiddenSubscriberCount INTEGER,
                        videoCount INTEGER,
                        privacyStatus TEXT,
                        longUploadsStatus TEXT,
                        madeForKids TEXT
                    )
                """)
        except sqlite3.Error as e:
            logger.error(f'Произошла ошибка при создании таблицы канала: {e}')

    def __update_table_channel(self, cursor: sqlite3.Cursor, channel_info: Dict[str, Any], existing_data: tuple) -> None:
        if (
            existing_data[4] != channel_info['title']
            or existing_data[5] != channel_info['publishedAt']
            or existing_data[6] != channel_info['thumbnails_url']
            or existing_data[7] != channel_info['thumbnails_width']
            or existing_data[8] != channel_info['thumbnails_height']
            or existing_data[9] != channel_info['viewCount']
            or existing_data[10] != channel_info['subscriberCount']
            or existing_data[11] != channel_info['hiddenSubscriberCount']
            or existing_data[12] != channel_info['videoCount']
            or existing_data[13] != channel_info['privacyStatus']
            or existing_data[14] != channel_info['longUploadsStatus']
            or existing_data[15] != channel_info['madeForKids']
        ):
            update_query = """
            UPDATE channel_info SET
                title = ?,
                publishedAt = ?,
                thumbnails_url = ?,
                thumbnails_width = ?,
                thumbnails_height = ?,
                viewCount = ?,
                subscriberCount = ?,
                hiddenSubscriberCount = ?,
                videoCount = ?,
                privacyStatus = ?,
                longUploadsStatus = ?,
                madeForKids = ?
            WHERE id_channel = ?
            """
            cursor.execute(update_query, (
                channel_info['id_channel'],
                channel_info['title'],
                channel_info['publishedAt'],
                channel_info['thumbnails_url'],
                channel_info['thumbnails_width'],
                channel_info['thumbnails_height'],
                channel_info['viewCount'],
                channel_info['subscriberCount'],
                channel_info['hiddenSubscriberCount'],
                channel_info['videoCount'],
                channel_info['privacyStatus'],
                channel_info['longUploadsStatus'],
                channel_info['madeForKids']
            ))


    def __insert_table_channel(self, cursor: sqlite3.Cursor, channel_info: dict) -> None:
        insert_query = """
        INSERT INTO channel_info (
            kind, etag, id_channel, title, publishedAt, thumbnails_url,
            thumbnails_width, thumbnails_height, viewCount, subscriberCount,
            hiddenSubscriberCount, videoCount, privacyStatus, longUploadsStatus,
            madeForKids
        ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """
        cursor.execute(insert_query, (
            channel_info.get('kind', ''),
            channel_info.get('etag', ''),
            channel_info.get('id_channel', ''),
            channel_info.get('title', ''),
            channel_info.get('publishedAt', ''),
            channel_info.get('thumbnails_url', ''),
            channel_info.get('thumbnails_width', 0),
            channel_info.get('thumbnails_height', 0),
            channel_info.get('viewCount', 0),
            channel_info.get('subscriberCount', 0),
            channel_info.get('hiddenSubscriberCount', 0),
            channel_info.get('videoCount', 0),
            channel_info.get('privacyStatus', ''),
            channel_info.get('longUploadsStatus', ''),
            channel_info.get('madeForKids', '')
        ))