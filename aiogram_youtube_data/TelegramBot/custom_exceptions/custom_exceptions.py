class InvalidVideoIdFormatError(Exception):
    def __init__(self, video_identifier: str = None) -> None:
        if video_identifier is not None:
            message = f'Неверный формат идентификатора видео: {video_identifier}'
        else:
            message = 'Неверный формат идентификатора видео'
        super().__init__(message)
