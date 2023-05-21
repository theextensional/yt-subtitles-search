import os
import sys

import yt_dlp
from yt_dlp import YoutubeDL

from .parse_youtube_url import parse_youtube_url

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from constants import DOWNLOAD_DIR  # noqa


class VideoDataError(Exception):
    def __init__(self, message: str = "Произошла ошибка при получении данных о видео.") -> None:
        super().__init__(message)


def download_subtitle(ydl: YoutubeDL, video_url: str, subtitle_file: str) -> bool:
    """
    Загружает субтитры для заданного видео из `video_url` и сохраняет их в
    файл `subtitle_file` при помощи переданного объекта `ydl` (YouTube-dl).
    Функция возвращает `True`, если субтитры были успешно загружены и
    сохранены в файле, и `False` в противном случае.
    """
    if os.path.isfile(subtitle_file):
        return True
    try:
        ydl.download([video_url])
        if os.path.isfile(subtitle_file):
            return True
    except yt_dlp.DownloadError:
        return False
    return False


def download_subtitles(video_url: str, lang: str = "ru", subtitle_format: str = "json3") -> list[str]:
    """
    Загружает субтитры для видео, расположенного по заданному URL-адресу `video_url`, на указанном языке `lang`
    и сохраняет их в формате `subtitle_format`. Возвращает список строк, содержащих пути к загруженным субтитрам.

    Параметры:
        - `video_url (str)`: URL-адрес видео или его идентификатор.
        - `lang (str)`: Язык субтитров. По умолчанию: 'ru'.
        - `subtitle_format (str)`: Формат субтитров. По умолчанию: 'json3'.

    Возвращает:
        `list[str]`: Список строк, содержащих пути к загруженным субтитрам.

    Исключения:
        - `ValueError`: Если `video_url` не является допустимым URL-адресом YouTube или его идентификатором.
        - `Exception`: Если не удалось получить данные о видео.

    Примеры использования:
    >>> download_subtitles('https://www.youtube.com/watch?v=Om7sRzxksXs', lang='en', subtitle_format='srt')
    ['/downloads/Om7sRzxksXs.en.srt']
    >>> download_subtitles('https://www.youtube.com/playlist?list=PLa2WHSYysn_FcroL3WX5hFh-BiwBvUMwn')
    ['/downloads/Om7sRzxksXs.ru.json3', '/downloads/0IdiKy6tAbw.ru.json3', ...]
    """
    subtitle_files: list[str] = []
    try:
        url_type, video_url, url_data = parse_youtube_url(video_url)
    except ValueError as e:
        print(f"ERROR: {e}")
        return subtitle_files

    ydl_options = {
        "extract_flat": True,
        "writesubtitles": True,
        "writeautomaticsub": True,
        "subtitleslangs": [lang],
        "subtitlesformat": subtitle_format,
        "outtmpl": f"{DOWNLOAD_DIR}/%(id)s",
        "skip_download": True,
        "quiet": True,
        "no_warnings": True,
    }

    def process_entry(entries: list) -> None:
        for entry in entries:
            entry_subtitle_file = f"{DOWNLOAD_DIR}/{entry['id']}.{lang}.{subtitle_format}"
            if download_subtitle(ydl, entry["url"], entry_subtitle_file):
                subtitle_files.append(entry_subtitle_file)

    with yt_dlp.YoutubeDL(ydl_options) as ydl:
        if url_type in ["video_url", "video_id", "short_url"]:
            subtitle_file = f"{DOWNLOAD_DIR}/{url_data}.{lang}.{subtitle_format}"
            if download_subtitle(ydl, video_url, subtitle_file):
                return [subtitle_file]
        else:
            video_info = ydl.extract_info(video_url, download=False)
            if not video_info:
                raise VideoDataError()

            if url_type in ["user_name", "channel_url", "channel_name", "channel_id"]:
                for page in video_info.get("entries", []):
                    process_entry(page.get("entries", []))
            elif url_type in ["playlist_url", "videos_url", "shorts_url", "streams_url"]:
                process_entry(video_info.get("entries", []))
            elif url_type in ["playlists_url"]:
                for playlist in video_info.get("entries", []):
                    playlist_info = ydl.extract_info(playlist["url"], download=False)
                    if not playlist_info:
                        raise VideoDataError()
                    process_entry(playlist_info.get("entries", []))

        return subtitle_files


if __name__ == "__main__":
    urls = [
        "https://www.youtube.com/@theextensional",  # пользователь
        "https://www.youtube.com/watch?v=dQw4w9WgXcQ",  # видео url
        "https://youtu.be/dQw4w9WgXcQ",  # short url
        "dQw4w9WgXcQ",  # видео ID
        "https://www.youtube.com/channel/UCrV_cFYbUwpjSOPVJOjTufg",  # канал ID
        "https://www.youtube.com/c/Экстенсиональный",  # название канала
        "UCrV_cFYbUwpjSOPVJOjTufg",  # канал ID
        "@theextensional",  # пользователь
        "https://www.google.com/",  # некорректный URL
        "https://www.youtube.com/@theextensional/playlists",  # плейлисты
        "https://www.youtube.com/watch?v=9rnc23q-dUk&list=PLa2WHSYysn_FcroL3WX5hFh-BiwBvUMwn",  # видео из плейлиста
        "https://www.youtube.com/playlist?list=PLa2WHSYysn_FcroL3WX5hFh-BiwBvUMwn",  # плейлист
        "https://www.youtube.com/@theextensional/podcasts",  # подкасты
    ]

    for url in urls:
        try:
            download_subtitles(url)
        except ValueError as e:
            print(f"❌ URL: {url}, Ошибка: {str(e)}")
