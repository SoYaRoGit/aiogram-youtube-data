class InvalidVideoIdFormatError(Exception):
    def __init__(self, video_identifier: str = None) -> None:
        if video_identifier is not None:
            message = f'Неверный формат идентификатора видео: {video_identifier}'
        else:
            message = 'Неверный формат идентификатора видео'
        super().__init__(message)


class InvalidPlaylistIdFormatError(Exception):
    def __init__(self, playlist_identifier: str = None) -> None:
        if playlist_identifier is not None:
            message = f'Неверный формат идентификатора плейлиста: {playlist_identifier}'
        else:
            message = 'Неверный формат идентификатора плейлиста'
        super().__init__(message)

