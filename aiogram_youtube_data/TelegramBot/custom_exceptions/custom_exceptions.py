class InvalidVideoIdFormatError(Exception):
    """
    Исключение, возникающее при неверном формате идентификатора видео.

    Attributes:
        video_identifier (str): Необязательный параметр, содержащий неверный идентификатор видео.
    """

    def __init__(self, video_identifier: str = None) -> None:
        """
        Инициализирует объект InvalidVideoIdFormatError.

        Args:
            video_identifier (str, optional): Неверный идентификатор видео. По умолчанию None.
        """
        if video_identifier is not None:
            message = f'Неверный формат идентификатора видео: {video_identifier}'
        else:
            message = 'Неверный формат идентификатора видео'
        super().__init__(message)


class InvalidPlaylistIdFormatError(Exception):
    """
    Исключение, возникающее при неверном формате идентификатора плейлиста.

    Attributes:
        playlist_identifier (str): Необязательный параметр, содержащий неверный идентификатор плейлиста.
    """

    def __init__(self, playlist_identifier: str = None) -> None:
        """
        Инициализирует объект InvalidPlaylistIdFormatError.

        Args:
            playlist_identifier (str, optional): Неверный идентификатор плейлиста. По умолчанию None.
        """
        if playlist_identifier is not None:
            message = f'Неверный формат идентификатора плейлиста: {playlist_identifier}'
        else:
            message = 'Неверный формат идентификатора плейлиста'
        super().__init__(message)


class InvalidChannelIdFormatError(Exception):
    """
    Исключение, возникающее при неверном формате идентификатора канала.

    Attributes:
        channel_identifier (str): Необязательный параметр, содержащий неверный идентификатор канала.
    """

    def __init__(self, channel_identifier: str = None) -> None:
        """
        Инициализирует объект InvalidChannelIdFormatError.

        Args:
            channel_identifier (str, optional): Неверный идентификатор канала. По умолчанию None.
        """
        if channel_identifier is not None:
            message = f'Неверный формат идентификатора канала: {channel_identifier}'
        else:
            message = 'Неверный формат идентификатора канала'
        super().__init__(message)