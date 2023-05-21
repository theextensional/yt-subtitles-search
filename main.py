import argparse
import os

from constants import DOWNLOAD_DIR
from utils import clean_text, download_subtitles, print_results, search_in_json


def search_subtitles(url: str, query: str, lang: str = "ru", open_file: bool = False) -> None:
    if not os.path.exists(DOWNLOAD_DIR):
        os.makedirs(DOWNLOAD_DIR)
    search_list = clean_text(query)
    subtitle_format = "json3"
    subtitle_files = download_subtitles(url, lang, subtitle_format)
    count, result = search_in_json(subtitle_files, search_list)
    print_results(search_list, count, result, open_file)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Search for a string in subtitles of a YouTube video.")
    parser.add_argument("url", type=str, help="YouTube video URL.")
    parser.add_argument("query", type=str, help="String to search for in subtitles.")
    parser.add_argument("--lang", type=str, default="ru", help="Language of subtitles (default: ru).")
    parser.add_argument(
        "--open",
        "-o",
        dest="open_file",
        action="store_true",
        help="Open result file (default: False).",
    )
    args = parser.parse_args()

    search_subtitles(args.url, args.query, args.lang, args.open_file)
