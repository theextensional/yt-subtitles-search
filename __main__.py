#!/usr/bin/env python3
# *_* coding: utf-8 *_*

"""
yt-subtitles - консольная программа для поиска по субтитрам YouTube видео.
"""

import logging
import multiprocessing
import shutil
from collections import defaultdict
from os import listdir, path, system

from bs4 import BeautifulSoup
from yt_dlp import DownloadError, YoutubeDL

logging.basicConfig(format="%(levelname)s: %(message)s", level=logging.ERROR)

PRINT_LINES = 10

DIRECTORY = path.dirname(__file__)
DOWNLOAD_DIR = f"{DIRECTORY}/downloads"


def subtitles_download(video_info):
    ydl_opts = {
        "writesubtitles": True,
        "writeautomaticsub": True,
        "subtitleslangs": ["ru"],
        "subtitlesformat": "srv3",
        "outtmpl": f"{DOWNLOAD_DIR}/%(id)s",
        "skip_download": True,
        "quiet": True,
    }
    try:
        with YoutubeDL(ydl_opts) as ydl:
            ydl.download(video_info["url"])
    except DownloadError:
        logging.error("❌ DonwloadError")
        return


def search_query(queries: list[str] | str):
    if isinstance(queries, str):
        queries = [queries]

    files = listdir(DOWNLOAD_DIR)

    result = {}
    count = 0
    result = defaultdict(list)
    for query in queries:
        query_lower = query.lower()
        for file in files:
            yt_link = f'https://youtu.be/{file.split(".")[0]}'

            with open(f"{DOWNLOAD_DIR}/{file}", encoding="utf-8") as f:
                soup = BeautifulSoup(f, "lxml")
                paragraphes = soup.find_all("p")
                for paragraph in paragraphes:
                    if paragraph.get_text().find(query_lower) != -1:
                        result[query].append(
                            f'{yt_link}?t={paragraph.get("t")}ms'
                        )
                        count += 1

    return result, count


def get_videos_info(url: str, multi: int = multiprocessing.cpu_count() * 4):
    ydl_opts = {
        "extract_flat": True,
        "skip_download": True,
        "quiet": True,
    }
    with YoutubeDL(ydl_opts) as ydl:
        videos_info = ydl.extract_info(url=url, download=False)
        try:
            videos_info = videos_info["entries"]
            with multiprocessing.Pool(multi) as process:
                process.map(subtitles_download, videos_info)
        except KeyError:
            videos_info = ydl.extract_info(url=url, download=False)
            videos_info["url"] = videos_info["original_url"]
            subtitles_download(videos_info)


def print_result(result: dict, url: str):
    print(f"url: {url}")
    for key, value in result.items():
        print(f"По запросу '{key}' найдено {len(result[key])}:")
        print("\n".join(value))


def write_result(result: dict, count: int, url: str):
    file = f"{DOWNLOAD_DIR}/result.txt"
    with open(file, "w") as f:
        f.write(f"url: {url}\n")
        f.write(f"Всего результатов найдено: {count}\n")
        for key, value in result.items():
            f.write(f"По запросу '{key}' найдено {len(result[key])}:\n")
            f.writelines("\n".join(value))
            f.write("\n")

    print(f"Results successfully saved to file: {file}")
    return file


def open_resultfile(file):
    system(f"xdg-open {file}")


def result_output(result: dict, count: int, url: str, open: bool = False):
    if not count:
        print("Oops, nothing found.")
    elif count <= PRINT_LINES:  # print to console
        print_result(result, url)
    else:  # write to file
        file = write_result(result, count, url)
        if open:
            open_resultfile(file)


def clear_tmp():
    shutil.rmtree(DOWNLOAD_DIR, ignore_errors=True)


def main(argv):
    import argparse

    CLI = argparse.ArgumentParser()
    CLI.add_argument("url", help="Search URL")
    CLI.add_argument("query", nargs="+", help="Search query")
    CLI.add_argument(
        "-o", "--open", action="store_true", help="Open result file"
    )

    if len(argv) == 1:
        print("\nError! You must specify at least one option.\n")
        CLI.print_help()
    else:
        args = CLI.parse_args()
        config = vars(args)
        logging.info(config)

        clear_tmp()
        get_videos_info(args.url)
        result, count = search_query(args.query)
        result_output(result, count, args.url, open=args.open)


if "__main__" == __name__:
    import sys

    main(sys.argv)
