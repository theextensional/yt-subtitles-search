import os
import subprocess
import sys
from datetime import datetime

from constants import RESULT_DIR


def format_video_url(video_id: str, timestamp: int) -> str:
    return f"https://youtu.be/{video_id}?t={timestamp}ms"


def save_results_to_file(lines: list[str]) -> str:
    if not os.path.exists(RESULT_DIR):
        os.makedirs(RESULT_DIR)
    file_path = f"{RESULT_DIR}/{datetime.now().strftime('%Y-%m-%d_%H-%M-%S')}.txt"
    with open(file_path, "w") as file:
        file.write("\n".join(lines))
    return file_path


def open_file_path(file_path: str) -> None:
    if sys.platform == "win32":
        os.startfile(file_path)
    else:
        opener = "open" if sys.platform == "darwin" else "xdg-open"
        subprocess.call([opener, file_path])


def print_results(
    query: list[str], count: int, result: dict[str, list[int]], open_file: bool = False, per_page: int = 10
) -> None:
    lines = []
    header = f"По запросу `{' '.join(query)}` найдено {count}:"
    print(header)
    for video_id, matches in result.items():
        for timestamp in matches:
            lines.append(format_video_url(video_id, timestamp))
    for i, line in enumerate(lines[:per_page], start=1):
        print(f"{i:2}. {line}")
    if count > per_page:
        lines.insert(0, header)
        file_path = save_results_to_file(lines)
        print(f"Все результаты сохранены в {file_path}")
        if open_file:
            open_file_path(file_path)
