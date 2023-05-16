import re

REGEX_PATTERNS = {
    "channel_id": re.compile(r"^[a-zA-Z0-9_-]{24}$"),
    "channel_url": re.compile(r"(?:(?:https?:)?//)?(?:www\.)?youtube\.com/channel/([a-zA-Z0-9_-]+)"),
    "playlist_url": re.compile(r"(?:(?:https?:)?//)?(?:www\.)?youtube\.com/.*[?&]list=([a-zA-Z0-9_-]+)"),
    "video_url": re.compile(r"(?:(?:https?:)?//)?(?:www\.)?youtube\.com/watch\?v=([a-zA-Z0-9_-]+)"),
    "video_id": re.compile(r"^[a-zA-Z0-9_-]{11}$"),
    "short_url": re.compile(r"(?:(?:https?:)?//)?(?:www\.)?youtu.be/([a-zA-Z0-9_-]+)"),
    "channel_name": re.compile(r"(?:(?:https?:)?//)?(?:www\.)?youtube.com/c/([^/\s?]+)"),
    "user_name": re.compile(r"^(?:https?:\/\/(?:www\.)?youtube\.com\/)?(?:@)?([a-zA-Z0-9_-]+)$"),
    "playlists_url": re.compile(r"(?:(?:https?:)?//)?(?:www\.)?youtube\.com/([^/\s?]+)/playlists"),
    "streams_url": re.compile(r"(?:(?:https?:)?//)?(?:www\.)?youtube\.com/([^/\s?]+)/streams"),
    "shorts_url": re.compile(r"(?:(?:https?:)?//)?(?:www\.)?youtube\.com/([^/\s?]+)/shorts"),
    "videos_url": re.compile(r"(?:(?:https?:)?//)?(?:www\.)?youtube\.com/([^/\s?]+)/videos"),
}

DATA_TYPE_MAP = {
    "channel_name": "https://www.youtube.com/c/{}",
    "channel_url": "https://www.youtube.com/channel/{}",
    "channel_id": "https://www.youtube.com/channel/{}",
    "video_url": "https://www.youtube.com/watch?v={}",
    "video_id": "https://www.youtube.com/watch?v={}",
    "short_url": "https://www.youtube.com/watch?v={}",
    "user_name": "https://www.youtube.com/@{}",
    "playlist_url": "https://www.youtube.com/playlist?list={}",
    "playlists_url": "https://www.youtube.com/{}/playlists?view=1&sort=dd&shelf_id=0",
    "streams_url": "https://www.youtube.com/{}/streams",
    "shorts_url": "https://www.youtube.com/{}/shorts",
    "videos_url": "https://www.youtube.com/{}/videos",
}


def parse_youtube_url(url: str) -> tuple[str, str, str]:
    """
    Разбирает YouTube-ссылку и извлекает соответствующие данные.

    Аргументы:
        `url (str)`: YouTube-ссылка для разбора.

    Возвращает:
        `tuple[str, str, str]`: Кортеж, содержащий тип данных (`data_type`), ссылку на данные (`data_url`)
        и идентификатор (`data_id`) соответствующего элемента YouTube.
    """
    for data_type, pattern in REGEX_PATTERNS.items():
        if match := pattern.match(url):
            if data_type in ["channel_id", "video_id"]:
                data = DATA_TYPE_MAP.get(data_type, "").format(match.group(0))
                return (data_type, data, match.group(0))
            else:
                data = DATA_TYPE_MAP.get(data_type, "").format(match.group(1))
                return (data_type, data, match.group(1))

    raise ValueError("Некорректная YouTube-ссылка")


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
            if data := parse_youtube_url(url):
                data_type, data_url, _ = data
                print(f"✅ URL: {url}, Данные: `{data_type}` Link: {data_url}")
        except ValueError as e:
            print(f"❌ URL: {url}, Ошибка: {str(e)}")
